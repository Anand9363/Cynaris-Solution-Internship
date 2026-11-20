
# W3D5 - KPI DESIGN
# E-Commerce Order Analytics

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')

# 1. Load Dataset
df = pd.read_csv(r"C:\Users\dkart\Downloads\archive\olist_order_items_dataset.csv")

# 2. Data Preparation
df['shipping_limit_date'] = pd.to_datetime(
    df['shipping_limit_date']
)

# 3. KPI Calculations
total_revenue = df['price'].sum()
total_orders = df['order_id'].nunique()
total_products_sold = len(df)

average_order_value = total_revenue / total_orders
average_product_price = df['price'].mean()

total_freight = df['freight_value'].sum()
average_freight = df['freight_value'].mean()

active_sellers = df['seller_id'].nunique()
unique_products = df['product_id'].nunique()

revenue_per_seller = total_revenue / active_sellers

# 4. KPI Framework
kpis = {
    'Total Revenue': total_revenue,
    'Total Orders': total_orders,
    'Total Products Sold': total_products_sold,
    'Average Order Value': average_order_value,
    'Average Product Price': average_product_price,
    'Total Freight': total_freight,
    'Average Freight': average_freight,
    'Active Sellers': active_sellers,
    'Unique Products': unique_products,
    'Revenue per Seller': revenue_per_seller
}

print("\n========== KPI DASHBOARD ==========\n")

for name, value in kpis.items():
    print(f"{name}: {value:,.2f}")

# 5. Visualize KPIs
plt.figure(figsize=(10, 5))

plt.bar(
    ['Revenue', 'Freight'],
    [total_revenue, total_freight]
)

plt.title('Revenue vs Freight')
plt.ylabel('Amount')

plt.tight_layout()
plt.savefig('kpi_revenue_freight.png')
plt.show()

# 6. Seller Performance
seller_revenue = df.groupby(
    'seller_id'
)['price'].sum().sort_values(ascending=False)

print("\nTop 5 Sellers by Revenue:")
print(seller_revenue.head())

# 7. Save KPI Results
kpi_df = pd.DataFrame(
    list(kpis.items()),
    columns=['KPI', 'Value']
)

kpi_df.to_csv('kpi_results.csv', index=False)

print("\nKPI analysis completed successfully!")



# 8. SINGLE-PAGE KPI DASHBOARD

fig = plt.figure(figsize=(16, 9))
gs = fig.add_gridspec(3, 5, height_ratios=[1, 1, 2])

fig.suptitle(
    "E-Commerce Business KPI Dashboard",
    fontsize=20,
    fontweight='bold'
)

# KPI cards
kpi_items = [
    ("Total Revenue", f"Rs. {total_revenue:,.0f}"),
    ("Total Orders", f"{total_orders:,}"),
    ("Products Sold", f"{total_products_sold:,}"),
    ("Average Order Value", f"Rs. {average_order_value:,.2f}"),
    ("Average Product Price", f"Rs. {average_product_price:,.2f}"),
    ("Total Freight", f"Rs. {total_freight:,.0f}"),
    ("Average Freight", f"Rs. {average_freight:,.2f}"),
    ("Active Sellers", f"{active_sellers:,}"),
    ("Unique Products", f"{unique_products:,}"),
    ("Revenue per Seller", f"Rs. {revenue_per_seller:,.2f}")
]

for i, (name, value) in enumerate(kpi_items):
    ax = fig.add_subplot(gs[i // 5, i % 5])
    ax.set_facecolor('#EAF2F8')
    ax.text(0.5, 0.65, name,
            ha='center', fontsize=11)
    ax.text(0.5, 0.35, value,
            ha='center', fontsize=15,
            fontweight='bold')
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

# Top 5 Sellers chart
ax1 = fig.add_subplot(gs[2, :3])

top5 = seller_revenue.head(5).sort_values()

ax1.barh(
    range(len(top5)),
    top5.values
)

ax1.set_yticks(range(len(top5)))
ax1.set_yticklabels(top5.index)
ax1.set_title("Top 5 Sellers by Revenue")
ax1.set_xlabel("Revenue (Rs.)")

# Business insights
ax2 = fig.add_subplot(gs[2, 3:])
ax2.axis('off')

insights = f"""
BUSINESS INSIGHTS

Total Revenue:
Rs. {total_revenue:,.2f}

Total Orders:
{total_orders:,}

Active Sellers:
{active_sellers:,}

Average Order Value:
Rs. {average_order_value:,.2f}

Freight / Revenue:
{(total_freight / total_revenue) * 100:.2f}%

Top Seller Revenue:
Rs. {seller_revenue.iloc[0]:,.2f}
"""

ax2.text(
    0.05, 0.95,
    insights,
    va='top',
    fontsize=12,
    linespacing=1.8
)

plt.tight_layout()

plt.savefig(
    "kpi_dashboard.png",
    dpi=200,
    bbox_inches='tight'
)

plt.show()

print("KPI Dashboard saved successfully!")
