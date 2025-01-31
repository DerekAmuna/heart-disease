import dash_bootstrap_components as dbc
from dash import dcc, html


def create_sidebar():
    return html.Div(
        [
            # Sidebar toggle button
            dbc.Button("☰", id="sidebar-toggle", color="primary", className="mb-3"),
            # Sidebar content
            dbc.Collapse(
                html.Div(
                    [
                        html.H5("Selectors", className="text-center fw-bold"),
                        html.Br(),
                        html.H6("COUNTRY", className=""),
                        dcc.Dropdown(
                            id="country-dropdown", options=[], placeholder="Select Country"
                        ),
                        html.Br(),
                        html.H6("REGION", className=""),
                        dcc.Dropdown(
                            id="region-dropdown", options=[], placeholder="Select Region"
                        ),
                        html.Br(),
                        html.H6("GENDER", className=""),
                        dcc.Dropdown(
                            id="gender-dropdown", options=[], placeholder="Select Gender"
                        ),
                        html.Br(),
                        html.H6("WORLD INCOME", className=""),
                        dcc.Dropdown(
                            id="income-dropdown", options=[], placeholder="Select Income Level"
                        ),
                        html.Br(),
                    ]
                ),
                id="sidebar",
                is_open=True,
            ),
        ],
        style={
            "padding": "1rem",
            "background-color": "#f8f9fa",
            "height": "100vh",
            "width": "250px",
            "position": "fixed",
            "z-index": "1",
        },
    )
