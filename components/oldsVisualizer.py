import numpy as np
import plotly.graph_objects as go
import plotly.colors


class Visualizer:
    """Class to create 2D and 3D visualizations with configurable value ranges."""

    @staticmethod
    def set_color_ranges(property_value, thickness, threshold_percentage):
        """
        Set custom color ranges based on actual property values.
        
        Args:
            property_value (np.ndarray): Input data array
            nominal_thickness (float): Chosen thickness value
            design_thickness (float): Design thickness value
            threshold_percentage (float): Percentage of nominal thickness to use as threshold (0-100)
        
        Returns:
            list: Configured color scale with ranges
            float: Minimum value in the dataset
            float: Maximum value in the dataset
            str: Warning message if threshold exceeds max value, otherwise empty string
            float: Adjusted threshold value if it exceeded max value
        """
        # Remove placeholder and invalid values
        valid_data = property_value[property_value != -1]

        # Determine data min and max if not explicitly specified in ranges
        data_min = np.min(valid_data)-1 if len(valid_data) > 0 else 0
        data_max = np.max(valid_data) if len(valid_data) > 0 else 1
        
        # Calculate threshold value based on percentage of nominal thickness
        threshold_value = thickness * (threshold_percentage / 100.0)
        
        # Check if threshold exceeds maximum value
        warning_message = ""
        if threshold_value > data_max:
            warning_message = f"Warning: Calculated threshold value ({threshold_value:.2f}) exceeds maximum data value ({data_max:.2f}). Threshold has been adjusted to maximum value."
            threshold_value = data_max

        # Normalize ranges for color mapping
        def normalize_value(val):
            f = float((val - data_min) / (data_max - data_min))
            return f if f>0 else 0.01
        
        # Below threshold is red, above threshold is blue
        normalized_threshold = normalize_value(threshold_value)
        if normalized_threshold<1:
            colorscale = [
                [0,'grey'],
                [0.01, '#67001f'],                # dark red
                [normalized_threshold, '#f4a582'],  # immediately start transitioning above threshold
                [normalized_threshold , '#92c5de'], # mid blue
                [1.0, '#2166ac'] # dark blue
            ]
        else:
            colorscale = [
                [0,'grey'],
                [0.01, '#67001f'],                # dark red
                [normalized_threshold, '#f4a582'],  # immediately start transitioning above threshold
                [normalized_threshold , '#92c5de'], # mid blue
            ]
        return colorscale, data_min, data_max, warning_message, threshold_value

    @staticmethod
    def create_3d_figure(property_value: np.ndarray, radius: float, rows: int, cols: int,
                        thickness: float,threshold_percentage: float) -> go.Figure:
        """Generate 3D visualization with configurable value ranges."""
        # Set color scale and get data ranges
        colorscale, vmin, vmax, warning_message, adjusted_threshold = Visualizer.set_color_ranges(
            property_value, thickness, threshold_percentage
        )

        # Existing 3D figure creation logic
        theta = np.linspace(0, 2 * np.pi, cols)
        z = np.linspace(0, rows, rows)
        theta, z_grid = np.meshgrid(theta, z)

        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        angle = theta*(180/np.pi)

        # Normalize values for color mapping
        z_norm = (property_value - vmin) / (vmax - vmin)
        z_norm = np.clip(z_norm, 0, 1)

        # Use adjusted threshold value for hover text
        threshold_value = adjusted_threshold

        # Hover text generation
        hover_text = np.empty_like(x, dtype=object)
        for i in range(rows):
            for j in range(cols):
                value = property_value[i][j]
                if value < threshold_value:
                    status = "Below threshold" 
                elif value==-1: status = "Not Measured"
                else:
                    status = "Above threshold"
                hover_text[i, j] = (f"Angle: {angle[i][j]//1} "
                                    f"Row: {i}, Column: {j}, "
                                    f"Value: {value:.2f}, "
                                    f"Status: {status}")

        # Create figure
        fig = go.Figure()

        # Add first surface for normalized view
        fig.add_trace(go.Surface(
            z=z_grid,
            x=x,
            y=y,
            colorscale=colorscale,
            surfacecolor=z_norm,
            colorbar=dict(
                title="Normalized Values",
                tickformat=".2f",
                x=-0.2
            ),
            text=hover_text,
            hoverinfo='text'
        ))

        # Add second surface for actual values
        fig.add_trace(go.Surface(
            z=z_grid,
            x=x,
            y=y,
            cmin=vmin,
            cmax=vmax,
            colorscale=colorscale,
            surfacecolor=property_value,
            colorbar=dict(title="Property Values"),
            text=hover_text,
            hoverinfo='text'
        ))

        # Add grid lines (same as previous implementation)
        for i in range(rows):
            fig.add_trace(go.Scatter3d(
                x=x[i, :], y=y[i, :], z=np.full(cols, z[i]),
                mode='lines', line=dict(color='black', width=2),
                showlegend=False
            ))

        for j in range(cols):
            fig.add_trace(go.Scatter3d(
                x=x[:, j], y=y[:, j], z=z,
                mode='lines', line=dict(color='black', width=1),
                showlegend=False
            ))

        # Update layout with warning message if present
        title = f"3D Heatmap Visualization, Cylinder with {rows} Rows and {cols} Columns<br>"
        title += f"Red: Below {threshold_percentage}% of Chosen Thickness, Blue: Above"
        
        if warning_message:
            title += f"<br>{warning_message}"

        fig.update_layout(
            scene=dict(
                xaxis_title="X",
                yaxis_title="Angular Position (Theta)",
                zaxis_title='Height/Rows Z'
            ),
            title=title
        )

        return fig

    @staticmethod
    def create_2d_figure(df: np.ndarray, property_value: np.ndarray, rows: int, cols: int,
                        thickness: float, threshold_percentage: float) -> go.Figure:
        """Generate 2D visualization with configurable value ranges."""
        # Set color scale and get data ranges
        colorscale, vmin, vmax, warning_message, adjusted_threshold = Visualizer.set_color_ranges(
            property_value, thickness, threshold_percentage
        )

        # Existing 2D figure creation logic
        theta = np.linspace(0, 2 * np.pi, cols)
        z = np.linspace(0, rows, rows)
        theta, z_grid = np.meshgrid(theta, z)

        # Normalize values for color mapping
        z_norm = (property_value - vmin) / (vmax - vmin)
        z_norm = np.clip(z_norm, 0, 1)

        # Use adjusted threshold value for hover text
        threshold_value = adjusted_threshold

        # Hover text generation with threshold indication
        hover_text = []
        for i in range(rows):
            row_text = []
            for j in range(cols):
                value = property_value[i][j]
                status = "Below threshold" if value < threshold_value else "Above threshold"
                row_text.append(f"Row: {i}, Column: {j}, Value: {value:.2f}, Status: {status}")
            hover_text.append(row_text)

        # Create figure
        fig = go.Figure()

        # Add first heatmap for normalized view
        fig.add_trace(go.Heatmap(
            x=np.ravel(theta),
            y=np.ravel(z_grid),
            z=np.ravel(z_norm),
            colorscale=colorscale,
            colorbar=dict(
                title="Normalized Values",
                tickformat=".2f",
                x=-0.2
            ),
            text=np.ravel(hover_text),
            name="Normalized Data Points"
        ))

        # Add second heatmap for actual values
        fig.add_trace(go.Heatmap(
            x=np.ravel(theta),
            y=np.ravel(z_grid),
            z=np.ravel(property_value),
            colorscale=colorscale,
            zmin=vmin,
            zmax=vmax,
            colorbar=dict(title="Property Values"),
            text=np.ravel(hover_text),
            hoverinfo='text'
        ))

        # Update layout with warning message if present
        title = f"2D Heatmap Visualization<br>"
        title += f"Red: Below {threshold_percentage}% of Chosen Thickness :{thickness}mm, Blue: Above"
        
        if warning_message:
            title += f"<br>{warning_message}"

        fig.update_layout(
            title=title,
            xaxis=dict(title="Theta/Angle"),
            yaxis=dict(title="Height/Z")
        )

        return fig