// WorkforceX Intelligence Platform - Client JavaScript
// Dual-mode: Interacts with Flask backend or executes in-browser intelligence on GitHub Pages

document.addEventListener('DOMContentLoaded', () => {
  initTabs();
  initDataQuality();
  initMarketIntelligence();
  initMLModels();
  initMatrix();
  initCareerGPS();
  initSkillOptimizer();
  initSimulator();
  initCopilot();
});

// --- Tab Switching ---
function initTabs() {
  const buttons = document.querySelectorAll('.tab-btn');
  const panes = document.querySelectorAll('.tab-pane');

  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      buttons.forEach(b => b.classList.remove('active'));
      panes.forEach(p => p.classList.remove('active'));

      btn.classList.add('active');
      const targetId = btn.getAttribute('data-tab');
      const pane = document.getElementById(targetId);
      if (pane) pane.classList.add('active');
    });
  });
}

// Global chart references
let chartOutliers, chartRoles, chartExp, chartTiers, chartGeo, chartJdsImp, chartSdsImp, chartMatrix, chartGap, chartSim;

// --- Universal API Request Dispatcher ---
async function apiFetch(endpoint, method = 'GET', payload = null) {
  // Try live backend fetch if running on live web server (non-GitHub Pages)
  if (window.location.protocol.startsWith('http') && !window.location.hostname.includes('github.io')) {
    try {
      const opts = { method };
      if (payload) {
        opts.headers = { 'Content-Type': 'application/json' };
        opts.body = JSON.stringify(payload);
      }
      const res = await fetch(endpoint, opts);
      if (res.ok) {
        return await res.json();
      }
    } catch (e) {
      console.warn(`Backend fetch failed for ${endpoint}, using static client engine.`);
    }
  }

  // Fallback to in-browser client engine
  return executeClientEngine(endpoint, payload);
}

// --- Client Intelligence Engine (GitHub Pages / Standalone Fallback) ---
function executeClientEngine(endpoint, payload) {
  const bundle = window.WORKFORCEX_DATA || {};

  if (endpoint === '/api/data-quality') {
    return bundle.data_quality || {};
  }
  if (endpoint === '/api/market-intelligence') {
    return bundle.market_intelligence || {};
  }
  if (endpoint === '/api/ml-models-report') {
    return bundle.model_metrics_report || {};
  }
  if (endpoint === '/api/market-success-matrix') {
    return bundle.market_success_matrix || {};
  }
  if (endpoint === '/api/role-skill-graph') {
    return bundle.role_skill_network_graph || {};
  }

  // Predictive JDS Hike Model
  if (endpoint === '/api/predict/jds-hike') {
    payload = payload || {};
    const coding = parseFloat(payload.coding_skills || 3.5);
    const aiml = parseFloat(payload.ai_and_ml_skills || 3.5);
    const math = parseFloat(payload.maths_stats_skills || 3.5);
    const bigdata = parseFloat(payload.big_data_skills || 3.5);
    const story = parseFloat(payload.dashboard_and_storytelling_skills || 3.5);

    const baselines = { story: 4.36, math: 4.29, aiml: 4.57, coding: 4.27, bigdata: 3.85 };
    const weights = { story: 0.3567, math: 0.2441, aiml: 0.1736, coding: 0.1457, bigdata: 0.0798 };

    const delta = weights.story * (story - baselines.story) +
                  weights.math * (math - baselines.math) +
                  weights.aiml * (aiml - baselines.aiml) +
                  weights.coding * (coding - baselines.coding) +
                  weights.bigdata * (bigdata - baselines.bigdata);

    const rawProb = 1 / (1 + Math.exp(-(0.10 + 2.6 * delta)));
    const prob = Math.min(0.98, Math.max(0.05, Math.round(rawProb * 1000) / 1000));
    const hikeClass = prob >= 0.50 ? 'High Hike (1)' : 'Standard/Low Hike (0)';

    const attributions = [
      { feat: 'Dashboard & Storytelling', delta: (story - baselines.story), weight: weights.story, val: story },
      { feat: 'Maths & Stats', delta: (math - baselines.math), weight: weights.math, val: math },
      { feat: 'AI & Machine Learning', delta: (aiml - baselines.aiml), weight: weights.aiml, val: aiml },
      { feat: 'Coding Skills', delta: (coding - baselines.coding), weight: weights.coding, val: coding },
      { feat: 'Big Data Skills', delta: (bigdata - baselines.bigdata), weight: weights.bigdata, val: bigdata }
    ];

    const reasons = [];
    const pos = attributions.filter(a => a.delta > 0).sort((a,b) => (b.delta * b.weight) - (a.delta * a.weight));
    const neg = attributions.filter(a => a.delta < 0).sort((a,b) => (a.delta * a.weight) - (b.delta * b.weight));

    if (pos.length > 0) {
      const lift = Math.round(pos[0].delta * pos[0].weight * 35 * 10) / 10;
      reasons.push(`Primary Positive Driver: High proficiency in '${pos[0].feat}' (${pos[0].val}/5.0) contributes +${lift}% probability uplift above baseline.`);
    }
    if (neg.length > 0) {
      const drag = Math.round(Math.abs(neg[0].delta * neg[0].weight * 35 * 10)) / 10;
      reasons.push(`Primary Bottleneck: Sub-cohort performance in '${neg[0].feat}' (${neg[0].val}/5.0) dampens hike probability by -${drag}%.`);
    } else {
      reasons.push("Skills are well-balanced across all technical dimensions.");
    }

    const netLift = Math.round((prob - 0.525) * 1000) / 1000;
    const conf = (Math.min(0.98, Math.max(0.68, Math.abs(prob - 0.5) * 1.6 + 0.65)) * 100).toFixed(0) + '%';

    return {
      prediction: {
        probability_high_hike: prob,
        predicted_hike_class: hikeClass
      },
      xai_explanation: {
        confidence_level: conf,
        net_probability_lift: netLift,
        defensible_rationale: reasons
      }
    };
  }

  // Predictive SDS Success Model
  if (endpoint === '/api/predict/sds-success') {
    payload = payload || {};
    const c = parseFloat(payload.conscientiousness || 0.72);
    const o = parseFloat(payload.openness_to_experience || 0.70);
    const e = parseFloat(payload.extraversion || 0.60);
    const a = parseFloat(payload.agreeableness || 0.65);
    const n = parseFloat(payload.neuroticism || 0.40);

    const baselines = { c: 0.72, o: 0.70, e: 0.61, a: 0.64, n: 0.39 };
    const delta = 0.35 * (c - baselines.c) +
                  0.28 * (o - baselines.o) +
                  0.22 * (e - baselines.e) +
                  0.18 * (a - baselines.a) -
                  0.38 * (n - baselines.n);

    const rawProb = 1 / (1 + Math.exp(-(0.35 + 4.2 * delta)));
    const prob = Math.min(0.98, Math.max(0.05, Math.round(rawProb * 1000) / 1000));
    const successClass = prob >= 0.50 ? 'High Success' : 'Low / Moderate Success';

    const reasons = [];
    if (c >= 0.75) {
      reasons.push(`High Conscientiousness (${(c*100).toFixed(0)}%) guarantees operational rigor in client-facing milestones.`);
    }
    if (n >= 0.45) {
      reasons.push(`Elevated Neuroticism (${(n*100).toFixed(0)}%) introduces emotional volatility risk under deadline pressure.`);
    } else {
      reasons.push(`Low Neuroticism (${(n*100).toFixed(0)}%) reflects high emotional stability in stakeholder negotiation.`);
    }
    if (o >= 0.75) {
      reasons.push(`High Openness (${(o*100).toFixed(0)}%) drives continuous architectural innovation.`);
    }

    const netLift = Math.round((prob - 0.58) * 1000) / 1000;
    const conf = (Math.min(0.98, Math.max(0.70, Math.abs(prob - 0.5) * 1.6 + 0.68)) * 100).toFixed(0) + '%';

    return {
      prediction: {
        probability_high_success: prob,
        predicted_success_class: successClass
      },
      xai_explanation: {
        confidence_level: conf,
        net_probability_lift: netLift,
        defensible_rationale: reasons
      }
    };
  }

  // Career GPS & Optimizer
  if (endpoint === '/api/career-optimizer') {
    payload = payload || {};
    const targets = [
      {
        target_role: 'Lead Data Scientist',
        target_median_salary_lpa: 22.5,
        min_exp: 5.0,
        core_skills: ['Python', 'Machine Learning', 'Statistical Modeling', 'Spark / PySpark', 'Deep Learning'],
        pathway_tier: 'Strategic Bet (Tier 1)',
        milestones: [
          { phase: 'Phase 1: Bridge Foundations', objective: 'Master PySpark & Advanced Modeling on distributed datasets.' },
          { phase: 'Phase 2: Production Scale', objective: 'Deploy end-to-end MLOps pipelines with Docker & Kubernetes.' },
          { phase: 'Phase 3: Executive Alignment', objective: 'Defend business value & model governance in stakeholder forums.' }
        ]
      },
      {
        target_role: 'Machine Learning Engineer',
        target_median_salary_lpa: 16.5,
        min_exp: 3.0,
        core_skills: ['Python', 'Machine Learning', 'Deep Learning', 'Docker / Kubernetes', 'ETL Pipelines'],
        pathway_tier: 'High Demand (Tier 1)',
        milestones: [
          { phase: 'Phase 1: Bridge Foundations', objective: 'Transition from analytical scripts to production Python microservices.' },
          { phase: 'Phase 2: Scalable Serving', objective: 'Package ML inference APIs into Docker containers.' },
          { phase: 'Phase 3: CI/CD & Drift', objective: 'Implement automated retraining and latency benchmarks.' }
        ]
      },
      {
        target_role: 'Data Architect',
        target_median_salary_lpa: 24.0,
        min_exp: 7.0,
        core_skills: ['SQL', 'Python', 'AWS', 'Azure', 'Hadoop', 'Spark / PySpark', 'ETL Pipelines'],
        pathway_tier: 'Enterprise Elite (Tier 1)',
        milestones: [
          { phase: 'Phase 1: Architecture Core', objective: 'Design distributed lakehouse architectures across multi-cloud.' },
          { phase: 'Phase 2: Governance & Security', objective: 'Establish enterprise schema evolution and RBAC access models.' },
          { phase: 'Phase 3: Cost Optimization', objective: 'Deliver FinOps query performance optimization and storage pruning.' }
        ]
      },
      {
        target_role: 'Senior Data Engineer',
        target_median_salary_lpa: 18.0,
        min_exp: 4.5,
        core_skills: ['SQL', 'Python', 'Spark / PySpark', 'Hadoop', 'ETL Pipelines', 'AWS'],
        pathway_tier: 'High Demand (Tier 1)',
        milestones: [
          { phase: 'Phase 1: Data Modernization', objective: 'Migrate legacy batch ETL to streaming event architectures.' },
          { phase: 'Phase 2: Distributed Spark', objective: 'Optimize partition layout, broadcast joins, and caching in PySpark.' },
          { phase: 'Phase 3: Orchestration', objective: 'Build resilient DAG workflows with Airflow & automated alerting.' }
        ]
      },
      {
        target_role: 'Business Intelligence Architect',
        target_median_salary_lpa: 19.0,
        min_exp: 6.0,
        core_skills: ['SQL', 'Tableau', 'Power BI', 'Excel / Advanced Excel', 'ETL Pipelines', 'AWS'],
        pathway_tier: 'Strategic Bet (Tier 2)',
        milestones: [
          { phase: 'Phase 1: Semantic Modeling', objective: 'Design enterprise dimensional star schemas and Kimball models.' },
          { phase: 'Phase 2: Real-time Dashboards', objective: 'Integrate direct lake and push streaming for sub-second executive KPIs.' },
          { phase: 'Phase 3: Self-Service BI', objective: 'Deploy certified data marts and self-service governance policies.' }
        ]
      }
    ];

    const userSkills = payload.skills || ['SQL', 'Tableau'];
    const curSal = parseFloat(payload.salary_lpa || 8.0);
    const curExp = parseFloat(payload.experience || 3.0);
    const obj = payload.objective || 'MAX_HIKE';

    const pathways = targets.map(t => {
      const matching = t.core_skills.filter(s => userSkills.includes(s));
      const missing = t.core_skills.filter(s => !userSkills.includes(s));
      const skillOverlap = matching.length / t.core_skills.length;
      const expRatio = Math.min(1.2, curExp / t.min_exp);
      const feasibility = Math.round(Math.min(95, Math.max(28, (skillOverlap * 65 + expRatio * 35))));
      const deltaLpa = Math.round((t.target_median_salary_lpa - curSal) * 10) / 10;
      const upliftPct = Math.round((deltaLpa / curSal) * 1000) / 10;

      return {
        target_role: t.target_role,
        target_median_salary_lpa: t.target_median_salary_lpa,
        feasibility_pct: feasibility,
        salary_delta_lpa: deltaLpa,
        salary_uplift_pct: upliftPct,
        pathway_tier: t.pathway_tier,
        missing_critical_skills: missing,
        milestones: t.milestones
      };
    });

    if (obj === 'FAST_TRANSITION') {
      pathways.sort((a,b) => b.feasibility_pct - a.feasibility_pct);
    } else if (obj === 'BALANCED') {
      pathways.sort((a,b) => (b.feasibility_pct * 0.5 + b.salary_uplift_pct * 0.5) - (a.feasibility_pct * 0.5 + a.salary_uplift_pct * 0.5));
    } else {
      pathways.sort((a,b) => b.salary_delta_lpa - a.salary_delta_lpa);
    }

    return {
      primary_recommendation: pathways[0],
      ranked_alternatives: pathways.slice(1)
    };
  }

  // Skill Optimizer
  if (endpoint === '/api/skill-optimizer') {
    return {
      top_recommended_skill: 'Generative AI / LLMs',
      top_recommendation_reason: 'Generative AI and PySpark yield maximum pricing power (+₹5.2L to +₹5.5L premium) with rapid market adoption.',
      skill_investment_rankings: [
        { skill: 'Generative AI / LLMs', associated_trait: 'ai_and_ml_skills', strategic_roi_score: 94.2, marginal_hike_gain_pct: 18.5, market_demand_postings: 2450, market_salary_premium_lpa: 5.2 },
        { skill: 'Spark / PySpark', associated_trait: 'big_data_skills', strategic_roi_score: 91.8, marginal_hike_gain_pct: 16.2, market_demand_postings: 3210, market_salary_premium_lpa: 4.8 },
        { skill: 'Python', associated_trait: 'coding_skills', strategic_roi_score: 89.5, marginal_hike_gain_pct: 14.8, market_demand_postings: 6850, market_salary_premium_lpa: 4.5 },
        { skill: 'Machine Learning', associated_trait: 'ai_and_ml_skills', strategic_roi_score: 88.0, marginal_hike_gain_pct: 15.0, market_demand_postings: 4920, market_salary_premium_lpa: 4.8 },
        { skill: 'AWS / Cloud Engineering', associated_trait: 'big_data_skills', strategic_roi_score: 84.6, marginal_hike_gain_pct: 12.4, market_demand_postings: 3780, market_salary_premium_lpa: 4.2 },
        { skill: 'Deep Learning', associated_trait: 'ai_and_ml_skills', strategic_roi_score: 82.1, marginal_hike_gain_pct: 13.1, market_demand_postings: 2190, market_salary_premium_lpa: 4.6 },
        { skill: 'Statistical Modeling', associated_trait: 'maths_stats_skills', strategic_roi_score: 79.8, marginal_hike_gain_pct: 11.5, market_demand_postings: 2840, market_salary_premium_lpa: 3.8 }
      ]
    };
  }

  // Skill Gap Engine
  if (endpoint === '/api/skill-gap') {
    payload = payload || {};
    const roleBenchmarks = {
      'Data Scientist': [
        { skill: 'Python', target_benchmark_level: 4.5, candidate_current_level: payload.ratings && payload.ratings['Python'] ? payload.ratings['Python'] : 3.8 },
        { skill: 'Machine Learning', target_benchmark_level: 4.5, candidate_current_level: payload.ratings && payload.ratings['Machine Learning'] ? payload.ratings['Machine Learning'] : 3.0 },
        { skill: 'SQL', target_benchmark_level: 4.0, candidate_current_level: 4.5 },
        { skill: 'Statistical Modeling', target_benchmark_level: 4.2, candidate_current_level: 3.2 },
        { skill: 'Tableau', target_benchmark_level: 3.0, candidate_current_level: 4.0 },
        { skill: 'Spark / PySpark', target_benchmark_level: 3.8, candidate_current_level: 2.0 }
      ],
      'Machine Learning Engineer': [
        { skill: 'Python', target_benchmark_level: 4.8, candidate_current_level: 3.8 },
        { skill: 'Machine Learning', target_benchmark_level: 4.7, candidate_current_level: 3.0 },
        { skill: 'Deep Learning', target_benchmark_level: 4.2, candidate_current_level: 2.2 },
        { skill: 'Docker / Kubernetes', target_benchmark_level: 3.8, candidate_current_level: 1.5 },
        { skill: 'ETL Pipelines', target_benchmark_level: 4.0, candidate_current_level: 3.5 },
        { skill: 'SQL', target_benchmark_level: 3.8, candidate_current_level: 4.5 }
      ],
      'Data Architect': [
        { skill: 'SQL', target_benchmark_level: 4.8, candidate_current_level: 4.5 },
        { skill: 'AWS / Cloud', target_benchmark_level: 4.5, candidate_current_level: 2.5 },
        { skill: 'ETL Pipelines', target_benchmark_level: 4.8, candidate_current_level: 3.5 },
        { skill: 'Spark / PySpark', target_benchmark_level: 4.2, candidate_current_level: 2.0 },
        { skill: 'Data Modeling', target_benchmark_level: 4.8, candidate_current_level: 3.8 },
        { skill: 'Python', target_benchmark_level: 4.0, candidate_current_level: 3.8 }
      ]
    };
    const details = roleBenchmarks[payload.target_role] || roleBenchmarks['Data Scientist'];
    const deficits = details.filter(d => d.target_benchmark_level > d.candidate_current_level);
    const avgRatio = details.reduce((acc, d) => acc + (d.candidate_current_level / d.target_benchmark_level), 0) / details.length;
    const readiness = Math.round(Math.min(100, avgRatio * 100));

    return {
      skill_gap_details: details,
      overall_role_readiness_pct: readiness,
      critical_gaps_count: deficits.length,
      top_priority_gaps: deficits
    };
  }

  // Workforce Digital Twin Simulator
  if (endpoint === '/api/simulator') {
    payload = payload || {};
    const N = parseInt(payload.cohort_size || 100);
    const P = parseFloat(payload.upskill_pct || 30.0);
    const count = Math.round(N * (P / 100));
    const intCost = Math.round(count * 0.60 * 10) / 10;
    const extCost = Math.round(count * 3.80 * 10) / 10;
    const savings = Math.round((extCost - intCost) * 10) / 10;
    const roi = (extCost / (intCost || 1)).toFixed(1) + 'x ROI';

    const highPerf = Math.min(95, Math.round((51.0 + P * 0.77) * 10) / 10);
    const hikeProb = Math.min(92, Math.round((52.4 + P * 0.54) * 10) / 10);

    return {
      upskilled_employees_count: count,
      build_vs_buy_economics: {
        internal_reskilling_investment_lpa: intCost,
        equivalent_external_acquisition_cost_lpa: extCost,
        net_capital_saved_lpa: savings,
        reskilling_roi_multiplier: roi,
        strategic_recommendation: `BUILD (Internal Upskilling) strongly validated. Generates ₹${savings} Lakhs in net capital savings at a ${roi} economic multiplier.`
      },
      baseline_metrics: {
        high_performance_rate_pct: 51.0,
        average_hike_probability: 52.4
      },
      post_simulation_metrics: {
        high_performance_rate_pct: highPerf,
        average_hike_probability: hikeProb
      }
    };
  }

  // Copilot Natural Language Assistant
  if (endpoint === '/api/copilot') {
    payload = payload || {};
    const q = (payload.query || '').toLowerCase();
    let resp = '';

    if (q.includes('salary') || q.includes('highest paying') || q.includes('benchmark')) {
      resp = `### 📊 Job Market Salary Benchmarks (Analyzed across 13,900+ Postings)\n\n` +
             `The empirical salary hierarchy across standardized analytics roles:\n\n` +
             `| Rank | Standardized Role | Median Salary (LPA) | 25th - 75th Percentile | Avg Exp Required |\n` +
             `| :--- | :--- | :--- | :--- | :--- |\n` +
             `| **#1** | Data Architect | **₹24.0 L** | ₹16.0L - ₹35.0L | 9.4 yrs |\n` +
             `| **#2** | Lead Data Scientist | **₹22.5 L** | ₹15.0L - ₹32.0L | 7.8 yrs |\n` +
             `| **#3** | Business Intelligence Architect | **₹19.0 L** | ₹13.0L - ₹27.0L | 7.2 yrs |\n` +
             `| **#4** | Senior Data Engineer | **₹18.0 L** | ₹12.0L - ₹26.0L | 6.5 yrs |\n` +
             `| **#5** | Machine Learning Engineer | **₹16.5 L** | ₹10.5L - ₹24.0L | 4.8 yrs |\n\n` +
             `**Key Insight:** **Data Architect** leads the market at a median of **₹24.0 LPA**, followed closely by **Lead Data Scientist** (**₹22.5 LPA**).`;
    } else if (q.includes('premium') || q.includes('python') || q.includes('spark') || q.includes('skill')) {
      resp = `### 💡 Empirical Skill Demand & Salary Premiums\n\n` +
             `Based on NLP extraction across 12,000+ job descriptions:\n\n` +
             `| Skill | Category | Market Demand (Postings) | Penetration % | Salary Premium (LPA) |\n` +
             `| :--- | :--- | :--- | :--- | :--- |\n` +
             `| **Python** | Coding & Scripting | 6,850 | 56.8% | **+₹4.5 LPA** (+36.0%) |\n` +
             `| **Spark / PySpark** | Big Data Engineering | 3,210 | 26.6% | **+₹5.2 LPA** (+41.6%) |\n` +
             `| **Machine Learning** | AI & Advanced Analytics | 4,920 | 40.8% | **+₹4.8 LPA** (+38.4%) |\n` +
             `| **Generative AI / LLMs** | AI & Advanced Analytics | 2,450 | 20.3% | **+₹5.5 LPA** (+44.0%) |\n` +
             `| **SQL** | Core Data Manipulation | 9,840 | 81.6% | **+₹1.2 LPA** (+9.6%) |\n\n` +
             `**Strategic Takeaway:** While **SQL** forms mandatory table stakes (81.6% market penetration), specialized skills like **Python, PySpark, and Generative AI** command an immediate **+₹4.5 to ₹5.5 Lakhs** empirical compensation premium.`;
    } else if (q.includes('transition') || q.includes('pathway') || q.includes('gps') || q.includes('analyst')) {
      resp = `### 🧭 AI Career GPS: Transition Pathways for Data Analyst\n\n` +
             `**Primary Recommended Destination:** **Machine Learning Engineer**\n` +
             `- **Feasibility Score:** \`78%\` (Low-to-Medium Friction)\n` +
             `- **Expected Compensation:** **₹16.5 LPA** (+₹8.5 LPA / +106.3%)\n` +
             `- **Missing Critical Skills:** \`Python, Machine Learning, Deep Learning, Docker / Kubernetes\`\n\n` +
             `**Step-by-Step Chronological Flight Plan:**\n` +
             `1. **Phase 1: Bridge Foundations**: Transition from spreadsheet/SQL logic to Python microservices.\n` +
             `2. **Phase 2: Scalable Modeling**: Train GBDT and Deep Learning models on cloud datasets.\n` +
             `3. **Phase 3: Production Serving**: Containerize models with Docker and configure CI/CD test automation.`;
    } else if (q.includes('simulate') || q.includes('build vs buy') || q.includes('cohort') || q.includes('reskill')) {
      resp = `### 🏢 Workforce Digital Twin: Cohort Simulation (100 Data Scientists)\n\n` +
             `**Scenario:** Upskilling 30% of Junior Cohort in **AI & Machine Learning** + **Advanced Coding**.\n\n` +
             `- **Baseline High Performance Rate:** \`51.0%\` -> **Simulated:** \`74.0%\` (+23 Engineers)\n` +
             `- **Average Hike Likelihood:** \`52.4%\` -> **Simulated:** \`68.7%\` (+16.3%)\n` +
             `- **Internal Reskilling Cost:** **₹18.0 Lakhs** (₹0.60L/head)\n` +
             `- **External Acquisition Cost:** **₹114.0 Lakhs** (₹3.80L/head)\n` +
             `- **Net Capital Saved:** **₹96.0 Lakhs**\n` +
             `- **Return on Investment (ROI):** **6.3× ROI**\n\n` +
             `**Strategic Verdict:** **BUILD (Internal Upskilling)** strongly outperforms external recruiting by preserving institutional domain knowledge while slashing talent acquisition expenditures by 84%.`;
    } else {
      resp = `### ⚡ WorkforceX Copilot Response\n\n` +
             `I can answer questions regarding any part of our SAS CU Hackathon analytics platform:\n\n` +
             `- **Job Market Benchmarks:** Ask *"What is the highest paying role?"* or *"Show salary benchmarks"*\n` +
             `- **Skill Premiums:** Ask *"What is the salary premium for Python?"* or *"Which skill pays the most?"*\n` +
             `- **Career Transitions:** Ask *"How do I transition from Data Analyst to ML Engineer?"*\n` +
             `- **Skill Optimization:** Ask *"Which skill should I learn next for maximum ROI?"*\n` +
             `- **Workforce Digital Twin:** Ask *"Simulate Build vs Buy economics for 100 engineers"*\n\n` +
             `Try asking any of the above questions!`;
    }

    return { response: resp };
  }

  return {};
}

// --- Tab 2: Data Quality ---
async function initDataQuality() {
  try {
    const data = await apiFetch('/api/data-quality');
    
    document.getElementById('dq-completeness').innerText = data.completeness_score_pct + '%';
    document.getElementById('dq-validity').innerText = data.validity_score_pct + '%';
    document.getElementById('dq-consistency').innerText = data.consistency_score_pct + '%';
    document.getElementById('dq-records').innerText = (data.total_analyzed_records || 13965).toLocaleString();

    // Outlier Chart
    const ctx = document.getElementById('chart-outliers').getContext('2d');
    chartOutliers = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['< 5 LPA', '5 - 10 LPA', '10 - 20 LPA', '20 - 35 LPA', '35 - 50 LPA', '50+ LPA (Outlier Tier)'],
        datasets: [{
          label: 'Postings Volume',
          data: [1850, 4820, 4310, 1940, 720, 325],
          backgroundColor: [
            'rgba(58, 123, 213, 0.6)',
            'rgba(0, 210, 255, 0.6)',
            'rgba(0, 242, 254, 0.6)',
            'rgba(246, 211, 101, 0.6)',
            'rgba(255, 65, 108, 0.6)',
            'rgba(255, 65, 108, 0.9)'
          ],
          borderColor: 'rgba(255,255,255,0.2)',
          borderWidth: 1,
          borderRadius: 6
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: {
          x: { grid: { color: 'rgba(64, 93, 160, 0.1)' }, ticks: { color: '#8fa0c2' } },
          y: { grid: { color: 'rgba(64, 93, 160, 0.1)' }, ticks: { color: '#8fa0c2' } }
        }
      }
    });
  } catch (err) {
    console.error('Data Quality init error:', err);
  }
}

// --- Tab 3: Market Intelligence ---
async function initMarketIntelligence() {
  try {
    const data = await apiFetch('/api/market-intelligence');
    
    // Roles Salary Benchmarks (Horizontal Bar)
    const roles = data.role_benchmarks;
    const ctxRoles = document.getElementById('chart-roles-salary').getContext('2d');
    chartRoles = new Chart(ctxRoles, {
      type: 'bar',
      data: {
        labels: roles.map(r => r.role),
        datasets: [
          {
            label: '25th Percentile LPA',
            data: roles.map(r => r.p25_lpa),
            backgroundColor: 'rgba(58, 123, 213, 0.4)',
            borderRadius: 4
          },
          {
            label: 'Median Salary LPA',
            data: roles.map(r => r.median_lpa),
            backgroundColor: 'rgba(0, 210, 255, 0.8)',
            borderRadius: 4
          },
          {
            label: '75th Percentile LPA',
            data: roles.map(r => r.p75_lpa),
            backgroundColor: 'rgba(0, 242, 254, 0.4)',
            borderRadius: 4
          }
        ]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        plugins: { legend: { labels: { color: '#8fa0c2' } } },
        scales: {
          x: { grid: { color: 'rgba(64, 93, 160, 0.1)' }, ticks: { color: '#8fa0c2' } },
          y: { grid: { display: false }, ticks: { color: '#f0f4fc' } }
        }
      }
    });

    // Experience Progression
    const expData = data.experience_progression;
    const ctxExp = document.getElementById('chart-exp-progression').getContext('2d');
    chartExp = new Chart(ctxExp, {
      type: 'line',
      data: {
        labels: expData.map(e => e.experience_tier.split(' ')[0]),
        datasets: [{
          label: 'Median LPA',
          data: expData.map(e => e.overall_median_lpa),
          borderColor: '#00d2ff',
          backgroundColor: 'rgba(0, 210, 255, 0.15)',
          fill: true,
          tension: 0.3,
          pointRadius: 5,
          pointBackgroundColor: '#00d2ff'
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: {
          x: { grid: { color: 'rgba(64, 93, 160, 0.1)' }, ticks: { color: '#8fa0c2' } },
          y: { grid: { color: 'rgba(64, 93, 160, 0.1)' }, ticks: { color: '#8fa0c2' } }
        }
      }
    });

    // Company Tiers
    const tierData = data.company_tiers;
    const ctxTiers = document.getElementById('chart-company-tiers').getContext('2d');
    chartTiers = new Chart(ctxTiers, {
      type: 'bar',
      data: {
        labels: tierData.map(t => t.company_tier.split(' ')[0] + ' ' + (t.company_tier.split(' ')[1] || '')),
        datasets: [{
          label: 'Median LPA',
          data: tierData.map(t => t.median_salary_lpa),
          backgroundColor: 'rgba(127, 0, 255, 0.7)',
          borderRadius: 4
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: {
          x: { grid: { display: false }, ticks: { color: '#8fa0c2', font: { size: 10 } } },
          y: { grid: { color: 'rgba(64, 93, 160, 0.1)' }, ticks: { color: '#8fa0c2' } }
        }
      }
    });

    // Geo Hubs
    const geoData = data.geographic_hubs;
    const ctxGeo = document.getElementById('chart-geo-hubs').getContext('2d');
    chartGeo = new Chart(ctxGeo, {
      type: 'doughnut',
      data: {
        labels: geoData.slice(0, 5).map(g => g.metro),
        datasets: [{
          data: geoData.slice(0, 5).map(g => g.total_job_postings),
          backgroundColor: ['#00d2ff', '#3a7bd5', '#7f00ff', '#f6d365', '#ff416c']
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { position: 'right', labels: { color: '#8fa0c2', font: { size: 10 } } } }
      }
    });

  } catch (err) {
    console.error('Market intelligence error:', err);
  }
}

// --- Tab 4: Predictive ML & XAI ---
async function initMLModels() {
  try {
    const data = await apiFetch('/api/ml-models-report');
    
    // JDS stats
    const jds = data.junior_data_scientist_skill_model;
    const jdsBest = jds.models[jds.best_model];
    document.getElementById('jds-best-tag').innerText = jds.best_model;
    document.getElementById('jds-roc-auc').innerText = (jdsBest.cv_roc_auc * 100).toFixed(1) + '%';
    document.getElementById('jds-f1').innerText = (jdsBest.cv_f1 * 100).toFixed(1) + '%';
    document.getElementById('jds-acc').innerText = (jdsBest.cv_accuracy * 100).toFixed(1) + '%';

    // SDS stats
    const sds = data.senior_data_scientist_personality_model;
    const sdsBest = sds.models[sds.best_model];
    document.getElementById('sds-best-tag').innerText = sds.best_model;
    document.getElementById('sds-roc-auc').innerText = (sdsBest.cv_roc_auc * 100).toFixed(1) + '%';
    document.getElementById('sds-f1').innerText = (sdsBest.cv_f1 * 100).toFixed(1) + '%';
    document.getElementById('sds-acc').innerText = (sdsBest.cv_accuracy * 100).toFixed(1) + '%';

    // JDS Feature Importance Chart
    const jdsImp = jdsBest.feature_importance;
    const ctxJds = document.getElementById('chart-jds-importance').getContext('2d');
    chartJdsImp = new Chart(ctxJds, {
      type: 'bar',
      data: {
        labels: Object.keys(jdsImp).map(k => k.replace('_skills', '').replace('_', ' ').toUpperCase()),
        datasets: [{
          data: Object.values(jdsImp),
          backgroundColor: 'rgba(0, 210, 255, 0.7)',
          borderRadius: 4
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        plugins: { legend: { display: false } },
        scales: {
          x: { grid: { color: 'rgba(64, 93, 160, 0.1)' }, ticks: { color: '#8fa0c2' } },
          y: { grid: { display: false }, ticks: { color: '#f0f4fc' } }
        }
      }
    });

    // SDS Feature Importance Chart
    const sdsImp = sdsBest.feature_importance;
    const ctxSds = document.getElementById('chart-sds-importance').getContext('2d');
    chartSdsImp = new Chart(ctxSds, {
      type: 'bar',
      data: {
        labels: Object.keys(sdsImp).map(k => k.replace('_to_experience', '').toUpperCase()),
        datasets: [{
          data: Object.values(sdsImp),
          backgroundColor: 'rgba(192, 132, 252, 0.7)',
          borderRadius: 4
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        plugins: { legend: { display: false } },
        scales: {
          x: { grid: { color: 'rgba(64, 93, 160, 0.1)' }, ticks: { color: '#8fa0c2' } },
          y: { grid: { display: false }, ticks: { color: '#f0f4fc' } }
        }
      }
    });

    // Bind JDS interactive sliders
    ['coding', 'aiml', 'math', 'bigdata', 'story'].forEach(id => {
      const sl = document.getElementById(`sl-${id}`);
      const val = document.getElementById(`val-${id}`);
      if (sl && val) {
        sl.addEventListener('input', () => { val.innerText = sl.value; });
      }
    });

    // Bind SDS interactive sliders
    ['c', 'o', 'e', 'a', 'n'].forEach(id => {
      const sl = document.getElementById(`sl-${id}`);
      const val = document.getElementById(`val-${id}`);
      if (sl && val) {
        sl.addEventListener('input', () => { val.innerText = sl.value; });
      }
    });

    // JDS evaluation button
    document.getElementById('btn-eval-jds').addEventListener('click', evalJDS);
    evalJDS(); // Trigger default

    // SDS evaluation button
    document.getElementById('btn-eval-sds').addEventListener('click', evalSDS);
    evalSDS(); // Trigger default

  } catch (err) {
    console.error('ML model report error:', err);
  }
}

async function evalJDS() {
  const payload = {
    coding_skills: parseFloat(document.getElementById('sl-coding').value),
    ai_and_ml_skills: parseFloat(document.getElementById('sl-aiml').value),
    maths_stats_skills: parseFloat(document.getElementById('sl-math').value),
    big_data_skills: parseFloat(document.getElementById('sl-bigdata').value),
    dashboard_and_storytelling_skills: parseFloat(document.getElementById('sl-story').value)
  };

  try {
    const data = await apiFetch('/api/predict/jds-hike', 'POST', payload);
    const prob = (data.prediction.probability_high_hike * 100).toFixed(1);
    document.getElementById('jds-pred-prob').innerText = `${prob}%`;
    document.getElementById('jds-pred-status').innerText = data.prediction.predicted_hike_class;
    
    // Rationale text
    const xai = data.xai_explanation;
    let html = `<strong>Confidence: ${xai.confidence_level} | Net Lift vs Baseline: ${xai.net_probability_lift > 0 ? '+' : ''}${(xai.net_probability_lift * 100).toFixed(1)}%</strong><br>`;
    xai.defensible_rationale.forEach(r => {
      html += `• ${r}<br>`;
    });
    document.getElementById('jds-xai-rationale').innerHTML = html;
  } catch (err) {
    console.error('JDS eval error:', err);
  }
}

async function evalSDS() {
  const payload = {
    conscientiousness: parseFloat(document.getElementById('sl-c').value),
    openness_to_experience: parseFloat(document.getElementById('sl-o').value),
    extraversion: parseFloat(document.getElementById('sl-e').value),
    agreeableness: parseFloat(document.getElementById('sl-a').value),
    neuroticism: parseFloat(document.getElementById('sl-n').value)
  };

  try {
    const data = await apiFetch('/api/predict/sds-success', 'POST', payload);
    const prob = (data.prediction.probability_high_success * 100).toFixed(1);
    document.getElementById('sds-pred-prob').innerText = `${prob}%`;
    document.getElementById('sds-pred-status').innerText = data.prediction.predicted_success_class;
    
    const xai = data.xai_explanation;
    let html = `<strong>Confidence: ${xai.confidence_level} | Net Lift vs Baseline: ${xai.net_probability_lift > 0 ? '+' : ''}${(xai.net_probability_lift * 100).toFixed(1)}%</strong><br>`;
    xai.defensible_rationale.forEach(r => {
      html += `• ${r}<br>`;
    });
    document.getElementById('sds-xai-rationale').innerHTML = html;
  } catch (err) {
    console.error('SDS eval error:', err);
  }
}

// --- Tab 5: Market x Success Matrix ---
async function initMatrix() {
  try {
    const data = await apiFetch('/api/market-success-matrix');
    
    const skills = data.skills_matrix;
    const tbody = document.querySelector('#table-matrix-skills tbody');
    tbody.innerHTML = '';

    const scatterData = {
      'Q1: Strategic Core Bets': [],
      'Q2: Table Stakes / Commodity': [],
      'Q3: Elite Differentiators': [],
      'Q4: Specialized / Lower Priority': []
    };

    skills.forEach(s => {
      // Scatter point
      if (scatterData[s.quadrant]) {
        scatterData[s.quadrant].push({
          x: s.market_demand_pct,
          y: s.success_impact_score,
          label: s.skill,
          premium: s.salary_premium_lpa
        });
      }

      // Table row
      const tr = document.createElement('tr');
      const tagClass = s.quadrant_code === 'Q1_Core_Bets' ? 'tag-q1' :
                       s.quadrant_code === 'Q2_Table_Stakes' ? 'tag-q2' :
                       s.quadrant_code === 'Q3_Elite_Differentiators' ? 'tag-q3' : 'tag-q4';
      tr.innerHTML = `
        <td><strong>${s.skill}</strong></td>
        <td>${s.category}</td>
        <td>${s.market_demand_pct}%</td>
        <td>${s.success_impact_score}</td>
        <td><strong style="color:${s.salary_premium_lpa > 0 ? 'var(--accent-cyan)' : 'var(--text-muted)'}">+${s.salary_premium_lpa} LPA</strong></td>
        <td><span class="badge-tag ${tagClass}">${s.quadrant.split(':')[0]}</span></td>
        <td style="font-size:0.75rem; color:var(--text-muted);">${s.strategic_action}</td>
      `;
      tbody.appendChild(tr);
    });

    // Render Scatter Plot
    const ctx = document.getElementById('chart-matrix').getContext('2d');
    chartMatrix = new Chart(ctx, {
      type: 'scatter',
      data: {
        datasets: Object.keys(scatterData).map(k => ({
          label: k,
          data: scatterData[k],
          backgroundColor: k.includes('Q1') ? '#00d2ff' : k.includes('Q2') ? '#f6d365' : k.includes('Q3') ? '#c084fc' : '#ff416c',
          pointRadius: 6,
          pointHoverRadius: 9
        }))
      },
      options: {
        responsive: true,
        plugins: {
          legend: { labels: { color: '#8fa0c2' } },
          tooltip: {
            callbacks: {
              label: (ctx) => `${ctx.raw.label}: Demand ${ctx.raw.x}%, Impact ${ctx.raw.y}, Premium +${ctx.raw.premium} LPA`
            }
          }
        },
        scales: {
          x: {
            title: { display: true, text: 'Market Demand % (Across 12,000+ Job Postings)', color: '#8fa0c2' },
            grid: { color: 'rgba(64, 93, 160, 0.15)' },
            ticks: { color: '#8fa0c2' }
          },
          y: {
            title: { display: true, text: 'Empirical Success Impact Score (0 - 100)', color: '#8fa0c2' },
            grid: { color: 'rgba(64, 93, 160, 0.15)' },
            ticks: { color: '#8fa0c2' }
          }
        }
      }
    });

  } catch (err) {
    console.error('Matrix error:', err);
  }
}

// --- Tab 6: AI Career GPS & Graph ---
async function initCareerGPS() {
  const commonSkills = [
    'Python', 'SQL', 'R', 'SAS', 'Tableau', 'Power BI', 'Excel / Advanced Excel',
    'Machine Learning', 'Deep Learning', 'Generative AI / LLMs', 'Spark / PySpark',
    'Hadoop', 'AWS', 'Azure', 'Docker / Kubernetes', 'ETL Pipelines', 'Statistical Modeling'
  ];

  const chkContainer = document.getElementById('gps-skill-checkboxes');
  chkContainer.innerHTML = '';
  commonSkills.forEach(s => {
    const lbl = document.createElement('label');
    lbl.style.display = 'inline-flex';
    lbl.style.alignItems = 'center';
    lbl.style.gap = '0.3rem';
    lbl.style.fontSize = '0.78rem';
    lbl.style.color = '#f0f4fc';
    lbl.style.background = 'rgba(255,255,255,0.05)';
    lbl.style.padding = '0.2rem 0.5rem';
    lbl.style.borderRadius = '4px';
    lbl.style.cursor = 'pointer';

    const defaultChecked = ['SQL', 'Tableau', 'Excel / Advanced Excel', 'Power BI'].includes(s);
    lbl.innerHTML = `<input type="checkbox" value="${s}" ${defaultChecked ? 'checked' : ''} style="accent-color:var(--accent-cyan);"> ${s}`;
    chkContainer.appendChild(lbl);
  });

  document.getElementById('btn-run-gps').addEventListener('click', runCareerGPS);
  runCareerGPS(); // Trigger default
  loadNetworkGraph();
}

async function runCareerGPS() {
  const currentRole = document.getElementById('gps-current-role').value;
  const exp = parseFloat(document.getElementById('gps-exp').value);
  const salary = parseFloat(document.getElementById('gps-salary').value);
  const objective = document.getElementById('gps-objective').value;

  const chks = document.querySelectorAll('#gps-skill-checkboxes input:checked');
  const skills = Array.from(chks).map(c => c.value);

  try {
    const data = await apiFetch('/api/career-optimizer', 'POST', {
      current_role: currentRole,
      experience: exp,
      salary_lpa: salary,
      skills: skills,
      objective: objective
    });
    
    const container = document.getElementById('gps-pathways-container');
    container.innerHTML = '';

    const paths = [data.primary_recommendation, ...(data.ranked_alternatives || [])];
    
    paths.forEach((p, idx) => {
      const card = document.createElement('div');
      card.style.background = idx === 0 ? 'rgba(0, 210, 255, 0.08)' : 'rgba(255,255,255,0.02)';
      card.style.border = `1px solid ${idx === 0 ? 'var(--accent-cyan)' : 'var(--border-color)'}`;
      card.style.borderRadius = '8px';
      card.style.padding = '0.8rem';

      let milestonesHtml = '';
      if (p.milestones && p.milestones.length > 0) {
        milestonesHtml = '<div style="margin-top:0.5rem; padding-top:0.5rem; border-top:1px solid rgba(255,255,255,0.05); font-size:0.75rem; color:var(--text-muted);">';
        p.milestones.forEach(m => {
          milestonesHtml += `<div><strong>${m.phase}:</strong> ${m.objective}</div>`;
        });
        milestonesHtml += '</div>';
      }

      card.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <strong style="color:#fff; font-size:0.95rem;">${idx === 0 ? '🥇 ' : ''}${p.target_role}</strong>
          <span class="badge ${p.feasibility_pct >= 60 ? 'badge-score' : 'badge-status'}">${p.feasibility_pct}% Feasibility</span>
        </div>
        <div style="font-size:0.8rem; margin-top:0.3rem;">
          <span style="color:var(--accent-cyan); font-weight:700;">₹${p.target_median_salary_lpa} LPA</span>
          <span style="color:var(--text-muted);"> (+₹${p.salary_delta_lpa} L / +${p.salary_uplift_pct}%)</span> |
          <span style="color:var(--text-muted);">Tier: ${p.pathway_tier.split(' ')[0]}</span>
        </div>
        <div style="font-size:0.75rem; color:var(--text-muted); margin-top:0.4rem;">
          Missing Skills: <strong style="color:#f6d365;">${p.missing_critical_skills.length > 0 ? p.missing_critical_skills.join(', ') : 'None! Direct fit'}</strong>
        </div>
        ${milestonesHtml}
      `;
      container.appendChild(card);
    });

  } catch (err) {
    console.error('GPS error:', err);
  }
}

// D3 Force Directed Network Graph
async function loadNetworkGraph() {
  try {
    const data = await apiFetch('/api/role-skill-graph');
    
    const container = document.getElementById('network-graph-container');
    container.innerHTML = '';
    
    const width = container.clientWidth || 600;
    const height = 400;

    const svg = d3.select('#network-graph-container')
      .append('svg')
      .attr('width', width)
      .attr('height', height);

    const simulation = d3.forceSimulation(data.nodes)
      .force('link', d3.forceLink(data.edges).id(d => d.id).distance(110))
      .force('charge', d3.forceManyBody().strength(-350))
      .force('center', d3.forceCenter(width / 2, height / 2));

    const link = svg.append('g')
      .selectAll('line')
      .data(data.edges)
      .enter().append('line')
      .attr('stroke', 'rgba(64, 93, 160, 0.4)')
      .attr('stroke-width', d => Math.max(1, d.weight * 3));

    const node = svg.append('g')
      .selectAll('g')
      .data(data.nodes)
      .enter().append('g')
      .call(d3.drag()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended));

    node.append('circle')
      .attr('r', d => Math.min(22, Math.max(12, d.median_salary_lpa * 0.7)))
      .attr('fill', d => d.id.includes('Senior') || d.id.includes('Architect') ? '#7f00ff' : '#00d2ff')
      .attr('stroke', '#fff')
      .attr('stroke-width', 1.5);

    node.append('text')
      .text(d => d.id.replace('Senior', 'Sr.').replace('Engineer', 'Eng.'))
      .attr('x', 0)
      .attr('y', 25)
      .attr('text-anchor', 'middle')
      .attr('fill', '#f0f4fc')
      .attr('font-size', '10px')
      .attr('font-weight', '600');

    simulation.on('tick', () => {
      link
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);
      node
        .attr('transform', d => `translate(${d.x},${d.y})`);
    });

    function dragstarted(event, d) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x; d.fy = d.y;
    }
    function dragged(event, d) {
      d.fx = event.x; d.fy = event.y;
    }
    function dragended(event, d) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null; d.fy = null;
    }

  } catch (err) {
    console.error('Network graph error:', err);
  }
}

// --- Tab 7: Skill Optimizer & Gap Engine ---
async function initSkillOptimizer() {
  document.getElementById('btn-calc-roi').addEventListener('click', runSkillOptimizer);
  runSkillOptimizer(); // Run default

  document.getElementById('gap-target-role').addEventListener('change', runSkillGap);
  runSkillGap(); // Run default
}

async function runSkillOptimizer() {
  const payload = {
    big_data_skills: 3.5,
    maths_stats_skills: 3.8,
    coding_skills: 4.0,
    ai_and_ml_skills: 3.2,
    dashboard_and_storytelling_skills: 4.2
  };

  try {
    const data = await apiFetch('/api/skill-optimizer', 'POST', payload);
    
    document.getElementById('roi-top-skill').innerText = `🚀 Strategic Pick: ${data.top_recommended_skill}`;
    document.getElementById('roi-top-reason').innerText = data.top_recommendation_reason;

    const tbody = document.querySelector('#table-roi-rankings tbody');
    tbody.innerHTML = '';
    data.skill_investment_rankings.slice(0, 7).forEach((s, idx) => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><strong>#${idx + 1}</strong></td>
        <td><strong>${s.skill}</strong> <span style="font-size:0.7rem; color:var(--text-muted);">(${s.associated_trait})</span></td>
        <td><strong style="color:var(--accent-cyan);">${s.strategic_roi_score} / 100</strong></td>
        <td><span style="color:var(--accent-emerald);">+${s.marginal_hike_gain_pct}%</span></td>
        <td>${s.market_demand_postings.toLocaleString()} jobs (+${s.market_salary_premium_lpa}L)</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    console.error('Skill optimizer error:', err);
  }
}

async function runSkillGap() {
  const targetRole = document.getElementById('gap-target-role').value;
  const skills = ['SQL', 'Tableau', 'Excel / Advanced Excel', 'Power BI'];
  const ratings = { 'SQL': 4.5, 'Tableau': 4.0, 'Excel / Advanced Excel': 4.8, 'Power BI': 3.8 };

  try {
    const data = await apiFetch('/api/skill-gap', 'POST', {
      target_role: targetRole,
      skills: skills,
      ratings: ratings
    });
    
    const details = data.skill_gap_details.slice(0, 6);
    
    const ctx = document.getElementById('chart-skill-gap').getContext('2d');
    if (chartGap) chartGap.destroy();

    chartGap = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: details.map(d => d.skill),
        datasets: [
          {
            label: 'Role Target Level (1-5)',
            data: details.map(d => d.target_benchmark_level),
            backgroundColor: 'rgba(58, 123, 213, 0.4)',
            borderRadius: 4
          },
          {
            label: 'Your Current Level (1-5)',
            data: details.map(d => d.candidate_current_level),
            backgroundColor: 'rgba(0, 210, 255, 0.8)',
            borderRadius: 4
          }
        ]
      },
      options: {
        responsive: true,
        plugins: { legend: { labels: { color: '#8fa0c2' } } },
        scales: {
          x: { grid: { color: 'rgba(64, 93, 160, 0.1)' }, ticks: { color: '#8fa0c2', font: { size: 9 } } },
          y: { min: 0, max: 5.0, grid: { color: 'rgba(64, 93, 160, 0.1)' }, ticks: { color: '#8fa0c2' } }
        }
      }
    });

    document.getElementById('gap-summary-text').innerHTML = `
      <strong>Overall Target Role Readiness:</strong> <span style="color:var(--accent-cyan); font-weight:700;">${data.overall_role_readiness_pct}%</span> | 
      Critical Deficits: <strong>${data.critical_gaps_count} skills</strong>.<br>
      Top Urgent Learning Gap: <strong>${data.top_priority_gaps[0] ? data.top_priority_gaps[0].skill : 'None'}</strong>.
    `;
  } catch (err) {
    console.error('Skill gap error:', err);
  }
}

// --- Tab 8: Workforce Simulator ---
async function initSimulator() {
  const slSize = document.getElementById('sim-size');
  const valSize = document.getElementById('val-sim-size');
  slSize.addEventListener('input', () => { valSize.innerText = slSize.value; });

  const slPct = document.getElementById('sim-pct');
  const valPct = document.getElementById('val-sim-pct');
  slPct.addEventListener('input', () => { valPct.innerText = slPct.value + '%'; });

  document.getElementById('btn-run-sim').addEventListener('click', runSimulator);
  runSimulator(); // Default
}

async function runSimulator() {
  const size = parseInt(document.getElementById('sim-size').value);
  const pct = parseFloat(document.getElementById('sim-pct').value);
  const focus = document.getElementById('sim-focus').value;

  try {
    const data = await apiFetch('/api/simulator', 'POST', {
      cohort_size: size,
      upskill_pct: pct,
      skill_focus: focus
    });
    
    document.getElementById('sim-cost-internal').innerText = `₹${data.build_vs_buy_economics.internal_reskilling_investment_lpa} L`;
    document.getElementById('sim-cost-external').innerText = `₹${data.build_vs_buy_economics.equivalent_external_acquisition_cost_lpa} L`;
    document.getElementById('sim-savings').innerText = `₹${data.build_vs_buy_economics.net_capital_saved_lpa} Lakhs`;
    document.getElementById('sim-roi').innerText = data.build_vs_buy_economics.reskilling_roi_multiplier;
    document.getElementById('sim-verdict').innerText = data.build_vs_buy_economics.strategic_recommendation;

    // Simulation comparison chart
    const ctx = document.getElementById('chart-sim-comparison').getContext('2d');
    if (chartSim) chartSim.destroy();

    chartSim = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['High Performer Ratio (%)', 'Cohort Average Hike Probability (%)'],
        datasets: [
          {
            label: 'Baseline Status Quo',
            data: [data.baseline_metrics.high_performance_rate_pct, data.baseline_metrics.average_hike_probability],
            backgroundColor: 'rgba(58, 123, 213, 0.5)',
            borderRadius: 6
          },
          {
            label: `Simulated (+${data.upskilled_employees_count} Upskilled)`,
            data: [data.post_simulation_metrics.high_performance_rate_pct, data.post_simulation_metrics.average_hike_probability],
            backgroundColor: 'rgba(0, 210, 255, 0.85)',
            borderRadius: 6
          }
        ]
      },
      options: {
        responsive: true,
        plugins: { legend: { labels: { color: '#8fa0c2' } } },
        scales: {
          x: { grid: { display: false }, ticks: { color: '#f0f4fc' } },
          y: { min: 0, max: 100, grid: { color: 'rgba(64, 93, 160, 0.1)' }, ticks: { color: '#8fa0c2' } }
        }
      }
    });
  } catch (err) {
    console.error('Sim error:', err);
  }
}

// --- Tab 9: Workforce Copilot ---
function initCopilot() {
  const input = document.getElementById('chat-input');
  const btn = document.getElementById('btn-send-chat');

  btn.addEventListener('click', sendChatMessage);
  input.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendChatMessage();
  });
}

async function sendChatMessage() {
  const input = document.getElementById('chat-input');
  const text = input.value.trim();
  if (!text) return;

  const history = document.getElementById('chat-history');

  // Add user bubble
  const userDiv = document.createElement('div');
  userDiv.className = 'chat-message chat-user';
  userDiv.innerText = text;
  history.appendChild(userDiv);
  input.value = '';

  // Add loading placeholder
  const botDiv = document.createElement('div');
  botDiv.className = 'chat-message chat-bot';
  botDiv.innerText = 'Analyzing market data & ML models...';
  history.appendChild(botDiv);
  history.scrollTop = history.scrollHeight;

  try {
    const data = await apiFetch('/api/copilot', 'POST', { query: text });
    
    // Simple markdown conversion
    let formatted = data.response
      .replace(/### (.*?)\n/g, '<h4 style="color:var(--accent-cyan); margin:0.3rem 0;">$1</h4>')
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/\n\n/g, '<br><br>')
      .replace(/\n/g, '<br>');

    botDiv.innerHTML = formatted;
  } catch (err) {
    botDiv.innerText = 'Error processing request.';
  }
  history.scrollTop = history.scrollHeight;
}
