import numpy as np
import plotly.graph_objects as go
class Visualizer:
    """Class to create 2D and 3D visualizations."""

    # Constants
    COLORSCALE = [
        [0.0, 'gray'], # Placeholder value color
        [0.01, 'red'], # Start of actual data range
        [0.20, 'yellow'],
        [1.0, 'green'] # End of data range
    ]

    VALUE_RANGE = {"min": 13, "max": 20} # Need to use

    @staticmethod
    def extract_values(property_value):
        valid_data = property_value[property_value != -1]  # Exclude placeholder values
        vmin = np.min(valid_data) // 1 if not np.isnan(np.min(valid_data)) else 0 # Handle nan case
        vmax = np.max(valid_data) // 1 if not np.isnan(np.max(valid_data)) else 1 # Handle nan case, set default vmax if no valid data
        # vmin = VALUE_RANGE["min"]
        #vmax = VALUE_RANGE["max"]
        z_norm = np.linspace(0, 1, 50)

        return z_norm, vmin, vmax

    @staticmethod
    def create_3d_figure(property_value: np.ndarray, radius: float, rows: int, cols: int) -> go.Figure:
        """Generate 3D visualization."""
        theta = np.linspace(0, 2 * np.pi, cols)
        z = np.linspace(0, rows, rows)
        theta, z_grid = np.meshgrid(theta, z)

        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        angle = theta*(180/np.pi)
        z_norm, vmin, vmax = Visualizer.extract_values(property_value)

        hover_text = np.empty_like(x, dtype=object)
        for i in range(rows):
            for j in range(cols):
                hover_text[i, j] = f"Angle: {angle[i][j]//1} Row: {i}, Column: {j}, value: {property_value[i][j]}"

        fig = go.Figure(data=[go.Surface(
            z=z_grid,
            x=x,
            y=y,
            colorscale=Visualizer.COLORSCALE,
            surfacecolor=z_norm,
            colorbar=dict(
                title="Thickness %",
                tickformat=".0%",  # Formats tick labels as percentages
                x=-0.2             # Position of the first colorbar
            ),
            text=hover_text,
            hoverinfo='text'
        )])
        fig.add_trace(go.Surface(
            z=z_grid,
            x=x,
            y=y,
            cmin=vmin,
            cmax=vmax,
            colorscale=Visualizer.COLORSCALE,
            surfacecolor=property_value,
            colorbar=dict(title="Thickness (in mm)"),
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
    def create_2d_figure(df: np.ndarray, property_value: np.ndarray, rows: int, cols: int) -> go.Figure:
        """Generate 2D visualization."""
        theta = np.linspace(0, 2 * np.pi, cols)
        z = np.linspace(0, rows, rows)
        theta, z_grid = np.meshgrid(theta, z)

        z_norm, vmin, vmax = Visualizer.extract_values(property_value)

        hover_text = [[f"Row: {i}, Column: {j}, value: {property_value[i][j]}"
                      for j in range(cols)] for i in range(rows)]

        fig = go.Figure(data=[go.Heatmap(
            x=np.ravel(theta),
            y=np.ravel(z_grid),
            z=np.ravel(z_norm),
            colorscale=Visualizer.COLORSCALE,
            colorbar=dict(
                title="Thickness %",
                tickformat=".0%",  # Formats tick labels as percentages
                x=-0.2             # Position of the first colorbar
            ),
            text=hover_text,
            name="Data Points"
        )])

        fig.add_trace(go.Heatmap(
            x=np.ravel(theta),
            y=np.ravel(z_grid),
            z=np.ravel(property_value),
            colorscale=Visualizer.COLORSCALE,
            zmin=vmin,
            zmax=vmax,
            colorbar=dict(title="Thickness (in mm)"),
            text=hover_text,
            hoverinfo='text'
        ))

        fig.update_layout(
            title="2D Heatmap Visualization",
            xaxis=dict(title="Theta/Angle"),
            yaxis=dict(title="Height/Z")
        )

        return fig

