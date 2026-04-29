"""
Data Analysis Module
Performs comprehensive sales analysis and generates insights
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class SalesAnalyzer:
    """Comprehensive sales analysis engine"""
    
    def __init__(self, df):
        """Initialize with cleaned dataframe"""
        self.df = df.copy()
        self.insights = {}
        
    def analyze_all(self):
        """Run complete analysis suite"""
        print("📊 Running Comprehensive Analysis...\n")
        
        self.calculate_kpis()
        self.analyze_by_region()
        self.analyze_by_category()
        self.analyze_trends()
        self.analyze_products()
        
        print("\n✅ Analysis Complete!")
        return self.insights
    
    def calculate_kpis(self):
        """Calculate key performance indicators"""
        print("📈 Calculating KPIs...")
        
        kpis = {
            'total_revenue': self.df['Sales Revenue'].sum(),
            'total_profit': self.df['Profit'].sum(),
            'total_cost': self.df['Cost'].sum(),
            'total_orders': len(self.df),
            'total_quantity': self.df['Quantity Sold'].sum(),
            'avg_order_value': self.df['Sales Revenue'].mean(),
            'overall_profit_margin': (self.df['Profit'].sum() / self.df['Sales Revenue'].sum() * 100),
            'unique_products': self.df['Product Name'].nunique(),
            'unique_categories': self.df['Category'].nunique(),
            'unique_regions': self.df['Region'].nunique()
        }
        
        self.insights['kpis'] = kpis
        print(f"   ✓ Total Revenue: ${kpis['total_revenue']:,.2f}")
        print(f"   ✓ Total Profit: ${kpis['total_profit']:,.2f}")
        print(f"   ✓ Profit Margin: {kpis['overall_profit_margin']:.2f}%")
        
    def analyze_by_region(self):
        """Analyze performance by region"""
        print("\n🗺️  Analyzing Regional Performance...")
        
        region_analysis = self.df.groupby('Region').agg({
            'Sales Revenue': ['sum', 'mean', 'count'],
            'Profit': 'sum',
            'Quantity Sold': 'sum'
        }).round(2)
        
        region_analysis.columns = ['Total Revenue', 'Avg Revenue', 'Orders', 'Total Profit', 'Quantity']
        region_analysis['Profit Margin (%)'] = (
            region_analysis['Total Profit'] / region_analysis['Total Revenue'] * 100
        ).round(2)
        
        region_analysis = region_analysis.sort_values('Total Revenue', ascending=False)
        
        # Calculate regional contribution
        region_analysis['Revenue Contribution (%)'] = (
            region_analysis['Total Revenue'] / region_analysis['Total Revenue'].sum() * 100
        ).round(2)
        
        self.insights['region_analysis'] = region_analysis
        
        # Identify best and worst regions
        best_region = region_analysis.index[0]
        worst_region = region_analysis.index[-1]
        
        self.insights['best_region'] = best_region
        self.insights['worst_region'] = worst_region
        
        print(f"   ✓ Best Region: {best_region}")
        print(f"   ✓ Worst Region: {worst_region}")
        
    def analyze_by_category(self):
        """Analyze performance by product category"""
        print("\n📦 Analyzing Category Performance...")
        
        category_analysis = self.df.groupby('Category').agg({
            'Sales Revenue': 'sum',
            'Profit': 'sum',
            'Quantity Sold': 'sum',
            'Product Name': 'nunique'
        }).round(2)
        
        category_analysis.columns = ['Total Revenue', 'Total Profit', 'Quantity', 'Product Count']
        category_analysis['Profit Margin (%)'] = (
            category_analysis['Total Profit'] / category_analysis['Total Revenue'] * 100
        ).round(2)
        
        category_analysis = category_analysis.sort_values('Total Revenue', ascending=False)
        
        # Calculate category contribution
        category_analysis['Revenue Contribution (%)'] = (
            category_analysis['Total Revenue'] / category_analysis['Total Revenue'].sum() * 100
        ).round(2)
        
        self.insights['category_analysis'] = category_analysis
        
        # Identify top and bottom categories
        top_category = category_analysis.index[0]
        bottom_category = category_analysis.index[-1]
        
        self.insights['top_category'] = top_category
        self.insights['bottom_category'] = bottom_category
        
        print(f"   ✓ Top Category: {top_category}")
        print(f"   ✓ Bottom Category: {bottom_category}")
        
    def analyze_trends(self):
        """Analyze monthly and yearly trends"""
        print("\n📅 Analyzing Time-Based Trends...")
        
        # Monthly trend
        monthly_trend = self.df.groupby(['Year', 'Month']).agg({
            'Sales Revenue': 'sum',
            'Profit': 'sum',
            'Quantity Sold': 'sum'
        }).round(2)
        
        monthly_trend['Profit Margin (%)'] = (
            monthly_trend['Profit'] / monthly_trend['Sales Revenue'] * 100
        ).round(2)
        
        self.insights['monthly_trend'] = monthly_trend
        
        # Calculate growth metrics
        revenue_trend = monthly_trend['Sales Revenue'].values
        if len(revenue_trend) > 1:
            revenue_growth = ((revenue_trend[-1] - revenue_trend[0]) / revenue_trend[0] * 100)
            self.insights['revenue_growth'] = revenue_growth
            print(f"   ✓ Revenue Growth: {revenue_growth:.2f}%")
        
        # Quarterly analysis
        quarterly_trend = self.df.groupby(['Year', 'Quarter']).agg({
            'Sales Revenue': 'sum',
            'Profit': 'sum'
        }).round(2)
        
        self.insights['quarterly_trend'] = quarterly_trend
        
        # Month-over-month analysis
        mom_analysis = self._calculate_mom_growth(monthly_trend)
        self.insights['mom_growth'] = mom_analysis
        
    def _calculate_mom_growth(self, monthly_data):
        """Calculate month-over-month growth"""
        revenue_list = monthly_data['Sales Revenue'].tolist()
        mom_growth = []
        
        for i in range(1, len(revenue_list)):
            growth = ((revenue_list[i] - revenue_list[i-1]) / revenue_list[i-1] * 100)
            mom_growth.append(growth)
        
        avg_mom_growth = np.mean(mom_growth) if mom_growth else 0
        return {
            'growth_rates': mom_growth,
            'avg_growth': avg_mom_growth
        }
    
    def analyze_products(self):
        """Analyze product performance"""
        print("\n🏆 Analyzing Product Performance...")
        
        product_analysis = self.df.groupby('Product Name').agg({
            'Sales Revenue': 'sum',
            'Profit': 'sum',
            'Quantity Sold': 'sum',
            'Order Date': 'count'
        }).round(2)
        
        product_analysis.columns = ['Total Revenue', 'Total Profit', 'Quantity', 'Orders']
        product_analysis['Profit Margin (%)'] = (
            product_analysis['Total Profit'] / product_analysis['Total Revenue'] * 100
        ).round(2)
        
        # Sort by revenue
        product_analysis = product_analysis.sort_values('Total Revenue', ascending=False)
        
        # Top 10 products
        top_10_products = product_analysis.head(10)
        self.insights['top_10_products'] = top_10_products
        
        # Bottom 10 products
        bottom_10_products = product_analysis.tail(10)
        self.insights['bottom_10_products'] = bottom_10_products
        
        print(f"   ✓ Top Product: {top_10_products.index[0]}")
        print(f"   ✓ Total Products Analyzed: {len(product_analysis)}")
        
    def get_insights(self):
        """Return all insights"""
        return self.insights
    
    def get_summary_report(self):
        """Generate executive summary"""
        kpis = self.insights.get('kpis', {})
        
        summary = f"""
╔══════════════════════════════════════════════════════════════╗
║              SALES PERFORMANCE EXECUTIVE SUMMARY              ║
╚══════════════════════════════════════════════════════════════╝

📊 KEY METRICS
├─ Total Revenue:        ${kpis.get('total_revenue', 0):,.2f}
├─ Total Profit:         ${kpis.get('total_profit', 0):,.2f}
├─ Total Cost:           ${kpis.get('total_cost', 0):,.2f}
├─ Profit Margin:        {kpis.get('overall_profit_margin', 0):.2f}%
├─ Total Orders:         {kpis.get('total_orders', 0):,}
└─ Avg Order Value:      ${kpis.get('avg_order_value', 0):,.2f}

🏆 TOP PERFORMERS
├─ Best Region:          {self.insights.get('best_region', 'N/A')}
├─ Top Category:         {self.insights.get('top_category', 'N/A')}
└─ Unique Products:      {kpis.get('unique_products', 0)}

📈 GROWTH
└─ Revenue Growth:       {self.insights.get('revenue_growth', 0):.2f}%
"""
        return summary


# Example usage
if __name__ == "__main__":
    # Load sample data
    sample_data = {
        'Order Date': pd.date_range('2023-01-01', periods=100, freq='D'),
        'Product Name': np.random.choice(['Laptop', 'Mouse', 'Keyboard', 'Monitor'], 100),
        'Category': np.random.choice(['Electronics', 'Accessories'], 100),
        'Region': np.random.choice(['North', 'South', 'East', 'West'], 100),
        'Sales Revenue': np.random.uniform(100, 2000, 100),
        'Cost': np.random.uniform(50, 1500, 100),
        'Quantity Sold': np.random.randint(1, 10, 100)
    }
    
    df = pd.DataFrame(sample_data)
    df['Profit'] = df['Sales Revenue'] - df['Cost']
    df['Year'] = df['Order Date'].dt.year
    df['Month'] = df['Order Date'].dt.month
    df['Quarter'] = df['Order Date'].dt.quarter
    
    # Analyze
    analyzer = SalesAnalyzer(df)
    insights = analyzer.analyze_all()
    
    print(analyzer.get_summary_report())