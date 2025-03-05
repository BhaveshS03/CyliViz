import numpy as np
import plotly.graph_objects as go

class Visualizer:
    """Class to create 2D and 3D visualizations with configurable value ranges."""

    @staticmethod
    def set_color_ranges(property_value, nominal_thickness, design_thickness, threshold_thickness):
        """
        Set custom color ranges based on actual property values.
        
        Args:
            property_value (np.ndarray): Input data array
            nominal_thickness :
            design_thickness : 
            threshold_thickness :
        
        Returns:
            list: Configured color scale with ranges
            float: Minimum value in the dataset
            float: Maximum value in the dataset
        """
        # Remove placeholder and invalid values
        valid_data = property_value[property_value != -1]

        # Determine data min and max if not explicitly specified in ranges
        data_min = np.min(valid_data)-1 if len(valid_data) > 0 else 0
        data_max = np.max(valid_data) if len(valid_data) > 0 else 1
        

        nominal_thickness = min(data_max,nominal_thickness)
        threshold_thickness = min(data_max,threshold_thickness)
        red_range=[data_min, threshold_thickness]
        yellow_range=[threshold_thickness, nominal_thickness]
        green_range=[nominal_thickness, design_thickness]

        # Normalize ranges for color mapping
        def normalize_value(val):
            return float((val - data_min) / (data_max - data_min))
        
        colorscale = [
            [0.0, 'gray'],  # Placeholder value color
            [0.01,'red'],
            [normalize_value(yellow_range[0]), 'yellow'],
            [normalize_value(yellow_range[1]), 'yellow'],
            [1, 'green']
        ]

        return colorscale, data_min, data_max

    @staticmethod
    def create_3d_figure(property_value: np.ndarray, radius: float, rows: int, cols: int,nominal_thickness: float, design_thickness: float, threshold_thickness: float) -> go.Figure:
        """Generate 3D visualization with configurable value ranges."""
        # Set color scale and get data ranges
        colorscale, vmin, vmax = Visualizer.set_color_ranges(
            property_value, nominal_thickness, design_thickness, threshold_thickness
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

        # Hover text generation
        hover_text = np.empty_like(x, dtype=object)
        for i in range(rows):
            for j in range(cols):
                hover_text[i, j] = (f"Angle: {angle[i][j]//1} "
                                    f"Row: {i}, Column: {j}, "
                                    f"Value: {property_value[i][j]:.2f}")

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

        # Update layout
        fig.update_layout(
            scene=dict(
                xaxis_title="X",
                yaxis_title="Angular Position (Theta)",
                zaxis_title='Height/Rows Z'
            ),
            title=f"3D Heatmap Visualization, Cylinder with {rows} Rows and {cols} Columns"
        )

        return fig

    @staticmethod
    def create_2d_figure(df: np.ndarray, property_value: np.ndarray, rows: int, cols: int,nominal_thickness: float, design_thickness: float, threshold_thickness: float) -> go.Figure:
        """Generate 2D visualization with configurable value ranges."""
        # Set color scale and get data ranges
        colorscale, vmin, vmax = Visualizer.set_color_ranges(
            property_value, nominal_thickness, design_thickness, threshold_thickness
        )

        # Existing 2D figure creation logic
        theta = np.linspace(0, 2 * np.pi, cols)
        z = np.linspace(0, rows, rows)
        theta, z_grid = np.meshgrid(theta, z)

        # Normalize values for color mapping
        z_norm = (property_value - vmin) / (vmax - vmin)
        z_norm = np.clip(z_norm, 0, 1)

        # Hover text generation
        hover_text = [[f"Row: {i}, Column: {j}, Value: {property_value[i][j]:.2f}"
                      for j in range(cols)] for i in range(rows)]

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
            text=hover_text,
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
            text=hover_text,
            hoverinfo='text'
        ))

        # Update layout
        fig.update_layout(
            title="2D Heatmap Visualization",
            xaxis=dict(title="Theta/Angle"),
            yaxis=dict(title="Height/Z")
        )

        return fig