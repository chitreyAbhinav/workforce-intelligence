"""
Workforce Intelligence Platform - Machine Learning Success Models
==================================================================
Directly addresses Round-2 30-mark Data Analysis criteria:
1. Junior Data Scientist (JDS) Skill Success Model
   - Predicts salary_hike_high_or_low (high performance hike)
   - Features: big_data, maths-stats, coding, ai_and_ml, dashboard_and_storytelling
2. Senior Data Scientist (SDS) Personality Success Model
   - Predicts success_classification_high_low (senior leadership success)
   - Features: Big Five OCEAN traits (neuroticism, extraversion, openness, agreeableness, conscientiousness)

Evaluates Random Forest, Gradient Boosting, and Logistic Regression with Stratified Cross-Validation,
ROC-AUC, Precision, Recall, F1-Score, and Confusion Matrices.
"""

import os
import sys
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, roc_curve
)

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


class MLSuccessModelsEngine:
    def __init__(self, processed_data_dir: str):
        self.proc_dir = processed_data_dir
        self.df_jds = pd.read_csv(os.path.join(self.proc_dir, 'cleaned_jds_traits.csv'))
        self.df_sds = pd.read_csv(os.path.join(self.proc_dir, 'cleaned_sds_traits.csv'))
        
        self.jds_feature_names = [
            'big_data_skills',
            'maths-stats_skills',
            'coding_skills',
            'ai_and_ml_skills',
            'dashboard_and_storytelling_skills'
        ]
        
        self.sds_feature_names = [
            'neuroticism',
            'extraversion',
            'openness_to_experience',
            'agreeableness',
            'conscientiousness'
        ]
        
        self.models_jds = {}
        self.models_sds = {}
        self.results_summary = {}

    def train_jds_skill_model(self):
        """Trains and benchmarks ML algorithms on JDS Technical Skills dataset."""
        print("Training Junior Data Scientist (JDS) Skill Success Models...")
        X = self.df_jds[self.jds_feature_names].values
        y = self.df_jds['salary_hike_high_or_low'].values
        
        candidates = {
            'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=4, min_samples_split=4, random_state=42),
            'Gradient Boosting': GradientBoostingClassifier(n_estimators=80, learning_rate=0.08, max_depth=3, random_state=42),
            'Logistic Regression': LogisticRegression(C=1.0, penalty='l2', solver='liblinear', random_state=42)
        }
        
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        model_metrics = {}
        
        for name, clf in candidates.items():
            cv_res = cross_validate(
                clf, X, y, cv=cv,
                scoring=['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
            )
            # Fit on full dataset for inference & feature importance
            clf.fit(X, y)
            y_pred = clf.predict(X)
            y_prob = clf.predict_proba(X)[:, 1]
            
            # ROC curve coordinates
            fpr, tpr, _ = roc_curve(y, y_prob)
            cm = confusion_matrix(y, y_pred).tolist()
            
            # Feature importance / weights
            if hasattr(clf, 'feature_importances_'):
                importances = dict(zip(self.jds_feature_names, [round(float(v), 4) for v in clf.feature_importances_]))
            elif hasattr(clf, 'coef_'):
                importances = dict(zip(self.jds_feature_names, [round(float(v), 4) for v in clf.coef_[0]]))
            else:
                importances = {}

            model_metrics[name] = {
                'cv_accuracy': round(float(np.mean(cv_res['test_accuracy'])), 3),
                'cv_precision': round(float(np.mean(cv_res['test_precision'])), 3),
                'cv_recall': round(float(np.mean(cv_res['test_recall'])), 3),
                'cv_f1': round(float(np.mean(cv_res['test_f1'])), 3),
                'cv_roc_auc': round(float(np.mean(cv_res['test_roc_auc'])), 3),
                'confusion_matrix': cm,
                'roc_curve': {
                    'fpr': [round(float(x), 3) for x in fpr.tolist()[:15]],
                    'tpr': [round(float(x), 3) for x in tpr.tolist()[:15]]
                },
                'feature_importance': importances
            }
            self.models_jds[name] = clf

        # Select Best Model based on ROC-AUC
        best_name = max(model_metrics.keys(), key=lambda k: model_metrics[k]['cv_roc_auc'])
        
        return {
            'target': 'salary_hike_high_or_low',
            'sample_size': len(X),
            'positive_ratio': round(float(np.mean(y)), 3),
            'features': self.jds_feature_names,
            'best_model': best_name,
            'models': model_metrics
        }

    def train_sds_personality_model(self):
        """Trains and benchmarks ML algorithms on SDS Personality Traits dataset."""
        print("Training Senior Data Scientist (SDS) Personality Success Models...")
        X = self.df_sds[self.sds_feature_names].values
        y = self.df_sds['success_binary'].values
        
        candidates = {
            'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=4, min_samples_split=4, random_state=42),
            'Gradient Boosting': GradientBoostingClassifier(n_estimators=80, learning_rate=0.08, max_depth=3, random_state=42),
            'Logistic Regression': LogisticRegression(C=1.0, penalty='l2', solver='liblinear', random_state=42)
        }
        
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        model_metrics = {}
        
        for name, clf in candidates.items():
            cv_res = cross_validate(
                clf, X, y, cv=cv,
                scoring=['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
            )
            clf.fit(X, y)
            y_pred = clf.predict(X)
            y_prob = clf.predict_proba(X)[:, 1]
            
            fpr, tpr, _ = roc_curve(y, y_prob)
            cm = confusion_matrix(y, y_pred).tolist()
            
            if hasattr(clf, 'feature_importances_'):
                importances = dict(zip(self.sds_feature_names, [round(float(v), 4) for v in clf.feature_importances_]))
            elif hasattr(clf, 'coef_'):
                importances = dict(zip(self.sds_feature_names, [round(float(v), 4) for v in clf.coef_[0]]))
            else:
                importances = {}

            model_metrics[name] = {
                'cv_accuracy': round(float(np.mean(cv_res['test_accuracy'])), 3),
                'cv_precision': round(float(np.mean(cv_res['test_precision'])), 3),
                'cv_recall': round(float(np.mean(cv_res['test_recall'])), 3),
                'cv_f1': round(float(np.mean(cv_res['test_f1'])), 3),
                'cv_roc_auc': round(float(np.mean(cv_res['test_roc_auc'])), 3),
                'confusion_matrix': cm,
                'roc_curve': {
                    'fpr': [round(float(x), 3) for x in fpr.tolist()[:15]],
                    'tpr': [round(float(x), 3) for x in tpr.tolist()[:15]]
                },
                'feature_importance': importances
            }
            self.models_sds[name] = clf

        best_name = max(model_metrics.keys(), key=lambda k: model_metrics[k]['cv_roc_auc'])
        
        return {
            'target': 'success_classification_high_low',
            'sample_size': len(X),
            'positive_ratio': round(float(np.mean(y)), 3),
            'features': self.sds_feature_names,
            'best_model': best_name,
            'models': model_metrics
        }

    def predict_jds_hike(self, skill_vector: dict, model_name: str = 'Random Forest'):
        """Inference function: predicts probability and class of high salary hike from 1-5 skill inputs."""
        clf = self.models_jds.get(model_name)
        if clf is None:
            clf = list(self.models_jds.values())[0]
            
        features = [
            float(skill_vector.get('big_data_skills', 3.5)),
            float(skill_vector.get('maths-stats_skills', skill_vector.get('maths_stats_skills', 3.5))),
            float(skill_vector.get('coding_skills', 3.5)),
            float(skill_vector.get('ai_and_ml_skills', 3.5)),
            float(skill_vector.get('dashboard_and_storytelling_skills', 3.5))
        ]
        
        X = np.array([features])
        prob_high = float(clf.predict_proba(X)[0][1])
        pred_label = int(clf.predict(X)[0])
        
        return {
            'probability_high_hike': round(prob_high, 3),
            'predicted_hike_class': 'High Hike (1)' if pred_label == 1 else 'Standard/Low Hike (0)',
            'features_input': dict(zip(self.jds_feature_names, features))
        }

    def predict_sds_success(self, personality_vector: dict, model_name: str = 'Random Forest'):
        """Inference function: predicts senior leadership success probability from 0-1 OCEAN inputs."""
        clf = self.models_sds.get(model_name)
        if clf is None:
            clf = list(self.models_sds.values())[0]
            
        features = [
            float(personality_vector.get('neuroticism', 0.40)),
            float(personality_vector.get('extraversion', 0.60)),
            float(personality_vector.get('openness_to_experience', 0.70)),
            float(personality_vector.get('agreeableness', 0.65)),
            float(personality_vector.get('conscientiousness', 0.72))
        ]
        
        X = np.array([features])
        prob_high = float(clf.predict_proba(X)[0][1])
        pred_label = int(clf.predict(X)[0])
        
        return {
            'probability_high_success': round(prob_high, 3),
            'predicted_success_class': 'High Success' if pred_label == 1 else 'Low / Moderate Success',
            'features_input': dict(zip(self.sds_feature_names, features))
        }

    def run_training_pipeline(self):
        """Executes full training for both models and writes model_metrics_report.json."""
        jds_results = self.train_jds_skill_model()
        print(f"[OK] JDS Skill Success Model trained. Best Model: {jds_results['best_model']} (ROC-AUC: {jds_results['models'][jds_results['best_model']]['cv_roc_auc']})")
        
        sds_results = self.train_sds_personality_model()
        print(f"[OK] SDS Personality Model trained. Best Model: {sds_results['best_model']} (ROC-AUC: {sds_results['models'][sds_results['best_model']]['cv_roc_auc']})")
        
        combined_report = {
            'junior_data_scientist_skill_model': jds_results,
            'senior_data_scientist_personality_model': sds_results
        }
        
        out_fp = os.path.join(self.proc_dir, 'model_metrics_report.json')
        with open(out_fp, 'w', encoding='utf-8') as f:
            json.dump(combined_report, f, indent=2)
            
        print(f"[OK] Model metrics report saved at {out_fp}")
        return combined_report


if __name__ == '__main__':
    proc_dir = r'C:\Users\chitr_mzkaj0t\.gemini\antigravity\scratch\workforce_intelligence\data\processed'
    engine = MLSuccessModelsEngine(proc_dir)
    res = engine.run_training_pipeline()
    
    # Test sample inference
    test_jds = engine.predict_jds_hike({
        'big_data_skills': 4.5,
        'maths-stats_skills': 4.8,
        'coding_skills': 4.9,
        'ai_and_ml_skills': 4.7,
        'dashboard_and_storytelling_skills': 4.2
    })
    print("\nSample JDS Inference:", test_jds)
    
    test_sds = engine.predict_sds_success({
        'neuroticism': 0.25,
        'extraversion': 0.75,
        'openness_to_experience': 0.85,
        'agreeableness': 0.70,
        'conscientiousness': 0.90
    })
    print("Sample SDS Inference:", test_sds)
