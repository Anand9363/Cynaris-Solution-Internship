
# ============================================================
# WEEK 3 - DAY 2: DAX BASICS
# Project: EDA on Indian Business Dataset
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')

# 1. LOAD DATASET
df = pd.read_csv(r"C:\Users\dkart\Downloads\archive\olist_order_items_dataset.csv"

)
df.columns = df.columns.str.strip()

print("=" * 60)
print("WEEK 3 - DAY 2: DAX BASICS")
print("=" * 60)

print("\nDataset Shape:", df.shape)

print("\nDataset Columns:")
print(df.columns.tolist())

print("\nFirst 5 Records:")
print(df.head())

# 2. DATA CLEANING
print("\nMissing Values:")
print(df.isnull().sum())

# Automatically identify columns
date_candidates = [
    'Date', 'Order_Date', 'Order Date',
    'Transaction_Date', 'Transaction Date',
    'Sales_Date', 'Invoice_Date'
]

revenue_candidates = [
    'Revenue', 'Sales', 'Total_Sales',
    'Amount', 'Sales_Amount', 'Total_Amount'
]

cost_candidates = [
    'Cost', 'Total_Cost', 'Purchase_Cost',
    'Expense', 'Expenses'
]

state_candidates = [
    'State', 'State_Name', 'Region', 'Location'
]

def find_column(candidates):
    for column in candidates:
        if column in df.columns:
            return column
    return None

date_col = find_column(date_candidates)
revenue_col = find_column(revenue_candidates)
cost_col = find_column(cost_candidates)
state_col = find_column(state_candidates)

print("\nDetected Columns:")
print("Date:", date_col)
print("Revenue:", revenue_col)
print("Cost:", cost_col)
print("State:", state_col)

# 3. CONVERT NUMERICAL COLUMNS
if revenue_col:
    df[revenue_col] = pd.to_numeric(
        df[revenue_col], errors='coerce'
    )

if cost_col:
    df[cost_col] = pd.to_numeric(
        df[cost_col], errors='coerce'
    )

# 4. CALCULATED COLUMN - PROFIT
if revenue_col and cost_col:

    df['Profit'] = df[revenue_col] - df[cost_col]

    print("\nProfit Column:")
    print(df['Profit'].head())

# 5. CALCULATED COLUMN - PROFIT MARGIN %
if revenue_col and cost_col:

    df['Profit_Margin'] = np.where(
        df[revenue_col] != 0,
        (df['Profit'] / df[revenue_col]) * 100,
        0
    )

    print("\nProfit Margin:")
    print(df['Profit_Margin'].head())

# 6. MEASURE - TOTAL SALES
if revenue_col:

    total_sales = df[revenue_col].sum()

    print("\nTotal Sales:", total_sales)

# 7. CALCULATE CONCEPT - STATE-WISE SALES
if revenue_col and state_col:

    state_sales = df.groupby(state_col)[revenue_col].sum()

    print("\nState-wise Sales:")
    print(state_sales)

# 8. YTD SALES - YEAR TO DATE
if revenue_col and date_col:

    df[date_col] = pd.to_datetime(
        df[date_col], errors='coerce'
    )

    valid_dates = df.dropna(subset=[date_col])

    if not valid_dates.empty:

        latest_year = valid_dates[date_col].max().year

        ytd_sales = valid_dates.loc[
            valid_dates[date_col].dt.year == latest_year,
            revenue_col
        ].sum()

        print("\nYTD Sales:", ytd_sales)

    else:
        print("\nYTD Sales: No valid dates found.")

else:
    print("\nYTD Sales: Date or Revenue column unavailable.")

# 9. RUNNING TOTAL
if revenue_col and date_col:

    valid_data = df.dropna(subset=[date_col]).copy()

    valid_data = valid_data.sort_values(date_col)

    valid_data['Running_Total'] = (
        valid_data.groupby(
            valid_data[date_col].dt.year
        )[revenue_col].cumsum()
    )

    print("\nRunning Total:")
    print(
        valid_data[
            [date_col, revenue_col, 'Running_Total']
        ].head(10)
    )

else:
    print("\nRunning Total: Required columns unavailable.")

# 10. BUSINESS SUMMARY
print("\n" + "=" * 60)
print("BUSINESS SUMMARY")
print("=" * 60)

if revenue_col:
    print("Total Revenue:", df[revenue_col].sum())

if cost_col:
    print("Total Cost:", df[cost_col].sum())

if 'Profit' in df.columns:
    print("Total Profit:", df['Profit'].sum())

if 'Profit_Margin' in df.columns:
    print(
        "Average Profit Margin:",
        df['Profit_Margin'].mean()
    )

# 11. STATE-WISE SALES VISUALIZATION
if revenue_col and state_col:

    state_sales = df.groupby(state_col)[revenue_col].sum()

    state_sales.plot(kind='bar', figsize=(10, 5))

    plt.title('State-wise Business Sales')
    plt.xlabel('State')
    plt.ylabel('Revenue')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# 12. MONTHLY SALES TREND
if revenue_col and date_col:

    valid_data = df.dropna(subset=[date_col]).copy()

    if not valid_data.empty:

        monthly_sales = (
            valid_data.set_index(date_col)[revenue_col]
            .resample('ME')
            .sum()
        )

        monthly_sales.plot(figsize=(10, 5))

        plt.title('Monthly Sales Trend')
        plt.xlabel('Month')
        plt.ylabel('Revenue')
        plt.tight_layout()
        plt.show()

# 13. SAVE UPDATED DATASET
df.to_csv('day2_business_analysis.csv', index=False)

print("\n" + "=" * 60)
print("WEEK 3 - DAY 2 ANALYSIS COMPLETED!")
print("Analysis saved successfully.")
print("=" * 60)
