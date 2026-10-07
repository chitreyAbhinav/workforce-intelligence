"""
Workforce Intelligence Platform - Skill Investment Optimizer
=============================================================
Hero Feature #3 & Locked Feature #10:
"If I can improve only one skill, which one gives me the strongest strategic value?"

Mathematical Framework:
Strategic Skill ROI(S) = [Marginal ML Hike Probability Gain (Delta P)]
                       * [Market Demand Multiplier (Open Positions & Penetration)]
                       * [Salary Premium Factor (LPA)]
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


class SkillInvestmentOptimizer:
    def __init__(self, processed_data_dir: str, ml_engine):
        self.proc_dir = processed_data_dir
        self.ml_engine = ml_engine
        with open(os.path.join(self.proc_dir, 'master_skill_taxonomy.json'), 'r', encoding='utf-8') as f:
            self.taxonomy = json.load(f)

        # Mapping between general skills and the JDS technical traits
        self.skill_to_feature_mapping = {
            'Python': 'coding_skills',
            'SQL': 'coding_skills',
            'R': 'maths-stats_skills',
            'SAS': 'coding_skills',
            'Machine Learning': 'ai_and_ml_skills',
            'Deep Learning': 'ai_and_ml_skills',
            'Generative AI / LLMs': 'ai_and_ml_skills',
            'Statistical Modeling': 'maths-stats_skills',
            'Spark / PySpark': 'big_data_skills',
            'Hadoop': 'big_data_skills',
            'ETL Pipelines': 'big_data_skills',
            'Tableau': 'dashboard_and_storytelling_skills',
            'Power BI': 'dashboard_and_storytelling_skills',
            'Data Visualization': 'dashboard_and_storytelling_skills',
            'Business Acumen': 'dashboard_and_storytelling_skills'
        }

    def optimize_skill_investment(self, current_skills_1to5: dict):
        """Calculates marginal return on investment for upgrading each skill by +1.0 grade."""
        base_scores = {
            'big_data_skills': float(current_skills_1to5.get('big_data_skills', 3.0)),
            'maths-stats_skills': float(current_skills_1to5.get('maths-stats_skills', 3.0)),
            'coding_skills': float(current_skills_1to5.get('coding_skills', 3.0)),
            'ai_and_ml_skills': float(current_skills_1to5.get('ai_and_ml_skills', 3.0)),
            'dashboard_and_storytelling_skills': float(current_skills_1to5.get('dashboard_and_storytelling_skills', 3.0))
        }

        base_res = self.ml_engine.predict_jds_hike(base_scores)
        base_hike_prob = base_res['probability_high_hike']

        # 1. Evaluate Trait Level Marginal Return
        trait_evaluations = []
        for trait, val in base_scores.items():
            if val < 5.0:
                upgraded = base_scores.copy()
                upgraded[trait] = min(5.0, val + 1.0)
                new_prob = self.ml_engine.predict_jds_hike(upgraded)['probability_high_hike']
                prob_gain = round(new_prob - base_hike_prob, 3)
            else:
                prob_gain = 0.0

            trait_evaluations.append({
                'skill_trait': trait,
                'display_name': trait.replace('_', ' ').title(),
                'current_level': round(val, 1),
                'upgraded_level': round(min(5.0, val + 1.0), 1),
                'marginal_hike_gain_pct': round(prob_gain * 100, 1)
            })

        # 2. Evaluate Specific Technology Skills
        skill_market_map = {s['skill']: s for s in self.taxonomy['market_skills_ranked']}
        tech_evaluations = []

        for skill, trait in self.skill_to_feature_mapping.items():
            m_info = skill_market_map.get(skill)
            if not m_info:
                continue

            curr_val = base_scores.get(trait, 3.0)
            if curr_val < 5.0:
                upgraded = base_scores.copy()
                upgraded[trait] = min(5.0, curr_val + 1.0)
                new_prob = self.ml_engine.predict_jds_hike(upgraded)['probability_high_hike']
                delta_prob = max(0.005, new_prob - base_hike_prob)
            else:
                delta_prob = 0.005

            demand_weight = m_info['market_penetration_pct'] / 100.0
            premium_weight = max(0.1, m_info['salary_premium_lpa'] + 2.0)
            
            # Unified Strategic ROI Score (normalized 0 - 100 scale)
            raw_roi = (delta_prob * 100.0) * 0.45 + (demand_weight * 100.0) * 0.35 + (premium_weight * 5.0) * 0.20
            strategic_roi = round(min(100.0, max(5.0, raw_roi * 1.5)), 1)

            tech_evaluations.append({
                'skill': skill,
                'category': m_info['category'],
                'associated_trait': trait.replace('_', ' ').title(),
                'current_trait_level': round(curr_val, 1),
                'strategic_roi_score': strategic_roi,
                'marginal_hike_gain_pct': round(delta_prob * 100, 1),
                'market_demand_postings': m_info['job_postings_count'],
                'market_salary_premium_lpa': m_info['salary_premium_lpa'],
                'recommendation_tier': 'Top Priority (Tier 1)' if strategic_roi >= 70 else ('High Value (Tier 2)' if strategic_roi >= 45 else 'Supporting (Tier 3)')
            })

        tech_evaluations = sorted(tech_evaluations, key=lambda x: x['strategic_roi_score'], reverse=True)

        return {
            'baseline_hike_probability': round(base_hike_prob * 100, 1),
            'top_recommended_skill': tech_evaluations[0]['skill'] if tech_evaluations else 'Machine Learning',
            'top_recommendation_reason': (
                f"Upgrading '{tech_evaluations[0]['skill']}' delivers the maximum composite strategic return "
                f"(ROI Score: {tech_evaluations[0]['strategic_roi_score']}/100) due to +{tech_evaluations[0]['marginal_hike_gain_pct']}% "
                f"predicted hike uplift combined with {tech_evaluations[0]['market_demand_postings']} active market postings."
            ),
            'trait_level_returns': sorted(trait_evaluations, key=lambda x: x['marginal_hike_gain_pct'], reverse=True),
            'skill_investment_rankings': tech_evaluations
        }
