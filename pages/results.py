# pages/results.py - Results page module without graphs
import dash
from dash import dcc, html, callback, Input, Output, State, dash_table
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple

# Import the Visualizer class
# from visualizer import Visualizer

class ResultAnalyzer:
    """Class to analyze visualization data and calculate statistics."""
    
    # Color thresholds based on the COLORSCALE from Visualizer
    RED_THRESHOLD = 0.01
    YELLOW_THRESHOLD = 0.20
    GREEN_THRESHOLD = 0.50
    
    @staticmethod
    def calculate_color_ratios(property_value: np.ndarray) -> Dict[str, float]:
        """Calculate the ratio of green, yellow, and red areas."""
        # Remove placeholder values (-1)
        valid_data = property_value[property_value != -1]
        total_cells = len(valid_data)
        
        if total_cells == 0:
            return {"red": 0, "yellow": 0, "green": 0}
        
        # Normalize the data between 0 and 1
        valid_min = np.min(valid_data)
        valid_max = np.max(valid_data)
        range_diff = valid_max - valid_min
        
        if range_diff == 0:  # Handle case where all values are the same
            normalized = np.zeros_like(valid_data)
        else:
            normalized = (valid_data - valid_min) / range_diff
        
        # Count cells in each color range
        red_count = np.sum((normalized >= 0) & (normalized < ResultAnalyzer.YELLOW_THRESHOLD))
        yellow_count = np.sum((normalized >= ResultAnalyzer.YELLOW_THRESHOLD) & (normalized < ResultAnalyzer.GREEN_THRESHOLD))
        green_count = np.sum(normalized >= ResultAnalyzer.GREEN_THRESHOLD)
        
        # Calculate ratios
        ratios = {
            "red": red_count / total_cells,
            "yellow": yellow_count / total_cells,
            "green": green_count / total_cells
        }
        
        return ratios
    
    @staticmethod
    def find_red_areas(property_value: np.ndarray, angle_matrix: np.ndarray) -> List[Dict]:
        """Find locations of red areas and return as a list of dictionaries for the table."""
        rows, cols = property_value.shape
        
        # Remove placeholder values (-1)
        valid_data = property_value.copy()
        valid_mask = valid_data != -1
        
        if not np.any(valid_mask):
            return []
        
        # Normalize the data between 0 and 1
        valid_min = np.min(valid_data[valid_mask])
        valid_max = np.max(valid_data[valid_mask])
        range_diff = valid_max - valid_min
        
        if range_diff == 0:  # Handle case where all values are the same
            normalized = np.zeros_like(valid_data)
        else:
            normalized = np.zeros_like(valid_data)
            normalized[valid_mask] = (valid_data[valid_mask] - valid_min) / range_diff
        
        # Find red areas
        red_areas = []
        for i in range(rows):
            for j in range(cols):
                if valid_mask[i, j] and normalized[i, j] < ResultAnalyzer.YELLOW_THRESHOLD:
                    red_areas.append({
                        "Row": i,
                        "Column": j,
                        "Angle": int(angle_matrix[i, j]),
                        "Value": property_value[i, j],
                        "Severity": "High" if normalized[i, j] < 0.1 else "Medium"
                    })
        
        # Sort by severity and value
        red_areas.sort(key=lambda x: (0 if x["Severity"] == "High" else 1, x["Value"]))
        
        return red_areas

# Define the layout for the results page
layout = html.Div([
    html.Div([
        html.H3("Results and Analysis", style={"text-align": "center", "font-size": "18px"}),
        html.Div(
            dcc.Link(
                'Back to view',
                href='/view',
                style={
                    "padding": "10px 20px",
                    "fontSize": "18px",
                    "backgroundColor": "#6a0dad",
                    "color": "white",
                    "border": "none",
                    "cursor": "pointer",
                    "borderRadius": "5px",
                    "fontWeight": "bold",
                    "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                    "textDecoration": "none",
                    "display": "inline-block"
                }
            ),
            style={"marginTop": "20px"}
        )
    ], className="header"),
    
    html.Div([
        html.Div([
            html.Div([
                html.H3("Thickness Statistics"),
                html.Div(id='thickness-stats', className="p-3 border rounded")
            ], className='col-md-6'),
            
            html.Div([
                html.H3("Color Distribution"),
                html.Div(id='color-distribution', className="p-3 border rounded")
            ], className='col-md-6'),
        ], className='row mb-4'),
        
        html.Div([
            html.H3("Critical Areas (Red Zones)", className="text-center"),
            dash_table.DataTable(
                id='red-areas-table',
                columns=[
                    {'name': 'Row', 'id': 'Row'},
                    {'name': 'Column', 'id': 'Column'},
                    {'name': 'Angle (°)', 'id': 'Angle'},
                    {'name': 'Thickness (mm)', 'id': 'Value', 'type': 'numeric', 'format': {'specifier': '.2f'}},
                    {'name': 'Severity', 'id': 'Severity'}
                ],
                style_data_conditional=[
                    {
                        'if': {'filter_query': '{Severity} = "High"'},
                        'backgroundColor': '#ffcccc',
                        'color': 'black'
                    },
                    {
                        'if': {'filter_query': '{Severity} = "Medium"'},
                        'backgroundColor': '#ffffcc',
                        'color': 'black'
                    }
                ],
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                },
                page_size=10,
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                # export_format="csv",
            )
        ], className='row'),
        
        html.Div([
            html.H3("Area Coverage Summary", className="text-center mt-4"),
            dash_table.DataTable(
                id='area-summary-table',
                columns=[
                    {'name': 'Color Category', 'id': 'category'},
                    {'name': 'Coverage (%)', 'id': 'coverage', 'type': 'numeric', 'format': {'specifier': '.1%'}},
                    {'name': 'Cell Count', 'id': 'count', 'type': 'numeric'},
                    {'name': 'Average Thickness (mm)', 'id': 'avg_thickness', 'type': 'numeric', 'format': {'specifier': '.2f'}}
                ],
                style_data_conditional=[
                    {
                        'if': {'filter_query': '{category} = "Red"'},
                        'backgroundColor': '#ffcccc',
                        'color': 'black'
                    },
                    {
                        'if': {'filter_query': '{category} = "Yellow"'},
                        'backgroundColor': '#ffffcc',
                        'color': 'black'
                    },
                    {
                        'if': {'filter_query': '{category} = "Green"'},
                        'backgroundColor': '#ccffcc',
                        'color': 'black'
                    }
                ],
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                }
            )
        ], className='row mt-4'),
    ], className="content"),
],style={
            "width": "95%",
            "max-width": "750px",
            "margin": "20px auto",
            "padding": "15px",
            "border": "1px solid #ccc",
            "border-radius": "8px",
            "box-sizing": "border-box",
            "background-color": "#fefefe",
            "box-shadow": "0 2px 5px rgba(0,0,0,0.1)",
            '@media (max-width: 768px)': {
                'width': '98%',
                'padding': '10px',
                'margin': '10px auto',
            },
            '@media (min-width: 769px)': {
                'width': '75%',
            }
            })

def register_callbacks(app):
    
    # Data processing and analysis callbacks
    @app.callback(
        [Output('thickness-stats', 'children'),
         Output('color-distribution', 'children'),
         Output('red-areas-table', 'data'),
         Output('area-summary-table', 'data')],
        Input('prop-store', 'data')
    )
    def update_results(stored_data):
        if not stored_data:
            # Return empty results if no data
            empty_stats = html.Div("No data available")
            empty_distribution = html.Div("No data available")
            return empty_stats, empty_distribution, [], []
        
        # Extract data from the store
        property_value = np.array(stored_data.get('property_value', []))
        
        if property_value.size == 0:
            empty_stats = html.Div("No data available")
            empty_distribution = html.Div("No data available")
            return empty_stats, empty_distribution, [], []
        
        rows, cols = property_value.shape
        
        # Create angle matrix
        theta = np.linspace(0, 2 * np.pi, cols)
        z = np.linspace(0, rows, rows)
        theta_grid, z_grid = np.meshgrid(theta, z)
        angle_matrix = theta_grid * (180/np.pi)
        
        # Calculate color ratios
        color_ratios = ResultAnalyzer.calculate_color_ratios(property_value)
        
        # Calculate thickness statistics
        valid_data = property_value[property_value != -1]
        valid_mask = property_value != -1
        normalized = np.zeros_like(property_value)
        
        valid_min = np.min(valid_data)
        valid_max = np.max(valid_data)
        range_diff = valid_max - valid_min
        
        if range_diff != 0:
            normalized[valid_mask] = (property_value[valid_mask] - valid_min) / range_diff
        
        # Get data for each color category
        red_mask = (normalized < ResultAnalyzer.YELLOW_THRESHOLD) & valid_mask
        yellow_mask = (normalized >= ResultAnalyzer.YELLOW_THRESHOLD) & (normalized < ResultAnalyzer.GREEN_THRESHOLD) & valid_mask
        green_mask = (normalized >= ResultAnalyzer.GREEN_THRESHOLD) & valid_mask
        
        red_count = np.sum(red_mask)
        yellow_count = np.sum(yellow_mask)
        green_count = np.sum(green_mask)
        total_count = red_count + yellow_count + green_count
        
        # Calculate average thickness per category
        red_avg = np.mean(property_value[red_mask]) if red_count > 0 else 0
        yellow_avg = np.mean(property_value[yellow_mask]) if yellow_count > 0 else 0
        green_avg = np.mean(property_value[green_mask]) if green_count > 0 else 0
        
        # Create thickness statistics table
        thickness_stats = html.Div([
            html.Table([
                html.Thead(html.Tr([
                    html.Th("Statistic"),
                    html.Th("Value")
                ])),
                html.Tbody([
                    html.Tr([html.Td("Min Thickness:"), html.Td(f"{np.min(valid_data):.2f} mm")]),
                    html.Tr([html.Td("Max Thickness:"), html.Td(f"{np.max(valid_data):.2f} mm")]),
                    html.Tr([html.Td("Average Thickness:"), html.Td(f"{np.mean(valid_data):.2f} mm")]),
                    html.Tr([html.Td("Median Thickness:"), html.Td(f"{np.median(valid_data):.2f} mm")]),
                    html.Tr([html.Td("Standard Deviation:"), html.Td(f"{np.std(valid_data):.2f} mm")]),
                    html.Tr([html.Td("Total Cells:"), html.Td(f"{total_count}")]),
                ])
            ], className="table table-striped")
        ])
        
        # Create color distribution table
        color_distribution = html.Div([
            html.Div([
                html.Div(style={"backgroundColor": "red", "width": f"{color_ratios['red']*100}%", "height": "30px", "float": "left", "textAlign": "center", "color": "white"}, children=f"{color_ratios['red']:.1%}"),
                html.Div(style={"backgroundColor": "yellow", "width": f"{color_ratios['yellow']*100}%", "height": "30px", "float": "left", "textAlign": "center"}, children=f"{color_ratios['yellow']:.1%}"),
                html.Div(style={"backgroundColor": "green", "width": f"{color_ratios['green']*100}%", "height": "30px", "float": "left", "textAlign": "center", "color": "white"}, children=f"{color_ratios['green']:.1%}"),
            ], style={"width": "100%", "overflow": "hidden", "marginBottom": "15px"}),
            html.Table([
                html.Thead(html.Tr([
                    html.Th("Color Category"),
                    html.Th("Percentage"),
                    html.Th("Cell Count")
                ])),
                html.Tbody([
                    html.Tr([
                        html.Td("Red", style={"backgroundColor": "#ffcccc"}), 
                        html.Td(f"{color_ratios['red']:.1%}"),
                        html.Td(f"{red_count}")
                    ]),
                    html.Tr([
                        html.Td("Yellow", style={"backgroundColor": "#ffffcc"}), 
                        html.Td(f"{color_ratios['yellow']:.1%}"),
                        html.Td(f"{yellow_count}")
                    ]),
                    html.Tr([
                        html.Td("Green", style={"backgroundColor": "#ccffcc"}), 
                        html.Td(f"{color_ratios['green']:.1%}"),
                        html.Td(f"{green_count}")
                    ]),
                ])
            ], className="table table-striped", )
        ])
        
        # Find red areas for table
        red_areas = ResultAnalyzer.find_red_areas(property_value, angle_matrix)
        
        # Create summary table data
        area_summary = [
            {"category": "Red", "coverage": color_ratios['red'], "count": red_count, "avg_thickness": red_avg},
            {"category": "Yellow", "coverage": color_ratios['yellow'], "count": yellow_count, "avg_thickness": yellow_avg},
            {"category": "Green", "coverage": color_ratios['green'], "count": green_count, "avg_thickness": green_avg},
            {"category": "Total", "coverage": 1.0, "count": total_count, "avg_thickness": np.mean(valid_data)}
        ]
        
        return thickness_stats, color_distribution, red_areas, area_summary