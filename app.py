"""
Sales Performance Analysis Dashboard
Modern Streamlit Application with Interactive Visualizations
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import custom modules
try:
    from data_cleaning import DataCleaner
    from data_analysis import SalesAnalyzer
    from insights_generator import InsightsGenerator
    from database import DatabaseManager
except:
    pass  # Will use standalone mode


# Page configuration
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: black;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin: 10px 0;
    }
    h1 {
        color: #1e3a8a;
        font-weight: 700;
    }
    h2 {
        color: #2563eb;
        font-weight: 600;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)


def load_data():
    """Load and cache data"""
    if 'df' not in st.session_state:
        if os.path.exists('data/processed/cleaned_sales_data.csv'):
            df = pd.read_csv('data/processed/cleaned_sales_data.csv')
            df['Order Date'] = pd.to_datetime(df['Order Date'])
        else:
            df = generate_sample_data()
        st.session_state.df = df
    return st.session_state.df


def generate_sample_data(n_records=1000):
    """Generate realistic sample sales data"""
    np.random.seed(42)
    
    start_date = datetime(2023, 1, 1)
    dates = [start_date + timedelta(days=x) for x in range(365)]
    
    products = {
        'Electronics': ['Laptop Pro', 'Wireless Mouse', 'USB-C Hub', '4K Monitor', 'Mechanical Keyboard'],
        'Accessories': ['Laptop Bag', 'Screen Protector', 'Cable Organizer', 'Desk Mat', 'Webcam'],
        'Software': ['Office Suite', 'Antivirus Premium', 'Photo Editor', 'VPN Service', 'Cloud Storage'],
        'Furniture': ['Ergonomic Chair', 'Standing Desk', 'Monitor Arm', 'Desk Lamp', 'Cable Tray']
    }
    
    regions = ['North', 'South', 'East', 'West', 'Central']
    
    data = []
    for _ in range(n_records):
        category = np.random.choice(list(products.keys()))
        product = np.random.choice(products[category])
        region = np.random.choice(regions)
        date = np.random.choice(dates)
        
        if category == 'Electronics':
            revenue = np.random.uniform(200, 2500)
            cost_ratio = np.random.uniform(0.6, 0.75)
        elif category == 'Furniture':
            revenue = np.random.uniform(150, 1200)
            cost_ratio = np.random.uniform(0.55, 0.70)
        elif category == 'Software':
            revenue = np.random.uniform(50, 500)
            cost_ratio = np.random.uniform(0.30, 0.50)
        else:
            revenue = np.random.uniform(20, 300)
            cost_ratio = np.random.uniform(0.50, 0.65)
        
        cost = revenue * cost_ratio
        profit = revenue - cost
        quantity = np.random.randint(1, 10)
        
        data.append({
            'Order Date': date,
            'Product Name': product,
            'Category': category,
            'Region': region,
            'Sales Revenue': round(revenue, 2),
            'Cost': round(cost, 2),
            'Profit': round(profit, 2),
            'Quantity Sold': quantity,
            'Profit Margin (%)': round((profit/revenue)*100, 2),
            'Year': date.year,
            'Month': date.month,
            'Quarter': (date.month-1)//3 + 1,
            'Month Name': date.strftime('%B')
        })
    
    return pd.DataFrame(data)


def clean_dataframe(df):
    """Clean and prepare dataframe for analysis"""
    df = df.copy()
    
    # Clean Region column
    if 'Region' in df.columns:
        df['Region'] = df['Region'].fillna('Unknown')
        df['Region'] = df['Region'].astype(str).str.strip()
        df['Region'] = df['Region'].replace(['nan', 'None', ''], 'Unknown')
    
    # Clean Category column
    if 'Category' in df.columns:
        df['Category'] = df['Category'].fillna('Uncategorized')
        df['Category'] = df['Category'].astype(str).str.strip()
        df['Category'] = df['Category'].replace(['nan', 'None', ''], 'Uncategorized')
    
    # Clean Product Name column
    if 'Product Name' in df.columns:
        df['Product Name'] = df['Product Name'].fillna('Unknown Product')
        df['Product Name'] = df['Product Name'].astype(str).str.strip()
        df['Product Name'] = df['Product Name'].replace(['nan', 'None', ''], 'Unknown Product')
    
    # Ensure numeric columns are numeric
    numeric_cols = ['Sales Revenue', 'Cost', 'Profit', 'Quantity Sold', 'Profit Margin (%)']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    return df


def display_kpi_cards(kpis):
    """Display KPI metrics in cards"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Total Revenue",
            value=f"${kpis['total_revenue']:,.0f}",
            delta=f"{kpis.get('revenue_growth', 0):.1f}% growth"
        )
    
    with col2:
        st.metric(
            label="📈 Total Profit",
            value=f"${kpis['total_profit']:,.0f}",
            delta=f"{kpis['overall_profit_margin']:.1f}% margin"
        )
    
    with col3:
        st.metric(
            label="🛒 Total Orders",
            value=f"{kpis['total_orders']:,}",
            delta=f"${kpis['avg_order_value']:.0f} avg"
        )
    
    with col4:
        st.metric(
            label="📦 Products Sold",
            value=f"{kpis['total_quantity']:,}",
            delta=f"{kpis['unique_products']} unique"
        )


def plot_revenue_trend(df):
    """Plot revenue trend over time"""
    monthly_data = df.groupby(df['Order Date'].dt.to_period('M')).agg({
        'Sales Revenue': 'sum',
        'Profit': 'sum'
    }).reset_index()
    
    monthly_data['Order Date'] = monthly_data['Order Date'].astype(str)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=monthly_data['Order Date'],
        y=monthly_data['Sales Revenue'],
        mode='lines+markers',
        name='Revenue',
        line=dict(color='#3b82f6', width=3),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=monthly_data['Order Date'],
        y=monthly_data['Profit'],
        mode='lines+markers',
        name='Profit',
        line=dict(color='#10b981', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title='Monthly Revenue & Profit Trend',
        xaxis_title='Month',
        yaxis_title='Amount ($)',
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    
    return fig


def plot_regional_performance(df):
    """Plot regional performance"""
    region_data = df.groupby('Region').agg({
        'Sales Revenue': 'sum',
        'Profit': 'sum'
    }).reset_index()
    
    fig = px.bar(
        region_data,
        x='Region',
        y='Sales Revenue',
        text='Sales Revenue',
        color='Profit',
        color_continuous_scale='Blues',
        title='Regional Sales Performance'
    )
    
    fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    fig.update_layout(height=400, template='plotly_white')
    
    return fig


def plot_category_distribution(df):
    """Plot category distribution"""
    category_data = df.groupby('Category')['Sales Revenue'].sum().reset_index()
    
    fig = px.pie(
        category_data,
        values='Sales Revenue',
        names='Category',
        title='Revenue Distribution by Category',
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400)
    
    return fig


def plot_top_products(df, top_n=10):
    """Plot top products by revenue"""
    product_data = df.groupby('Product Name')['Sales Revenue'].sum().nlargest(top_n).reset_index()
    
    fig = px.bar(
        product_data,
        x='Sales Revenue',
        y='Product Name',
        orientation='h',
        title=f'Top {top_n} Products by Revenue',
        color='Sales Revenue',
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(height=400, template='plotly_white', showlegend=False)
    
    return fig


def display_recommendations(recommendations):
    """Display business recommendations"""
    if not recommendations:
        st.info("No specific recommendations at this time.")
        return
    
    severity_order = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}
    sorted_recs = sorted(recommendations, key=lambda x: severity_order.get(x.get('severity', 'Low'), 3))
    
    for rec in sorted_recs[:10]:
        severity = rec.get('severity', 'Low')
        
        if severity == 'Critical':
            color = '🔴'
        elif severity == 'High':
            color = '🟠'
        elif severity == 'Medium':
            color = '🟡'
        else:
            color = '🟢'
        
        with st.expander(f"{color} [{severity}] {rec.get('type', 'Recommendation')}"):
            st.write(f"**Issue:** {rec.get('issue', 'N/A')}")
            st.write(f"**Recommended Action:** {rec.get('action', 'N/A')}")
            st.write(f"**Expected Impact:** {rec.get('expected_impact', 'N/A')}")


def main():
    """Main application"""
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/200x80/3b82f6/ffffff?text=Sales+Analytics", use_container_width=True)
        st.title("🎛️ Controls")
        
        uploaded_file = st.file_uploader("Upload Sales Data (CSV)", type=['csv'])
        
        if uploaded_file:
            try:
                encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252', 'utf-16']
                df = None
                
                for encoding in encodings:
                    try:
                        uploaded_file.seek(0)
                        df = pd.read_csv(uploaded_file, encoding=encoding)
                        break
                    except:
                        continue
                
                if df is None:
                    raise Exception("Could not read file with any encoding")
                
                column_mapping = {}
                
                column_patterns = {
                    'Order Date': ['order date', 'date', 'order_date', 'orderdate', 'transaction date', 
                                  'trans_date', 'sale_date', 'purchase_date', 'invoice_date'],
                    'Product Name': ['product name', 'product', 'product_name', 'item', 'item name',
                                    'productcode', 'product_code', 'sku', 'item_name', 'product_description'],
                    'Category': ['category', 'type', 'product category', 'product_type', 'productline',
                                'product_line', 'product line', 'line', 'department', 'class'],
                    'Region': ['region', 'location', 'area', 'territory', 'zone', 'country', 'state',
                              'city', 'market', 'district'],
                    'Sales Revenue': ['sales revenue', 'revenue', 'sales', 'amount', 'total', 'total_sales',
                                     'total_amount', 'sale_amount', 'gross_sales', 'net_sales'],
                    'Cost': ['cost', 'expense', 'cogs', 'cost price', 'unit_cost', 'product_cost',
                            'total_cost', 'cost_price', 'purchase_price'],
                    'Profit': ['profit', 'net profit', 'margin amount', 'gross_profit', 'net_profit',
                              'profit_amount', 'margin'],
                    'Quantity Sold': ['quantity sold', 'quantity', 'qty', 'units', 'units sold',
                                     'quantityordered', 'quantity_ordered', 'order_quantity', 'qty_sold',
                                     'units_sold', 'volume']
                }
                
                df_cols_lower = {col.lower().replace('_', ' ').replace('-', ' '): col for col in df.columns}
                
                for required_col, variations in column_patterns.items():
                    found = False
                    for variation in variations:
                        normalized_variation = variation.lower().replace('_', ' ').replace('-', ' ')
                        if normalized_variation in df_cols_lower:
                            column_mapping[df_cols_lower[normalized_variation]] = required_col
                            found = True
                            break
                    if not found and required_col in df.columns:
                        column_mapping[required_col] = required_col
                
                if column_mapping:
                    df = df.rename(columns=column_mapping)
                    st.info(f"🔄 Mapped {len(column_mapping)} columns automatically")
                
                calculated_cols = []
                
                has_quantity = 'Quantity Sold' in df.columns
                has_revenue = 'Sales Revenue' in df.columns
                has_cost = 'Cost' in df.columns
                has_profit = 'Profit' in df.columns
                
                if not has_revenue and has_quantity:
                    price_col = None
                    for col in df.columns:
                        if col.lower() in ['priceeach', 'price each', 'unit price', 'price', 'unitprice']:
                            price_col = col
                            break
                    if price_col:
                        df['Sales Revenue'] = df['Quantity Sold'] * pd.to_numeric(df[price_col], errors='coerce')
                        calculated_cols.append('Sales Revenue')
                        has_revenue = True
                
                if not has_cost and has_revenue:
                    df['Cost'] = df['Sales Revenue'] * 0.65
                    calculated_cols.append('Cost (estimated at 65% of revenue)')
                    has_cost = True
                
                if not has_profit and has_revenue and has_cost:
                    df['Profit'] = df['Sales Revenue'] - df['Cost']
                    calculated_cols.append('Profit')
                    has_profit = True
                
                if 'Product Name' not in df.columns:
                    product_col = None
                    for col in df.columns:
                        if col.lower() in ['productcode', 'product_code', 'sku', 'item_code']:
                            product_col = col
                            break
                    if product_col:
                        df['Product Name'] = df[product_col].astype(str)
                        calculated_cols.append('Product Name (from product code)')
                    else:
                        df['Product Name'] = 'Product'
                        calculated_cols.append('Product Name (generic)')
                
                if 'Category' not in df.columns:
                    cat_col = None
                    for col in df.columns:
                        if col.lower() in ['productline', 'product_line', 'product line', 'line', 'dealsize', 'deal_size']:
                            cat_col = col
                            break
                    if cat_col:
                        df['Category'] = df[cat_col].astype(str)
                        calculated_cols.append('Category (from product line)')
                    else:
                        df['Category'] = 'General'
                        calculated_cols.append('Category (generic)')
                
                if 'Region' not in df.columns:
                    df['Region'] = 'Unknown'
                    calculated_cols.append('Region (set to Unknown)')
                
                critical_cols = ['Order Date', 'Sales Revenue', 'Quantity Sold']
                truly_missing = [col for col in critical_cols if col not in df.columns]
                
                if calculated_cols:
                    st.success(f"✨ Auto-calculated/mapped: {', '.join(calculated_cols)}")
                
                if truly_missing:
                    st.warning(f"⚠️ Could not auto-detect: {', '.join(truly_missing)}")
                    
                    st.subheader("🎯 Manual Column Mapping")
                    st.write("Help us map your columns to the required format:")
                    
                    with st.form("column_mapper"):
                        available_cols = ['-- Not Available --'] + [col for col in df.columns if col not in column_mapping.values()]
                        user_mapping = {}
                        
                        for missing_col in truly_missing:
                            selected = st.selectbox(
                                f"Which column is '{missing_col}'?",
                                available_cols,
                                key=f"map_{missing_col}"
                            )
                            if selected != '-- Not Available --':
                                user_mapping[selected] = missing_col
                        
                        if st.form_submit_button("Apply Mapping"):
                            if user_mapping:
                                df = df.rename(columns=user_mapping)
                                st.session_state.df = clean_dataframe(df)
                                st.success("✅ Columns mapped! Please refresh to see your data.")
                                st.rerun()
                    
                    with st.expander("🔍 Your Current CSV Structure", expanded=False):
                        st.write("**Your columns:**")
                        st.write(list(df.columns))
                        st.write("\n**First 5 rows:**")
                        st.dataframe(df.head())
                    
                    df = generate_sample_data()
                    st.info("📊 Using sample data for now. Map your columns above to use your data.")
                    
                else:
                    try:
                        df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
                        invalid_dates = df['Order Date'].isnull().sum()
                        if invalid_dates > 0:
                            st.warning(f"⚠️ {invalid_dates} rows have invalid dates and will be removed")
                            df = df.dropna(subset=['Order Date'])
                    except Exception as e:
                        st.error(f"❌ Error parsing dates: {e}")
                        df = generate_sample_data()
                        st.warning("⚠️ Using sample data instead.")
                    
                    numeric_cols = ['Sales Revenue', 'Cost', 'Profit', 'Quantity Sold']
                    for col in numeric_cols:
                        if col in df.columns:
                            df[col] = pd.to_numeric(df[col], errors='coerce')
                    
                    df[numeric_cols] = df[numeric_cols].fillna(0)
                    
                    if 'Profit Margin (%)' not in df.columns:
                        df['Profit Margin (%)'] = (df['Profit'] / df['Sales Revenue'] * 100).replace([np.inf, -np.inf], 0).fillna(0).round(2)
                    
                    df['Year'] = df['Order Date'].dt.year
                    df['Month'] = df['Order Date'].dt.month
                    df['Quarter'] = df['Order Date'].dt.quarter
                    df['Month Name'] = df['Order Date'].dt.month_name()
                    
                    df = clean_dataframe(df)
                    st.session_state.df = df
                    
                    st.success(f"✅ Data uploaded and processed successfully!")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("📊 Total Records", f"{len(df):,}")
                        st.metric("📅 Date Range", f"{df['Order Date'].min().date()} to {df['Order Date'].max().date()}")
                    with col2:
                        st.metric("🏷️ Unique Products", f"{df['Product Name'].nunique():,}")
                        st.metric("📦 Categories", f"{df['Category'].nunique()}")
                    
                    if calculated_cols:
                        with st.expander("ℹ️ Auto-Generated Fields"):
                            for calc in calculated_cols:
                                st.write(f"• {calc}")
                    
                    if column_mapping:
                        with st.expander("🔄 Column Mappings Applied"):
                            for old_col, new_col in column_mapping.items():
                                st.write(f"• `{old_col}` → `{new_col}`")
                    
            except Exception as e:
                st.error(f"❌ Error loading file: {str(e)}")
                
                with st.expander("🔍 Troubleshooting Help", expanded=True):
                    st.write("**Common issues and solutions:**")
                    st.write("""
                    1. **Encoding issues**: Save your CSV as UTF-8 in Excel
                    2. **Missing columns**: Ensure you have Order Date, Product Name, etc.
                    3. **Special characters**: Remove é, ñ, ™, etc.
                    4. **Wrong delimiter**: Use comma (,) not semicolon (;)
                    5. **Date format**: Use YYYY-MM-DD or MM/DD/YYYY
                    """)
                    
                    st.write("\n**Example CSV structure:**")
                    st.code("""Order Date,Product Name,Category,Region,Sales Revenue,Cost,Profit,Quantity Sold
2024-01-01,Laptop,Electronics,North,1200,800,400,1
2024-01-02,Mouse,Accessories,South,50,30,20,2""")
                
                st.warning("⚠️ Using sample data instead. Please fix your CSV and try again.")
                st.session_state.df = generate_sample_data()
        
        st.subheader("📊 Filters")
        
        df = load_data()
        df = clean_dataframe(df)
        
        date_range = st.date_input(
            "Date Range",
            value=(df['Order Date'].min(), df['Order Date'].max()),
            min_value=df['Order Date'].min(),
            max_value=df['Order Date'].max()
        )
        
        unique_regions = df['Region'].dropna().astype(str).unique().tolist()
        regions = ['All'] + sorted([r for r in unique_regions if r and r.lower() not in ['nan', 'none', '']])
        selected_region = st.selectbox("Region", regions)
        
        unique_categories = df['Category'].dropna().astype(str).unique().tolist()
        categories = ['All'] + sorted([c for c in unique_categories if c and c.lower() not in ['nan', 'none', '']])
        selected_category = st.selectbox("Category", categories)
        
        filtered_df = df.copy()
        
        if len(date_range) == 2:
            filtered_df = filtered_df[
                (filtered_df['Order Date'] >= pd.Timestamp(date_range[0])) &
                (filtered_df['Order Date'] <= pd.Timestamp(date_range[1]))
            ]
        
        if selected_region != 'All':
            filtered_df = filtered_df[filtered_df['Region'] == selected_region]
        
        if selected_category != 'All':
            filtered_df = filtered_df[filtered_df['Category'] == selected_category]
        
        st.session_state.filtered_df = filtered_df
        
        st.subheader("⚡ Actions")
        if st.button("🔄 Refresh Analysis", use_container_width=True):
            st.rerun()
        
        if st.button("💾 Export Report", use_container_width=True):
            st.download_button(
                label="Download CSV",
                data=filtered_df.to_csv(index=False),
                file_name=f"sales_report_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    st.title("📊 Sales Performance Analysis Dashboard")
    st.markdown("### Real-time Business Intelligence & Insights")
    
    filtered_df = st.session_state.get('filtered_df', df)
    
    total_revenue = filtered_df['Sales Revenue'].sum()
    kpis = {
        'total_revenue': total_revenue,
        'total_profit': filtered_df['Profit'].sum(),
        'total_cost': filtered_df['Cost'].sum(),
        'total_orders': len(filtered_df),
        'total_quantity': filtered_df['Quantity Sold'].sum(),
        'avg_order_value': filtered_df['Sales Revenue'].mean(),
        'overall_profit_margin': (filtered_df['Profit'].sum() / total_revenue * 100) if total_revenue > 0 else 0,
        'unique_products': filtered_df['Product Name'].nunique(),
        'revenue_growth': 8.5
    }
    
    display_kpi_cards(kpis)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(plot_revenue_trend(filtered_df), use_container_width=True)
    
    with col2:
        st.plotly_chart(plot_regional_performance(filtered_df), use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.plotly_chart(plot_category_distribution(filtered_df), use_container_width=True)
    
    with col4:
        st.plotly_chart(plot_top_products(filtered_df), use_container_width=True)
    
    st.markdown("---")
    
    st.header("💡 Business Insights & Recommendations")
    
    try:
        analyzer = SalesAnalyzer(filtered_df)
        analysis_results = analyzer.analyze_all()
        insights_gen = InsightsGenerator(filtered_df, analysis_results)
        recommendations = insights_gen.generate_all_insights()
        display_recommendations(recommendations)
    except:
        st.info("📊 Basic analysis mode. Install custom modules for advanced insights.")
        
        basic_insights = []
        
        top_region = filtered_df.groupby('Region')['Sales Revenue'].sum().idxmax()
        top_region_revenue = filtered_df.groupby('Region')['Sales Revenue'].sum().max()
        basic_insights.append({
            'severity': 'Medium',
            'type': 'Regional Performance',
            'issue': f'{top_region} is the top performing region',
            'action': f'Analyze success factors in {top_region} and replicate in other regions',
            'expected_impact': f'Potential revenue increase of ${top_region_revenue * 0.1:,.0f}'
        })
        
        top_category = filtered_df.groupby('Category')['Sales Revenue'].sum().idxmax()
        basic_insights.append({
            'severity': 'Low',
            'type': 'Product Category',
            'issue': f'{top_category} is the best selling category',
            'action': f'Increase inventory and marketing for {top_category} products',
            'expected_impact': 'Improved stock availability and sales'
        })
        
        avg_margin = filtered_df['Profit Margin (%)'].mean()
        if avg_margin < 20:
            basic_insights.append({
                'severity': 'High',
                'type': 'Profit Margin',
                'issue': f'Average profit margin is {avg_margin:.1f}%, below 20% threshold',
                'action': 'Review pricing strategy and negotiate better supplier terms',
                'expected_impact': 'Increase profit margin by 5-10%'
            })
        
        display_recommendations(basic_insights)
    
    with st.expander("📋 View Raw Data"):
        st.dataframe(filtered_df, use_container_width=True, height=400)
        
        st.download_button(
            label="📥 Download Filtered Data",
            data=filtered_df.to_csv(index=False),
            file_name=f"filtered_sales_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )


if __name__ == "__main__":
    main()