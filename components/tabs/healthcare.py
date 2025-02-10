
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
    """Create healthcare-related visualizations in a grid layout."""
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

    return dbc.Container([
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(html.H4("Obesity vs Death Rate", className="text-center")),
                    dbc.CardBody(
                        create_scatter_plot(
                            "obesity%",
                            "death_rate",
                            data[data["Year"] == year].dropna(subset=["obesity%", "death_rate"]),
                            hue="WB_Income"
                        ),
                        style={"height": "350px", "overflow": "auto"}
                    ),
                ], className="mb-3 shadow-sm"),
                xs=12, sm=12, md=6, lg=6, xl=6
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(html.H4("CT Units by Country", className="text-center")),
                    dbc.CardBody(
                        create_bar_plot(
                            "ct_units",
                            data.dropna(subset=["ct_units"]),
                            top_n=top_n,
                            color="WB_Income"
                        ),
                        style={"height": "350px", "overflow": "auto"}
                    ),
                ], className="mb-3 shadow-sm"),
                xs=12, sm=12, md=6, lg=6, xl=6
            )
        ], className="mb-3"),
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(html.H4("High Blood Pressure", className="text-center")),
                    dbc.CardBody(
                        create_bar_plot("t_high_bp_30-79", data, top_n=top_n),
                        style={"height": "350px", "overflow": "auto"}
                    ),
                ], className="mb-3 shadow-sm"),
                xs=12, sm=12, md=6, lg=6, xl=6
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(html.H4("Sankey Diagram", className="text-center")),
                    dbc.CardBody(
                        create_sankey_diagram(data, metric, year),
                        style={"height": "350px", "overflow": "auto"}
                    ),
                ], className="mb-3 shadow-sm"),
                xs=12, sm=12, md=6, lg=6, xl=6
            )
        ])
    ], fluid=True, style={
        "backgroundColor": "#f8f9fa", 
        "borderRadius": "8px", 
        "padding": "15px",
    })