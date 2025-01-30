import dash_bootstrap_components as dbc
from dash import dcc, html


def create_year_slider(min_year=1950, max_year=2023, default=2021):
    return dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Button("▶️", id="play-button", n_clicks=0),
                            dcc.Interval(id="animation-interval", interval=1000, disabled=True),
                        ],
                        width=1,
                    ),
                    dbc.Col(
                        [
                            dbc.Label("Select Year"),
                            dcc.Slider(
                                id="year-slider",
                                min=min_year,
                                max=max_year,
                                value=default,
                                marks={
                                    str(year): str(year)
                                    for year in range(min_year, max_year + 1, 5)
                                },
                                step=1,
                                tooltip={"placement": "bottom", "always_visible": True},
                                included=False,
                            ),
                        ],
                        width=11,
                    ),
                ]
            )
        ]
    )
