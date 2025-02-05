from dash import dcc, html


def create_healthcare_tab():
    """FUnction to display the layout for the healthcare tab"""
    return html.Div(
        [html.H3("Healthcare Features Visualization"), dcc.Graph(id="healthcare-graph")]
    )
