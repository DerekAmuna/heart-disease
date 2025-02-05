import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import dcc, html, Output, Input, callback

from components.visualisations import (
    create_scatter_plot,
    create_bar_plot,
    create_line_plot
)
from components.data.data import data

def create_plot(graph_id):
    return dcc.Graph(
        id=graph_id,
        config={"displayModeBar": False},
        style={"height": "37vh"},  # Fixed height based on viewport height
    )

@callback(
    Output('4x4plots','children'),
    Input('year-slider', 'value'),
    Input('metric-dropdown', 'value'),
    Input('gender-dropdown', 'value'),
)
def create_plots(year, metric, gender):
    """Create a grid of plots using visualizations from visualisations.py."""
    if not year or not metric or not gender:
        return html.Div(style={"margin": "20px", "height": "calc(90vh - 150px)"})

    # Filter data by year
    df = data[data['Year'] == year].copy()
    if df.empty:
        return html.Div(style={"margin": "20px", "height": "calc(90vh - 150px)"})

    gender_prefix = "f_" if gender == "Female" else "m_" if gender == "Male" else ""
    metric_mapping = {
        "P": {
            "Prevalence Percent": f"{gender_prefix}prev%",
            "Prevalence Rate": f"{gender_prefix}prev_rate",
            "Prevalence": f"{gender_prefix}prev",
        },
        "D": {
            "Death Percent": f"{gender_prefix}deaths%",
            "Death Rate": f"{gender_prefix}death_rate",
            "Death": f"{gender_prefix}deaths",
        },
    }
    col = metric_mapping.get(metric[0], {}).get(metric)
    if not col:
        return html.Div(style={"margin": "20px", "height": "calc(90vh - 150px)"})

    # Create each plot with proper spacing
    gdp_scatter = dbc.Col(
        create_scatter_plot("gdp_pc", "death_std", df), 
        width=6, 
        className="p-3"
    )
    
    metric_bar = dbc.Col(
        create_bar_plot(col, df, top_n=10), 
        width=6, 
        className="p-3"
    )
    
    pop_line = dbc.Col(
        create_line_plot("Population", df, countries=df.nlargest(5, col)["Entity"].tolist()), 
        width=6, 
        className="p-3"
    )
    
    gender_scatter = dbc.Col(
        create_scatter_plot("f_deaths", "m_deaths", df), 
        width=6, 
        className="p-3"
    )

    # Create rows with increased spacing
    row1 = dbc.Row([gdp_scatter, metric_bar], className="g-4 mb-4")
    row2 = dbc.Row([pop_line, gender_scatter], className="g-4")

    return html.Div(
        [row1, row2],
        style={
            "margin": "20px",
            "height": "calc(90vh - 150px)",
        }
    )
