"""
Automated Unit Tests - Machine Learning Success Models & XAI
============================================================
Verifies:
- JDS Skill Success Model training, CV ROC-AUC (> 0.70)
- SDS Personality Success Model training, CV ROC-AUC (> 0.70)
- Inference probability bounds [0.0, 1.0]
- Explainable AI feature attribution consistency
"""

import os
import pytest
from src.ml_success_models import MLSuccessModelsEngine
from src.explainable_ai import ExplainableAIEngine

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC_DIR = os.path.join(BASE_DIR, 'data', 'processed')


@pytest.fixture(scope="module")
def ml_suite():
    engine = MLSuccessModelsEngine(PROC_DIR)
    engine.run_training_pipeline()
    xai = ExplainableAIEngine(engine)
    return engine, xai


def test_jds_model_training(ml_suite):
    engine, _ = ml_suite
    results = engine.train_jds_skill_model()
    best_name = results['best_model']
    best_auc = results['models'][best_name]['cv_roc_auc']
    assert best_auc >= 0.70, f"Expected JDS ROC-AUC >= 0.70, got {best_auc}"
    assert results['sample_size'] >= 100


def test_sds_model_training(ml_suite):
    engine, _ = ml_suite
    results = engine.train_sds_personality_model()
    best_name = results['best_model']
    best_auc = results['models'][best_name]['cv_roc_auc']
    assert best_auc >= 0.70, f"Expected SDS ROC-AUC >= 0.70, got {best_auc}"
    assert results['sample_size'] >= 100


def test_jds_inference_bounds(ml_suite):
    engine, _ = ml_suite
    pred = engine.predict_jds_hike({
        'big_data_skills': 4.5,
        'maths-stats_skills': 4.8,
        'coding_skills': 4.7,
        'ai_and_ml_skills': 4.9,
        'dashboard_and_storytelling_skills': 4.2
    })
    prob = pred['probability_high_hike']
    assert 0.0 <= prob <= 1.0
    assert 'High' in pred['predicted_hike_class'] or 'Standard' in pred['predicted_hike_class']


def test_explainable_ai_attribution(ml_suite):
    engine, xai = ml_suite
    explanation = xai.explain_jds_prediction({
        'big_data_skills': 4.8,
        'maths-stats_skills': 4.5,
        'coding_skills': 4.9,
        'ai_and_ml_skills': 4.9,
        'dashboard_and_storytelling_skills': 4.2
    })
    assert 'confidence_level' in explanation
    assert len(explanation['defensible_rationale']) >= 1
    assert 'coding_skills' in explanation['feature_attributions']
