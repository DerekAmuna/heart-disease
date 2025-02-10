# import dash_bootstrap_components as dbc
# from dash import Input, Output, callback, dcc, html

# from components.common.filter_slider import create_filter_slider
# from components.common.year_slider import create_year_slider
# from components.data.data import data
# from components.visualisations import create_trend_plot


# def create_trends_tab():
#     """Function to create layout and visualations in the trends tab"""
#     return html.Div(
#         [
#             dcc.Store(id="general-data"),
#             create_filter_slider(),
#             html.Br(),
#             html.Div(id="trend-plots"),
#             html.Br(),
#             create_year_slider(),
#         ]
#     )


# @callback(
#     Output("trend-plots", "children"),
#     Input("year-slider", "value"),
#     Input("metric-dropdown", "value"),
#     Input("gender-dropdown", "value"),
#     Input("top-filter-slider", "value"),
#     Input("country-dropdown", "value"),
#     Input("region-dropdown", "value"),
#     Input("income-dropdown", "value"),
# )
# def update_trend_plots(year, metric, gender, top_n, countries, regions, income):
#     """Update trend plots based on user selections."""
#     if not year or not metric:
#         return html.Div()

#     filtered_data = data.copy()

#     # Apply filters
#     if countries:
#         filtered_data = filtered_data[filtered_data["Entity"].isin(countries)]
#     if regions:
#         filtered_data = filtered_data[filtered_data["region"] == regions]
#     if income:
#         filtered_data = filtered_data[filtered_data["WB_Income"] == income]

#     return dbc.Row([dbc.Col(create_trend_plot(filtered_data, metric, year, gender), width=12)])


import dash_bootstrap_components as dbc
from dash import Input, Output, callback, dcc, html
import pandas as pd

from components.common.filter_slider import create_filter_slider
from components.common.year_slider import create_year_slider
from components.data.data import data
from components.visualisations import create_trend_plot

def create_trends_tab():
    """Function to create layout and visualations in the trends tab"""
    return html.Div(
        [
            dcc.Store(id="trend-data"),
            create_filter_slider(),
            html.Br(),
            html.Div(id="trend-plots"),
            html.Br(),
            create_year_slider(),
        ]
    )


@callback(
    Output("trend-plots", "children"),
    Input("trend-data", "data"),
    Input("metric-dropdown", "value"),
    Input("gender-dropdown", "value"),
    Input("income-dropdown", "value"),
)
def update_trend_plots(trends_data, metric, gender, income):
    """Update trend plots based on filtered data."""
    if not trends_data or not metric or not gender:
        return html.Div("No Data")

    df = pd.DataFrame(trends_data)
    if df.empty:
        return html.Div("No Data")

    return dbc.Container([
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(html.H4(f"Trend Analysis: {metric}", className="text-center")),
                    dbc.CardBody(
                        create_trend_plot(df, metric, None, gender),
                        style={"height": "500px", "overflow": "auto"}
                    ),
                ], className="mb-3 shadow-sm"),
                xs=12, sm=12, md=12, lg=12, xl=12
            )
        ])
    ], fluid=True, style={
        "backgroundColor": "#f8f9fa",
        "borderRadius": "8px",
        "padding": "15px",
    })
