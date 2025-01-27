# Code Reference

## Main Functions

### `interpolate_series(group_data, column_name)`
Interpolates missing values in time series data using cubic spline interpolation.
- Requires at least 2 data points
- Falls back to linear interpolation if cubic spline fails
- Returns original values for valid data points

### `impute_extremes(group_data, column_name)`
Handles missing values at the start/end of time series.
- Uses mode for categorical variables
- Applies exponential weighted means for numeric data
- Combines forward/backward fills for robust imputation

## Data Processing Pipeline

1. **Initial Data Load**
   ```python
   merged_df = pd.read_excel("path/to/base/data.xlsx")
   for source_file in data_sources:
       temp_df = pd.read_excel/csv(source_file)
       merged_df = pd.merge(merged_df, temp_df, on=["Entity", "Code", "Year"], how="outer")
   ```

2. **Data Cleaning**
   ```python
   # Standardize country names
   ihme_data["location"] = ihme_data["location"].replace(name_mapping)
   
   # Process by entity
   for entity in result_df["Entity"].unique():
       entity_data = result_df[result_df["Entity"] == entity]
       for col in numeric_cols:
           result_df.loc[entity_data.index, col] = interpolate_series(entity_data, col)
   ```

3. **Final Processing**
   ```python
   # Merge population data
   result_df = result_df.merge(pop[["Entity", "Year", "Population"]], 
                              on=["Entity", "Year"], how="left")
   
   # Save processed data
   result_df.to_csv("../heart_disease_data.csv", index=False)
   ```
