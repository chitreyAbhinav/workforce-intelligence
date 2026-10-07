// WorkforceX Intelligence Platform - Client JavaScript
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

// --- Tab 2: Data Quality ---
async function initDataQuality() {
  try {
    const res = await fetch('/api/data-quality');
    const data = await res.json();
    
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
    const res = await fetch('/api/market-intelligence');
    const data = await res.json();
    
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
    const res = await fetch('/api/ml-models-report');
    const data = await res.json();
    
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
    const res = await fetch('/api/predict/jds-hike', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
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
    const res = await fetch('/api/predict/sds-success', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
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
    const res = await fetch('/api/market-success-matrix');
    const data = await res.json();
    
    const skills = data.skills_matrix;
    const tbody = document.querySelector('#table-matrix-skills tbody');
    tbody.innerHTML = '';

    const colors = {
      'Q1_Core_Bets': '#00d2ff',
      'Q2_Table_Stakes': '#f6d365',
      'Q3_Elite_Differentiators': '#c084fc',
      'Q4_Low_Priority': '#ff416c'
    };

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
    const res = await fetch('/api/career-optimizer', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        current_role: currentRole,
        experience: exp,
        salary_lpa: salary,
        skills: skills,
        objective: objective
      })
    });
    const data = await res.json();
    
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
    const res = await fetch('/api/role-skill-graph');
    const data = await res.json();
    
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
    const res = await fetch('/api/skill-optimizer', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    
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
    const res = await fetch('/api/skill-gap', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        target_role: targetRole,
        skills: skills,
        ratings: ratings
      })
    });
    const data = await res.json();
    
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
    const res = await fetch('/api/simulator', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        cohort_size: size,
        upskill_pct: pct,
        skill_focus: focus
      })
    });
    const data = await res.json();
    
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
    const res = await fetch('/api/copilot', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: text })
    });
    const data = await res.json();
    
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
