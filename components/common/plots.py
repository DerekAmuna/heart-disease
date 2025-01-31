import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import dcc, html


def create_plot(graph_id):
    return dcc.Graph(
        id=graph_id,
        config={"displayModeBar": False},
        style={"height": "37vh"},  # Fixed height based on viewport height
    )


def create_plots():
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(create_plot("graph-1"), width=6, className="p-1"),
                    dbc.Col(create_plot("graph-2"), width=6, className="p-1"),
                ],
                className="g-0",
            ),
            dbc.Row(
                [
                    dbc.Col(create_plot("graph-3"), width=6, className="p-1"),
                    dbc.Col(create_plot("graph-4"), width=6, className="p-1"),
                ],
                className="g-0",
            ),
        ],
        style={"margin": "0", "height": "calc(90vh - 150px)"},
    )
