from dash import html, Output, Input, callback,dcc
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
                UIComponents.create_input_field("THRESHOLD THICKNESS", "threshold-thickness"),
            ], style={"margin-bottom": "10px"}),

            html.Div([
                html.P("Incremental thickness for wall loss from 80% to each 1%, represented with a color code.", style={"font-size": "10px", "font-style": "italic", "color": "#777", "margin-bottom": "5px"})
            ], style={"margin-bottom": "8px"}),

        html.Div(
            id="validation-message",
            style={"color": "#D32F2F", "text-align": "center", "margin-bottom": "10px"}
        ),
    html.Div(
            dcc.Link(
                'Next',
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
            style={"textAlign": "center", "marginTop": "20px"}
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
    @callback(
    [Output("data-store", "data"), Output("validation-message", "children")],
    [Input("input-OuterDia", "value"), Input("input-TestArea", "value"), Input("input-Height", "value"), Input("input-TotalHeight", "value"),Input("nominal-thickness", "value"),Input("design-thickness","value"),Input("threshold-thickness","value")],
    prevent_initial_call=True)
    def update_store(outer_dia, test_area, height, total_height,nominal_thickness,design_thickness,threshold_thickness):
        """Show/hide upload button based on input validation."""
        if not all([outer_dia, test_area, height, total_height,nominal_thickness,design_thickness,threshold_thickness]):
            return None, "Please fill in all input fields to proceed"
        try:
            # Validate inputs are positive numbers
            values = [float(x) for x in [outer_dia, test_area, height, total_height]]
            if not all(v > 0 for v in values):
                return None, "All values must be positive numbers"
            elif height > total_height:
                return None, "Total Height must be greater than calculated height"

            return {"OD":outer_dia, "TA" : test_area,"HE": height,"TH": total_height, "NT": nominal_thickness, "DT":design_thickness, "TT":threshold_thickness}, ""

        except ValueError:
            return None, "All inputs must be valid numbers"
