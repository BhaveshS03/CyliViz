# app.py - Main application file
import dash
from dash import dcc, html, callback, Input, Output, State

# Import page modules
from pages import home, view, results

# Import all callbacks
from pages.home import register_callbacks as register_home_callbacks
from pages.view import register_callbacks as register_view_callbacks
from pages.results import register_callbacks as register_results_callbacks

# Initialize the Dash app
app = dash.Dash(__name__, 
                suppress_callback_exceptions=True,
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])

server = app.server

# Define the layout with multiple pages
app.layout = html.Div([
    # Location component tracks URL
    dcc.Location(id='url', refresh=False),
    
    # Store component for data
    dcc.Store(id='data-store', storage_type='session'),
    dcc.Store(id='prop-store', storage_type='session'),
    
    # Content will be rendered here
    html.Div(id='page-content', className='container')
])

# Callback to render different page content based on URL
@callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/' or pathname == '/home':
        return home.layout
    if pathname == '/view':
        return view.layout
    if pathname == '/results':
        return results.layout    

    return html.Div([
        html.H2('404 - Page not found', className='text-danger'),
        html.P(f"The page {pathname} does not exist.")
 ])

# Register callbacks
register_home_callbacks(app)
register_view_callbacks(app)
register_results_callbacks(app)

class StandaloneRunner:
    """Class to run the Dash app standalone with webview."""

    def __init__(self, app):
        self.app = app

    def run(self):
        """Run the Dash app server and webview."""
        import threading
        import webview
        from waitress import serve

        def run_server():
            serve(self.app.server, host="127.0.0.1", port=8080)

        # Start the Dash server in a background thread.
        threading.Thread(target=run_server, daemon=True).start()

        def set_zoom(window):
            window.evaluate_js("document.body.style.zoom = '80%'")

        # Open the desktop window pointing to the local Dash app.
        webview.create_window("InjoTech App", "http://127.0.0.1:8080")
        webview.start()


def run_standalone(app_manager):
    """Run the Dash app standalone."""
    standalone_runner = StandaloneRunner(app_manager)
    standalone_runner.run()

if __name__ == '__main__':
    #run_standalone(app)
    app.run_server(debug=True)