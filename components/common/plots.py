import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import dcc, html


def create_plot(graph_id):
    # Sample figure
    return dcc.Graph(
        id=graph_id, config={"displayModeBar": False}, style={"height": "100%", "width": "100%"}
    )


def create_plots():
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(create_plot("graph-1"), body=True, style={"padding": "0"}),
                        width=6,
                    ),
                    dbc.Col(
                        dbc.Card(create_plot("graph-2"), body=True, style={"padding": "0"}),
                        width=6,
                    ),
                    dbc.Col(
                        dbc.Card(create_plot("graph-3"), body=True, style={"padding": "0"}),
                        width=6,
                    ),
                    dbc.Col(
                        dbc.Card(create_plot("graph-4"), body=True, style={"padding": "0"}),
                        width=6,
                    ),
                ],
                className="g-3",
            ),  # Decrease the gutter size between columns
        ],
        style={"padding": "10px"},
    )  # Optional: Add outer padding for the plot area
