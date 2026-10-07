"""
Workforce Intelligence Platform - AI Career GPS Engine
======================================================
Hero Feature #1: "Where can I go from here?"
- Computes optimal transition paths from candidate's current state to target roles
- Quantifies Transition Feasibility %, Expected Salary Uplift (LPA & %), and Effort Index
- Identifies Exact Critical Skill Gaps needed to unlock each career step
- Generates Chronological Career Milestones & Learning Roadmap
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


class AICareerGPSEngine:
    def __init__(self, processed_data_dir: str):
        self.proc_dir = processed_data_dir
        with open(os.path.join(self.proc_dir, 'role_skill_profiles.json'), 'r', encoding='utf-8') as f:
            self.role_profiles = json.load(f)
        with open(os.path.join(self.proc_dir, 'market_intelligence_report.json'), 'r', encoding='utf-8') as f:
            self.market_report = json.load(f)
        with open(os.path.join(self.proc_dir, 'role_skill_network_graph.json'), 'r', encoding='utf-8') as f:
            self.network_graph = json.load(f)

        self.salary_lookup = {r['role']: r for r in self.market_report['role_benchmarks']}

    def find_career_pathways(self, current_role: str, user_skills: list, current_exp: float = 3.0, current_salary_lpa: float = None):
        """Discovers and ranks all next-stage career transition destinations from current role."""
        if current_role not in self.role_profiles:
            current_role = 'Data Analyst'

        cur_benchmark = self.salary_lookup.get(current_role, {'median_lpa': 8.0, 'mean_lpa': 8.5})
        cur_salary = current_salary_lpa if (current_salary_lpa and current_salary_lpa > 0) else cur_benchmark['median_lpa']
        
        sim_scores = self.network_graph['similarity_matrix'].get(current_role, {})
        user_skills_set = set(user_skills)
        
        destinations = []
        for target_role, t_profile in self.role_profiles.items():
            if target_role == current_role:
                continue
                
            t_benchmark = self.salary_lookup.get(target_role, {'median_lpa': 12.0, 'mean_lpa': 13.0})
            target_salary = t_benchmark['median_lpa']
            salary_delta_lpa = round(target_salary - cur_salary, 1)
            salary_uplift_pct = round((salary_delta_lpa / cur_salary) * 100, 1)
            
            # Target required top skills
            req_skills = [s['skill'] for s in t_profile['top_skills'][:6]]
            req_skill_weights = {s['skill']: s['penetration_pct'] for s in t_profile['top_skills'][:6]}
            
            # Skill matches & gaps
            matching_skills = [s for s in req_skills if s in user_skills_set]
            missing_skills = [s for s in req_skills if s not in user_skills_set]
            
            # Weighted skill match score
            total_req_weight = sum(req_skill_weights.values())
            matched_weight = sum(req_skill_weights[s] for s in matching_skills)
            skill_readiness_pct = round((matched_weight / total_req_weight) * 100, 1) if total_req_weight > 0 else 50.0
            
            # Structural transition feasibility combining graph distance and user skill overlap
            graph_sim = sim_scores.get(target_role, 0.5)
            feasibility_pct = round(0.55 * skill_readiness_pct + 0.45 * (graph_sim * 100), 1)
            
            # Categorize recommendation tier
            if feasibility_pct >= 70:
                tier = "Immediate Natural Transition (0-3 Months)"
                difficulty = "Low"
            elif feasibility_pct >= 45:
                tier = "High-Uplift Upskilling Pathway (3-6 Months)"
                difficulty = "Moderate"
            else:
                tier = "Strategic Pivot / Long-Term Leap (6-12 Months)"
                difficulty = "High"

            # Chronological milestones
            milestones = []
            if missing_skills:
                milestones.append({
                    'phase': 'Phase 1: Foundational Bridge (Months 1-2)',
                    'objective': f"Acquire core missing skill: {missing_skills[0]}",
                    'focus': f"Target {missing_skills[0]} applied projects and workflow integration"
                })
                if len(missing_skills) > 1:
                    milestones.append({
                        'phase': 'Phase 2: Advanced Competency (Months 3-4)',
                        'objective': f"Master {', '.join(missing_skills[1:3])}",
                        'focus': "Build end-to-end portfolio artifacts showcasing domain proficiency"
                    })
                milestones.append({
                    'phase': 'Phase 3: Market Transition (Months 5-6)',
                    'objective': f"Position resume and interview for {target_role}",
                    'focus': f"Target companies with median compensation of {target_salary} LPA"
                })
            else:
                milestones.append({
                    'phase': 'Direct Transition Ready',
                    'objective': f"Immediate eligibility for {target_role} roles",
                    'focus': f"Negotiate compensation toward 75th percentile ({t_benchmark.get('p75_lpa', target_salary * 1.2)} LPA)"
                })

            destinations.append({
                'target_role': target_role,
                'target_median_salary_lpa': target_salary,
                'salary_delta_lpa': salary_delta_lpa,
                'salary_uplift_pct': salary_uplift_pct,
                'feasibility_pct': feasibility_pct,
                'difficulty': difficulty,
                'pathway_tier': tier,
                'skill_readiness_pct': skill_readiness_pct,
                'matching_skills': matching_skills,
                'missing_critical_skills': missing_skills,
                'milestones': milestones
            })

        # Rank by composite score: 60% Feasibility + 40% Salary Uplift
        def composite_rank(x):
            norm_uplift = max(0, x['salary_uplift_pct']) / 100.0
            return (0.60 * (x['feasibility_pct'] / 100.0)) + (0.40 * min(1.5, norm_uplift))

        destinations = sorted(destinations, key=composite_rank, reverse=True)
        
        return {
            'candidate_profile': {
                'current_role': current_role,
                'current_salary_lpa': cur_salary,
                'current_experience_years': current_exp,
                'skills_possessed': user_skills
            },
            'recommended_pathways': destinations
        }


if __name__ == '__main__':
    proc_dir = r'C:\Users\chitr_mzkaj0t\.gemini\antigravity\scratch\workforce_intelligence\data\processed'
    gps = AICareerGPSEngine(proc_dir)
    test_res = gps.find_career_pathways(
        current_role='Data Analyst',
        user_skills=['SQL', 'Excel / Advanced Excel', 'Tableau', 'Power BI'],
        current_exp=3.0,
        current_salary_lpa=7.5
    )
    print(f"[OK] Career GPS Pathfinding Complete for {test_res['candidate_profile']['current_role']} (Current: {test_res['candidate_profile']['current_salary_lpa']} LPA):")
    for p in test_res['recommended_pathways'][:3]:
        print(f"  -> {p['target_role']}: Feasibility {p['feasibility_pct']}%, Target {p['target_median_salary_lpa']} LPA (+{p['salary_delta_lpa']} LPA / +{p['salary_uplift_pct']}%), Missing: {p['missing_critical_skills']}")
