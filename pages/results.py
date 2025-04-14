# pages/results.py - Modern Results Page Module with Fixed Min-Max Range Zones
import dash
from dash import dcc, html, callback, Input, Output, State, dash_table
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any
import dash_bootstrap_components as dbc
import colorsys

# --- Define Fixed Range Zone Structure and Colors ---
# 4 Zones within Min-Max + Below Min + Above Max
NUM_MAIN_ZONES = 4
ZONE_DEFINITIONS_FIXED = [
    {'name': 'Below Min',        'color': '#808080'},  # Gray for below range
    {'name': 'Zone 1 (Lowest)',  'color': '#7a0402'},  # Min to Min + 25% range
    {'name': 'Zone 2',           'color': '#f36315'},  # Min + 25% to Min + 50% range
    {'name': 'Zone 3',           'color': '#a4fc3b'},  # Min + 50% to Min + 75% range
    {'name': 'Zone 4 (Highest)', 'color': '#39a2fc'},  # Min + 75% range to Max
    {'name': 'Above Max',        'color': '#404040'},  # Dark Gray for above range
]
# Ensure the number of colors matches 2 + NUM_MAIN_ZONES
assert len(ZONE_DEFINITIONS_FIXED) == NUM_MAIN_ZONES + 2

# Function to lighten hex colors (remains the same)
def lighten_color(hex_color, factor=0.7):
    # ... (lighten_color function code remains the same) ...
    try:
        h, l, s = colorsys.rgb_to_hls(*[int(hex_color[i:i+2], 16)/255.0 for i in (1, 3, 5)])
        new_l = min(1.0, l + (1.0 - l) * factor if factor < 1 else l * (1/factor))
        new_l = max(0.5, new_l)
        r, g, b = colorsys.hls_to_rgb(h, new_l, s)
        return '#%02x%02x%02x' % (int(r*255), int(g*255), int(b*255))
    except:
        return hex_color


# --- Modern Color Palette ---
PRIMARY_COLOR = "#007bff"
SECONDARY_COLOR = "#6c757d"
ACCENT_COLOR = "#28a745"
WARNING_COLOR = "#ffc107"
LIGHT_GRAY = "#f8f9fa"
DARK_GRAY = "#343a40"
TEXT_COLOR = "#495057"

# --- Modern Styles Dictionary (Dynamically Populated for Fixed Zones) ---
modern_style = {
    "container": { "width": "95%", "maxWidth": "900px", "margin": "20px auto", "padding": "25px", "border": "0", "borderRadius": "10px", "boxSizing": "border-box", "backgroundColor": "white", "boxShadow": "0 4px 8px rgba(0,0,0,0.05)", "fontFamily": "Arial, sans-serif", "color": TEXT_COLOR },
    "header": { "textAlign": "center", "fontSize": "24px", "fontWeight": "bold", "marginBottom": "20px", "color": DARK_GRAY },
    "section_header": { "fontSize": "20px", "fontWeight": "bold", "marginTop": "25px", "marginBottom": "15px", "color": DARK_GRAY },
    "button": { "backgroundColor": PRIMARY_COLOR, "color": "white", "border": "none", "borderRadius": "8px", "padding": "10px 20px", "cursor": "pointer", "fontSize": "16px", "fontWeight": "600", "marginLeft": "10px", "boxShadow": "0 2px 4px rgba(0,0,0,0.05)" },
    "back_button": { "backgroundColor": LIGHT_GRAY, "color": DARK_GRAY, "border": "1px solid #ddd", "borderRadius": "8px", "padding": "10px 20px", "cursor": "pointer", "fontSize": "16px", "fontWeight": "600", "boxShadow": "0 1px 2px rgba(0,0,0,0.05)" },
    "stats_section": { "padding": "20px", "border": "1px solid #eee", "borderRadius": "8px", "backgroundColor": LIGHT_GRAY },
    "table_header": { "backgroundColor": "#e9ecef", "fontWeight": "bold", "textAlign": "left" },
    "color_distribution_bar_container": { "width": "100%", "overflow": "hidden", "marginBottom": "15px", "borderRadius": "8px", "border": "1px solid #ddd", "display": "flex", "height": "35px", "lineHeight": "35px", "fontSize": "14px" },
    "warning_alert": { "display": "none", "marginBottom": "15px", "color": DARK_GRAY, "backgroundColor": WARNING_COLOR, "borderColor": WARNING_COLOR, "borderRadius": "8px", "padding": "10px 15px" },
    "error_alert": { "display": "none", "marginBottom": "15px", "color": "white", "backgroundColor": "#dc3545", "borderColor": "#dc3545", "borderRadius": "8px", "padding": "10px 15px" }, # For critical errors
}
unit = "mm"
# Dynamically add styles for each fixed zone definition
for zone_def in ZONE_DEFINITIONS_FIXED:
    hex_color = zone_def['color']
    safe_key = hex_color.replace('#', '')
    modern_style[f"category_row_{safe_key}"] = {
        "backgroundColor": lighten_color(hex_color, 0.65),
        "color": DARK_GRAY,
    }
    modern_style[f"dist_bar_{safe_key}"] = {
        "backgroundColor": hex_color,
        "textAlign": "center",
        "color": "white" if colorsys.rgb_to_hls(*[int(hex_color[i:i+2], 16)/255.0 for i in (1, 3, 5)])[1] < 0.5 else DARK_GRAY,
    }


# --- Layout Definition ---
layout = html.Div(
    [
        html.Div(id="results-print-area",
                 children=[
                     html.Div([ # Header and Buttons
                         html.H3("Results and Analysis", style=modern_style["header"]),
                         html.Div([
                             dcc.Link(html.Button("← Back to Input Form", id="back-button", style=modern_style["back_button"]), href='/'),
                             dbc.Button("Print Results", id="print-button", style=modern_style["button"]),
                         ], style={"textAlign": "left", "display": "flex", "justify-content": "space-between"}),
                     ]),
                     html.Div([ # Main Content Area
                         # Input Validation Error Area
                         html.Div(id='input-error', className="alert alert-danger", style=modern_style["error_alert"]),

                         # Row for Stats and Distribution
                         html.Div([
                             html.Div([
                                 html.H3("Scan Details & Statistics", style=modern_style["section_header"]),
                                 html.Div(id='thickness-stats', className="p-3", style=modern_style["stats_section"])
                             ], className='col-md-6'),
                             html.Div([
                                 html.H3(id='distribution-header', children="Thickness Distribution by Zone", style=modern_style["section_header"]), # Dynamic Header
                                 html.Div(id='color-distribution', className="p-3", style=modern_style["stats_section"])
                             ], className='col-md-6'),
                         ], className='row mb-4'),

                         # Row for Critical Areas Table
                         html.Div([
                             html.Div(id='general-warning', className="alert alert-warning", style=modern_style["warning_alert"]),
                             html.H3("Critical Areas (Zone 1 / Below Min)", className="text-center", style=modern_style["section_header"]),
                             dash_table.DataTable(
                                 id='critical-areas-table',
                                 columns=[
                                     {'name': 'Row', 'id': 'Row'},
                                     {'name': 'Column', 'id': 'Column'},
                                     {'name': 'Angle (°)', 'id': 'Angle'},
                                     {'name': 'Thickness ({unit})', 'id': 'Value', 'type': 'numeric', 'format': {'specifier': '.2f'}},
                                     {'name': 'Zone Category', 'id': 'Category'}
                                 ],
                                 # Style critical rows if needed
                                 style_data_conditional=[
                                      {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'},
                                     # Highlight "Below Min" rows explicitly
                                      {
                                         'if': {'filter_query': f'{{Category}} = "{ZONE_DEFINITIONS_FIXED[0]["name"]}"'}, # "Below Min"
                                         'style': modern_style[f"category_row_{ZONE_DEFINITIONS_FIXED[0]['color'].replace('#','')}"]
                                      },
                                       # Highlight "Zone 1" rows
                                      {
                                         'if': {'filter_query': f'{{Category}} = "{ZONE_DEFINITIONS_FIXED[1]["name"]}"'}, # Zone 1
                                         'style': modern_style[f"category_row_{ZONE_DEFINITIONS_FIXED[1]['color'].replace('#','')}"]
                                      },
                                 ],
                                 style_header=modern_style["table_header"],
                                 style_cell={'textAlign': 'left', 'padding': '8px'},
                                 page_size=10, filter_action="native", sort_action="native", sort_mode="multi",
                                 style_table={'overflowX': 'auto'},
                             )
                         ], className='row mb-4'),

                         # Row for Area Summary Table
                         html.Div([
                             html.H3("Area Coverage Summary by Zone", className="text-center mt-4", style=modern_style["section_header"]),
                             dash_table.DataTable(
                                 id='area-summary-table',
                                 columns=[
                                     {'name': 'Zone Category', 'id': 'category'},
                                     {'name': 'Thickness Range ({unit})', 'id': 'threshold_value_range'}, # The defining range
                                     {'name': 'Coverage (%)', 'id': 'coverage', 'type': 'numeric', 'format': {'specifier': '.1%'}},
                                     {'name': 'Cell Count', 'id': 'count', 'type': 'numeric'},
                                     {'name': 'Average Thickness ({unit})', 'id': 'avg_thickness', 'type': 'numeric', 'format': {'specifier': '.2f'}}
                                 ],
                                 style_data_conditional=[], # Populated in callback
                                 style_header=modern_style["table_header"],
                                 style_cell={'textAlign': 'left', 'padding': '8px'},
                                 style_table={'overflowX': 'auto'},
                             )
                         ], className='row mt-4'),
                     ], className="content"),
                 ], style=modern_style["container"]),
        html.Div(id="dummy-print-output", style={'display': 'none'})
    ]
)


# --- Result Analysis Logic (Fixed Min-Max Range) ---
class ResultAnalyzerFixedRange:
    """Analyzes visualization data using zones defined by a fixed Min-Max range."""

    @staticmethod
    def calculate_fixed_range_zones(
        property_value: np.ndarray,
        min_threshold: float,
        max_threshold: float,
        num_main_zones: int, # e.g., 4
        zone_definitions: List[Dict[str, str]] # Should have num_main_zones + 2 entries
    ) -> Tuple[List[Dict[str, Any]], np.ndarray, List[float]]:
        """
        Calculates masks and details for zones based on a fixed Min-Max range.

        Args:
            property_value (np.ndarray): Input thickness data array.
            min_threshold (float): User-specified minimum boundary.
            max_threshold (float): User-specified maximum boundary.
            num_main_zones (int): How many zones to create between Min and Max.
            zone_definitions (List): Defines names and colors for all zones (Below, Main 1..N, Above).

        Returns:
            Tuple: (List of zone dictionaries, valid_mask, list of calculated threshold values in {unit})
                   Zone dict: 'name', 'color', 'threshold_value_range_str_mm', 'mask'.
                   Threshold values: Boundaries between the main zones [thresh1, thresh2, ...].
        """
        zones = []
        valid_mask = property_value != -1
        global unit
        # Calculate threshold values within the main range
        # linspace includes start and end, so need num_main_zones + 1 points for N zones
        try:
            threshold_values_mm = np.linspace(min_threshold, max_threshold, num_main_zones + 1)
            # The thresholds *between* zones are the inner values
            intermediate_thresholds = threshold_values_mm[1:-1].tolist() # [thresh1, thresh2, thresh3] for 4 zones
        except Exception as e:
             print(f"Error calculating thresholds: {e}")
             # Handle case where linspace fails (e.g., Max=Min) - handled later by validation
             intermediate_thresholds = []


        current_zones = []

        # 1. Below Min Zone
        mask_below = (property_value < min_threshold) & valid_mask
        range_str_below = f"< {min_threshold:.2f} {unit}"
        current_zones.append({
            'name': zone_definitions[0]['name'], 'color': zone_definitions[0]['color'],
            'threshold_value_range_str_mm': range_str_below, 'mask': mask_below
        })

        # 2. Main Zones (Zone 1 to N)
        last_thresh = min_threshold
        for i in range(num_main_zones):
            # Determine upper boundary for this main zone
            # If intermediate_thresholds is shorter than expected (e.g. Max=Min), this handles it
            if i < len(intermediate_thresholds):
                 current_thresh = intermediate_thresholds[i]
                 range_str = f"{last_thresh:.2f} {unit} - <= {current_thresh:.2f} {unit}"
                 mask = (property_value >= last_thresh) & (property_value <= current_thresh) & valid_mask
            else: # This handles the *last* main zone, ensuring it goes up to Max
                 current_thresh = max_threshold
                 # If Max == Min, the first zone covers the single value. This handles subsequent zones.
                 if i == 0: # First main zone covers the single point if Max=Min
                     mask = (property_value >= last_thresh) & (property_value <= current_thresh) & valid_mask
                     range_str = f"== {last_thresh:.2f} {unit}" if last_thresh == current_thresh else f"{last_thresh:.2f} {unit} - <= {current_thresh:.2f} {unit}"
                 else: # For zones 2,3,4 if Max=Min, their masks should be empty
                     mask = np.zeros_like(property_value, dtype=bool)
                     range_str = f"N/A (Range Collapsed)"

                 # Special mask for the very last main zone to include Max exactly
                 if i == num_main_zones - 1 and last_thresh != current_thresh:
                      mask = (property_value > last_thresh) & (property_value <= current_thresh) & valid_mask
                      range_str = f"> {last_thresh:.2f} {unit} - <= {current_thresh:.2f} {unit}"
                 elif i == num_main_zones - 1 and last_thresh == current_thresh: # Max=Min case for last zone
                     pass # Mask already handled by i==0 case above

            current_zones.append({
                'name': zone_definitions[i+1]['name'], 'color': zone_definitions[i+1]['color'],
                'threshold_value_range_str_mm': range_str, 'mask': mask
            })
            last_thresh = current_thresh


        # 3. Above Max Zone
        mask_above = (property_value > max_threshold) & valid_mask
        range_str_above = f"> {max_threshold:.2f} {unit}"
        current_zones.append({
            'name': zone_definitions[-1]['name'], 'color': zone_definitions[-1]['color'],
            'threshold_value_range_str_mm': range_str_above, 'mask': mask_above
        })

        return current_zones, valid_mask, intermediate_thresholds


    @staticmethod
    def calculate_statistics(
        property_value: np.ndarray,
        min_threshold: float,
        max_threshold: float,
        num_main_zones: int,
        zone_definitions: List[Dict[str, str]]
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Calculates coverage, counts, and average thickness for each fixed-range zone, plus overall stats.
        """
        zones_data, valid_mask, _ = ResultAnalyzerFixedRange.calculate_fixed_range_zones(
            property_value, min_threshold, max_threshold, num_main_zones, zone_definitions
        )

        valid_data = property_value[valid_mask]
        total_valid_cells = np.sum(valid_mask)
        zone_stats = []

        if total_valid_cells == 0:
            overall_stats = {'min': 0, 'max': 0, 'mean': 0, 'median': 0, 'std': 0, 'total_valid_cells': 0}
            # Populate empty stats based on zone_definitions
            for i, zone_def in enumerate(zone_definitions):
                 zone_stats.append({
                    'name': zone_def['name'], 'color': zone_def['color'],
                    'threshold_value_range_str_mm': "N/A",
                    'count': 0, 'coverage': 0.0, 'avg_thickness': 0.0
                })
            return zone_stats, overall_stats

        # Calculate stats for each zone
        for zone in zones_data:
            count = np.sum(zone['mask'])
            coverage = count / total_valid_cells if total_valid_cells > 0 else 0.0
            zone_values = property_value[zone['mask']]
            avg_thickness = np.mean(zone_values) if count > 0 else 0.0

            zone_stats.append({
                'name': zone['name'],
                'color': zone['color'],
                'threshold_value_range_str_mm': zone['threshold_value_range_str_mm'],
                'count': count,
                'coverage': coverage,
                'avg_thickness': avg_thickness
            })

        # Overall statistics (still useful)
        overall_stats = {
            'min': np.min(valid_data) if valid_data.size > 0 else 0,
            'max': np.max(valid_data) if valid_data.size > 0 else 0,
            'mean': np.mean(valid_data) if valid_data.size > 0 else 0,
            'median': np.median(valid_data) if valid_data.size > 0 else 0,
            'std': np.std(valid_data) if valid_data.size > 0 else 0,
            'total_valid_cells': total_valid_cells
        }

        return zone_stats, overall_stats

    @staticmethod
    def find_critical_areas(
        property_value: np.ndarray,
        angle_matrix: np.ndarray,
        min_threshold: float,
        max_threshold: float,
        num_main_zones: int,
        zone_definitions: List[Dict[str, str]]
    ) -> List[Dict[str, Any]]:
        """
        Finds locations Below Min or in Zone 1 (lowest segment within the range).
        """
        zones_data, _, _ = ResultAnalyzerFixedRange.calculate_fixed_range_zones(
            property_value, min_threshold, max_threshold, num_main_zones, zone_definitions
        )

        if not zones_data or len(zones_data) < 2: # Need at least Below Min and Zone 1 definitions
            return []

        # Combine masks for "Below Min" and "Zone 1"
        critical_mask_below = zones_data[0]['mask'] # Below Min mask
        critical_mask_zone1 = zones_data[1]['mask'] # Zone 1 mask
        combined_critical_mask = critical_mask_below | critical_mask_zone1

        if not np.any(combined_critical_mask):
            return []

        critical_areas = []
        rows, cols = property_value.shape
        for i in range(rows):
            for j in range(cols):
                if combined_critical_mask[i, j]:
                    # Determine category based on which mask was true
                    category = zones_data[0]['name'] if critical_mask_below[i, j] else zones_data[1]['name']
                    critical_areas.append({
                        "Row": i,
                        "Column": j,
                        "Angle": int(angle_matrix[i, j]) if angle_matrix is not None else 'N/A',
                        "Value": property_value[i, j],
                        "Category": category
                    })

        critical_areas.sort(key=lambda x: x["Value"])
        return critical_areas

# --- Callbacks ---
def register_callbacks(app):

    @app.callback(
        [Output('thickness-stats', 'children'),
         Output('color-distribution', 'children'),
         Output('distribution-header', 'children'), # Update header dynamically
         Output('critical-areas-table', 'data'),
         Output('area-summary-table', 'data'),
         Output('area-summary-table', 'style_data_conditional'),
         Output('input-error', 'children'),      # Output for input errors
         Output('input-error', 'style'),         # Style for input errors
         Output('general-warning', 'children'),  # Output for general warnings
         Output('general-warning', 'style')],    # Style for warnings
        [Input('prop-store', 'data'),
         Input('data-store','data')],
        prevent_initial_call=False
    )
    def update_results(stored_data, info_data):
        # Default empty state
        empty_div = html.Div("No data available")
        no_display = {'display': 'none'}
        error_display = {**modern_style["error_alert"], 'display': 'block'}
        default_dist_header = "Thickness Distribution by Zone"

        if not stored_data or not info_data:
            return empty_div, empty_div, default_dist_header, [], [], [], "No data received from previous step.", error_display, "", no_display

        # --- 1. Extract Data ---
        property_value = np.array(stored_data.get('property_value', []))
        nominal_thickness = stored_data.get("T") # Still potentially useful for context
        min_val = stored_data.get("TT") # Get user-defined Min
        max_val = stored_data.get("T") # Get user-defined Max
        global unit
        # --- Input Validation ---
        error_messages = []
        if property_value.size == 0:
            error_messages.append("Thickness data array is empty.")
        if min_val is None:
            error_messages.append("Minimum threshold (Min) not provided.")
        if max_val is None:
            error_messages.append("Maximum threshold (Max) not provided.")
        if min_val is not None and max_val is not None:
            if not isinstance(min_val, (int, float)):
                 error_messages.append(f"Minimum threshold ({min_val}) is not a valid number.")
            if not isinstance(max_val, (int, float)):
                 error_messages.append(f"Maximum threshold ({max_val}) is not a valid number.")
            elif max_val <= min_val:
                 error_messages.append(f"Maximum threshold ({max_val:.2f}) must be greater than Minimum threshold ({min_val:.2f}).")

        if error_messages:
            error_str = "Input Errors: " + " | ".join(error_messages)
            return empty_div, empty_div, default_dist_header, [], [], [], error_str, error_display, "", no_display

        # --- Passed Validation ---
        input_error_style = no_display
        input_error_msg = ""
        distribution_header = f"Distribution within {min_val:.2f}{unit} - {max_val:.2f}{unit} Range"

        # Extract metadata (same as before)
        report_no = info_data.get("report_no", "N/A")
        # ... (extract other info_data fields) ...
        client_name = info_data.get("client_name", "N/A")
        address = info_data.get("address", "N/A")
        date = info_data.get("date", "N/A")
        po_number = info_data.get("po_number", "N/A")
        date_inspection = info_data.get("date_inspection", "N/A")
        make = info_data.get("make", "N/A")
        model = info_data.get("model", "N/A")
        sr_no = info_data.get("sr_no", "N/A")
        calibration_due_date = info_data.get("calibration_due_date", "N/A")
        part_name = info_data.get("part_name", "N/A")
        material = info_data.get("material", "N/A")
        drawing_number = info_data.get("drawing_number", "N/A")
        unit = info_data.get("unit", "N/A")
        rows, cols = property_value.shape

        # --- 2. Perform Analysis using Fixed Range ---
        try:
            zone_stats, overall_stats = ResultAnalyzerFixedRange.calculate_statistics(
                property_value, min_val, max_val, NUM_MAIN_ZONES, ZONE_DEFINITIONS_FIXED
            )

            # Create angle matrix
            angle_matrix = None
            if overall_stats['total_valid_cells'] > 0 and cols > 0:
                 try:
                     theta = np.linspace(0, 360, cols, endpoint=False)
                     z = np.arange(rows)
                     theta_grid, _ = np.meshgrid(theta, z)
                     angle_matrix = theta_grid
                 except Exception as e:
                     print(f"Error creating angle matrix: {e}")

            critical_areas_data = ResultAnalyzerFixedRange.find_critical_areas(
                 property_value, angle_matrix, min_val, max_val, NUM_MAIN_ZONES, ZONE_DEFINITIONS_FIXED
            )
        except Exception as e:
             print(f"Error during analysis: {e}")
             analysis_error_str = f"Analysis Error: {e}"
             return empty_div, empty_div, default_dist_header, [], [], [], analysis_error_str, error_display, "", no_display

        # --- 3. Build UI Components ---

        # 3.1 Thickness Stats & Scan Details Table
        details_rows = [
            # ... (Report, Client, Equip, Part details - same as before) ...
            html.Tr([html.Td("Report No:"), html.Td(report_no)]),
            html.Tr([html.Td("Client Name:"), html.Td(client_name)]),
            html.Tr([html.Td("Address:"), html.Td(address)]),
            html.Tr([html.Td("Date:"), html.Td(date)]),
            html.Tr([html.Td("PO Number:"), html.Td(po_number)]),
            html.Tr([html.Td("Date Inspection:"), html.Td(date_inspection)]),
            html.Tr([html.Td(html.Hr(), colSpan="2")]),
            html.Tr([html.Td("Equipment Make:"), html.Td(make)]),
            html.Tr([html.Td("Equipment Model:"), html.Td(model)]),
            html.Tr([html.Td("Equipment SR. No:"), html.Td(sr_no)]),
            html.Tr([html.Td("Calibration Due Date:"), html.Td(calibration_due_date)]),
            html.Tr([html.Td(html.Hr(), colSpan="2")]),
            html.Tr([html.Td("Part Name:"), html.Td(part_name)]),
            html.Tr([html.Td("Material:"), html.Td(material)]),
            html.Tr([html.Td("Drawing Number:"), html.Td(drawing_number)]),
            html.Tr([html.Td(html.Hr(), colSpan="2")]),
            # --- Analysis Parameters & Overall Stats ---
            html.Tr([html.Td("Analysis Parameters", style=modern_style["table_header"]), html.Td("")]),
            html.Tr([html.Td("Analysis Type:"), html.Td(f"Fixed Range ({NUM_MAIN_ZONES} zones)")]),
            html.Tr([html.Td("Minimum Threshold:"), html.Td(f"{min_val:.2f} {unit}")]),
            html.Tr([html.Td("Maximum Threshold:"), html.Td(f"{max_val:.2f} {unit}")]),
            html.Tr([html.Td("Nominal Thickness (T):"), html.Td(f"{nominal_thickness:.2f} {unit}" if nominal_thickness is not None else "N/A")]),
            html.Tr([html.Td("Overall Statistics", style=modern_style["table_header"]), html.Td("")]),
            html.Tr([html.Td("Min Thickness Found:"), html.Td(f"{overall_stats['min']:.2f} {unit}")]),
            html.Tr([html.Td("Max Thickness Found:"), html.Td(f"{overall_stats['max']:.2f} {unit}")]),
            html.Tr([html.Td("Average Thickness:"), html.Td(f"{overall_stats['mean']:.2f} {unit}")]),
            html.Tr([html.Td("Median Thickness:"), html.Td(f"{overall_stats['median']:.2f} {unit}")]),
            html.Tr([html.Td("Standard Deviation:"), html.Td(f"{overall_stats['std']:.2f} {unit}")]),
            html.Tr([html.Td("Total Valid Cells:"), html.Td(f"{overall_stats['total_valid_cells']}")])
        ]
        thickness_stats_component = html.Div([
            html.Table(html.Tbody(details_rows), className="table table-sm table-borderless")
        ])

        # 3.2 Color Distribution Bar and Table
        dist_bar_segments = []
        dist_table_rows = []
        summary_table_data = []
        summary_table_styles = []

        dist_table_rows.append(html.Thead(html.Tr([
                html.Th("Zone", style=modern_style["table_header"]),
                html.Th("Thickness Range ({unit})", style=modern_style["table_header"]),
                html.Th("Coverage", style=modern_style["table_header"]),
                html.Th("Count", style=modern_style["table_header"])
            ])))

        dist_table_body_rows = []
        # Iterate through zone_stats which are in the correct order (Below, 1..N, Above)
        for zone in zone_stats:
            color = zone['color']
            coverage = zone['coverage']
            safe_key = color.replace('#', '')
            bar_style_key = f"dist_bar_{safe_key}"
            row_style_key = f"category_row_{safe_key}"

            if coverage > 0:
                dist_bar_segments.append(
                    html.Div(
                        style={**modern_style.get(bar_style_key, {}), "width": f"{coverage * 100:.1f}%"},
                        children=f"{coverage:.1%}"
                    )
                )

            dist_table_body_rows.append(html.Tr([
                html.Td(zone['name'], style=modern_style.get(row_style_key, {})),
                html.Td(zone['threshold_value_range_str_mm']),
                html.Td(f"{coverage:.1%}"),
                html.Td(f"{zone['count']}")
            ]))

            # Data for area summary table
            summary_table_data.append({
                "category": zone['name'],
                "threshold_value_range": zone['threshold_value_range_str_mm'],
                "coverage": coverage,
                "count": zone['count'],
                "avg_thickness": zone['avg_thickness'],
            })

            summary_table_styles.append({
                'if': {'filter_query': f'{{category}} = "{zone["name"]}"'},
                'style': modern_style.get(row_style_key, {})
            })

        # Add total row to summary table data
        summary_table_data.append({
            "category": "Total Valid", # Changed label slightly
            "threshold_value_range": "Overall",
            "coverage": 1.0 if overall_stats['total_valid_cells'] > 0 else 0.0,
            "count": overall_stats['total_valid_cells'],
            "avg_thickness": overall_stats['mean'],
        })
        summary_table_styles.append({
             'if': {'filter_query': '{category} = "Total Valid"'},
             'style': {'fontWeight': 'bold', 'borderTop': f'2px solid {DARK_GRAY}'}
        })

        color_distribution_component = html.Div([
            html.Div(dist_bar_segments, style=modern_style["color_distribution_bar_container"]),
            html.Table(dist_table_rows + [html.Tbody(dist_table_body_rows)], className="table table-sm table-borderless")
        ])

        # 3.3 Warnings (e.g., data outside measured range, if T provided)
        warning_message = ""
        if overall_stats['total_valid_cells'] > 0:
             if overall_stats['min'] < min_val or overall_stats['max'] > max_val:
                  warning_message += f"Note: Measured data ({overall_stats['min']:.2f}-{overall_stats['max']:.2f} {unit}) extends beyond the specified Min/Max range ({min_val:.2f}-{max_val:.2f} {unit}). "
             if nominal_thickness is not None and (nominal_thickness < overall_stats['min'] or nominal_thickness > overall_stats['max']):
                 warning_message += f"Note: Chosen thickness T ({nominal_thickness:.2f} {unit}) is greater than measured data range. "

        warning_style = {**modern_style["warning_alert"], 'display': 'block'} if warning_message else no_display

        # --- 4. Return Components ---
        return (
            thickness_stats_component,
            color_distribution_component,
            distribution_header, # Pass dynamic header
            critical_areas_data,
            summary_table_data,
            summary_table_styles,
            input_error_msg,    # Empty if no errors
            input_error_style,  # no_display if no errors
            warning_message,
            warning_style
        )
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

    # Clientside callback for printing (remains the same, ensure CSS covers new styles)
    # app.clientside_callback(
    #     """
    #     function(n_clicks) {
    #         // ... (print function code - check CSS injection includes styles for Below/Above Min/Max) ...
    #         if (n_clicks > 0 && n_clicks !== window.dash_clientside_print_last_click) {
    #             window.dash_clientside_print_last_click = n_clicks; // Prevent multi-trigger
    #             var printContents = document.getElementById('results-print-area').innerHTML;
    #             var originalContents = document.body.innerHTML;
    #             var originalTitle = document.title;

    #             var reportNoElement = document.querySelector("#results-print-area table tbody tr:first-child td:last-child");
    #              if (reportNoElement) {
    #                  // Robust check for textContent existence
    #                  const reportNoText = reportNoElement.textContent || reportNoElement.innerText || "";
    #                  document.title = "Report_" + reportNoText.trim().replace(/[^a-zA-Z0-9]/g, '_'); // Sanitize title
    #              }


    #             // Optional: Add basic print styles
    #             var style = document.createElement('style');
    #             style.media = 'print';
    #             style.innerHTML = `
    #                 @page { size: auto; margin: 0.5in; }
    #                 body { margin: 0; padding: 0; font-family: Arial, sans-serif; }
    #                 .container { width: 100%; }
    #                 h3 { margin-top: 1em; margin-bottom: 0.5em; page-break-after: avoid; }
    #                 table { width: 100%; border-collapse: collapse; margin-bottom: 1em; }
    #                 th, td { border: 1px solid #ddd; padding: 4px; text-align: left; font-size: 9pt; word-wrap: break-word; } /* Added word-wrap */
    #                 thead th { background-color: #f2f2f2; font-weight: bold; }
    #                 .table-borderless th, .table-borderless td { border: none; }
    #                 #color-distribution .table-borderless th, #color-distribution .table-borderless td { padding: 2px 4px;}
    #                 .alert { padding: 8px; margin-bottom: 1em; border: 1px solid transparent; border-radius: .25rem; font-size: 9pt; color-adjust: exact; -webkit-print-color-adjust: exact; } /* Added color-adjust */
    #                 .alert-danger { background-color: #f8d7da !important; border-color: #f5c6cb !important; color: #721c24 !important; }
    #                 .alert-warning { background-color: #fff3cd !important; border-color: #ffeeba !important; color: #856404 !important; }
    #                 /* Add specific background colors for rows in print */
    #                 ${Object.entries(modern_style)
    #                     .filter(([key, value]) => key.startsWith('category_row_'))
    #                     .map(([key, value]) => `[data-dash-is-loading="false"] tr td[style*="background-color: ${value.backgroundColor}"], [data-dash-is-loading="false"] tr[style*="background-color: ${value.backgroundColor}"] td { background-color: ${value.backgroundColor} !important; color-adjust: exact; -webkit-print-color-adjust: exact; }`)
    #                     .join('\n')}
    #                  /* Ensure total row border prints */
    #                 tr[style*="borderTop: 2px solid"] { border-top: 2px solid ${DARK_GRAY} !important; }
    #                 tr[style*="borderTop: 2px solid"] td { border-top: 2px solid ${DARK_GRAY} !important; }
    #                 /* Hide buttons in print */
    #                 #back-button, #print-button, #input-error:empty, #general-warning:empty { display: none !important; } /* Hide empty alerts too */
    #                  /* Style distribution bar for print */
    #                 #color-distribution-bar-container { display: flex !important; border: 1px solid #ccc !important; height: 20px !important; line-height: 20px !important; font-size: 8pt !important; margin-bottom: 5px !important; color-adjust: exact; -webkit-print-color-adjust: exact;}
    #                 #color-distribution-bar-container > div { height: 100% !important; float: none !important; color-adjust: exact; -webkit-print-color-adjust: exact;}
    #                 #color-distribution-bar-container > div[style*="background-color"] { color-adjust: exact; -webkit-print-color-adjust: exact;} /* Force background color print */
    #              `;
    #             document.head.appendChild(style);

    #             document.body.innerHTML = '<div class="container">' + printContents + '</div>';
    #             // Delay print slightly to allow styles to apply
    #             setTimeout(() => {
    #                  window.print();
    #                  // Cleanup MUST happen after print dialog closes/cancels
    #                  // This is tricky - best bet is to restore immediately, but styles might flash
    #                  document.head.removeChild(style);
    #                  document.body.innerHTML = originalContents;
    #                  document.title = originalTitle;
    #                  // Re-initialize or rebind might be needed if complex interactions are broken
    #                  // window.location.reload(); // Avoid if possible
    #             }, 250); // 250ms delay

    #             return 'printed: ' + n_clicks;
    #         }
    #         return '';
    #     }
    #     """,
    #     Output("dummy-print-output", "children"),
    #     Input("print-button", "n_clicks"),
    #     State("results-print-area", "children"), # Pass state to access styles if needed
    #     prevent_initial_call=True
    # )