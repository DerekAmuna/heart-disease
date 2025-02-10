

import dash_bootstrap_components as dbc
from dash import Input, Output, callback, dcc, html

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
            dcc.Store(id="general-data"),
            dbc.Row(
                [
                    dbc.Col(create_filter_slider(), width=12, lg=6),
                ],
                className="mb-3",
            ),
            html.Div(id="4x4plots"),
            dbc.Row(
                [
                    dbc.Col(create_year_slider(), width=12, lg=6),
                ],
                className="mb-3",
            ),
        ],
        fluid=True,
    )

@callback(
    Output("4x4plots", "children"),
    Input("year-slider", "value"),
    Input("metric-dropdown", "value"),
    Input("gender-dropdown", "value"),
    Input("top-filter-slider", "value"),
    Input("country-dropdown", "value"),
    Input("region-dropdown", "value"),
    Input("income-dropdown", "value"),
)
def create_geo_eco_plots(year, metric, gender, top_n, countries, regions, income):
    """Create a grid of plots using visualizations from visualisations.py."""
    
    # Handle missing inputs
    if not year or not metric or not gender:
        return html.Div(style={"margin": "20px", "height": "100vh"})

    # Filter data
    df = filter_data(year, regions, income)
    if df.empty:
        return html.Div(style={"margin": "20px", "height": "100vh"})

    col = get_metric_column(gender, metric)
    if not col:
        return html.Div(style={"margin": "20px", "height": "100vh"})

    # Get selected countries or top N
    selected_countries = countries if countries else df.nlargest(top_n, col)["Entity"].tolist()

 
    return dbc.Container([
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(html.H4("GDP vs Death Rate", className="text-center")),
                dbc.CardBody(
                    create_scatter_plot("gdp_pc", "death_std", df, top_n=top_n),
                    style={"height": "350px", "overflow": "auto"}
                ),
            ], className="mb-3 shadow-sm"),
            xs=12, sm=12, md=6, lg=6, xl=6
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(html.H4("Population Growth", className="text-center")),
                dbc.CardBody(
                    create_line_plot("Population", data, countries=selected_countries, top_n=top_n),
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
                    create_bar_plot(col, df, top_n=top_n),
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