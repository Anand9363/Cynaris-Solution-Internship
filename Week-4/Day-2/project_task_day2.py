
# Week 4 - Day 2: Probability
# Project: EDA on Indian Business Dataset

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")
np.random.seed(42)

# ------------------------------------------
# 1. LOAD DATASET
# ------------------------------------------

df = pd.read_csv(r"C:\Users\dkart\Downloads\archive\olist_order_items_dataset.csv")

print("Dataset Shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())

print("\nColumn names:")
print(df.columns.tolist())

# ------------------------------------------
# 2. BASIC PROBABILITY
# ------------------------------------------

# Select a column to create an event
# Example: first categorical column
categorical_cols = df.select_dtypes(
    include=["object", "category", "bool"]
).columns.tolist()

if categorical_cols:
    event_column = categorical_cols[0]

    # Remove missing values
    series = df[event_column].dropna()

    # Select most common category as event A
    event_value = series.mode()[0]

    # P(A) = Number of occurrences / Total observations
    probability_A = (series == event_value).mean()

    print("\n--- Basic Probability ---")
    print(f"Event A: {event_column} = {event_value}")
    print(f"P(A): {probability_A:.4f}")
    print(f"P(A) Percentage: {probability_A * 100:.2f}%")

else:
    print("\nNo categorical columns found for basic probability.")

# ------------------------------------------
# 3. JOINT & CONDITIONAL PROBABILITY
# ------------------------------------------

if len(categorical_cols) >= 2:

    col1 = categorical_cols[0]
    col2 = categorical_cols[1]

    temp = df[[col1, col2]].dropna()

    # Contingency table
    contingency_table = pd.crosstab(temp[col1], temp[col2])

    print("\n--- Contingency Table ---")
    print(contingency_table)

    # Select most common categories for A and B
    A_value = temp[col1].mode()[0]
    B_value = temp[col2].mode()[0]

    event_A = temp[col1] == A_value
    event_B = temp[col2] == B_value

    # P(A)
    P_A = event_A.mean()

    # P(B)
    P_B = event_B.mean()

    # P(A and B)
    P_A_and_B = (event_A & event_B).mean()

    # P(A | B)
    P_A_given_B = (event_A & event_B).sum() / event_B.sum()

    print("\n--- Probability Calculations ---")
    print(f"P(A): {P_A:.4f}")
    print(f"P(B): {P_B:.4f}")
    print(f"P(A and B): {P_A_and_B:.4f}")
    print(f"P(A | B): {P_A_given_B:.4f}")

    # Visualize contingency table
    contingency_table.plot(
        kind="bar",
        figsize=(10, 5)
    )

    plt.title("Contingency Table Analysis")
    plt.xlabel(col1)
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("probability_contingency.png")
    plt.show()

else:
    print("\nNeed at least 2 categorical columns for conditional probability.")

# ------------------------------------------
# 4. NORMAL DISTRIBUTION
# ------------------------------------------

numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

if numeric_cols:

    numeric_column = numeric_cols[0]
    data = df[numeric_column].dropna()

    mean = data.mean()
    std = data.std()

    print("\n--- Normal Distribution ---")
    print("Numeric Column:", numeric_column)
    print(f"Mean: {mean:.2f}")
    print(f"Standard Deviation: {std:.2f}")

    # Generate normal curve
    x = np.linspace(mean - 4 * std, mean + 4 * std, 1000)

    if std > 0:
        pdf = (1 / (std * np.sqrt(2 * np.pi))) * \
              np.exp(-0.5 * ((x - mean) / std) ** 2)

        plt.figure(figsize=(10, 5))
        plt.plot(x, pdf, label="Normal Distribution")
        plt.axvline(mean, linestyle="--", label="Mean")
        plt.axvline(mean - std, linestyle=":", label="-1 SD")
        plt.axvline(mean + std, linestyle=":", label="+1 SD")

        plt.title(f"Normal Distribution - {numeric_column}")
        plt.xlabel(numeric_column)
        plt.ylabel("Probability Density")
        plt.legend()
        plt.tight_layout()
        plt.savefig("probability_normal_distribution.png")
        plt.show()

    # 68-95-99.7 Rule
    within_1_sd = ((data >= mean - std) & (data <= mean + std)).mean()
    within_2_sd = ((data >= mean - 2 * std) & (data <= mean + 2 * std)).mean()
    within_3_sd = ((data >= mean - 3 * std) & (data <= mean + 3 * std)).mean()

    print("\n--- Empirical 68-95-99.7 Rule ---")
    print(f"Within 1 SD: {within_1_sd * 100:.2f}%")
    print(f"Within 2 SD: {within_2_sd * 100:.2f}%")
    print(f"Within 3 SD: {within_3_sd * 100:.2f}%")

else:
    print("\nNo numeric columns found.")

# ------------------------------------------
# 5. BINOMIAL DISTRIBUTION SIMULATION
# ------------------------------------------

# Example: probability of a successful sale = 30%
# 10 sales opportunities
# Repeat this experiment 10000 times

n = 10
p = 0.30
simulations = 10000

binomial_results = np.random.binomial(
    n=n,
    p=p,
    size=simulations
)

print("\n--- Binomial Simulation ---")
print("Trials per experiment:", n)
print("Success probability:", p)
print("Simulations:", simulations)
print("Average successes:", binomial_results.mean())

plt.figure(figsize=(8, 5))

plt.hist(
    binomial_results,
    bins=np.arange(-0.5, n + 1.5, 1),
    edgecolor="black"
)

plt.title("Binomial Distribution Simulation")
plt.xlabel("Number of Successful Sales")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("probability_binomial.png")
plt.show()

# ------------------------------------------
# 6. CENTRAL LIMIT THEOREM (CLT)
# ------------------------------------------

# Take many samples from the dataset
# Calculate the mean of each sample

if numeric_cols:

    population = df[numeric_column].dropna().values

    sample_size = 30
    number_of_samples = 1000

    sample_means = []

    for i in range(number_of_samples):

        sample = np.random.choice(
            population,
            size=sample_size,
            replace=True
        )

        sample_means.append(sample.mean())

    sample_means = np.array(sample_means)

    print("\n--- Central Limit Theorem ---")
    print("Sample Size:", sample_size)
    print("Number of Samples:", number_of_samples)
    print(f"Mean of Sample Means: {sample_means.mean():.2f}")
    print(f"Population Mean: {population.mean():.2f}")

    plt.figure(figsize=(8, 5))

    plt.hist(
        sample_means,
        bins=30,
        edgecolor="black"
    )

    plt.title("Central Limit Theorem - Sampling Distribution")
    plt.xlabel("Sample Mean")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig("probability_clt.png")
    plt.show()

# ------------------------------------------
# 7. SAVE PROBABILITY SUMMARY
# ------------------------------------------

summary = {
    "Concept": [
        "Binomial Mean",
        "Binomial Theoretical Mean",
        "CLT Mean of Sample Means"
    ],
    "Value": [
        binomial_results.mean(),
        n * p,
        sample_means.mean() if numeric_cols else np.nan
    ]
}

summary_df = pd.DataFrame(summary)

summary_df.to_csv(
    "probability_summary.csv",
    index=False
)

print("\nProbability summary saved successfully!")
print(summary_df)

print("\nDay 2 Probability Analysis Completed!")
