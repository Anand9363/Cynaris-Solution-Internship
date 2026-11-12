
# Week 2, Day 4 — Data Cleaning
# Project: EDA on Indian Business Dataset

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
import sys

warnings.filterwarnings('ignore')

print(f"Python {sys.version}")

# 1. Load Dataset
df = pd.read_csv(
    r"C:\Users\dkart\Downloads\archive\olist_order_items_dataset.csv"
)

print("\nOriginal Dataset Shape:", df.shape)
print("\nFirst 5 Records:")
print(df.head())

# 2. Check Missing Values
print("\nMissing Values:")
print(df.isnull().sum())

# 3. Check Duplicate Records
print("\nDuplicate Records:", df.duplicated().sum())

# 4. Remove Duplicates
df = df.drop_duplicates()

# 5. Handle Missing Values
numeric_cols = df.select_dtypes(include=np.number).columns

for col in numeric_cols:
    df[col] = df[col].fillna(df[col].median())

# 6. Convert Date Column
df['shipping_limit_date'] = pd.to_datetime(
    df['shipping_limit_date'], errors='coerce'
)

# 7. Standardise String Values
string_cols = df.select_dtypes(include='object').columns

for col in string_cols:
    df[col] = df[col].str.strip()

# 8. Detect Outliers Using IQR
print("\nOutlier Detection:")

for col in ['price', 'freight_value']:

    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)

    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = df[
        (df[col] < lower) | (df[col] > upper)
    ]

    print(f"{col} Outliers:", len(outliers))

# 9. Check Data Quality After Cleaning
print("\nMissing Values After Cleaning:")
print(df.isnull().sum())

print("\nDuplicates After Cleaning:", df.duplicated().sum())

# 10. Save Cleaned Dataset
df.to_csv("cleaned_dataset.csv", index=False)

print("\nFinal Dataset Shape:", df.shape)
print("\nData Cleaning Completed Successfully!")
