"""
Workforce Intelligence Platform - Web Application & REST API
============================================================
Production Flask application serving the interactive Executive Dashboard,
REST endpoints for Career GPS, ML Inference, XAI, Optimizer, Simulator, and Copilot.
"""

import os
import sys
import json
from flask import Flask, render_template, jsonify, request

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from src.data_quality_engine import DataQualityEngine
from src.market_intelligence import MarketIntelligenceEngine
from src.skill_demand_engine import SkillDemandEngine
from src.ml_success_models import MLSuccessModelsEngine
from src.explainable_ai import ExplainableAIEngine
from src.role_skill_graph import RoleSkillGraphEngine
from src.career_gps import AICareerGPSEngine
from src.skill_gap_engine import SkillGapEngine
from src.skill_optimizer import SkillInvestmentOptimizer
from src.market_success_matrix import MarketSuccessMatrixEngine
from src.career_optimizer import CareerObjectiveOptimizer
from src.workforce_simulator import WorkforceSimulatorEngine
from src.copilot import WorkforceCopilot

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sas-cu-hackathon-workforce-intelligence-2026'

# Initialize all backend engines
RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')
PROC_DIR = os.path.join(BASE_DIR, 'data', 'processed')

print("Initializing Workforce Intelligence Engines...")
dq_engine = DataQualityEngine(RAW_DIR, PROC_DIR)
market_engine = MarketIntelligenceEngine(PROC_DIR)
skill_engine = SkillDemandEngine(PROC_DIR)
ml_engine = MLSuccessModelsEngine(PROC_DIR)

# Ensure prerequisite data files are generated
market_rep_fp = os.path.join(PROC_DIR, 'market_intelligence_report.json')
if not os.path.exists(market_rep_fp):
    market_engine.generate_full_report()

skill_tax_fp = os.path.join(PROC_DIR, 'master_skill_taxonomy.json')
if not os.path.exists(skill_tax_fp):
    skill_engine.build_skill_demand_analytics()

if not os.path.exists(os.path.join(PROC_DIR, 'model_metrics_report.json')):
    ml_engine.run_training_pipeline()
else:
    ml_engine.train_jds_skill_model()
    ml_engine.train_sds_personality_model()

xai_engine = ExplainableAIEngine(ml_engine)
graph_engine = RoleSkillGraphEngine(PROC_DIR)
graph_fp = os.path.join(PROC_DIR, 'role_skill_network_graph.json')
if not os.path.exists(graph_fp):
    graph_engine.compute_role_adjacencies()
gps_engine = AICareerGPSEngine(PROC_DIR)
gap_engine = SkillGapEngine(PROC_DIR)
opt_engine = SkillInvestmentOptimizer(PROC_DIR, ml_engine)
matrix_engine = MarketSuccessMatrixEngine(PROC_DIR)
career_opt_engine = CareerObjectiveOptimizer(gps_engine, opt_engine, ml_engine)
sim_engine = WorkforceSimulatorEngine(ml_engine, market_engine)
copilot_engine = WorkforceCopilot(market_engine, skill_engine, ml_engine, gps_engine, opt_engine, sim_engine)
print("✓ All Engines Initialized Successfully!")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/data-quality', methods=['GET'])
def get_data_quality():
    report_fp = os.path.join(PROC_DIR, 'data_quality_report.json')
    if os.path.exists(report_fp):
        with open(report_fp, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    return jsonify(dq_engine.run_all())


@app.route('/api/market-intelligence', methods=['GET'])
def get_market_intelligence():
    report_fp = os.path.join(PROC_DIR, 'market_intelligence_report.json')
    if os.path.exists(report_fp):
        with open(report_fp, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    return jsonify(market_engine.generate_full_report())


@app.route('/api/skill-taxonomy', methods=['GET'])
def get_skill_taxonomy():
    report_fp = os.path.join(PROC_DIR, 'master_skill_taxonomy.json')
    if os.path.exists(report_fp):
        with open(report_fp, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    return jsonify(skill_engine.build_skill_demand_analytics())


@app.route('/api/ml-models-report', methods=['GET'])
def get_ml_models_report():
    report_fp = os.path.join(PROC_DIR, 'model_metrics_report.json')
    if os.path.exists(report_fp):
        with open(report_fp, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    return jsonify(ml_engine.run_training_pipeline())


@app.route('/api/predict/jds-hike', methods=['POST'])
def predict_jds_hike():
    data = request.json or {}
    pred = ml_engine.predict_jds_hike(data)
    explanation = xai_engine.explain_jds_prediction(data)
    return jsonify({
        'prediction': pred,
        'xai_explanation': explanation
    })


@app.route('/api/predict/sds-success', methods=['POST'])
def predict_sds_success():
    data = request.json or {}
    pred = ml_engine.predict_sds_success(data)
    explanation = xai_engine.explain_sds_prediction(data)
    return jsonify({
        'prediction': pred,
        'xai_explanation': explanation
    })


@app.route('/api/career-gps', methods=['POST'])
def get_career_gps():
    data = request.json or {}
    current_role = data.get('current_role', 'Data Analyst')
    user_skills = data.get('skills', ['SQL', 'Tableau', 'Excel / Advanced Excel'])
    current_exp = float(data.get('experience', 3.0))
    current_salary = float(data.get('salary_lpa', 8.0))
    
    pathways = gps_engine.find_career_pathways(
        current_role=current_role,
        user_skills=user_skills,
        current_exp=current_exp,
        current_salary_lpa=current_salary
    )
    return jsonify(pathways)


@app.route('/api/role-skill-graph', methods=['GET'])
def get_role_skill_graph():
    report_fp = os.path.join(PROC_DIR, 'role_skill_network_graph.json')
    if os.path.exists(report_fp):
        with open(report_fp, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    return jsonify(graph_engine.compute_role_adjacencies())


@app.route('/api/skill-gap', methods=['POST'])
def get_skill_gap():
    data = request.json or {}
    target_role = data.get('target_role', 'Data Scientist')
    skills = data.get('skills', ['SQL', 'Excel / Advanced Excel'])
    ratings = data.get('ratings', {})
    
    gap_res = gap_engine.analyze_candidate_gap(target_role, skills, ratings)
    return jsonify(gap_res)


@app.route('/api/skill-gap/heatmap', methods=['POST'])
def get_skill_gap_heatmap():
    data = request.json or {}
    skills = data.get('skills', ['SQL', 'Tableau', 'Python'])
    heatmap = gap_engine.generate_cross_role_heatmap(skills)
    return jsonify(heatmap)


@app.route('/api/skill-optimizer', methods=['POST'])
def optimize_skills():
    data = request.json or {}
    res = opt_engine.optimize_skill_investment(data)
    return jsonify(res)


@app.route('/api/market-success-matrix', methods=['GET'])
def get_market_success_matrix():
    report_fp = os.path.join(PROC_DIR, 'market_success_matrix.json')
    if os.path.exists(report_fp):
        with open(report_fp, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    return jsonify(matrix_engine.build_matrix())


@app.route('/api/career-optimizer', methods=['POST'])
def optimize_career_objective():
    data = request.json or {}
    current_role = data.get('current_role', 'Data Analyst')
    user_skills = data.get('skills', ['SQL', 'Tableau', 'Power BI'])
    current_exp = float(data.get('experience', 3.0))
    current_salary = float(data.get('salary_lpa', 8.0))
    objective = data.get('objective', 'MAX_HIKE')
    
    res = career_opt_engine.optimize_career_plan(
        current_role=current_role,
        user_skills=user_skills,
        current_exp=current_exp,
        current_salary_lpa=current_salary,
        objective=objective
    )
    return jsonify(res)


@app.route('/api/simulator', methods=['POST'])
def simulate_workforce():
    data = request.json or {}
    cohort_size = int(data.get('cohort_size', 100))
    upskill_pct = float(data.get('upskill_pct', 30.0))
    skill_focus = data.get('skill_focus', 'ai_and_ml_skills')
    
    sim_res = sim_engine.simulate_cohort_upskilling(
        cohort_size=cohort_size,
        upskill_pct=upskill_pct,
        target_skill_focus=skill_focus
    )
    return jsonify(sim_res)


@app.route('/api/copilot', methods=['POST'])
def ask_copilot():
    data = request.json or {}
    query = data.get('query', '')
    if not query:
        return jsonify({'response': "Please provide a question for the Copilot."})
    answer = copilot_engine.ask(query)
    return jsonify({'response': answer})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
