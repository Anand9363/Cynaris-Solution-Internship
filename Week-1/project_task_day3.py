
# ============================================================
# Week 1, Day 3 — SQL Aggregations: GROUP BY & HAVING
# Project: EDA on Indian Business Dataset
# Dataset: E-Commerce Order Items
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')


# ============================================================
# 1. LOAD DATASET
# ============================================================

df = pd.read_csv(r"C:\Users\dkart\Downloads\archive\olist_order_items_dataset.csv")

print("\n========== FIRST 5 RECORDS ==========")
print(df.head())


# ============================================================
# 2. DATASET INFORMATION
# ============================================================

print("\n========== DATASET INFORMATION ==========")
df.info()

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

print("\n========== COLUMN NAMES ==========")
print(df.columns.tolist())


# ============================================================
# 3. DATA CLEANING AND PREPARATION
# ============================================================

# Convert shipping date into datetime format
df['shipping_limit_date'] = pd.to_datetime(
    df['shipping_limit_date'],
    errors='coerce'
)

# Check duplicate records
print("\n========== DUPLICATE RECORDS ==========")
print(df.duplicated().sum())

# Check missing values again
print("\n========== MISSING VALUES AFTER DATE CONVERSION ==========")
print(df.isnull().sum())


# ============================================================
# 4. AGGREGATE FUNCTIONS
# COUNT, SUM, AVG, MAX, MIN
# ============================================================

print("\n========== AGGREGATE FUNCTIONS ==========")

# COUNT
print("\nTotal Order Items:")
print(df['order_item_id'].count())

# SUM
print("\nTotal Product Sales:")
print(df['price'].sum())

# AVG
print("\nAverage Product Price:")
print(df['price'].mean())

# MAX
print("\nHighest Product Price:")
print(df['price'].max())

# MIN
print("\nLowest Product Price:")
print(df['price'].min())

# Total Freight
print("\nTotal Freight Value:")
print(df['freight_value'].sum())


# ============================================================
# 5. GROUP BY SELLER
# ============================================================

seller_sales = df.groupby('seller_id').agg(
    total_sales=('price', 'sum'),
    average_price=('price', 'mean'),
    total_items=('order_item_id', 'count'),
    total_freight=('freight_value', 'sum')
).reset_index()

print("\n========== SALES BY SELLER ==========")
print(seller_sales.head(10))


# ============================================================
# 6. GROUP BY PRODUCT
# ============================================================

product_sales = df.groupby('product_id').agg(
    total_revenue=('price', 'sum'),
    average_price=('price', 'mean'),
    total_items=('order_item_id', 'count')
).reset_index()

print("\n========== SALES BY PRODUCT ==========")
print(product_sales.head(10))


# ============================================================
# 7. GROUP BY SELLER AND PRODUCT
# ============================================================

seller_product_sales = df.groupby(
    ['seller_id', 'product_id']
).agg(
    total_sales=('price', 'sum'),
    total_items=('order_item_id', 'count')
).reset_index()

print("\n========== SELLER AND PRODUCT SALES ==========")
print(seller_product_sales.head(10))


# ============================================================
# 8. GROUP BY MONTH
# ============================================================

df['Month'] = df['shipping_limit_date'].dt.to_period('M')

monthly_sales = df.groupby('Month').agg(
    total_sales=('price', 'sum'),
    average_price=('price', 'mean'),
    total_items=('order_item_id', 'count')
).reset_index()

print("\n========== MONTHLY SALES ==========")
print(monthly_sales)


# ============================================================
# 9. HAVING EQUIVALENT
# Find sellers with total sales above 50,000
# ============================================================

high_performing_sellers = seller_sales[
    seller_sales['total_sales'] > 50000
]

print("\n========== HIGH PERFORMING SELLERS ==========")
print(high_performing_sellers)


# ============================================================
# 10. HAVING EQUIVALENT FOR PRODUCTS
# ============================================================

high_sales_products = product_sales[
    product_sales['total_revenue'] > 50000
]

print("\n========== HIGH SALES PRODUCTS ==========")
print(high_sales_products.head(10))


# ============================================================
# 11. WINDOW FUNCTION EQUIVALENT
# SUM() OVER (PARTITION BY seller_id)
# ============================================================

df['seller_total_sales'] = (
    df.groupby('seller_id')['price'].transform('sum')
)

print("\n========== WINDOW FUNCTION ==========")

print(
    df[['order_id', 'seller_id', 'price',
        'seller_total_sales']].head(10)
)


# ============================================================
# 12. BUSINESS KPI SUMMARY
# ============================================================

print("\n========== BUSINESS KPI SUMMARY ==========")

print("Total Order Items:", df['order_item_id'].count())

print("Unique Orders:", df['order_id'].nunique())

print("Unique Sellers:", df['seller_id'].nunique())

print("Unique Products:", df['product_id'].nunique())

print("Total Product Sales:", df['price'].sum())

print("Average Product Price:", df['price'].mean())

print("Total Freight:", df['freight_value'].sum())

print("Highest Product Price:", df['price'].max())

print("Lowest Product Price:", df['price'].min())


# ============================================================
# 13. VISUALIZATION
# Top 10 Sellers by Sales
# ============================================================

top_sellers = seller_sales.sort_values(
    by='total_sales',
    ascending=False
).head(10)

plt.figure(figsize=(10, 5))

plt.bar(
    top_sellers['seller_id'],
    top_sellers['total_sales']
)

plt.title('Top 10 Sellers by Total Sales')
plt.xlabel('Seller ID')
plt.ylabel('Total Sales')
plt.xticks(rotation=45, ha='right')

plt.tight_layout()
plt.show()


# ============================================================
# 14. MONTHLY SALES VISUALIZATION
# ============================================================

plt.figure(figsize=(12, 5))

plt.plot(
    monthly_sales['Month'].astype(str),
    monthly_sales['total_sales'],
    marker='o'
)

plt.title('Monthly Product Sales')
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


# ============================================================
# 15. FINAL MESSAGE
# ============================================================

print("\n==========================================")
print("DAY 3 EDA ANALYSIS COMPLETED SUCCESSFULLY")
print("==========================================")
