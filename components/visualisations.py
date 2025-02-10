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

from statsmodels.nonparametric.smoothers_lowess import lowess

logger = logging.getLogger(__name__)

# Common layout settings
BASE_LAYOUT = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font": {"size": 12},
}

COMMON_LAYOUT = {
    "showlegend": False,
}


GRID_SETTINGS = {"gridwidth": 1, "gridcolor": "rgba(128,128,128,0.1)", "zeroline": False}


@lru_cache(maxsize=32)
def get_title_text(metric):
    """Cache title text generation."""
    return metric.replace("_", " ").title()


def create_scatter_plot(x_metric, y_metric, data, size=None, hue=None, top_n=5):
    """Create a scatter plot comparing two metrics with optional size and color encoding."""
    print(f"Creating scatter plot: x={x_metric}, y={y_metric}, data shape={data.shape}")
    print(f"Data columns: {data.columns.tolist()}")
    print(f"Data values:\n{data[[x_metric, y_metric]].head()}")

    if data.empty or x_metric not in data.columns or y_metric not in data.columns:
        print(f"Data validation failed: empty={data.empty}, x_exists={x_metric in data.columns}, y_exists={y_metric in data.columns}")
        return create_no_data_figure("No data available for selected metrics")

    plot_data = data.copy()

    # Convert numeric columns
    plot_data[x_metric] = pd.to_numeric(plot_data[x_metric], errors='coerce')
    plot_data[y_metric] = pd.to_numeric(plot_data[y_metric], errors='coerce')
    plot_data = plot_data.dropna(subset=[x_metric, y_metric])

    print(f"After numeric conversion: shape={plot_data.shape}")
    print(f"Numeric values:\n{plot_data[[x_metric, y_metric]].head()}")

    # Take top N if specified
    if top_n:
        plot_data = plot_data.nlargest(int(top_n), y_metric)
        print(f"After top_n filter: shape={plot_data.shape}")

    fig = px.scatter(
        data_frame=plot_data,
        x=x_metric,
        y=y_metric,
        color=hue if hue in plot_data.columns else None,
        hover_name="Entity",
        labels={x_metric: get_title_text(x_metric), y_metric: get_title_text(y_metric)},
    )

    layout = {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"size": 12},
        "showlegend": True if hue else False,
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
    for axis in [fig.update_xaxes, fig.update_yaxes]:
        axis(**GRID_SETTINGS)

    return dcc.Graph(figure=fig, style={"height": "100%"}, config={"displayModeBar": False})


def format_value(value, is_percent=True, is_estimate=True, is_obesity=False):
    """Format a value for display.

    Args:
        value: The value to format
        is_percent (bool): Whether the value is a percentage
        is_estimate (bool): Whether to show decimal places
        is_obesity (bool): Whether this is an obesity rate (already in percentage)

    Returns:
        str: Formatted value
    """
    if pd.isna(value):
        return "N/A"

    try:
        if is_percent:
            if is_obesity:
                return f"{float(value):.1f}%"
            return f"{float(value) * 100:.1f}%"
        elif isinstance(value, (int, float)):
            if value >= 1000000:
                return f"{value/1000000:.1f}M"
            elif value >= 1000:
                return f"{value/1000:.1f}K"
            else:
                return f"{value:.1f}" if is_estimate else f"{int(value):,}"
        return str(value)
    except:
        return "N/A"


def create_tooltip(country_name, metric, gender, age, selected_year=None):
    """Create a tooltip with time series plot and risk factors for a country."""
    # Get data for the country
    df = data.copy()
    df = df[df["Entity"] == country_name]

    if df.empty:
        return None, {"message": "No data available for this country"}

    # Get appropriate column based on metric and gender
    col = get_metric_column(gender, metric)
    if not col:
        return None, {"message": "Invalid metric selection"}

    # Check if metric is a percent type
    is_percent = "percent" in metric.lower()

    # Create time series plot for cardiovascular diseases
    cv_df = df[(df["cause"].str.lower() == "cardiovascular diseases") & (df['age'] == age)]
    cv_df = cv_df.dropna(subset=[col])

    if cv_df.empty:
        return None, {"message": f"No data available for {metric} with age group: {age}"}

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=cv_df["Year"],
            y=cv_df[col],
            mode="lines+markers",
            name=metric,
            line=dict(color="#1f77b4"),
        )
    )

    # Add marker for selected year if provided
    if selected_year:
        year_data = cv_df[cv_df["Year"] == selected_year]
        if not year_data.empty:
            fig.add_trace(
                go.Scatter(
                    x=[selected_year],
                    y=[year_data[col].iloc[0]],
                    mode="markers",
                    marker=dict(size=10, color="red"),
                    name=f"Selected Year ({selected_year})",
                )
            )

    fig.update_layout(
        title=f"{metric} in {country_name}",
        xaxis_title="Year",
        yaxis_title=metric,
        showlegend=False,
        margin=dict(l=0, r=0, t=30, b=0),
        height=200,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    # Get other causes data for the selected year
    risk_factors = {"Year": selected_year if selected_year else "No year selected"}

    if selected_year:
        # Add obesity and GDP per capita
        year_data = df[df["Year"] == selected_year].iloc[0]
        if "obesity%" in year_data and pd.notna(year_data["obesity%"]):
            risk_factors["Obesity Rate"] = format_value(year_data["obesity%"], is_percent=True, is_obesity=True)
        if "gdp_pc" in year_data and pd.notna(year_data["gdp_pc"]):
            risk_factors["GDP per capita"] = format_value(year_data["gdp_pc"], is_percent=False)

        # Add other causes
        other_causes = df[
            (df["Year"] == selected_year) &
            (df["cause"].str.lower() != "cardiovascular diseases") &
            (df["age"] == age)
        ]
        other_causes = other_causes.dropna(subset=[col])

        # Add each cause's value
        for _, row in other_causes.iterrows():
            risk_factors[row["cause"]] = format_value(row[col], is_percent=is_percent)

    return fig, risk_factors


def create_no_data_figure(message):
    """Create an empty figure with a message for no data cases."""
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=14),
    )
    fig.update_layout(
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=False, showticklabels=False),
        height=200,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


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
        **BASE_LAYOUT,
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


def create_line_plot(metric, data, top_n=5, n_metric=None):
    """Create a line plot for a given metric over time."""
    filtered_data = data[data["Year"] >= 2000]
    print(f"Line plot for {metric}")
    print(f"Years in data: {sorted(filtered_data['Year'].unique())}")
    print(f"Sample of data:\n{filtered_data[['Year', metric]].head()}")

    # Get top N entities by metric value in the most recent year
    latest_year = filtered_data["Year"].max()
    if n_metric and n_metric in filtered_data.columns:
        sort_metric = n_metric
    else:
        sort_metric = metric

    top_entities = (
        filtered_data[filtered_data["Year"] == latest_year]
        .nlargest(top_n, sort_metric)["Entity"]
        .tolist()
    )
    filtered_data = filtered_data[filtered_data["Entity"].isin(top_entities)]
    print(f"Unique years per entity:")
    print(filtered_data.groupby("Entity")["Year"].nunique())

    fig = px.line(
        filtered_data,
        x="Year",
        y=metric,
        color="Entity",
        labels={metric: get_title_text(metric)},
    )

    layout = {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"size": 12},
        "showlegend": True,
        "margin": {"l": 60, "r": 30, "t": 50, "b": 50},
        "height": None,
        "title": {
            "text": f"{get_title_text(metric)} Over Time" + (f" by {get_title_text(n_metric)}" if n_metric else ""),
            "y": 1,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 14},
        },
    }

    fig.update_layout(**layout)
    for axis in [fig.update_xaxes, fig.update_yaxes]:
        axis(**GRID_SETTINGS)

    return dcc.Graph(figure=fig, style={"height": "100%"}, config={"displayModeBar": False})


def create_chloropleth_map(filtered_data, metric, gender="Both"):
    """Create a choropleth map visualization from filtered data.

    Args:
        filtered_data (list): List of dictionaries containing filtered data
        metric (str): Selected metric name
        gender (str, optional): Selected gender. Defaults to "Both".

    Returns:
        plotly.graph_objects.Figure: The choropleth map figure
    """

    # Convert list of dicts to DataFrame
    df = pd.DataFrame(filtered_data)
    if df.empty:
        return go.Figure()

    # Get the appropriate column based on metric and gender
    metric_col = get_metric_column(gender, metric)
    if not metric_col:
        return go.Figure()

    # Create figure
    fig = go.Figure(
        data=go.Choropleth(
            locations=df["Entity"],
            locationmode="country names",
            z=df[metric_col],
            text=df["Entity"],
            colorscale="Viridis",
            autocolorscale=False,
            reversescale=True,
            marker_line_color="darkgray",
            marker_line_width=0.5,
            colorbar_title=metric,
        )
    )

    #projection types
#     ['airy', 'aitoff', 'albers', 'albers usa', 'august',
# 'azimuthal equal area', 'azimuthal equidistant', 'baker',
# 'bertin1953', 'boggs', 'bonne', 'bottomley', 'bromley',
# 'collignon', 'conic conformal', 'conic equal area', 'conic
# equidistant', 'craig', 'craster', 'cylindrical equal
# area', 'cylindrical stereographic', 'eckert1', 'eckert2',
# 'eckert3', 'eckert4', 'eckert5', 'eckert6', 'eisenlohr',
# 'equal earth', 'equirectangular', 'fahey', 'foucaut',
# 'foucaut sinusoidal', 'ginzburg4', 'ginzburg5',
# 'ginzburg6', 'ginzburg8', 'ginzburg9', 'gnomonic',
# 'gringorten', 'gringorten quincuncial', 'guyou', 'hammer',
# 'hill', 'homolosine', 'hufnagel', 'hyperelliptical',
# 'kavrayskiy7', 'lagrange', 'larrivee', 'laskowski',
# 'loximuthal', 'mercator', 'miller', 'mollweide', 'mt flat
# polar parabolic', 'mt flat polar quartic', 'mt flat polar
# sinusoidal', 'natural earth', 'natural earth1', 'natural
# earth2', 'nell hammer', 'nicolosi', 'orthographic',
# 'patterson', 'peirce quincuncial', 'polyconic',
# 'rectangular polyconic', 'robinson', 'satellite', 'sinu
# mollweide', 'sinusoidal', 'stereographic', 'times',
# 'transverse mercator', 'van der grinten', 'van der
# grinten2', 'van der grinten3', 'van der grinten4',
# 'wagner4', 'wagner6', 'wiechel', 'winkel tripel',
# 'winkel3']

    fig.update_layout(
        **COMMON_LAYOUT,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=None,
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type="orthographic",
            showocean=True,
            oceancolor="rgba(0,0,0,0)",
            showland=True,
            landcolor="rgba(0,0,0,0)",
            showlakes=True,
            lakecolor="rgba(0,0,0,0)",
            showrivers=True,
            rivercolor="rgba(0,0,0,0)",
            showcountries=True,
            countrycolor="gray",
            countrywidth=0.5,
            showsubunits=True,
            subunitcolor="gray",
            subunitwidth=0.5
        ),
    )

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
        **BASE_LAYOUT,
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


def create_trend_plot(data, metric, year, gender):
    """Create a trend plot showing the metric over time for each cause."""
    df = data.copy()

    # Get appropriate column based on metric and gender
    col = get_metric_column(gender, metric)
    if not col or df.empty:
        return create_no_data_figure("No data available for selected filters")

    # Create figure
    fig = go.Figure()

    # Color mapping for causes
    colors = {
        "Cardiovascular diseases": "#1f77b4",
        "Cancer": "#ff7f0e",
        "Respiratory diseases": "#2ca02c",
        "Diabetes": "#d62728",
        "Liver diseases": "#9467bd",
        "Digestive diseases": "#8c564b",
        "Lower respiratory infections": "#e377c2",
        "Alzheimer's disease": "#7f7f7f",
    }

    # Add traces for each cause
    for cause in df["cause"].unique():
        cause_data = df[df["cause"] == cause]

        # Group by year to get mean values
        yearly_data = cause_data.groupby("Year")[col].mean().reset_index()

        # Get color for cause (default to gray if not in mapping)
        color = colors.get(cause, "#17becf")

        # Add actual data
        fig.add_trace(
            go.Scatter(
                x=yearly_data["Year"],
                y=yearly_data[col],
                name=cause,
                mode="lines+markers",
                line=dict(color=color),
            )
        )

        # Fit LOWESS to existing data
        lowess_data = lowess(
            yearly_data[col],
            yearly_data["Year"],
            frac=0.5,
            it=1,
            return_sorted=True
        )

        # Project trend to 2030
        last_years = lowess_data[-5:]  # Use last 5 years for projection
        slope = np.polyfit(last_years[:, 0], last_years[:, 1], deg=1)[0]
        future_years = np.arange(yearly_data["Year"].max() + 1, 2031)
        projection = slope * (future_years - yearly_data["Year"].max()) + lowess_data[-1, 1]

        # Add LOWESS trend
        fig.add_trace(
            go.Scatter(
                x=lowess_data[:, 0],
                y=lowess_data[:, 1],
                name=f"{cause} (Trend)",
                mode="lines",
                line=dict(
                    dash="dot",
                    color=color,
                ),
                showlegend=False,
            )
        )

        # Add projection
        fig.add_trace(
            go.Scatter(
                x=future_years,
                y=projection,
                name=f"{cause} (Projection)",
                mode="lines",
                line=dict(
                    dash="dash",
                    color=color,
                ),
                showlegend=False,
            )
        )

    fig.update_layout(
        title=f"{metric} Trends Over Time",
        xaxis_title="Year",
        yaxis_title=metric,
        height=600,
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255, 255, 255, 0.8)",
        ),
        hovermode="x unified",
    )

    return dcc.Graph(figure=fig, config={"displayModeBar": False})
