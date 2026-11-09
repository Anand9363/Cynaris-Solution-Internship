
# Week 2, Day 1 — Data Visualisation
# Project: EDA on Business Dataset

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')

# 1. Load Dataset
df = pd.read_csv(
    r"C:\Users\dkart\Downloads\archive\olist_order_items_dataset.csv"
)

print("Dataset Shape:", df.shape)
print(df.head())
print(df.info())

# 2. Data Cleaning
df['shipping_limit_date'] = pd.to_datetime(
    df['shipping_limit_date']
)

# Apply Seaborn Theme
sns.set_theme(style="whitegrid")

# 3. Line Chart - Monthly Sales Trend
df['month'] = df['shipping_limit_date'].dt.to_period('M')

monthly_sales = df.groupby('month')['price'].sum()

plt.figure(figsize=(10, 5))
plt.plot(monthly_sales.index.astype(str),
         monthly_sales.values, marker='o')

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("line_chart.png")
plt.show()

# 4. Bar Chart - Top 10 Sellers
top_sellers = df.groupby('seller_id')['price'].sum().nlargest(10)

plt.figure(figsize=(10, 5))
sns.barplot(x=top_sellers.index, y=top_sellers.values)

plt.title("Top 10 Sellers by Sales")
plt.xlabel("Seller ID")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("bar_chart.png")
plt.show()

# 5. Scatter Plot - Price vs Freight
sample_df = df.sample(min(2000, len(df)), random_state=42)

plt.figure(figsize=(8, 5))
sns.scatterplot(data=sample_df,
                x='price', y='freight_value')

plt.title("Product Price vs Freight Value")
plt.xlabel("Product Price")
plt.ylabel("Freight Value")
plt.tight_layout()
plt.savefig("scatter_chart.png")
plt.show()

# 6. Histogram - Price Distribution
plt.figure(figsize=(8, 5))
sns.histplot(data=df, x='price', bins=30, kde=True)

plt.title("Product Price Distribution")
plt.xlabel("Product Price")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("histogram.png")
plt.show()

# 7. Box Plot - Price Outliers
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x='price')

plt.title("Product Price Outliers")
plt.xlabel("Product Price")
plt.tight_layout()
plt.savefig("boxplot.png")
plt.show()

print("All 5 visualisations completed successfully!")
