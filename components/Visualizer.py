import numpy as np
import plotly.graph_objects as go
import plotly.colors
import plotly.express as px

class Visualizer:
    """Class to create 2D and 3D visualizations with configurable value ranges."""

    @staticmethod
    def set_color_ranges(property_value, min_thickness, design_thickness):
        # Create custom colorscale
        zmin, zmax = min_thickness, design_thickness
        colors = px.colors.sequential.Turbo_r
        
        # Create colorscale with gray for -1
        custom_colorscale = [
            [0,"grey"],
            [0.01, colors[0]],
        ]
        
        for i in range(len(colors)):
            percentage = i / len(colors)
            next_percentage = (i + 1) / len(colors)
            
            if i < len(colors)-1:
                custom_colorscale.append([next_percentage, colors[i]])
                custom_colorscale.append([next_percentage, colors[i+1]])
        
        # Add the end of the colorscale
        custom_colorscale.append([1, colors[len(colors)-1]])

        # Find max value in actual data (excluding -1 values)
        max_data_value = np.max(property_value[property_value != -1]) if np.any(property_value != -1) else zmax
        
        # Create ticks for the colorbar
        base_ticks = 5  # Number of ticks in the 0-100% range
        
        # If max value exceeds zmax, add more ticks beyond 100%
        if max_data_value > zmax:
            # Calculate how many additional ticks needed (in 25% increments)
            percent_of_max = (max_data_value - zmin) / (zmax - zmin) * 100
            max_percent_rounded = int(np.ceil(percent_of_max / 25) * 25)  # Round up to nearest 25%
            
            # Generate tick values
            percent_ticks = list(range(0, 101, 25)) + list(range(100, max_percent_rounded + 1, 25))
            tickvals = [zmin + (p/100) * (zmax - zmin) for p in percent_ticks]
            ticktext = [f"{val:.1f} ({p}%)" for val, p in zip(tickvals, percent_ticks)]
        else:
            # Standard ticks if data is within range
            num_ticks = base_ticks
            tickvals = [zmin + (i * (zmax - zmin) / (num_ticks-1)) for i in range(num_ticks)]
            ticktext = [f"{tickvals[i]:.1f} ({i * 100/(num_ticks-1):.0f}%)" for i in range(num_ticks)]
        
        return custom_colorscale, zmin, zmax, tickvals, ticktext, max_data_value

    @staticmethod
    def create_3d_figure(property_value: np.ndarray, radius: float, rows: int, cols: int,
                        thickness: float, threshold_percentage: float) -> go.Figure:
        """Generate 3D visualization with configurable value ranges."""
        # Add second surface for actual values
        theta = np.linspace(0, 2 * np.pi, cols)
        z = np.linspace(0, rows, rows)
        theta, z_grid = np.meshgrid(theta, z)

        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        angle = theta*(180/np.pi)

        # Create hover text
        hover_text = np.empty_like(x, dtype=object)
        for i in range(rows):
            for j in range(cols):
                value = property_value[i][j]
                if value == -1: 
                    status = "Not Measured"
                else: 
                    status = "Above threshold"
                hover_text[i, j] = (f"Angle: {angle[i][j]//1} "
                                    f"Row: {i}, Column: {j}, "
                                    f"Value: {value:.2f}, "
                                    f"Status: {status}")
        
        custom_colorscale, zmin, zmax, tickvals, ticktext, max_data_value = Visualizer.set_color_ranges(property_value)
        
        
        fig = go.Figure()
        fig.add_trace(go.Surface(
            z=z_grid,
            x=x,
            y=y,
            cmin=zmin,
            cmax=max(zmax, max_data_value),  # Ensure colorbar covers all data
            colorscale=custom_colorscale,
            surfacecolor=property_value,
            colorbar=dict(
                title="Property Values",
                tickvals=tickvals,
                ticktext=ticktext,
                tickmode="array"
            ),
            text=hover_text,
            hoverinfo='text'
        ))
        
        # Add grid lines
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

        return fig

    @staticmethod
    def create_2d_figure(df: np.ndarray, property_value: np.ndarray, rows: int, cols: int, 
                    thickness: float) -> go.Figure:
        """Generate 2D visualization with configurable value ranges."""
        theta = np.linspace(0, 2 * np.pi, cols)
        z = np.linspace(0, rows, rows)
        theta, z_grid = np.meshgrid(theta, z)
        hover_text = []
        
        for i in range(rows):
            row_text = []
            for j in range(cols):
                value = property_value[i][j]
                row_text.append(f"Row: {i}, Column: {j}, Value: {value:.2f}")
            hover_text.append(row_text)
        
        custom_colorscale, zmin, zmax, tickvals, ticktext, max_data_value = Visualizer.set_color_ranges(property_value)
    
        
        # Create figure
        fig = go.Figure()
        fig.add_trace(go.Heatmap(
            x=np.ravel(theta),
            y=np.ravel(z_grid),
            z=np.ravel(property_value),
            zmin=zmin,
            zmax=max(zmax, max_data_value),  # Ensure colorbar covers all data
            colorscale=custom_colorscale,
            colorbar=dict(
                title="Property Values",
                tickvals=tickvals,
                ticktext=ticktext,
                tickmode="array"
            ),
            text=np.ravel(hover_text),
            hoverinfo='text'
        ))
        
        return fig