
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
    Input("healthcare-data", "data"),
    Input("metric-dropdown", "value"),
    Input("gender-dropdown", "value"),
)
def create_healthcare_plots(data, metric, gender):
    """Create healthcare-related visualizations in a grid layout.

    Returns:
        html.Div: A div containing a 2x2 grid of healthcare-related plots
    """
    if not data or not metric or not gender:
        return html.Div("Please select metric and gender")

    df = pd.DataFrame(data)
    if df.empty:
        return html.Div("No data available for the selected filters")

    # Convert numeric columns
    numeric_cols = [
        "obesity%",
        "ct_units",
        "pacemaker_1m",
        "statin_use_k"
    ]
    for col in numeric_cols + [col for col in df.columns if col not in numeric_cols]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    metric_col = next((col for col in df.columns if col not in numeric_cols), None)
    if not metric_col:
        return html.Div("No metric data available")

    return dbc.Container([
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(html.H4("Obesity vs Death Rate", className="text-center")),
                    dbc.CardBody(
                        create_scatter_plot(
                            "obesity%",
                            metric_col,
                            df.dropna(subset=["obesity%", metric_col]),
                            hue="WB_Income",
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
                        create_scatter_plot(
                            "ct_units",
                            metric_col,
                            df.dropna(subset=["ct_units", metric_col]),
                            hue="WB_Income",
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
                        create_scatter_plot(
                            "pacemaker_1m",
                            metric_col,
                            df.dropna(subset=["pacemaker_1m", metric_col]),
                            hue="WB_Income",
                        ),
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
