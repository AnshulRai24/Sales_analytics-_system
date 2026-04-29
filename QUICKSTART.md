# 🚀 Quick Start Guide - Sales Analytics System

Get up and running in 5 minutes!

---

## ⚡ Fastest Setup (3 Steps)

### 1️⃣ Install Dependencies
```bash
pip install streamlit pandas numpy plotly sqlalchemy
```

### 2️⃣ Create Project Structure
```bash
mkdir -p sales-analytics-system/src sales-analytics-system/data/raw sales-analytics-system/data/processed
cd sales-analytics-system
```

### 3️⃣ Launch Dashboard
```bash
# The app includes auto-generated sample data
streamlit run app.py
```

**That's it!** 🎉 The dashboard will open at `http://localhost:8501`

---

## 📋 Complete Setup (Recommended)

### Step-by-Step Commands

```bash
# 1. Create project directory
mkdir sales-analytics-system
cd sales-analytics-system

# 2. Create folder structure
mkdir -p data/raw data/processed src

# 3. Install all dependencies
pip install -r requirements.txt

# 4. Generate sample data (5000 records)
python generate_sample_data.py

# 5. (Optional) Set up database
python -c "from src.database import DatabaseManager; db = DatabaseManager(); db.connect(); db.create_tables()"

# 6. Launch dashboard
streamlit run app.py
```

---

## 🎯 What You'll See

### Dashboard Features:
✅ **4 KPI Cards** showing key metrics  
✅ **Revenue & Profit Trend Chart** (monthly view)  
✅ **Regional Performance Comparison** (bar chart)  
✅ **Category Distribution** (pie chart)  
✅ **Top 10 Products** (horizontal bar chart)  
✅ **Business Insights & Recommendations** (automated)  
✅ **Interactive Filters** (date, region, category)  
✅ **Data Export** (CSV download)

---

## 🔄 Using Your Own Data

### Option 1: Upload via Dashboard
1. Click the **"Upload Sales Data (CSV)"** button in the sidebar
2. Select your CSV file
3. Dashboard automatically refreshes with your data

### Option 2: Replace Sample Data
Place your CSV file at:
```
data/raw/sales_data.csv
```

**Required CSV Columns:**
```
Order Date, Product Name, Category, Region, Sales Revenue, Cost, Profit, Quantity Sold
```

---

## 🎨 Dashboard Controls

### Sidebar Menu:
- **📁 Upload Data** - Import your own CSV
- **📊 Filters** - Date range, region, category
- **⚡ Actions** - Refresh, export reports

### Main Dashboard:
- **KPI Cards** - Quick overview metrics
- **Charts** - Interactive visualizations (hover for details)
- **Insights** - Expandable recommendation cards
- **Raw Data** - View and download filtered data

---

## 💡 Quick Tips

### Analyzing Your Data:
1. **Start broad** - View overall KPIs
2. **Apply filters** - Focus on specific regions/categories
3. **Check trends** - Look at the monthly chart
4. **Review insights** - Read automated recommendations
5. **Export data** - Download filtered results

### Common Workflows:

#### Regional Analysis
```
1. Select region filter
2. Compare to other regions
3. Review regional recommendations
```

#### Product Performance
```
1. Scroll to "Top Products" chart
2. Check profit margins
3. Identify winners and losers
```

#### Time-Series Analysis
```
1. Adjust date range filter
2. View revenue trend chart
3. Identify seasonal patterns
```

---

## 🐛 Troubleshooting

### Dashboard Won't Start?
```bash
# Try different port
streamlit run app.py --server.port 8502
```

### Import Errors?
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### No Data Showing?
```bash
# Generate sample data
python generate_sample_data.py
```

### Charts Not Displaying?
```bash
# Update plotly
pip install plotly --upgrade
```

---

## 📊 Sample Insights You'll Get

The system automatically generates:

### 🔴 Critical Issues
- Products with negative profit margins
- Severe underperforming regions

### 🟠 High Priority
- Regional performance gaps
- Low-margin categories
- Top growth opportunities

### 🟡 Medium Priority
- Seasonal demand patterns
- Inventory optimization suggestions
- Market expansion opportunities

### 🟢 Strategic Initiatives
- Customer loyalty recommendations
- Digital transformation suggestions
- Omnichannel strategies

---

## 🎓 Learning the System

### 5-Minute Tutorial:
1. **Launch** the dashboard
2. **Explore** KPI cards at the top
3. **Interact** with charts (hover, zoom, pan)
4. **Filter** data using sidebar controls
5. **Read** the automated insights
6. **Export** your findings

### Advanced Features:
- Run custom Python analysis using the modules
- Query the database directly
- Modify business rules in `insights_generator.py`
- Customize charts in `app.py`

---

## 📚 Next Steps

### To Customize:
1. **Edit `app.py`** - Modify dashboard layout/colors
2. **Update `insights_generator.py`** - Add custom business rules
3. **Modify `schema.sql`** - Extend database schema
4. **Create new modules** - Add specialized analysis

### To Deploy:
```bash
# Streamlit Cloud (easiest)
streamlit run app.py

# Or Docker
docker build -t sales-analytics .
docker run -p 8501:8501 sales-analytics
```

---

## 🆘 Need Help?

### Check These First:
1. ✅ Python 3.8+ installed?
2. ✅ All dependencies installed?
3. ✅ In the correct directory?
4. ✅ Data file exists?

### Still Stuck?
- Review the full README.md
- Check module docstrings
- Verify file paths
- Test individual modules

---

## 🎉 Success Checklist

After setup, you should have:
- ✅ Dashboard running on localhost:8501
- ✅ Sample data loaded (5000+ records)
- ✅ All visualizations displaying
- ✅ Filters working correctly
- ✅ Insights generated automatically
- ✅ Ability to export data

---

## 🚀 Ready to Analyze!

Your sales analytics system is now ready. Start exploring your data and discovering actionable insights!

**Dashboard URL:** http://localhost:8501

**Happy analyzing!** 📊✨