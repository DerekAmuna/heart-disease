from dash import dcc, html


def create_sidebar():
    sidebar = html.Div(
        [
            html.Div(
                [
                    html.Button(
                        html.I(className="fas fa-bars"),
                        className="navbar-toggler",
                        id="navbar-toggle",
                    ),
                ],
                className="sidebar-header",
            ),
            html.Div(
                [
                    html.H2("Filters", className="display-4"),
                    html.Hr(),
                    # Region Selector
                    html.Div(
                        [
                            html.H6("Region", className="text-primary"),
                            dcc.Dropdown(
                                id="region-dropdown",
                                options=[
                                    {"label": "All Regions", "value": "all"},
                                    {"label": "Africa", "value": "africa"},
                                    {"label": "North America", "value": "north_america"},
                                    {"label": "South America", "value": "south_america"},
                                    {"label": "Asia", "value": "asia"},
                                    {"label": "Europe", "value": "europe"},
                                    {"label": "Oceania", "value": "oceania"},
                                ],
                                value="all",
                                clearable=False,
                                className="mb-3",
                            ),
                        ]
                    ),
                    # Country Selector
                    html.Div(
                        [
                            html.H6("Country", className="text-primary"),
                            dcc.Dropdown(
                                id="country-dropdown",
                                placeholder="Select a country...",
                                multi=True,
                                className="mb-3",
                            ),
                        ]
                    ),
                    # World Income Selector
                    html.Div(
                        [
                            html.H6("World Income", className="text-primary"),
                            dcc.Dropdown(
                                id="income-dropdown",
                                options=[
                                    {"label": "All Income Levels", "value": "all"},
                                    {"label": "High Income", "value": "high"},
                                    {"label": "Upper Middle Income", "value": "upper_middle"},
                                    {"label": "Lower Middle Income", "value": "lower_middle"},
                                    {"label": "Low Income", "value": "low"},
                                ],
                                value="all",
                                clearable=False,
                                className="mb-3",
                            ),
                        ]
                    ),
                    # Gender Selector
                    html.Div(
                        [
                            html.H6("Gender", className="text-primary"),
                            dcc.Dropdown(
                                id="gender-dropdown",
                                options=[
                                    {"label": "All Genders", "value": "all"},
                                    {"label": "Male", "value": "M"},
                                    {"label": "Female", "value": "F"},
                                ],
                                value="all",
                                clearable=False,
                                className="mb-3",
                            ),
                        ]
                    ),
                    html.Hr(),
                ],
                id="sidebar-content",
            ),
        ],
        id="sidebar",
        style={
            "position": "fixed",
            "top": 0,
            "left": 0,
            "bottom": 0,
            "width": "16rem",
            "height": "100vh",
            "padding": "2rem 1rem",
            "background-color": "#f8f9fa",
            "z-index": 1,  # Ensure sidebar is above other content
            "overflow-y": "auto",
            "transition": "margin-left .3s",
        },
    )
    return sidebar
