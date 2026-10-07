"""
Workforce Intelligence Platform - Skill Gap Engine & Heatmap
=============================================================
Locked Feature #9: Converts analytics into personalized action:
- Performs rigorous gap diffing between Candidate Skill Vector and Role Benchmarks
- Classifies gap severity: Critical Shortfall, Moderate Deficit, or Competency Match
- Generates Skill Gap Heatmap matrix across all 10 analytics roles
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


class SkillGapEngine:
    def __init__(self, processed_data_dir: str):
        self.proc_dir = processed_data_dir
        with open(os.path.join(self.proc_dir, 'role_skill_profiles.json'), 'r', encoding='utf-8') as f:
            self.role_profiles = json.load(f)
        with open(os.path.join(self.proc_dir, 'master_skill_taxonomy.json'), 'r', encoding='utf-8') as f:
            self.taxonomy = json.load(f)

    def analyze_candidate_gap(self, target_role: str, candidate_skills: list, candidate_ratings: dict = None):
        """Analyzes skill deficiencies of a candidate relative to target role requirements."""
        if target_role not in self.role_profiles:
            target_role = 'Data Scientist'

        role_info = self.role_profiles[target_role]
        cand_skill_set = set(candidate_skills)
        ratings = candidate_ratings or {}
        
        breakdown = []
        total_benchmark_weight = 0
        candidate_coverage_weight = 0

        for s_obj in role_info['top_skills']:
            skill_name = s_obj['skill']
            market_req_pct = s_obj['penetration_pct']
            total_benchmark_weight += market_req_pct
            
            is_present = skill_name in cand_skill_set
            user_rating = float(ratings.get(skill_name, 4.0 if is_present else 1.0))
            
            # Target benchmark proficiency (scaled 1-5 based on market penetration)
            target_benchmark_level = 3.0 + (market_req_pct / 100.0) * 2.0
            
            gap_magnitude = round(max(0.0, target_benchmark_level - user_rating), 2)
            
            if is_present:
                candidate_coverage_weight += market_req_pct * (user_rating / target_benchmark_level)

            if not is_present:
                if market_req_pct >= 50.0:
                    status = "Critical Shortfall"
                    severity = "High"
                else:
                    status = "Secondary Deficit"
                    severity = "Moderate"
            else:
                if user_rating >= target_benchmark_level:
                    status = "Strong Competency"
                    severity = "None"
                else:
                    status = "Needs Further Depth"
                    severity = "Low"

            breakdown.append({
                'skill': skill_name,
                'market_importance_pct': market_req_pct,
                'target_benchmark_level': round(target_benchmark_level, 1),
                'candidate_current_level': round(user_rating, 1),
                'gap_magnitude': gap_magnitude,
                'status': status,
                'severity': severity
            })

        overall_readiness_pct = round((candidate_coverage_weight / total_benchmark_weight) * 100, 1) if total_benchmark_weight > 0 else 0.0
        
        # Sort gaps by gap magnitude * market importance
        prioritized_gaps = sorted(
            [b for b in breakdown if b['gap_magnitude'] > 0],
            key=lambda x: x['gap_magnitude'] * x['market_importance_pct'],
            reverse=True
        )

        return {
            'target_role': target_role,
            'role_sample_size': role_info['total_postings'],
            'overall_role_readiness_pct': min(100.0, max(0.0, overall_readiness_pct)),
            'total_skills_evaluated': len(breakdown),
            'critical_gaps_count': sum(1 for b in breakdown if b['severity'] == 'High'),
            'skill_gap_details': breakdown,
            'top_priority_gaps': prioritized_gaps[:5]
        }

    def generate_cross_role_heatmap(self, candidate_skills: list):
        """Generates a matrix of readiness and gaps across ALL 10 analytics roles for heatmap visualization."""
        matrix = []
        cand_set = set(candidate_skills)
        
        for role, r_info in self.role_profiles.items():
            req_top = r_info['top_skills'][:8]
            matched = sum(1 for s in req_top if s['skill'] in cand_set)
            readiness = round((matched / len(req_top)) * 100, 1)
            
            skills_status = {}
            for s in req_top:
                skills_status[s['skill']] = {
                    'possessed': s['skill'] in cand_set,
                    'market_demand': s['penetration_pct']
                }

            matrix.append({
                'role': role,
                'readiness_pct': readiness,
                'matched_count': matched,
                'total_required': len(req_top),
                'skills_status': skills_status
            })

        matrix = sorted(matrix, key=lambda x: x['readiness_pct'], reverse=True)
        return matrix


if __name__ == '__main__':
    proc_dir = r'C:\Users\chitr_mzkaj0t\.gemini\antigravity\scratch\workforce_intelligence\data\processed'
    engine = SkillGapEngine(proc_dir)
    res = engine.analyze_candidate_gap(
        target_role='Data Scientist',
        candidate_skills=['SQL', 'Tableau', 'Excel / Advanced Excel'],
        candidate_ratings={'SQL': 4.5, 'Tableau': 4.0, 'Excel / Advanced Excel': 4.8}
    )
    print(f"[OK] Skill Gap Analysis for {res['target_role']} (Readiness: {res['overall_role_readiness_pct']}%):")
    for g in res['top_priority_gaps']:
        print(f"  Gap: {g['skill']} - Target {g['target_benchmark_level']}, Current {g['candidate_current_level']}, Status: {g['status']}")
