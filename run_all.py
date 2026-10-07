"""
Workforce Intelligence Platform - Master Orchestrator
=====================================================
Executes the full pipeline:
1. Data Quality & Cleansing Engine
2. Market Intelligence Engine
3. Skill Demand & Taxonomy Mining
4. Predictive ML Success Models (JDS & SDS)
5. Market x Success Intelligence Matrix
6. Role-Skill Network Graph
7. Pytest Automated Test Suite (Unit, Integration, AI-Assisted)
8. Formal Approach Note (.docx) & Presentation (.pptx) Generator
9. Starts Production Flask Web Application
"""

import os
import sys
import argparse
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def run_pipeline():
    print("=" * 70)
    print("🚀 WORKFORCEX: STARTING END-TO-END PIPELINE")
    print("=" * 70)

    raw_dir = os.path.join(BASE_DIR, 'data', 'raw')
    proc_dir = os.path.join(BASE_DIR, 'data', 'processed')

    # Step 1: Data Quality Engine
    print("\n[STEP 1/6] Running Data Quality Engine (25 Marks)...")
    from src.data_quality_engine import DataQualityEngine
    dq = DataQualityEngine(raw_dir, proc_dir)
    dq.run_all()

    # Step 2: Market Intelligence Engine
    print("\n[STEP 2/6] Running Job Market Intelligence Engine...")
    from src.market_intelligence import MarketIntelligenceEngine
    market = MarketIntelligenceEngine(proc_dir)
    market.generate_full_report()

    # Step 3: Skill Demand Engine
    print("\n[STEP 3/6] Running Skill Demand & Taxonomy Engine...")
    from src.skill_demand_engine import SkillDemandEngine
    skill = SkillDemandEngine(proc_dir)
    skill.build_skill_demand_analytics()

    # Step 4: Predictive ML Models
    print("\n[STEP 4/6] Training Predictive ML Models (30 Marks)...")
    from src.ml_success_models import MLSuccessModelsEngine
    ml = MLSuccessModelsEngine(proc_dir)
    ml.run_training_pipeline()

    # Step 5: Market x Success Matrix
    print("\n[STEP 5/6] Building Market x Success Intelligence Matrix...")
    from src.market_success_matrix import MarketSuccessMatrixEngine
    matrix = MarketSuccessMatrixEngine(proc_dir)
    matrix.build_matrix()

    # Step 6: Role-Skill Graph
    print("\n[STEP 6/6] Computing Role-Skill Adjacency Network Graph...")
    from src.role_skill_graph import RoleSkillGraphEngine
    graph = RoleSkillGraphEngine(proc_dir)
    graph.compute_role_adjacencies()

    print("\n" + "=" * 70)
    print("✅ PIPELINE EXECUTION COMPLETED SUCCESSFULLY!")
    print("=" * 70)


def run_tests():
    print("\n" + "=" * 70)
    print("🧪 RUNNING COMPREHENSIVE AUTOMATED TEST SUITE (pytest)")
    print("=" * 70)
    cmd = [sys.executable, "-m", "pytest", "tests/test_data_quality.py", "tests/test_ml_models.py", "tests/test_engines.py", "tests/test_ai_assisted.py", "tests/test_api.py", "-v"]
    res = subprocess.run(cmd, cwd=BASE_DIR)
    return res.returncode


def generate_reports():
    print("\n" + "=" * 70)
    print("📄 GENERATING FORMAL APPROACH NOTE & PRESENTATION DECK")
    print("=" * 70)
    from reports.build_submission_artifacts import build_approach_note_docx, build_presentation_pptx
    build_approach_note_docx()
    build_presentation_pptx()
    print("=" * 70)


def start_server(port=5000):
    print("\n" + "=" * 70)
    print(f"🌐 LAUNCHING WORKFORCEX DASHBOARD AT http://127.0.0.1:{port}")
    print("=" * 70)
    from app.app import app
    app.run(host="127.0.0.1", port=port, debug=False)


def main():
    parser = argparse.ArgumentParser(description="WorkforceX Intelligence Platform")
    parser.add_argument("--test", action="store_true", help="Run automated test suite")
    parser.add_argument("--generate-reports", action="store_true", help="Generate Word Approach Note & PPTX Presentation")
    parser.add_argument("--server", action="store_true", help="Start web dashboard server")
    parser.add_argument("--port", type=int, default=5000, help="Port for web dashboard")
    args = parser.parse_args()

    if args.test:
        run_tests()
    elif args.generate_reports:
        generate_reports()
    elif args.server:
        start_server(port=args.port)
    else:
        # Default: Full workflow execution
        run_pipeline()
        generate_reports()
        run_tests()
        start_server(port=args.port)


if __name__ == '__main__':
    main()
