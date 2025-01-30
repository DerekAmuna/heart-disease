import plotly.express as px
from dash import Input, Output, callback, dcc, html


def create_world_map_tab():
    return html.Div(
        [
            html.Div(
                id="world-map-container",
                style={"height": "calc(100vh - 200px)", "margin": "0px", "padding": "0px"},
            ),
            html.Div(id="year-slider-container"),
        ]
    )


@callback(Output("world-map-container", "children"), Input("year-slider", "value"))
def update_map():
    fig = px.choropleth(
        locations=["USA", "GBR", "CAN"],
        locationmode="ISO-3",
        color=[1, 2, 3],
        color_continuous_scale="Reds",
    )
    fig.update_layout(
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=None,
    )
    return dcc.Graph(figure=fig, style={"height": "100%"}, config={"responsive": True})
