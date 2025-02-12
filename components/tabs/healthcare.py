import logging

import dash_bootstrap_components as dbc
import pandas as pd
import polars as pl
from dash import Input, Output, callback, dcc, html
from numpy._core.numeric import True_

from components.common.filter_slider import create_filter_slider
from components.common.gender_metric_selector import get_metric_column
from components.common.year_slider import create_year_slider
from components.visualisations import create_bar_plot, create_scatter_plot

logger = logging.getLogger(__name__)


def create_healthcare_tab():
    """Function to display the layout for the healthcare tab with visualizations."""
    return html.Div(
        [
            dcc.Store(id="healthcare-data"),
            dcc.Store(id="hpt-data"),
            create_filter_slider(),
            # html.Br(),
            html.Div(id="healthcare-plots"),
            # html.Br(),
            create_year_slider(),
        ]
    )


@callback(
    Output("healthcare-plots", "children"),
    Input("healthcare-data", "data"),
    Input("hpt-data", "data"),
    Input("gender-dropdown", "value"),
    Input("metric-dropdown", "value"),
    Input("year-slider", "value"),
)
def create_healthcare_plots(data, hpt, gender, metric, year):
    """Create healthcare-related visualizations in a grid layout.

    Returns:
        html.Div: A div containing a 2x2 grid of healthcare-related plots
    """
    if not data or not metric or not gender:
        return html.Div("Please select metric and gender")

    # Convert data to Polars DataFrame
    df = pl.DataFrame(data)
    logger.debug(f"first load view {df.head()}")
    if df.is_empty():
        return html.Div("No data available for the selected filters")

    metric_col = get_metric_column(gender, metric)
    if not metric_col:
        return html.Div("No metric data available")

    hpt_df = pd.DataFrame(hpt)
    hpt_clean = (hpt_df
                .dropna(subset=["t_htn_ctrl"])
                .sort_values('t_htn_ctrl', ascending=False))
    hpt_clean_bp = hpt_df.dropna(subset=["t_high_bp_30-79"]).sort_values(
        "t_high_bp_30-79", ascending=False
    )
    logger.debug(f"HPT DataFrame columns: {hpt_df.columns.tolist()}")
    logger.debug(f"HPT DataFrame head:\n{hpt_df.head()}")
    # logger.debug(msg=hpt.head())

    # Get sankey data directly
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
                                        data=df.drop_nulls(subset=["obesity%", metric_col]),
                                        x_metric="obesity%",
                                        y_metric=metric_col,
                                        # gender="Both"
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
                                    html.H4(
                                        "Hypertension Control by Country", className="text-center"
                                    )
                                ),
                                dbc.CardBody(
                                    create_bar_plot(
                                        "t_htn_ctrl",
                                        hpt_clean,
                                        top_n=20,
                                        color="WB_Income",
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
                                        data=hpt_clean_bp,
                                        x_metric="t_high_bp_30-79",
                                        y_metric=metric_col,
                                        hue="WB_Income",
                                        top_n=50,
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
                                    html.H4("Male vs Female Comparison", className="text-center")
                                ),
                                dbc.CardBody(
                                    create_scatter_plot(
                                        data=df.filter(pl.col("Year").eq(year)),
                                        x_metric=get_metric_column("Female", metric),
                                        y_metric=get_metric_column("Male", metric),
                                        add_diagonal=True,
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
