from dash import dcc, html

from components.common.filter_slider import create_filter_slider
from components.common.plots import create_plots
from components.common.year_slider import create_year_slider


def create_geo_eco_tab():
    return html.Div(
        [
            # Add Store component for data
            dcc.Store(id='general-data'),
            create_filter_slider(),
            html.Br(),
            # Create a container div for the plots with the ID that matches the callback
            html.Div(id='4x4plots'),
            html.Br(),
            create_year_slider(),
        ]
    )
