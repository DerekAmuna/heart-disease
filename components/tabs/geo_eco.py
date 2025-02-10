

import dash_bootstrap_components as dbc
from dash import Input, Output, callback, dcc, html
import pandas as pd

from components.common.filter_slider import create_filter_slider
from components.common.gender_metric_selector import get_metric_column
from components.common.year_slider import create_year_slider
from components.data.data import data, filter_data
from components.visualisations import create_bar_plot, create_line_plot, create_scatter_plot


# def create_geo_eco_tab():
#     """Function to create layout and visualizations in the geo eco tab"""
#     return html.Div(
#         [
#             # Add Store component for data
#             dcc.Store(id="general-data"),
#             create_filter_slider(),
#             html.Br(),
#             # Create a container div for the plots with the ID that matches the callback
#             html.Div(id="4x4plots"),
#             html.Br(),
#             create_year_slider(),
#         ]
#     )
def create_geo_eco_tab():
    """Function to create layout and visualations in the geo eco tab"""
    return dbc.Container(
        [
            # Add Store component for data
            dcc.Store(id="geo-eco-data"),
            dbc.Row(
                [
                    dbc.Col(create_filter_slider(), width=12, lg=6),
                ],
                className="mb-3",
            ),
           html.Div(id="geo-eco-plots"),
            dbc.Row(
                [
                    dbc.Col(create_year_slider(min_year=1990,default=2021), width=12, lg=6),
                ],
                className="mb-3",
            ),
        ],
        fluid=True,
        
    )

@callback(
    Output("geo-eco-plots", "children"),
    Input("geo-eco-data", "data"),
    Input("metric-dropdown", "value"),
    Input("gender-dropdown", "value"),
    Input("top-filter-slider", "value"),
    Input('year-slider', 'value')
)
def create_geo_eco_plots(data, metric, gender, top_n, year):
    """Create a grid of plots using visualizations from visualisations.py."""
    if not data or not metric or not gender:
        print("Missing data:", not data, "Missing metric:", not metric, "Missing gender:", not gender)
        return html.Div("Please select metric and gender", style={"margin": "20px"})

    df = pd.DataFrame(data)
    print("DataFrame shape:", df.shape)
    print("DataFrame columns:", df.columns.tolist())

    if df.empty:
        return html.Div("No data available for the selected filters", style={"margin": "20px"})

    col = get_metric_column(gender, metric)
    print("Metric column:", col)
    if not col or col not in df.columns:
        return html.Div("Selected metric data not available", style={"margin": "20px"})


    return dbc.Container([
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(html.H4("GDP vs Death Rate", className="text-center")),
                dbc.CardBody(
                    create_scatter_plot("gdp_pc", col, df[df['Year']==year].dropna(subset=["gdp_pc", col]), hue="WB_Income", top_n=top_n),
                    style={"height": "350px", "overflow": "auto"}
                ),
            ], className="mb-3 shadow-sm"),
            xs=12, sm=12, md=6, lg=6, xl=6
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(html.H4("Population Growth", className="text-center")),
                dbc.CardBody(
                    create_line_plot("Population", df, top_n=top_n, n_metric=col),
                    style={"height": "350px", "overflow": "auto"}
                ),
            ], className="mb-3 shadow-sm"),
            xs=12, sm=12, md=6, lg=6, xl=6
        )
    ], className="mb-3"),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(html.H4(f"{metric} Distribution", className="text-center")),
                dbc.CardBody(
                    create_bar_plot(col, df[df['Year']==year].dropna(subset=[col]), top_n=top_n),
                    style={"height": "350px", "overflow": "auto"}
                ),
            ], className="mb-3 shadow-sm"),
            xs=12, sm=12, md=6, lg=6, xl=6
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(html.H4("Male vs Female Deaths", className="text-center")),
                dbc.CardBody(
                    create_scatter_plot("f_deaths", "m_deaths", df),
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
