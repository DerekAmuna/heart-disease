import logging
import os

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from flask import Flask

import components.data  # Import data module to register callbacks
from components.sidebar import create_sidebar
from components.tabs.geo_eco import create_geo_eco_tab
from components.tabs.healthcare import create_healthcare_tab
from components.tabs.introduction import create_introduction_tab
from components.tabs.trends import create_trends_tab
from components.tabs.world_map import create_world_map_tab

#  FontAwesome for icons
FA = "https://use.fontawesome.com/releases/v5.15.4/css/all.css"

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

server = Flask(__name__)
app = dash.Dash(
    __name__,
    server=server,
    external_stylesheets=[dbc.themes.ZEPHYR, FA],
    suppress_callback_exceptions=True,
)
application = app.server

# Navbar Component
navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand("HEART DISEASE DATA VISUALIZATION ", className="ms-2"),
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink("Introduction 📋", id="tab-0-link", active=True)),
                    dbc.NavItem(dbc.NavLink("Choropleth Visualization 🌐", id="tab-1-link")),
                    dbc.NavItem(dbc.NavLink("GEO-ECO Features 💰", id="tab-2-link")),
                    dbc.NavItem(dbc.NavLink("Healthcare Features 🏥", id="tab-3-link")),
                    dbc.NavItem(dbc.NavLink("Trends 📈", id="tab-4-link")),
                ],
                className="ms-auto",
            ),
        ]
    ),
    color="primary",
    dark=True,
     fixed="top",
    className="mb-5", 
)

# Main Layout
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        navbar,
        dcc.Store(id='general-data',data=[]),
        dbc.Row(
            [
                # Sidebar
                dbc.Col(create_sidebar(), width="auto", className="p-0"),
                # Main content area
                dbc.Col(
                    html.Div(
                        [
                            html.Br(),
                            # Tab content with loading state
                            dbc.Spinner(
                                dcc.Store(id="tab-store", data={}),
                                color="primary",
                            ),
                            html.Div(id="tab-content"),
                        ],
                        style={
                            "padding": "20px",
                            "padding-left": "80px",  # extra padding for collapsed sidebar
                            "background-color": "#f8f9fa",
                            "min-height": "calc(100vh - 56px)",  # Full height minus navbar
                            "margin-top": "56px",  # Add margin to account for the fixed navbar
                        },
                    ),
                    className="ms-auto",
                ),
            ],
            className="g-0",
        ),
    ]
)


# Callback to update active tab links
@app.callback(
    [Output(f"tab-{i}-link", "active") for i in range(5)],
    [Input(f"tab-{i}-link", "n_clicks") for i in range(5)],
)
def update_active_tab(*args):
    ctx = dash.callback_context
    if not ctx.triggered:
        return [True] + [False] * 4
    clicked_tab = ctx.triggered[0]["prop_id"].split(".")[0]
    return [f"tab-{i}-link" == clicked_tab for i in range(5)]


# Callback to update tab content
@app.callback(
    Output("tab-content", "children"),
    [Input(f"tab-{i}-link", "active") for i in range(5)],
    [State("tab-store", "data")],
)
def render_tab_content(*active_tabs):
    ctx = dash.callback_context
    if not ctx.triggered:
        return create_introduction_tab()

    tab_mapping = {
        0: create_introduction_tab,
        1: create_world_map_tab,
        2: create_geo_eco_tab,
        3: create_healthcare_tab,
        4: create_trends_tab,
    }

    for i, is_active in enumerate(active_tabs):
        if is_active:
            return tab_mapping[i]()

    return "No tab selected"


if __name__ == "__main__":
    app.run_server(
        debug=True,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        dev_tools_hot_reload=True,
        dev_tools_ui=True,
    )
