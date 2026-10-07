"""
Workforce Intelligence Platform - Market × Success Intelligence Matrix
======================================================================
Hero Feature #2 & Locked Feature #11:
Analyzes the intersection of:
- Axis X: Empirical Market Demand (% of job listings demanding the skill)
- Axis Y: Empirical Success & Hike Impact (Statistical & ML weight on performance hikes)

Categorizes all analytics skills into 4 Strategic Quadrants:
1. Quadrant I: Strategic Core Bets (High Demand x High Success Impact)
2. Quadrant II: Table Stakes / Commodity (High Demand x Low Outcome Impact)
3. Quadrant III: Elite Differentiators (Low Demand x High Outcome Impact)
4. Quadrant IV: Deprecated / Low-ROI (Low Demand x Low Outcome Impact)
"""

import os
import sys
import json
import numpy as np

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


class MarketSuccessMatrixEngine:
    def __init__(self, processed_data_dir: str):
        self.proc_dir = processed_data_dir
        with open(os.path.join(self.proc_dir, 'master_skill_taxonomy.json'), 'r', encoding='utf-8') as f:
            self.taxonomy = json.load(f)
        with open(os.path.join(self.proc_dir, 'model_metrics_report.json'), 'r', encoding='utf-8') as f:
            self.model_metrics = json.load(f)

    def build_matrix(self):
        """Computes coordinate points and assigns quadrant classifications to all skills."""
        jds_importances = self.model_metrics['junior_data_scientist_skill_model']['models']['Random Forest']['feature_importance']
        
        # Skill to ML impact mapping
        trait_to_skills = {
            'coding_skills': ['Python', 'SQL', 'Scala', 'Java', 'SAS', 'C++'],
            'ai_and_ml_skills': ['Machine Learning', 'Deep Learning', 'Natural Language Processing', 'Computer Vision', 'TensorFlow', 'PyTorch', 'Generative AI / LLMs', 'MLOps'],
            'big_data_skills': ['Spark / PySpark', 'Hadoop', 'Hive', 'Kafka', 'Airflow', 'Databricks', 'Snowflake', 'ETL Pipelines', 'AWS', 'Azure', 'GCP'],
            'dashboard_and_storytelling_skills': ['Tableau', 'Power BI', 'Data Visualization', 'Excel / Advanced Excel', 'Business Acumen'],
            'maths-stats_skills': ['Statistical Modeling', 'R', 'Julia']
        }
        
        skill_impact_map = {}
        for trait, skills in trait_to_skills.items():
            imp = jds_importances.get(trait, 0.20)
            for s in skills:
                # Add granular variance within trait based on premium
                skill_impact_map[s] = imp

        market_skills = self.taxonomy['market_skills_ranked']
        
        # Calculate median demand threshold for split
        all_demands = [s['market_penetration_pct'] for s in market_skills]
        demand_threshold = float(np.median(all_demands)) if all_demands else 10.0
        # If median is low, use 15% as standard threshold
        demand_threshold = max(12.0, demand_threshold)
        impact_threshold = 0.18 # Based on random forest feature importance split (0.20 is average for 5 features)

        matrix_items = []
        quadrant_counts = {'Q1_Core_Bets': 0, 'Q2_Table_Stakes': 0, 'Q3_Elite_Differentiators': 0, 'Q4_Low_Priority': 0}

        for s_info in market_skills:
            skill = s_info['skill']
            demand_pct = s_info['market_penetration_pct']
            
            # Outcome impact score normalized (0 to 100)
            base_imp = skill_impact_map.get(skill, 0.15)
            # Adjust impact slightly with salary premium
            premium_adj = max(-0.05, min(0.10, s_info['salary_premium_lpa'] / 50.0))
            impact_score = round((base_imp + premium_adj) * 100, 1)

            # Assign Quadrant
            if demand_pct >= demand_threshold and (base_imp + premium_adj) >= impact_threshold:
                quadrant = "Q1: Strategic Core Bets"
                q_code = "Q1_Core_Bets"
                action = "Must master; drives high hiring volume AND top compensation outcomes."
            elif demand_pct >= demand_threshold and (base_imp + premium_adj) < impact_threshold:
                quadrant = "Q2: Table Stakes / Commodity"
                q_code = "Q2_Table_Stakes"
                action = "Foundational prerequisite; expected by everyone but offers limited compensation premium."
            elif demand_pct < demand_threshold and (base_imp + premium_adj) >= impact_threshold:
                quadrant = "Q3: Elite Differentiators"
                q_code = "Q3_Elite_Differentiators"
                action = "High pricing power; specialized skills commanding top-decile compensation."
            else:
                quadrant = "Q4: Specialized / Lower Priority"
                q_code = "Q4_Low_Priority"
                action = "Learn as situational support; not a primary career catalyst."

            quadrant_counts[q_code] += 1
            matrix_items.append({
                'skill': skill,
                'category': s_info['category'],
                'market_demand_pct': demand_pct,
                'success_impact_score': impact_score,
                'salary_premium_lpa': s_info['salary_premium_lpa'],
                'job_postings_count': s_info['job_postings_count'],
                'quadrant': quadrant,
                'quadrant_code': q_code,
                'strategic_action': action
            })

        matrix_payload = {
            'thresholds': {
                'demand_threshold_pct': demand_threshold,
                'impact_threshold_score': round(impact_threshold * 100, 1)
            },
            'quadrant_distribution': quadrant_counts,
            'skills_matrix': matrix_items
        }

        out_fp = os.path.join(self.proc_dir, 'market_success_matrix.json')
        with open(out_fp, 'w', encoding='utf-8') as f:
            json.dump(matrix_payload, f, indent=2)

        print(f"[OK] Market x Success Intelligence Matrix saved at {out_fp}")
        return matrix_payload


if __name__ == '__main__':
    proc_dir = r'C:\Users\chitr_mzkaj0t\.gemini\antigravity\scratch\workforce_intelligence\data\processed'
    engine = MarketSuccessMatrixEngine(proc_dir)
    res = engine.build_matrix()
    print("Market x Success Matrix Quadrant Counts:", res['quadrant_distribution'])
    for q in ['Q1: Strategic Core Bets', 'Q3: Elite Differentiators']:
        print(f"\nTop skills in {q}:")
        matching = [s['skill'] for s in res['skills_matrix'] if s['quadrant'] == q][:4]
        print(" ", ", ".join(matching))
