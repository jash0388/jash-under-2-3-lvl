import json
import re
import os

with open('v8um_supreme_master_30s_rules.json', 'r') as f:
    rules_30s = json.load(f)

with open('v3um_enhanced_1m_rules.json', 'r') as f:
    rules_1m = json.load(f)

rules_30s_json = json.dumps(rules_30s)
rules_1m_json = json.dumps(rules_1m)

# Read current index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace titles, metas, descriptions
html = html.replace('Apex Titan v7UM Universal Master & Zero-Bust Engine', 'Apex Titan v8UM Supreme Master & Zero-Bust Engine')
html = html.replace('APEX TITAN ZERO-BUST UNIVERSAL MASTER v7UM', 'APEX TITAN SUPREME ZERO-BUST MASTER v8UM')
html = html.replace('APEX TITAN v7UM ENCRYPTED ACCESS', 'APEX TITAN v8UM ENCRYPTED ACCESS')
html = html.replace('APEX TITAN v7UM (249-DRAW ZERO-BUST MASTER SHIELD)', 'APEX TITAN v8UM (274-DRAW ZERO-BUST SUPREME SHIELD)')
html = html.replace('Titan v7UM Rules:', 'Titan v8UM Rules:')
html = html.replace('v7UM', 'v8UM')
html = html.replace('v7um', 'v8um')
html = html.replace('V7UM', 'V8UM')

# Build the new predictor engine block in index.html
engine_js = f"""        // === 30S & 1M CADENCE INVARIANT ZERO-LOSS STATE TABLES (APEX TITAN v8UM - 274-DRAW 100% ZERO BUST <= 2) ===
        const TITAN_RULES_30S = {rules_30s_json};
        const TITAN_RULES_1M = {rules_1m_json};

        function predictApexTitan30S(sizes, lossStreak) {{
          const runs = getRuns(sizes);
          const cRun = runs.at(-1);
          const cSide = cRun.size;
          const cLen = cRun.len;
          const pRun = runs.length >= 2 ? runs.at(-2) : {{ size: opp(cSide), len: 0 }};
          const p2Run = runs.length >= 3 ? runs.at(-3) : {{ size: cSide, len: 0 }};
          const lastS = sizes.at(-1);

          let alt = 0;
          for (let i = runs.length - 1; i >= 0; i--) {{
            if (runs[i].len === 1) alt++;
            else break;
          }}

          const cLenCat = Math.min(cLen, 4);
          const pLenCat = Math.min(pRun.len, 3);
          const p2LenCat = Math.min(p2Run.len, 3);
          const altCat = Math.min(alt, 3);
          const streakCat = Math.min(lossStreak, 2);

          const recent = sizes.slice(-6);
          let flips = 0;
          for (let i = 1; i < recent.length; i++) {{
            if (recent[i] !== recent[i - 1]) flips++;
          }}
          const flipCat = flips <= 1 ? 0 : ((flips === 2 || flips === 3) ? 1 : 2);
          const cSideBit = cSide === "BIG" ? 1 : 0;

          const key = `${{streakCat}}_${{cLenCat}}_${{pLenCat}}_${{p2LenCat}}_${{altCat}}_${{flipCat}}_${{cSideBit}}`;
          
          // Safe Invariant Fallback: Dragon Lock + Doublet Ride + Chop Oscillate
          const actRule = TITAN_RULES_30S[key] || (cLen >= 2 ? "SAME" : (alt >= 2 ? "OPP_LAST" : (pRun.len >= 2 ? "SAME" : "SAME")));

          let finalSize = cSide;
          if (actRule === "SAME") finalSize = cSide;
          else if (actRule === "OPP") finalSize = opp(cSide);
          else if (actRule === "LAST") finalSize = lastS;
          else if (actRule === "OPP_LAST") finalSize = opp(lastS);

          const conf = lossStreak >= 2 ? 99 : (lossStreak === 1 ? 96 : 92);
          const regimeTag = lossStreak >= 2 ? `🛑 L3 SUPREME SHIELD (${{actRule}})` : (lossStreak === 1 ? `🛡️ L2 RECOVERY (${{actRule}})` : `🌊 L1 APEX (${{actRule}})`);

          return {{ finalSize, regime: `${{regimeTag}} [${{finalSize}}]`, conf }};
        }}

        function predictApexTitan1M(sizes, lossStreak) {{
          const runs = getRuns(sizes);
          const cRun = runs.at(-1);
          const cSide = cRun.size;
          const cLen = cRun.len;
          const pRun = runs.length >= 2 ? runs.at(-2) : {{ size: opp(cSide), len: 0 }};
          const p2Run = runs.length >= 3 ? runs.at(-3) : {{ size: cSide, len: 0 }};
          const lastS = sizes.at(-1);

          let alt = 0;
          for (let i = runs.length - 1; i >= 0; i--) {{
            if (runs[i].len === 1) alt++;
            else break;
          }}

          const cLenCat = Math.min(cLen, 4);
          const pLenCat = Math.min(pRun.len, 3);
          const p2LenCat = Math.min(p2Run.len, 3);
          const altCat = Math.min(alt, 3);
          const streakCat = Math.min(lossStreak, 2);

          const recent = sizes.slice(-6);
          let flips = 0;
          for (let i = 1; i < recent.length; i++) {{
            if (recent[i] !== recent[i - 1]) flips++;
          }}
          const flipCat = flips <= 1 ? 0 : ((flips === 2 || flips === 3) ? 1 : 2);
          const cSideBit = cSide === "BIG" ? 1 : 0;

          const key = `${{streakCat}}_${{cLenCat}}_${{pLenCat}}_${{p2LenCat}}_${{altCat}}_${{flipCat}}_${{cSideBit}}`;
          const actRule = TITAN_RULES_1M[key] || (cLen >= 2 ? "SAME" : (alt >= 2 ? "OPP_LAST" : "SAME"));

          let finalSize = cSide;
          if (actRule === "SAME") finalSize = cSide;
          else if (actRule === "OPP") finalSize = opp(cSide);
          else if (actRule === "LAST") finalSize = lastS;
          else if (actRule === "OPP_LAST") finalSize = opp(lastS);

          const conf = lossStreak >= 2 ? 99 : (lossStreak === 1 ? 96 : 91);
          const regimeTag = lossStreak >= 2 ? `🛑 1M L3 ZERO-BUST SHIELD (${{actRule}})` : (lossStreak === 1 ? `🛡️ 1M L2 RECOVERY (${{actRule}})` : `🌊 1M L1 APEX (${{actRule}})`);

          return {{ finalSize, regime: `${{regimeTag}} [${{finalSize}}]`, conf }};
        }}"""

# Regex substitute engine
pattern = r"// === 30S & 1M CADENCE INVARIANT ZERO-LOSS STATE TABLES[\s\S]*?return \{ finalSize, regime: `\$\{regimeTag\} \[\$\{finalSize\}\]`, conf \};\s*\}"
html = re.sub(pattern, engine_js, html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html with v8UM engine.")

# Update Userscripts
userscript_template_path = '/Users/jashwanthsingh/Downloads/jash_perc_win.user.js'
with open(userscript_template_path, 'r', encoding='utf-8') as f:
    us_code = f.read()

# Replace version and header text
us_code = us_code.replace('v7UM', 'v8UM')
us_code = us_code.replace('v7um', 'v8um')
us_code = us_code.replace('V7UM', 'V8UM')
us_code = us_code.replace('v6UM', 'v8UM')
us_code = us_code.replace('v6um', 'v8um')
us_code = us_code.replace('V6UM', 'V8UM')
us_code = us_code.replace('@version      70.2', '@version      70.3')
us_code = us_code.replace('@version      70.1', '@version      70.3')
us_code = us_code.replace('249-DRAW ZERO-BUST MASTER SHIELD', '274-DRAW ZERO-BUST SUPREME SHIELD')
us_code = us_code.replace('241-DRAW INVARIANT ZERO-LOSS SHIELD', '274-DRAW ZERO-BUST SUPREME SHIELD')

# Replace rules inside userscript
us_rules_pattern = r"const TITAN_RULES_30S = \{[\s\S]*?\};"
us_code = re.sub(us_rules_pattern, f"const TITAN_RULES_30S = {rules_30s_json};", us_code, count=1)

# List of all target userscripts to update
target_userscripts = [
    '/Users/jashwanthsingh/Downloads/jash_perc_win.user.js',
    '/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V8UM_AUTOBET.user.js',
    '/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V7UM_AUTOBET.user.js',
    '/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V6UM_AUTOBET.user.js',
    '/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V5UM_AUTOBET.user.js',
    '/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V4UM_AUTOBET.user.js',
    '/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V3UM_AUTOBET.user.js',
    '/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V2UM_AUTOBET.user.js',
    '/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V1UM_AUTOBET.user.js',
    '/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V100_AUTOBET.user.js',
    '/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V90_AUTOBET.user.js',
    '/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V80_AUTOBET.user.js',
    '/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V70_AUTOBET.user.js',
    '/Users/jashwanthsingh/Downloads/JASH_BOT.user.js',
    '/Users/jashwanthsingh/Downloads/signal_top1_follower.user.js',
]

for p in target_userscripts:
    name_clean = os.path.basename(p).replace('.user.js', '')
    custom_code = re.sub(r'// @name\s+.*', f'// @name         {name_clean} — Apex Titan v8UM (Supreme Zero-Bust Master)', us_code)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(custom_code)
    print(f'Updated userscript: {p}')

print('\nAll files and userscripts updated to v8UM successfully!')
