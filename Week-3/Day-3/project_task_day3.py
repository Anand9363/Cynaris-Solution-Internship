
# ============================================================
# WEEK 3 - DAY 3: EXCEL FOR ANALYSIS
# Project: EDA on Indian Business Dataset
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

print("=" * 60)
print("W3D3 - EXCEL FOR ANALYSIS")
print("=" * 60)

# Load dataset using its absolute path
file_path = Path(
    r"C:\Users\dkart\Downloads\archive\olist_order_items_dataset.csv"
)

if not file_path.exists():
    raise FileNotFoundError("Dataset not found!")

df = pd.read_csv(file_path)

# Select the first CSV file


print("\nDataset Loaded:", file_path.name)

# 2. BASIC DATASET INFORMATION
print("\nDataset Shape:", df.shape)

print("\nFirst 5 Records:")
print(df.head())

print("\nColumn Names:")
print(df.columns.tolist())

print("\nDataset Information:")
df.info()

# 3. DATA QUALITY ANALYSIS
print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Records:", df.duplicated().sum())

# 4. DATA CLEANING
df.columns = df.columns.str.strip()

# Remove duplicate records
df = df.drop_duplicates()

# Handle missing values
for col in df.select_dtypes(include="number").columns:
    df[col] = df[col].fillna(df[col].median())

for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].fillna("Unknown")

print("\nData Cleaning Completed!")
print("Cleaned Dataset Shape:", df.shape)

# 5. NUMERICAL ANALYSIS
print("\nStatistical Summary:")
print(df.describe())

# 6. CATEGORICAL ANALYSIS
categorical_columns = df.select_dtypes(
    include="object"
).columns

for col in categorical_columns:
    print(f"\nTop 10 values in {col}:")
    print(df[col].value_counts().head(10))

# 7. NUMERICAL CORRELATION
numeric_df = df.select_dtypes(include="number")

if not numeric_df.empty:
    print("\nCorrelation Analysis:")
    print(numeric_df.corr())

    plt.figure(figsize=(10, 6))
    plt.imshow(numeric_df.corr(), cmap="coolwarm")
    plt.colorbar()
    plt.xticks(
        range(len(numeric_df.columns)),
        numeric_df.columns,
        rotation=45,
        ha="right"
    )
    plt.yticks(
        range(len(numeric_df.columns)),
        numeric_df.columns
    )
    plt.title("Business Dataset Correlation")
    plt.tight_layout()
    plt.savefig("correlation_day3.png")
    plt.show()

# 8. NUMERICAL DISTRIBUTION
for col in numeric_df.columns[:5]:
    plt.figure(figsize=(7, 4))
    plt.hist(df[col].dropna(), bins=20)
    plt.title(f"Distribution of {col}")
    plt.xlabel(col)
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(f"distribution_{col}.png")
    plt.show()

# 9. AUTOMATIC CATEGORY SUMMARY
# Useful for creating PivotTable-style summaries

for col in categorical_columns:
    summary = df.groupby(col).size().reset_index(
        name="Record_Count"
    )

    print(f"\nSummary by {col}:")
    print(summary.head(10))

# 10. EXPORT DATA FOR EXCEL
with pd.ExcelWriter(
    "analysis_workbook.xlsx",
    engine="openpyxl"
) as writer:

    df.to_excel(
        writer,
        sheet_name="Cleaned_Data",
        index=False
    )

    df.describe(include="all").to_excel(
        writer,
        sheet_name="Statistics"
    )

    if not numeric_df.empty:
        numeric_df.corr().to_excel(
            writer,
            sheet_name="Correlation"
        )

    for col in categorical_columns[:5]:
        summary = df.groupby(col).size().reset_index(
            name="Record_Count"
        )

        summary.to_excel(
            writer,
            sheet_name=f"Summary_{col[:20]}",
            index=False
        )

print("\nExcel Workbook Created Successfully!")
print("File: analysis_workbook.xlsx")

print("\n" + "=" * 60)
print("W3D3 ANALYSIS COMPLETED")
print("=" * 60)
