# Week 1, Day 5 — Python for Data: Pandas Basics
# Project: EDA on Business Dataset

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')

# 1. Load dataset
df = pd.read_csv(
    r"C:\Users\dkart\Downloads\archive\olist_order_items_dataset.csv"
)

# 2. Basic inspection
print("Dataset Shape:", df.shape)

print("\nFirst 5 Rows:")
print(df.head())

print("\nDataset Information:")
df.info()

print("\nStatistical Summary:")
print(df.describe())

# 3. Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# 4. Check duplicates
print("\nDuplicate Rows:", df.duplicated().sum())

# 5. Select columns
print("\nSelected Columns:")
print(df[['order_id', 'product_id', 'price', 'freight_value']].head())

# 6. Filter rows
high_price = df[df['price'] > 100]

print("\nProducts Above 100:")
print(high_price.head())

# 7. Value counts
print("\nTop 10 Sellers:")
print(df['seller_id'].value_counts().head(10))

# 8. GroupBy and aggregation
seller_analysis = df.groupby('seller_id').agg(
    total_orders=('order_id', 'nunique'),
    total_sales=('price', 'sum'),
    average_price=('price', 'mean'),
    total_freight=('freight_value', 'sum')
).reset_index()

print("\nSeller Analysis:")
print(seller_analysis.head(10))

# 9. Handle missing values
df_cleaned = df.drop_duplicates().copy()

print("\nCleaned Dataset Shape:", df_cleaned.shape)

# 10. Export cleaned data
df_cleaned.to_csv('cleaned_business_dataset.csv', index=False)

print("\nCleaned dataset exported successfully!")

df['shipping_limit_date'] = pd.to_datetime(
    df['shipping_limit_date'],
    errors='coerce'
)

print(df.dtypes)


seller_analysis = seller_analysis.sort_values(
    by='total_sales',
    ascending=False
)

print(seller_analysis.head(10))

top_sellers_orders = seller_analysis.sort_values(
    by='total_orders',
    ascending=False
)

print(top_sellers_orders.head(5))