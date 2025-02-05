# import dash 
import io
import base64
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import webview
from waitress import serve
import threading
import sys,time

def expand_data(df, OuterDia, TestArea, H, TH):
    pv = df.to_numpy()
    # Dimensions
    total_circumference = np.pi * OuterDia
    height = H  # mm
    total_height = TH  # mm
    fill_value=-1

    # Calculate the expansion factor
    expansion_factor_cols = (total_circumference / TestArea)
    expansion_factor_rows = (total_height / height)
    rows, cols = pv.shape
    # Generate expanded DataFrame
    num_cols = int(expansion_factor_cols * cols)
    num_rows = int(expansion_factor_rows * rows)
    expanded_df = pd.DataFrame(columns=range(num_cols), index=range(num_rows))

    # Fill values into the expanded DataFrame
    expanded_df.iloc[:rows, :cols] = df.values
    expanded_df.fillna(fill_value, inplace=True)

    return expanded_df

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

variable_values = {
    "OuterDia": "1",
    "TestArea": "1",
    "height": "1",
    "TotalHeight": "1"
}

# App layout
app.layout = html.Div([
    html.Div([
    html.H1("Dynamic 2D & 3D Visualization from Excel Data", style={"color": "#2E3A59", "text-align": "center"}),
    dbc.Modal(
        [
            dbc.ModalHeader("Large Modal Header"),
            dbc.ModalBody("This is the content of a large modal. You can add more content here to make it as detailed as needed."),
            dbc.ModalFooter(
                dbc.Button("Close", id="close-modal", className="ml-auto", color="secondary")
            ),
        ],
        id="large-modal",
        is_open=False,
        size="lg"  # Set modal size to large
    ),

    # Upload Component
    dcc.Upload(
        id="upload-data",
        children=html.Button("Upload Excel File", style={"background-color": "#6A1B9A", "color": "white", "border": "none", "padding": "10px 20px", "cursor": "pointer", "font-size": "16px",  "border-radius": "8px", 
        "transition": "all 0.3s ease",
        "box-shadow": "0 4px 8px rgba(76, 175, 80, 0.3)"}),
        multiple=False,
        style={"margin-bottom": "20px", "text-align": "center"}
    ),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label':"Select Excel",'value':"0"}],
        value="0",  # Default value
        style={"width": "200px", "margin": "auto", "margin-bottom": "20px", "border-radius": "8px"}
    ),
    # Input fields in grid layout
    html.Div([
        html.Div([
            html.Label("Outer Diameter:", style={"font-size": "20px", "font-weight": "bold", "color": "#333"}),
            dcc.Input(id='input-OuterDia', type='text', placeholder='Enter Outer Diameter', style={"font-size": "18px", "padding": "12px", "width": "90%", "text-align": "center", "margin-bottom": "10px", "border-radius": "10px"}),
        ], style={"width": "40%", "display": "inline-block", "margin-right": "5%"}),

        html.Div([
            html.Label("Testing Area:", style={"font-size": "20px", "font-weight": "bold", "color": "#333"}),
            dcc.Input(id='input-TestArea', type='text', placeholder='Enter Testing Area', style={"font-size": "18px", "padding": "12px", "width": "90%", "text-align": "center", "margin-bottom": "10px", "border-radius": "10px"}),
        ], style={"width": "40%", "display": "inline-block"}),

        html.Div([
            html.Label("Height:", style={"font-size": "20px", "font-weight": "bold", "color": "#333"}),
            dcc.Input(id='input-height', type='text', placeholder='Enter Height', style={"font-size": "18px", "padding": "12px", "width": "90%", "text-align": "center", "margin-bottom": "10px", "border-radius": "10px"}),
        ], style={"width": "40%", "display": "inline-block", "margin-right": "5%", "margin-top": "20px"}),

        html.Div([
            html.Label("Total Height:", style={"font-size": "20px", "font-weight": "bold", "color": "#333"}),
            dcc.Input(id='input-TotalHeight', type='text', placeholder='Enter Total Height', style={"font-size": "18px", "padding": "12px", "width": "90%", "text-align": "center", "margin-bottom": "10px", "border-radius": "10px"}),
        ], style={"width": "40%", "display": "inline-block", "margin-top": "20px"}),

    ], style={"margin-bottom": "20px", "padding": "20px", "border-radius": "8px", "text-align": "center"}),

   # Buttons for 2D and 3D views
    html.Div([
        html.Button("2D View", id="btn-2d", n_clicks=0, style={
            "margin-right": "20px", 
            "background-color": "#6A1B9A",  # Light Green
            "color": "white", 
            "border": "none", 
            "padding": "15px 30px", 
            "cursor": "pointer", 
            "font-size": "16px", 
            "border-radius": "8px", 
            "transition": "all 0.3s ease",
            "box-shadow": "0 4px 8px rgba(76, 175, 80, 0.3)"  # Soft shadow for depth
        }, className="btn-animated"),
        html.Button("3D View", id="btn-3d", n_clicks=0, style={
            "background-color": "#6A1B9A",  # Light Green (same as 2D View)
            "color": "white", 
            "border": "none", 
            "padding": "15px 30px", 
            "cursor": "pointer", 
            "font-size": "16px", 
            "border-radius": "8px", 
            "transition": "all 0.3s ease",
            "box-shadow": "0 4px 8px rgba(76, 175, 80, 0.3)"  # Soft shadow for depth
        }, className="btn-animated"),
    ], style={"display": "flex", "justify-content": "center", "gap": "20px", "margin": "20px 0"}),



    # Graph Output
    dcc.Graph(id="graph", style={"height": "80vh", "width": "100%", "background-color": "#FFFFFF"}),

    # Status Message
    html.Div(id="status-message", style={"margin-top": "20px", "color": "#D32F2F", "text-align": "center"}),
    # html.Div([
    #     html.Button("Review", id="open-modal", n_clicks=0, style={
    #         "margin-right": "20px", 
    #         "background-color": "#6A1B9A",  # Light Green
    #         "color": "white", 
    #         "border": "none", 
    #         "padding": "15px 30px", 
    #         "cursor": "pointer", 
    #         "font-size": "16px", 
    #         "border-radius": "8px", 
    #         "transition": "all 0.3s ease",
    #         "box-shadow": "0 4px 8px rgba(76, 175, 80, 0.3)"  # Soft shadow for depth
    #     }, className="btn-animated"),
    # ], style={"display": "flex", "justify-content": "center", "gap": "20px", "margin": "20px 0"}),
    html.Div(id='output', style={'margin-top': '20px'}),
]),])

# @app.callback(
#     Output("large-modal", "is_open"),
#     [Input("open-modal", "n_clicks"), Input("close-modal", "n_clicks")],
#     [State("large-modal", "is_open")]
# )
# def toggle_modal(open_clicks, close_clicks, is_open):
#     if open_clicks or close_clicks:
#         return not is_open
#     return is_open

@app.callback(
    Output('output', 'children'),
    [Input('input-OuterDia', 'value'),
     Input('input-TestArea', 'value'),
     Input('input-height', 'value'),
     Input('input-TotalHeight', 'value')]
)

def update_variables(OuterDia, TestArea, height, TotalHeight):
    global variable_values
    variable_values['OuterDia'] = OuterDia if OuterDia else variable_values['OuterDia']
    variable_values['TestArea'] = TestArea if TestArea else variable_values['TestArea']
    variable_values['height'] = height if height else variable_values['height']
    variable_values['TotalHeight'] = TotalHeight if TotalHeight else variable_values['TotalHeight']

# app.callback for generating the graph
@app.callback(
    Output('dropdown', 'options'),
    Output("graph", "figure"),
    Output("status-message", "children"),
    [Input("upload-data", "contents"), Input("btn-2d", "n_clicks"), Input("btn-3d", "n_clicks"), Input('dropdown', 'value')],
    [State("upload-data", "filename")],
    prevent_initial_call=True
)

def update_graph(contents, n_clicks_2d, n_clicks_3d, value, filename):
    # Initialize an empty figure
    fig = go.Figure()

    # Check if a file has been uploaded
    if contents and filename:
        try:
            # Decode the uploaded file
            content_type, content_string = contents.split(",")
            decoded = base64.b64decode(content_string)
            file_data = io.BytesIO(decoded)

            ef = pd.ExcelFile(file_data)
            ret = [{'label': f"{label}", "value": f"{i}"} for i, label in enumerate(ef.sheet_names)]
            df = ef.parse(int(value))

            nan_idx = df[df.isnull().all(axis=1)].index[0]
            df = df[:nan_idx]
            df = df.drop(columns=['Sr. No'])

            a, b, c, d = int(variable_values['OuterDia']), int(variable_values['TestArea']), int(variable_values['height']), int(variable_values['TotalHeight'])

            expanded_df = expand_data(df, a, b, c, d)
            property_value = expanded_df.to_numpy()
            property_value = property_value[::-1]

            rows, cols = property_value.shape

            # Generate 3D cylinder grid
            radius = a // 2  # radius of the cylinder
            height = rows  # height of the cylinder

            # Create the cylinder using meshgrid for surface
            theta = np.linspace(0, 2 * np.pi, cols)
            z = np.linspace(0, height, rows)
            theta, z_grid = np.meshgrid(theta, z)

            # Convert to x and y coordinates for the surface
            x = radius * np.cos(theta)
            y = radius * np.sin(theta)
            colorscale = [
                [0.0, 'gray'],       # Placeholder value color
                [0.01, 'red'],       # Start of actual data range
                [0.20, 'yellow'],
                [1.0, 'green']       # End of data range
            ]
            # Create hover text for row and column
            hover_text = np.empty_like(x, dtype=object)
            for i in range(rows):
                for j in range(cols):
                    hover_text[i, j] = f"Row: {i}, Column: {j}, value: {property_value[i][j]}"

            # Determine which button was clicked
            if n_clicks_3d > n_clicks_2d:
                # Generate 3D visualization
                fig = go.Figure(data=[go.Surface(
                    z=z_grid,
                    x=x,
                    y=y,
                    cmin=13,    # Minimum of actual data range
                    cmax=25,     # Maximum of actual data range
                    colorscale=colorscale,
                    surfacecolor=property_value,
                    colorbar=dict(title="Property Value"),
                    text=hover_text,  # Add hover text
                    hoverinfo='text'  # Show text on hover
                )])
                for i in range(rows):
                    fig.add_trace(go.Scatter3d(
                        x=x[i, :],
                        y=y[i, :],  # Constant height for the line
                        z=np.full(cols, z[i]),
                        mode='lines',
                        line=dict(color='black', width=2),
                        name=f"Row {i}",
                        showlegend=False,
                    ))
                for j in range(cols):
                    fig.add_trace(go.Scatter3d(
                        x=x[:, j],
                        y=y[:, j],  # All row heights for the line
                        z=z,
                        mode='lines',
                        line=dict(color='black', width=1),
                        name=f"Angle {j}",
                        showlegend=False,
                    ))

                # Set axis labels and layout
                fig.update_layout(
                    scene=dict(
                        xaxis_title="X",
                        yaxis_title="Angular Position (Theta)",
                        zaxis_title='Height/Rows Z'
                    ), title=f"3D Heatmap Visualization, Cylinder with {rows} Rows and {cols} Columns",
                )

            else:
               # Generate 2D heatmap visualization
                fig = go.Figure(data=[go.Heatmap(
                    x=np.ravel(theta),
                    y=np.ravel(z_grid),
                    z=np.ravel(property_value),
                    colorscale=colorscale,
                    zmin=13,    # Minimum of actual data range
                    zmax=25,     # Maximum of actual data range
                    colorbar=dict(title="Property Value"),
                    text=hover_text,  # Add hover text
                    hoverinfo='text'  # Show text on hover
                )])
                fig.update_layout(
                    title="2D Heatmap Visualization",
                    xaxis=dict(title="Theta/Angle"),
                    yaxis=dict(title="Height/Z"),
                )

            return ret, fig, ""

        except Exception as e:
            return [], go.Figure(), f"Error: {e}"

    return [], go.Figure(), "No file uploaded."

if __name__ == "__main__":
    app.run_server(debug=True)
