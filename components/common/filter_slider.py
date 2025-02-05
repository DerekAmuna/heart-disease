from dash import dcc, html


def create_filter_slider():
    marks = {i: str(i) for i in range(10, 101, 10)}  # Generate marks for the slider
    return html.Div(
        [
            html.Label("Filter by top:"),
            dcc.Slider(
                id="top-filter-slider",
                min=10,
                max=100,
                step=10,
                value=10,  # Adjusted initial value to be within bounds
                marks=marks,
            ),
        ]
    )
