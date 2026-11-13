
# Week 2, Day 5 — NumPy for Data
# Project: EDA on Business Dataset

import sys
import time
import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

print("=" * 55)
print("WEEK 2 DAY 5 - NUMPY FOR DATA")
print("=" * 55)

print(f"Python Version: {sys.version}")

# 1. Load Dataset
df = pd.read_csv(r"C:\Users\dkart\Downloads\archive\olist_order_items_dataset.csv")

print("\nDataset loaded successfully!")
print("Dataset Shape:", df.shape)

print("\nFirst 5 Records:")
print(df.head())

# 2. Select Numerical Columns
numeric_df = df.select_dtypes(include=np.number)

print("\nNumerical Columns:")
print(numeric_df.columns.tolist())

# Convert numerical data into NumPy array
data = numeric_df.to_numpy()

print("\nNumPy Array:")
print(data[:5])

print("Array Shape:", data.shape)
print("Array Dimensions:", data.ndim)

# 3. Create 1D, 2D and 3D Arrays
arr_1d = np.array([10, 20, 30, 40, 50])

arr_2d = np.array([
    [10, 20, 30],
    [40, 50, 60]
])

arr_3d = np.array([
    [[1, 2], [3, 4]],
    [[5, 6], [7, 8]]
])

print("\n1D Array:", arr_1d)
print("2D Array:\n", arr_2d)
print("3D Array:\n", arr_3d)

# 4. Vectorised Operations
prices = df["price"].to_numpy()
freight = df["freight_value"].to_numpy()

print("\nVectorised Operations")
print("First 5 Prices:", prices[:5])
print("Prices + 100:", prices[:5] + 100)
print("Prices * 2:", prices[:5] * 2)

# Total sales and average price
print("Total Sales:", np.sum(prices))
print("Average Price:", np.mean(prices))

# 5. Aggregation Across Axes
sample_array = np.array([
    [10, 20, 30],
    [40, 50, 60]
])

print("\nAxis Operations")
print("Column-wise Sum:", np.sum(sample_array, axis=0))
print("Row-wise Sum:", np.sum(sample_array, axis=1))

# 6. Boolean Masking
high_price = prices[prices > 100]

print("\nBoolean Masking")
print("Products above 100:", len(high_price))
print("First 10 high prices:", high_price[:10])

# 7. Fancy Indexing
print("\nFancy Indexing")
print("Selected Prices:", prices[[0, 2, 4, 6, 8]])

# 8. Statistical Analysis
print("\nStatistical Analysis")

print("Mean Price:", np.mean(prices))
print("Median Price:", np.median(prices))
print("Standard Deviation:", np.std(prices))
print("25th Percentile:", np.percentile(prices, 25))
print("50th Percentile:", np.percentile(prices, 50))
print("75th Percentile:", np.percentile(prices, 75))
print("Maximum Price:", np.max(prices))
print("Minimum Price:", np.min(prices))

# 9. Correlation Analysis
correlation = np.corrcoef(prices, freight)[0, 1]

print("\nCorrelation Analysis")
print("Price and Freight Correlation:", correlation)

# 10. Broadcasting
sample_sales = np.array([
    [1000, 2000, 3000],
    [4000, 5000, 6000]
])

tax = 100

print("\nBroadcasting")
print("Original Sales:\n", sample_sales)
print("After Adding Tax:\n", sample_sales + tax)

# 11. Performance Comparison - 1 Million Rows
numbers = list(range(1_000_000))

start = time.perf_counter()
python_result = [x * 2 for x in numbers]
python_time = time.perf_counter() - start

numpy_numbers = np.arange(1_000_000)

start = time.perf_counter()
numpy_result = numpy_numbers * 2
numpy_time = time.perf_counter() - start

print("\nPerformance Comparison")
print("Python Loop Time:", python_time, "seconds")
print("NumPy Time:", numpy_time, "seconds")

if numpy_time > 0:
    print("Speedup:", python_time / numpy_time)

# 12. Visualisation
plt.figure(figsize=(8, 5))
plt.hist(prices, bins=30)
plt.title("Price Distribution")
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# 13. Final Summary
print("\n" + "=" * 55)
print("NUMPY ANALYSIS COMPLETED SUCCESSFULLY!")
print("=" * 55)

print("Total Records:", len(df))
print("Total Numerical Columns:", len(numeric_df.columns))
print("Total Sales:", np.sum(prices))
print("Average Price:", np.mean(prices))
print("Price-Freight Correlation:", correlation)
