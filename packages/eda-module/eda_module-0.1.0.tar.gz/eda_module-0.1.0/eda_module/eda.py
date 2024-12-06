# eda_module.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import skew, kurtosis
import warnings

warnings.filterwarnings("ignore")

def load_data(file_path):
    """
    Load a dataset from a CSV file.
    """
    return pd.read_csv(file_path)

def data_overview(df):
    """
    Print basic details about the dataset.
    """
    print("\nDataset Info:\n")
    print(df.info())
    print("\nShape of the dataset:", df.shape)
    print("\nDataset Summary:\n")
    print(df.describe(include="all").T)

def check_missing_values(df):
    """
    Check for missing values in the dataset.
    """
    missing_values = df.isnull().sum().sort_values(ascending=False)
    missing_percent = (df.isnull().sum() / len(df) * 100).sort_values(ascending=False)
    missing_df = pd.DataFrame({"Missing Count": missing_values, "Percentage (%)": missing_percent})
    print("\nMissing Values:\n")
    print(missing_df[missing_df["Missing Count"] > 0])

def data_types_and_uniques(df):
    """
    Check data types and number of unique values.
    """
    print("\nData Types and Unique Values:\n")
    for col in df.columns:
        print(f"{col}: Type = {df[col].dtype}, Unique Values = {df[col].nunique()}")

def handle_duplicates(df):
    """
    Drop duplicate rows and display the number of duplicates.
    """
    print(f"\nNumber of duplicate rows: {df.duplicated().sum()}")
    df.drop_duplicates(inplace=True)

def univariate_analysis(df):
    """
    Perform univariate analysis on the dataset.
    """
    print("\nUnivariate Analysis:\n")
    for col in df.select_dtypes(include=["int64", "float64"]).columns:
        print(f"\n{col}:")
        print(f"Mean = {df[col].mean():.2f}, Median = {df[col].median():.2f}, Skewness = {skew(df[col]):.2f}, Kurtosis = {kurtosis(df[col]):.2f}")
        sns.histplot(df[col], kde=True, bins=30)
        plt.title(f"Distribution of {col}")
        plt.show()

def visualize_categorical(df):
    """
    Visualize categorical variables using bar plots.
    """
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns
    for col in categorical_cols:
        plt.figure(figsize=(8, 4))
        sns.countplot(data=df, x=col, order=df[col].value_counts().index)
        plt.title(f"Count Plot of {col}")
        plt.xticks(rotation=45)
        plt.show()

def bivariate_analysis(df, target_column):
    """
    Perform bivariate analysis between features and a target variable.
    """
    print("\nBivariate Analysis:\n")
    for col in df.columns:
        if col != target_column and df[col].dtype in ["int64", "float64"]:
            sns.scatterplot(data=df, x=col, y=target_column)
            plt.title(f"{col} vs {target_column}")
            plt.show()

def correlation_heatmap(df):
    """
    Plot a heatmap of the correlations.
    """
    plt.figure(figsize=(12, 8))
    corr_matrix = df.corr()
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm")
    plt.title("Correlation Heatmap")
    plt.show()

def detect_outliers(df, num_cols):
    """
    Detect and visualize outliers using boxplots.
    """
    print("\nOutlier Detection:\n")
    for col in num_cols:
        plt.figure(figsize=(8, 4))
        sns.boxplot(x=df[col])
        plt.title(f"Boxplot of {col}")
        plt.show()