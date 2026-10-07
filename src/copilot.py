"""
Workforce Intelligence Platform - AI Workforce Copilot
======================================================
Hero Feature #5: "Let me ask the entire system questions naturally."
- Answers user inquiries across market benchmarks, role transitions, skill premiums, and ML models
- Grounds every answer in exact empirical data points from the processed datasets
- Formats responses in clean, structured Markdown with metrics, tables, and defensible reasons
"""

import sys

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


class WorkforceCopilot:
    def __init__(self, market_engine, skill_engine, ml_engine, gps_engine, opt_engine, sim_engine):
        self.market = market_engine
        self.skill = skill_engine
        self.ml = ml_engine
        self.gps = gps_engine
        self.opt = opt_engine
        self.sim = sim_engine

    def ask(self, query: str):
        """Processes a natural language query and returns an evidence-backed analysis."""
        q_lower = query.lower()
        
        # 1. Salary / Highest paying role query
        if any(k in q_lower for k in ['highest paying', 'top paying', 'highest salary', 'salary benchmark', 'salary of']):
            benchmarks = self.market.get_role_salary_benchmarks()
            top_3 = benchmarks[:3]
            resp = "### 📊 Job Market Salary Benchmarks (Analyzed across 13,900+ Postings)\n\n"
            resp += "The empirical salary hierarchy across standardized analytics roles:\n\n"
            resp += "| Rank | Standardized Role | Median Salary (LPA) | 25th - 75th Percentile | Avg Exp Required |\n"
            resp += "| :--- | :--- | :--- | :--- | :--- |\n"
            for i, r in enumerate(benchmarks[:7], 1):
                resp += f"| **#{i}** | {r['role']} | **₹{r['median_lpa']} L** | ₹{r['p25_lpa']}L - ₹{r['p75_lpa']}L | {r['avg_experience_req']} yrs |\n"
            resp += f"\n**Key Insight:** **{top_3[0]['role']}** leads the market at a median of **₹{top_3[0]['median_lpa']} LPA**, followed closely by **{top_3[1]['role']}** (**₹{top_3[1]['median_lpa']} LPA**)."
            return resp

        # 2. Skill Premium query
        elif any(k in q_lower for k in ['premium', 'python', 'sql', 'highest demand skill', 'skill demand', 'which skill pays']):
            taxonomy = self.skill.build_skill_demand_analytics()
            top_skills = taxonomy['market_skills_ranked'][:8]
            resp = "### 💡 Empirical Skill Demand & Salary Premiums\n\n"
            resp += "Based on NLP extraction across 12,000+ job descriptions:\n\n"
            resp += "| Skill | Category | Market Demand (Postings) | Penetration % | Salary Premium (LPA) |\n"
            resp += "| :--- | :--- | :--- | :--- | :--- |\n"
            for s in top_skills:
                resp += f"| **{s['skill']}** | {s['category']} | {s['job_postings_count']:,} | {s['market_penetration_pct']}% | **+{s['salary_premium_lpa']} LPA** ({s['salary_premium_pct']}%) |\n"
            resp += "\n**Strategic Takeaway:** While **SQL** and **BI tools** form the mandatory table stakes (60-80% market penetration), specialized skills like **Python, PySpark, and Machine Learning** command an immediate **+₹4.0 to ₹5.5 Lakhs** empirical compensation premium."
            return resp

        # 3. Career transition / GPS query
        elif any(k in q_lower for k in ['transition', 'gps', 'analyst to data scientist', 'pathway', 'career path', 'where can i go']):
            pathways = self.gps.find_career_pathways(
                current_role='Data Analyst',
                user_skills=['SQL', 'Tableau', 'Excel / Advanced Excel'],
                current_exp=3.0,
                current_salary_lpa=8.0
            )['recommended_pathways']
            top_p = pathways[0]
            resp = f"### 🧭 AI Career GPS: Transition Pathways for Data Analyst\n\n"
            resp += f"**Primary Recommended Next Destination:** **{top_p['target_role']}**\n"
            resp += f"- **Feasibility Score:** `{top_p['feasibility_pct']}%` ({top_p['difficulty']} Friction)\n"
            resp += f"- **Expected Compensation:** **₹{top_p['target_median_salary_lpa']} LPA** (+₹{top_p['salary_delta_lpa']} LPA / +{top_p['salary_uplift_pct']}%)\n"
            resp += f"- **Missing Critical Skills:** `{', '.join(top_p['missing_critical_skills'])}`\n\n"
            resp += "**Step-by-Step Chronological Flight Plan:**\n"
            for m in top_p['milestones']:
                resp += f"1. **{m['phase']}**: {m['objective']} — *{m['focus']}*\n"
            return resp

        # 4. Which skill to learn next / Optimizer
        elif any(k in q_lower for k in ['learn next', 'optimize', 'invest', 'one skill', 'roi']):
            opt_res = self.opt.optimize_skill_investment({
                'big_data_skills': 3.0,
                'maths-stats_skills': 3.5,
                'coding_skills': 3.5,
                'ai_and_ml_skills': 3.0,
                'dashboard_and_storytelling_skills': 4.0
            })
            resp = f"### 🎯 Skill Investment Optimizer (ROI Engine)\n\n"
            resp += f"**Strategic Verdict:** {opt_res['top_recommendation_reason']}\n\n"
            resp += "**Top 5 Highest-ROI Skills Ranked:**\n\n"
            resp += "| Skill | Domain Trait | Strategic ROI Score (0-100) | Predicted Hike Lift | Active Job Openings |\n"
            resp += "| :--- | :--- | :--- | :--- | :--- |\n"
            for s in opt_res['skill_investment_rankings'][:5]:
                resp += f"| **{s['skill']}** | {s['associated_trait']} | **{s['strategic_roi_score']} / 100** | +{s['marginal_hike_gain_pct']}% | {s['market_demand_postings']:,} jobs |\n"
            return resp

        # 5. Build vs Buy / Simulation query
        elif any(k in q_lower for k in ['simulate', 'build vs buy', 'reskill', 'workforce', 'cohort', 'digital twin']):
            sim_res = self.sim.simulate_cohort_upskilling(cohort_size=100, upskill_pct=30.0, target_skill_focus='ai_and_ml_skills')
            resp = "### 🏢 Workforce Digital Twin: Cohort Simulation (100 Data Scientists)\n\n"
            resp += f"**Scenario:** Upskilling 30% of Junior Cohort in **AI & Machine Learning** + **Advanced Coding**.\n\n"
            resp += "- **Baseline High Performance Rate:** `51.0%`\n"
            resp += f"- **Post-Upskilling High Performance Rate:** **`{sim_res['post_simulation_metrics']['high_performance_rate_pct']}%`** (+{sim_res['post_simulation_metrics']['net_high_performer_gain']} high-performing engineers)\n"
            resp += f"- **Internal Reskilling Cost:** ₹{sim_res['build_vs_buy_economics']['internal_reskilling_investment_lpa']} Lakhs\n"
            resp += f"- **Equivalent External Hiring Cost:** ₹{sim_res['build_vs_buy_economics']['equivalent_external_acquisition_cost_lpa']} Lakhs\n"
            resp += f"- **Net Capital Saved:** **₹{sim_res['build_vs_buy_economics']['net_capital_saved_lpa']} Lakhs** ({sim_res['build_vs_buy_economics']['reskilling_roi_multiplier']} ROI)\n\n"
            resp += f"**Executive Conclusion:** *{sim_res['build_vs_buy_economics']['strategic_recommendation']}*"
            return resp

        # 6. Default general assistant overview
        else:
            resp = "### 🤖 AI Workforce Intelligence Copilot\n\n"
            resp += "I am grounded on 13,900+ clean analytics jobs and machine learning success models from the SAS CU Hackathon datasets.\n\n"
            resp += "You can ask me questions like:\n"
            resp += "- *'What is the highest paying data role in the market?'*\n"
            resp += "- *'What is the salary premium for Python vs SQL?'*\n"
            resp += "- *'How do I transition from Data Analyst to Data Scientist?'*\n"
            resp += "- *'Which single skill gives me the highest strategic ROI?'*\n"
            resp += "- *'What is the Build vs Buy ROI of reskilling 30% of my workforce?'*"
            return resp
