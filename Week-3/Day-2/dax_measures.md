
# Week 3 - Day 2: DAX Basics

## 1. Total Sales
```dax
Total Sales = SUM(Sales[Revenue])
```
Explanation: Calculates total revenue.

## 2. CALCULATE - State-wise Sales
```dax
Tamil Nadu Sales =
CALCULATE(
    [Total Sales],
    Sales[State] = "Tamil Nadu"
)
```
Explanation: Calculates sales only for Tamil Nadu.

## 3. YTD Sales
```dax
YTD Sales =
TOTALYTD(
    [Total Sales],
    'Date'[Date]
)
```
Explanation: Calculates sales from the beginning of the year.

## 4. Running Total
```dax
Running Total =
CALCULATE(
    [Total Sales],
    FILTER(
        ALL('Date'[Date]),
        'Date'[Date] <= MAX('Date'[Date])
    )
)
```
Explanation: Calculates cumulative sales over time.

## 5. Profit Margin %
```dax
Profit Margin % =
DIVIDE(
    SUM(Sales[Revenue]) - SUM(Sales[Cost]),
    SUM(Sales[Revenue]),
    0
) * 100
```
Explanation: Calculates profit as a percentage of revenue.

## Context Concepts

- Row Context: Calculation for each individual row.
- Filter Context: Calculation based on applied filters.
- Context Transition: CALCULATE converts row context into filter context.
