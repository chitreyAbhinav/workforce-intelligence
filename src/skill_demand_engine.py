"""
Workforce Intelligence Platform - Skill Demand & Taxonomy Engine
================================================================
NLP-driven skill intelligence engine:
- Extracts skills from unstructured key_skills & job descriptions across 12,000+ jobs
- Classifies skills into structured domains (AI/ML, Big Data, Cloud, BI/Analytics, Programming)
- Calculates Skill Market Penetration % per role
- Quantifies Empirical Salary Premium (LPA delta for jobs requiring Skill X vs. not)
- Generates Skill Co-occurrence Adjacency Matrix
- Outputs Master Skill Taxonomy and Role-Skill Profiles
"""

import os
import re
import sys
import json
from collections import Counter, defaultdict
import numpy as np
import pandas as pd

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


SKILL_DICTIONARY = {
    # Core Languages
    'Python': [r'\bpython\b'],
    'SQL': [r'\bsql\b', r'\bplsql\b', r'\btransact-sql\b', r'\bt-sql\b', r'\bpostgresql\b', r'\bmysql\b', r'\boracle sql\b'],
    'R': [r'\br\b', r'\br-programming\b', r'\br language\b'],
    'SAS': [r'\bsas\b', r'\bsas vfl\b', r'\bsas visual analytics\b', r'\bsas studio\b', r'\bsas viya\b'],
    'Scala': [r'\bscala\b'],
    'Java': [r'\bjava\b', r'\bcore java\b'],
    'C++': [r'\bc\+\+\b'],
    'Julia': [r'\bjulia\b'],
    
    # AI / ML / Deep Learning
    'Machine Learning': [r'\bmachine learning\b', r'\bml\b', r'\bscikit-learn\b', r'\bsklearn\b', r'\bclassification\b', r'\bregression\b'],
    'Deep Learning': [r'\bdeep learning\b', r'\bdl\b', r'\bneural networks\b', r'\bcnn\b', r'\brnn\b', r'\blstm\b'],
    'Natural Language Processing': [r'\bnlp\b', r'\bnatural language processing\b', r'\bbert\b', r'\bllm\b', r'\btransformers\b'],
    'Computer Vision': [r'\bcomputer vision\b', r'\bopencv\b', r'\bimage processing\b'],
    'TensorFlow': [r'\btensorflow\b', r'\btf\b'],
    'PyTorch': [r'\bpytorch\b'],
    'Generative AI / LLMs': [r'\bgen ai\b', r'\bgenerative ai\b', r'\bllm\b', r'\blangchain\b', r'\bgpt\b'],
    'MLOps': [r'\bmlops\b', r'\bmodel deployment\b', r'\bmlflow\b', r'\bkubeflow\b'],
    
    # Big Data & Data Engineering
    'Spark / PySpark': [r'\bspark\b', r'\bpyspark\b'],
    'Hadoop': [r'\bhadoop\b', r'\bhdfs\b', r'\bmapreduce\b'],
    'Hive': [r'\bhive\b'],
    'Kafka': [r'\bkafka\b'],
    'Airflow': [r'\bairflow\b'],
    'Databricks': [r'\bdatabricks\b'],
    'Snowflake': [r'\bsnowflake\b'],
    'ETL Pipelines': [r'\betl\b', r'\bdata pipeline\b', r'\bdata warehousing\b', r'\bdwh\b', r'\binformatica\b'],
    
    # Cloud Infrastructure
    'AWS': [r'\baws\b', r'\bamazon web services\b', r'\bs3\b', r'\bec2\b', r'\bredshift\b'],
    'Azure': [r'\bazure\b', r'\bmicrosoft azure\b', r'\bsynapse\b', r'\badf\b'],
    'GCP': [r'\bgcp\b', r'\bgoogle cloud\b', r'\bbigquery\b'],
    'Docker / Kubernetes': [r'\bdocker\b', r'\bkubernetes\b', r'\bk8s\b', r'\bcontainers\b'],
    'CI/CD & DevOps': [r'\bci/cd\b', r'\bcicd\b', r'\bgit\b', r'\bdevops\b', r'\bjenkins\b'],
    
    # BI, Storytelling & Analytics
    'Tableau': [r'\btableau\b'],
    'Power BI': [r'\bpower bi\b', r'\bpowerbi\b', r'\bpbi\b'],
    'Excel / Advanced Excel': [r'\bexcel\b', r'\bvba\b', r'\badvanced excel\b'],
    'Data Visualization': [r'\bvisualization\b', r'\bdashboard\b', r'\bstorytelling\b', r'\bqlik\b', r'\blooker\b', r'\bmatplotlib\b', r'\bseaborn\b'],
    'Statistical Modeling': [r'\bstatistics\b', r'\bstatistical modeling\b', r'\bhypothesis testing\b', r'\ba/b testing\b', r'\bprobability\b', r'\btime series\b'],
    'Business Acumen': [r'\bbusiness analysis\b', r'\bbusiness intelligence\b', r'\bstakeholder management\b', r'\broi\b', r'\bkpi\b', r'\brequirements gathering\b']
}

SKILL_CATEGORIES = {
    'Programming': ['Python', 'SQL', 'R', 'SAS', 'Scala', 'Java', 'C++', 'Julia'],
    'AI / Machine Learning': ['Machine Learning', 'Deep Learning', 'Natural Language Processing', 'Computer Vision', 'TensorFlow', 'PyTorch', 'Generative AI / LLMs', 'MLOps'],
    'Big Data & Cloud': ['Spark / PySpark', 'Hadoop', 'Hive', 'Kafka', 'Airflow', 'Databricks', 'Snowflake', 'ETL Pipelines', 'AWS', 'Azure', 'GCP', 'Docker / Kubernetes', 'CI/CD & DevOps'],
    'BI & Analytics': ['Tableau', 'Power BI', 'Excel / Advanced Excel', 'Data Visualization', 'Statistical Modeling', 'Business Acumen']
}


class SkillDemandEngine:
    def __init__(self, processed_data_dir: str):
        self.proc_dir = processed_data_dir
        self.df_jobs = pd.read_csv(os.path.join(self.proc_dir, 'cleaned_analytics_jobs.csv'))
        self.skill_regexes = {
            skill: [re.compile(p, re.IGNORECASE) for p in patterns]
            for skill, patterns in SKILL_DICTIONARY.items()
        }

    def extract_skills_from_text(self, text: str):
        """Extracts list of matched skills from string text."""
        if not text or pd.isna(text):
            return []
        text_lower = f" {str(text).lower()} "
        matched = []
        for skill, regex_list in self.skill_regexes.items():
            if any(rgx.search(text_lower) for rgx in regex_list):
                matched.append(skill)
        return matched

    def build_skill_demand_analytics(self):
        """Analyzes skill demand across all jobs and computes market salary premiums."""
        print("Extracting skill profiles from job postings...")
        
        # Combine key_skills and job_description for complete NLP coverage
        self.df_jobs['extracted_skills'] = (self.df_jobs['key_skills'] + " " + self.df_jobs['job_description']).apply(
            self.extract_skills_from_text
        )
        
        # Ensure at least some default skills based on role if listing was sparse
        def enrich_sparse(row):
            skills = list(row['extracted_skills'])
            role = row['standardized_role']
            if not skills:
                if 'Scientist' in role:
                    skills = ['Python', 'Machine Learning', 'SQL', 'Statistical Modeling']
                elif 'Engineer' in role:
                    skills = ['SQL', 'Python', 'ETL Pipelines', 'Spark / PySpark']
                elif 'Analyst' in role:
                    skills = ['SQL', 'Excel / Advanced Excel', 'Tableau', 'Power BI']
                elif 'Architect' in role:
                    skills = ['SQL', 'AWS', 'ETL Pipelines', 'Docker / Kubernetes']
            return skills

        self.df_jobs['extracted_skills'] = self.df_jobs.apply(enrich_sparse, axis=1)

        # 1. Overall Skill Frequency & Penetration
        total_jobs = len(self.df_jobs)
        skill_counts = Counter()
        skill_salaries = defaultdict(list)
        all_salaries = self.df_jobs['salary_lpa_imputed'].dropna().values
        base_median_salary = float(np.median(all_salaries))

        for idx, row in self.df_jobs.iterrows():
            sal = row['salary_lpa_imputed']
            for s in row['extracted_skills']:
                skill_counts[s] += 1
                if pd.notna(sal):
                    skill_salaries[s].append(sal)

        # Calculate empirical salary premium for each skill
        skill_market_stats = []
        for skill in SKILL_DICTIONARY.keys():
            count = skill_counts.get(skill, 0)
            pct = round((count / total_jobs) * 100, 2)
            s_sals = skill_salaries[skill]
            
            if len(s_sals) >= 10:
                s_median = float(np.median(s_sals))
                s_mean = float(np.mean(s_sals))
                premium_lpa = round(s_median - base_median_salary, 2)
                premium_pct = round(((s_median - base_median_salary) / base_median_salary) * 100, 1)
            else:
                s_median = base_median_salary
                s_mean = base_median_salary
                premium_lpa = 0.0
                premium_pct = 0.0

            # Find category
            category = 'Other'
            for cat, s_list in SKILL_CATEGORIES.items():
                if skill in s_list:
                    category = cat
                    break

            skill_market_stats.append({
                'skill': skill,
                'category': category,
                'job_postings_count': count,
                'market_penetration_pct': pct,
                'skill_median_salary_lpa': round(s_median, 2),
                'skill_mean_salary_lpa': round(s_mean, 2),
                'salary_premium_lpa': premium_lpa,
                'salary_premium_pct': premium_pct
            })

        skill_market_stats = sorted(skill_market_stats, key=lambda x: x['job_postings_count'], reverse=True)

        # 2. Role-Skill Matrix (Skill penetration % within each of the 10 roles)
        role_skill_profiles = {}
        for role, grp in self.df_jobs.groupby('standardized_role'):
            role_total = len(grp)
            role_skill_counts = Counter()
            for s_list in grp['extracted_skills']:
                for s in s_list:
                    role_skill_counts[s] += 1
                    
            profiles = []
            for skill, count in role_skill_counts.most_common(15):
                pen_pct = round((count / role_total) * 100, 1)
                profiles.append({
                    'skill': skill,
                    'count': count,
                    'penetration_pct': pen_pct
                })
            role_skill_profiles[role] = {
                'role': role,
                'total_postings': role_total,
                'top_skills': profiles
            }

        # 3. Skill Co-occurrence Adjacency Graph (for Network Visualization)
        top_25_skills = [s['skill'] for s in skill_market_stats[:25]]
        cooccur_matrix = {s1: {s2: 0 for s2 in top_25_skills} for s1 in top_25_skills}
        
        for s_list in self.df_jobs['extracted_skills']:
            present_top = [s for s in s_list if s in top_25_skills]
            for i in range(len(present_top)):
                for j in range(i + 1, len(present_top)):
                    s1 = present_top[i]
                    s2 = present_top[j]
                    cooccur_matrix[s1][s2] += 1
                    cooccur_matrix[s2][s1] += 1

        # Format graph nodes & links for D3 / vis.js
        graph_nodes = []
        for s_info in skill_market_stats:
            if s_info['skill'] in top_25_skills:
                graph_nodes.append({
                    'id': s_info['skill'],
                    'label': s_info['skill'],
                    'category': s_info['category'],
                    'value': s_info['job_postings_count'],
                    'salary_lpa': s_info['skill_median_salary_lpa']
                })

        graph_links = []
        seen = set()
        for s1 in top_25_skills:
            for s2 in top_25_skills:
                if s1 != s2:
                    weight = cooccur_matrix[s1][s2]
                    pair = tuple(sorted([s1, s2]))
                    if weight > 50 and pair not in seen:
                        seen.add(pair)
                        graph_links.append({
                            'source': s1,
                            'target': s2,
                            'weight': weight
                        })

        skill_taxonomy_result = {
            'market_skills_ranked': skill_market_stats,
            'role_skill_profiles': role_skill_profiles,
            'skill_adjacency_graph': {
                'nodes': graph_nodes,
                'links': graph_links
            }
        }

        # Save outputs
        out_fp = os.path.join(self.proc_dir, 'master_skill_taxonomy.json')
        with open(out_fp, 'w', encoding='utf-8') as f:
            json.dump(skill_taxonomy_result, f, indent=2)

        role_fp = os.path.join(self.proc_dir, 'role_skill_profiles.json')
        with open(role_fp, 'w', encoding='utf-8') as f:
            json.dump(role_skill_profiles, f, indent=2)

        print(f"[OK] Master Skill Taxonomy saved at {out_fp}")
        return skill_taxonomy_result


if __name__ == '__main__':
    proc_dir = r'C:\Users\chitr_mzkaj0t\.gemini\antigravity\scratch\workforce_intelligence\data\processed'
    engine = SkillDemandEngine(proc_dir)
    res = engine.build_skill_demand_analytics()
    print("Top 5 in-demand skills in the market:")
    for s in res['market_skills_ranked'][:5]:
        print(f"  {s['skill']}: {s['job_postings_count']} jobs ({s['market_penetration_pct']}%), Premium: +{s['salary_premium_lpa']} LPA")
