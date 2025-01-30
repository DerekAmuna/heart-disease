import os

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from flask import Flask

from components.common.year_slider import create_year_slider
from components.sidebar import create_sidebar
from components.tabs.world_map import create_world_map_tab

#  FontAwesome for icons
FA = "https://use.fontawesome.com/releases/v5.15.4/css/all.css"


# Initialize Flask server
server = Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP, FA])
application = app.server  # for eb


# main content
main_content = html.Div(
    [
        # Tabs
        dbc.Tabs(
            [
                dbc.Tab(label="World Map", tab_id="tab-1", children=[create_world_map_tab()]),
                dbc.Tab(label="Geo-Eco Features", tab_id="tab-2"),
                dbc.Tab(label="Healthcare Features", tab_id="tab-3"),
                dbc.Tab(label="Trends", tab_id="tab-4"),
            ],
            id="tabs",
            active_tab="tab-1",
        ),
        create_year_slider(),
    ],
    id="page-content",
    style={
        "margin-left": "16rem",
        "padding": "2rem",
        "transition": "margin-left .3s",
        "width": "calc(100% - 16rem)",
    },
)

# main app layout
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), create_sidebar(), main_content],
    style={"position": "relative"},
)

if __name__ == "__main__":
    app.run_server(
        debug=True,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        dev_tools_hot_reload=True,
        dev_tools_ui=True,
    )
