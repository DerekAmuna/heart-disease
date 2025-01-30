import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State

from components.sidebar import create_sidebar

#  FontAwesome for icons
FA = "https://use.fontawesome.com/releases/v5.15.4/css/all.css"
application = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, FA])

# main content
main_content = html.Div(
    [
        # Tabs
        dbc.Tabs(
            [
                dbc.Tab(label="World Map", tab_id="tab-1"),
                dbc.Tab(label="Geo-Eco Features", tab_id="tab-2"),
                dbc.Tab(label="Healthcare Features", tab_id="tab-3"),
                dbc.Tab(label="Trends", tab_id="tab-4"),
            ],
            id="tabs",
            active_tab="tab-1",
        ),
        # Tab content
        html.Div(id="tab-content", className="mt-3"),
    ],
    id="page-content",
    style={
        "margin-left": "16rem",
        "padding": "2rem",
        "transition": "margin-left .3s",
        "width": "calc(100% - 16rem)",
    },
)

# main app layout
application.layout = html.Div(
    [dcc.Location(id="url", refresh=False), create_sidebar(), main_content],
    style={"position": "relative"},
)

if __name__ == "__main__":
    application.run_server(debug=True, dev_tools_hot_reload=True, dev_tools_ui=True)
