"""
AI-Assisted & Metamorphic Property Testing Suite
=================================================
Verifies fundamental behavioral and mathematical invariants across ML models and algorithms:
1. Metamorphic Invariant 1: Monotonicity of Technical Skill Upgrades
2. Metamorphic Invariant 2: Directional Symmetry of Neuroticism Penalty
3. Metamorphic Invariant 3: Perfect Competency Identity (Zero Skill Gap)
4. Metamorphic Invariant 4: Graph Distance Symmetry Principle
5. Metamorphic Invariant 5: Build vs. Buy Economic Conservation Law
"""

import os
import pytest
import numpy as np
from src.ml_success_models import MLSuccessModelsEngine
from src.role_skill_graph import RoleSkillGraphEngine
from src.skill_gap_engine import SkillGapEngine
from src.workforce_simulator import WorkforceSimulatorEngine
from src.market_intelligence import MarketIntelligenceEngine

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC_DIR = os.path.join(BASE_DIR, 'data', 'processed')


@pytest.fixture(scope="module")
def ai_test_env():
    ml = MLSuccessModelsEngine(PROC_DIR)
    ml.train_jds_skill_model()
    ml.train_sds_personality_model()
    market = MarketIntelligenceEngine(PROC_DIR)
    graph = RoleSkillGraphEngine(PROC_DIR)
    gap = SkillGapEngine(PROC_DIR)
    sim = WorkforceSimulatorEngine(ml, market)
    return ml, graph, gap, sim


def test_invariant_1_skill_monotonicity(ai_test_env):
    """INVARIANT 1: Increasing a technical skill must monotonically not decrease hike probability."""
    ml, _, _, _ = ai_test_env
    base_candidate = {
        'big_data_skills': 3.0,
        'maths-stats_skills': 3.0,
        'coding_skills': 2.0,
        'ai_and_ml_skills': 3.0,
        'dashboard_and_storytelling_skills': 3.0
    }
    
    p_low = ml.predict_jds_hike(base_candidate)['probability_high_hike']
    
    upgraded_candidate = base_candidate.copy()
    upgraded_candidate['coding_skills'] = 5.0
    p_high = ml.predict_jds_hike(upgraded_candidate)['probability_high_hike']
    
    assert p_high >= p_low, (
        f"Metamorphic Monotonicity Invariant Violated: P(hike|coding=2.0)={p_low} "
        f"was unexpectedly greater than P(hike|coding=5.0)={p_high}"
    )


def test_invariant_2_neuroticism_penalty(ai_test_env):
    """INVARIANT 2: Lowering neuroticism (higher emotional stability) must not decrease senior success probability."""
    ml, _, _, _ = ai_test_env
    high_anxiety_candidate = {
        'neuroticism': 0.85,
        'extraversion': 0.60,
        'openness_to_experience': 0.70,
        'agreeableness': 0.65,
        'conscientiousness': 0.75
    }
    
    p_anxious = ml.predict_sds_success(high_anxiety_candidate)['probability_high_success']
    
    calm_candidate = high_anxiety_candidate.copy()
    calm_candidate['neuroticism'] = 0.15
    p_calm = ml.predict_sds_success(calm_candidate)['probability_high_success']
    
    assert p_calm >= p_anxious, (
        f"Behavioral Invariant Violated: P(success|neuroticism=0.85)={p_anxious} "
        f"was unexpectedly greater than P(success|neuroticism=0.15)={p_calm}"
    )


def test_invariant_3_identity_skill_gap(ai_test_env):
    """INVARIANT 3: If candidate possesses 100% of target role benchmark skills at top score, gap must be 0."""
    _, _, gap, _ = ai_test_env
    target_role = 'Data Scientist'
    role_skills = [s['skill'] for s in gap.role_profiles[target_role]['top_skills']]
    
    # Candidate possesses all top skills with maximum 5.0 ratings
    ratings = {s: 5.0 for s in role_skills}
    res = gap.analyze_candidate_gap(target_role, role_skills, ratings)
    
    assert res['overall_role_readiness_pct'] == 100.0, f"Expected 100% readiness, got {res['overall_role_readiness_pct']}%"
    assert res['critical_gaps_count'] == 0, f"Expected 0 critical gaps, got {res['critical_gaps_count']}"


def test_invariant_4_symmetric_role_distance(ai_test_env):
    """INVARIANT 4: Role similarity must be symmetric: Sim(Role_A, Role_B) == Sim(Role_B, Role_A)."""
    _, graph, _, _ = ai_test_env
    sim_matrix = graph.compute_role_adjacencies()['similarity_matrix']
    roles = list(sim_matrix.keys())
    
    for r1 in roles:
        for r2 in roles:
            sim_12 = sim_matrix[r1][r2]
            sim_21 = sim_matrix[r2][r1]
            assert abs(sim_12 - sim_21) < 1e-4, f"Symmetry Invariant Violated for {r1} <-> {r2}: {sim_12} != {sim_21}"


def test_invariant_5_build_vs_buy_economics(ai_test_env):
    """INVARIANT 5: Whenever external hire cost > internal upskill cost, net savings must be positive."""
    _, _, _, sim = ai_test_env
    res = sim.simulate_cohort_upskilling(cohort_size=50, upskill_pct=20.0)
    net_savings = res['build_vs_buy_economics']['net_capital_saved_lpa']
    assert net_savings > 0, f"Economic Invariant Violated: Net savings was non-positive ({net_savings} LPA)"
