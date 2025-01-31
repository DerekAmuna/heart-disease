from dash import dcc, html


def create_filter_slider():
    return html.Div(
        [
            html.Label("Filter by top:"),
            dcc.Slider(
                id="top-filter-slider",
                min=10,
                max=100,
                step=10,
                value=5,
                marks={i: str(i) for i in range(10, 110, 10)},
            ),
        ]
    )
