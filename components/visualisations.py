import logging
from functools import lru_cache

import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html
from scipy import stats
from scipy.stats import t

from components.common import gender_metric_selector
from components.common.gender_metric_selector import get_metric_column
from components.data.data import data  # Import the DataFrame directly

logger = logging.getLogger(__name__)

# Common layout settings
COMMON_LAYOUT = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font": {"size": 12},
    "showlegend": False,
}

GRID_SETTINGS = {"gridwidth": 1, "gridcolor": "rgba(128,128,128,0.1)", "zeroline": False}


@lru_cache(maxsize=32)
def get_title_text(metric):
    """Cache title text generation."""
    return metric.replace("_", " ").title()


def create_scatter_plot(x_metric, y_metric, data, size=None, hue=None, top_n=5):
    """Create a scatter plot comparing two metrics with optional size and color encoding."""
    plot_data = data.copy()

    # Handle NaN values in size column if specified
    if size is not None:
        # Fill NaN values with the minimum non-NaN value
        min_size = plot_data[size].min()
        plot_data[size] = plot_data[size].fillna(min_size)

    fig = px.scatter(
        data_frame=plot_data,
        x=x_metric,
        y=y_metric,
        size=size,
        color=hue,
        hover_name="Entity",
        labels={x_metric: get_title_text(x_metric), y_metric: get_title_text(y_metric)},
    )

    layout = {
        **COMMON_LAYOUT,
        "margin": {"l": 60, "r": 30, "t": 50, "b": 50},
        "height": 300,
        "title": {
            "text": f"{get_title_text(x_metric)} vs {get_title_text(y_metric)}",
            "y": 1,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 14},
        },
    }

    fig.update_layout(**layout)
    fig.update_traces(marker=dict(size=8), selector=dict(mode="markers"))

    for axis in [fig.update_xaxes, fig.update_yaxes]:
        axis(**GRID_SETTINGS)

    return dcc.Graph(figure=fig, style={"height": "100%"}, config={"displayModeBar": False})


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
    country_data = data[data["Code"] == country_code]
    if country_data.empty:
        return "No data available"

    col = get_metric_column(gender, metric)
    if not col:
        return "Invalid metric"

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

    df = country_data[columns_needed].copy()
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


def create_bar_plot(metric, data, top_n=5, color=None):
    """Create a bar plot for a given metric.

    Args:
        metric (str): Column to plot
        data (pd.DataFrame): Data to plot
        top_n (int, optional): Number of top entries to show. Defaults to 5.
        color (str, optional): Column to use for color coding. Defaults to None.
    """
    df = data.nlargest(top_n, metric)

    fig = px.bar(
        df,
        x="Entity",
        y=metric,
        hover_name="Entity",
        labels={metric: get_title_text(metric)},
        color=color,
    )

    layout = {
        **COMMON_LAYOUT,
        "margin": {"l": 60, "r": 30, "t": 50, "b": 70},
        "height": None,
        "coloraxis_showscale": False,
        "title": {
            "text": f"Top {top_n} Countries by {get_title_text(metric)}",
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 14},
        },
    }

    fig.update_layout(**layout)
    fig.update_xaxes(tickangle=-45, showgrid=False, title=None)
    fig.update_yaxes(**GRID_SETTINGS)

    return dcc.Graph(figure=fig, style={"height": "100%"}, config={"displayModeBar": False})


def create_line_plot(metric, data, countries=None, top_n=5):
    """Create a line plot for a given metric over time by specified countries."""
    filtered_data = data[data["Year"] >= 2000].copy()

    if countries is None:
        countries = data["Entity"].unique()[:top_n]
    filtered_data = filtered_data[filtered_data["Entity"].isin(countries)]

    fig = px.line(
        filtered_data, x="Year", y=metric, color="Entity", labels={metric: get_title_text(metric)}
    )

    layout = {
        **COMMON_LAYOUT,
        "margin": {"l": 20, "r": 10, "t": 15, "b": 15},
        "height": None,
        "showlegend": True,
        "legend": {
            "orientation": "v",
            "yanchor": "top",
            "y": 1,
            "xanchor": "left",
            "x": 0,
            "font": {"size": 10},
            # 'position':'left'
        },
        "title": {
            "text": f"{get_title_text(metric)} Over Time",
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 14},
        },
    }

    fig.update_layout(**layout)
    fig.update_traces(line={"width": 2})

    x_axis_settings = {**GRID_SETTINGS, "dtick": 5, "tick0": 2000}

    fig.update_xaxes(**x_axis_settings)
    fig.update_yaxes(**GRID_SETTINGS)

    return dcc.Graph(figure=fig, style={"height": "100%"}, config={"displayModeBar": False})


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


def create_sankey_diagram(data, metric, gender):
    """Create a Sankey diagram showing flow between Region -> Income -> Metric Ranges."""
    metric = get_metric_column(gender, metric)
    df = data[data["Year"] == 2019]
    df = df.dropna(subset=[metric, "region", "WB_Income"])

    if df.empty:
        return dcc.Graph()

    try:
        labels = [f"{get_title_text(metric)} ({i}%)" for i in ["0-25", "25-50", "50-75", "75-100"]]
        df["metric_range"] = pd.qcut(df[metric], q=4, labels=labels, duplicates="drop")
    except ValueError:
        bins = [
            df[metric].min(),
            df[metric].mean() / 2,
            df[metric].mean(),
            df[metric].mean() * 1.5,
            df[metric].max(),
        ]
        labels = [
            f"{get_title_text(metric)} (Low)",
            f"{get_title_text(metric)} (Medium-Low)",
            f"{get_title_text(metric)} (Medium-High)",
            f"{get_title_text(metric)} (High)",
        ]
        df["metric_range"] = pd.cut(df[metric], bins=bins, labels=labels, duplicates="drop")

    regions = df["region"].unique().tolist()
    incomes = df["WB_Income"].unique().tolist()
    ranges = df["metric_range"].unique().tolist()
    nodes = regions + incomes + ranges
    sources, targets, values = [], [], []
    link_colors = []

    for region in regions:
        region_idx = nodes.index(region)
        region_data = df[df["region"] == region]
        for income in incomes:
            income_idx = nodes.index(income)
            income_data = region_data[region_data["WB_Income"] == income]
            if not income_data.empty:
                sources.append(region_idx)
                targets.append(income_idx)
                values.append(len(income_data))
                link_colors.append("rgba(31, 119, 180, 0.4)")  # Light blue

    for income in incomes:
        income_idx = nodes.index(income)
        income_data = df[df["WB_Income"] == income]
        for range_val in ranges:
            range_idx = nodes.index(range_val)
            range_data = income_data[income_data["metric_range"] == range_val]
            if not range_data.empty:
                sources.append(income_idx)
                targets.append(range_idx)
                values.append(len(range_data))
                link_colors.append("rgba(44, 160, 44, 0.4)")  # Light green

    node_colors = (
        ["#1f77b4"] * len(regions) + ["#2ca02c"] * len(incomes) + ["#ff7f0e"] * len(ranges)
    )

    fig = go.Figure(
        data=[
            go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=nodes,
                    color=node_colors,
                ),
                link=dict(source=sources, target=targets, value=values, color=link_colors),
            )
        ]
    )

    fig.update_layout(
        **COMMON_LAYOUT,
        height=400,
        title=dict(
            text=f"Distribution of {get_title_text(metric)} across Regions and Income Groups",
            y=0.95,
            x=0.5,
            xanchor="center",
            yanchor="top",
            font=dict(size=14),
        ),
    )

    return dcc.Graph(figure=fig, config={"displayModeBar": False})


def create_trend_plot(data, metric, year, gender="Both"):
    """Create a line plot with LOWESS trend and projection to 2030."""
    metric_col = get_metric_column(gender, metric)
    if not metric_col:
        return dcc.Graph()

    df = data.copy()
    df = df.dropna(subset=[metric_col, "Year"])
    yearly_means = df.groupby("Year")[metric_col].mean().reset_index()

    from statsmodels.nonparametric.smoothers_lowess import lowess

    historical_lowess = lowess(
        yearly_means[metric_col], yearly_means["Year"], frac=0.5, it=1, return_sorted=True
    )

    future_years = np.linspace(yearly_means["Year"].max(), 2030, num=20)
    last_points = historical_lowess[-10:]
    last_slope = np.polyfit(last_points[:, 0], last_points[:, 1], deg=1)[0]
    projection = (future_years - yearly_means["Year"].max()) * last_slope + historical_lowess[
        -1, 1
    ]

    std_dev = np.std(
        yearly_means[metric_col]
        - np.interp(yearly_means["Year"], historical_lowess[:, 0], historical_lowess[:, 1])
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=yearly_means["Year"],
            y=yearly_means[metric_col],
            mode="markers",
            name="Historical Data",
            marker=dict(color="#1f77b4", size=8),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=historical_lowess[:, 0],
            y=historical_lowess[:, 1],
            mode="lines",
            name="LOWESS Trend",
            line=dict(color="#2ca02c", width=2),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=future_years,
            y=projection,
            mode="lines",
            name="Projection to 2030",
            line=dict(color="#ff7f0e", dash="dash", width=2),
        )
    )

    for data, color, name in [
        (historical_lowess, "rgba(44, 160, 44, 0.2)", "95% Confidence Band"),
        (
            np.column_stack((future_years, projection)),
            "rgba(255, 127, 14, 0.2)",
            "Projection Uncertainty",
        ),
    ]:
        fig.add_trace(
            go.Scatter(
                x=data[:, 0],
                y=data[:, 1] + 2 * std_dev,
                mode="lines",
                line=dict(width=0),
                showlegend=False,
                hoverinfo="skip",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=data[:, 0],
                y=data[:, 1] - 2 * std_dev,
                mode="lines",
                line=dict(width=0),
                fill="tonexty",
                fillcolor=color,
                name=name,
                hoverinfo="skip",
            )
        )

    fig.add_vline(x=year, line_dash="dot", line_color="gray", opacity=0.5)

    layout = {
        **COMMON_LAYOUT,
        "title": dict(
            text=f"Trend Analysis: {get_title_text(metric)} ({gender})",
            y=0.95,
            x=0.5,
            xanchor="center",
            yanchor="top",
        ),
        "xaxis": dict(title="Year", range=[yearly_means["Year"].min() - 1, 2031]),
        "yaxis": dict(title=get_title_text(metric)),
        "hovermode": "x unified",
    }

    fig.update_layout(layout)
    return dcc.Graph(figure=fig, config={"displayModeBar": False})
