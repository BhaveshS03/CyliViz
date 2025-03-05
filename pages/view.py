import plotly.graph_objects as go
from dash import html, Output, Input, callback, dcc,callback_context
from components.UIComponents import UIComponents
from components.DataProcessor import DataProcessor
from components.Visualizer import Visualizer


layout = html.Div([
    # Upload Data 
    dcc.Upload(
        id="upload-data",
        children=UIComponents.create_button("Upload Excel File", "upload-button"),
        multiple=False,
        style={"margin-bottom": "20px", "text-align": "center"}
    ),
    #Select Excel
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': "Select Excel", 'value': "0"}],
        value="0",
        style={
            "width": "400px",
            "margin": "auto",
            "border-radius": "8px"
        }
    ),

    # View Buttons
    html.Div([
        UIComponents.create_button("2D View", "btn-2d"),
        UIComponents.create_button("3D View", "btn-3d")
    ], style={
        "display": "flex",
        "justify-content": "center",
        "gap": "20px",
        "margin": "20px 0"
    }),

    # Status
    html.Div(
        id="status-message",
        style={"color": "#D32F2F", "text-align": "center", "margin-bottom": "10px"}
    ),

    # Graph
    dcc.Graph(
        id="graph",
        style={"height": "80vh", "width": "100%", "background-color": "#FFFFFF"}
    ),
    html.Div(
    dcc.Link(
        'Results',
        href='/results',
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
    style={"textAlign": "center"}
)
], style={'height': '100vh', 'width': '100vw', 'display': 'flex', 'flexDirection': 'column'})


def register_callbacks(app):
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

    def update_visualization(contents, n_clicks_2d, n_clicks_3d, sheet_value,data):
        """Update visualization based on user inputs and uploaded data."""
        print(contents, sheet_value)
        if not data:
            return [], go.Figure(), "Please Enter the Values",{}
        if not all([contents]):
            return [], go.Figure(), "Please upload an Excel file.",{}
        try:
            outer_dia = data["OD"]
            test_area = data["TA"]
            height = data["HE"]
            total_height = data["TH"]
            nominal_thickness = int(data["NT"])
            design_thickness = int(data["DT"])
            threshold_thickness = int(data["TT"])
            if sheet_value == None: sheet_value=0
            df, sheet_options = DataProcessor.process_excel_data(contents, int(sheet_value))
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
    
            ctx = callback_context
            if not ctx.triggered:
                view_type = '2d' # default view
            else:
                button_id = ctx.triggered[0]['prop_id'].split('.')[0]
                view_type = '3d' if button_id == "btn-3d" else '2d'

            if view_type == '3d':
                fig = Visualizer.create_3d_figure(property_value, radius, rows, cols, nominal_thickness, design_thickness, threshold_thickness)
            else:
                fig = Visualizer.create_2d_figure(df.to_numpy(), property_value, rows, cols, nominal_thickness, design_thickness, threshold_thickness)

            return sheet_options, fig, "", {"property_value": property_value, "NT":nominal_thickness, "DT":design_thickness, "TT":threshold_thickness }
        except Exception as e:
            print(str(e))
            return [], go.Figure(), f"Error: {str(e)}",{}

