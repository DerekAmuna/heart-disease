# Heart Disease Data Processing Documentation

This documentation covers the data processing pipeline for cardiovascular disease datasets.

## Overview

The pipeline processes and merges multiple cardiovascular disease datasets from various sources, including:
- WHO mortality data
- IHME Global Burden of Disease data
- World Bank economic indicators
- Regional health statistics

## Data Processing Steps

1. **Data Loading**
   - Loads base dataset from cardiovascular death rate vs GDP per capita
   - Merges additional datasets from Our World in Data
   - Incorporates IHME GBD data

2. **Data Cleaning**
   - Standardizes country names using a mapping dictionary
   - Handles missing values through interpolation and imputation
   - Normalizes column names for consistency

3. **Data Transformation**
   - Pivots data for deaths and prevalence by gender
   - Creates standardized metrics for death rates and prevalence
   - Combines regional and global statistics

4. **Output**
   - Produces a comprehensive CSV file with merged data
   - Includes population data for normalization
   - Maintains consistent column naming for easy analysis

## Running the Pipeline

```bash
python3 cleaning_and_merging.py
```

The script will process all data sources and output a file named `heart_disease_data.csv` in the parent directory.

## Data Dictionary

Key columns in the output dataset:

- `Entity`: Country or region name
- `Year`: Data year
- `deaths_total`: Total deaths from cardiovascular diseases
- `deaths_female/male`: Gender-specific death counts
- `prev_total`: Total disease prevalence
- `prev_female/male`: Gender-specific prevalence
- Additional metrics for death rates, risk factors, and healthcare indicators
