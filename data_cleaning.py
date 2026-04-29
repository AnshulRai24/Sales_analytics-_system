"""
Data Cleaning Module
Handles missing values, duplicates, and data type corrections
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


class DataCleaner:
    """Comprehensive data cleaning for sales data"""
    
    def __init__(self, df):
        """Initialize with raw dataframe"""
        self.df = df.copy()
        self.cleaning_report = {}
        
    def clean_data(self):
        """Execute full cleaning pipeline"""
        print("🧹 Starting Data Cleaning Process...\n")
        
        self._initial_summary()
        self._handle_missing_values()
        self._remove_duplicates()
        self._fix_data_types()
        self._validate_numeric_columns()
        self._standardize_text_columns()
        self._calculate_derived_fields()
        self._final_validation()
        
        print("\n✅ Data Cleaning Complete!")
        self._print_report()
        
        return self.df
    
    def _initial_summary(self):
        """Display initial data summary"""
        print(f"📊 Initial Data Shape: {self.df.shape}")
        print(f"   Rows: {len(self.df)}, Columns: {len(self.df.columns)}")
        self.cleaning_report['initial_rows'] = len(self.df)
        
    def _handle_missing_values(self):
        """Handle missing values intelligently"""
        print("\n🔍 Handling Missing Values...")
        
        missing_before = self.df.isnull().sum().sum()
        
        # Strategy for each column type
        if 'Order Date' in self.df.columns:
            # Drop rows with missing dates (critical field)
            self.df = self.df.dropna(subset=['Order Date'])
        
        if 'Product Name' in self.df.columns:
            self.df = self.df.dropna(subset=['Product Name'])
        
        # Fill categorical columns with 'Unknown'
        categorical_cols = ['Category', 'Region']
        for col in categorical_cols:
            if col in self.df.columns:
                self.df[col].fillna('Unknown', inplace=True)
        
        # Fill numeric columns with median
        numeric_cols = ['Sales Revenue', 'Cost', 'Profit', 'Quantity Sold']
        for col in numeric_cols:
            if col in self.df.columns:
                self.df[col].fillna(self.df[col].median(), inplace=True)
        
        missing_after = self.df.isnull().sum().sum()
        self.cleaning_report['missing_handled'] = missing_before - missing_after
        print(f"   ✓ Handled {missing_before - missing_after} missing values")
        
    def _remove_duplicates(self):
        """Remove duplicate records"""
        print("\n🗑️  Removing Duplicates...")
        
        duplicates_before = self.df.duplicated().sum()
        self.df = self.df.drop_duplicates()
        duplicates_removed = duplicates_before - self.df.duplicated().sum()
        
        self.cleaning_report['duplicates_removed'] = duplicates_removed
        print(f"   ✓ Removed {duplicates_removed} duplicate rows")
        
    def _fix_data_types(self):
        """Correct data types for each column"""
        print("\n🔧 Fixing Data Types...")
        
        # Convert date column
        if 'Order Date' in self.df.columns:
            self.df['Order Date'] = pd.to_datetime(self.df['Order Date'], errors='coerce')
            # Drop rows with invalid dates
            self.df = self.df.dropna(subset=['Order Date'])
        
        # Convert numeric columns
        numeric_cols = ['Sales Revenue', 'Cost', 'Profit', 'Quantity Sold']
        for col in numeric_cols:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        
        # Convert categorical to string and strip whitespace
        categorical_cols = ['Product Name', 'Category', 'Region']
        for col in categorical_cols:
            if col in self.df.columns:
                self.df[col] = self.df[col].astype(str).str.strip()
        
        print("   ✓ Data types corrected")
        
    def _validate_numeric_columns(self):
        """Validate and clean numeric columns"""
        print("\n✅ Validating Numeric Values...")
        
        # Remove negative values from revenue, cost, quantity
        if 'Sales Revenue' in self.df.columns:
            invalid_revenue = (self.df['Sales Revenue'] < 0).sum()
            self.df = self.df[self.df['Sales Revenue'] >= 0]
            
        if 'Cost' in self.df.columns:
            invalid_cost = (self.df['Cost'] < 0).sum()
            self.df = self.df[self.df['Cost'] >= 0]
            
        if 'Quantity Sold' in self.df.columns:
            invalid_quantity = (self.df['Quantity Sold'] <= 0).sum()
            self.df = self.df[self.df['Quantity Sold'] > 0]
        
        print("   ✓ Removed invalid numeric values")
        
    def _standardize_text_columns(self):
        """Standardize text columns (capitalization, spelling)"""
        print("\n📝 Standardizing Text Fields...")
        
        # Standardize category names
        if 'Category' in self.df.columns:
            self.df['Category'] = self.df['Category'].str.title()
            
        # Standardize region names
        if 'Region' in self.df.columns:
            self.df['Region'] = self.df['Region'].str.title()
            
        # Standardize product names
        if 'Product Name' in self.df.columns:
            self.df['Product Name'] = self.df['Product Name'].str.title()
        
        print("   ✓ Text fields standardized")
        
    def _calculate_derived_fields(self):
        """Calculate derived fields if missing"""
        print("\n🧮 Calculating Derived Fields...")
        
        # Calculate profit if missing
        if 'Profit' not in self.df.columns or self.df['Profit'].isnull().any():
            if 'Sales Revenue' in self.df.columns and 'Cost' in self.df.columns:
                self.df['Profit'] = self.df['Sales Revenue'] - self.df['Cost']
                print("   ✓ Calculated Profit column")
        
        # Add profit margin
        if 'Sales Revenue' in self.df.columns and 'Profit' in self.df.columns:
            self.df['Profit Margin (%)'] = (self.df['Profit'] / self.df['Sales Revenue'] * 100).round(2)
            print("   ✓ Calculated Profit Margin")
        
        # Extract date components
        if 'Order Date' in self.df.columns:
            self.df['Year'] = self.df['Order Date'].dt.year
            self.df['Month'] = self.df['Order Date'].dt.month
            self.df['Quarter'] = self.df['Order Date'].dt.quarter
            self.df['Month Name'] = self.df['Order Date'].dt.month_name()
            print("   ✓ Extracted date components")
    
    def _final_validation(self):
        """Final validation checks"""
        print("\n🔍 Final Validation...")
        
        # Check for any remaining null values in critical columns
        critical_cols = ['Order Date', 'Product Name', 'Sales Revenue', 'Profit']
        null_check = self.df[critical_cols].isnull().sum()
        
        if null_check.sum() > 0:
            print("   ⚠️  Warning: Some critical fields still have null values")
        else:
            print("   ✓ All critical fields validated")
        
        self.cleaning_report['final_rows'] = len(self.df)
        
    def _print_report(self):
        """Print cleaning summary report"""
        print("\n" + "="*50)
        print("📋 CLEANING REPORT")
        print("="*50)
        print(f"Initial Rows:        {self.cleaning_report.get('initial_rows', 0):,}")
        print(f"Final Rows:          {self.cleaning_report.get('final_rows', 0):,}")
        print(f"Rows Removed:        {self.cleaning_report.get('initial_rows', 0) - self.cleaning_report.get('final_rows', 0):,}")
        print(f"Duplicates Removed:  {self.cleaning_report.get('duplicates_removed', 0):,}")
        print(f"Missing Values Fixed: {self.cleaning_report.get('missing_handled', 0):,}")
        print("="*50)
        
    def get_cleaned_data(self):
        """Return cleaned dataframe"""
        return self.df
    
    def save_cleaned_data(self, filepath):
        """Save cleaned data to CSV"""
        self.df.to_csv(filepath, index=False)
        print(f"\n💾 Cleaned data saved to: {filepath}")


# Example usage
if __name__ == "__main__":
    # Sample data for testing
    sample_data = {
        'Order Date': ['2023-01-15', '2023-01-20', None, '2023-02-10'],
        'Product Name': ['Laptop', 'Mouse', 'Keyboard', 'Laptop'],
        'Category': ['Electronics', 'accessories', 'Electronics', 'Electronics'],
        'Region': ['North', 'South', 'East', 'north'],
        'Sales Revenue': [1200, 25, 75, 1200],
        'Cost': [900, 15, 50, 900],
        'Profit': [None, 10, 25, 300],
        'Quantity Sold': [1, 5, 3, 1]
    }
    
    df = pd.DataFrame(sample_data)
    
    # Clean the data
    cleaner = DataCleaner(df)
    cleaned_df = cleaner.clean_data()
    
    print("\n📊 Sample of Cleaned Data:")
    print(cleaned_df.head())