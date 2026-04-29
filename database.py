"""
Database Module
Handles all database operations for the sales analytics system
"""

import pandas as pd
import sqlite3
from datetime import datetime
import os


class DatabaseManager:
    """Manage database connections and operations"""
    
    def __init__(self, db_path='sales_analytics.db'):
        """Initialize database connection"""
        self.db_path = db_path
        self.conn = None
        
    def connect(self):
        """Establish database connection"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            print(f"✅ Connected to database: {self.db_path}")
            return self.conn
        except Exception as e:
            print(f"❌ Database connection error: {e}")
            return None
    
    def create_tables(self):
        """Create necessary tables"""
        if not self.conn:
            self.connect()
        
        cursor = self.conn.cursor()
        
        # Sales transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales_transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_date DATE NOT NULL,
                product_name TEXT NOT NULL,
                category TEXT NOT NULL,
                region TEXT NOT NULL,
                sales_revenue REAL NOT NULL,
                cost REAL NOT NULL,
                profit REAL NOT NULL,
                quantity_sold INTEGER NOT NULL,
                profit_margin REAL,
                year INTEGER,
                month INTEGER,
                quarter INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Monthly performance summary table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS monthly_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                year INTEGER NOT NULL,
                month INTEGER NOT NULL,
                region TEXT NOT NULL,
                category TEXT NOT NULL,
                total_revenue REAL,
                total_profit REAL,
                total_quantity INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(year, month, region, category)
            )
        ''')
        
        # Product performance summary
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS product_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL UNIQUE,
                category TEXT NOT NULL,
                total_revenue REAL,
                total_profit REAL,
                total_quantity INTEGER,
                avg_profit_margin REAL,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
        print("✅ Database tables created successfully")
        
    def insert_sales_data(self, df):
        """Insert sales data from dataframe"""
        if not self.conn:
            self.connect()
        
        try:
            # Prepare dataframe for insertion
            df_to_insert = df[[
                'Order Date', 'Product Name', 'Category', 'Region',
                'Sales Revenue', 'Cost', 'Profit', 'Quantity Sold'
            ]].copy()
            
            # Add additional columns if they exist
            if 'Profit Margin (%)' in df.columns:
                df_to_insert['profit_margin'] = df['Profit Margin (%)']
            if 'Year' in df.columns:
                df_to_insert['year'] = df['Year']
            if 'Month' in df.columns:
                df_to_insert['month'] = df['Month']
            if 'Quarter' in df.columns:
                df_to_insert['quarter'] = df['Quarter']
            
            # Insert data
            df_to_insert.to_sql('sales_transactions', self.conn, 
                               if_exists='append', index=False)
            
            print(f"✅ Inserted {len(df)} records into database")
            return True
            
        except Exception as e:
            print(f"❌ Error inserting data: {e}")
            return False
    
    def update_summary_tables(self):
        """Update aggregated summary tables"""
        if not self.conn:
            self.connect()
        
        cursor = self.conn.cursor()
        
        # Update product performance
        cursor.execute('''
            INSERT OR REPLACE INTO product_performance 
            (product_name, category, total_revenue, total_profit, 
             total_quantity, avg_profit_margin, last_updated)
            SELECT 
                product_name,
                category,
                SUM(sales_revenue) as total_revenue,
                SUM(profit) as total_profit,
                SUM(quantity_sold) as total_quantity,
                AVG(profit_margin) as avg_profit_margin,
                CURRENT_TIMESTAMP
            FROM sales_transactions
            GROUP BY product_name, category
        ''')
        
        # Update monthly performance
        cursor.execute('''
            INSERT OR REPLACE INTO monthly_performance
            (year, month, region, category, total_revenue, 
             total_profit, total_quantity, created_at)
            SELECT 
                year,
                month,
                region,
                category,
                SUM(sales_revenue) as total_revenue,
                SUM(profit) as total_profit,
                SUM(quantity_sold) as total_quantity,
                CURRENT_TIMESTAMP
            FROM sales_transactions
            WHERE year IS NOT NULL AND month IS NOT NULL
            GROUP BY year, month, region, category
        ''')
        
        self.conn.commit()
        print("✅ Summary tables updated")
    
    def query_data(self, query):
        """Execute custom SQL query and return dataframe"""
        if not self.conn:
            self.connect()
        
        try:
            df = pd.read_sql_query(query, self.conn)
            return df
        except Exception as e:
            print(f"❌ Query error: {e}")
            return None
    
    def get_sales_by_region(self):
        """Get sales data grouped by region"""
        query = '''
            SELECT 
                region,
                SUM(sales_revenue) as total_revenue,
                SUM(profit) as total_profit,
                COUNT(*) as transaction_count,
                AVG(profit_margin) as avg_profit_margin
            FROM sales_transactions
            GROUP BY region
            ORDER BY total_revenue DESC
        '''
        return self.query_data(query)
    
    def get_sales_by_category(self):
        """Get sales data grouped by category"""
        query = '''
            SELECT 
                category,
                COUNT(DISTINCT product_name) as product_count,
                SUM(sales_revenue) as total_revenue,
                SUM(profit) as total_profit,
                SUM(quantity_sold) as total_quantity,
                AVG(profit_margin) as avg_profit_margin
            FROM sales_transactions
            GROUP BY category
            ORDER BY total_revenue DESC
        '''
        return self.query_data(query)
    
    def get_monthly_trends(self):
        """Get monthly sales trends"""
        query = '''
            SELECT 
                year,
                month,
                SUM(sales_revenue) as revenue,
                SUM(profit) as profit,
                SUM(quantity_sold) as quantity,
                AVG(profit_margin) as avg_margin
            FROM sales_transactions
            WHERE year IS NOT NULL AND month IS NOT NULL
            GROUP BY year, month
            ORDER BY year, month
        '''
        return self.query_data(query)
    
    def get_top_products(self, limit=10):
        """Get top performing products"""
        query = f'''
            SELECT 
                product_name,
                category,
                total_revenue,
                total_profit,
                total_quantity,
                avg_profit_margin
            FROM product_performance
            ORDER BY total_revenue DESC
            LIMIT {limit}
        '''
        return self.query_data(query)
    
    def get_bottom_products(self, limit=10):
        """Get worst performing products"""
        query = f'''
            SELECT 
                product_name,
                category,
                total_revenue,
                total_profit,
                total_quantity,
                avg_profit_margin
            FROM product_performance
            ORDER BY total_revenue ASC
            LIMIT {limit}
        '''
        return self.query_data(query)
    
    def get_kpis(self):
        """Get overall KPIs"""
        query = '''
            SELECT 
                COUNT(*) as total_transactions,
                COUNT(DISTINCT product_name) as unique_products,
                COUNT(DISTINCT category) as unique_categories,
                COUNT(DISTINCT region) as unique_regions,
                SUM(sales_revenue) as total_revenue,
                SUM(profit) as total_profit,
                SUM(cost) as total_cost,
                SUM(quantity_sold) as total_quantity,
                AVG(sales_revenue) as avg_order_value,
                AVG(profit_margin) as avg_profit_margin
            FROM sales_transactions
        '''
        return self.query_data(query)
    
    def backup_database(self, backup_path=None):
        """Create database backup"""
        if not backup_path:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = f'backup_sales_analytics_{timestamp}.db'
        
        try:
            import shutil
            shutil.copy2(self.db_path, backup_path)
            print(f"✅ Database backed up to: {backup_path}")
            return True
        except Exception as e:
            print(f"❌ Backup error: {e}")
            return False
    
    def clear_all_data(self):
        """Clear all data from tables (use with caution!)"""
        if not self.conn:
            self.connect()
        
        cursor = self.conn.cursor()
        
        cursor.execute('DELETE FROM sales_transactions')
        cursor.execute('DELETE FROM monthly_performance')
        cursor.execute('DELETE FROM product_performance')
        
        self.conn.commit()
        print("⚠️  All data cleared from database")
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("✅ Database connection closed")


# Example usage
if __name__ == "__main__":
    # Initialize database
    db = DatabaseManager('test_sales.db')
    db.connect()
    db.create_tables()
    
    # Create sample data
    sample_data = {
        'Order Date': pd.date_range('2023-01-01', periods=50, freq='D'),
        'Product Name': ['Laptop'] * 50,
        'Category': ['Electronics'] * 50,
        'Region': ['North'] * 50,
        'Sales Revenue': [1200] * 50,
        'Cost': [900] * 50,
        'Profit': [300] * 50,
        'Quantity Sold': [1] * 50
    }
    
    df = pd.DataFrame(sample_data)
    
    # Insert data
    db.insert_sales_data(df)
    db.update_summary_tables()
    
    # Query data
    print("\nKPIs:")
    print(db.get_kpis())
    
    # Close connection
    db.close()