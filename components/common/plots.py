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
    # Create a list of graph IDs to reduce redundancy.
    graph_ids = ["graph-1", "graph-2", "graph-3", "graph-4"]
    # Use list comprehension to create the columns.
    cols = [dbc.Col(create_plot(graph_id), width=6, className="p-1") for graph_id in graph_ids]

    # Group columns into rows.
    rows = [dbc.Row(cols[i:i + 2], className="g-0") for i in range(0, len(cols), 2)]

    return html.Div(
        rows,  # Use the generated rows directly
        style={"margin": "0", "height": "calc(90vh - 150px)"},
    )
