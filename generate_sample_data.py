"""
Sample Sales Data Generator
Creates realistic sales data for testing and demonstration
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


def generate_sales_data(n_records=5000, start_date='2023-01-01', end_date='2024-12-31'):
    """
    Generate realistic sales data
    
    Args:
        n_records: Number of records to generate
        start_date: Start date for transactions
        end_date: End date for transactions
    
    Returns:
        DataFrame with sales data
    """
    
    print(f"🎲 Generating {n_records} sales records...")
    
    # Set random seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    # Define product catalog
    product_catalog = {
        'Electronics': {
            'Laptop Pro 15': {'price_range': (1200, 2500), 'cost_ratio': (0.65, 0.75)},
            'Laptop Pro 13': {'price_range': (900, 1800), 'cost_ratio': (0.65, 0.75)},
            'Wireless Mouse': {'price_range': (25, 80), 'cost_ratio': (0.50, 0.60)},
            'Mechanical Keyboard': {'price_range': (80, 200), 'cost_ratio': (0.55, 0.65)},
            '4K Monitor 27"': {'price_range': (300, 800), 'cost_ratio': (0.70, 0.80)},
            'USB-C Hub': {'price_range': (30, 100), 'cost_ratio': (0.45, 0.55)},
            'Webcam HD': {'price_range': (50, 150), 'cost_ratio': (0.50, 0.60)},
            'External SSD 1TB': {'price_range': (100, 250), 'cost_ratio': (0.60, 0.70)},
            'Wireless Headset': {'price_range': (80, 300), 'cost_ratio': (0.55, 0.65)},
            'Portable Charger': {'price_range': (30, 80), 'cost_ratio': (0.45, 0.55)}
        },
        'Accessories': {
            'Laptop Bag Premium': {'price_range': (40, 120), 'cost_ratio': (0.50, 0.60)},
            'Screen Protector': {'price_range': (15, 40), 'cost_ratio': (0.30, 0.45)},
            'Cable Organizer': {'price_range': (10, 30), 'cost_ratio': (0.35, 0.45)},
            'Desk Mat XXL': {'price_range': (25, 60), 'cost_ratio': (0.40, 0.50)},
            'Phone Stand': {'price_range': (15, 45), 'cost_ratio': (0.35, 0.45)},
            'Laptop Stand': {'price_range': (30, 80), 'cost_ratio': (0.45, 0.55)},
            'Cable Set': {'price_range': (20, 50), 'cost_ratio': (0.40, 0.50)},
            'Cleaning Kit': {'price_range': (15, 35), 'cost_ratio': (0.30, 0.40)}
        },
        'Software': {
            'Office Suite Pro': {'price_range': (150, 300), 'cost_ratio': (0.20, 0.35)},
            'Antivirus Premium': {'price_range': (50, 100), 'cost_ratio': (0.15, 0.30)},
            'Photo Editor Pro': {'price_range': (100, 250), 'cost_ratio': (0.25, 0.40)},
            'VPN Service Annual': {'price_range': (60, 120), 'cost_ratio': (0.20, 0.35)},
            'Cloud Storage 2TB': {'price_range': (100, 200), 'cost_ratio': (0.25, 0.40)},
            'Video Editor': {'price_range': (150, 400), 'cost_ratio': (0.30, 0.45)},
            'Project Manager': {'price_range': (80, 180), 'cost_ratio': (0.20, 0.35)}
        },
        'Furniture': {
            'Ergonomic Chair': {'price_range': (200, 600), 'cost_ratio': (0.55, 0.68)},
            'Standing Desk Electric': {'price_range': (400, 1200), 'cost_ratio': (0.60, 0.72)},
            'Monitor Arm Dual': {'price_range': (80, 200), 'cost_ratio': (0.50, 0.62)},
            'Desk Lamp LED': {'price_range': (40, 120), 'cost_ratio': (0.45, 0.58)},
            'Cable Tray': {'price_range': (20, 50), 'cost_ratio': (0.40, 0.52)},
            'Footrest': {'price_range': (30, 80), 'cost_ratio': (0.42, 0.55)},
            'Desk Organizer': {'price_range': (25, 70), 'cost_ratio': (0.40, 0.52)}
        }
    }
    
    # Regions with different performance characteristics
    regions = {
        'North': 1.2,      # 20% above average
        'South': 0.9,      # 10% below average
        'East': 1.1,       # 10% above average
        'West': 1.05,      # 5% above average
        'Central': 0.95    # 5% below average
    }
    
    # Generate date range
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    date_range = [start + timedelta(days=x) for x in range((end - start).days + 1)]
    
    # Generate records
    records = []
    
    for i in range(n_records):
        # Select random category and product
        category = random.choice(list(product_catalog.keys()))
        product_name = random.choice(list(product_catalog[category].keys()))
        product_info = product_catalog[category][product_name]
        
        # Select region
        region = random.choice(list(regions.keys()))
        region_multiplier = regions[region]
        
        # Generate date with seasonal pattern
        date = random.choice(date_range)
        month = date.month
        
        # Seasonal multiplier (higher sales in Nov-Dec, lower in Jan-Feb)
        if month in [11, 12]:
            seasonal_multiplier = 1.3
        elif month in [1, 2]:
            seasonal_multiplier = 0.8
        else:
            seasonal_multiplier = 1.0
        
        # Calculate price with variations
        base_price = random.uniform(*product_info['price_range'])
        price = base_price * region_multiplier * seasonal_multiplier
        
        # Calculate cost
        cost_ratio = random.uniform(*product_info['cost_ratio'])
        cost = price * cost_ratio
        
        # Calculate profit
        profit = price - cost
        
        # Quantity (more for cheaper items)
        if price < 100:
            quantity = random.randint(1, 8)
        elif price < 500:
            quantity = random.randint(1, 4)
        else:
            quantity = random.randint(1, 2)
        
        # Adjust for bulk orders
        sales_revenue = round(price * quantity, 2)
        total_cost = round(cost * quantity, 2)
        total_profit = round(profit * quantity, 2)
        
        # Create record
        record = {
            'Order Date': date.strftime('%Y-%m-%d'),
            'Product Name': product_name,
            'Category': category,
            'Region': region,
            'Sales Revenue': sales_revenue,
            'Cost': total_cost,
            'Profit': total_profit,
            'Quantity Sold': quantity
        }
        
        records.append(record)
        
        # Progress indicator
        if (i + 1) % 1000 == 0:
            print(f"   Generated {i + 1}/{n_records} records...")
    
    # Create DataFrame
    df = pd.DataFrame(records)
    
    # Add some missing values (2-3% missing)
    missing_indices = random.sample(range(len(df)), int(len(df) * 0.02))
    for idx in missing_indices[:len(missing_indices)//3]:
        df.loc[idx, 'Category'] = None
    for idx in missing_indices[len(missing_indices)//3:2*len(missing_indices)//3]:
        df.loc[idx, 'Region'] = None
    
    # Add some duplicates (1%)
    duplicate_indices = random.sample(range(len(df)), int(len(df) * 0.01))
    duplicates = df.iloc[duplicate_indices].copy()
    df = pd.concat([df, duplicates], ignore_index=True)
    
    # Add some incorrect data types (convert some to strings)
    string_indices = random.sample(range(len(df)), min(50, int(len(df) * 0.01)))
    for idx in string_indices:
        df.loc[idx, 'Sales Revenue'] = str(df.loc[idx, 'Sales Revenue'])
    
    print(f"\n✅ Generated {len(df)} records (including {len(duplicates)} duplicates)")
    print(f"📊 Data Summary:")
    print(f"   - Date Range: {df['Order Date'].min()} to {df['Order Date'].max()}")
    print(f"   - Categories: {df['Category'].nunique()} unique")
    print(f"   - Products: {df['Product Name'].nunique()} unique")
    print(f"   - Regions: {df['Region'].nunique()} unique")
    print(f"   - Total Revenue: ${df['Sales Revenue'].sum():,.2f}")
    
    return df


def save_sample_data(df, filepath='data/raw/sales_data.csv'):
    """Save generated data to CSV"""
    import os
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Save to CSV
    df.to_csv(filepath, index=False)
    print(f"\n💾 Data saved to: {filepath}")


if __name__ == "__main__":
    # Generate sample data
    print("="*60)
    print("SALES DATA GENERATOR")
    print("="*60)
    
    # Generate 5000 records covering 2 years
    df = generate_sales_data(
        n_records=5000,
        start_date='2023-01-01',
        end_date='2024-12-31'
    )
    
    # Save to file
    save_sample_data(df)
    
    print("\n" + "="*60)
    print("Sample records:")
    print(df.head(10))
    print("="*60)