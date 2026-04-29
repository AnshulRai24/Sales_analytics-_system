"""
Business Insights Generator
Generates actionable business recommendations based on data analysis
"""

import pandas as pd
import numpy as np


class InsightsGenerator:
    """Generate actionable business insights and recommendations"""
    
    def __init__(self, df, analysis_results):
        """Initialize with dataframe and analysis results"""
        self.df = df
        self.analysis = analysis_results
        self.recommendations = []
        
    def generate_all_insights(self):
        """Generate comprehensive business insights"""
        print("💡 Generating Business Insights...\n")
        
        self._analyze_weak_regions()
        self._analyze_weak_categories()
        self._analyze_weak_products()
        self._analyze_seasonality()
        self._analyze_profitability()
        self._analyze_growth_opportunities()
        self._generate_strategic_recommendations()
        
        print("\n✅ Insights Generation Complete!")
        return self.recommendations
    
    def _analyze_weak_regions(self):
        """Identify and recommend improvements for weak regions"""
        print("🗺️  Analyzing Regional Weaknesses...")
        
        region_analysis = self.analysis.get('region_analysis')
        
        if region_analysis is not None and not region_analysis.empty:
            # Identify regions below average performance
            avg_revenue = region_analysis['Total Revenue'].mean()
            weak_regions = region_analysis[region_analysis['Total Revenue'] < avg_revenue]
            
            for region in weak_regions.index:
                revenue = weak_regions.loc[region, 'Total Revenue']
                gap = avg_revenue - revenue
                gap_pct = (gap / avg_revenue * 100)
                
                recommendation = {
                    'type': 'Regional Performance',
                    'severity': 'High' if gap_pct > 30 else 'Medium',
                    'region': region,
                    'issue': f'{region} is underperforming by {gap_pct:.1f}%',
                    'action': f'Increase marketing efforts in {region}. Consider promotional campaigns, local partnerships, or sales team expansion.',
                    'expected_impact': f'Potential revenue increase of ${gap:,.2f}'
                }
                self.recommendations.append(recommendation)
                
        print(f"   ✓ Identified {len(weak_regions)} underperforming regions")
    
    def _analyze_weak_categories(self):
        """Identify weak product categories"""
        print("\n📦 Analyzing Category Weaknesses...")
        
        category_analysis = self.analysis.get('category_analysis')
        
        if category_analysis is not None and not category_analysis.empty:
            # Find low profit margin categories
            avg_margin = category_analysis['Profit Margin (%)'].mean()
            low_margin_cats = category_analysis[category_analysis['Profit Margin (%)'] < avg_margin]
            
            for category in low_margin_cats.index:
                margin = low_margin_cats.loc[category, 'Profit Margin (%)']
                
                recommendation = {
                    'type': 'Category Optimization',
                    'severity': 'Medium',
                    'category': category,
                    'issue': f'{category} has low profit margin of {margin:.2f}%',
                    'action': f'Review pricing strategy for {category}. Consider cost optimization, premium product lines, or bundling strategies.',
                    'expected_impact': 'Improve profit margin by 5-10%'
                }
                self.recommendations.append(recommendation)
                
        print(f"   ✓ Identified {len(low_margin_cats)} low-margin categories")
    
    def _analyze_weak_products(self):
        """Identify underperforming products"""
        print("\n🏷️  Analyzing Product Performance...")
        
        bottom_products = self.analysis.get('bottom_10_products')
        
        if bottom_products is not None and not bottom_products.empty:
            # Check for negative profit products
            negative_profit = bottom_products[bottom_products['Total Profit'] < 0]
            
            for product in negative_profit.index:
                loss = abs(negative_profit.loc[product, 'Total Profit'])
                
                recommendation = {
                    'type': 'Product Strategy',
                    'severity': 'Critical',
                    'product': product,
                    'issue': f'{product} is losing ${loss:,.2f}',
                    'action': f'Consider discontinuing {product} or renegotiating supplier costs. Analyze if it serves as a loss leader.',
                    'expected_impact': f'Eliminate ${loss:,.2f} in losses'
                }
                self.recommendations.append(recommendation)
            
            # Low performers
            low_performers = bottom_products[bottom_products['Total Profit'] >= 0].head(5)
            for product in low_performers.index:
                recommendation = {
                    'type': 'Product Improvement',
                    'severity': 'Low',
                    'product': product,
                    'issue': f'{product} is among the lowest revenue generators',
                    'action': f'Boost {product} visibility through targeted marketing or consider product refresh.',
                    'expected_impact': 'Potential 20-30% revenue increase'
                }
                self.recommendations.append(recommendation)
                
        print(f"   ✓ Generated {len(negative_profit) + min(5, len(low_performers))} product recommendations")
    
    def _analyze_seasonality(self):
        """Detect seasonal patterns and trends"""
        print("\n📅 Analyzing Seasonal Patterns...")
        
        monthly_trend = self.analysis.get('monthly_trend')
        
        if monthly_trend is not None and not monthly_trend.empty:
            # Calculate monthly revenue variance
            monthly_revenues = monthly_trend['Sales Revenue']
            revenue_std = monthly_revenues.std()
            revenue_mean = monthly_revenues.mean()
            cv = (revenue_std / revenue_mean) * 100  # Coefficient of variation
            
            if cv > 20:  # High variability indicates seasonality
                best_months = monthly_revenues.nlargest(3)
                worst_months = monthly_revenues.nsmallest(3)
                
                recommendation = {
                    'type': 'Seasonal Strategy',
                    'severity': 'Medium',
                    'issue': f'Significant seasonal variation detected (CV: {cv:.1f}%)',
                    'action': f'Prepare inventory and staffing for peak months. Implement off-season promotions to smooth demand.',
                    'expected_impact': 'Reduce revenue volatility by 15-25%'
                }
                self.recommendations.append(recommendation)
                
                print(f"   ✓ Detected seasonality pattern (CV: {cv:.1f}%)")
            else:
                print("   ✓ Stable monthly performance detected")
    
    def _analyze_profitability(self):
        """Analyze overall profitability health"""
        print("\n💰 Analyzing Profitability...")
        
        kpis = self.analysis.get('kpis', {})
        overall_margin = kpis.get('overall_profit_margin', 0)
        
        # Industry benchmarks (general retail: 5-10%, tech: 15-25%)
        if overall_margin < 10:
            recommendation = {
                'type': 'Profitability Improvement',
                'severity': 'High',
                'issue': f'Overall profit margin is {overall_margin:.2f}%, below healthy threshold',
                'action': 'Conduct comprehensive cost analysis. Negotiate better supplier terms, reduce operational costs, and review pricing strategy.',
                'expected_impact': 'Increase profit margin to 12-15%'
            }
            self.recommendations.append(recommendation)
            print(f"   ⚠️  Low profit margin: {overall_margin:.2f}%")
        else:
            print(f"   ✓ Healthy profit margin: {overall_margin:.2f}%")
    
    def _analyze_growth_opportunities(self):
        """Identify growth opportunities"""
        print("\n🚀 Identifying Growth Opportunities...")
        
        # High-performing products
        top_products = self.analysis.get('top_10_products')
        
        if top_products is not None and not top_products.empty:
            top_3 = top_products.head(3)
            
            for product in top_3.index:
                revenue = top_3.loc[product, 'Total Revenue']
                
                recommendation = {
                    'type': 'Growth Opportunity',
                    'severity': 'High',
                    'product': product,
                    'issue': f'{product} is a top performer with ${revenue:,.2f} revenue',
                    'action': f'Expand {product} product line. Consider premium versions, bundles, or market expansion.',
                    'expected_impact': f'Potential 30-50% revenue increase in this segment'
                }
                self.recommendations.append(recommendation)
        
        # Best region expansion
        best_region = self.analysis.get('best_region')
        if best_region:
            recommendation = {
                'type': 'Market Expansion',
                'severity': 'Medium',
                'region': best_region,
                'issue': f'{best_region} shows strongest performance',
                'action': f'Replicate {best_region} success model in other regions. Analyze what makes it successful.',
                'expected_impact': '20-30% revenue growth in target regions'
            }
            self.recommendations.append(recommendation)
            
        print(f"   ✓ Identified {len(top_3) + 1} growth opportunities")
    
    def _generate_strategic_recommendations(self):
        """Generate high-level strategic recommendations"""
        print("\n🎯 Generating Strategic Recommendations...")
        
        kpis = self.analysis.get('kpis', {})
        
        # Data-driven strategic recommendations
        strategic_recs = [
            {
                'type': 'Strategic Initiative',
                'severity': 'High',
                'issue': 'Customer retention analysis needed',
                'action': 'Implement customer loyalty program. Track repeat purchase rate and customer lifetime value.',
                'expected_impact': 'Increase repeat purchases by 15-25%'
            },
            {
                'type': 'Strategic Initiative',
                'severity': 'Medium',
                'issue': 'Inventory optimization opportunity',
                'action': 'Implement just-in-time inventory for slow-moving products. Increase stock for top performers.',
                'expected_impact': 'Reduce inventory costs by 10-15%'
            },
            {
                'type': 'Strategic Initiative',
                'severity': 'Medium',
                'issue': 'Digital transformation',
                'action': 'Enhance e-commerce presence and implement omnichannel strategy.',
                'expected_impact': 'Expand market reach by 20-30%'
            }
        ]
        
        self.recommendations.extend(strategic_recs)
        print(f"   ✓ Generated {len(strategic_recs)} strategic initiatives")
    
    def get_recommendations(self):
        """Return all recommendations"""
        return self.recommendations
    
    def get_priority_recommendations(self, top_n=5):
        """Get top N priority recommendations"""
        severity_order = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}
        sorted_recs = sorted(
            self.recommendations,
            key=lambda x: severity_order.get(x.get('severity', 'Low'), 3)
        )
        return sorted_recs[:top_n]
    
    def print_recommendations(self):
        """Print formatted recommendations"""
        print("\n" + "="*70)
        print("📋 BUSINESS RECOMMENDATIONS & ACTION ITEMS")
        print("="*70)
        
        for i, rec in enumerate(self.recommendations, 1):
            severity_emoji = {
                'Critical': '🔴',
                'High': '🟠',
                'Medium': '🟡',
                'Low': '🟢'
            }
            
            emoji = severity_emoji.get(rec.get('severity', 'Low'), '⚪')
            
            print(f"\n{emoji} [{rec.get('severity', 'Low')}] {rec.get('type', 'General')}")
            print(f"   Issue: {rec.get('issue', 'N/A')}")
            print(f"   Action: {rec.get('action', 'N/A')}")
            print(f"   Impact: {rec.get('expected_impact', 'N/A')}")
            
        print("\n" + "="*70)


# Example usage
if __name__ == "__main__":
    # Mock analysis results
    mock_analysis = {
        'kpis': {
            'total_revenue': 500000,
            'overall_profit_margin': 8.5
        },
        'best_region': 'North',
        'worst_region': 'South'
    }
    
    mock_df = pd.DataFrame()
    
    generator = InsightsGenerator(mock_df, mock_analysis)
    generator._analyze_profitability()
    generator.print_recommendations()