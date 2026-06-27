#!/usr/bin/env python3
"""Build the self-contained skills HTML page."""
import json, os, html

BASE_WS = os.path.expanduser("~/.openclaw/workspace/skills")
BASE_G  = os.path.expanduser("~/.openclaw/skills")

def rd(path, max_lines=500):
    """Read a file, truncate at max_lines."""
    if path is None:
        return {"content": "(fichier binaire)", "binary": True, "truncated": False}
    try:
        with open(os.path.expanduser(path), "r", errors="replace") as f:
            lines = f.readlines()
        truncated = len(lines) > max_lines
        if truncated:
            content = "".join(lines[:max_lines]) + "\n\n... (tronqué — {} lignes au total)".format(len(lines))
        else:
            content = "".join(lines)
        return {"content": content, "binary": False, "truncated": truncated}
    except Exception as e:
        return {"content": f"(erreur de lecture: {e})", "binary": False, "truncated": False}

WORKSPACE_SKILLS = {
    "goal": ([(f"{BASE_WS}/goal/SKILL.md", True)], []),
    "gog": ([(f"{BASE_WS}/gog/SKILL.md", True), (f"{BASE_WS}/gog/_meta.json", False)], []),
    "subagent-creator": ([(f"{BASE_WS}/subagent-creator/SKILL.md", True)], [
        ("references", [
            ("export-patterns.md", f"{BASE_WS}/subagent-creator/references/export-patterns.md", True),
            ("validation-checklist.md", f"{BASE_WS}/subagent-creator/references/validation-checklist.md", True),
            ("artifact-templates.md", f"{BASE_WS}/subagent-creator/references/artifact-templates.md", True),
            ("architecture-principles.md", f"{BASE_WS}/subagent-creator/references/architecture-principles.md", True),
        ])
    ]),
    "teach": ([(f"{BASE_WS}/teach/SKILL.md", True)], [
        ("references", [
            ("MISSION-FORMAT.md", f"{BASE_WS}/teach/references/MISSION-FORMAT.md", True),
            ("RESOURCES-FORMAT.md", f"{BASE_WS}/teach/references/RESOURCES-FORMAT.md", True),
            ("LEARNING-RECORD-FORMAT.md", f"{BASE_WS}/teach/references/LEARNING-RECORD-FORMAT.md", True),
        ])
    ]),
}

GLOBAL_SKILLS = {
    "admin-factory": ([(f"{BASE_G}/admin-factory/SKILL.md", True)], []),
    "agent-architect": ([(f"{BASE_G}/agent-architect/SKILL.md", True)], []),
    "analyse-entretien-ac66": ([(f"{BASE_G}/analyse-entretien-ac66/SKILL.md", True)], []),
    "article-publication": ([(f"{BASE_G}/article-publication/SKILL.md", True)], []),
    "article-writing": ([(f"{BASE_G}/article-writing/SKILL.md", True)], [
        ("references", [
            ("ANTI_CALQUE.md", f"{BASE_G}/article-writing/references/ANTI_CALQUE.md", True),
            ("PREFLIGHT.md", f"{BASE_G}/article-writing/references/PREFLIGHT.md", True),
            ("VOICE_CALIBRATION.md", f"{BASE_G}/article-writing/references/VOICE_CALIBRATION.md", True),
        ])
    ]),
    "bd-carousel": ([(f"{BASE_G}/bd-carousel/SKILL.md", True)], [
        ("references", [
            ("api_reference.md", f"{BASE_G}/bd-carousel/references/api_reference.md", True),
            ("linkedin-specs.md", f"{BASE_G}/bd-carousel/references/linkedin-specs.md", True),
            ("style-guide.md", f"{BASE_G}/bd-carousel/references/style-guide.md", True),
            ("narrative-structure.md", f"{BASE_G}/bd-carousel/references/narrative-structure.md", True),
        ]),
        ("scripts", [
            ("assemble_carousel.py", f"{BASE_G}/bd-carousel/scripts/assemble_carousel.py", False),
            ("example.py", f"{BASE_G}/bd-carousel/scripts/example.py", False),
            ("generate_bd_carousel.py", f"{BASE_G}/bd-carousel/scripts/generate_bd_carousel.py", False),
        ]),
        ("assets", [
            ("example_asset.txt", f"{BASE_G}/bd-carousel/assets/example_asset.txt", False),
        ])
    ]),
    "clawddocs": ([(f"{BASE_G}/clawddocs/SKILL.md", True)], [
        ("snippets", [
            ("common-configs.md", f"{BASE_G}/clawddocs/snippets/common-configs.md", True),
        ]),
        ("scripts", [
            ("build-index.sh", f"{BASE_G}/clawddocs/scripts/build-index.sh", False),
            ("cache.sh", f"{BASE_G}/clawddocs/scripts/cache.sh", False),
            ("fetch-doc.sh", f"{BASE_G}/clawddocs/scripts/fetch-doc.sh", False),
            ("recent.sh", f"{BASE_G}/clawddocs/scripts/recent.sh", False),
            ("search.sh", f"{BASE_G}/clawddocs/scripts/search.sh", False),
            ("sitemap.sh", f"{BASE_G}/clawddocs/scripts/sitemap.sh", False),
            ("track-changes.sh", f"{BASE_G}/clawddocs/scripts/track-changes.sh", False),
        ])
    ]),
    "copywriter-publisher": ([(f"{BASE_G}/copywriter-publisher/SKILL.md", True)], []),
    "doodle-creator": ([(f"{BASE_G}/doodle-creator/SKILL.md", True)], []),
    "fleet-health": ([(f"{BASE_G}/fleet-health/SKILL.md", True)], []),
    "fleet-map": ([(f"{BASE_G}/fleet-map/SKILL.md", True)], [
        ("references", [
            ("fleet-schema.md", f"{BASE_G}/fleet-map/references/fleet-schema.md", True),
            ("agent-interactions.md", f"{BASE_G}/fleet-map/references/agent-interactions.md", True),
        ]),
        ("scripts", [
            ("scan_fleet.py", f"{BASE_G}/fleet-map/scripts/scan_fleet.py", False),
        ])
    ]),
    "google-gemini-tts": ([(f"{BASE_G}/google-gemini-tts/SKILL.md", True), (f"{BASE_G}/google-gemini-tts/README.md", True)], [
        ("scripts", [
            ("gemini_tts.sh", f"{BASE_G}/google-gemini-tts/scripts/gemini_tts.sh", False),
        ])
    ]),
    "linkedin-api": ([(f"{BASE_G}/linkedin-api/SKILL.md", True)], []),
    "linkedin-search": ([(f"{BASE_G}/linkedin-search/SKILL.md", True)], [
        ("references", [
            ("costs.md", f"{BASE_G}/linkedin-search/references/costs.md", True),
        ])
    ]),
    "openclaw-cli": ([(f"{BASE_G}/openclaw-cli/SKILL.md", True), (f"{BASE_G}/openclaw-cli/README.md", True)], [
        ("references", [
            ("command-map.md", f"{BASE_G}/openclaw-cli/references/command-map.md", True),
        ]),
        ("agents", [
            ("openai.yaml", f"{BASE_G}/openclaw-cli/agents/openai.yaml", False),
        ])
    ]),
    "pdf": ([(f"{BASE_G}/pdf/SKILL.md", True)], []),
    "powerpoint-pptx": ([(f"{BASE_G}/powerpoint-pptx/SKILL.md", True)], []),
    "presentation-image-first": ([(f"{BASE_G}/presentation-image-first/SKILL.md", True)], [
        ("references", [
            ("brand-style.yaml", f"{BASE_G}/presentation-image-first/references/brand-style.yaml", False),
            ("charte-graphique.md", f"{BASE_G}/presentation-image-first/references/charte-graphique.md", True),
            ("image-quality-checklist.md", f"{BASE_G}/presentation-image-first/references/image-quality-checklist.md", True),
        ]),
        ("scripts", [
            ("assemble_pptx_from_images.py", f"{BASE_G}/presentation-image-first/scripts/assemble_pptx_from_images.py", False),
        ]),
        ("templates", [
            ("presentation_scenario.md", f"{BASE_G}/presentation-image-first/templates/presentation_scenario.md", True),
            ("slides_manifest.yaml", f"{BASE_G}/presentation-image-first/templates/slides_manifest.yaml", False),
            ("image_prompt_template.txt", f"{BASE_G}/presentation-image-first/templates/image_prompt_template.txt", False),
        ]),
        ("assets", [
            ("logo_reference_laurent_serre_developpement.png", None, None),
            ("photo_reference_laurent_serre.jpg", None, None),
        ])
    ]),
    "self-improving-agent": ([(f"{BASE_G}/self-improving-agent/SKILL.md", True)], [
        ("references", [
            ("examples.md", f"{BASE_G}/self-improving-agent/references/examples.md", True),
            ("hooks-setup.md", f"{BASE_G}/self-improving-agent/references/hooks-setup.md", True),
            ("openclaw-integration.md", f"{BASE_G}/self-improving-agent/references/openclaw-integration.md", True),
        ]),
        ("hooks", [
            ("openclaw/HOOK.md", f"{BASE_G}/self-improving-agent/hooks/openclaw/HOOK.md", True),
        ]),
        ("scripts", [
            ("activator.sh", f"{BASE_G}/self-improving-agent/scripts/activator.sh", False),
            ("error-detector.sh", f"{BASE_G}/self-improving-agent/scripts/error-detector.sh", False),
            ("extract-skill.sh", f"{BASE_G}/self-improving-agent/scripts/extract-skill.sh", False),
        ]),
        ("assets", [
            ("LEARNINGS.md", f"{BASE_G}/self-improving-agent/assets/LEARNINGS.md", True),
            ("ERRORS.md", f"{BASE_G}/self-improving-agent/assets/ERRORS.md", True),
            ("FEATURE_REQUESTS.md", f"{BASE_G}/self-improving-agent/assets/FEATURE_REQUESTS.md", True),
            ("SKILL-TEMPLATE.md", f"{BASE_G}/self-improving-agent/assets/SKILL-TEMPLATE.md", True),
        ])
    ]),
    "serp-analyzer": ([(f"{BASE_G}/serp-analyzer/SKILL.md", True)], []),
    "skill-creator": ([(f"{BASE_G}/skill-creator/SKILL.md", True)], [
        ("references", [
            ("schemas.md", f"{BASE_G}/skill-creator/references/schemas.md", True),
        ]),
        ("agents", [
            ("grader.md", f"{BASE_G}/skill-creator/agents/grader.md", True),
            ("comparator.md", f"{BASE_G}/skill-creator/agents/comparator.md", True),
            ("analyzer.md", f"{BASE_G}/skill-creator/agents/analyzer.md", True),
        ]),
        ("scripts", [
            ("__init__.py", f"{BASE_G}/skill-creator/scripts/__init__.py", False),
            ("aggregate_benchmark.py", f"{BASE_G}/skill-creator/scripts/aggregate_benchmark.py", False),
            ("generate_report.py", f"{BASE_G}/skill-creator/scripts/generate_report.py", False),
            ("improve_description.py", f"{BASE_G}/skill-creator/scripts/improve_description.py", False),
            ("package_skill.py", f"{BASE_G}/skill-creator/scripts/package_skill.py", False),
            ("quick_validate.py", f"{BASE_G}/skill-creator/scripts/quick_validate.py", False),
            ("run_eval.py", f"{BASE_G}/skill-creator/scripts/run_eval.py", False),
            ("run_loop.py", f"{BASE_G}/skill-creator/scripts/run_loop.py", False),
            ("utils.py", f"{BASE_G}/skill-creator/scripts/utils.py", False),
        ]),
        ("assets", [
            ("eval_review.html", f"{BASE_G}/skill-creator/assets/eval_review.html", False),
        ]),
        ("eval-viewer", [
            ("generate_review.py", f"{BASE_G}/skill-creator/eval-viewer/generate_review.py", False),
            ("viewer.html", f"{BASE_G}/skill-creator/eval-viewer/viewer.html", False),
        ])
    ]),
    "skills-registry": ([(f"{BASE_G}/skills-registry/SKILL.md", True)], [
        ("scripts", [
            ("update-registry.py", f"{BASE_G}/skills-registry/scripts/update-registry.py", False),
        ])
    ]),
    "telegram-doc": ([(f"{BASE_G}/telegram-doc/SKILL.md", True)], [
        ("references", [
            ("doc-map.md", f"{BASE_G}/telegram-doc/references/doc-map.md", True),
        ])
    ]),
    "word-docx": ([(f"{BASE_G}/word-docx/SKILL.md", True)], []),
    "youtube-api-skill": ([(f"{BASE_G}/youtube-api-skill/SKILL.md", True)], []),
}

def build_skill_data(name, files_list, subdirs_list, source):
    """Build a skill data dict."""
    main_files = []
    for fpath, is_md in files_list:
        fname = os.path.basename(fpath) if fpath else os.path.basename(fpath)
        data = rd(fpath)
        main_files.append({
            "name": fname,
            "is_md": is_md,
            "content": data["content"],
            "binary": data["binary"],
            "truncated": data["truncated"]
        })
    
    subdirs = []
    for subdir_name, subdir_files in subdirs_list:
        sd_files = []
        for fname, fpath, is_md in subdir_files:
            data = rd(fpath)
            sd_files.append({
                "name": fname,
                "is_md": is_md,
                "content": data["content"],
                "binary": data["binary"],
                "truncated": data["truncated"]
            })
        subdirs.append({"name": subdir_name, "files": sd_files})
    
    return {
        "name": name,
        "source": source,
        "files": main_files,
        "subdirs": subdirs
    }

all_skills = []
for name, (files, subdirs) in WORKSPACE_SKILLS.items():
    all_skills.append(build_skill_data(name, files, subdirs, "Workspace"))
for name, (files, subdirs) in GLOBAL_SKILLS.items():
    all_skills.append(build_skill_data(name, files, subdirs, "Global"))

skills_json = json.dumps(all_skills, ensure_ascii=False)

HTML_TEMPLATE = r'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ClawdIA — Skills Explorer</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  :root {
    --bg: #0a0a0f;
    --card: #13131a;
    --card-hover: #181820;
    --border: #25252e;
    --border-active: #3a3a4a;
    --text: #e4e4e7;
    --text-dim: #71717a;
    --text-bright: #fafafa;
    --accent: #6366f1;
    --accent-dim: #4f46e5;
    --ws-color: #10b981;
    --global-color: #f59e0b;
    --code-bg: #1e1e26;
    --radius: 10px;
  }
  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'Inter', system-ui, sans-serif;
    line-height: 1.6;
    min-height: 100vh;
  }
  .container { max-width: 1100px; margin: 0 auto; padding: 40px 20px 80px; }
  header { text-align: center; margin-bottom: 48px; }
  header h1 {
    font-size: 2.2rem; font-weight: 800;
    background: linear-gradient(135deg, #6366f1, #a855f7, #ec4899);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 8px;
  }
  header p { color: var(--text-dim); font-size: 1rem; }
  .stats {
    display: flex; justify-content: center; gap: 24px; margin-top: 20px; flex-wrap: wrap;
  }
  .stat {
    background: var(--card); border: 1px solid var(--border);
    border-radius: var(--radius); padding: 12px 24px; text-align: center;
  }
  .stat-num { font-size: 1.5rem; font-weight: 700; color: var(--text-bright); }
  .stat-label { font-size: 0.8rem; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.5px; }
  
  .section-title {
    font-size: 1.3rem; font-weight: 700; color: var(--text-bright);
    margin: 40px 0 16px; padding-bottom: 8px;
    border-bottom: 2px solid var(--border);
    display: flex; align-items: center; gap: 10px;
  }
  .section-title .count {
    font-size: 0.85rem; color: var(--text-dim); font-weight: 400;
    background: var(--card); padding: 2px 10px; border-radius: 20px;
  }

  .skill-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    margin-bottom: 8px;
    overflow: hidden;
    transition: border-color 0.2s;
  }
  .skill-card:hover { border-color: var(--border-active); }
  .skill-card.open { border-color: var(--accent-dim); }

  .skill-header {
    padding: 16px 20px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: space-between;
    user-select: none;
    transition: background 0.15s;
  }
  .skill-header:hover { background: var(--card-hover); }
  .skill-header-left { display: flex; align-items: center; gap: 12px; }
  .skill-name {
    font-weight: 600; font-size: 1rem; color: var(--text-bright);
    font-family: 'JetBrains Mono', monospace;
  }
  .badge {
    font-size: 0.7rem; font-weight: 600; padding: 3px 10px;
    border-radius: 20px; text-transform: uppercase; letter-spacing: 0.5px;
  }
  .badge-workspace { background: rgba(16,185,129,0.15); color: #34d399; border: 1px solid rgba(16,185,129,0.3); }
  .badge-global { background: rgba(245,158,11,0.15); color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); }
  
  .chevron {
    width: 20px; height: 20px;
    transition: transform 0.3s ease;
    color: var(--text-dim);
  }
  .skill-card.open .chevron { transform: rotate(90deg); }

  .skill-body {
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.4s ease;
  }
  .skill-card.open .skill-body { max-height: none; }
  .skill-content { padding: 0 20px 20px; }

  .file-block {
    background: var(--code-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    margin-top: 12px;
    overflow: hidden;
  }
  .file-header {
    padding: 10px 16px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    color: var(--text-dim);
    border-bottom: 1px solid var(--border);
    display: flex; align-items: center; gap: 8px;
  }
  .file-icon { font-size: 0.9rem; }
  .file-content { padding: 16px; overflow-x: auto; }
  .file-content.markdown-body { color: var(--text); }
  .file-content pre {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    white-space: pre-wrap;
    word-break: break-word;
    color: var(--text);
    line-height: 1.5;
  }

  /* Markdown rendered content */
  .markdown-body h1, .markdown-body h2, .markdown-body h3,
  .markdown-body h4, .markdown-body h5, .markdown-body h6 {
    color: var(--text-bright);
    margin-top: 20px; margin-bottom: 8px;
  }
  .markdown-body h1 { font-size: 1.5rem; }
  .markdown-body h2 { font-size: 1.25rem; border-bottom: 1px solid var(--border); padding-bottom: 6px; }
  .markdown-body h3 { font-size: 1.1rem; }
  .markdown-body p { margin: 8px 0; }
  .markdown-body ul, .markdown-body ol { margin: 8px 0; padding-left: 24px; }
  .markdown-body li { margin: 4px 0; }
  .markdown-body code {
    background: var(--code-bg);
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85em;
    border: 1px solid var(--border);
  }
  .markdown-body pre {
    background: var(--bg) !important;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 14px;
    overflow-x: auto;
    margin: 12px 0;
  }
  .markdown-body pre code {
    background: none; border: none; padding: 0;
    font-size: 0.82rem; line-height: 1.5;
  }
  .markdown-body table {
    border-collapse: collapse;
    width: 100%;
    margin: 12px 0;
  }
  .markdown-body th, .markdown-body td {
    border: 1px solid var(--border);
    padding: 8px 12px;
    text-align: left;
  }
  .markdown-body th { background: var(--card); color: var(--text-bright); }
  .markdown-body blockquote {
    border-left: 3px solid var(--accent);
    padding-left: 16px;
    margin: 12px 0;
    color: var(--text-dim);
  }
  .markdown-body a { color: var(--accent); text-decoration: none; }
  .markdown-body a:hover { text-decoration: underline; }
  .markdown-body hr { border: none; border-top: 1px solid var(--border); margin: 20px 0; }
  .markdown-body strong { color: var(--text-bright); }

  .subdir-card {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    margin-top: 12px;
    overflow: hidden;
  }
  .subdir-header {
    padding: 10px 16px;
    cursor: pointer;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    color: var(--text-dim);
    display: flex; align-items: center; gap: 8px;
    user-select: none;
    transition: background 0.15s;
  }
  .subdir-header:hover { background: var(--card-hover); }
  .subdir-header .folder-icon { color: var(--accent); }
  .subdir-header .count-badge {
    margin-left: auto;
    font-size: 0.75rem;
    background: var(--card);
    padding: 2px 8px;
    border-radius: 12px;
  }
  .subdir-body {
    max-height: 0; overflow: hidden;
    transition: max-height 0.3s ease;
  }
  .subdir-card.open .subdir-body { max-height: none; }
  .subdir-content { padding: 0 16px 16px; }

  .search-bar {
    width: 100%;
    padding: 12px 18px;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    color: var(--text);
    font-size: 0.95rem;
    font-family: 'Inter', sans-serif;
    margin-bottom: 24px;
    transition: border-color 0.2s;
  }
  .search-bar:focus {
    outline: none;
    border-color: var(--accent);
  }
  .search-bar::placeholder { color: var(--text-dim); }

  footer {
    text-align: center;
    margin-top: 60px;
    color: var(--text-dim);
    font-size: 0.85rem;
  }
</style>
</head>
<body>
<div class="container">
  <header>
    <h1>🧠 ClawdIA Skills Explorer</h1>
    <p>Tous les skills de l'agent ClawdIA — cliquez pour explorer</p>
    <div class="stats">
      <div class="stat">
        <div class="stat-num" id="total-skills">0</div>
        <div class="stat-label">Skills</div>
      </div>
      <div class="stat">
        <div class="stat-num" id="total-files">0</div>
        <div class="stat-label">Fichiers</div>
      </div>
      <div class="stat">
        <div class="stat-num" id="ws-count">0</div>
        <div class="stat-label">Workspace</div>
      </div>
      <div class="stat">
        <div class="stat-num" id="g-count">0</div>
        <div class="stat-label">Globaux</div>
      </div>
    </div>
  </header>

  <input type="text" class="search-bar" id="search" placeholder="🔍 Filtrer les skills par nom..." oninput="filterSkills()">

  <div id="workspace-section">
    <div class="section-title">
      📂 Skills Workspace
      <span class="count" id="ws-count-label"></span>
    </div>
    <div id="workspace-skills"></div>
  </div>

  <div id="global-section">
    <div class="section-title">
      🌍 Skills Globaux
      <span class="count" id="g-count-label"></span>
    </div>
    <div id="global-skills"></div>
  </div>

  <footer>
    Généré le 2026-06-27 — ClawdIA Skills Explorer
  </footer>
</div>

<script>
const ALL_SKILLS = __SKILLS_JSON__;

const chevronSVG = '<svg class="chevron" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>';

function getFileIcon(name) {
  if (name.endsWith('.md')) return '📄';
  if (name.endsWith('.py')) return '🐍';
  if (name.endsWith('.sh')) return '⚙️';
  if (name.endsWith('.json')) return '📋';
  if (name.endsWith('.yaml') || name.endsWith('.yml')) return '⚙️';
  if (name.endsWith('.txt')) return '📝';
  if (name.endsWith('.html')) return '🌐';
  if (name.endsWith('.png') || name.endsWith('.jpg') || name.endsWith('.jpeg')) return '🖼️';
  return '📄';
}

function renderFile(file) {
  const icon = getFileIcon(file.name);
  let inner;
  if (file.binary) {
    inner = '<pre><code>' + escapeHtml(file.content) + '</code></pre>';
  } else if (file.is_md) {
    inner = '<div class="markdown-body">' + marked.parse(file.content) + '</div>';
  } else {
    inner = '<pre><code>' + escapeHtml(file.content) + '</code></pre>';
  }
  const truncNote = file.truncated ? ' <span style="color:#f59e0b;">⚠️ tronqué</span>' : '';
  return `<div class="file-block">
    <div class="file-header"><span class="file-icon">${icon}</span> ${escapeHtml(file.name)}${truncNote}</div>
    <div class="file-content">${inner}</div>
  </div>`;
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

function renderSubdir(subdir) {
  const fileCount = subdir.files.length;
  let filesHtml = subdir.files.map(renderFile).join('');
  return `<div class="subdir-card" onclick="event.stopPropagation()">
    <div class="subdir-header" onclick="this.parentElement.classList.toggle('open')">
      <span class="folder-icon">📁</span>
      <span>${escapeHtml(subdir.name)}/</span>
      <span class="count-badge">${fileCount} fichier${fileCount > 1 ? 's' : ''}</span>
      ${chevronSVG}
    </div>
    <div class="subdir-body">
      <div class="subdir-content">${filesHtml}</div>
    </div>
  </div>`;
}

function renderSkill(skill) {
  const badgeClass = skill.source === 'Workspace' ? 'badge-workspace' : 'badge-global';
  const badgeText = skill.source;
  
  let bodyContent = '';
  
  // Main files
  for (const f of skill.files) {
    bodyContent += renderFile(f);
  }
  
  // Subdirs
  for (const sd of skill.subdirs) {
    bodyContent += renderSubdir(sd);
  }
  
  return `<div class="skill-card" data-name="${escapeHtml(skill.name.toLowerCase())}">
    <div class="skill-header" onclick="this.parentElement.classList.toggle('open')">
      <div class="skill-header-left">
        <span class="skill-name">${escapeHtml(skill.name)}</span>
        <span class="badge ${badgeClass}">${badgeText}</span>
      </div>
      ${chevronSVG}
    </div>
    <div class="skill-body">
      <div class="skill-content">${bodyContent}</div>
    </div>
  </div>`;
}

function render() {
  const wsContainer = document.getElementById('workspace-skills');
  const gContainer = document.getElementById('global-skills');
  
  const wsSkills = ALL_SKILLS.filter(s => s.source === 'Workspace');
  const gSkills = ALL_SKILLS.filter(s => s.source === 'Global');
  
  wsContainer.innerHTML = wsSkills.map(renderSkill).join('');
  gContainer.innerHTML = gSkills.map(renderSkill).join('');
  
  // Stats
  document.getElementById('total-skills').textContent = ALL_SKILLS.length;
  document.getElementById('ws-count').textContent = wsSkills.length;
  document.getElementById('g-count').textContent = gSkills.length;
  
  let totalFiles = 0;
  for (const s of ALL_SKILLS) {
    totalFiles += s.files.length;
    for (const sd of s.subdirs) totalFiles += sd.files.length;
  }
  document.getElementById('total-files').textContent = totalFiles;
  
  document.getElementById('ws-count-label').textContent = wsSkills.length + ' skills';
  document.getElementById('g-count-label').textContent = gSkills.length + ' skills';
}

function filterSkills() {
  const q = document.getElementById('search').value.toLowerCase();
  const cards = document.querySelectorAll('.skill-card');
  cards.forEach(card => {
    const name = card.getAttribute('data-name') || '';
    card.style.display = (!q || name.includes(q)) ? '' : 'none';
  });
}

// Configure marked
marked.setOptions({
  breaks: true,
  gfm: true
});

render();
</script>
</body>
</html>'''

final_html = HTML_TEMPLATE.replace("__SKILLS_JSON__", skills_json)

outpath = "/tmp/clawdia-skills/index.html"
with open(outpath, "w", encoding="utf-8") as f:
    f.write(final_html)

print(f"✅ HTML généré: {outpath}")
print(f"   Taille: {os.path.getsize(outpath):,} octets")
print(f"   Skills: {len(all_skills)}")
total_files = sum(len(s["files"]) + sum(len(sd["files"]) for sd in s["subdirs"]) for s in all_skills)
print(f"   Fichiers: {total_files}")
