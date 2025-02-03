from dash import html
import dash_bootstrap_components as dbc

def create_introduction_tab():
    return dbc.Container([
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

                html.Br(),
                html.Hr(),
                html.H4("Overview of Dataset", className="fw-bold"),
                html.Br(),

                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.H5("Data Source", className="card-title"),
                                html.P("World Health Organization (WHO) Global Health Observatory", className="card-text")
                            ], md=6),
                            dbc.Col([
                                html.H5("Time Period", className="card-title"),
                                html.P("1950-2022", className="card-text")
                            ], md=6),
                        ]),
                        html.Br(),
                        html.H5("Key Variables", className="card-title"),
                        dbc.Row([
                            dbc.Col([
                                dbc.ListGroup([
                                    dbc.ListGroupItem([
                                        html.Strong("Health Metrics"),
                                        html.Ul([
                                            html.Li("Heart disease mortality rate"),
                                            html.Li("Healthcare expenditure"),
                                            html.Li("Medical access and intervention outcomes"),
                                        ], className="mb-0")
                                    ]),
                                    dbc.ListGroupItem([
                                        html.Strong("Economic Indicators"),
                                        html.Ul([
                                            html.Li("GDP per capita"),
                                            html.Li("Healthcare spending % of GDP"),
                                            html.Li("Development index")
                                        ], className="mb-0")
                                    ]),
                                    dbc.ListGroupItem([
                                        html.Strong("Demographic Factors"),
                                        html.Ul([
                                            html.Li("Population demographics"),
                                            html.Li("Geographic regions"),
                                            html.Li("Urban vs rural distribution")
                                        ], className="mb-0")
                                    ])
                                ], flush=True)
                            ])
                        ]),
                        html.Br(),
                        html.H5("Data Coverage", className="card-title"),
                        html.P([
                            "This dataset covers ", 
                            html.Strong("194 countries"),
                            " across all WHO regions, providing a comprehensive global perspective on heart disease trends and related factors."
                        ]),
                    ])
                ], className="shadow-sm")
            ], md=8)
        ], justify="center"),
    ], fluid=True)