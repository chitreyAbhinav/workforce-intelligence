"""
Workforce Intelligence Platform - Role-Skill Adjacency Network Graph
=====================================================================
Constructs the graph network linking roles and skills:
- Calculates skill similarity distances between roles (Cosine & Jaccard)
- Identifies bridge skills between adjacent career roles
- Builds interactive graph payload for D3.js / network visualization
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


class RoleSkillGraphEngine:
    def __init__(self, processed_data_dir: str):
        self.proc_dir = processed_data_dir
        with open(os.path.join(self.proc_dir, 'role_skill_profiles.json'), 'r', encoding='utf-8') as f:
            self.role_profiles = json.load(f)
        with open(os.path.join(self.proc_dir, 'master_skill_taxonomy.json'), 'r', encoding='utf-8') as f:
            self.taxonomy = json.load(f)
        with open(os.path.join(self.proc_dir, 'market_intelligence_report.json'), 'r', encoding='utf-8') as f:
            self.market_report = json.load(f)

    def compute_role_adjacencies(self):
        """Computes distance matrix and bridge skills between all analytics roles."""
        roles = list(self.role_profiles.keys())
        all_skills = [s['skill'] for s in self.taxonomy['market_skills_ranked']]
        
        # Build vector representations of roles based on skill penetration
        role_vectors = {}
        for r in roles:
            vec = {s: 0.0 for s in all_skills}
            for s_info in self.role_profiles[r]['top_skills']:
                vec[s_info['skill']] = s_info['penetration_pct'] / 100.0
            role_vectors[r] = np.array([vec[s] for s in all_skills])

        # Cosine similarity matrix
        sim_matrix = {}
        transitions = []
        for i, r1 in enumerate(roles):
            sim_matrix[r1] = {}
            v1 = role_vectors[r1]
            norm1 = np.linalg.norm(v1)
            for j, r2 in enumerate(roles):
                if i == j:
                    sim_matrix[r1][r2] = 1.0
                    continue
                v2 = role_vectors[r2]
                norm2 = np.linalg.norm(v2)
                if norm1 > 0 and norm2 > 0:
                    cos_sim = float(np.dot(v1, v2) / (norm1 * norm2))
                else:
                    cos_sim = 0.0
                sim_matrix[r1][r2] = round(cos_sim, 3)
                
                # Identify transition viability
                if i < j and cos_sim >= 0.40:
                    # Find bridge skills (skills shared with high penetration in both)
                    r1_skills = {s['skill']: s['penetration_pct'] for s in self.role_profiles[r1]['top_skills']}
                    r2_skills = {s['skill']: s['penetration_pct'] for s in self.role_profiles[r2]['top_skills']}
                    common = set(r1_skills.keys()).intersection(set(r2_skills.keys()))
                    bridge = sorted(list(common), key=lambda s: (r1_skills[s] + r2_skills[s]), reverse=True)[:3]
                    
                    transitions.append({
                        'source_role': r1,
                        'target_role': r2,
                        'similarity_score': round(cos_sim, 3),
                        'transition_difficulty': 'Low' if cos_sim >= 0.70 else ('Moderate' if cos_sim >= 0.50 else 'High'),
                        'bridge_skills': bridge
                    })

        transitions = sorted(transitions, key=lambda x: x['similarity_score'], reverse=True)

        # Graph node generation
        salary_lookup = {r['role']: r['median_lpa'] for r in self.market_report['role_benchmarks']}
        nodes = []
        for r in roles:
            nodes.append({
                'id': r,
                'label': r,
                'median_salary_lpa': salary_lookup.get(r, 10.0),
                'job_postings': self.role_profiles[r]['total_postings'],
                'top_skills': [s['skill'] for s in self.role_profiles[r]['top_skills'][:4]]
            })

        graph_payload = {
            'nodes': nodes,
            'edges': [
                {
                    'source': t['source_role'],
                    'target': t['target_role'],
                    'weight': t['similarity_score'],
                    'difficulty': t['transition_difficulty'],
                    'bridge_skills': t['bridge_skills']
                }
                for t in transitions
            ],
            'similarity_matrix': sim_matrix
        }

        out_fp = os.path.join(self.proc_dir, 'role_skill_network_graph.json')
        with open(out_fp, 'w', encoding='utf-8') as f:
            json.dump(graph_payload, f, indent=2)

        return graph_payload


if __name__ == '__main__':
    proc_dir = r'C:\Users\chitr_mzkaj0t\.gemini\antigravity\scratch\workforce_intelligence\data\processed'
    engine = RoleSkillGraphEngine(proc_dir)
    res = engine.compute_role_adjacencies()
    print(f"[OK] Generated Role-Skill Network Graph with {len(res['nodes'])} nodes and {len(res['edges'])} edges.")
    print("Top 3 natural career transitions:")
    for e in res['edges'][:3]:
        print(f"  {e['source']} <-> {e['target']}: Similarity {e['weight']} (Bridge Skills: {', '.join(e['bridge_skills'])})")
