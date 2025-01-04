import dash
from dash import Dash, html, dcc

app = Dash(__name__, use_pages=True)

app.layout = html.Div([
    dash.page_container
],)

if __name__ == '__main__':
    app.run(debug=True)