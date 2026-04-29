-- Sales Performance Analysis Database Schema
-- MySQL/PostgreSQL Compatible

-- Create Database
CREATE DATABASE IF NOT EXISTS sales_analytics;
USE sales_analytics;

-- Sales Transactions Table
CREATE TABLE IF NOT EXISTS sales_transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    order_date DATE NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    region VARCHAR(100) NOT NULL,
    sales_revenue DECIMAL(10, 2) NOT NULL,
    cost DECIMAL(10, 2) NOT NULL,
    profit DECIMAL(10, 2) NOT NULL,
    quantity_sold INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_order_date (order_date),
    INDEX idx_category (category),
    INDEX idx_region (region)
);

-- Aggregated Monthly Performance Table
CREATE TABLE IF NOT EXISTS monthly_performance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    year INT NOT NULL,
    month INT NOT NULL,
    region VARCHAR(100) NOT NULL,
    category VARCHAR(100) NOT NULL,
    total_revenue DECIMAL(12, 2),
    total_profit DECIMAL(12, 2),
    total_quantity INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_period (year, month, region, category)
);

-- Product Performance Summary
CREATE TABLE IF NOT EXISTS product_performance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    total_revenue DECIMAL(12, 2),
    total_profit DECIMAL(12, 2),
    total_quantity INT,
    avg_profit_margin DECIMAL(5, 2),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_product (product_name)
);

-- Common Queries for Analysis

-- Query 1: Total Sales and Profit by Region
CREATE OR REPLACE VIEW v_region_performance AS
SELECT 
    region,
    SUM(sales_revenue) as total_revenue,
    SUM(profit) as total_profit,
    SUM(quantity_sold) as total_quantity,
    AVG(profit / sales_revenue * 100) as avg_profit_margin
FROM sales_transactions
GROUP BY region
ORDER BY total_revenue DESC;

-- Query 2: Monthly Sales Trend
CREATE OR REPLACE VIEW v_monthly_trend AS
SELECT 
    YEAR(order_date) as year,
    MONTH(order_date) as month,
    DATE_FORMAT(order_date, '%Y-%m') as period,
    SUM(sales_revenue) as revenue,
    SUM(profit) as profit,
    SUM(quantity_sold) as quantity
FROM sales_transactions
GROUP BY year, month, period
ORDER BY year, month;

-- Query 3: Top 10 Products by Revenue
CREATE OR REPLACE VIEW v_top_products AS
SELECT 
    product_name,
    category,
    SUM(sales_revenue) as total_revenue,
    SUM(profit) as total_profit,
    SUM(quantity_sold) as total_quantity
FROM sales_transactions
GROUP BY product_name, category
ORDER BY total_revenue DESC
LIMIT 10;

-- Query 4: Category Performance
CREATE OR REPLACE VIEW v_category_performance AS
SELECT 
    category,
    COUNT(DISTINCT product_name) as product_count,
    SUM(sales_revenue) as total_revenue,
    SUM(profit) as total_profit,
    AVG(profit / sales_revenue * 100) as avg_profit_margin
FROM sales_transactions
GROUP BY category
ORDER BY total_revenue DESC;