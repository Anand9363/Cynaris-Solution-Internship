
-- Week 1, Day 4
-- SQL Subqueries & CTEs
-- Project: E-Commerce Business Dataset

-- TASK 1: Non-correlated subquery
-- Find products with above-average price

SELECT
    product_id,
    price
FROM business
WHERE price > (
    SELECT AVG(price)
    FROM business
);


-- TASK 2: Correlated subquery
-- Find the highest-priced product in each seller's listings

SELECT
    b1.seller_id,
    b1.product_id,
    b1.price
FROM business b1
WHERE b1.price = (
    SELECT MAX(b2.price)
    FROM business b2
    WHERE b2.seller_id = b1.seller_id
);


-- TASK 3: Rewrite nested subquery using CTE
-- Calculate average product price

WITH average_price AS (
    SELECT AVG(price) AS avg_price
    FROM business
)
SELECT
    product_id,
    price
FROM business
WHERE price > (
    SELECT avg_price
    FROM average_price
);


-- TASK 4: Chain two CTEs
-- Find sellers whose total sales value is
-- above the average seller sales value

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
SELECT
    seller_id,
    total_sales
FROM seller_sales
WHERE total_sales > (
    SELECT avg_sales
    FROM average_seller_sales
)
ORDER BY total_sales DESC;
