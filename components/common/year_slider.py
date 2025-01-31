from dash import dcc, html


def create_year_slider():
    return html.Div(
        [
            html.Label("Year Slider"),
            dcc.Slider(
                id="year-slider",
                min=1960,
                max=2022,
                step=1,
                value=2000,
                marks={i: str(i) for i in range(1960, 2022, 5)},
            ),
        ],
        style={"margin-bottom": "30px"},
    )
