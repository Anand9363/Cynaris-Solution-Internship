
# Week 2, Day 2 — Pandas Advanced
# Project: EDA on Indian Business Dataset

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')

# 1. Load Dataset
df = pd.read_csv(
    r"C:\Users\dkart\Downloads\archive\olist_order_items_dataset.csv"
)

print("Original Dataset Shape:", df.shape)
print(df.head())

# 2. Create Two DataFrames for Merge
orders = df[['order_id', 'product_id', 'seller_id', 'price']].copy()

products = df[['product_id', 'freight_value']].drop_duplicates(
    subset='product_id'
).copy()

# 3. Merge Operations

# Inner Join
inner_merge = pd.merge(orders, products, on='product_id', how='inner')
print("\nInner Join:", inner_merge.shape)

# Left Join
left_merge = pd.merge(orders, products, on='product_id', how='left')
print("Left Join:", left_merge.shape)

# Right Join
right_merge = pd.merge(orders, products, on='product_id', how='right')
print("Right Join:", right_merge.shape)

# Outer Join
outer_merge = pd.merge(orders, products, on='product_id', how='outer')
print("Outer Join:", outer_merge.shape)

# 4. Pivot Table
pivot_table = pd.pivot_table(
    df,
    values='price',
    index='seller_id',
    columns='order_item_id',
    aggfunc='sum',
    fill_value=0
)

print("\nSales Pivot Table:")
print(pivot_table.head())

# 5. Melt — Wide to Long Format
sales_wide = pd.DataFrame({
    'Seller': ['Seller A', 'Seller B', 'Seller C'],
    'January': [10000, 15000, 12000],
    'February': [12000, 18000, 14000],
    'March': [14000, 20000, 16000]
})

sales_long = pd.melt(
    sales_wide,
    id_vars=['Seller'],
    var_name='Month',
    value_name='Sales'
)

print("\nMelted Data:")
print(sales_long)

# 6. Method Chaining
seller_analysis = (
    df.assign(total_value=df['price'] + df['freight_value'])
      .groupby('seller_id')
      .agg(
          total_sales=('price', 'sum'),
          total_freight=('freight_value', 'sum'),
          total_orders=('order_id', 'nunique'),
          average_price=('price', 'mean'),
          total_value=('total_value', 'sum')
      )
      .reset_index()
      .sort_values(by='total_sales', ascending=False)
)

print("\nTop 10 Sellers:")
print(seller_analysis.head(10))

# 7. Save Analysis Results
seller_analysis.to_csv('seller_analysis_day2.csv', index=False)
sales_long.to_csv('sales_melted_day2.csv', index=False)

print("\nAnalysis completed successfully!")
