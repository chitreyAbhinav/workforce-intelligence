"""
Workforce Intelligence Platform - Explainable AI (XAI) Engine
==============================================================
Addresses Locked Feature #6 and Hero Feature #5:
"Don't just tell me the answer. Show me why."
- Calculates Local & Global Feature Attributions (SHAP-style additive feature explanations)
- Generates transparent, defensible natural language rationales backed by empirical data
- Computes Confidence & Evidence Layers for all career recommendations
"""

import sys
import numpy as np

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


class ExplainableAIEngine:
    def __init__(self, ml_engine):
        self.ml_engine = ml_engine
        
        # Base population means for attribution baseline
        self.jds_baseline = {
            'big_data_skills': 3.85,
            'maths-stats_skills': 4.29,
            'coding_skills': 4.27,
            'ai_and_ml_skills': 4.57,
            'dashboard_and_storytelling_skills': 4.36
        }
        
        self.sds_baseline = {
            'neuroticism': 0.39,
            'extraversion': 0.61,
            'openness_to_experience': 0.70,
            'agreeableness': 0.64,
            'conscientiousness': 0.72
        }

    def explain_jds_prediction(self, skill_vector: dict):
        """Generates SHAP-style local attributions and defensible rationale for a JDS candidate."""
        base_pred = self.ml_engine.predict_jds_hike(self.jds_baseline)
        base_prob = base_pred['probability_high_hike']
        
        cand_pred = self.ml_engine.predict_jds_hike(skill_vector)
        cand_prob = cand_pred['probability_high_hike']
        
        # Marginal impact per feature
        attributions = {}
        feature_names = self.ml_engine.jds_feature_names
        
        for feat in feature_names:
            # Perturb feature back to baseline while keeping others
            perturbed = skill_vector.copy()
            perturbed[feat] = self.jds_baseline[feat]
            p_prob = self.ml_engine.predict_jds_hike(perturbed)['probability_high_hike']
            # Marginal contribution = cand_prob - prob_without_feat_lift
            marginal = round(cand_prob - p_prob, 3)
            attributions[feat] = {
                'candidate_score': float(skill_vector.get(feat, 3.5)),
                'cohort_baseline': float(self.jds_baseline[feat]),
                'marginal_probability_impact': marginal,
                'impact_direction': 'Positive Booster (+)' if marginal > 0 else ('Negative Drag (-)' if marginal < 0 else 'Neutral')
            }
            
        # Synthesize Human-Defensible Rationale
        positives = [f for f, v in attributions.items() if v['marginal_probability_impact'] > 0]
        negatives = [f for f, v in attributions.items() if v['marginal_probability_impact'] < 0]
        
        def get_val(vec, key, default=3.5):
            if key in vec: return vec[key]
            k_alt1 = key.replace('-', '_')
            if k_alt1 in vec: return vec[k_alt1]
            k_alt2 = key.replace('_', '-')
            if k_alt2 in vec: return vec[k_alt2]
            return default

        reasons = []
        if positives:
            top_pos = max(positives, key=lambda f: attributions[f]['marginal_probability_impact'])
            top_lift = attributions[top_pos]['marginal_probability_impact']
            val = get_val(skill_vector, top_pos)
            reasons.append(
                f"Primary Positive Driver: High proficiency in '{top_pos.replace('-', ' ').replace('_', ' ').title()}' "
                f"({val}/5.0) contributes +{round(top_lift * 100, 1)}% probability uplift above baseline."
            )
        if negatives:
            top_neg = min(negatives, key=lambda f: attributions[f]['marginal_probability_impact'])
            top_drag = abs(attributions[top_neg]['marginal_probability_impact'])
            val = get_val(skill_vector, top_neg)
            reasons.append(
                f"Primary Bottleneck: Sub-cohort performance in '{top_neg.replace('-', ' ').replace('_', ' ').title()}' "
                f"({val}/5.0) dampens hike probability by -{round(top_drag * 100, 1)}%."
            )
        else:
            reasons.append("Skills are well-balanced across all technical dimensions.")

        confidence_score = round(min(0.98, max(0.65, abs(cand_prob - 0.5) * 1.6 + 0.65)), 2)
        
        return {
            'predicted_hike_probability': cand_prob,
            'prediction_label': cand_pred['predicted_hike_class'],
            'cohort_baseline_probability': base_prob,
            'net_probability_lift': round(cand_prob - base_prob, 3),
            'confidence_level': f"{int(confidence_score * 100)}%",
            'feature_attributions': attributions,
            'defensible_rationale': reasons
        }

    def explain_sds_prediction(self, personality_vector: dict):
        """Generates SHAP-style local attributions and defensible rationale for an SDS candidate."""
        base_pred = self.ml_engine.predict_sds_success(self.sds_baseline)
        base_prob = base_pred['probability_high_success']
        
        cand_pred = self.ml_engine.predict_sds_success(personality_vector)
        cand_prob = cand_pred['probability_high_success']
        
        attributions = {}
        feature_names = self.ml_engine.sds_feature_names
        
        for feat in feature_names:
            perturbed = personality_vector.copy()
            perturbed[feat] = self.sds_baseline[feat]
            p_prob = self.ml_engine.predict_sds_success(perturbed)['probability_high_success']
            marginal = round(cand_prob - p_prob, 3)
            attributions[feat] = {
                'candidate_score': float(personality_vector.get(feat, 0.5)),
                'cohort_baseline': float(self.sds_baseline[feat]),
                'marginal_probability_impact': marginal,
                'impact_direction': 'Positive Booster (+)' if marginal > 0 else ('Negative Drag (-)' if marginal < 0 else 'Neutral')
            }
            
        positives = [f for f, v in attributions.items() if v['marginal_probability_impact'] > 0]
        negatives = [f for f, v in attributions.items() if v['marginal_probability_impact'] < 0]
        
        reasons = []
        if positives:
            top_pos = max(positives, key=lambda f: attributions[f]['marginal_probability_impact'])
            top_lift = attributions[top_pos]['marginal_probability_impact']
            reasons.append(
                f"Senior Success Driver: Exceptional '{top_pos.replace('_', ' ').title()}' "
                f"({personality_vector[top_pos]}) increases executive success likelihood by +{round(top_lift * 100, 1)}%."
            )
        if negatives:
            top_neg = min(negatives, key=lambda f: attributions[f]['marginal_probability_impact'])
            top_drag = abs(attributions[top_neg]['marginal_probability_impact'])
            reasons.append(
                f"Leadership Risk Factor: Trait alignment in '{top_neg.replace('_', ' ').title()}' "
                f"({personality_vector[top_neg]}) reduces success score by -{round(top_drag * 100, 1)}%."
            )

        confidence_score = round(min(0.98, max(0.65, abs(cand_prob - 0.5) * 1.6 + 0.65)), 2)

        return {
            'predicted_success_probability': cand_prob,
            'prediction_label': cand_pred['predicted_success_class'],
            'cohort_baseline_probability': base_prob,
            'net_probability_lift': round(cand_prob - base_prob, 3),
            'confidence_level': f"{int(confidence_score * 100)}%",
            'feature_attributions': attributions,
            'defensible_rationale': reasons
        }
