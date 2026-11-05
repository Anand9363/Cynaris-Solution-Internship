
# Week 1, Day 4 — SQL Subqueries & CTEs
# Project: EDA on Indian Business Dataset

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
import sqlite3

warnings.filterwarnings('ignore')

# 1. Load dataset
df = pd.read_csv(r"C:\Users\dkart\Downloads\archive\olist_order_items_dataset.csv")


# 2. Basic EDA
print("Dataset Shape:", df.shape)
print("\nFirst 5 Rows:")
print(df.head())

print("\nColumn Names:")
print(df.columns.tolist())

print("\nMissing Values:")
print(df.isnull().sum())

# 3. Connect Python with SQLite
conn = sqlite3.connect(':memory:')

# Load dataframe as SQL table
df.to_sql('business', conn, index=False, if_exists='replace')

# 4. SQL Query: Check total records
query_task1 = """
SELECT product_id, price
FROM business
WHERE price > (
    SELECT AVG(price)
    FROM business
);
"""

print("\nTASK 1: Above Average Price Products")
print(pd.read_sql_query(query_task1, conn).head(10))

# 5. SQL Query: Non-correlated subquery
# Find businesses with values above average.
# Replace revenue with your actual numeric column.

query_task2 = """
SELECT
    seller_id,
    MAX(price) AS highest_price
FROM business
GROUP BY seller_id
ORDER BY highest_price DESC;
"""

result_task2 = pd.read_sql_query(query_task2, conn)

print("\nTASK 2: Highest Price Per Seller")
print(result_task2.head(10))
print("Total sellers:", len(result_task2))



# TASK 3: CTE
# Find products with above-average prices

query3 = """
WITH average_price AS (
    SELECT AVG(price) AS avg_price
    FROM business
)
SELECT product_id, price
FROM business
WHERE price > (
    SELECT avg_price
    FROM average_price
);
"""

result3 = pd.read_sql_query(query3, conn)

print("\nTASK 3: Above Average Price Products")
print(result3.head(10))


# TASK 4: Two Chained CTEs
# Find sellers with above-average total sales

query4 = """
WITH seller_sales AS (
    SELECT
        seller_id,
        SUM(price) AS total_sales
    FROM business
    GROUP BY seller_id
),
average_seller_sales AS (
    SELECT AVG(total_sales) AS avg_sales
    FROM seller_sales
)
SELECT seller_id, total_sales
FROM seller_sales
WHERE total_sales > (
    SELECT avg_sales
    FROM average_seller_sales
)
ORDER BY total_sales DESC;
"""

result4 = pd.read_sql_query(query4, conn)

print("\nTASK 4: Above Average Seller Sales")
print(result4.head(10))


# Close connection at the end
conn.close()



