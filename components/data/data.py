
#! usr/bin/env python3
import logging
import os

import pandas as pd
from dash import Input, Output, callback

logger = logging.getLogger(__name__)

data_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "heart_disease_data.csv"
)
data = pd.read_csv(data_path)
logger.info("Loaded data shape: %s", data.shape)


@callback(Output("general-data", "data"), Input("year-slider", "value"))
def year_filter(year: int):
    """Filter data by year."""
    logger.debug("Year filter called with: %s", year)
    #TODO: review unreachable
    if year is None:
        logger.debug("No year selected")
        return []
    df = data.copy()
    df = df[df["Year"] == year]
    logger.debug("Year filtered data shape: %s", df.shape)
    return df.to_dict("records")

@callback(
    Output('geo-eco-data', 'data'),
    Input('general-data', 'data'),
    # Input('metric-dropdown', 'value'),
    Input('gender-dropdown', 'value'),
    Input('region-dropdown', 'value'),
    Input('income-dropdown', 'value'),
    Input('top-filter-slider', 'value')
)
def geo_eco_data(data, gender, region, income, top_n):
    """_summary_

    Args:
        data (_type_): _description_
        gender (_type_): _description_
        region (_type_): _description_
        income (_type_): _description_
        top_n (_type_): _description_

    Returns:
        _type_: _description_
    """
    logger.debug("Geo eco data called with: %s, %s, %s, %s", gender, region, income, top_n)
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
    




@callback(
    Output("chloropleth_data", "data"),
    Input("general-data", "data"),
    Input("metric-dropdown", "value"),
    Input("gender-dropdown", "value"),
)
def chloropleth_data(year_filtered_data, metric, gender):
    """Get data for chloropleth map."""
    logger.debug("Chloropleth data called with: %s, %s", metric, gender)
    logger.debug(
        "Year filtered data: %s", len(year_filtered_data) if year_filtered_data else "None"
    )

    if not year_filtered_data or not metric or not gender:
        logger.debug("Missing required data")
        return []

    df = pd.DataFrame(year_filtered_data)
    logger.debug("Received data shape: %s", df.shape)

    needed = ["Entity", "Year", "Code"]
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
    logger.debug("Looking for column: %s", col)
    if col is not None and col in df.columns:
        df = df[needed + [col]].dropna(subset=[col])
        logger.debug("Final data shape: %s", df.shape)
        return df.to_dict("records")
    logger.warning("Column not found or invalid")
    return []
