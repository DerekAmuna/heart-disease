import pandas as pd
from dash import Input, Output, callback, dcc, html, no_update, State
import dash_bootstrap_components as dbc

from components.common.year_slider import create_year_slider
from components.visualisations import create_chloropleth_map, create_tooltip
import components.data


def create_world_map_tab():
    """Create the world map tab with choropleth map and year slider."""
    return html.Div(
        [
            dcc.Store(id="general-data"),
            dcc.Store(id="chloropleth_data"),
            html.Div(
                [
                    html.H2(id="map-title", style={"textAlign": "center", "marginBottom": "5px"}),
                    html.Div(
                        [
                            dcc.Graph(
                                id="chloropleth-map",
                                style={"height": "75vh"},
                                config={"displayModeBar": False}
                            ),
                            dcc.Tooltip(id="graph-tooltip"),
                        ],
                        style={"position": "relative"}
                    ),
                    create_year_slider(default=2000),
                ],
                id="world-map-container",
                style={
                    "height": "85vh",
                    "display": "flex",
                    "flexDirection": "column",
                    "gap": "10px",
                    "padding": "5px"
                }
            ),
        ]
    )


@callback(
    Output("map-title", "children"),
    Input("year-slider", "value"),
    Input("metric-dropdown", "value")
)
def update_map_title(year, metric):
    """Update the map title based on selected year and metric."""
    if not year or not metric:
        return ""
    return f"{metric} for {year}"


@callback(
    Output("chloropleth-map", "figure"),
    Input("chloropleth_data", "data"),
    Input("metric-dropdown", "value"),
    Input("gender-dropdown", "value")
)
def update_map(filtered_data, metric, gender):
    """Update the choropleth map based on filtered data and selected options."""
    print("Update map called with:", metric, gender)
    if not filtered_data or not metric or not gender:
        return {}
    return create_chloropleth_map(filtered_data)


@callback(
    Output("graph-tooltip", "show"),
    Output("graph-tooltip", "bbox"),
    Output("graph-tooltip", "children"),
    Input("chloropleth-map", "hoverData"),
    Input("metric-dropdown", "value"),
    Input("gender-dropdown", "value"),
    Input("year-slider", "value"),
)
def display_hover(hover_data, metric, gender, year):
    """Display time series plot in tooltip when hovering over a country."""
    if not hover_data or not metric or not gender:
        return False, no_update, no_update

    pt = hover_data["points"][0]
    country_code = pt["location"]

    fig, risk_factors = create_tooltip(country_code, metric, gender, year)

    children = [
        dcc.Graph(
            figure=fig,
            config={"displayModeBar": False},
            style={"width": "300px", "height": "200px"}
        ),
        html.Div(
            [
                html.H6(f"Risk Factors ({risk_factors.get('Year', 'Latest Year')})",
                    style={"marginTop": "10px", "marginBottom": "5px", "fontSize": "12px"}),
                html.Div(
                    [
                        html.Div([
                            html.Strong(f"{k}: ", style={"fontSize": "11px"}),
                            html.Span(v, style={"fontSize": "11px"})
                        ], style={"marginBottom": "3px"})
                        for k, v in risk_factors.items()
                        if k != 'Year'  # Skip the Year in display since it's in the header
                    ],
                    style={"paddingLeft": "5px"}
                )
            ],
            style={"backgroundColor": "white", "padding": "5px"}
        )
    ]

    bbox = pt["bbox"]
    return True, bbox, children
