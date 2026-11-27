
# Week 4 - Day 5: Data Analysis Capstone
# Project: EDA on Indian Business Dataset

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
import os

warnings.filterwarnings("ignore")

# Create output folders
os.makedirs("outputs/charts", exist_ok=True)

# 1. Load dataset
df = pd.read_csv(r"C:\Users\dkart\Downloads\archive\olist_order_items_dataset.csv")

print("DATASET OVERVIEW")
print("=" * 50)
print("Shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())

# 2. Data understanding
print("\nDataset Information:")
df.info()

print("\nColumn Names:")
print(df.columns.tolist())

print("\nData Types:")
print(df.dtypes)

# 3. Data cleaning
print("\nMissing Values Before Cleaning:")
print(df.isnull().sum())

print("\nDuplicate Rows:", df.duplicated().sum())

# Remove duplicates
df = df.drop_duplicates()

# Save missing value report
missing_report = df.isnull().sum().to_frame("missing_values")
missing_report["missing_percentage"] = (
    missing_report["missing_values"] / len(df) * 100
)
missing_report.to_csv("outputs/missing_values.csv")

# Fill numeric missing values using median
numeric_cols = df.select_dtypes(include=np.number).columns

for col in numeric_cols:
    df[col] = df[col].fillna(df[col].median())

# Fill categorical missing values using mode
categorical_cols = df.select_dtypes(include="object").columns

for col in categorical_cols:
    if df[col].isnull().any() and not df[col].mode().empty:
        df[col] = df[col].fillna(df[col].mode()[0])

print("\nShape After Cleaning:", df.shape)
print("Remaining Missing Values:", df.isnull().sum().sum())

# 4. Descriptive statistics
summary = df.describe(include="all")
print("\nDescriptive Statistics:")
print(summary)

summary.to_csv("outputs/descriptive_statistics.csv")

# 5. Numerical analysis
numeric_cols = df.select_dtypes(include=np.number).columns

if len(numeric_cols) > 0:
    print("\nNumerical Column Analysis:")
    print(df[numeric_cols].mean())

    # Histograms
    for col in numeric_cols[:5]:
        plt.figure(figsize=(8, 5))
        df[col].hist(bins=30)
        plt.title(f"Distribution of {col}")
        plt.xlabel(col)
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.savefig(f"outputs/charts/{col}_distribution.png")
        plt.show()

# 6. Categorical analysis
categorical_cols = df.select_dtypes(
    include=["object", "category"]
).columns

for col in categorical_cols[:5]:
    print(f"\nTop Categories in {col}:")
    print(df[col].value_counts().head(10))

# 7. Correlation analysis
if len(numeric_cols) >= 2:
    correlation = df[numeric_cols].corr()
    print("\nCorrelation Matrix:")
    print(correlation)

    correlation.to_csv("outputs/correlation_matrix.csv")

    plt.figure(figsize=(10, 6))
    plt.imshow(correlation, cmap="coolwarm", aspect="auto")
    plt.colorbar()
    plt.xticks(range(len(correlation.columns)),
               correlation.columns, rotation=90)
    plt.yticks(range(len(correlation.columns)),
               correlation.columns)
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig("outputs/charts/correlation_heatmap.png")
    plt.show()

# 8. Final cleaned dataset
df.to_csv("outputs/cleaned_dataset.csv", index=False)

print("\nCapstone EDA Completed Successfully!")
