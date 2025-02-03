import dash_html_components as html
import dash_bootstrap_components as dbc

introduction = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.H1("Heart Disease Data Visualization", className="text-center text-primary fw-bold"),
            html.P(
                "Welcome to the Heart Disease Data Visualization Dashboard. "
                "This dashboard provides in-depth insights into heart disease statistics worldwide.",
                className="lead text-center"
            ),

            
            html.Hr(),
            html.H4("What You Can Do Here:", className="fw-bold"),
            html.Br(),

            html.Ul([
                html.Li("🌍 View heart disease distribution across the world"),
                html.Li("📊 Analyze economic and geographical factors"),
                html.Li("🏥 Investigate healthcare trends"),
                html.Li("🔎 Filter data by year, region, and more"),
            ], className="fs-5"),
        ], md=8)
    ], justify="center"),
], fluid=True)