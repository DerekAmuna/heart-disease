"""Module for selecting gender-specific metrics and columns."""


def get_metric_column(gender: str, metric: str) -> str:
    """Get the appropriate column name based on gender and metric.

    Args:
        gender (str): Gender selection ('Female', 'Male', or 'Both')
        metric (str): Selected metric name

    Returns:
        str: Column name for the selected gender and metric
    """
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
    return metric_mapping.get(metric[0], {}).get(metric) if metric else None
