#! usr/bin/env python3
import logging
import os
from functools import lru_cache
import functools
from flask import current_app
from flask_caching import Cache

cache = Cache()

def init_cache(app):
    cache.init_app(app, config={
        'CACHE_TYPE': 'RedisCache',
        'CACHE_REDIS_URL': os.environ.get('REDIS_URL', 'redis://localhost:6379/0'),
        'CACHE_DEFAULT_TIMEOUT': 86400
    })

import pandas as pd
from dash import Input, Output, callback
from components.common.gender_metric_selector import get_metric_column

logger = logging.getLogger(__name__)


@cache.memoize(timeout=3600)
def load_data():
    """Load data with caching."""
    logger.debug("Cache info for load_data: %s", load_data.cache_info())
    data_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "data",
        "heart_disease_data.csv",
    )
    df = pd.read_csv(data_path)

    # Pre-process data once during loading
    df["Year"] = pd.to_numeric(df["Year"], downcast="integer")

    # Convert numeric columns to efficient types
    for col in df.select_dtypes(include=["float64"]).columns:
        if col != "WB_Income":  # Skip WB_Income as it contains mixed types
            df[col] = pd.to_numeric(df[col], downcast="float")

    # Handle WB_Income column - convert NaN to string 'Unknown'
    df["WB_Income"] = df["WB_Income"].fillna("Unknown")
    df["WB_Income"] = df["WB_Income"].astype(str)

    logger.info("Loaded data shape: %s", df.shape)
    return df


# Load data once at module level
if current_app:
    data = load_data()
    UNIQUE_REGIONS = sorted(data["region"].unique())
    UNIQUE_INCOMES = sorted(data["WB_Income"].unique())
    UNIQUE_ENTITIES = sorted(data["Entity"].unique())
    YEAR_RANGE = (int(data["Year"].min()), int(data["Year"].max()))


@cache.memoize(timeout=3600)
@functools.lru_cache(maxsize=128)
def filter_data(year, regions=None, income=None):
    """Filter data with caching for common filter combinations."""
    logger.debug("Cache info for filter_data: %s", filter_data.cache_info())
    filtered = data[data["Year"] == year].copy()

    if regions and regions != ["All"]:
        filtered = filtered[filtered["region"].isin(regions)]

    if income and income != "All":
        filtered = filtered[filtered["WB_Income"] == str(income)]

    return filtered


@callback(Output("general-data", "data"), Input("year-slider", "value"))
def year_filter(year: int):
    """Filter data by year."""
    if year is None:
        logger.debug("No year selected")
        return []

    filtered_df = filter_data(year)
    return filtered_df.to_dict("records")


@callback(
    Output("geo-eco-data", "data"),
    Input("general-data", "data"),
    # Input('metric-dropdown', 'value'),
    Input("gender-dropdown", "value"),
    Input("region-dropdown", "value"),
    Input("income-dropdown", "value"),
    Input("top-filter-slider", "value"),
)
@functools.lru_cache(maxsize=256)
def geo_eco_data(data, metric, gender, region, income, top_n):
    """_summary_

    Args:
        data (_type_): _description_
        metric (_type_): _description_
        gender (_type_): _description_
        region (_type_): _description_
        income (_type_): _description_
        top_n (_type_): _description_

    Returns:
        _type_: _description_
    """
    logger.debug("Geo eco data called with: %s, %s, %s, %s", gender, region, income, top_n)
    # gender_prefix = "f_" if gender == "Female" else "m_" if gender == "Male" else ""
    # metric_mapping = {
    #     "P": {
    #         "Prevalence Percent": f"{gender_prefix}prev%",
    #         "Prevalence Rate": f"{gender_prefix}prev_rate",
    #         "Prevalence": f"{gender_prefix}prev",
    #     },
    #     "D": {
    #         "Death Percent": f"{gender_prefix}deaths%",
    #         "Death Rate": f"{gender_prefix}death_rate",
    #         "Death": f"{gender_prefix}deaths",
    #     },
    # }
    if gender is None or gender or region is None or income is None:
        return data

    if region is not None:
        df = data[data["region"] == region]
    if income is not None:
        df = df[df["WB_Income"] == str(income)]
    if top_n is not None:
        df = df.nlargest(int(top_n), float(metric))
    if gender is not None:
        col = get_metric_column(gender,metric)
        df = df[
            ["Entity", "Year", "Code", col, "gdp_pc", "WB_Income", "Population", "region"]
        ].dropna(subset=[col])

    return df


@callback(
    Output("chloropleth_data", "data"),
    Input("general-data", "data"),
    Input("metric-dropdown", "value"),
    Input("gender-dropdown", "value"),
)
def chloropleth_data(year_filtered_data, metric, gender):
    """Get data for chloropleth map."""
    if not year_filtered_data or not metric or not gender:
        return []

    df = pd.DataFrame(year_filtered_data)
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
    if not col:
        return []

    needed_cols = ["Entity", "Year", "Code", col]
    return df[needed_cols].to_dict("records")
