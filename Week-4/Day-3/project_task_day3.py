
# Week 4 - Day 3: Regression Analysis
# Project: EDA on Indian Business Dataset

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings("ignore")

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

# -----------------------------------
# 1. Load Dataset
# -----------------------------------

df = pd.read_csv(r"C:\Users\dkart\Downloads\archive\olist_order_items_dataset.csv")

print("Dataset Shape:", df.shape)
print("\nFirst 5 Rows:")
print(df.head())

print("\nDataset Information:")
print(df.info())

# -----------------------------------
# 2. Data Cleaning
# -----------------------------------

df = df.drop_duplicates()
df = df.dropna()

numeric_df = df.select_dtypes(include=np.number)

print("\nNumeric Columns:")
print(numeric_df.columns.tolist())

# -----------------------------------
# 3. Pearson Correlation
# -----------------------------------

pearson_corr = numeric_df.corr(method="pearson")

print("\nPearson Correlation:")
print(pearson_corr.round(2))

# -----------------------------------
# 4. Spearman Correlation
# -----------------------------------

spearman_corr = numeric_df.corr(method="spearman")

print("\nSpearman Correlation:")
print(spearman_corr.round(2))

# -----------------------------------
# 5. Correlation Heatmap
# -----------------------------------

plt.figure(figsize=(10, 7))

sns.heatmap(
    pearson_corr,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    center=0
)

plt.title("Pearson Correlation Heatmap")
plt.tight_layout()
plt.savefig("outputs/correlation_heatmap.png")
plt.show()

# -----------------------------------
# 6. Scatter Matrix
# -----------------------------------

selected_columns = numeric_df.columns[:5]

pd.plotting.scatter_matrix(
    numeric_df[selected_columns],
    figsize=(12, 10),
    diagonal="hist"
)

plt.suptitle("Scatter Matrix of Numerical Variables")
plt.tight_layout()
plt.savefig("outputs/scatter_matrix.png")
plt.show()

# 7. Select Regression Variables

print("\nAvailable columns:")
print(df.columns.tolist())

feature_column = input("Enter feature column name: ")
target_column = input("Enter target column name: ")

if feature_column not in df.columns:
    raise ValueError(f"Feature column '{feature_column}' not found!")

if target_column not in df.columns:
    raise ValueError(f"Target column '{target_column}' not found!")

X = df[[feature_column]]
y = df[target_column]

print("\nFeature selected:", feature_column)
print("Target selected:", target_column)
# -----------------------------------
# 8. Train-Test Split
# -----------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# -----------------------------------
# 9. Build Linear Regression Model
# -----------------------------------

model = LinearRegression()

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("\nRegression Model")
print("Slope:", model.coef_[0])
print("Intercept:", model.intercept_)

# -----------------------------------
# 10. Model Evaluation
# -----------------------------------

r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print("\nModel Evaluation:")
print("R2 Score:", round(r2, 4))
print("MAE:", round(mae, 2))
print("RMSE:", round(rmse, 2))

# -----------------------------------
# 11. Actual vs Predicted Plot
# -----------------------------------

plt.figure(figsize=(8, 5))

plt.scatter(y_test, y_pred)
plt.xlabel("Actual Values")
plt.ylabel("Predicted Values")
plt.title("Actual vs Predicted")

plt.tight_layout()
plt.savefig("outputs/actual_vs_predicted.png")
plt.show()

# -----------------------------------
# 12. Residual Analysis
# -----------------------------------

residuals = y_test - y_pred

plt.figure(figsize=(8, 5))

plt.scatter(y_pred, residuals)
plt.axhline(y=0, color="red", linestyle="--")

plt.xlabel("Predicted Values")
plt.ylabel("Residuals")
plt.title("Residual Plot")

plt.tight_layout()
plt.savefig("outputs/residual_plot.png")
plt.show()

# -----------------------------------
# 13. Residual Distribution
# -----------------------------------

plt.figure(figsize=(8, 5))

sns.histplot(residuals, kde=True)

plt.title("Residual Distribution")
plt.xlabel("Residuals")

plt.tight_layout()
plt.savefig("outputs/residual_distribution.png")
plt.show()

# -----------------------------------
# 14. Save Results
# -----------------------------------

results = pd.DataFrame({
    "Actual": y_test.values,
    "Predicted": y_pred,
    "Residual": residuals.values
})

results.to_csv("outputs/regression_results.csv", index=False)

print("\nRegression analysis completed successfully!")
