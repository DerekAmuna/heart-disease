import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, dcc, html
from data.data import region_selector


def create_sidebar():
    return html.Div(
        [
            # Sidebar toggle button
            dbc.Button(
                "☰",
                id="sidebar-toggle",
                color="primary",
                className="mb-3",
                style={"position": "absolute", "top": "10px", "right": "-20px", "zIndex": "1000"},
            ),
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
                            id="region-dropdown", options=[
                                    region_selector()
                            ], placeholder="Select Region"
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
                        html.H6("METRIC", className=""),
                        dcc.Dropdown(
                            id="metric-dropdown", options=[], placeholder="Select Preferred Metric"
                        ),
                        html.Br(),
                    ],
                    style={"padding": "1rem"},
                ),
                id="sidebar",
                is_open=True,
            ),
        ],
        id="sidebar-container",
        style={
            "padding": "1rem",
            "background-color": "#f8f9fa",
            "height": "100vh",
            "width": "250px",
            "position": "fixed",
            "z-index": "1",
            "transition": "all 0.3s",
            "box-shadow": "3px 0 10px rgba(0,0,0,0.1)",
        },
    )


@callback(
    Output("sidebar", "is_open"),
    Output("sidebar-container", "style"),
    Input("sidebar-toggle", "n_clicks"),
    State("sidebar", "is_open"),
    prevent_initial_call=True,
)
def toggle_sidebar(n_clicks, is_open):
    if n_clicks is None:
        return True, {
            "padding": "1rem",
            "background-color": "#f8f9fa",
            "height": "100vh",
            "width": "250px",
            "position": "fixed",
            "z-index": "1",
            "transition": "all 0.3s",
            "box-shadow": "3px 0 10px rgba(0,0,0,0.1)",
        }

    if is_open:
        # Collapsed state
        return False, {
            "padding": "1rem",
            "background-color": "#f8f9fa",
            "height": "100vh",
            "width": "60px",  # Reduced width when collapsed
            "position": "fixed",
            "z-index": "1",
            "transition": "all 0.3s",
            "box-shadow": "3px 0 10px rgba(0,0,0,0.1)",
        }
    else:
        # Expanded state
        return True, {
            "padding": "1rem",
            "background-color": "#f8f9fa",
            "height": "100vh",
            "width": "250px",
            "position": "fixed",
            "z-index": "1",
            "transition": "all 0.3s",
            "box-shadow": "3px 0 10px rgba(0,0,0,0.1)",
        }
