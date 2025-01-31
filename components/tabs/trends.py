from dash import dcc, html

from components.common.filter_slider import create_filter_slider
from components.common.plots import create_plots
from components.common.year_slider import create_year_slider


def create_trends_tab():
    return html.Div(
        [
            create_filter_slider(),
            create_plots(),
            html.Br(),
        ]
    )
