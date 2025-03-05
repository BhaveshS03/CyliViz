# pages/results.py - Results page module without graphs
import dash
from dash import dcc, html, callback, Input, Output, State, dash_table
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple

# Import the Visualizer class
# from visualizer import Visualizer

import numpy as np
from typing import Dict, List, Optional

# class ResultAnalyzer:
#     """Class to analyze visualization data and calculate statistics with configurable thresholds."""
    
#     @staticmethod
#     def set_color_thresholds(
#         property_value: np.ndarray, 
#         red_range: Optional[tuple] = None, 
#         yellow_range: Optional[tuple] = None, 
#         green_range: Optional[tuple] = None
#     ) -> Dict[str, float]:
#         """
#         Set color thresholds based on input ranges or data distribution.
        
#         Args:
#             property_value (np.ndarray): Input data array
#             red_range (tuple, optional): Range for red category (min, max)
#             yellow_range (tuple, optional): Range for yellow category (min, max)
#             green_range (tuple, optional): Range for green category (min, max)
        
#         Returns:
#             Dict with normalized thresholds for red, yellow, green
#         """
#         # Remove placeholder values
#         valid_data = property_value[property_value != -1]
        
#         if len(valid_data) == 0:
#             return {"red": 0, "yellow": 0.2, "green": 0.5}
        
#         # Determine data min and max
#         data_min = np.min(valid_data)
#         data_max = np.max(valid_data)
        
#         # Normalize ranges if provided, otherwise use default distribution
#         def normalize_range(input_range):
#             if input_range is None:
#                 return None
#             norm_min = (input_range[0] - data_min) / (data_max - data_min)
#             norm_max = (input_range[1] - data_min) / (data_max - data_min)
#             return (norm_min, norm_max)
        
#         norm_red_range = normalize_range(red_range)
#         norm_yellow_range = normalize_range(yellow_range)
#         norm_green_range = normalize_range(green_range)
        
#         # Default thresholds if not fully specified
#         if norm_red_range is None:
#             norm_red_range = (0, 0.2)
#         if norm_yellow_range is None:
#             norm_yellow_range = (0.2, 0.5)
#         if norm_green_range is None:
#             norm_green_range = (0.5, 1.0)
        
#         # Validate ranges
#         # if not (0 <= norm_red_range[0] < norm_red_range[1] <= 
#         #         norm_yellow_range[0] < norm_yellow_range[1] <= 
#         #         norm_green_range[0] < norm_green_range[1] <= 1.0):
#         #     raise ValueError("Invalid color ranges. Ensure ranges are in ascending order and within 0-1.")
#         print(norm_red_range[0],":" , norm_red_range[1] ,":",
#                 norm_yellow_range[0] ,":", norm_yellow_range[1] , ":",
#                 norm_green_range[0] ,":" ,norm_green_range[1] )
#         return {
#             "red": norm_red_range[1],
#             "yellow": norm_yellow_range[1],
#             "green": 1
#         }
    
#     @staticmethod
#     def calculate_color_ratios(
#         property_value: np.ndarray, 
#         red_range: Optional[tuple] = None, 
#         yellow_range: Optional[tuple] = None, 
#         green_range: Optional[tuple] = None
#     ) -> Dict[str, float]:
#         """
#         Calculate the ratio of green, yellow, and red areas with configurable thresholds.
        
#         Args:
#             property_value (np.ndarray): Input data array
#             red_range (tuple, optional): Range for red category
#             yellow_range (tuple, optional): Range for yellow category
#             green_range (tuple, optional): Range for green category
        
#         Returns:
#             Dict with color ratios
#         """
#         # Remove placeholder values
#         valid_data = property_value[property_value != -1]
#         total_cells = len(valid_data)
        
#         if total_cells == 0:
#             return {"red": 0, "yellow": 0, "green": 0}
        
#         # Get normalized thresholds
#         thresholds = ResultAnalyzer.set_color_thresholds(
#             property_value, red_range, yellow_range, green_range
#         )
        
#         # Normalize the data between 0 and 1
#         valid_min = np.min(valid_data)
#         valid_max = np.max(valid_data)
#         range_diff = valid_max - valid_min
        
#         if range_diff == 0:  # Handle case where all values are the same
#             normalized = np.zeros_like(valid_data)
#         else:
#             normalized = (valid_data - valid_min) / range_diff
        
#         # Count cells in each color range
#         red_count = np.sum(normalized < thresholds["red"])
#         yellow_count = np.sum((normalized >= thresholds["red"]) & (normalized < thresholds["yellow"]))
#         green_count = np.sum(normalized >= thresholds["yellow"])
        
#         # Calculate ratios
#         ratios = {
#             "red": red_count / total_cells,
#             "yellow": yellow_count / total_cells,
#             "green": green_count / total_cells
#         }
        
#         return ratios
    
#     @staticmethod
#     def find_red_areas(
#         property_value: np.ndarray, 
#         angle_matrix: np.ndarray, 
#         red_range: Optional[tuple] = None
#     ) -> List[Dict]:
#         """
#         Find locations of red areas with configurable red threshold.
        
#         Args:
#             property_value (np.ndarray): Input data array
#             angle_matrix (np.ndarray): Matrix of corresponding angles
#             red_range (tuple, optional): Range defining red areas
        
#         Returns:
#             List of dictionaries with red area details
#         """
#         rows, cols = property_value.shape
        
#         # Remove placeholder values
#         valid_data = property_value.copy()
#         valid_mask = valid_data != -1
        
#         if not np.any(valid_mask):
#             return []
        
#         # Normalize the data between 0 and 1
#         valid_min = np.min(valid_data[valid_mask])
#         valid_max = np.max(valid_data[valid_mask])
#         range_diff = valid_max - valid_min
        
#         if range_diff == 0:  # Handle case where all values are the same
#             normalized = np.zeros_like(valid_data)
#         else:
#             normalized = np.zeros_like(valid_data)
#             normalized[valid_mask] = (valid_data[valid_mask] - valid_min) / range_diff
        
#         # Get red threshold
#         thresholds = ResultAnalyzer.set_color_thresholds(
#             property_value, red_range=red_range
#         )
#         red_threshold = thresholds["red"]
        
#         # Find red areas
#         red_areas = []
#         for i in range(rows):
#             for j in range(cols):
#                 if valid_mask[i, j] < red_threshold:
#                     red_areas.append({
#                         "Row": i,
#                         "Column": j,
#                         "Angle": int(angle_matrix[i, j]),
#                         "Value": property_value[i, j],
#                         "Severity": "High" if normalized[i, j] < (red_threshold/2) else "Medium"
#                     })
        
#         # Sort by severity and value
#         red_areas.sort(key=lambda x: (0 if x["Severity"] == "High" else 1, x["Value"]))
        
#         return red_areas


# # Define the layout for the results page
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

# def register_callbacks(app):
    
#     # Data processing and analysis callbacks
#     @app.callback(
#         [Output('thickness-stats', 'children'),
#          Output('color-distribution', 'children'),
#          Output('red-areas-table', 'data'),
#          Output('area-summary-table', 'data')],
#         Input('prop-store', 'data')
#     )
#     def update_results(stored_data):
#         if not stored_data:
#             # Return empty results if no data
#             empty_stats = html.Div("No data available")
#             empty_distribution = html.Div("No data available")
#             return empty_stats, empty_distribution, [], []
        
#         # Extract data from the store
#         property_value = np.array(stored_data.get('property_value', []))
        
#         if property_value.size == 0:
#             empty_stats = html.Div("No data available")
#             empty_distribution = html.Div("No data available")
#             return empty_stats, empty_distribution, [], []
        
#         rows, cols = property_value.shape
        
#         # Create angle matrix
#         theta = np.linspace(0, 2 * np.pi, cols)
#         z = np.linspace(0, rows, rows)
#         theta_grid, z_grid = np.meshgrid(theta, z)
#         angle_matrix = theta_grid * (180/np.pi)
        
#         # Calculate color ratios
#         # color_ratios = ResultAnalyzer.calculate_color_ratios(property_value)
#         color_ratios = ResultAnalyzer.calculate_color_ratios(
#         property_value, 
#         red_range=(13, 15),    # Red is from 13 to 15
#         yellow_range=(15, 17), # Yellow is from 15 to 17
#         green_range=(17, 20)   # Green is from 17 to 20
#         )
    
        
#         # Calculate thickness statistics
#         valid_data = property_value[property_value != -1]
#         valid_mask = property_value != -1
#         normalized = np.zeros_like(property_value)
        
#         valid_min = np.min(valid_data)
#         valid_max = np.max(valid_data)
#         range_diff = valid_max - valid_min
        
#         if range_diff != 0:
#             normalized[valid_mask] = (property_value[valid_mask] - valid_min) / range_diff
        
#         # Get data for each color category
#         red_mask = (normalized < ResultAnalyzer.YELLOW_THRESHOLD) & valid_mask
#         yellow_mask = (normalized >= ResultAnalyzer.YELLOW_THRESHOLD) & (normalized < ResultAnalyzer.GREEN_THRESHOLD) & valid_mask
#         green_mask = (normalized >= ResultAnalyzer.GREEN_THRESHOLD) & valid_mask
        
#         red_count = np.sum(red_mask)
#         yellow_count = np.sum(yellow_mask)
#         green_count = np.sum(green_mask)
#         total_count = red_count + yellow_count + green_count
        
#         # Calculate average thickness per category
#         red_avg = np.mean(property_value[red_mask]) if red_count > 0 else 0
#         yellow_avg = np.mean(property_value[yellow_mask]) if yellow_count > 0 else 0
#         green_avg = np.mean(property_value[green_mask]) if green_count > 0 else 0
        
#         # Create thickness statistics table
#         thickness_stats = html.Div([
#             html.Table([
#                 html.Thead(html.Tr([
#                     html.Th("Statistic"),
#                     html.Th("Value")
#                 ])),
#                 html.Tbody([
#                     html.Tr([html.Td("Min Thickness:"), html.Td(f"{np.min(valid_data):.2f} mm")]),
#                     html.Tr([html.Td("Max Thickness:"), html.Td(f"{np.max(valid_data):.2f} mm")]),
#                     html.Tr([html.Td("Average Thickness:"), html.Td(f"{np.mean(valid_data):.2f} mm")]),
#                     html.Tr([html.Td("Median Thickness:"), html.Td(f"{np.median(valid_data):.2f} mm")]),
#                     html.Tr([html.Td("Standard Deviation:"), html.Td(f"{np.std(valid_data):.2f} mm")]),
#                     html.Tr([html.Td("Total Cells:"), html.Td(f"{total_count}")]),
#                 ])
#             ], className="table table-striped")
#         ])
        
#         # Create color distribution table
#         color_distribution = html.Div([
#             html.Div([
#                 html.Div(style={"backgroundColor": "red", "width": f"{color_ratios['red']*100}%", "height": "30px", "float": "left", "textAlign": "center", "color": "white"}, children=f"{color_ratios['red']:.1%}"),
#                 html.Div(style={"backgroundColor": "yellow", "width": f"{color_ratios['yellow']*100}%", "height": "30px", "float": "left", "textAlign": "center"}, children=f"{color_ratios['yellow']:.1%}"),
#                 html.Div(style={"backgroundColor": "green", "width": f"{color_ratios['green']*100}%", "height": "30px", "float": "left", "textAlign": "center", "color": "white"}, children=f"{color_ratios['green']:.1%}"),
#             ], style={"width": "100%", "overflow": "hidden", "marginBottom": "15px"}),
#             html.Table([
#                 html.Thead(html.Tr([
#                     html.Th("Color Category"),
#                     html.Th("Percentage"),
#                     html.Th("Cell Count")
#                 ])),
#                 html.Tbody([
#                     html.Tr([
#                         html.Td("Red", style={"backgroundColor": "#ffcccc"}), 
#                         html.Td(f"{color_ratios['red']:.1%}"),
#                         html.Td(f"{red_count}")
#                     ]),
#                     html.Tr([
#                         html.Td("Yellow", style={"backgroundColor": "#ffffcc"}), 
#                         html.Td(f"{color_ratios['yellow']:.1%}"),
#                         html.Td(f"{yellow_count}")
#                     ]),
#                     html.Tr([
#                         html.Td("Green", style={"backgroundColor": "#ccffcc"}), 
#                         html.Td(f"{color_ratios['green']:.1%}"),
#                         html.Td(f"{green_count}")
#                     ]),
#                 ])
#             ], className="table table-striped", )
#         ])
        
#         # Find red areas for table
#         red_areas = ResultAnalyzer.find_red_areas(property_value, angle_matrix)
        
#         # Create summary table data
#         area_summary = [
#             {"category": "Red", "coverage": color_ratios['red'], "count": red_count, "avg_thickness": red_avg},
#             {"category": "Yellow", "coverage": color_ratios['yellow'], "count": yellow_count, "avg_thickness": yellow_avg},
#             {"category": "Green", "coverage": color_ratios['green'], "count": green_count, "avg_thickness": green_avg},
#             {"category": "Total", "coverage": 1.0, "count": total_count, "avg_thickness": np.mean(valid_data)}
#         ]
        
#         return thickness_stats, color_distribution, red_areas, area_summary


class ResultAnalyzer:
    """Class to analyze visualization data and calculate statistics with configurable thresholds."""
    
    @staticmethod
    def calculate_color_zones(
        property_value: np.ndarray, 
        nominal_thickness: float,
        design_thickness: float,
        threshold_thickness: float
    ) -> Dict[str, np.ndarray]:
        """
        Calculate color zones based on thickness thresholds.
        
        Args:
            property_value (np.ndarray): Input thickness data array
            nominal_thickness (float): Target nominal thickness (green threshold)
            design_thickness (float): Minimum design thickness (yellow threshold)
        
        Returns:
            Dict with masks for red, yellow, and green zones
        """
        # Remove placeholder values
        valid_mask = property_value != -1
        
        # Define color zones based on absolute thickness values
        green_mask = (property_value >= nominal_thickness) & valid_mask
        yellow_mask = (property_value >= threshold_thickness) & (property_value < nominal_thickness) & valid_mask
        red_mask = (property_value < threshold_thickness) & valid_mask
        
        return {
            "red": red_mask,
            "yellow": yellow_mask,
            "green": green_mask,
            "valid": valid_mask
        }
    
    @staticmethod
    def calculate_color_ratios(
        property_value: np.ndarray, 
        nominal_thickness: float,
        design_thickness: float,
        threshold_thickness :float
    ) -> Dict[str, float]:
        """
        Calculate the ratio of green, yellow, and red areas based on thickness thresholds.
        
        Args:
            property_value (np.ndarray): Input thickness data array
            nominal_thickness (float): Target nominal thickness (green threshold)
            design_thickness (float): Minimum design thickness (yellow threshold)
        
        Returns:
            Dict with color ratios
        """
        # Get color zone masks
        zones = ResultAnalyzer.calculate_color_zones(
            property_value, nominal_thickness, design_thickness,  threshold_thickness
        )
        
        # Count cells in each zone
        total_valid_cells = np.sum(zones["valid"])
        
        if total_valid_cells == 0:
            return {"red": 0, "yellow": 0, "green": 0}
        
        # Calculate ratios
        ratios = {
            "red": np.sum(zones["red"]) / total_valid_cells,
            "yellow": np.sum(zones["yellow"]) / total_valid_cells,
            "green": np.sum(zones["green"]) / total_valid_cells
        }
        
        return ratios
    
    @staticmethod
    def find_red_areas(
        property_value: np.ndarray, 
        angle_matrix: np.ndarray, 
        nominal_thickness: float,
        design_thickness: float,
        threshold_thickness: float
    ) -> List[Dict]:
        """
        Find locations of red areas (below design thickness).
        
        Args:
            property_value (np.ndarray): Input thickness data array
            angle_matrix (np.ndarray): Matrix of corresponding angles
            threshold_thickness (float): Minimum design thickness threshold
        
        Returns:
            List of dictionaries with red area details
        """
        rows, cols = property_value.shape
        
        # Define red mask - below design thickness
        valid_mask = property_value != -1
        red_mask = (property_value < threshold_thickness) & valid_mask
        
        if not np.any(red_mask):
            return []
        
        # Find red areas
        red_areas = []
        for i in range(rows):
            for j in range(cols):
                if red_mask[i, j]:
                    # Calculate severity based on how far below design thickness
                    # severity_ratio = property_value[i, j] / threshold_thickness if threshold_thickness > 0 else 0
                    if property_value[i, j] <= threshold_thickness:
                        severity = "High"

                    
                        red_areas.append({
                            "Row": i,
                            "Column": j,
                            "Angle": int(angle_matrix[i, j]),
                            "Value": property_value[i, j],
                            "Severity": severity
                        })
        
        # Sort by severity and value
        red_areas.sort(key=lambda x: (0 if x["Severity"] == "High" else 1, x["Value"]))
        
        return red_areas

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
        nominal_thickness = stored_data["NT"]
        design_thickness = stored_data["DT"]
        threshold_thickness = stored_data["TT"]
        # Default thresholds if not provided
        if nominal_thickness is None:
            nominal_thickness = 18.0  # Example nominal thickness
        if design_thickness is None:
            design_thickness = 15.0  # Example design thickness
        
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
        
        # Calculate color zones and ratios
        zones = ResultAnalyzer.calculate_color_zones(
            property_value, nominal_thickness, design_thickness, threshold_thickness
        )
        color_ratios = ResultAnalyzer.calculate_color_ratios(
            property_value, nominal_thickness, design_thickness, threshold_thickness
        )
        
        # Get valid data
        valid_data = property_value[zones["valid"]]
        
        # Count cells in each color category
        red_count = np.sum(zones["red"])
        yellow_count = np.sum(zones["yellow"])
        green_count = np.sum(zones["green"])
        total_count = red_count + yellow_count + green_count
        
        # Calculate average thickness per category
        red_avg = np.mean(property_value[zones["red"]]) if red_count > 0 else 0
        yellow_avg = np.mean(property_value[zones["yellow"]]) if yellow_count > 0 else 0
        green_avg = np.mean(property_value[zones["green"]]) if green_count > 0 else 0
        
        # Create thickness statistics table
        thickness_stats = html.Div([
            html.Table([
                html.Thead(html.Tr([
                    html.Th("Statistic"),
                    html.Th("Value")
                ])),
                html.Tbody([
                    html.Tr([html.Td("Nominal Thickness:"), html.Td(f"{nominal_thickness:.2f} mm")]),
                    html.Tr([html.Td("Design Thickness:"), html.Td(f"{design_thickness:.2f} mm")]),
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
                    html.Th("Threshold"),
                    html.Th("Percentage"),
                    html.Th("Cell Count")
                ])),
                html.Tbody([
                    html.Tr([
                        html.Td("Red", style={"backgroundColor": "#ffcccc"}), 
                        html.Td(f"< {threshold_thickness:.2f} mm"),
                        html.Td(f"{color_ratios['red']:.1%}"),
                        html.Td(f"{red_count}")
                    ]),
                    html.Tr([
                        html.Td("Yellow", style={"backgroundColor": "#ffffcc"}), 
                        html.Td(f"{threshold_thickness:.2f} - {nominal_thickness:.2f} mm"),
                        html.Td(f"{color_ratios['yellow']:.1%}"),
                        html.Td(f"{yellow_count}")
                    ]),
                    html.Tr([
                        html.Td("Green", style={"backgroundColor": "#ccffcc"}), 
                        html.Td(f"≥ {nominal_thickness:.2f} mm"),
                        html.Td(f"{color_ratios['green']:.1%}"),
                        html.Td(f"{green_count}")
                    ]),
                ])
            ], className="table table-striped", )
        ])
        
        # Find red areas for table
        red_areas = ResultAnalyzer.find_red_areas(property_value, angle_matrix, nominal_thickness, design_thickness,threshold_thickness)
        
        # Create summary table data
        area_summary = [
            {"category": "Red", "coverage": color_ratios['red'], "count": red_count, "avg_thickness": red_avg},
            {"category": "Yellow", "coverage": color_ratios['yellow'], "count": yellow_count, "avg_thickness": yellow_avg},
            {"category": "Green", "coverage": color_ratios['green'], "count": green_count, "avg_thickness": green_avg},
            {"category": "Total", "coverage": 1.0, "count": total_count, "avg_thickness": np.mean(valid_data)}
        ]
        
        return thickness_stats, color_distribution, red_areas, area_summary