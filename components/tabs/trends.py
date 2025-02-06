import dash_bootstrap_components as dbc
from dash import Input, Output, callback, dcc, html

from components.common.filter_slider import create_filter_slider
from components.common.year_slider import create_year_slider
from components.data.data import data
from components.visualisations import create_trend_plot


def create_trends_tab():
    """Function to create layout and visualations in the trends tab"""
    return html.Div(
        [
            dcc.Store(id="general-data"),
            create_filter_slider(),
            html.Br(),
            html.Div(id="trend-plots"),
            html.Br(),
            create_year_slider(),
        ]
    )


@callback(
    Output("trend-plots", "children"),
    Input("year-slider", "value"),
    Input("metric-dropdown", "value"),
    Input("gender-dropdown", "value"),
    Input("top-filter-slider", "value"),
    Input("country-dropdown", "value"),
    Input("region-dropdown", "value"),
    Input("income-dropdown", "value"),
)
def update_trend_plots(year, metric, gender, top_n, countries, regions, income):
    """Update trend plots based on user selections."""
    if not year or not metric:
        return html.Div()

    filtered_data = data.copy()

    # Apply filters
    if countries:
        filtered_data = filtered_data[filtered_data["Entity"].isin(countries)]
    if regions:
        filtered_data = filtered_data[filtered_data["region"] == regions]
    if income:
        filtered_data = filtered_data[filtered_data["WB_Income"] == income]

    return dbc.Row([dbc.Col(create_trend_plot(filtered_data, metric, year, gender), width=12)])
