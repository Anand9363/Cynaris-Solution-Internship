
# ============================================================
# WEEK 3 - DAY 4: LOOKER STUDIO
# Project: EDA on Indian Business Dataset
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")

# 1. LOAD DATASET
df = pd.read_csv( r"C:\Users\dkart\Downloads\archive\olist_order_items_dataset.csv"
)


print("\n========== DATASET INFORMATION ==========")

print("Dataset Shape:", df.shape)
print("\nFirst 5 Records:")
print(df.head())

# 2. DATA CLEANING
print("\n========== DATA CLEANING ==========")

print("Missing Values:")
print(df.isnull().sum())

df = df.drop_duplicates()

# Fill missing numerical values
for col in df.select_dtypes(include=np.number).columns:
    df[col] = df[col].fillna(df[col].median())

# Fill missing categorical values
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].fillna("Unknown")

print("\nCleaned Dataset Shape:", df.shape)

# 3. DESCRIPTIVE ANALYSIS
print("\n========== DESCRIPTIVE ANALYSIS ==========")

print(df.describe(include="all"))

# 4. NUMERICAL COLUMN ANALYSIS
numeric_cols = df.select_dtypes(include=np.number).columns

for col in numeric_cols:
    print(f"\n{col} Analysis:")
    print("Total:", df[col].sum())
    print("Average:", df[col].mean())
    print("Maximum:", df[col].max())
    print("Minimum:", df[col].min())

# 5. CATEGORICAL ANALYSIS
categorical_cols = df.select_dtypes(include="object").columns

for col in categorical_cols:
    print(f"\n{col} Distribution:")
    print(df[col].value_counts().head(10))

# 6. CORRELATION ANALYSIS
print("\n========== CORRELATION ==========")

correlation = df.select_dtypes(include=np.number).corr()

print(correlation)

plt.figure(figsize=(10, 6))
plt.imshow(correlation, cmap="coolwarm")
plt.colorbar()
plt.xticks(range(len(correlation.columns)),
           correlation.columns, rotation=45)
plt.yticks(range(len(correlation.columns)),
           correlation.columns)
plt.title("Business Dataset Correlation")
plt.tight_layout()
plt.savefig("correlation_day4.png")
plt.show()

# 7. EXPORT CLEANED DATASET
df.to_csv("cleaned_indian_business_dataset.csv",
          index=False)

print("\nCleaned dataset exported successfully!")

# 8. EXPORT SUMMARY FOR DASHBOARD
summary = pd.DataFrame({
    "Metric": [
        "Total Records",
        "Total Columns",
        "Duplicate Records Removed",
        "Missing Values Remaining"
    ],
    "Value": [
        len(df),
        len(df.columns),
        "Check original dataset",
        df.isnull().sum().sum()
    ]
})

summary.to_csv("business_summary_day4.csv", index=False)

print("\n========== DAY 4 COMPLETED ==========")
