import logging

import dash_bootstrap_components as dbc
import polars as pl
from dash import Input, Output, callback, dcc, html

from components.common.filter_slider import create_filter_slider
from components.common.year_slider import create_year_slider
from components.visualisations import create_trend_plot

logger = logging.getLogger(__name__)


def create_trends_tab():
    """Function to create layout and visualations in the trends tab"""
    return html.Div(
        [
            dcc.Store(id="trends-data"),
            # create_filter_slider(),
            html.Br(),
            html.Div(id="trend-plots"),
            html.Br(),
            # create_year_slider(),
        ]
    )


@callback(
    Output("trend-plots", "children"),
    Input("trends-data", "data"),
    Input("metric-dropdown", "value"),
    Input("gender-dropdown", "value"),
    Input("income-dropdown", "value"),
)
def update_trend_plots(trends_data, metric, gender, income):
    """Update trend plots based on filtered data."""
    if not trends_data or not metric or not gender:
        return html.Div("No Data")

    df = pl.DataFrame(trends_data)
    logger.debug(f"first load view {df.head()}")
    if df.height == 0:
        return html.Div("No Data")

    return dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    html.H4(f"Trend Analysis: {metric}", className="text-center")
                                ),
                                dbc.CardBody(
                                    create_trend_plot(df, metric, None, gender),
                                    style={"height": "100%", "overflow": "auto"},
                                ),
                            ],
                            className="mb-3 shadow-sm",
                        ),
                        xs=12,
                        sm=12,
                        md=12,
                        lg=12,
                        xl=12,
                    )
                ]
            )
        ],
        fluid=True,
        style={
            "backgroundColor": "#f8f9fa",
            "borderRadius": "8px",
            "padding": "15px",
            'height':'100%'
        },
    )
