create database Superstore;
use Superstore;

CREATE TABLE superstore (
    row_id INT PRIMARY KEY,
    order_id VARCHAR(20),
    order_date DATE,
    ship_date DATE,
    ship_mode VARCHAR(50),
    customer_id VARCHAR(20),
    customer_name VARCHAR(100),
    segment VARCHAR(50),
    country VARCHAR(50),
    city VARCHAR(50),
    state VARCHAR(50),
    postal_code INT,
    region VARCHAR(50),
    product_id VARCHAR(20),
    category VARCHAR(50),
    sub_category VARCHAR(50),
    product_name TEXT,
    sales FLOAT,
    quantity INT,
    discount FLOAT,
    profit FLOAT
);

SELECT 
    YEAR(order_date) AS Year,
    MONTH(order_date) AS Month,
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit
FROM superstore
GROUP BY Year, Month
ORDER BY Year, Month;

SELECT 
    category, sub_category,
    SUM(Sales) AS Sales,
    SUM(Profit) AS Profit
FROM superstore
GROUP BY category, sub_category
ORDER BY Sales DESC;

SELECT product_name, SUM(Sales), SUM(Profit)
FROM superstore
GROUP BY Product_name
HAVING SUM(Profit) < 0
ORDER BY SUM(Sales) DESC;

SELECT 
    region, state,
    SUM(Sales) AS Sales,
    SUM(Profit) AS Profit,
    SUM(Profit) / SUM(Sales) AS Profit_Margin
FROM superstore
GROUP BY region, state
ORDER BY Profit DESC;



SELECT 
    ship_mode,
    AVG(DATEDIFF(ship_date, order_date)) AS Avg_Delivery_Time,
    SUM(Sales) AS Sales,
    SUM(Profit) AS Profit
FROM superstore
GROUP BY ship_mode;