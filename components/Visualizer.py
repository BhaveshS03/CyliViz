import numpy as np
import plotly.graph_objects as go
import plotly.colors
import plotly.express as px
from components.Mapper import Mapper

class Visualizer:
    """Class to create 2D and 3D visualizations with configurable value ranges."""

    @staticmethod
    def set_color_ranges(property_value, min_thickness, design_thickness, percent_gap=25):
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
        
        # Create ticks for the colorbar based on percent_gap
        if max_data_value > zmax:
            # Calculate how many additional ticks needed (based on percent_gap)
            percent_of_max = (max_data_value - zmin) / (zmax - zmin) * 100
            max_percent_rounded = int(np.ceil(percent_of_max / percent_gap) * percent_gap)
            
            # Generate all percentages from 0 to max_percent_rounded in steps of percent_gap
            percent_ticks = list(range(0, max_percent_rounded + 1, percent_gap))
            
            # Add 100% if it's not already included and max > 100%
            if 100 not in percent_ticks and max_percent_rounded > 100:
                percent_ticks.append(100)
                percent_ticks.sort()
        else:
            # Standard ticks if data is within range
            percent_ticks = list(range(0, 101, percent_gap))
        
        # Calculate tick values and text
        tickvals = [zmin + (p/100) * (zmax - zmin) for p in percent_ticks]
        ticktext = [f"{val:.1f} ({p}%)" for val, p in zip(tickvals, percent_ticks)]
        
        
        return custom_colorscale, zmin, zmax, tickvals, ticktext, max_data_value

    @staticmethod
    def create_3d_figure(property_value: np.ndarray, radius: float, rows: int, cols: int,
                        thickness: float, threshold_thickness: float) -> go.Figure:
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
                                    f"Value: {value:.2f}")
        
        custom_colorscale, zmin, zmax, tickvals, ticktext, max_data_value = Visualizer.set_color_ranges(property_value,threshold_thickness,thickness)
        
        
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
                    thickness: float, threshold_thickness: float) -> go.Figure:
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
        
        custom_colorscale, zmin, zmax, tickvals, ticktext, max_data_value = Visualizer.set_color_ranges(property_value, threshold_thickness,thickness)
    
        
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