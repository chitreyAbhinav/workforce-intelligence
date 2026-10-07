"""
Workforce Intelligence Platform - Career Objective Optimizer
=============================================================
Locked Feature #12: Makes career navigation dynamic and goal-tailored.
Optimizes candidate strategy across three distinct objective functions:
1. 'MAX_HIKE': Maximize short-term compensation growth and hike probability
2. 'MAX_SENIORITY': Maximize long-term progression into Senior Leadership / Architecture
3. 'MIN_EFFORT': Find the fastest, lowest-friction career path requiring minimal upskilling
"""

import sys

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


class CareerObjectiveOptimizer:
    def __init__(self, gps_engine, skill_opt_engine, ml_engine):
        self.gps = gps_engine
        self.skill_opt = skill_opt_engine
        self.ml_engine = ml_engine

    def optimize_career_plan(self, current_role: str, user_skills: list, current_exp: float, current_salary_lpa: float, objective: str = 'MAX_HIKE'):
        """Generates tailored strategic career recommendation based on target objective."""
        pathways = self.gps.find_career_pathways(
            current_role=current_role,
            user_skills=user_skills,
            current_exp=current_exp,
            current_salary_lpa=current_salary_lpa
        )['recommended_pathways']

        obj_upper = objective.upper()

        if obj_upper == 'MAX_HIKE':
            # Rank strictly by expected salary uplift (LPA & %)
            ranked = sorted(pathways, key=lambda x: x['salary_delta_lpa'], reverse=True)
            top_path = ranked[0]
            strategy_name = "Aggressive Salary Maximization Strategy"
            rationale = (
                f"Prioritizes maximum immediate economic expansion. Recommends target role '{top_path['target_role']}' "
                f"delivering an expected uplift of +{top_path['salary_delta_lpa']} LPA (+{top_path['salary_uplift_pct']}%) "
                f"with a feasible transition window."
            )
            key_levers = top_path['missing_critical_skills'][:2] if top_path['missing_critical_skills'] else ['Domain Leadership']

        elif obj_upper == 'MAX_SENIORITY':
            # Filter toward Senior / Architect roles, rank by seniority payoff
            senior_candidates = [p for p in pathways if 'Senior' in p['target_role'] or 'Architect' in p['target_role'] or 'Scientist' in p['target_role']]
            if not senior_candidates:
                senior_candidates = pathways
            ranked = sorted(senior_candidates, key=lambda x: (x['target_median_salary_lpa'] * 0.6 + x['feasibility_pct'] * 0.4), reverse=True)
            top_path = ranked[0]
            strategy_name = "Executive & Senior Technical Leadership Pathway"
            rationale = (
                f"Aligns technical and soft-skill mastery toward '{top_path['target_role']}'. "
                f"Focuses on Big Five leadership competencies (High Conscientiousness & Emotional Stability) "
                f"combined with strategic technical architecture capabilities."
            )
            key_levers = ["Strategic Architecture", "End-to-End Ownership"] + top_path['missing_critical_skills'][:2]

        elif obj_upper == 'MIN_EFFORT':
            # Rank strictly by highest feasibility (lowest skill distance)
            ranked = sorted(pathways, key=lambda x: x['feasibility_pct'], reverse=True)
            top_path = ranked[0]
            strategy_name = "Frictionless Natural Pivot Strategy"
            rationale = (
                f"Maximizes immediate transition velocity. Recommends '{top_path['target_role']}' with "
                f"{top_path['feasibility_pct']}% structural readiness, requiring acquisition of only "
                f"{len(top_path['missing_critical_skills'])} new skills while still capturing +{top_path['salary_delta_lpa']} LPA."
            )
            key_levers = top_path['missing_critical_skills'][:2] if top_path['missing_critical_skills'] else ['Immediate Role Applications']

        else:
            ranked = pathways
            top_path = ranked[0]
            strategy_name = "Balanced Career Progression"
            rationale = "Optimizes simultaneously for transition safety and financial uplift."
            key_levers = top_path['missing_critical_skills'][:2]

        return {
            'selected_objective': objective,
            'strategy_name': strategy_name,
            'primary_recommendation': top_path,
            'strategic_rationale': rationale,
            'key_development_levers': key_levers,
            'ranked_alternatives': ranked[1:4]
        }
