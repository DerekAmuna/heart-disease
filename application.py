import os

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from flask import Flask

# from components.common.navbar import create_navbar
from components.common.filter_slider import create_filter_slider
from components.common.plots import create_plots
from components.common.year_slider import create_year_slider
from components.sidebar import create_sidebar
from components.tabs.healthcare import create_healthcare_tab

#  FontAwesome for icons
FA = "https://use.fontawesome.com/releases/v5.15.4/css/all.css"


server = Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.ZEPHYR, FA])

# For gunicorn
application = server

# Navbar Component
navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand("HEART DISEASE DATA VISUALIZATION ", className="ms-2"),
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink("Choropleth Visualization 🌐", href="#")),
                    dbc.NavItem(dbc.NavLink("GEO-ECO Features 💰", href="#")),
                    dbc.NavItem(dbc.NavLink("Healthcare Features 🏥", href="#")),
                    dbc.NavItem(dbc.NavLink("Trends 📈", href="#")),
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
                dbc.Col(create_sidebar(), width=2),
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.Br(),
                                create_filter_slider(),
                                html.Br(),
                                create_plots(),
                                html.Br(),
                                create_year_slider(),
                            ],
                            style={"padding": "20px", "background-color": "#f8f9fa"},
                        )
                    ],
                    width=10,
                ),
            ],
            className="g-0",
        ),
    ]
)


if __name__ == "__main__":
    app.run_server(
        debug=True,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        dev_tools_hot_reload=True,
        dev_tools_ui=True,
    )
