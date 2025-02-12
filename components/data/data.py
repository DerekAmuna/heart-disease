#! usr/bin/env python3
import logging
import os
from functools import lru_cache

import polars as pl
from cachetools import TTLCache, cached
from cachetools.keys import hashkey
from dash import Input, Output, callback

from components.common.gender_metric_selector import get_metric_column

logger = logging.getLogger(__name__)


def make_hashable(value):
    """Convert unhashable types to hashable ones for caching."""
    if isinstance(value, list):
        return tuple(sorted(value))
    return value


def cache_key(*args, **kwargs):
    """Create a hashable key for caching."""
    return hashkey(
        *(make_hashable(arg) for arg in args), **{k: make_hashable(v) for k, v in kwargs.items()}
    )


@cached(cache=TTLCache(maxsize=128, ttl=300), key=cache_key)
def load_data():
    """Load data with caching using Polars."""
    # logger.debug("Cache info for load_data: %s", load_data.cache_info())
    data_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "heart_processed.csv"
    )
    df = pl.read_csv(data_path)
    # Pre-process data once during loading: convert Year to integer
    df = df.with_columns(pl.col("Year").cast(pl.Int32))

    # Convert numeric columns to efficient types, skipping WB_Income
    schema = df.schema
    float_cols = [col for col, typ in schema.items() if typ == pl.Float64 and col != "WB_Income"]
    for col in float_cols:
        df = df.with_columns(pl.col(col).cast(pl.Float32))
    # Handle WB_Income column
    df = df.with_columns(pl.col("WB_Income").fill_null("Unknown").cast(pl.Utf8))

    logger.info("Loaded data shape: %s", df.shape)
    return df


# Load data once at module level
data = load_data()

# Pre-calculate unique values for filters
UNIQUE_REGIONS = sorted(data["region"].drop_nulls().unique())
UNIQUE_INCOMES = sorted(data["WB_Income"].drop_nulls().unique())
UNIQUE_ENTITIES = sorted(data["Entity"].unique())
UNIQUE_AGES = sorted(data["age"].unique())
YEAR_RANGE = (int(data["Year"].min()), int(data["Year"].max()))
METRICS = sorted(data["cause"].unique())

# Pre-calculate region to countries mapping
REGION_COUNTRIES = {
    region: sorted(data.filter(pl.col("region") == region)["Entity"].unique())
    for region in UNIQUE_REGIONS
}


@cached(cache=TTLCache(maxsize=32, ttl=300), key=cache_key)
def filter_data(
    year=None, regions=None, income=None, gender="Both", metric=None, age=None, cause=None
):
    """Base filter function for filtering data based on various criteria."""
    filtered = data
    if year:
        filtered = data.filter(pl.col("Year") == year)
    if regions and regions != ["All"]:
        filtered = filtered.filter(pl.col("region").is_in(regions))
    if income and income != "All":
        filtered = filtered.filter(pl.col("WB_Income") == str(income))
    if age:
        filtered = filtered.filter(pl.col("age") == age)
    if cause:
        filtered = filtered.filter(pl.col("cause") == cause)

    if metric and gender:
        col = get_metric_column(gender, metric)
        if col:
            filtered = filtered.drop_nulls(subset=[col])
    logger.debug(msg=f'columns: {filtered.columns}')
    return filtered


data_2019 = filter_data(year=2019, age="Age-standardized", cause="Cardiovascular diseases")
print(data_2019.head())


@callback(
    Output("geo-eco-data", "data"),
    Input("year-slider", "value"),
    Input("region-dropdown", "value"),
    Input("income-dropdown", "value"),
    Input("gender-dropdown", "value"),
    Input("metric-dropdown", "value"),
    Input("top-filter-slider", "value"),
)
def get_geo_eco_data(year, regions, income, gender, metric, top_n):
    """Get filtered data for geo-economic visualizations."""
    print("Geo eco inputs:", year, regions, income, gender, metric, top_n)

    if not year or not gender or not metric:
        return []

    cols = [get_metric_column(g, metric) for g in ["Both", "Female", "Male"]]
    cols = [col for col in cols if col]

    df = filter_data(None, regions, income, gender, metric)
    print("Filtered data shape:", df.shape)
    print(f"Years in data: {sorted(df['Year'].unique())}")
    print(f"Available columns: {df.columns}")

    if cols:
        keep_cols = [
            "Entity",
            "Year",
            "Code",
            "gdp_pc",
            "WB_Income",
            "Population",
            "region",
            "cause",
        ] + cols
        df = df.select(keep_cols)
        df = df.with_columns(
            [pl.col(col).cast(pl.Float32) for col in cols + ["gdp_pc", "Population"]]
        )
        df = df.drop_nulls(subset=cols + ["gdp_pc", "Population"])
        print("Post dropna:", df.shape)
        print("Final data shape:", df.shape)
        print("Final columns:", df.columns)
        print(f"Sample data:\n{df[cols + ['gdp_pc', 'Year']].head()}")
    return df.to_dicts()


@callback(
    Output("world-map-data", "data"),
    Input("year-slider", "value"),
    Input("region-dropdown", "value"),
    Input("income-dropdown", "value"),
    Input("gender-dropdown", "value"),
    Input("metric-dropdown", "value"),
    Input("age-dropdown", "value"),
)
def get_world_map_data(year, regions, income, gender, metric, age):
    """Get filtered data for world map visualization."""
    if not year or not metric or not gender:
        return []

    df = filter_data(year, regions, income, gender, metric, age)
    col = get_metric_column(gender, metric)

    if col:
        df = df.select(["Entity", "Code", col, "region", "WB_Income", "cause"])
        df = df.filter(pl.col("cause").str.to_lowercase() == "cardiovascular diseases")

    return df.to_dicts()


@callback(
    Output("trends-data", "data"),
    Input("metric-dropdown", "value"),
    Input("gender-dropdown", "value"),
    Input("country-dropdown", "value"),
    Input("region-dropdown", "value"),
    Input("income-dropdown", "value"),
)
def get_trends_data(metric, gender, countries, regions, income):
    """Get filtered data for trends visualization."""
    if not metric or not gender:
        return []

    df = filter_data(None, regions, income, gender, metric)  # No year filter for trends

    # Filter by countries if specified
    if countries:
        df = df.filter(pl.col("Entity").is_in(countries))

    # Sum across ages for each year, entity, and cause
    df = df.group_by(["Year", "Entity", "cause", "region", "WB_Income"]).sum()
    logger.debug(f"Trend data shape: {df.shape}")

    return df.to_dicts()


@callback(
    Output("healthcare-data", "data"),
    Input("year-slider", "value"),
    Input("region-dropdown", "value"),
    Input("income-dropdown", "value"),
    Input("gender-dropdown", "value"),
    Input("metric-dropdown", "value"),
)
def get_healthcare_data(year, regions, income, gender, metric):
    """Get filtered data for healthcare system visualization."""
    if not year or not metric:
        return []

    df = filter_data(
        year, regions, income, gender=gender, metric=metric
    )  # Use Both to get all gender data
    df = df.filter(pl.col("cause").str.to_lowercase() == "cardiovascular diseases")
    df = df.filter(pl.col("age").str.contains("Age-standardized"))

    # Keep required columns
    required_cols = ["Entity", "Code", "region", "WB_Income", "Year", "cause"]
    optional_cols = ["ct_units", "obesity%", "pacemaker_1m", "statin_avail", "statin_use_k"]

    # Add all val* columns
    val_cols = [col for col in df.columns if col.startswith("val")]

    # Check which optional columns exist and combine with val columns
    available_cols = required_cols + val_cols + [c for c in optional_cols if c in df.columns]

    # Only keep rows where required columns are not null
    df = df.select(available_cols).drop_nulls(subset=required_cols)

    logger.debug(f"Healthcare data shape: {df.shape}")
    logger.debug(df.head())
    return df.to_dicts()


@callback(
    Output("sankey-data", "data"),
    Input("region-dropdown", "value"),
    Input("income-dropdown", "value"),
    Input("gender-dropdown", "value"),
    Input("metric-dropdown", "value"),
)
def get_sankey_data(regions, income, gender, metric):
    """Get unfiltered data for Sankey diagram visualization."""
    df = filter_data(year=2019, regions=regions, income=income, gender=gender, metric=metric, cause="Cardiovascular diseases", age="Age-standardized")
    col = get_metric_column(gender, metric)

    if col and col in df.columns:
        required_cols = ["Entity", "Code", "region", "WB_Income", "Year", "cause"]
        df = df.select(required_cols + [col]).drop_nulls(subset=required_cols + [col])
        logger.debug(f"Sankey data shape: {df.shape}")
        logger.debug(msg=df.head())
        return df.to_dicts()

    return []


@callback(
    Output("hpt-data", "data"),Input("_", "data"))
def get_hpt_data(_):
    """Get hypertension data."""
    df = data_2019
    # df = filter_data(year=2019)
    # df = df.with_columns(
    #     pl.col("t_htn_ctrl").cast(pl.Float64),
    #     pl.col("t_high_bp_30-79").cast(pl.Float64),
    # )
    logger.debug(f"HPT DataFrame columns: {df.columns.tolist()}")
    return df.to_dicts()
