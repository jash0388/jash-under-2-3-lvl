import re
import os
import json

# 1. Read old_pred_page.html to get the exact original web code and rules
with open('old_pred_page.html', 'r', encoding='utf-8') as f:
    pred_code = f.read()

# Extract TITAN_RULES_30S and TITAN_RULES_1M JSON
r30_m = re.search(r'const TITAN_RULES_30S = (\{.*?\});', pred_code)
r1m_m = re.search(r'const TITAN_RULES_1M = (\{.*?\});', pred_code)

titan_rules_30s_str = r30_m.group(1)
titan_rules_1m_str = r1m_m.group(1)

# Ensure pred.html has the topbar link to /
topbar_replacement = """            <!-- HEADER -->
            <div class="topbar">
              <div class="brand-lockup">
                <div class="brand-mark">ϟ</div>
                <div>
                  <div class="brand-name">JASH VIP</div>
                  <div class="brand-sub">APEX TITAN ULTIMATE ZERO-BUST MASTER v9UM</div>
                </div>
              </div>
              <div style="display:flex;align-items:center;gap:6px">
                <a href="/" class="filter-button" style="padding:6px 10px;border-radius:8px;font-size:9px;text-decoration:none;display:inline-flex;align-items:center;gap:4px;color:#e8e6db;border:1px solid rgba(255,255,255,0.18);background:rgba(255,255,255,0.06);font-weight:700;">
                  📊 BOT STATS
                </a>
                <button class="filter-button is-active" data-action="sync" style="padding:6px 10px;border-radius:8px;font-size:9px">
                  <span class="live-dot"></span>${state.synced ? "LIVE" : state.loading ? "SYNCING…" : "RETRY"}
                </button>
                <button class="lock-out-btn" data-action="lock-vault" title="Lock Terminal">🔒 LOCK</button>
              </div>
            </div>"""

if '📊 BOT STATS' not in pred_code:
    pred_code = re.sub(r'<!-- HEADER -->[\s\S]*?</div>\s*</div>', topbar_replacement, pred_code, count=1)

# Write pred.html to all destinations
for p in ['pred.html', 'public/pred.html', 'public/pred/index.html', 'pred/index.html']:
    d = os.path.dirname(p)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(pred_code)
    print(f"Updated: {p}")

# 2. Update build_script.py to use the EXACT web strategy
with open('build_script.py', 'r', encoding='utf-8') as f:
    builder_code = f.read()

bot_engine_block = f"""  // ── 5. 👑 NEURAL MASTER · APEX TITAN v9UM STRATEGY ENGINE (100% WEB STRATEGY) ───
  const opp = s => (s === 'BIG' ? 'SMALL' : 'BIG');

  function getRuns(sizes) {{
    if (!sizes || !sizes.length) return [];
    const runs = [];
    let curr = sizes[0], l = 1;
    for (let i = 1; i < sizes.length; i++) {{
      if (sizes[i] === curr) l++;
      else {{ runs.push({{ size: curr, len: l }}); curr = sizes[i]; l = 1; }}
    }}
    runs.push({{ size: curr, len: l }});
    return runs;
  }}

  const TITAN_RULES_30S = {titan_rules_30s_str};
  const TITAN_RULES_1M = {titan_rules_1m_str};

  function predictApexTitan30S(sizes, lossStreak) {{
    if (!sizes || sizes.length === 0) return {{ finalSize: 'BIG', regime: 'INITIALIZING', conf: 85 }};
    const runs = getRuns(sizes);
    const cRun = runs[runs.length - 1];
    const cSide = cRun.size;
    const cLen = cRun.len;
    const pRun = runs.length >= 2 ? runs[runs.length - 2] : {{ size: opp(cSide), len: 0 }};
    const lastS = sizes[sizes.length - 1];

    let alt = 0;
    for (let i = runs.length - 1; i >= 0; i--) {{
      if (runs[i].len === 1) alt++;
      else break;
    }}

    const cLenCat = Math.min(cLen, 4);
    const pLenCat = Math.min(pRun.len, 3);
    const altCat = Math.min(alt, 3);
    const streakCat = Math.min(lossStreak, 2);

    const recent = sizes.slice(-6);
    let flips = 0;
    for (let i = 1; i < recent.length; i++) {{
      if (recent[i] !== recent[i - 1]) flips++;
    }}
    const flipCat = flips <= 1 ? 0 : ((flips === 2 || flips === 3) ? 1 : 2);

    const key = `${{streakCat}}_${{cLenCat}}_${{pLenCat}}_${{altCat}}_${{flipCat}}`;
    const actRule = TITAN_RULES_30S[key] || "SAME";

    let finalSize = cSide;
    if (actRule === "SAME") finalSize = cSide;
    else if (actRule === "OPP") finalSize = opp(cSide);
    else if (actRule === "LAST") finalSize = lastS;
    else if (actRule === "OPP_LAST") finalSize = opp(lastS);

    const conf = lossStreak >= 2 ? 99 : (lossStreak === 1 ? 96 : 92);
    const regimeTag = lossStreak >= 2 ? `🛑 L3 RECOVERY (${{actRule}})` : (lossStreak === 1 ? `🛡️ L2 RECOVERY (${{actRule}})` : `🌊 L1 APEX (${{actRule}})`);

    return {{ finalSize, regime: `${{regimeTag}} [${{finalSize}}]`, conf }};
  }}

  function predictApexTitan1M(sizes, lossStreak) {{
    const runs = getRuns(sizes);
    const cRun = runs[runs.length - 1];
    const cSide = cRun.size;
    const cLen = cRun.len;
    const pRun = runs.length >= 2 ? runs[runs.length - 2] : {{ size: opp(cSide), len: 0 }};
    const lastS = sizes[sizes.length - 1];

    let alt = 0;
    for (let i = runs.length - 1; i >= 0; i--) {{
      if (runs[i].len === 1) alt++;
      else break;
    }}

    const cLenCat = Math.min(cLen, 4);
    const pLenCat = Math.min(pRun.len, 3);
    const altCat = Math.min(alt, 3);
    const streakCat = Math.min(lossStreak, 2);

    const recent = sizes.slice(-6);
    let flips = 0;
    for (let i = 1; i < recent.length; i++) {{
      if (recent[i] !== recent[i - 1]) flips++;
    }}
    const flipCat = flips <= 1 ? 0 : ((flips === 2 || flips === 3) ? 1 : 2);

    const key = `${{streakCat}}_${{cLenCat}}_${{pLenCat}}_${{altCat}}_${{flipCat}}`;
    const actRule = TITAN_RULES_1M[key] || "SAME";

    let finalSize = cSide;
    if (actRule === "SAME") finalSize = cSide;
    else if (actRule === "OPP") finalSize = opp(cSide);
    else if (actRule === "LAST") finalSize = lastS;
    else if (actRule === "OPP_LAST") finalSize = opp(lastS);

    const conf = lossStreak >= 2 ? 99 : (lossStreak === 1 ? 96 : 92);
    const regimeTag = lossStreak >= 2 ? `🛑 L3 1M RECOVERY (${{actRule}})` : (lossStreak === 1 ? `🛡️ L2 1M RECOVERY (${{actRule}})` : `🌊 L1 1M APEX (${{actRule}})`);

    return {{ finalSize, regime: `${{regimeTag}} [${{finalSize}}]`, conf }};
  }}"""

# Replace engine in build_script.py
engine_pattern = r"// ── 5\. 👑 NEURAL MASTER · APEX TITAN v9UM STRATEGY ENGINE[\s\S]*?function predictApexTitan1M\(sizes, lossStreak\) \{[\s\S]*?\}"
builder_code = re.sub(engine_pattern, bot_engine_block, builder_code)

with open('build_script.py', 'w', encoding='utf-8') as f:
    f.write(builder_code)

print("Updated build_script.py with exact web strategy!")
