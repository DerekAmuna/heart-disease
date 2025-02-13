#! usr/bin/env python3
import logging
import os
from functools import lru_cache

import pandas as pd
from dash import Input, Output, callback

from components.common.gender_metric_selector import get_metric_column

logger = logging.getLogger(__name__)


@lru_cache(maxsize=128)
def load_data():
    """Load data with caching."""
    logger.debug("Cache info for load_data: %s", (load_data.cache_info()))
    data_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "data",
        "heart_processed.csv",
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
data = load_data()

# Pre-calculate unique values for filters
UNIQUE_REGIONS = sorted(data["region"].dropna().unique())
UNIQUE_INCOMES = sorted(data["WB_Income"].dropna().unique())
UNIQUE_ENTITIES = sorted(data["Entity"].unique())
UNIQUE_AGES = sorted(data["age"].unique())
YEAR_RANGE = (int(data["Year"].min()), int(data["Year"].max()))
METRICS = sorted(data["cause"].unique())

# Pre-calculate region to countries mapping
REGION_COUNTRIES = {
    region: sorted(data[data["region"] == region]["Entity"].unique()) for region in UNIQUE_REGIONS
}


@lru_cache(maxsize=32)
def filter_data(year=None, regions=None, income=None, gender="Both", metric=None, age=None):
    """Base filter function with caching for common filter combinations."""
    filtered = pd.DataFrame(data)

    if year:
        filtered = filtered[filtered["Year"] == year]
    if regions and regions != ["All"]:
        filtered = filtered[filtered["region"].isin(regions)]
    if income and income != "All":
        filtered = filtered[filtered["WB_Income"] == str(income)]
    if age:
        filtered = filtered[filtered["age"] == age]

    if metric and gender:
        col = get_metric_column(gender, metric)
        if col:
            filtered = filtered.dropna(subset=[col])

    return filtered


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

    # Get all gender columns for the metric
    cols = []
    for g in ["Both", "Female", "Male"]:
        col = get_metric_column(g, metric)
        if col:
            cols.append(col)

    df = filter_data(None, regions, income, gender, metric)
    print("Filtered data shape:", df.shape)
    print(f"Years in data: {sorted(df['Year'].unique())}")
    print(f"Available columns: {df.columns.tolist()}")

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
        df = df[keep_cols]
        # Convert numeric columns
        for num_col in cols + ["gdp_pc", "Population"]:
            df[num_col] = pd.to_numeric(df[num_col], errors="coerce")
        print("Pre dropna:", df.shape)
        df = df.dropna(subset=cols + ["gdp_pc", "Population"])
        print("Post dropna:", df.shape)
        print("Final data shape:", df.shape)
        print("Final columns:", df.columns.tolist())
        print(f"Sample data:\n{df[cols + ['gdp_pc', 'Year']].head()}")

    return df.to_dict("records")


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
        df = df[["Entity", "Code", col, "region", "WB_Income", "cause"]]
        df = df[df["cause"].str.lower() == "cardiovascular diseases"]

    return df.to_dict("records")


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

    df = filter_data(None, regions, income, gender, metric) # No year filter for trends

    # Filter by countries if specified
    if countries:
        df = df[df["Entity"].isin(countries)]

    # Sum across ages for each year, entity, and cause
    df = df.groupby(["Year", "Entity", "cause", "region", "WB_Income"]).sum().reset_index()
    logger.debug(f"Trend data shape: {df.shape}")

    return df.to_dict("records")


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
        year, regions, income, gender="Both", metric=metric
    )  # Use Both to get all gender data
    df = df[df["cause"].str.lower() == "cardiovascular diseases"]
    df = df[df["age"].str.contains("Age-standardized", case=False, na=False)]

    # Keep required columns
    required_cols = ["Entity", "Code", "region", "WB_Income", "Year", "cause"]
    optional_cols = ["ct_units", "obesity%", "pacemaker_1m", "statin_avail", "statin_use_k"]

    # Add all val* columns
    val_cols = [col for col in df.columns if col.startswith("val")]

    # Check which optional columns exist and combine with val columns
    available_cols = required_cols + val_cols + [c for c in optional_cols if c in df.columns]

    # Only keep rows where required columns are not null
    df = df[available_cols].dropna(subset=required_cols)

    logger.debug(f"Healthcare data shape: {df.shape}")
    logger.debug(df.head())
    return df.to_dict("records")


def get_sankey_data(regions, income, gender, metric):
    """Get unfiltered data for Sankey diagram visualization."""
    df = filter_data(regions=regions, income=income, gender=gender, metric=metric)
    col = get_metric_column(gender, metric)

    if col and col in df.columns:
        df = df[df["age"].str.contains("Age-standardized", case=False, na=False)]
        required_cols = ["Entity", "Code", "region", "WB_Income", "Year", "cause"]
        df = df[required_cols + [col]].dropna(subset=required_cols + [col])
        df = df[df["cause"].str.lower() == "cardiovascular diseases"]
        logger.debug(f"Sankey data shape: {df.shape}")
        return df.to_dict("records")

    return []


def get_hpt_data():
    df = (
        data[data["Year"] == 2019]
        .dropna(subset=["t_htn_ctrl", "t_high_bp_30-79"])
        .drop_duplicates(subset=["Entity", "Year", "t_htn_ctrl", "t_high_bp_30-79"])
    )

    logger.debug(msg=df.head())
    return df
