# Week 2, Day 3 — EDA Workflow
# Project: EDA on Indian Business Dataset

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')

# -----------------------------------------
# 1. Load Dataset
# -----------------------------------------

df = pd.read_csv(
    r"C:\Users\dkart\Downloads\archive\olist_order_items_dataset.csv"
)

print("Dataset loaded successfully!")
print("Dataset Shape:", df.shape)

print("\nFirst 5 Records:")
print(df.head())

# -----------------------------------------
# 2. Dataset Profiling
# -----------------------------------------

print("\nDataset Information:")
df.info()

print("\nColumn Names:")
print(df.columns.tolist())

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Records:")
print(df.duplicated().sum())

# -----------------------------------------
# 3. Data Cleaning
# -----------------------------------------

df['shipping_limit_date'] = pd.to_datetime(
    df['shipping_limit_date'],
    errors='coerce'
)

print("\nData Types After Conversion:")
print(df.dtypes)

# -----------------------------------------
# 4. Summary Statistics
# -----------------------------------------

summary = df.describe().T

summary['median'] = df.median(numeric_only=True)
summary['missing_values'] = df.isnull().sum()

print("\nSummary Statistics:")
print(summary)

summary.to_csv("eda_summary_statistics.csv")

# -----------------------------------------
# 5. Numeric Column Distributions
# -----------------------------------------

numeric_cols = df.select_dtypes(include=np.number).columns

for col in numeric_cols:
    plt.figure(figsize=(8, 4))

    plt.hist(df[col].dropna(), bins=30, edgecolor='black')

    plt.title(f"Distribution of {col}")
    plt.xlabel(col)
    plt.ylabel("Frequency")

    plt.tight_layout()
    plt.show()

# -----------------------------------------
# 6. Correlation Heatmap
# -----------------------------------------

correlation = df[numeric_cols].corr()

plt.figure(figsize=(8, 5))

plt.imshow(correlation, cmap='coolwarm', aspect='auto',
           vmin=-1, vmax=1)

plt.colorbar(label="Correlation")

plt.xticks(range(len(numeric_cols)), numeric_cols, rotation=45)
plt.yticks(range(len(numeric_cols)), numeric_cols)

for i in range(len(numeric_cols)):
    for j in range(len(numeric_cols)):
        plt.text(j, i, f"{correlation.iloc[i, j]:.2f}",
                 ha='center', va='center')

plt.title("Correlation Heatmap")
plt.tight_layout()
plt.show()

# -----------------------------------------
# 7. Outlier Detection Using IQR
# -----------------------------------------

for col in numeric_cols:

    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)

    IQR = Q3 - Q1

    lower_limit = Q1 - 1.5 * IQR
    upper_limit = Q3 + 1.5 * IQR

    outliers = df[
        (df[col] < lower_limit) |
        (df[col] > upper_limit)
    ]

    print(f"\n{col}")
    print("Lower Limit:", lower_limit)
    print("Upper Limit:", upper_limit)
    print("Outlier Count:", len(outliers))

# -----------------------------------------
# 8. Business Insights
# -----------------------------------------

# Insight 1: Total Sales Value

total_sales = df['price'].sum()

print("\n1. Total Sales Value:", round(total_sales, 2))

plt.figure(figsize=(6, 4))
plt.bar(['Total Sales'], [total_sales])
plt.title("Total Sales Value")
plt.ylabel("Sales Value")
plt.show()

# Insight 2: Top 5 Sellers

top_sellers = (
    df.groupby('seller_id')['price']
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

print("\n2. Top 5 Sellers:")
print(top_sellers)

top_sellers.plot(kind='bar', figsize=(9, 4))

plt.title("Top 5 Sellers by Sales Value")
plt.xlabel("Seller ID")
plt.ylabel("Sales Value")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Insight 3: Average Product Price

average_price = df['price'].mean()

print("\n3. Average Product Price:", round(average_price, 2))

plt.figure(figsize=(7, 4))
plt.hist(df['price'], bins=30, edgecolor='black')
plt.axvline(average_price, linestyle='--',
            label='Average Price')

plt.title("Product Price Distribution")
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.legend()
plt.show()

# Insight 4: Freight Cost Analysis

total_freight = df['freight_value'].sum()
average_freight = df['freight_value'].mean()

print("\n4. Total Freight:", round(total_freight, 2))
print("Average Freight:", round(average_freight, 2))

plt.figure(figsize=(7, 4))
plt.scatter(
    df['price'],
    df['freight_value'],
    alpha=0.3
)

plt.title("Product Price vs Freight Value")
plt.xlabel("Product Price")
plt.ylabel("Freight Value")
plt.show()

# Insight 5: Order Analysis

order_analysis = (
    df.groupby('order_id')
    .agg(
        total_items=('order_item_id', 'count'),
        order_value=('price', 'sum')
    )
)

print("\n5. Order Analysis:")
print(order_analysis.describe())

plt.figure(figsize=(8, 4))
plt.hist(order_analysis['total_items'], bins=30,
         edgecolor='black')

plt.title("Items per Order Distribution")
plt.xlabel("Number of Items")
plt.ylabel("Number of Orders")
plt.show()

# -----------------------------------------
# 9. Final EDA Report
# -----------------------------------------

print("\n========== FINAL EDA REPORT ==========")

print("Total Records:", len(df))
print("Total Columns:", len(df.columns))
print("Total Orders:", df['order_id'].nunique())
print("Total Sellers:", df['seller_id'].nunique())
print("Total Products:", df['product_id'].nunique())
print("Missing Values:", df.isnull().sum().sum())
print("Duplicate Records:", df.duplicated().sum())
print("Total Sales Value:", round(total_sales, 2))
print("Average Product Price:", round(average_price, 2))
print("Total Freight:", round(total_freight, 2))

print("\nEDA Workflow Completed Successfully!")