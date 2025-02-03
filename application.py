import os

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from flask import Flask

from components.sidebar import create_sidebar
from components.tabs.introduction import create_introduction_tab
from components.tabs.geo_eco import create_geo_eco_tab
from components.tabs.healthcare import create_healthcare_tab
from components.tabs.trends import create_trends_tab
from components.tabs.world_map import create_world_map_tab

#  FontAwesome for icons
FA = "https://use.fontawesome.com/releases/v5.15.4/css/all.css"

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
)

# Main Layout
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        navbar,
        dbc.Row(
            [
                # Sidebar
                dbc.Col(create_sidebar(), width="auto", className="p-0"),
                # Main content area
                dbc.Col(
                    [
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
                            },
                        )
                    ],
                    className="ms-auto",
                ),
            ],
            className="g-0",
        ),
    ]
)


# Callback to update active tab links
@app.callback(
    [Output(f"tab-{i}-link", "active") for i in range(0, 5)],
    [Input(f"tab-{i}-link", "n_clicks") for i in range(0, 5)],
)
def update_active_tab(*args):
    ctx = dash.callback_context
    if not ctx.triggered:
        return True, False, False, False, False
    clicked_tab = ctx.triggered[0]["prop_id"].split(".")[0]
    return [f"tab-{i}-link" == clicked_tab for i in range(0, 5)]


# Callback to update tab content
@app.callback(
    Output("tab-content", "children"),
    [Input(f"tab-{i}-link", "active") for i in range(0, 5)],
    [State("tab-store", "data")],
)
def render_tab_content(tab0_active, tab1_active, tab2_active, tab3_active, tab4_active, store_data):
    ctx = dash.callback_context
    if not ctx.triggered:
        # Default to first tab
        return create_introduction_tab()
    
    if tab0_active:
        return create_introduction_tab()
    elif tab1_active:
        return create_world_map_tab()
    elif tab2_active:
        return create_geo_eco_tab()
    elif tab3_active:
        return create_healthcare_tab()
    elif tab4_active:
        return create_trends_tab()

    return "No tab selected"


if __name__ == "__main__":
    app.run_server(
        debug=True,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        dev_tools_hot_reload=True,
        dev_tools_ui=True,
    )
