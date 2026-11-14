
# ============================================================
# W2D6: DATA GOVERNANCE - QUALITY, CONTRACTS & GREAT EXPECTATIONS
# Project: EDA on Indian Business Dataset
# ============================================================

import sys
import json
import warnings
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import great_expectations as gx

warnings.filterwarnings("ignore")

# ============================================================
# 1. LOAD DATASET
# ============================================================

print("=" * 65)
print("W2D6 - DATA GOVERNANCE")
print("=" * 65)

print("Python Version:", sys.version)

FILE_PATH = r"C:\Users\dkart\Downloads\archive\olist_order_items_dataset.csv"

df = pd.read_csv(FILE_PATH)

if df.empty:
    raise ValueError("Dataset is empty!")

if len(df.columns) < 2:
    raise ValueError("Dataset needs at least two columns.")

print("\nDataset Loaded Successfully!")
print("Dataset Shape:", df.shape)

print("\nFirst 5 Records:")
print(df.head())

print("\nDataset Information:")
df.info()

# ============================================================
# 2. INITIAL DATA QUALITY ANALYSIS
# ============================================================

print("\n" + "=" * 65)
print("INITIAL DATA QUALITY ANALYSIS")
print("=" * 65)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Records:", df.duplicated().sum())

print("\nData Types:")
print(df.dtypes)

# Identify columns
numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

id_cols = [
    col for col in df.columns
    if "id" in col.lower()
]

id_col = id_cols[0] if id_cols else df.columns[0]

num_col = numeric_cols[0] if numeric_cols else None

# ============================================================
# 3. SIX DAMA DATA QUALITY DIMENSIONS
# ============================================================

print("\n" + "=" * 65)
print("SIX DAMA DATA QUALITY DIMENSIONS")
print("=" * 65)

total_cells = df.size

# 1. Completeness
completeness = (
    100 * (1 - df.isnull().sum().sum() / total_cells)
    if total_cells else 0
)

# 2. Accuracy (basic numeric plausibility proxy)
if numeric_cols:
    numeric_data = df[numeric_cols]
    total_numeric = numeric_data.notna().sum().sum()

    accuracy = (
        100 * (numeric_data.ge(0).sum().sum() / total_numeric)
        if total_numeric else np.nan
    )
else:
    accuracy = np.nan

# 3. Consistency (basic structural consistency proxy)
consistency = 100 if df.columns.is_unique else 0

# 4. Timeliness (date parseability proxy, not an SLA test)
date_cols = [
    col for col in df.columns
    if any(word in col.lower()
           for word in ["date", "time", "created", "updated"])
]

if date_cols:
    date_values = pd.to_datetime(
        df[date_cols[0]], errors="coerce"
    )
    timeliness = 100 * date_values.notna().mean()
else:
    timeliness = np.nan

# 5. Uniqueness (complete-row uniqueness)
uniqueness = 100 * (1 - df.duplicated().mean())

# 6. Validity (basic non-empty column-name check)
validity = (
    100 if all(
        isinstance(col, str) and col.strip()
        for col in df.columns
    ) else 0
)

quality_scorecard = pd.DataFrame({
    "Dimension": [
        "Completeness",
        "Accuracy",
        "Consistency",
        "Timeliness",
        "Uniqueness",
        "Validity"
    ],
    "Score (%)": [
        completeness,
        accuracy,
        consistency,
        timeliness,
        uniqueness,
        validity
    ]
})

print(quality_scorecard.to_string(index=False))

quality_scorecard.to_csv(
    "data_quality_scorecard.csv", index=False
)

# ============================================================
# 4. DEFINE EXACTLY EIGHT GREAT EXPECTATIONS
# ============================================================

print("\n" + "=" * 65)
print("GREAT EXPECTATIONS - EIGHT CHECKS")
print("=" * 65)

# A valid identifier must be unique and non-null for these checks.
# Review this assumption if your selected ID column is not unique.

expectations = [
    # 1. Dataset must contain at least one row
    gx.expectations.ExpectTableRowCountToBeBetween(
        min_value=1
    ),

    # 2. Dataset must contain at least two columns
    gx.expectations.ExpectTableColumnCountToBeBetween(
        min_value=2
    ),

    # 3. ID must not be null
    gx.expectations.ExpectColumnValuesToNotBeNull(
        column=id_col
    ),

    # 4. ID must be unique
    gx.expectations.ExpectColumnValuesToBeUnique(
        column=id_col
    )
]

# 5. Numeric values must be non-negative
if num_col:
    expectations.append(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column=num_col,
            min_value=0
        )
    )
else:
    # Fallback when dataset has no numeric columns
    expectations.append(
        gx.expectations.ExpectColumnValuesToNotBeNull(
            column=df.columns[1]
        )
    )

# 6, 7, 8. Three additional column completeness checks
additional_cols = [
    col for col in df.columns
    if col != id_col and col != num_col
]

for col in additional_cols[:3]:
    expectations.append(
        gx.expectations.ExpectColumnValuesToNotBeNull(
            column=col
        )
    )

# Fill remaining checks with non-null checks if needed
while len(expectations) < 8:
    col = df.columns[len(expectations) % len(df.columns)]

    expectations.append(
        gx.expectations.ExpectColumnValuesToNotBeNull(
            column=col
        )
    )

expectations = expectations[:8]

assert len(expectations) == 8

# ============================================================
# 5. CREATE GREAT EXPECTATIONS CONTEXT AND SUITE
# ============================================================

print("\nCreating Great Expectations suite...")

context = gx.get_context()

data_source = context.data_sources.add_pandas(
    name="business_data_source"
)

data_asset = data_source.add_dataframe_asset(
    name="business_data"
)

batch_definition = (
    data_asset.add_batch_definition_whole_dataframe(
        "business_batch"
    )
)

suite = gx.ExpectationSuite(
    name="business_data_quality_suite"
)

for expectation in expectations:
    suite.add_expectation(expectation)

context.suites.add(suite)

validation_definition = gx.ValidationDefinition(
    name="business_data_validation",
    data=batch_definition,
    suite=suite
)

context.validation_definitions.add(
    validation_definition
)

# ============================================================
# 6. VALIDATE ORIGINAL DATA
# ============================================================

print("\n" + "=" * 65)
print("ORIGINAL DATA VALIDATION")
print("=" * 65)

original_result = validation_definition.run(
    batch_parameters={"dataframe": df}
)

print("Original Data Success:", original_result.success)

original_results = []

for item in original_result.results:
    original_results.append({
        "Expectation": item.expectation_config.type,
        "Status": "PASS" if item.success else "FAIL"
    })

original_df = pd.DataFrame(original_results)

print(original_df.to_string(index=False))

# ============================================================
# 7. INJECT THREE INTENTIONAL ERRORS
# ============================================================

print("\n" + "=" * 65)
print("INJECTING THREE DATA QUALITY ERRORS")
print("=" * 65)

test_df = df.copy(deep=True)

# Error 1: Inject a missing ID
test_df.loc[test_df.index[0], id_col] = np.nan

print("Error 1: Missing ID value injected")

# Error 2: Inject a negative numeric value
if num_col:
    test_df.loc[test_df.index[1], num_col] = -999
    print("Error 2: Negative numeric value injected")
else:
    print("Error 2: Skipped - no numeric column available")

# Error 3: Inject a duplicate ID
test_df.loc[test_df.index[-1], id_col] = test_df.iloc[0][id_col]

# The first ID is now missing, so instead use a known non-null ID
valid_ids = df[id_col].dropna()

if not valid_ids.empty:
    test_df.loc[test_df.index[-1], id_col] = valid_ids.iloc[0]

print("Error 3: Duplicate ID injected")

# ============================================================
# 8. VALIDATE CORRUPTED DATA WITH GX
# ============================================================

print("\n" + "=" * 65)
print("CORRUPTED DATA - GREAT EXPECTATIONS VALIDATION")
print("=" * 65)

corrupted_result = validation_definition.run(
    batch_parameters={"dataframe": test_df}
)

print("Corrupted Data Success:", corrupted_result.success)

corrupted_results = []

for item in corrupted_result.results:
    corrupted_results.append({
        "Expectation": item.expectation_config.type,
        "Status": "PASS" if item.success else "FAIL"
    })

corrupted_df = pd.DataFrame(corrupted_results)

print(corrupted_df.to_string(index=False))

print("\nFailed Expectations:")
print(
    corrupted_df[corrupted_df["Status"] == "FAIL"]
    .to_string(index=False)
)

# ============================================================
# 9. VERIFY THREE INJECTED ERRORS
# ============================================================

print("\n" + "=" * 65)
print("ERROR DETECTION VERIFICATION")
print("=" * 65)

missing_detected = test_df[id_col].isnull().any()

duplicate_detected = test_df[id_col].duplicated().any()

negative_detected = (
    (test_df[num_col] < 0).any()
    if num_col else False
)

print("Missing Value Detected:", missing_detected)
print("Duplicate ID Detected:", duplicate_detected)
print("Negative Value Detected:", negative_detected)

# ============================================================
# 10. PII CLASSIFICATION
# ============================================================

print("\n" + "=" * 65)
print("PII CLASSIFICATION")
print("=" * 65)

pii_keywords = [
    "name", "email", "phone", "mobile",
    "address", "aadhaar", "pan", "passport",
    "dob", "birth", "customer_id"
]

pii_results = []

for col in df.columns:

    if any(word in col.lower() for word in pii_keywords):

        classification = "Confidential / Potential PII"
        strategy = "Mask or tokenize sensitive values"

    else:

        classification = "Review required"
        strategy = "Check context before sharing"

    pii_results.append({
        "Column": col,
        "Classification": classification,
        "Protection Strategy": strategy
    })

pii_df = pd.DataFrame(pii_results)

print(pii_df.to_string(index=False))

pii_df.to_csv(
    "pii_classification.csv", index=False
)

# ============================================================
# 11. CREATE YAML DATA CONTRACT
# ============================================================

print("\n" + "=" * 65)
print("CREATING DATA CONTRACT")
print("=" * 65)

import yaml

contract = {
    "dataContractSpecification": "0.9.3",

    "id": "indian-business-data-v1",

    "info": {
        "title": "Indian Business Dataset",
        "owner": "Data Analyst",
        "producer": "Data Analyst",
        "consumer": "BI Dashboard",
        "description": "Data quality and governance contract"
    },

    "quality": {
        "completeness": "Required fields must not be null",
        "uniqueness": "Identifier fields must be unique",
        "validity": "Values must follow defined formats",
        "freshness": "Refresh schedule must be agreed"
    },

    "models": {
        "business": {
            "fields": {}
        }
    },

    "security": {
        "pii_handling": [
            "Identify sensitive columns",
            "Mask personal information",
            "Restrict access to authorised users",
            "Use tokenisation where appropriate"
        ]
    },

    "sla": {
        "freshness": "To be agreed with BI dashboard consumer",
        "quality": "Critical validation failures must be resolved"
    }
}

for col in df.columns:

    contract["models"]["business"]["fields"][str(col)] = {
        "type": str(df[col].dtype),
        "required": bool(not df[col].isnull().any()),
        "classification": (
            "Confidential / Potential PII"
            if any(word in col.lower() for word in pii_keywords)
            else "Review required"
        )
    }

with open(
    "data_contract.yaml",
    "w",
    encoding="utf-8"
) as file:

    yaml.safe_dump(
        contract,
        file,
        sort_keys=False,
        allow_unicode=True
    )

print("Data Contract Created Successfully!")

# ============================================================
# 12. GENERATE HTML VALIDATION REPORT
# ============================================================

print("\nGenerating HTML Report...")

html_report = f"""
<html>
<head>
<title>W2D6 Data Quality Report</title>

<style>
body {{
    font-family: Arial;
    margin: 30px;
}}

table {{
    border-collapse: collapse;
    width: 100%;
}}

th, td {{
    border: 1px solid #ddd;
    padding: 10px;
}}

th {{
    background-color: #eeeeee;
}}
</style>
</head>

<body>

<h1>W2D6 - Data Governance Report</h1>

<h2>Dataset Overview</h2>

<p>Rows: {len(df)}</p>
<p>Columns: {len(df.columns)}</p>

<h2>DAMA Data Quality Scorecard</h2>

{quality_scorecard.to_html(index=False)}

<h2>Original Data Validation</h2>

<p>GX Success: {original_result.success}</p>

{original_df.to_html(index=False)}

<h2>Corrupted Data Validation</h2>

<p>GX Success: {corrupted_result.success}</p>

{corrupted_df.to_html(index=False)}

<h2>Error Detection</h2>

<p>Missing Value Detected: {missing_detected}</p>
<p>Duplicate ID Detected: {duplicate_detected}</p>
<p>Negative Value Detected: {negative_detected}</p>

<h2>PII Classification</h2>

{pii_df.to_html(index=False)}

</body>
</html>
"""

with open(
    "great_expectations_report.html",
    "w",
    encoding="utf-8"
) as file:

    file.write(html_report)

# ============================================================
# 13. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 65)
print("W2D6 DATA GOVERNANCE - COMPLETED")
print("=" * 65)

print("Dataset Shape:", df.shape)

print("DAMA Dimensions Evaluated:", 6)

print("Great Expectations Checks:", len(expectations))

print("Original Validation:", original_result.success)

print("Corrupted Validation:", corrupted_result.success)

print("Missing Value Detected:", missing_detected)

print("Duplicate ID Detected:", duplicate_detected)

print("Negative Value Detected:", negative_detected)

print("\nGenerated Deliverables:")

print("1. data_quality_scorecard.csv")
print("2. data_contract.yaml")
print("3. pii_classification.csv")
print("4. great_expectations_report.html")

print("\nW2D6 Analysis Completed Successfully!")
