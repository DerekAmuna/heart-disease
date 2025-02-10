import logging

import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, callback, dcc, html

from components.common.filter_slider import create_filter_slider
from components.common.gender_metric_selector import get_metric_column
from components.common.year_slider import create_year_slider
from components.data.data import data, get_sankey_data
from components.visualisations import (
    create_bar_plot,
    create_line_plot,
    create_sankey_diagram,
    create_scatter_plot,
)

logger = logging.getLogger(__name__)


def create_healthcare_tab():
    """Function to display the layout for the healthcare tab with visualizations."""
    return html.Div(
        [
            dcc.Store(id="healthcare-data"),
            # create_filter_slider(),
            # html.Br(),
            html.Div(id="healthcare-plots"),
            # html.Br(),
            create_year_slider(),
        ]
    )


@callback(
    Output("healthcare-plots", "children"),
    Input("healthcare-data", "data"),
    Input("region-dropdown", "value"),
    Input("income-dropdown", "value"),
    Input("gender-dropdown", "value"),
    Input("metric-dropdown", "value"),
)
def create_healthcare_plots(data, regions, income, gender, metric):
    """Create healthcare-related visualizations in a grid layout.

    Returns:
        html.Div: A div containing a 2x2 grid of healthcare-related plots
    """
    if not data or not metric or not gender:
        return html.Div("Please select metric and gender")

    df = pd.DataFrame(data)
    logger.debug(f"first load view {df.head()}")
    if df.empty:
        return html.Div("No data available for the selected filters")

    metric_col = get_metric_column(metric=metric, gender=gender)
    if not metric_col:
        return html.Div("No metric data available")

    # Get sankey data directly
    sankey_data = get_sankey_data(regions, income, gender, metric)
    logger.debug(f"Creating plots for {metric_col}, \n {df.head()}")

    return dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    html.H4("Obesity vs Death Rate", className="text-center")
                                ),
                                dbc.CardBody(
                                    create_scatter_plot(
                                        "obesity%",
                                        metric_col,
                                        df.dropna(subset=["obesity%", metric_col]),
                                        hue="WB_Income",
                                        top_n=50
                                    ),
                                    style={"height": "350px", "overflow": "auto"},
                                ),
                            ],
                            className="mb-3 shadow-sm",
                        ),
                        xs=12,
                        sm=12,
                        md=6,
                        lg=6,
                        xl=6,
                    ),
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    html.H4("CT Units by Country", className="text-center")
                                ),
                                dbc.CardBody(
                                    create_scatter_plot(
                                        "ct_units",
                                        metric_col,
                                        df.dropna(subset=["ct_units", metric_col]),
                                        hue="WB_Income",
                                    ),
                                    style={"height": "350px", "overflow": "auto"},
                                ),
                            ],
                            className="mb-3 shadow-sm",
                        ),
                        xs=12,
                        sm=12,
                        md=6,
                        lg=6,
                        xl=6,
                    ),
                ],
                className="mb-3",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    html.H4("High Blood Pressure", className="text-center")
                                ),
                                dbc.CardBody(
                                    create_scatter_plot(
                                        "pacemaker_1m",
                                        metric_col,
                                        df.dropna(subset=["pacemaker_1m", metric_col]),
                                        hue="WB_Income",
                                    ),
                                    style={"height": "350px", "overflow": "auto"},
                                ),
                            ],
                            className="mb-3 shadow-sm",
                        ),
                        xs=12,
                        sm=12,
                        md=6,
                        lg=6,
                        xl=6,
                    ),
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(html.H4("Sankey Diagram", className="text-center")),
                                dbc.CardBody(
                                    create_sankey_diagram(sankey_data, metric, gender),
                                    style={"height": "350px", "overflow": "auto"},
                                ),
                            ],
                            className="mb-3 shadow-sm",
                        ),
                        xs=12,
                        sm=12,
                        md=6,
                        lg=6,
                        xl=6,
                    ),
                ]
            ),
        ],
        fluid=True,
        style={
            "backgroundColor": "#f8f9fa",
            "borderRadius": "8px",
            "padding": "15px",
        },
    )
