# pages/results.py - Modern Results Page Module with Color Scheme
import dash
from dash import dcc, html, callback, Input, Output, State, dash_table
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import dash_bootstrap_components as dbc

# Modern Color Palette
PRIMARY_COLOR = "#007bff"        # Bootstrap primary blue
SECONDARY_COLOR = "#6c757d"      # Bootstrap secondary gray
ACCENT_COLOR = "#28a745"         # Bootstrap success green
WARNING_COLOR = "#ffc107"        # Bootstrap warning yellow
DANGER_COLOR = "#dc3545"         # Bootstrap danger red
LIGHT_GRAY = "#f8f9fa"          # Bootstrap light gray
DARK_GRAY = "#343a40"           # Bootstrap dark gray
TEXT_COLOR = "#495057"           # Default text color

# Modern Styles Dictionary
modern_style = {
    "container": {
        "width": "95%",
        "maxWidth": "900px",  # Increased max width for larger screens
        "margin": "20px auto",
        "padding": "25px",      # Increased padding
        "border": "0",         # Removed border
        "borderRadius": "10px", # More rounded corners
        "boxSizing": "border-box",
        "backgroundColor": "white", # White background
        "boxShadow": "0 4px 8px rgba(0,0,0,0.05)", # Softer shadow
        "fontFamily": "Arial, sans-serif", # Modern font
        "color": TEXT_COLOR,
    },
    "header": {
        "textAlign": "center",
        "fontSize": "24px",    # Larger header font
        "fontWeight": "bold",
        "marginBottom": "20px",
        "color": DARK_GRAY,
    },
    "section_header": {
        "fontSize": "20px",    # Slightly smaller section headers
        "fontWeight": "bold",
        "marginTop": "25px",
        "marginBottom": "15px",
        "color": DARK_GRAY,
    },
    "button": {
        "backgroundColor": PRIMARY_COLOR,
        "color": "white",
        "border": "none",
        "borderRadius": "8px",  # Rounded buttons
        "padding": "10px 20px", # Increased button padding
        "cursor": "pointer",
        "fontSize": "16px",
        "fontWeight": "600",
        "marginLeft": "10px",
        "boxShadow": "0 2px 4px rgba(0,0,0,0.05)", # Button shadow
    },
    "back_button": {
        "backgroundColor": LIGHT_GRAY,
        "color": DARK_GRAY,
        "border": "1px solid #ddd", # Lighter border
        "borderRadius": "8px",
        "padding": "10px 20px",
        "cursor": "pointer",
        "fontSize": "16px",
        "fontWeight": "600",
        "boxShadow": "0 1px 2px rgba(0,0,0,0.05)",
    },
    "stats_section": {
        "padding": "20px",
        "border": "1px solid #eee", # Very light border
        "borderRadius": "8px",
        "backgroundColor": LIGHT_GRAY, # Light gray background for stats
    },
    "table_header": {
        "backgroundColor": "#e9ecef", # Bootstrap light gray table header
        "fontWeight": "bold",
        "textAlign": "left",
    },
    "red_severity_row": {
        "backgroundColor": "#ffe0e0", # Lighter red for severity
        "color": DARK_GRAY,
    },
    "red_category_row": {
        "backgroundColor": "#ffe0e0",
        "color": DARK_GRAY,
    },
    "blue_category_row": {
        "backgroundColor": "#e0e0ff", # Lighter blue
        "color": DARK_GRAY,
    },
    "warning_alert": {
        "display": "none",
        "marginBottom": "15px",
        "color": DARK_GRAY,
        "backgroundColor": WARNING_COLOR, # Yellow warning background
        "borderColor": WARNING_COLOR,
        "borderRadius": "8px",
        "padding": "10px 15px",
    },
    "color_distribution_bar_container": {
        "width": "100%",
        "overflow": "hidden",
        "marginBottom": "15px",
        "borderRadius": "8px", # Rounded bar container
        "border": "1px solid #ddd", # Light border for the bar
    },
    "color_distribution_bar_red": {
        "backgroundColor": DANGER_COLOR, # Use danger red for red zone
        "height": "35px",           # Slightly taller bars
        "float": "left",
        "textAlign": "center",
        "color": "white",
        "lineHeight": "35px",       # Vertically center text in bar
    },
    "color_distribution_bar_blue": {
        "backgroundColor": PRIMARY_COLOR, # Use primary blue for blue zone
        "height": "35px",
        "float": "left",
        "textAlign": "center",
        "color": "white",
        "lineHeight": "35px",
    },
}


# Define the layout for the results page with modern styles
layout = html.Div(
    [
        # ocation(id='url', refresh=True),  # **IMPORTANT: refresh=True**
        html.Div(id="results-print-area",  # Added ID for printable area
                 children=[
                     html.Div([
                         html.H3("Results and Analysis", style=modern_style["header"]),
                         html.Div([
                             dcc.Link(
                                 html.Button(
                                     "← Back to Input Form",
                                     id="back-button",
                                     style=modern_style["back_button"]
                                 ),
                                 href='/',
                             ),
                             dbc.Button(  # Added Print Button
                                 "Print Results",
                                 id="print-button",
                                 style=modern_style["button"]
                             ),
                         ], style={"textAlign": "left", "display": "flex", "justify-content": "space-between"}),  # Adjusted style for button alignment
                     ]),
                     html.Div([
                         html.Div([
                             html.Div([
                                 html.H3("Thickness Statistics", style=modern_style["section_header"]),
                                 html.Div(id='thickness-stats', className="p-3", style=modern_style["stats_section"]) # Removed border and rounded from class, using style
                             ], className='col-md-6'),

                             html.Div([
                                 html.H3("Color Distribution", style=modern_style["section_header"]),
                                 html.Div(id='color-distribution', className="p-3", style=modern_style["stats_section"]) # Removed border and rounded from class, using style
                             ], className='col-md-6'),
                         ], className='row mb-4'),

                         html.Div([
                             html.H3("Critical Areas (Red Zones)", className="text-center", style=modern_style["section_header"]),
                             html.Div(id='threshold-warning', className="alert alert-warning", style=modern_style["warning_alert"]), # Using modern_style for warning
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
                                         'style': modern_style["red_severity_row"], # Using modern style for red rows
                                     }
                                 ],
                                 style_header=modern_style["table_header"], # Using modern style for table header
                                 style_cell={'textAlign': 'left'}, # Default cell alignment left
                                 page_size=10,
                                 filter_action="native",
                                 sort_action="native",
                                 sort_mode="multi",
                                #  className="table table-striped table-hover", # Bootstrap table classes
                             )
                         ], className='row'),

                         html.Div([
                             html.H3("Area Coverage Summary", className="text-center mt-4", style=modern_style["section_header"]),
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
                                         'style': modern_style["red_category_row"], # Using modern style for red category
                                     },
                                     {
                                         'if': {'filter_query': '{category} = "Blue"'},
                                         'style': modern_style["blue_category_row"], # Using modern style for blue category
                                     }
                                 ],
                                 style_header=modern_style["table_header"], # Using modern style for table header
                                 style_cell={'textAlign': 'left'},
                                #  className="table table-striped table-hover", # Bootstrap table classes
                             )
                         ], className='row mt-4'),
                     ], className="content"),
                 ], style=modern_style["container"]), # Apply modern container style
        html.Div(id="dummy-print-output", style={'display': 'none'})  # Dummy output for clientside callback
    ]
)


class ResultAnalyzer:
    """Class to analyze visualization data and calculate statistics with configurable thresholds."""

    @staticmethod
    def calculate_color_zones(
            property_value: np.ndarray,
            thickness: float,
            threshold_percentage: float
    ) -> Dict[str, np.ndarray]:
        """
        Calculate binary color zones based on threshold percentage of max thickness.

        Args:
            property_value (np.ndarray): Input thickness data array
            thickness (float): Maximum thickness value
            threshold_percentage (float): Percentage threshold for red/blue distinction

        Returns:
            Dict with masks for red and blue zones, warning message if threshold exceeds max
        """
        # Remove placeholder values
        valid_mask = property_value != -1
        valid_data = property_value[valid_mask]

        # Calculate threshold value
        threshold_value = thickness * (threshold_percentage / 100.0)

        # Warning message if threshold exceeds max value
        warning_message = ""
        data_max = np.max(valid_data) if len(valid_data) > 0 else 0

        if threshold_value > data_max:
            warning_message = f"Warning: Calculated threshold value ({threshold_value:.2f}) exceeds maximum data value ({data_max:.2f}). Threshold has been adjusted to maximum value."
            threshold_value = data_max

        # Define binary color zones based on threshold
        red_mask = (property_value <= threshold_value) & valid_mask
        blue_mask = (property_value > threshold_value) & valid_mask

        return {
            "red": red_mask,
            "blue": blue_mask,
            "valid": valid_mask,
            "warning": warning_message,
            "adjusted_threshold": threshold_value
        }

    @staticmethod
    def calculate_color_ratios(
            property_value: np.ndarray,
            thickness: float,
            threshold_percentage: float
    ) -> Dict[str, float]:
        """
        Calculate the ratio of red and blue areas based on threshold.

        Args:
            property_value (np.ndarray): Input thickness data array
            thickness (float): Maximum thickness value
            threshold_percentage (float): Percentage threshold for red/blue distinction

        Returns:
            Dict with color ratios and warning if applicable
        """
        # Get color zone masks
        zones = ResultAnalyzer.calculate_color_zones(
            property_value, thickness, threshold_percentage
        )

        # Count cells in each zone
        total_valid_cells = np.sum(zones["valid"])

        if total_valid_cells == 0:
            return {"red": 0, "blue": 0, "warning": zones["warning"], "adjusted_threshold": zones["adjusted_threshold"]}

        # Calculate ratios
        ratios = {
            "red": np.sum(zones["red"]) / total_valid_cells,
            "blue": np.sum(zones["blue"]) / total_valid_cells,
            "warning": zones["warning"],
            "adjusted_threshold": zones["adjusted_threshold"]
        }

        return ratios

    @staticmethod
    def find_red_areas(
            property_value: np.ndarray,
            angle_matrix: np.ndarray,
            thickness: float,
            threshold_percentage: float
    ) -> Tuple[List[Dict], str, float]:
        """
        Find locations of red areas (below threshold).

        Args:
            property_value (np.ndarray): Input thickness data array
            angle_matrix (np.ndarray): Matrix of corresponding angles
            thickness (float): Maximum thickness value
            threshold_percentage (float): Percentage threshold for red/blue distinction

        Returns:
            Tuple of (list of dictionaries with red area details, warning message, adjusted threshold)
        """
        rows, cols = property_value.shape

        # Get zones including warning message if threshold is adjusted
        zones = ResultAnalyzer.calculate_color_zones(
            property_value, thickness, threshold_percentage
        )

        red_mask = zones["red"]
        warning_message = zones["warning"]
        adjusted_threshold = zones["adjusted_threshold"]

        if not np.any(red_mask):
            return [], warning_message, adjusted_threshold

        # Find red areas
        red_areas = []
        for i in range(rows):
            for j in range(cols):
                if red_mask[i, j]:
                    # All red areas are high severity in binary scheme
                    severity = "High"

                    red_areas.append({
                        "Row": i,
                        "Column": j,
                        "Angle": int(angle_matrix[i, j]),
                        "Value": property_value[i, j],
                        "Severity": severity
                    })

        # Sort by value (lowest thickness first)
        red_areas.sort(key=lambda x: x["Value"])

        return red_areas, warning_message, adjusted_threshold


def register_callbacks(app):
    # Data processing and analysis callbacks
    @app.callback(
        [Output('thickness-stats', 'children'),
         Output('color-distribution', 'children'),
         Output('red-areas-table', 'data'),
         Output('area-summary-table', 'data'),
         Output('threshold-warning', 'children'),
         Output('threshold-warning', 'style')],
        [Input('prop-store', 'data'),       
         Input('data-store','data')],   
        prevent_initial_call=False
    )
    def update_results(stored_data, info_data):
        if not stored_data or info_data:
            # Return empty results if no data
            empty_stats = html.Div("No data available")
            empty_distribution = html.Div("No data available")
            return empty_stats, empty_distribution, [], [], "", {'display': 'none'}
        
        # Accessing the data using the info_data dictionary
        report_no = info_data["report_no"]
        client_name = info_data["client_name"]
        address = info_data["address"]
        date = info_data["date"]
        po_number = info_data["po_number"]
        date_inspection = info_data["date_inspection"]

        # Equipment details
        make = info_data["make"]
        model = info_data["model"]
        sr_no = info_data["sr_no"]
        calibration_due_date = info_data["calibration_due_date"]

        # Part details
        part_name = info_data["part_name"]
        material = info_data["material"]
        drawing_number = info_data["drawing_number"]

        # Example usage:  Print some of the values
        print(f"Report Number: {report_no}")
        print(f"Client Name: {client_name}")
        print(f"Part Name: {part_name}")
        print(f"Equipment Serial Number: {sr_no}")
        # Extract parameters from stored data
        thickness = stored_data.get("T")
        threshold_percentage = stored_data.get("TT")
        print(thickness, threshold_percentage)
        # Extract data from the store
        property_value = np.array(stored_data.get('property_value', []))

        if property_value.size == 0:
            empty_stats = html.Div("No data available")
            empty_distribution = html.Div("No data available")
            return empty_stats, empty_distribution, [], [], "", {'display': 'none'}

        rows, cols = property_value.shape

        # Create angle matrix
        theta = np.linspace(0, 2 * np.pi, cols)
        z = np.linspace(0, rows, rows)
        theta_grid, z_grid = np.meshgrid(theta, z)
        angle_matrix = theta_grid * (180 / np.pi)

        # Calculate color zones and ratios
        color_ratios = ResultAnalyzer.calculate_color_ratios(
            property_value, thickness, threshold_percentage
        )

        zones = ResultAnalyzer.calculate_color_zones(
            property_value, thickness, threshold_percentage
        )

        # Get valid data
        valid_data = property_value[zones["valid"]]

        # Get the adjusted threshold and warning message
        adjusted_threshold = color_ratios["adjusted_threshold"]
        warning_message = color_ratios["warning"]

        # Count cells in each color category
        red_count = np.sum(zones["red"])
        blue_count = np.sum(zones["blue"])
        total_count = red_count + blue_count

        # Calculate average thickness per category
        red_avg = np.mean(property_value[zones["red"]]) if red_count > 0 else 0
        blue_avg = np.mean(property_value[zones["blue"]]) if blue_count > 0 else 0


        # Create thickness statistics table
        thickness_stats = html.Div([
            html.Table([
                html.Thead(html.Tr([
                    html.Th("Statistic", style=modern_style["table_header"]),
                    html.Th("Value", style=modern_style["table_header"])
                ])),
                html.Tbody([
                    html.Tr([html.Td("Max Thickness:"), html.Td(f"{thickness:.2f} mm")]),
                    html.Tr([html.Td("Threshold Percentage:"), html.Td(f"{threshold_percentage:.1f}%")]),
                    html.Tr([html.Td("Threshold Value:"), html.Td(f"{adjusted_threshold:.2f} mm")]),
                    html.Tr([html.Td("Min Thickness:"), html.Td(f"{np.min(valid_data):.2f} mm")]),
                    html.Tr([html.Td("Max Thickness:"), html.Td(f"{np.max(valid_data):.2f} mm")]),
                    html.Tr([html.Td("Average Thickness:"), html.Td(f"{np.mean(valid_data):.2f} mm")]),
                    html.Tr([html.Td("Median Thickness:"), html.Td(f"{np.median(valid_data):.2f} mm")]),
                    html.Tr([html.Td("Standard Deviation:"), html.Td(f"{np.std(valid_data):.2f} mm")]),
                    html.Tr([html.Td("Total Cells:"), html.Td(f"{total_count}")]),
                ])
            ], className="table table-borderless") # Removed striped, added borderless for cleaner look
        ])

        # Create color distribution table with binary scheme
        color_distribution = html.Div([
            html.Div([
                html.Div(style={**modern_style["color_distribution_bar_red"], "width": f"{color_ratios['red'] * 100}%"}, children=f"{color_ratios['red']:.1%}"), # Using spread operator to merge styles
                html.Div(style={**modern_style["color_distribution_bar_blue"], "width": f"{color_ratios['blue'] * 100}%"}, children=f"{color_ratios['blue']:.1%}"), # Using spread operator to merge styles
            ], style=modern_style["color_distribution_bar_container"]), # Applying container style
            html.Table([
                html.Thead(html.Tr([
                    html.Th("Color Category", style=modern_style["table_header"]),
                    html.Th("Threshold", style=modern_style["table_header"]),
                    html.Th("Percentage", style=modern_style["table_header"]),
                    html.Th("Cell Count", style=modern_style["table_header"])
                ])),
                html.Tbody([
                    html.Tr([
                        html.Td("Red", style=modern_style["red_category_row"]), # Applying row style
                        html.Td(f"< {adjusted_threshold:.2f} mm"),
                        html.Td(f"{color_ratios['red']:.1%}"),
                        html.Td(f"{red_count}")
                    ]),
                    html.Tr([
                        html.Td("Blue", style=modern_style["blue_category_row"]), # Applying row style
                        html.Td(f"≥ {adjusted_threshold:.2f} mm"),
                        html.Td(f"{color_ratios['blue']:.1%}"),
                        html.Td(f"{blue_count}")
                    ]),
                ])
            ], className="table table-borderless") # Removed striped, added borderless for cleaner look
        ])

        # Find red areas for table
        red_areas, warning_msg, adjusted_threshold = ResultAnalyzer.find_red_areas(
            property_value, angle_matrix, thickness, threshold_percentage
        )

        # Create summary table data with binary scheme
        area_summary = [
            {"category": "Red", "coverage": color_ratios['red'], "count": red_count, "avg_thickness": red_avg},
            {"category": "Blue", "coverage": color_ratios['blue'], "count": blue_count, "avg_thickness": blue_avg},
            {"category": "Total", "coverage": 1.0, "count": total_count, "avg_thickness": np.mean(valid_data)}
        ]

        # Set warning message display style
        warning_style = {'display': 'block', **modern_style["warning_alert"]} if warning_message else {'display': 'none'} # Using spread operator to merge styles

        return thickness_stats, color_distribution, red_areas, area_summary, warning_message, warning_style

    app.clientside_callback(
        """
        function(n_clicks) {
            if (n_clicks > 0) {
                var printContents = document.getElementById('results-print-area').innerHTML;
                var originalContents = document.body.innerHTML;

                document.body.innerHTML = printContents;

                window.print();

                document.body.innerHTML = originalContents;
                //window.location.reload(); // Optional: Reload page after print - can be commented out if not needed
                return 'printed'; // Return a value to trigger output (dummy-print-output)
            }
            return ''; // Return empty string if button not clicked
        }
        """,
        Output("dummy-print-output", "children"),
        Input("print-button", "n_clicks"),
    )