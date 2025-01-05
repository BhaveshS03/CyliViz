import dash
from dash import dcc, html, Input, Output, State,callback
import dash_bootstrap_components as dbc
import flask

# Initialize Dash app
# server = flask.Flask(__name__)  # Shared server
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], server=server)

dash.register_page(__name__, path='/login')

# Global variable to store user credentials
user_credentials = {}  # Empty to allow user registration

# Define app layout
layout = html.Div(
    children=[
        dcc.Location(id="url", refresh=True),  # For navigation
        html.Div(
            children=[
                # Login Form
                html.Div(
                    id="login-form",
                    children=[
                        html.H2("Login", style={"color": "#6A1B9A", "text-align": "center", "margin-bottom": "30px", "font-family": "Arial, sans-serif", "font-weight": "bold"}),
                        dbc.Form(
                            [
                                dbc.Label("Username", html_for="login-username", style={"color": "#333", "font-weight": "bold", "font-size": "14px"}),
                                dbc.Input(id="login-username", placeholder="Enter your username", type="text", 
                                          style={"font-size": "16px", "padding": "12px", "border-radius": "8px", "margin-bottom": "20px", "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1)"}),
                                dbc.Label("Password", html_for="login-password", style={"color": "#333", "font-weight": "bold", "font-size": "14px"}),
                                dbc.Input(id="login-password", placeholder="Enter your password", type="password", 
                                          style={"font-size": "16px", "padding": "12px", "border-radius": "8px", "margin-bottom": "20px", "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1)"}),
                                html.Button("Login", id="login-button", n_clicks=0, style={
                                    "background-color": "#6A1B9A", 
                                    "color": "white", 
                                    "border": "none", 
                                    "padding": "12px 24px", 
                                    "font-size": "16px", 
                                    "border-radius": "8px", 
                                    "cursor": "pointer", 
                                    "transition": "all 0.3s ease",
                                    "width": "100%",
                                    "margin-top": "10px",
                                    "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.1)"
                                }),
                                html.Div(id="login-status", style={"color": "#D32F2F", "text-align": "center", "margin-top": "20px", "font-size": "14px", "font-family": "Arial, sans-serif"})
                            ],style={"display":"grid"}
                        ),
                        html.Div(
                            children=[
                                html.P("Don't have an account? ", style={"text-align": "center", "margin-top": "20px", "font-size": "14px", "font-family": "Arial, sans-serif"}),
                                html.A("Sign Up", href="#", id="signup-link", style={
                                    "color": "#6A1B9A", 
                                    "text-decoration": "none", 
                                    "font-weight": "bold", 
                                    "margin-left": "10px",
                                    "cursor": "pointer"
                                })
                            ],
                            style={"display": "flex", "justify-content": "center", "align-items": "center", "margin-top": "30px"}
                        )
                    ],
                    
                ),
                # Signup Form
                html.Div(
                    id="signup-form",
                    children=[
                        html.H3("Sign Up", style={"color": "#6A1B9A", "text-align": "center", "font-family": "Arial, sans-serif", "font-weight": "bold"}),
                        dbc.Form(
                            [
                                dbc.Label("Username", html_for="signup-username", style={"color": "#333", "font-weight": "bold", "font-size": "14px"}),
                                dbc.Input(id="signup-username", placeholder="Enter your username", type="text", 
                                          style={"font-size": "16px", "padding": "12px", "border-radius": "8px", "margin-bottom": "20px", "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1)"}),
                                dbc.Label("Password", html_for="signup-password", style={"color": "#333", "font-weight": "bold", "font-size": "14px"}),
                                dbc.Input(id="signup-password", placeholder="Enter your password", type="password", 
                                          style={"font-size": "16px", "padding": "12px", "border-radius": "8px", "margin-bottom": "20px", "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1)"}),
                                dbc.Label("Confirm Password", html_for="signup-confirm-password", style={"color": "#333", "font-weight": "bold", "font-size": "14px"}),
                                dbc.Input(id="signup-confirm-password", placeholder="Confirm your password", type="password", 
                                          style={"font-size": "16px", "padding": "12px", "border-radius": "8px", "margin-bottom": "20px", "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1)"}),
                                html.Button("Sign Up", id="signup-button-submit", n_clicks=0, style={
                                    "background-color": "#6A1B9A", 
                                    "color": "white", 
                                    "border": "none", 
                                    "padding": "12px 24px", 
                                    "font-size": "16px", 
                                    "border-radius": "8px", 
                                    "cursor": "pointer", 
                                    "transition": "all 0.3s ease",
                                    "width": "100%",
                                    "margin-top": "10px",
                                    "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.1)"
                                }),
                                html.Div(id="signup-status", style={"color": "#D32F2F", "text-align": "center", "margin-top": "20px", "font-size": "14px", "font-family": "Arial, sans-serif"})
                            ],
                            style={"display":"grid"}
                        ),
                        html.Div(
                            children=[
                                html.P("Already have an account? ", style={"text-align": "center", "margin-top": "20px", "font-size": "14px", "font-family": "Arial, sans-serif"}),
                                html.A("Login", href="#", id="login-link", style={
                                    "color": "#6A1B9A", 
                                    "text-decoration": "none", 
                                    "font-weight": "bold", 
                                    "margin-left": "10px",
                                    "cursor": "pointer"
                                })
                            ],
                            style={"display": "flex", "justify-content": "center", "align-items": "center", "margin-top": "25px"}
                        )
                    ],
                    style={"display": "none"},
                )
            ],
            style={
                "max-width": "500px", 
                "margin": "50px auto", 
                "padding": "40px", 
                "background-color": "#F8F8F8", 
                "border-radius": "10px", 
                "box-shadow": "0 4px 10px rgba(0, 0, 0, 0.1)",
                "font-family": "Arial, sans-serif"
            }
        )
    ]
)

@callback(
    [
        Output("login-status", "children"),
        Output("signup-status", "children"),
        Output("login-status", "style"),
        Output("signup-status", "style"),
        Output("login-form", "style"),
        Output("signup-form", "style"),
        Output("url", "href")
    ],
    [
        Input("login-button", "n_clicks"),
        Input("signup-link", "n_clicks"),
        Input("login-link", "n_clicks"),
        Input("signup-button-submit", "n_clicks")
    ],

    [
        State("login-username", "value"),
        State("login-password", "value"),
        State("signup-username", "value"),
        State("signup-password", "value"),
        State("signup-confirm-password", "value")
    ]
)
def manage_forms(login_clicks, signup_link_clicks, login_link_clicks, signup_submit_clicks, login_username, login_password, signup_username, signup_password, signup_confirm_password):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # If Login button is clicked
    if trigger_id == "login-button":
        if not login_username or not login_password:
            return "Please enter both fields.", "", {"color": "#D32F2F"}, {}, {"display": "block"}, {"display": "none"}, None
        if user_credentials.get(login_username) == login_password:
            return "Login successful! Redirecting...", "", {"color": "#388E3C"}, {}, {"display": "none"}, {"display": "none"}, "/main"
        return "Invalid credentials.", "", {"color": "#D32F2F"}, {}, {"display": "block"}, {"display": "none"}, None

    # If Signup button is clicked
    if trigger_id == "signup-button-submit":
        if not signup_username or not signup_password or not signup_confirm_password:
            return "", "All fields are required.", {}, {"color": "#D32F2F"}, {"display": "none"}, {"display": "block"}, None
        if signup_password != signup_confirm_password:
            return "", "Passwords do not match.", {}, {"color": "#D32F2F"}, {"display": "none"}, {"display": "block"}, None
        if signup_username in user_credentials:
            return "", "Username already exists.", {}, {"color": "#D32F2F"}, {"display": "none"}, {"display": "block"}, None
        user_credentials[signup_username] = signup_password
        return "", "Signup successful! Please login.", {}, {"color": "#388E3C"}, {"display": "block"}, {"display": "none"}, None

    # Switch between Login and Signup forms
    if trigger_id == "signup-link":
        return "", "", {}, {}, {"display": "none"}, {"display": "block"}, None
    if trigger_id == "login-link":
        return "", "", {}, {}, {"display": "block"}, {"display": "none"}, None

    return "", "", {}, {}, {"display": "block"}, {"display": "none"}, None

