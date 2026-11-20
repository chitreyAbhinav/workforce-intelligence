"""
Build Script for WorkforceX Live GitHub Pages Preview
====================================================
Generates docs/ directory with self-contained assets and client-side inference engine.
"""

import os
import json
import shutil

base_dir = r'C:\Users\chitr_mzkaj0t\.gemini\antigravity\scratch\workforce_intelligence'
proc_dir = os.path.join(base_dir, 'data', 'processed')
docs_dir = os.path.join(base_dir, 'docs')
docs_static_js = os.path.join(docs_dir, 'static', 'js')
docs_static_css = os.path.join(docs_dir, 'static', 'css')
docs_api = os.path.join(docs_dir, 'api')

os.makedirs(docs_static_js, exist_ok=True)
os.makedirs(docs_static_css, exist_ok=True)
os.makedirs(docs_api, exist_ok=True)

# Copy CSS
shutil.copyfile(
    os.path.join(base_dir, 'app', 'static', 'css', 'style.css'),
    os.path.join(docs_static_css, 'style.css')
)

# Load all processed data
files = {
    'data_quality': 'data_quality_report.json',
    'market_intelligence': 'market_intelligence_report.json',
    'market_success_matrix': 'market_success_matrix.json',
    'master_skill_taxonomy': 'master_skill_taxonomy.json',
    'model_metrics_report': 'model_metrics_report.json',
    'role_skill_network_graph': 'role_skill_network_graph.json',
    'role_skill_profiles': 'role_skill_profiles.json'
}

bundle = {}
for key, fname in files.items():
    fp = os.path.join(proc_dir, fname)
    with open(fp, 'r', encoding='utf-8') as f:
        data = json.load(f)
        bundle[key] = data
        with open(os.path.join(docs_api, fname), 'w', encoding='utf-8') as api_f:
            json.dump(data, api_f, indent=2)

# Write bundle-data.js
bundle_js_path = os.path.join(docs_static_js, 'bundle-data.js')
with open(bundle_js_path, 'w', encoding='utf-8') as f:
    f.write('window.WORKFORCEX_DATA = ' + json.dumps(bundle, separators=(',', ':')) + ';\n')

shutil.copyfile(bundle_js_path, os.path.join(base_dir, 'app', 'static', 'js', 'bundle-data.js'))

# Prepare docs/index.html
with open(os.path.join(base_dir, 'app', 'templates', 'index.html'), 'r', encoding='utf-8') as f:
    html = f.read()

# Make CSS and JS paths relative
html_docs = html.replace('href="/static/css/style.css"', 'href="static/css/style.css"')
html_docs = html_docs.replace(
    '<script src="/static/js/app.js"></script>',
    '<script src="static/js/bundle-data.js"></script>\n  <script src="static/js/app.js"></script>'
)

# Add GitHub link and preview tag in badges
old_badges = '<span class="badge badge-status">13,965 Analyzed Records</span>'
new_badges = ('<span class="badge badge-status">13,965 Analyzed Records</span>\n'
              '      <a href="https://github.com/chitreyAbhinav/workforce-intelligence" target="_blank" class="badge" style="background: rgba(0, 210, 255, 0.15); color: #00d2ff; text-decoration: none; border: 1px solid rgba(0, 210, 255, 0.4); display: inline-flex; align-items: center; gap: 0.3rem;">★ GitHub Repository</a>')
html_docs = html_docs.replace(old_badges, new_badges)

with open(os.path.join(docs_dir, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(html_docs)

print("[OK] docs/index.html, bundle-data.js, and static assets created successfully!")
