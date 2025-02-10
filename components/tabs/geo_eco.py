import dash_bootstrap_components as dbc
from dash import Input, Output, callback, dcc, html

from components.common.filter_slider import create_filter_slider
from components.common.gender_metric_selector import get_metric_column
from components.common.year_slider import create_year_slider
from components.data.data import data, filter_data
from components.visualisations import create_bar_plot, create_line_plot, create_scatter_plot


def create_geo_eco_tab():
    """Function to create layout and visualations in the geo eco tab"""
    return html.Div(
        [
            # Add Store component for data
            dcc.Store(id="general-data"),
            create_filter_slider(),
            html.Br(),
            # Create a container div for the plots with the ID that matches the callback
            html.Div(id="4x4plots"),
            html.Br(),
            create_year_slider(),
        ]
    )


# @callback(
#     Output("4x4plots", "children"),
#     Input("year-slider", "value"),
#     Input("metric-dropdown", "value"),
#     Input("gender-dropdown", "value"),
#     Input("top-filter-slider", "value"),
#     Input("country-dropdown", "value"),
#     Input("region-dropdown", "value"),
#     Input("income-dropdown", "value"),
# )
# def create_geo_eco_plots(year, metric, gender, top_n, countries, regions, income):
#     """Create a grid of plots using visualizations from visualisations.py."""
#     if not year or not metric or not gender:
#         return html.Div(style={"margin": "20px", "height": "100vh"})

#     # Use cached filter function
#     df = filter_data(year, regions, income)
#     if df.empty:
#         return html.Div(style={"margin": "20px", "height": "100vh"})

#     col = get_metric_column(gender, metric)
#     if not col:
#         return html.Div(style={"margin": "20px", "height": "100vh"})

#     # Get selected countries or top N
#     selected_countries = countries if countries else df.nlargest(top_n, col)["Entity"].tolist()

#     # Create plots
#     plots = {
#         "gdp_scatter": dbc.Col(
#             create_scatter_plot("gdp_pc", "death_std", df, top_n=top_n),
#             width=7,  # Make it take the full row
#             className="px-2 py-2",
#         ),
#         "metric_bar": dbc.Col(
#             create_bar_plot(col, df, top_n=top_n), width=7, className="px-2 py-2"
#         ),
#         "pop_line": dbc.Col(
#             create_line_plot("Population", data, countries=selected_countries, top_n=top_n),
#             width=7,
#             className="px-2 py-2",
#         ),
#         "gender_scatter": dbc.Col(
#             create_scatter_plot("f_deaths", "m_deaths", df), width=7, className="px-2 py-2"
#         ),
#     }

#     # Adjust rows to take equal space
#     row1 = dbc.Row(plots["gdp_scatter"], className="h-25 g-0")
#     row2 = dbc.Row(plots["pop_line"], className="h-25 g-0")
#     row3 = dbc.Row(plots["metric_bar"], className="h-25 g-0")
#     row4 = dbc.Row(plots["gender_scatter"], className="h-25 g-0")

#     return html.Div(
#         [row1, row2, row3, row4],
#         style={
#             "height": "100vh",
#             "backgroundColor": "white",
#             "borderRadius": "8px",
#             "padding": "15px",
#             "boxShadow": "0 2px 4px rgba(0,0,0,0.05)",
#             "display": "flex",
#             "flexDirection": "column",
#         },
#     )
# @callback(
#     Output("4x4plots", "children"),
#     Input("year-slider", "value"),
#     Input("metric-dropdown", "value"),
#     Input("gender-dropdown", "value"),
#     Input("top-filter-slider", "value"),
#     Input("country-dropdown", "value"),
#     Input("region-dropdown", "value"),
#     Input("income-dropdown", "value"),
# )
# def create_geo_eco_plots(year, metric, gender, top_n, countries, regions, income):
#     """Create a grid of plots using visualizations from visualisations.py."""
#     if not year or not metric or not gender:
#         return html.Div(style={"margin": "20px", "height": "100vh"})

#     # Use cached filter function
#     df = filter_data(year, regions, income)
#     if df.empty:
#         return html.Div(style={"margin": "20px", "height": "100vh"})

#     col = get_metric_column(gender, metric)
#     if not col:
#         return html.Div(style={"margin": "20px", "height": "100vh"})

#     # Get selected countries or top N
#     selected_countries = countries if countries else df.nlargest(top_n, col)["Entity"].tolist()

#     # Create wrapped plots with titles inside Bootstrap Cards
#     plots = {
#         "gdp_scatter": dbc.Col(
#             dbc.Card([
#                 dbc.CardHeader(html.H4("GDP vs Death Rate")),
#                 dbc.CardBody(create_scatter_plot("gdp_pc", "death_std", df, top_n=top_n)),
#             ],className="mb-3 shadow-sm"),
#             width=12,
#         ),
#         "metric_bar": dbc.Col(
#             dbc.Card([
#                 dbc.CardHeader(html.H4(f"{metric} Distribution")),
#                 dbc.CardBody(create_bar_plot(col, df, top_n=top_n)),
#             ], className="mb-3 shadow-sm"),
#             width=12,
#         ),
#         "pop_line": dbc.Col(
#             dbc.Card([
#                 dbc.CardHeader(html.H4("Population Growth Over Time")),
#                 dbc.CardBody(create_line_plot("Population", data, countries=selected_countries, top_n=top_n)),
#             ], className="mb-3 shadow-sm"),
#             width=12,
#         ),
#         "gender_scatter": dbc.Col(
#             dbc.Card([
#                 dbc.CardHeader(html.H4("Male vs Female Deaths")),
#                 dbc.CardBody(create_scatter_plot("f_deaths", "m_deaths", df)),
#             ], className="mb-3 shadow-sm"),
#             width=12,
#         ),
#     }

#     # Layout with evenly spaced rows
#     row1 = dbc.Row(plots["gdp_scatter"], className="h-25 g-0 mb-3")
#     row2 = dbc.Row(plots["pop_line"], className="h-25 g-0 mb-3")
#     row3 = dbc.Row(plots["metric_bar"], className="h-25 g-0 mb-3")
#     row4 = dbc.Row(plots["gender_scatter"], className="h-25 g-0 mb-3")

#     return html.Div(
#         [row1, row2, row3, row4],
#         style={
#             "height": "100vh",
#             "backgroundColor": "#f8f9fa",
#             "borderRadius": "8px",
#             "padding": "15px",
#             "boxShadow": "0 2px 4px rgba(0,0,0,0.05)",
#             "display": "flex",
#             "flexDirection": "column",
#             "gap": "15px",
#         },
#     )


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

    # Create layout with plots wrapped inside Bootstrap Cards
    return html.Div(
        [
            dbc.Row(
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(html.H4("GDP vs Death Rate", className="text-center")),
                        dbc.CardBody(create_scatter_plot("gdp_pc", "death_std", df, top_n=top_n)),
                    ], className="mb-3 shadow-sm"),
                    width=12,
                ),
                className="h-25 g-0"
            ),
            dbc.Row(
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(html.H4("Population Growth Over Time", className="text-center")),
                        dbc.CardBody(create_line_plot("Population", data, countries=selected_countries, top_n=top_n)),
                    ], className="mb-3 shadow-sm"),
                    width=12,
                ),
                className="h-25 g-0"
            ),
            dbc.Row(
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(html.H4(f"{metric} Distribution", className="text-center")),
                        dbc.CardBody(create_bar_plot(col, df, top_n=top_n)),
                    ], className="mb-3 shadow-sm"),
                    width=12,
                ),
                className="h-25 g-0"
            ),
            dbc.Row(
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(html.H4("Male vs Female Deaths", className="text-center")),
                        dbc.CardBody(create_scatter_plot("f_deaths", "m_deaths", df)),
                    ], className="mb-3 shadow-sm"),
                    width=12,
                ),
                className="h-25 g-0"
            ),
        ],
        style={
            "height": "100vh",
            "backgroundColor": "#f8f9fa",
            "borderRadius": "8px",
            "padding": "15px",
            "boxShadow": "0 2px 4px rgba(0,0,0,0.05)",
            "display": "flex",
            "flexDirection": "column",
        },
    )
