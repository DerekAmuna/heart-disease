import logging

import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, callback, dcc, html

from components.data.data import data  # Import the DataFrame directly

logger = logging.getLogger(__name__)


def create_scatter_plot(x_metric, y_metric, size=None, hue=None):
    """Create a scatter plot comparing two metrics with optional size and color encoding.

    Args:
        x_metric (str): Metric for x-axis
        y_metric (str): Metric for y-axis
        size (str, optional): Metric for point sizes
        hue (str, optional): Metric for point colors

    Returns:
        plotly.graph_objects.Figure: The scatter plot figure
    """
    fig = px.scatter(
        data_frame=data,
        x=x_metric,
        y=y_metric,
        size=size,
        color=hue,
        hover_data=["Entity", "Year"],
    )
    return fig


def estimate_risk_factors(df, target_year):
    """Estimate risk factors for years other than 2019 using linear interpolation."""
    if target_year == 2019:
        return df[df["Year"] == 2019].iloc[0], False

    # Get 2019 values as reference
    ref_data = df[df["Year"] == 2019]
    if ref_data.empty:
        return df.iloc[-1], True

    ref_data = ref_data.iloc[0]
    target_data = df[df["Year"] == target_year].iloc[0].copy()

    try:
        ref_death_rate = float(ref_data["m_death_rate"])
        target_death_rate = float(target_data["m_death_rate"])

        if pd.isna(ref_death_rate) or pd.isna(target_death_rate) or ref_death_rate == 0:
            return target_data, True

        ratio = target_death_rate / ref_death_rate

        risk_columns = ["obesity%", "t_htn_30-79", "t_high_bp_30-79", "t_htn_ctrl_30-79"]
        for col in risk_columns:
            if pd.notna(ref_data[col]):
                try:
                    ref_value = float(ref_data[col])
                    dampened_ratio = 1 + (ratio - 1) * 0.7
                    target_data[col] = ref_value * dampened_ratio
                except (ValueError, TypeError):
                    continue
    except (ValueError, TypeError):
        pass

    return target_data, True


def format_value(value, is_percent=True, is_estimate=False):
    """Format a numeric value as percentage or currency."""
    try:
        if pd.isna(value):
            return "N/A"
        if is_percent:
            formatted = f"{float(value):.1f}%"
        else:
            formatted = f"${int(value):,}"
        return f"{formatted} (est.)" if is_estimate else formatted
    except (ValueError, TypeError):
        return "N/A"


def create_tooltip(country_code, metric, gender, selected_year=None):
    """Create a tooltip with time series plot and risk factors for a country."""
    gender_prefix = "f_" if gender == "Female" else "m_" if gender == "Male" else ""
    metric_mapping = {
        "P": {
            "Prevalence Percent": f"{gender_prefix}prev%",
            "Prevalence Rate": f"{gender_prefix}prev_rate",
            "Prevalence": f"{gender_prefix}prev",
        },
        "D": {
            "Death Percent": f"{gender_prefix}deaths%",
            "Death Rate": f"{gender_prefix}death_rate",
            "Death": f"{gender_prefix}deaths",
        },
    }
    col = metric_mapping.get(metric[0], {}).get(metric)
    if col is None:
        return go.Figure(), {}

    columns_needed = [
        "Year",
        col,
        "Entity",
        "obesity%",
        "t_htn_30-79",
        "t_high_bp_30-79",
        "t_htn_ctrl_30-79",
        "gdp_pc",
    ]
    if col != "m_death_rate":
        columns_needed.append("m_death_rate")

    df = data[data["Code"] == country_code][columns_needed].copy()
    if df.empty:
        return go.Figure(), {}

    df = df[df["Year"] >= 1990].copy()

    if selected_year and selected_year in df["Year"].values:
        year_data, is_estimate = estimate_risk_factors(df, selected_year)
        year_text = f"{selected_year}"
    else:
        year_data, is_estimate = estimate_risk_factors(df, df.iloc[-1]["Year"])
        year_text = "Latest Year"

    risk_factors = {
        "Year": year_text + (" (values estimated)" if is_estimate else ""),
        "Obesity Rate": format_value(year_data["obesity%"], is_estimate=False),
        "Hypertension Prevalence": format_value(year_data["t_htn_30-79"], is_estimate=is_estimate),
        "High Blood Pressure": format_value(year_data["t_high_bp_30-79"], is_estimate=is_estimate),
        "Hypertension Control": format_value(
            year_data["t_htn_ctrl_30-79"], is_estimate=is_estimate
        ),
        "GDP per Capita": format_value(year_data["gdp_pc"], is_percent=False),
    }

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df["Year"],
            y=df[col],
            mode="lines+markers",
            name=metric,
            line=dict(width=2),
            marker=dict(size=6),
        )
    )

    if selected_year and selected_year in df["Year"].values:
        selected_value = df[df["Year"] == selected_year][col].iloc[0]
        fig.add_trace(
            go.Scatter(
                x=[selected_year],
                y=[selected_value],
                mode="markers",
                name="Selected Year",
                marker=dict(color="red", size=10, symbol="diamond"),
                showlegend=False,
            )
        )

    fig.update_layout(
        margin=dict(l=5, r=5, t=25, b=5),
        title=dict(
            text=f"{df['Entity'].iloc[0]}<br>{metric}", x=0.5, xanchor="center", font=dict(size=10)
        ),
        showlegend=False,
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor="lightgray", title=None, dtick=5),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor="lightgray", title=None),
    )

    return fig, risk_factors


def create_chloropleth_map(filtered_data):
    """Create a choropleth map visualization from filtered data.

    Args:
        filtered_data (list): List of dictionaries containing filtered data with
                            Entity, Year, Code, and metric columns

    Returns:
        plotly.graph_objects.Figure: The choropleth map figure
    """
    if not filtered_data:
        logger.debug("Creating chloropleth with no data")
        return go.Figure()

    df = pd.DataFrame(filtered_data)
    if df.empty:
        return go.Figure()

    metric_col = [col for col in df.columns if col not in ["Entity", "Year", "Code"]]
    if not metric_col:
        logger.warning("No metric column found in: %s", df.columns)
        return go.Figure()
    metric_col = metric_col[0]

    fig = go.Figure(
        data=go.Choropleth(
            locations=df["Code"],
            z=df[metric_col],
            locationmode="ISO-3",
            colorscale="RdYlBu_r",
            zmin=df[metric_col].quantile(0.1),
            zmax=df[metric_col].quantile(0.9),
            customdata=df[["Entity"]].values,
            hovertemplate="<b>%{customdata[0]}</b><br>"
            + f"{metric_col}: %{{z:,.2f}}<br>"
            + "<extra></extra>",
        )
    )

    fig.update_layout(
        margin={"l": 0, "r": 0, "t": 5, "b": 0},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        coloraxis_showscale=True,
        hovermode="closest",
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type="equirectangular",
            showland=True,
            landcolor="lightgray",
            showocean=True,
            oceancolor="aliceblue",
            projection=dict(scale=1.1),
        ),
    )

    fig.update_coloraxes(colorbar=dict(thickness=15, len=0.7, x=0.95, y=0.5, xanchor="left"))

    return fig


def create_bar_plot(metric, top_n=10):
    """Create a bar plot for the top N countries by a given metric."""
    sorted_data = data.nlargest(top_n, metric)
    fig = px.bar(
        sorted_data,
        x="Entity",
        y=metric,
        title=f"Top {top_n} Countries by {metric}",
        color=metric,
        color_continuous_scale="Reds",
    )

    fig.update_layout(
        margin={"l": 20, "r": 20, "t": 40, "b": 20},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=None,
        xaxis_tickangle=-45,
    )

    return dcc.Graph(figure=fig, style={"height": "100%"}, config={"displayModeBar": False})


def create_line_plot(metric, countries=None):
    """Create a line plot for a given metric over time by specified countries."""
    if countries is None:
        countries = data["Entity"].unique()[:5]  # Default to top 5 countries

    filtered_data = data[data["Entity"].isin(countries)]

    fig = px.line(
        filtered_data, x="Year", y=metric, color="Entity", title=f"{metric} Over Time by Country"
    )

    fig.update_layout(
        margin={"l": 20, "r": 20, "t": 40, "b": 20},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=None,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    return dcc.Graph(figure=fig, style={"height": "100%"}, config={"displayModeBar": False})


def create_geo_eco_plots():
    """Create geographical and economic plots in a layout."""
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(create_scatter_plot("gdp_pc", "death_std"), width=6, className="p-1"),
                    dbc.Col(create_bar_plot("life_expectancy"), width=6, className="p-1"),
                ],
                className="g-0",
            ),
            dbc.Row(
                [
                    dbc.Col(create_line_plot("population"), width=6, className="p-1"),
                    dbc.Col(create_scatter_plot("f_deaths", "m_deaths"), width=6, className="p-1"),
                ],
                className="g-0",
            ),
        ],
        style={"margin": "0", "height": "calc(90vh - 150px)"},
    )
