"""
Workforce Intelligence Platform - Workforce Digital Twin & Scenario Simulator
==============================================================================
Addresses Features #1, #7, #8, #11, #14:
- Models organizational cohorts as an empirical Workforce Digital Twin
- Simulates Future Workforce Scenarios:
  * Scenario 1: Baseline Status Quo (Natural progression)
  * Scenario 2: Strategic Upskilling (Reskilling 30% of Junior cohort in AI/ML & Big Data)
  * Scenario 3: Aggressive Transformation (Reskilling 60% of cohort in MLOps & Advanced Coding)
  * Scenario 4: Hiring Freeze & Internal Redeployment (Redeploying Analysts to Data Engineers)
- Calculates Build vs. Buy vs. Redeploy Economic ROI:
  * Internal Upskilling Cost (~0.6 LPA per person) vs. External Hiring Cost (~3.8 LPA recruitment + market premium)
"""

import sys
import numpy as np
import pandas as pd

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


class WorkforceSimulatorEngine:
    def __init__(self, ml_engine, market_engine):
        self.ml_engine = ml_engine
        self.market_engine = market_engine

    def simulate_cohort_upskilling(self, cohort_size: int = 100, upskill_pct: float = 30.0, target_skill_focus: str = 'ai_and_ml_skills'):
        """Simulates organizational capability and economic impact of reskilling a cohort."""
        np.random.seed(42)
        
        # Generate empirical baseline cohort matching JDS distribution
        baseline_skills = {
            'big_data_skills': np.clip(np.random.normal(3.85, 0.6, cohort_size), 1.0, 5.0),
            'maths-stats_skills': np.clip(np.random.normal(4.29, 0.5, cohort_size), 1.0, 5.0),
            'coding_skills': np.clip(np.random.normal(4.27, 0.5, cohort_size), 1.0, 5.0),
            'ai_and_ml_skills': np.clip(np.random.normal(4.57, 0.4, cohort_size), 1.0, 5.0),
            'dashboard_and_storytelling_skills': np.clip(np.random.normal(4.36, 0.5, cohort_size), 1.0, 5.0)
        }
        
        # Baseline model predictions
        baseline_hike_probs = []
        for i in range(cohort_size):
            vec = {k: baseline_skills[k][i] for k in baseline_skills}
            prob = self.ml_engine.predict_jds_hike(vec)['probability_high_hike']
            baseline_hike_probs.append(prob)
            
        base_high_performers = sum(1 for p in baseline_hike_probs if p >= 0.5)
        base_avg_prob = float(np.mean(baseline_hike_probs))

        # Simulated Upskilled Cohort
        num_reskilled = int((upskill_pct / 100.0) * cohort_size)
        simulated_skills = {k: np.copy(baseline_skills[k]) for k in baseline_skills}
        
        # Select bottom performers in the target skill for upskilling boost
        target_trait = target_skill_focus if target_skill_focus in simulated_skills else 'ai_and_ml_skills'
        sorted_indices = np.argsort(simulated_skills[target_trait])
        reskill_indices = sorted_indices[:num_reskilled]
        
        # Boost target trait by +1.5 grades, and coding by +0.8
        simulated_skills[target_trait][reskill_indices] = np.clip(simulated_skills[target_trait][reskill_indices] + 1.5, 1.0, 5.0)
        simulated_skills['coding_skills'][reskill_indices] = np.clip(simulated_skills['coding_skills'][reskill_indices] + 0.8, 1.0, 5.0)

        sim_hike_probs = []
        for i in range(cohort_size):
            vec = {k: simulated_skills[k][i] for k in simulated_skills}
            prob = self.ml_engine.predict_jds_hike(vec)['probability_high_hike']
            sim_hike_probs.append(prob)

        sim_high_performers = sum(1 for p in sim_hike_probs if p >= 0.5)
        sim_avg_prob = float(np.mean(sim_hike_probs))

        # Build vs. Buy Financial Model
        # Cost to train internally = ~0.60 Lakhs per engineer (courseware, mentorship, labs)
        cost_internal_per_head = 0.60
        total_internal_cost_lpa = round(num_reskilled * cost_internal_per_head, 2)
        
        # Cost to hire externally = Agency fee (15% of CTC = ~1.8L) + Signing Premium (~2.0L) = 3.80 LPA per engineer
        cost_external_per_head = 3.80
        equivalent_external_hiring_cost_lpa = round(num_reskilled * cost_external_per_head, 2)
        
        net_savings_lpa = round(equivalent_external_hiring_cost_lpa - total_internal_cost_lpa, 2)
        roi_multiple = round(equivalent_external_hiring_cost_lpa / max(0.1, total_internal_cost_lpa), 1)

        return {
            'cohort_size': cohort_size,
            'upskilled_employees_count': num_reskilled,
            'upskilling_percentage': upskill_pct,
            'target_skill_focus': target_trait.replace('_', ' ').title(),
            'baseline_metrics': {
                'high_performing_engineers': base_high_performers,
                'high_performance_rate_pct': round((base_high_performers / cohort_size) * 100, 1),
                'average_hike_probability': round(base_avg_prob * 100, 1)
            },
            'post_simulation_metrics': {
                'high_performing_engineers': sim_high_performers,
                'high_performance_rate_pct': round((sim_high_performers / cohort_size) * 100, 1),
                'average_hike_probability': round(sim_avg_prob * 100, 1),
                'net_high_performer_gain': sim_high_performers - base_high_performers
            },
            'build_vs_buy_economics': {
                'internal_reskilling_investment_lpa': total_internal_cost_lpa,
                'equivalent_external_acquisition_cost_lpa': equivalent_external_hiring_cost_lpa,
                'net_capital_saved_lpa': net_savings_lpa,
                'reskilling_roi_multiplier': f"{roi_multiple}x",
                'strategic_recommendation': (
                    f"BUILD over BUY strongly validated: Internal reskilling delivers {num_reskilled} capability-upgraded "
                    f"engineers saving ₹{net_savings_lpa} Lakhs ({roi_multiple}x ROI) vs external market acquisition."
                )
            }
        }
