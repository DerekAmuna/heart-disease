import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import dcc, html, Output, Input, callback

from components.visualisations import (
    create_scatter_plot,
    create_bar_plot,
    create_line_plot
)

def create_plot(graph_id):
    return dcc.Graph(
        id=graph_id,
        config={"displayModeBar": False},
        style={"height": "37vh"},  # Fixed height based on viewport height
    )

@callback(
    Output('4x4plots','children'),
    Input('general-data', 'data'),
    # Input('year-slider', 'value'),
    # Input('metric-dropdown', 'value'),
    Input('gender-dropdown', 'value'),
    Input('region-dropdown', 'value'),
    Input('income-dropdown', 'value')
)

def create_plots(data):
    """Create a grid of plots using visualizations from visualisations.py."""
    plots = [
        ("gdp_pc", "death_std", create_scatter_plot),  # GDP vs Death Rate scatter
        ("m_deaths", None, create_bar_plot),    
        ("Population", None, create_line_plot),        # Population over time
        ("f_deaths", "m_deaths", create_scatter_plot)  # Female vs Male deaths scatter
    ]

    # Create columns with the plots
    cols = []
    for i, (metric1, metric2, plot_func) in enumerate(plots, 1):
        if metric2:
            plot = plot_func(metric1, metric2)
        else:
            plot = plot_func(metric1)

        # Ensure the plot has an ID for callbacks
        if isinstance(plot, dcc.Graph):
            plot.id = f"graph-{i}"

        cols.append(dbc.Col(plot, width=6, className="p-1"))

    # Group columns into rows
    rows = [dbc.Row(cols[i:i + 2], className="g-0") for i in range(0, len(cols), 2)]

    return html.Div(
        rows,
        style={"margin": "0", "height": "calc(90vh - 150px)"},
    )
