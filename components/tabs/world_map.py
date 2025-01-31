import plotly.express as px
from dash import Input, Output, callback, dcc, html

from components.common.year_slider import create_year_slider


def create_world_map_tab():
    return html.Div(
        [
            html.Div(
                id="world-map-container",
                style={"height": "calc(100vh - 300px)", "margin": "0px", "padding": "0px"},
            ),
            html.Br(),
            create_year_slider(),
        ]
    )


@callback(Output("world-map-container", "children"), Input("year-slider", "value"))
def update_map(selected_year):
    if selected_year is None:
        selected_year = 2021  # Default year if none selected

    # For now using dummy data
    fig = px.choropleth(
        locations=["USA", "GBR", "CAN"],
        locationmode="ISO-3",
        color=[1, 2, 3],
        color_continuous_scale="Reds",
        title=f"Heart Disease Data for {selected_year}",
        color_continuous_midpoint=2,
    ).update_traces(showscale=False)

    fig.update_layout(
        margin={"l": 0, "r": 0, "t": 30, "b": 0},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=None,
        showlegend=False,
        geo=dict(showframe=False, showcoastlines=True, projection_type="equirectangular"),
    )
    return dcc.Graph(
        figure=fig,
        style={"height": "100%"},
        config={"responsive": True, "displayModeBar": False, "scrollZoom": True},
    )
