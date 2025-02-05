import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback
from components.visualisations import create_scatter_plot, create_bar_plot, create_line_plot
from components.data.data import data, filter_data

@callback(
    Output('4x4plots','children'),
    Input('year-slider', 'value'),
    Input('metric-dropdown', 'value'),
    Input('gender-dropdown', 'value'),
    Input('top-filter-slider', 'value'),
    Input('country-dropdown', 'value'),
    Input('region-dropdown', 'value'),
    Input('income-dropdown', 'value')
)
def create_plots(year, metric, gender, top_n, countries, regions, income):
    """Create a grid of plots using visualizations from visualisations.py."""
    if not year or not metric or not gender:
        return html.Div(style={"margin": "20px", "height": "calc(90vh - 150px)"})

    # Use cached filter function
    df = filter_data(year, regions, income)
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

    # Get selected countries or top N
    selected_countries = countries if countries else df.nlargest(top_n, col)["Entity"].tolist()
    
    # Create plots
    plots = {
        'gdp_scatter': dbc.Col(
            create_scatter_plot("gdp_pc", "death_std", df, top_n=top_n),
            width=6,
            className="px-2 py-2"
        ),
        'metric_bar': dbc.Col(
            create_bar_plot(col, df, top_n=top_n),
            width=6,
            className="px-2 py-2"
        ),
        'pop_line': dbc.Col(
            create_line_plot("Population", data, countries=selected_countries, top_n=top_n),
            width=6,
            className="px-2 py-2"
        ),
        'gender_scatter': dbc.Col(
            create_scatter_plot("f_deaths", "m_deaths", df),
            width=6,
            className="px-2 py-2"
        )
    }

    # Create layout
    row1 = dbc.Row([plots['gdp_scatter'], plots['metric_bar']], className="g-0 mb-2")
    row2 = dbc.Row([plots['pop_line'], plots['gender_scatter']], className="g-0")

    return html.Div(
        [row1, row2],
        style={
            "margin": "10px",
            "height": "calc(90vh - 150px)",
            "backgroundColor": "white",
            "borderRadius": "8px",
            "padding": "15px",
            "boxShadow": "0 2px 4px rgba(0,0,0,0.05)"
        }
    )
