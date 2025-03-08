from dash import html, Output, Input, callback, dcc, State
from components.UIComponents import UIComponents

"""Create the main application layout."""
layout = html.Div([
        html.H1(
            "Cylinder 2D & 3D Visualization",
            style={"color": "#2E3A59", "text-align": "center"}
        ),
        html.Div(
            id="status-message",
            style={"margin-top": "20px", "color": "#D32F2F", "text-align": "center"}
        ),
        # Input Fields
            html.Div([
                html.H3("INJOTECH INDIA PVT. LTD", style={"text-align": "center", "font-size": "18px"}),
                html.H5("WALL THICKNESS MEASUREMENT REPORT", style={"text-align": "center", "font-size": "14px", "margin-top": "5px"})
            ], style={"margin-bottom": "10px"}),

            html.Div([
                UIComponents.create_input_field("REPORT NO", "report-no"),
                UIComponents.create_input_field("CLIENT NAME", "client-name"),
                UIComponents.create_input_field("ADDRESS", "address"),
                UIComponents.create_date_picker("Date","date"),
            ], style={"margin-bottom": "8px"}),

            html.Div([
                UIComponents.create_input_field("PO NUMBER", "po-number"),
                UIComponents.create_input_field("DATE OF INSPECTION", "date-inspection"),
            ], style={"margin-bottom": "12px"}),

            html.Div([
                html.H6("EQUIPMENT DETAILS", style={"font-weight": "bold", "margin-bottom": "5px", "font-size": "12px"})
            ]),

            html.Div([
                UIComponents.create_input_field("MAKE", "make"),
                UIComponents.create_input_field("MODEL", "model"),
                UIComponents.create_input_field("SR. NO.", "sr-no"),
                UIComponents.create_date_picker("CALIBRATION DUE DATE", "calibration-due-date"),
            ], style={"margin-bottom": "12px"}),

            html.Div([
                html.H6("PART DETAILS", style={"font-weight": "bold", "margin-bottom": "5px", "font-size": "12px"})
            ]),

            html.Div([
                UIComponents.create_input_field("PART NAME", "part-name"),
                UIComponents.create_input_field("MATERIAL", "material"),
                UIComponents.create_input_field("DRAWING NUMBER", "drawing-number"),
            ], style={"margin-bottom": "8px"}),

            html.Div([
                html.H6("DIMENSIONS", style={"font-weight": "bold", "margin-bottom": "5px", "font-size": "12px"})
            ]),

            html.Div([
                UIComponents.create_input_field("Outer Diameter", "input-OuterDia"),
                UIComponents.create_input_field("Test Area","input-TestArea"),
                UIComponents.create_input_field("Height", "input-Height"),
                UIComponents.create_input_field("Total Height", "input-TotalHeight"),
                UIComponents.create_input_field("NOMINAL THICKNESS", "nominal-thickness"),
                UIComponents.create_input_field("DESIGN THICKNESS", "design-thickness"),
            ], style={"margin-bottom": "10px"}),

            html.Div([
                html.H6("THRESHOLD PERCENTAGE TYPE", style={"font-weight": "bold", "margin-bottom": "5px", "font-size": "12px"})
            ]),

            html.Div([
                dcc.RadioItems(
                    id='threshold-type-toggle',
                    options=[
                        {'label': 'Nominal Thickness (%)', 'value': 'nominal'},
                        {'label': 'Design Thickness (%)', 'value': 'design'},
                        {'label': 'Relative to Minimum Thickness (%)', 'value': 'custom'}
                    ],
                    value='nominal',  # Default value
                    inline=True # Display options in a line
                )
            ], style={"margin-bottom": "8px"}),

            html.Div([
                UIComponents.create_input_field("THRESHOLD Value", "threshold-thickness"),
            ], style={"margin-bottom": "10px"}),


            html.Div([
                html.P("Incremental thickness for wall loss from 80% to each 1%, represented with a color code.", style={"font-size": "10px", "font-style": "italic", "color": "#777", "margin-bottom": "5px"})
            ], style={"margin-bottom": "8px"}),

        html.Div(
            id="validation-message",
            style={"color": "#D32F2F", "text-align": "center", "margin-bottom": "10px"}
        ),
        
        # Message for incomplete form
        html.Div(
            id="form-status-message",
            style={"color": "#1976D2", "text-align": "center", "margin-bottom": "10px", "font-weight": "bold"}
        ),
        
        # Next button container (will be shown/hidden based on validation)
        html.Div(
            id="next-button-container",
            children=[
                dcc.Link(
                    'Next',
                    id="next-button",
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
                )
            ],
            style={"textAlign": "center", "marginTop": "20px", "display": "none"}  # Hidden by default
        )
    ],
        style={
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
    # New callback to populate form fields with stored data
    @callback(
        [Output("report-no", "value"),
         Output("client-name", "value"),
         Output("address", "value"),
         Output("date", "date"),
         Output("po-number", "value"),
         Output("date-inspection", "value"),
         Output("make", "value"),
         Output("model", "value"),
         Output("sr-no", "value"),
         Output("calibration-due-date", "date"),
         Output("part-name", "value"),
         Output("material", "value"),
         Output("drawing-number", "value"),
         Output("input-OuterDia", "value"),
         Output("input-TestArea", "value"),
         Output("input-Height", "value"),
         Output("input-TotalHeight", "value"),
         Output("nominal-thickness", "value"),
         Output("design-thickness", "value"),
         Output("threshold-thickness", "value"),
         Output("threshold-type-toggle", "value"),
         Output("form-status-message", "children"),
         Output("next-button-container", "style")],
        [Input("data-store", "data")],
        [State("data-store", "storage_type")]
    )
    def populate_form_fields(stored_data, storage_type):
        """Populate form fields with previously stored data from session storage."""
        # Default values for all fields when no data is available
        default_values = {
            "report_no": "",
            "client_name": "",
            "address": "",
            "date": None,
            "po_number": "",
            "date_inspection": "",
            "make": "",
            "model": "",
            "sr_no": "",
            "calibration_due_date": None,
            "part_name": "",
            "material": "",
            "drawing_number": "",
            "OD": "", 
            "TA": "",
            "HE": "",
            "TH": "",
            "NT": "",
            "DT": "",
            "TT": "",
            "threshold_type": "nominal"
        }
        
        # Default button style - hidden
        button_style = {"textAlign": "center", "marginTop": "20px", "display": "none"}
        status_message = "Please fill in all required fields to proceed"
        
        # If no stored data, return default values
        if not stored_data:
            return (
                "", "", "", None, "", "", 
                "", "", "", None, 
                "", "", "", 
                "", "", "", "", "", "", "", "nominal",
                status_message, button_style
            )
        
        # Merge stored data with defaults to handle any missing fields
        data = {**default_values, **stored_data}
        
        # Check if critical fields for visualization are filled
        critical_fields = [
            data["OD"], data["TA"], data["HE"], data["TH"], 
            data["NT"], data["DT"], data["TT"]
        ]
        
        # Determine if we should show the Next button
        all_filled = all(critical_fields)
        valid_values = False
        
        if all_filled:
            try:
                # Validate critical inputs are positive numbers
                values = [float(x) for x in critical_fields[:-1]]  # Exclude threshold_type
                valid_values = all(v > 0 for v in values)
                
                # Additional validation
                height_valid = float(data["HE"]) <= float(data["TH"])
                threshold_valid = 0 <= float(data["TT"]) <= 100
                
                if valid_values and height_valid and threshold_valid:
                    button_style = {"textAlign": "center", "marginTop": "20px", "display": "block"}
                    status_message = "All fields are complete. You can proceed!"
                elif not height_valid:
                    status_message = "Total Height must be greater than calculated height"
                elif not threshold_valid:
                    status_message = "Threshold Percentage must be between 0 and 100"
                else:
                    status_message = "All measurement values must be positive numbers"
            except (ValueError, TypeError):
                status_message = "All measurement inputs must be valid numbers"
        
        # Return values for all form fields
        return (
            data["report_no"],
            data["client_name"],
            data["address"],
            data["date"],
            data["po_number"],
            data["date_inspection"],
            data["make"],
            data["model"],
            data["sr_no"],
            data["calibration_due_date"],
            data["part_name"],
            data["material"],
            data["drawing_number"],
            data["OD"],
            data["TA"],
            data["HE"],
            data["TH"],
            data["NT"],
            data["DT"],
            data["TT"],
            data["threshold_type"],
            status_message,
            button_style
        )
    
    @callback(
    [Output("data-store", "data"), 
     Output("validation-message", "children"),
     Output("next-button-container", "style", allow_duplicate=True),
     Output("form-status-message", "children", allow_duplicate=True)],
    [Input("report-no", "value"),
     Input("client-name", "value"),
     Input("address", "value"),
     Input("date", "date"),
     Input("po-number", "value"),
     Input("date-inspection", "value"),
     Input("make", "value"),
     Input("model", "value"),
     Input("sr-no", "value"),
     Input("calibration-due-date", "date"),
     Input("part-name", "value"),
     Input("material", "value"),
     Input("drawing-number", "value"),
     Input("input-OuterDia", "value"), 
     Input("input-TestArea", "value"), 
     Input("input-Height", "value"), 
     Input("input-TotalHeight", "value"),
     Input("nominal-thickness", "value"),
     Input("design-thickness", "value"),
     Input("threshold-thickness", "value"), 
     Input("threshold-type-toggle", "value")],
    prevent_initial_call=True)
    def update_store(report_no, client_name, address, date, po_number, date_inspection,
                    make, model, sr_no, calibration_due_date, part_name, material, drawing_number,
                    outer_dia, test_area, height, total_height, nominal_thickness, design_thickness, 
                    threshold_percentage, threshold_type):
        """Update data store and control Next button visibility based on input validation."""
        # Default styles - button hidden
        button_style = {"textAlign": "center", "marginTop": "20px", "display": "none"}
        status_message = "Please fill in all required fields to proceed"
        
        # Store all form values in a dictionary (even if some are incomplete)
        all_data = {
            # Company and report info
            "report_no": report_no,
            "client_name": client_name,
            "address": address,
            "date": date,
            "po_number": po_number,
            "date_inspection": date_inspection,
            
            # Equipment details
            "make": make,
            "model": model,
            "sr_no": sr_no,
            "calibration_due_date": calibration_due_date,
            
            # Part details
            "part_name": part_name,
            "material": material,
            "drawing_number": drawing_number,
            
            # Critical dimensions (required for visualization)
            "OD": outer_dia, 
            "TA": test_area,
            "HE": height,
            "TH": total_height, 
            "NT": nominal_thickness, 
            "DT": design_thickness, 
            "TT": threshold_percentage, 
            "threshold_type": threshold_type
        }
        
        # Check if critical fields for visualization are filled
        critical_fields = [outer_dia, test_area, height, total_height, nominal_thickness, design_thickness, threshold_percentage]
        if not all(critical_fields):
            return all_data, "Please fill in all measurement fields", button_style, status_message
        
        try:
            # Validate critical inputs are positive numbers
            values = [float(x) for x in critical_fields[:-1]]  # Exclude threshold_type
            if not all(v > 0 for v in values):
                return all_data, "All measurement values must be positive numbers", button_style, status_message
            elif float(height) > float(total_height):
                return all_data, "Total Height must be greater than calculated height", button_style, status_message

            if threshold_type in ['nominal', 'design', 'custom']:
                try:
                    threshold_value = float(threshold_percentage)
                    if not 0 <= threshold_value <= 100:
                        return all_data, "Threshold Percentage must be between 0 and 100", button_style, status_message
                except ValueError:
                    return all_data, "Threshold Percentage must be a valid number", button_style, status_message
            else:  # Should not reach here, but for safety
                return all_data, "Invalid Threshold Type selected", button_style, status_message

            # All validations passed - show the button and update the message
            button_style = {"textAlign": "center", "marginTop": "20px", "display": "block"}
            
            # Additional data validation for completeness (not blocking but informative)
            missing_fields = []
            if not report_no: missing_fields.append("Report No")
            if not client_name: missing_fields.append("Client Name")
            if not part_name: missing_fields.append("Part Name")
            
            if missing_fields:
                status_msg = f"Note: {', '.join(missing_fields)} not filled. You can still proceed."
            else:
                status_msg = "All fields are complete. You can proceed!"
            
            return all_data, "", button_style, status_msg

        except ValueError:
            return all_data, "All measurement inputs must be valid numbers", button_style, status_message