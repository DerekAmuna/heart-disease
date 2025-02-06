import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, callback, dcc, html

from components.common.filter_slider import create_filter_slider
from components.common.year_slider import create_year_slider
from components.data.data import data
from components.visualisations import (
    create_bar_plot,
    create_line_plot,
    create_sankey_diagram,
    create_scatter_plot,
)


def create_healthcare_tab():
    """Function to display the layout for the healthcare tab with visualizations."""
    return html.Div(
        [
            dcc.Store(id="healthcare-data"),
            create_filter_slider(),
            html.Br(),
            html.Div(id="healthcare-plots"),
            html.Br(),
            create_year_slider(),
        ]
    )


@callback(
    Output("healthcare-plots", "children"),
    Input("year-slider", "value"),
    Input("country-dropdown", "value"),
    Input("income-dropdown", "value"),
    Input("region-dropdown", "value"),
    Input("top-filter-slider", "value"),
    Input("metric-dropdown", "value"),
)
def create_healthcare_plots(
    year: int, countries: list, income: str, region: str, top_n: int, metric: str
):
    """Create healthcare-related visualizations in a grid layout.

    Returns:
        html.Div: A div containing a 2x2 grid of healthcare-related plots
    """

    numeric_cols = [
        "obesity%",
        "death_rate",
        "t_htn_30-79",
        "t_high_bp_30-79",
        "t_htn_ctrl_30-79",
        "ct_units",
    ]
    for col in numeric_cols:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        create_scatter_plot(
                            "obesity%",
                            "death_rate",
                            data[data["Year"] == year].dropna(subset=["obesity%", "death_rate"]),
                            hue="WB_Income",
                        ),
                        width=6,
                    ),
                    dbc.Col(
                        create_bar_plot(
                            "ct_units",
                            data.dropna(subset=["ct_units"]),
                            top_n=top_n,
                            color="WB_Income",
                        ),
                        width=6,
                    ),
                ]
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        create_bar_plot("t_high_bp_30-79", data, top_n=top_n),
                        width=6,
                    ),
                    dbc.Col(
                        create_sankey_diagram(data, metric, year),
                        width=6,
                    ),
                ]
            ),
        ]
    )
