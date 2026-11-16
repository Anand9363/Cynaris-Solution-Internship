
# ============================================================
# WEEK 3 - DAY 1: POWER BI
# Project: EDA on Indian Business Dataset
# ============================================================

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")

print("=" * 60)
print("WEEK 3 - DAY 1: BUSINESS DATA ANALYSIS")
print("=" * 60)

print("Python Version:", sys.version)

# 1. Load Dataset
df = pd.read_csv(r"C:\Users\dkart\Downloads\archive\olist_order_items_dataset.csv"
)

print("\nDataset Loaded Successfully!")

# 2. Dataset Information
print("\nDataset Shape:", df.shape)

print("\nFirst 5 Records:")
print(df.head())

print("\nDataset Information:")
df.info()

# 3. Statistical Summary
print("\nStatistical Summary:")
print(df.describe(include="all"))

# 4. Missing Values
print("\nMissing Values:")
print(df.isnull().sum())

# 5. Duplicate Records
print("\nDuplicate Records:", df.duplicated().sum())

# 6. Data Types
print("\nColumn Data Types:")
print(df.dtypes)

# 7. Separate Numeric and Categorical Columns
numeric_columns = df.select_dtypes(include=np.number).columns
categorical_columns = df.select_dtypes(include="object").columns

print("\nNumeric Columns:", list(numeric_columns))
print("Categorical Columns:", list(categorical_columns))

# 8. Numeric Column Analysis
if len(numeric_columns) > 0:
    print("\nNumeric Column Averages:")
    print(df[numeric_columns].mean())

# 9. Categorical Column Analysis
for column in categorical_columns:
    print(f"\nTop 5 Values in {column}:")
    print(df[column].value_counts().head())

# 10. Visualizations

# Numeric Column Histograms
for column in numeric_columns[:4]:
    plt.figure(figsize=(7, 4))
    df[column].dropna().hist(bins=20)
    plt.title(f"Distribution of {column}")
    plt.xlabel(column)
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()

# Correlation Analysis
if len(numeric_columns) >= 2:
    correlation = df[numeric_columns].corr()

    print("\nCorrelation Matrix:")
    print(correlation)

    plt.figure(figsize=(8, 5))
    plt.imshow(correlation, cmap="coolwarm", aspect="auto")
    plt.colorbar()
    plt.xticks(range(len(correlation.columns)),
               correlation.columns, rotation=45)
    plt.yticks(range(len(correlation.columns)),
               correlation.columns)
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.show()

# 11. Final Summary
print("\n" + "=" * 60)
print("EDA COMPLETED SUCCESSFULLY")
print("=" * 60)

print("Total Rows:", df.shape[0])
print("Total Columns:", df.shape[1])
print("Missing Values:", df.isnull().sum().sum())
print("Duplicate Records:", df.duplicated().sum())

print("\nAnalysis Completed!")
