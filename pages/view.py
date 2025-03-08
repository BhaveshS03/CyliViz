import plotly.graph_objects as go
import numpy as np
from dash import html, Output, Input, callback, dcc, callback_context, State
from components.UIComponents import UIComponents
from components.DataProcessor import DataProcessor
from components.Visualizer import Visualizer
import time


layout = html.Div([
    # Add a back button at the top
        html.Div([
        html.Div([
            dcc.Link(
                html.Button(
                    "← Back to Input Form",
                    id="back-button",
                    style={
                        "backgroundColor": "#f0f0f0",
                        "border": "1px solid #ccc",
                        "borderRadius": "4px",
                        "padding": "8px 15px",
                        "cursor": "pointer",
                        "fontSize": "14px",
                        "fontWeight": "600",
                        "color": "#333",
                    }
                ),
                href='/', 
            )
        ], style={"textAlign": "left"}), # Removed marginLeft and marginTop from here to manage in parent

        html.Div([
            dcc.Link(
                html.Button(
                'View Detailed Results',
                id="results-button",
                style={
                        "backgroundColor": "#f0f0f0",
                        "border": "1px solid #ccc",
                        "borderRadius": "4px",
                        "padding": "8px 15px",
                        "cursor": "pointer",
                        "fontSize": "14px",
                        "fontWeight": "600",
                        "color": "#333",
                    }
                ),
                href=f'/results',
            )
        ],id="results-button-container",  style={ "display": "none"}),
    ], style={
        "display": "flex",           # Enable flexbox for horizontal layout
        "justify-content": "space-between", # Distribute space between the divs
        "align-items": "flex-start",   # Align items to the top
        "padding": "5px 5px",       # Add padding to the container for spacing from edges
        "width": "100%"              # Take full width of parent if needed, adjust as necessary
    }),
    # Upload Data 
    dcc.Upload(
        id="upload-data",
        children=UIComponents.create_button("Upload Excel File", "upload-button"),
        multiple=False,
        style={"margin-bottom": "20px", "text-align": "center", "marginTop": "20px"}
    ),
    
    # Select Excel - Hidden until file is uploaded
    html.Div([
        dcc.Dropdown(
            id='dropdown',
            options=[{'label': "Select Excel Sheet", 'value': "0"}],
            value="0",
            style={
                "width": "400px",
                "margin": "auto",
                "borderRadius": "8px"
            }
        )
    ], id="dropdown-container", style={"display": "none", "marginBottom": "20px"}),

    # View Buttons - Hidden until file is uploaded and sheet is selected
    html.Div([
        UIComponents.create_button("2D View", "btn-2d"),
        UIComponents.create_button("3D View", "btn-3d")
    ], 
    id="view-buttons-container",
    style={
        "display": "none",
        "justifyContent": "center",
        "gap": "20px",
        "margin": "20px 0"
    }),

    # Status
    html.Div(
        id="status-message",
        style={"color": "#D32F2F", "textAlign": "center", "margin": "20px 0", "fontWeight": "bold"}
    ),

    # Instructions div - shown when no file is uploaded
    html.Div([
        html.Div([
            html.H3("Visualization Instructions", style={"color": "#2E3A59", "textAlign": "center"}),
            html.Ol([
                html.Li("Upload your Excel file containing measurement data"),
                html.Li("Select the appropriate sheet from the dropdown"),
                html.Li("Choose between 2D and 3D visualization"),
                html.Li("After reviewing the visualization, proceed to Results")
            ], style={"textAlign": "left", "maxWidth": "450px", "margin": "0 auto", "paddingLeft": "30px"})
        ], style={"backgroundColor": "#f8f9fa", "padding": "20px", "borderRadius": "8px", "maxWidth": "500px", "margin": "30px auto", "boxShadow": "0 2px 5px rgba(0,0,0,0.1)"})
    ], id="instructions-container"),

    # Graph - Hidden until file is uploaded and sheet is selected
    html.Div([
        dcc.Graph(
            id="graph",
            style={"height": "70vh", "width": "100%", "backgroundColor": "#FFFFFF"}
        )
    ], id="graph-container", style={"display": "none", "flex": "1"}),
    
    # Results button - Hidden until visualization is shown

    # Add hidden data store for processed data
    # dcc.Store(id="prop-store", storage_type="session")
    html.Div(
    style={"textAlign": "center"}
    )
], style={'minHeight': '100vh', 'width': '100%', 'display': 'flex', 'flexDirection': 'column'})


def register_callbacks(app):
    # Create callback for managing component visibility
    @app.callback(
        [Output("dropdown-container", "style"),
         Output("view-buttons-container", "style"),
         Output("graph-container", "style"),
         Output("results-button-container", "style"),
         Output("instructions-container", "style")],
        [Input("upload-data", "contents"),
         Input("dropdown", "value"),
         Input("graph", "figure")]
    )
    def manage_component_visibility(contents, sheet_value, figure):
        """Control visibility of components based on user actions"""
        # Default states - all visualization components hidden
        dropdown_style = {"display": "none", "marginBottom": "20px"}
        buttons_style = {"display": "none", "justifyContent": "center", "gap": "20px"}
        graph_style = {"display": "none", "flex": "1"}
        results_style = {"textAlign": "center","display": "none"}
        instructions_style = {"display": "block"}
        
        # If file is uploaded, show dropdown
        if contents:
            dropdown_style["display"] = "block"
            instructions_style = {"display": "none"}
            
            # If sheet is selected (not the default "Select Excel" option)
            if sheet_value != None:
                buttons_style["display"] = "flex"
                
                # Check if figure data exists (initial empty figure has 0 or 1 traces)
                try:
                    if len(figure.get('data', [])) > 0:
                        graph_style["display"] = "block"
                        results_style["display"] = "block"
                except:
                    pass
        
        return dropdown_style, buttons_style, graph_style, results_style, instructions_style

    @app.callback(
        [Output('dropdown', 'options'),
         Output("graph", "figure"),
         Output("status-message", "children"),
         Output("prop-store", "data")],
        [Input("upload-data", "contents"),
         Input("btn-2d", "n_clicks"),
         Input("btn-3d", "n_clicks"),
         Input('dropdown', 'value'),
         Input("data-store", "data")],
        prevent_initial_call=True
    )
    def update_visualization(contents, n_clicks_2d, n_clicks_3d, sheet_value, data):
        """Update visualization based on user inputs and uploaded data."""
        ctx = callback_context
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None
        
        # Initialize with empty figure
        empty_figure = go.Figure()
        empty_figure.update_layout(
            title="No data to display",
            xaxis=dict(title="X"),
            yaxis=dict(title="Y"),
            template="plotly_white"
        )
        
        # Check for input form data
        if not data:
            return [], empty_figure, "Please go back and fill the input form first.", {}
            
        # Check if file is uploaded
        if not contents:
            return [], empty_figure, "Please upload an Excel file.", {}
            
        try:
            # Get parameters from input form
            outer_dia = data["OD"]
            test_area = data["TA"]
            height = data["HE"]
            total_height = data["TH"]
            nominal_thickness = int(data["NT"])
            design_thickness = int(data["DT"])
            threshold_percentage = int(data["TT"])
            threshold_type = str(data["threshold_type"])


            # If just uploaded or sheet changed, process the Excel file
            if trigger_id in ["upload-data", "dropdown"]:
                if sheet_value is None:
                    df, sheet_options = DataProcessor.process_excel_data(contents, 0)
                    return sheet_options, empty_figure, "Select a sheet to continue.", {}
                else:
                    df, sheet_options = DataProcessor.process_excel_data(contents, int(sheet_value))
            else:
                # For visualization type changes, reuse the sheet value
                sheet_value = "0" if sheet_value is None else sheet_value
                df, sheet_options = DataProcessor.process_excel_data(contents, int(sheet_value))
            
            if threshold_type != None:
                print(threshold_type)
                if threshold_type == "nominal":
                    thickness = nominal_thickness
                elif threshold_type == "design":
                    thickness = design_thickness
                else:
                    thickness = np.max(df) 
            # Process data for visualization
            expanded_df = DataProcessor.expand_data(
                df,
                int(outer_dia),
                int(test_area),
                int(height),
                int(total_height)
            )

            property_value = expanded_df.to_numpy()[::-1]
            rows, cols = property_value.shape
            radius = int(outer_dia) // 2
    
            # Determine view type based on button click
            if trigger_id == "btn-3d" or (not trigger_id and n_clicks_3d):
                view_type = '3d'
            else:
                view_type = '2d'  # Default to 2D view

            # Create visualization
            if view_type == '3d':
                fig = Visualizer.create_3d_figure(
                    property_value, radius, rows, cols, 
                    thickness, threshold_percentage
                )
            else:
                fig = Visualizer.create_2d_figure(
                    df.to_numpy(), property_value, rows, cols, 
                    thickness, threshold_percentage
                )

            success_message = f"Displaying {view_type.upper()} visualization. You can now view detailed results."
            
            return sheet_options, fig, success_message, {
                "property_value": property_value, 
                "T": thickness,  
                "TT": threshold_percentage,
                
            }
            
        except Exception as e:
            print(str(e), thickness)
            return [], empty_figure, f"Error: {str(e)}", {}