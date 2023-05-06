import dash_html_components as html
from dash.dependencies import Input, Output
import dash_core_components as dcc
from app import app
from pages import page1, page2
from pages import navbar

import index

if __name__ == '__main__':
    app.run_server(debug=True)