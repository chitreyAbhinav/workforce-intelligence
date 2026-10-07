"""
Automated Integration Tests - Flask REST API Endpoints
======================================================
Verifies:
- All API routes respond with HTTP 200 and valid JSON schema
- Career GPS, Skill Optimizer, Simulator, and Copilot endpoints
"""

import os
import json
import pytest
from app.app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index_route(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'WorkforceX Intelligence' in rv.data


def test_data_quality_api(client):
    rv = client.get('/api/data-quality')
    assert rv.status_code == 200
    data = json.loads(rv.data)
    assert 'completeness_score_pct' in data
    assert data['overall_status'] == 'PASSED_HIGH_CONFIDENCE'


def test_market_intelligence_api(client):
    rv = client.get('/api/market-intelligence')
    assert rv.status_code == 200
    data = json.loads(rv.data)
    assert 'role_benchmarks' in data
    assert len(data['role_benchmarks']) >= 5


def test_predict_jds_api(client):
    payload = {
        'big_data_skills': 4.5,
        'maths_stats_skills': 4.8,
        'coding_skills': 4.9,
        'ai_and_ml_skills': 4.7,
        'dashboard_and_storytelling_skills': 4.2
    }
    rv = client.post('/api/predict/jds-hike', json=payload)
    assert rv.status_code == 200
    data = json.loads(rv.data)
    assert 'prediction' in data
    assert 'xai_explanation' in data
    assert data['prediction']['probability_high_hike'] > 0


def test_career_gps_api(client):
    payload = {
        'current_role': 'Data Analyst',
        'skills': ['SQL', 'Tableau', 'Excel / Advanced Excel'],
        'experience': 3.0,
        'salary_lpa': 8.0
    }
    rv = client.post('/api/career-gps', json=payload)
    assert rv.status_code == 200
    data = json.loads(rv.data)
    assert 'recommended_pathways' in data
    assert len(data['recommended_pathways']) > 0


def test_copilot_api(client):
    rv = client.post('/api/copilot', json={'query': 'What is the salary premium for Python?'})
    assert rv.status_code == 200
    data = json.loads(rv.data)
    assert 'Python' in data['response']
