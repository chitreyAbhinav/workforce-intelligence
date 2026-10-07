"""
Automated Integration Tests - Core Intelligence Engines
========================================================
Verifies:
- Career GPS pathfinding and milestones
- Skill Investment Optimizer ROI score bounds
- Role-Skill Adjacency Network topology
- Workforce Simulator Build vs Buy economics
"""

import os
import pytest
from src.market_intelligence import MarketIntelligenceEngine
from src.skill_demand_engine import SkillDemandEngine
from src.ml_success_models import MLSuccessModelsEngine
from src.role_skill_graph import RoleSkillGraphEngine
from src.career_gps import AICareerGPSEngine
from src.skill_gap_engine import SkillGapEngine
from src.skill_optimizer import SkillInvestmentOptimizer
from src.workforce_simulator import WorkforceSimulatorEngine

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC_DIR = os.path.join(BASE_DIR, 'data', 'processed')


@pytest.fixture(scope="module")
def engines_suite():
    ml = MLSuccessModelsEngine(PROC_DIR)
    ml.train_jds_skill_model()
    ml.train_sds_personality_model()
    market = MarketIntelligenceEngine(PROC_DIR)
    gps = AICareerGPSEngine(PROC_DIR)
    opt = SkillInvestmentOptimizer(PROC_DIR, ml)
    gap = SkillGapEngine(PROC_DIR)
    sim = WorkforceSimulatorEngine(ml, market)
    graph = RoleSkillGraphEngine(PROC_DIR)
    return gps, opt, gap, sim, graph


def test_career_gps_pathways(engines_suite):
    gps, _, _, _, _ = engines_suite
    res = gps.find_career_pathways('Data Analyst', ['SQL', 'Tableau', 'Excel / Advanced Excel'], 3.0, 7.5)
    paths = res['recommended_pathways']
    assert len(paths) >= 3
    top_p = paths[0]
    assert top_p['feasibility_pct'] > 0
    assert len(top_p['milestones']) >= 1


def test_skill_investment_optimizer(engines_suite):
    _, opt, _, _, _ = engines_suite
    res = opt.optimize_skill_investment({
        'big_data_skills': 3.0,
        'maths-stats_skills': 3.5,
        'coding_skills': 3.5,
        'ai_and_ml_skills': 3.0,
        'dashboard_and_storytelling_skills': 4.0
    })
    assert 'top_recommended_skill' in res
    assert len(res['skill_investment_rankings']) >= 5
    top_s = res['skill_investment_rankings'][0]
    assert 0.0 <= top_s['strategic_roi_score'] <= 100.0


def test_workforce_simulator(engines_suite):
    _, _, _, sim, _ = engines_suite
    res = sim.simulate_cohort_upskilling(cohort_size=100, upskill_pct=30.0, target_skill_focus='ai_and_ml_skills')
    assert res['upskilled_employees_count'] == 30
    econ = res['build_vs_buy_economics']
    assert econ['net_capital_saved_lpa'] > 0
    assert 'x' in econ['reskilling_roi_multiplier']


def test_role_skill_network_graph(engines_suite):
    _, _, _, _, graph = engines_suite
    res = graph.compute_role_adjacencies()
    assert len(res['nodes']) == 10
    assert len(res['edges']) >= 5
