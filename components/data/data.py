import pandas as pd

loaded_data = pd.read_csv("./data/heart_disease_data.csv")

# removing leading and trailing whitespaces from column names
loaded_data.columns = loaded_data.columns.str.strip()

# removing leading and trailing whitespaces from values in the dataframe
loaded_data = loaded_data.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# print(loaded_data.columns)


def region_selector():
    return loaded_data["region"].unique()


def country_selector(input):
    if input == "Africa":
        return loaded_data[loaded_data["region"] == "Africa"]["Entity"].unique()
    elif input == "Asia":
        return loaded_data[loaded_data["region"] == "Asia"]["Entity"].unique()
    elif input == "Europe":
        return loaded_data[loaded_data["region"] == "Europe"]["Entity"].unique()
    elif input == "North America":
        return loaded_data[loaded_data["region"] == "North America"]["Entity"].unique()
    elif input == "Oceania":
        return loaded_data[loaded_data["region"] == "Oceania"]["Entity"].unique()
    elif input == "South America":
        return loaded_data[loaded_data["region"] == "South America"]["Entity"].unique()
    else:
        return loaded_data["country"].unique()


region = region_selector()[1]
# print(region)

country = country_selector(region)


# print(country)
def world_imcome_level_selector():
    return loaded_data["WB_Income"].unique()


def metric_selector():
    columns_to_show = ["obesity%", "population", "cvd_share"]
    return loaded_data.columns[columns_to_show]


def gender_selector(gender):
    """
    Selects gender-specific columns based on user choice (Male 'M' or Female 'F').
    """
    gender_map = {
        "M": {
            "Prevalence": "m_prev",
            "Death Percent": "m_deaths%",
            "Death": "m_deaths",
            "Hypertension Prevalence": "m_htn_30-79",
        },
        "F": {
            "Prevalence": "f_prev",
            "Death Percent": "f_deaths%",
            "Death": "f_deaths",
            "Hypertension Prevalence": "f_htn_30-79",
        },
    }

    return gender_map.get(gender, {})


# Example Usage
selected_gender = "M"  # or "F"
columns = gender_selector(selected_gender)

# Print the selected columns
print(columns)


def metric_selector():
    columns_to_show = ["obesity%", "population", "cvd_share"]
    return loaded_data.columns[columns_to_show]
