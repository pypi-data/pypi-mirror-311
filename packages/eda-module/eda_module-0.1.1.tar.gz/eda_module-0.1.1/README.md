# EDA Module

A reusable module for performing exploratory data analysis (EDA) in Python.

## Features
- Load and describe datasets.
- Check for missing values and duplicates.
- Perform univariate and bivariate analysis.
- Visualize correlations and outliers.

## Installation
```bash
pip install eda_module

## Usage

import eda_module as eda

df = eda.load_data("path/to/dataset.csv")
eda.data_overview(df)
eda.check_missing_values(df)
