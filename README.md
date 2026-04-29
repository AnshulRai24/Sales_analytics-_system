# 📊 Sales Performance Analysis & Business Insights System

A comprehensive, production-ready sales analytics platform with modern UI, automated insights, and actionable business recommendations.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 🎯 Project Overview

This system provides end-to-end sales data analysis with:
- **Automated data cleaning** and validation
- **Comprehensive analytics** across regions, categories, and products
- **Interactive dashboard** with real-time filtering
- **AI-powered insights** and business recommendations
- **SQL database integration** for enterprise-scale data

---

## 🚀 Features

### 📊 Data Management
- ✅ Intelligent data cleaning (handles missing values, duplicates, type errors)
- ✅ Automated data validation and quality checks
- ✅ SQL database integration (SQLite/MySQL/PostgreSQL)
- ✅ Export capabilities (CSV, Excel)

### 📈 Analytics Engine
- ✅ KPI calculation (revenue, profit, margins, growth rates)
- ✅ Regional performance analysis
- ✅ Category and product performance tracking
- ✅ Time-series trend analysis (monthly, quarterly, yearly)
- ✅ Top/bottom performers identification

### 💡 Business Intelligence
- ✅ Automated insights generation
- ✅ Weak area identification (regions, products, categories)
- ✅ Seasonality detection
- ✅ Growth opportunity identification
- ✅ Actionable recommendations with expected impact

### 🎨 Modern Dashboard
- ✅ Clean, professional UI with custom styling
- ✅ Interactive filters (date range, region, category)
- ✅ Real-time visualizations (Plotly charts)
- ✅ Responsive layout
- ✅ Export and download capabilities

---

## 📁 Project Structure

```
sales-analytics-system/
│
├── data/
│   ├── raw/                    # Raw, unprocessed data
│   │   └── sales_data.csv
│   └── processed/              # Cleaned, processed data
│       └── cleaned_sales_data.csv
│
├── src/
│   ├── data_cleaning.py        # Data cleaning module
│   ├── data_analysis.py        # Analytics engine
│   ├── insights_generator.py  # AI insights generator
│   └── database.py             # Database operations
│
├── app.py                      # Main Streamlit dashboard
├── generate_sample_data.py     # Sample data generator
├── schema.sql                  # Database schema
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- (Optional) MySQL or PostgreSQL for production database

### Step 1: Clone/Download the Project
```bash
# Create project directory
mkdir sales-analytics-system
cd sales-analytics-system
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Generate Sample Data (Optional)
```bash
python generate_sample_data.py
```

This will create 5,000 sample sales records in `data/raw/sales_data.csv`

### Step 4: Set Up Database (Optional)
For SQLite (default):
```bash
python -c "from src.database import DatabaseManager; db = DatabaseManager(); db.connect(); db.create_tables()"
```

For MySQL/PostgreSQL:
```bash
mysql -u username -p < schema.sql
# or
psql -U username -d database_name -f schema.sql
```

---

## 🚀 Running the Application

### Launch the Dashboard
```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

### Using Individual Modules

#### Data Cleaning
```python
from src.data_cleaning import DataCleaner
import pandas as pd

# Load raw data
df = pd.read_csv('data/raw/sales_data.csv')

# Clean data
cleaner = DataCleaner(df)
cleaned_df = cleaner.clean_data()

# Save cleaned data
cleaner.save_cleaned_data('data/processed/cleaned_sales_data.csv')
```

#### Data Analysis
```python
from src.data_analysis import SalesAnalyzer

# Analyze data
analyzer = SalesAnalyzer(cleaned_df)
insights = analyzer.analyze_all()

# Print executive summary
print(analyzer.get_summary_report())
```

#### Generate Insights
```python
from src.insights_generator import InsightsGenerator

# Generate business recommendations
generator = InsightsGenerator(cleaned_df, insights)
recommendations = generator.generate_all_insights()

# Print recommendations
generator.print_recommendations()
```

#### Database Operations
```python
from src.database import DatabaseManager

# Connect to database
db = DatabaseManager('sales_analytics.db')
db.connect()
db.create_tables()

# Insert data
db.insert_sales_data(cleaned_df)
db.update_summary_tables()

# Query data
kpis = db.get_kpis()
top_products = db.get_top_products(10)
```

---

## 📊 Dashboard Features

### 1. **KPI Cards**
- Total Revenue
- Total Profit
- Total Orders
- Products Sold

### 2. **Interactive Visualizations**
- Monthly revenue & profit trends
- Regional performance comparison
- Category distribution (pie chart)
- Top 10 products by revenue

### 3. **Filters**
- Date range selector
- Region filter
- Category filter

### 4. **Business Insights**
- Automated recommendations
- Severity-based prioritization
- Expected impact analysis

### 5. **Data Export**
- Download filtered data as CSV
- Export complete reports

---

## 🎨 Customization

### Changing Color Scheme
Edit the CSS in `app.py`:
```python
st.markdown("""
    <style>
    .main {
        background-color: #your-color;
    }
    </style>
""", unsafe_allow_html=True)
```

### Adding New Visualizations
Add new chart functions in `app.py`:
```python
def plot_custom_chart(df):
    fig = px.chart_type(...)
    return fig
```

### Custom Business Rules
Modify `src/insights_generator.py` to add domain-specific logic:
```python
def _custom_analysis(self):
    # Your custom business logic
    pass
```

---

## 📈 Sample Data Details

The generated sample data includes:
- **Date Range:** 2023-01-01 to 2024-12-31
- **Categories:** Electronics, Accessories, Software, Furniture
- **Regions:** North, South, East, West, Central
- **Records:** 5,000+ transactions
- **Realistic Features:**
  - Seasonal patterns (holiday peaks)
  - Regional variations
  - Intentional data quality issues for cleaning demonstration

---

## 🔧 Database Schema

### Tables

#### `sales_transactions`
Primary transaction data table
```sql
- transaction_id (PK)
- order_date
- product_name
- category
- region
- sales_revenue
- cost
- profit
- quantity_sold
- profit_margin
- year, month, quarter
```

#### `monthly_performance`
Aggregated monthly metrics
```sql
- year, month, region, category
- total_revenue, total_profit, total_quantity
```

#### `product_performance`
Product-level aggregations
```sql
- product_name
- total_revenue, total_profit
- avg_profit_margin
```

---

## 📊 Key Metrics Calculated

### Revenue Metrics
- Total Sales Revenue
- Average Order Value
- Revenue by Region/Category/Product
- Revenue Growth Rate

### Profitability Metrics
- Total Profit
- Profit Margin (%)
- Cost Analysis
- ROI by Category

### Operational Metrics
- Total Orders
- Quantity Sold
- Unique Products
- Regional Distribution

### Growth Metrics
- Month-over-Month Growth
- Year-over-Year Growth
- Seasonal Patterns

---

## 💡 Business Insights Generated

### 1. **Performance Issues**
- Underperforming regions
- Low-margin categories
- Unprofitable products

### 2. **Growth Opportunities**
- High-performing products to expand
- Successful regions to replicate
- Market expansion opportunities

### 3. **Strategic Recommendations**
- Pricing optimization
- Inventory management
- Marketing focus areas
- Cost reduction opportunities

### 4. **Risk Alerts**
- Products with negative margins
- High seasonal volatility
- Regional performance gaps

---

## 🔍 Troubleshooting

### Common Issues

**Issue:** Module import errors
```bash
# Solution: Ensure you're in the project root directory
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**Issue:** Streamlit won't start
```bash
# Solution: Check if port 8501 is available
streamlit run app.py --server.port 8502
```

**Issue:** Database connection errors
```bash
# Solution: Verify database credentials and create database
python -c "from src.database import DatabaseManager; DatabaseManager().connect()"
```

**Issue:** Missing data visualizations
```bash
# Solution: Ensure plotly is installed
pip install plotly --upgrade
```

---

## 📚 Tech Stack Details

### Backend & Analysis
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computations
- **Python datetime** - Date/time handling

### Database
- **SQLite** - Default embedded database
- **SQLAlchemy** - ORM and database abstraction
- **PyMySQL / psycopg2** - MySQL/PostgreSQL connectors

### Visualization
- **Plotly** - Interactive charts (preferred for web)
- **Matplotlib** - Static visualizations
- **Seaborn** - Statistical visualizations

### Dashboard
- **Streamlit** - Web application framework
- **Custom CSS** - UI styling

---

## 🎯 Future Enhancements

### Planned Features
- [ ] Machine learning predictions
- [ ] Customer segmentation analysis
- [ ] Real-time data streaming
- [ ] Email report automation
- [ ] Multi-user authentication
- [ ] Advanced forecasting models
- [ ] Integration with ERP systems
- [ ] Mobile app version

---

## 📄 License

This project is licensed under the MIT License.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

---

## 📧 Support

For questions or support, please open an issue in the project repository.

---

## 🙏 Acknowledgments

Built with modern data analytics best practices and industry-standard tools.

---

