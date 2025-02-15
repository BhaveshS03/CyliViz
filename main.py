import io
import base64
from typing import List, Tuple, Dict, Any
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

# Constants
COLORSCALE = [
    [0.0, 'gray'],    # Placeholder value color
    [0.01, 'red'],    # Start of actual data range
    [0.20, 'yellow'],
    [1.0, 'green']    # End of data range
]

VALUE_RANGE = {"min": 13, "max": 25} # Need to use

def create_input_field(label: str, input_id: str) -> html.Div:
    """Create a styled input field with label."""
    return html.Div([
        html.Label(f"{label}:", style={
            "font-size": "20px",
            "font-weight": "bold",
            "color": "#333"
        }),
        dcc.Input(
            id=input_id,
            type='text',
            placeholder=f'Enter {label}',
            style={
                "font-size": "18px",
                "padding": "12px",
                "width": "90%",
                "text-align": "center",
                "margin-bottom": "10px",
                "border-radius": "10px"
            }
        )
    ], style={"width": "40%", "display": "inline-block", "margin-right": "5%" if label in ["Outer Diameter", "Height"] else "0"})

def create_button(text: str, button_id: str) -> html.Button:
    """Create a styled button."""
    return html.Button(
        text,
        id=button_id,
        n_clicks=0,
        style={
            "background-color": "#6A1B9A",
            "color": "white",
            "border": "none",
            "padding": "15px 30px",
            "cursor": "pointer",
            "font-size": "16px",
            "border-radius": "8px",
            "transition": "all 0.3s ease",
            "box-shadow": "0 4px 8px rgba(76, 175, 80, 0.3)"
        },
        className="btn-animated"
    )

def create_app_layout() -> html.Div:
    """Create the main application layout."""
    return html.Div([
        html.H1(
            "Dynamic 2D & 3D Visualization from Excel Data",
            style={"color": "#2E3A59", "text-align": "center"}
        ),
        html.Div(
            id="status-message",
            style={"margin-top": "20px", "color": "#D32F2F", "text-align": "center"}
        ),

        # Input Fields
        html.Div([
            create_input_field("Outer Diameter", "input-OuterDia"),
            create_input_field("Testing Area", "input-TestArea"),
            create_input_field("Height", "input-height"),
            create_input_field("Total Height", "input-TotalHeight"),
        ], style={
            "margin-bottom": "20px",
            "padding": "20px",
            "border-radius": "8px",
            "text-align": "center"
        }),
        
        # Input validation message
        html.Div(
            id="validation-message",
            style={"color": "#D32F2F", "text-align": "center", "margin-bottom": "10px"}
        ),
        
        # Upload Component (initially hidden)
        html.Div([
            dcc.Upload(
                id="upload-data",
                children=create_button("Upload Excel File", "upload-button"),
                multiple=False,
                style={"margin-bottom": "20px", "text-align": "center"}
            ),
        ], id="upload-container", style={"display": "none"}),
        
        # Sheet Selection Dropdown
        dcc.Dropdown(
            id='dropdown',
            options=[{'label': "Select Excel", 'value': "0"}],
            value="0",
            style={
                "width": "200px",
                "margin": "auto",
                "margin-bottom": "20px",
                "border-radius": "8px"
            }
        ),
        
        # View Buttons
        html.Div([
            create_button("2D View", "btn-2d"),
            create_button("3D View", "btn-3d"),
        ], style={
            "display": "flex",
            "justify-content": "center",
            "gap": "20px",
            "margin": "20px 0"
        }),
        
        # Graph and Status
        dcc.Graph(
            id="graph",
            style={"height": "80vh", "width": "100%", "background-color": "#FFFFFF"}
        ),
    ])

def expand_data(df: pd.DataFrame, outer_dia: int, test_area: int, height: int, total_height: int) -> pd.DataFrame:
    """Expand the input data based on given parameters."""
    pv = df.to_numpy()
    total_circumference = np.pi * outer_dia
    expansion_factor_cols = total_circumference / test_area
    expansion_factor_rows = total_height / height
    
    rows, cols = pv.shape
    num_cols = int(expansion_factor_cols * cols)
    num_rows = int(expansion_factor_rows * rows)
    
    expanded_df = pd.DataFrame(columns=range(num_cols), index=range(num_rows))
    expanded_df.iloc[:rows, :cols] = df.values
    expanded_df.fillna(-1, inplace=True)
    
    return expanded_df

def extract_values(property_value):
    valid_data = property_value[property_value != -1]  # Exclude placeholder values
    vmin = np.min(valid_data)//1
    vmax = np.max(valid_data)//1
    z_norm = np.linspace(0, 1, 50)
    # If using arr
    # z_norm = (valid_data-np.min(valid_data))/(np.max(valid_data)-np.min(valid_data))
    return z_norm,vmin,vmax

def create_3d_figure(property_value: np.ndarray, radius: float, rows: int, cols: int) -> go.Figure:
    """Generate 3D visualization."""
    theta = np.linspace(0, 2 * np.pi, cols)
    z = np.linspace(0, rows, rows)
    theta, z_grid = np.meshgrid(theta, z)

    x = radius * np.cos(theta)
    y = radius * np.sin(theta)

    z_norm,vmin,vmax = extract_values(property_value)

    hover_text = np.empty_like(x, dtype=object)
    for i in range(rows):
        for j in range(cols):
            hover_text[i, j] = f"Row: {i}, Column: {j}, value: {property_value[i][j]}"

    fig = go.Figure(data=[go.Surface(
        z=z_grid,
        x=x,
        y=y,
        colorscale=COLORSCALE,
        surfacecolor=z_norm,
        colorbar=dict(
                title="Thickness %",
                tickformat=".0%",  # Formats tick labels as percentages
                x=-0.2            # Position of the first colorbar
            ),
        text=hover_text,
        hoverinfo='text'
    )])
    fig.add_trace(go.Surface(
        z=z_grid,
        x=x,
        y=y,
        cmin=vmin,
        cmax=vmax,
        colorscale=COLORSCALE,
        surfacecolor=property_value,
        colorbar=dict(title="Thickness (in mm)"),
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
    
    fig.update_layout(
        scene=dict(
            xaxis_title="X",
            yaxis_title="Angular Position (Theta)",
            zaxis_title='Height/Rows Z'
        ),
        title=f"3D Heatmap Visualization, Cylinder with {rows} Rows and {cols} Columns"
    )
    
    return fig

def create_2d_figure(df: np.ndarray, property_value: np.ndarray, rows: int, cols: int) -> go.Figure:
    """Generate 2D visualization."""
    theta = np.linspace(0, 2 * np.pi, cols)
    z = np.linspace(0, rows, rows)
    theta, z_grid = np.meshgrid(theta, z)

    z_norm,vmin,vmax = extract_values(property_value)

    hover_text = [[f"Row: {i}, Column: {j}, value: {property_value[i][j]}"
                   for j in range(cols)] for i in range(rows)]

    fig = go.Figure(data=[go.Heatmap(
        x=np.ravel(theta),
        y=np.ravel(z_grid),
        z=np.ravel(z_norm),
        colorscale=COLORSCALE,
        colorbar=dict(
                title="Thickness %",
                tickformat=".0%",  # Formats tick labels as percentages
                x=-0.2            # Position of the first colorbar
            ),
        text=hover_text,
        name="Data Points"
    )])

    fig.add_trace(go.Heatmap(
        x=np.ravel(theta),
        y=np.ravel(z_grid),
        z=np.ravel(property_value),
        colorscale=COLORSCALE,
        zmin=vmin,
        zmax=vmax,
        colorbar=dict(title="Thickness (in mm)"),
        text=hover_text,
        hoverinfo='text'
    ))

    fig.update_layout(
        title="2D Heatmap Visualization",
        xaxis=dict(title="Theta/Angle"),
        yaxis=dict(title="Height/Z")
    )
    
    return fig


def process_excel_data(contents: str, filename: str, sheet_index: int) -> Tuple[pd.DataFrame, List[Dict[str, str]]]:
    """Process uploaded Excel file and return dataframe and sheet options."""
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    file_data = io.BytesIO(decoded)
    
    ef = pd.ExcelFile(file_data)
    sheet_options = [{'label': label, 'value': str(i)} 
                    for i, label in enumerate(ef.sheet_names)]
    
    df = ef.parse(sheet_index)
    nan_idx = df[df.isnull().all(axis=1)].index[0]
    df = df[:nan_idx]
    df = df.drop(columns=['Sr. No'])
    
    return df, sheet_options

def init_app() -> Dash:
    """Initialize and configure the Dash application."""
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.layout = create_app_layout()
    
    @app.callback(
        [Output("upload-container", "style"),
         Output("validation-message", "children")],
        [Input("input-OuterDia", "value"),
         Input("input-TestArea", "value"),
         Input("input-height", "value"),
         Input("input-TotalHeight", "value")]
    )
    def toggle_upload_button(outer_dia, test_area, height, total_height):
        """Show/hide upload button based on input validation."""
        if not all([outer_dia, test_area, height, total_height]):
            return {"display": "none"}, "Please fill in all input fields to proceed"
        
        try:
            # Validate inputs are positive numbers
            values = [float(x) for x in [outer_dia, test_area, height, total_height]]
            if not all(v > 0 for v in values):
                return {"display": "none"}, "All values must be positive numbers"
            
            return {"display": "block"}, ""
            
        except ValueError:
            return {"display": "none"}, "All inputs must be valid numbers"
    
    @app.callback(
        [Output('dropdown', 'options'),
         Output("graph", "figure"),
         Output("status-message", "children")],
        [Input("upload-data", "contents"),
         Input("btn-2d", "n_clicks"),
         Input("btn-3d", "n_clicks"),
         Input('dropdown', 'value')],
        [State("upload-data", "filename"),
         State("input-OuterDia", "value"),
         State("input-TestArea", "value"),
         State("input-height", "value"),
         State("input-TotalHeight", "value")],
        prevent_initial_call=True
    )
    def update_visualization(contents, n_clicks_2d, n_clicks_3d, sheet_value,
                           filename, outer_dia, test_area, height, total_height):
        """Update visualization based on user inputs and uploaded data."""
        if not all([contents, filename]):
            return [], go.Figure(), "Please upload an Excel file."
        
        try:
            df, sheet_options = process_excel_data(contents, filename, int(sheet_value))
            expanded_df = expand_data(
                df,
                int(outer_dia),
                int(test_area),
                int(height),
                int(total_height)
            )
            
            property_value = expanded_df.to_numpy()[::-1]
            rows, cols = property_value.shape
            radius = int(outer_dia) // 2
            
            if n_clicks_3d > n_clicks_2d:
                fig = create_3d_figure(property_value, radius, rows, cols)
            else:
                fig = create_2d_figure(df, property_value, rows, cols)
            
            return sheet_options, fig, ""
            
        except Exception as e:
            print(str(e))
            return [], go.Figure(), f"Error: {str(e)}"
    
    return app

def run_standalone(app: Dash):
    """
    To run app server and webview
    """
    import threading
    import webview
    from waitress import serve

    def run_server():
        serve(app.server, host="0.0.0.0", port=8080)

    # Start the Dash server in a background thread.
    threading.Thread(target=run_server, daemon=True).start()

    # Open the desktop window pointing to the local Dash app.
    window = webview.create_window("InjoTech App", "http://127.0.0.1:8080")
    webview.start()

if __name__ == "__main__":
    app = init_app()
    app.run_server(debug=True)
    #run_standalone(app)

