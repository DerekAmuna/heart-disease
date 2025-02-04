#! usr/bin/env python3
import os
import pandas as pd
from dash import callback, Input, Output

data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "heart_disease_data.csv")
data = pd.read_csv(data_path)
print("Loaded data shape:", data.shape)

@callback(
    Output("general-data", "data"),
    Input("year-slider", "value"),
)
def year_filter(year:int):
    print("Year filter called with:", year)
    if year is None:
        print("No year selected")
        return []
    df = data.copy()
    df = df[df['Year'] == year]
    print("Year filtered data shape:", df.shape)
    return df.to_dict('records')

@callback(
    Output("chloropleth_data", "data"),
    Input("general-data", "data"),
    Input("metric-dropdown", "value"),
    Input("gender-dropdown", "value")
)
def chloropleth_data(year_filtered_data, metric, gender):
    print("Chloropleth data called with:", metric, gender)
    print("Year filtered data:", len(year_filtered_data) if year_filtered_data else "None")
    
    if not year_filtered_data or not metric or not gender:
        print("Missing required data")
        return []
        
    df = pd.DataFrame(year_filtered_data)
    print("Received data shape:", df.shape)
    
    needed = ['Entity', 'Year', 'Code']
    gender_prefix = 'f_' if gender == 'Female' else 'm_' if gender == 'Male' else ''
    metric_mapping = {
        'P': {
            'Prevalence Percent': f'{gender_prefix}prev%',
            'Prevalence Rate': f'{gender_prefix}prev_rate',
            'Prevalence': f'{gender_prefix}prev'
        },
        'D': {
            'Death Percent': f'{gender_prefix}deaths%',
            'Death Rate': f'{gender_prefix}death_rate',
            'Death': f'{gender_prefix}deaths'
        }
    }

    col = metric_mapping.get(metric[0], {}).get(metric)
    print("Looking for column:", col)
    if col is not None and col in df.columns:
        df = df[needed + [col]].dropna(subset=[col])
        print("Final data shape:", df.shape)
        return df.to_dict('records')
    print("Column not found or invalid")
    return []
