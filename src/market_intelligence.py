"""
Workforce Intelligence Platform - Market Intelligence Engine
=============================================================
Computes comprehensive job market analytics:
- Salary benchmarks across 10 roles (percentiles 10th, 25th, 50th, 75th, 90th, mean)
- Experience vs. Salary progression curves (Entry, Mid, Senior, Lead/Exec)
- Company tier intelligence (Product, FAANG/MNC Tech, FinTech/Banks, IT Services)
- Metro geographic salary index & job volumes
- Supply & Demand volume dynamics (17,400+ job positions across 640+ companies)
"""

import os
import sys
import json
import numpy as np
import pandas as pd

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


class MarketIntelligenceEngine:
    def __init__(self, processed_data_dir: str):
        self.proc_dir = processed_data_dir
        self.df_ds = pd.read_csv(os.path.join(self.proc_dir, 'cleaned_data_science_jobs.csv'))
        self.df_aj = pd.read_csv(os.path.join(self.proc_dir, 'cleaned_analytics_jobs.csv'))
        self.master_jobs = self._create_unified_market_data()

    def _create_unified_market_data(self):
        """Merges cleaned Data Science Jobs and Analytics Jobs into a unified market dataset."""
        # Dataset 1: DS jobs (aggregated company level postings)
        ds_subset = pd.DataFrame({
            'source': 'data_science_jobs',
            'role': self.df_ds['standardized_role'],
            'company': self.df_ds['company_name'],
            'min_exp': self.df_ds['min_experience_clean'],
            'avg_exp': self.df_ds['min_experience_clean'] + 1.5,
            'max_exp': self.df_ds['min_experience_clean'] + 3.0,
            'salary_lpa': self.df_ds['avg_salary_lpa'],
            'min_salary_lpa': self.df_ds['min_salary_lpa'],
            'max_salary_lpa': self.df_ds['max_salary_lpa'],
            'location': 'India (Multi-City)',
            'metro_location': 'India (Multi-City)',
            'key_skills': self.df_ds['job_title']
        })

        # Dataset 2: Analytics jobs (individual listings)
        aj_subset = pd.DataFrame({
            'source': 'analytics_jobs',
            'role': self.df_aj['standardized_role'],
            'company': 'Enterprise Postings',
            'min_exp': self.df_aj['min_exp_years'],
            'avg_exp': self.df_aj['avg_exp_years'],
            'max_exp': self.df_aj['max_exp_years'],
            'salary_lpa': self.df_aj['salary_lpa_imputed'],
            'min_salary_lpa': self.df_aj['salary_lpa_imputed'] * 0.75,
            'max_salary_lpa': self.df_aj['salary_lpa_imputed'] * 1.35,
            'location': self.df_aj['location'],
            'metro_location': self.df_aj['metro_location'],
            'key_skills': self.df_aj['key_skills']
        })

        unified = pd.concat([ds_subset, aj_subset], ignore_index=True)
        return unified

    def get_role_salary_benchmarks(self):
        """Calculates granular salary percentiles for each standardized role."""
        records = []
        for role, grp in self.master_jobs.groupby('role'):
            salaries = grp['salary_lpa'].dropna()
            if len(salaries) == 0:
                continue
            records.append({
                'role': role,
                'sample_size': int(len(salaries)),
                'min_lpa': round(float(salaries.min()), 1),
                'p10_lpa': round(float(salaries.quantile(0.10)), 1),
                'p25_lpa': round(float(salaries.quantile(0.25)), 1),
                'median_lpa': round(float(salaries.median()), 1),
                'mean_lpa': round(float(salaries.mean()), 1),
                'p75_lpa': round(float(salaries.quantile(0.75)), 1),
                'p90_lpa': round(float(salaries.quantile(0.90)), 1),
                'max_lpa': round(float(salaries.max()), 1),
                'avg_experience_req': round(float(grp['avg_exp'].dropna().mean()), 1)
            })
        
        # Sort by median salary descending
        records = sorted(records, key=lambda x: x['median_lpa'], reverse=True)
        return records

    def get_experience_salary_curves(self):
        """Calculates experience tier progression curves across analytics careers."""
        df = self.master_jobs.copy()
        
        def exp_tier(exp):
            if exp <= 2:
                return '0-2 yrs (Entry)'
            elif exp <= 5:
                return '3-5 yrs (Mid-Level)'
            elif exp <= 8:
                return '6-8 yrs (Senior)'
            else:
                return '9+ yrs (Lead / Principal)'

        df['exp_tier'] = df['avg_exp'].apply(exp_tier)
        
        curve = []
        for tier in ['0-2 yrs (Entry)', '3-5 yrs (Mid-Level)', '6-8 yrs (Senior)', '9+ yrs (Lead / Principal)']:
            tier_df = df[df['exp_tier'] == tier]
            if len(tier_df) > 0:
                by_role = {}
                for role, r_grp in tier_df.groupby('role'):
                    by_role[role] = {
                        'median_lpa': round(float(r_grp['salary_lpa'].median()), 1),
                        'mean_lpa': round(float(r_grp['salary_lpa'].mean()), 1),
                        'count': int(len(r_grp))
                    }
                curve.append({
                    'experience_tier': tier,
                    'overall_median_lpa': round(float(tier_df['salary_lpa'].median()), 1),
                    'overall_mean_lpa': round(float(tier_df['salary_lpa'].mean()), 1),
                    'sample_count': int(len(tier_df)),
                    'role_breakdown': by_role
                })
        return curve

    def get_company_tier_analysis(self):
        """Categorizes employers into Strategic Archetypes and benchmarks compensation premiums."""
        # Classify companies from Data Science Jobs
        df = self.df_ds.copy()
        
        def classify_company(comp):
            c_lower = str(comp).lower()
            if any(k in c_lower for k in ['google', 'microsoft', 'amazon', 'adobe', 'apple', 'walmart', 'paypal', 'meta']):
                return 'Global Tech & Cloud Giants'
            elif any(k in c_lower for k in ['flipkart', 'swiggy', 'zomato', 'paytm', 'oyo', 'ola', 'meesho', 'cars24']):
                return 'Tech Unicorns & Product Disruptors'
            elif any(k in c_lower for k in ['jp morgan', 'citibank', 'barclays', 'hsbc', 'wells fargo', 'goldman sachs', 'hdfc', 'icici', 'standard chartered', 'bank of america']):
                return 'Banking, FinTech & GCC Hubs'
            elif any(k in c_lower for k in ['deloitte', 'pwc', 'ey', 'ernst & young', 'kpmg', 'mckinsey', 'bcg', 'bain', 'gartner', 'fractal', 'tiger analytics', 'mu sigma']):
                return 'Strategic Consulting & Analytics Specialists'
            elif any(k in c_lower for k in ['tcs', 'accenture', 'ibm', 'cognizant', 'infosys', 'wipro', 'capgemini', 'tech mahindra', 'hcl']):
                return 'Tier-1 IT & Global Systems Integrators'
            else:
                return 'Mid-Market Enterprise & GCCs'

        df['company_tier'] = df['company_name'].apply(classify_company)
        
        tiers = []
        for tier_name, grp in df.groupby('company_tier'):
            tiers.append({
                'company_tier': tier_name,
                'companies_represented': int(grp['company_name'].nunique()),
                'sample_postings': int(grp['num_of_jobs_clean'].sum()),
                'median_salary_lpa': round(float(grp['avg_salary_lpa'].median()), 1),
                'mean_salary_lpa': round(float(grp['avg_salary_lpa'].mean()), 1),
                'min_salary_lpa': round(float(grp['min_salary_lpa'].min()), 1),
                'max_salary_lpa': round(float(grp['max_salary_lpa'].max()), 1),
                'top_hiring_companies': grp.groupby('company_name')['num_of_jobs_clean'].sum().nlargest(5).to_dict()
            })
            
        tiers = sorted(tiers, key=lambda x: x['median_salary_lpa'], reverse=True)
        return tiers

    def get_geographic_distribution(self):
        """Analyzes metro geographical talent hubs, salary index, and volume."""
        df = self.df_aj.copy()
        metros = []
        for metro, grp in df.groupby('metro_location'):
            metros.append({
                'metro': metro,
                'total_job_postings': int(len(grp)),
                'market_share_pct': round(float(len(grp) / len(df) * 100), 1),
                'median_salary_lpa': round(float(grp['salary_lpa_imputed'].median()), 1),
                'mean_salary_lpa': round(float(grp['salary_lpa_imputed'].mean()), 1),
                'top_roles': grp['standardized_role'].value_counts().head(3).to_dict()
            })
        metros = sorted(metros, key=lambda x: x['total_job_postings'], reverse=True)
        return metros

    def generate_full_report(self):
        """Assembles all market intelligence components into a unified report."""
        report = {
            'role_benchmarks': self.get_role_salary_benchmarks(),
            'experience_progression': self.get_experience_salary_curves(),
            'company_tiers': self.get_company_tier_analysis(),
            'geographic_hubs': self.get_geographic_distribution()
        }
        
        out_fp = os.path.join(self.proc_dir, 'market_intelligence_report.json')
        with open(out_fp, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
            
        print(f"[OK] Market Intelligence report generated at {out_fp}")
        return report


if __name__ == '__main__':
    proc_dir = r'C:\Users\chitr_mzkaj0t\.gemini\antigravity\scratch\workforce_intelligence\data\processed'
    engine = MarketIntelligenceEngine(proc_dir)
    rep = engine.generate_full_report()
    print("Market Intelligence complete. Top 3 highest paying roles:")
    for r in rep['role_benchmarks'][:3]:
        print(f"  {r['role']}: Median {r['median_lpa']} LPA (Range {r['min_lpa']}-{r['max_lpa']} LPA)")
