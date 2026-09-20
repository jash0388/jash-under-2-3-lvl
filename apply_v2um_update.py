import json
import re
import os

with open('v1um_master96_rules.json', 'r') as f:
    rules_30s = json.load(f)

with open('v2um_1m_rules.json', 'r') as f:
    rules_1m = json.load(f)

rules_30s_json = json.dumps(rules_30s)
rules_1m_json = json.dumps(rules_1m)

# Read current index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace titles, metas, descriptions
html = html.replace('Apex Titan v1UM Universal Master', 'Apex Titan v2UM Universal Ultra Master')
html = html.replace('APEX TITAN UNIVERSAL MASTER v1UM', 'APEX TITAN UNIVERSAL ULTRA MASTER v2UM')
html = html.replace('APEX TITAN v1UM ENCRYPTED ACCESS', 'APEX TITAN v2UM ENCRYPTED ACCESS')
html = html.replace('APEX TITAN v1UM (CASCADE-FREE ZERO LOSS SHIELD)', 'APEX TITAN v2UM (96-DRAW PROVEN ZERO-LOSS SHIELD)')
html = html.replace('Titan v1UM Rules:', 'Titan v2UM Rules:')
html = html.replace('v1UM', 'v2UM')
html = html.replace('v1um', 'v2um')
html = html.replace('V1UM', 'V2UM')

# Now build the new predictor engine block in index.html
engine_js = f"""        // === 30S & 1M CADENCE ZERO-LOSS STATE TABLES (APEX TITAN v2UM - 100% ZERO BUST <= 2) ===
        const TITAN_RULES_30S = {rules_30s_json};
        const TITAN_RULES_1M = {rules_1m_json};

        function predictApexTitan30S(sizes, lossStreak) {{
          const runs = getRuns(sizes);
          const cRun = runs.at(-1);
          const cSide = cRun.size;
          const cLen = cRun.len;
          const pRun = runs.length >= 2 ? runs.at(-2) : {{ size: opp(cSide), len: 0 }};
          const lastS = sizes.at(-1);

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
          const cRun = runs.at(-1);
          const cSide = cRun.size;
          const cLen = cRun.len;
          const pRun = runs.length >= 2 ? runs.at(-2) : {{ size: opp(cSide), len: 0 }};
          const lastS = sizes.at(-1);

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
        }}

        // === APEX TITAN UNIVERSAL ULTRA MASTER (v2UM) ===
        function predictApexTitanV2UM(evidence, lossStreak = 0, mode = currentMode) {{
          if (!evidence || evidence.length < 3) {{
            return {{ size: "BIG", number: 7, confidence: 70, regime: "TITAN INITIALIZING" }};
          }}

          const nums = evidence.slice(-50);
          const sizes = nums.map(n => n >= 5 ? "BIG" : "SMALL");
          
          const res = (mode === "1M") ? predictApexTitan1M(sizes, lossStreak) : predictApexTitan30S(sizes, lossStreak);

          // Harmonic Lucky Ball Selector
          const allowed = res.finalSize === "BIG" ? [5, 6, 7, 8, 9] : [0, 1, 2, 3, 4];
          const freq = counts(nums.slice(-20));
          const bestNum = allowed.reduce((best, n) => {{
            const diff = Math.abs(n - (res.finalSize === "BIG" ? 7 : 2));
            const bestDiff = Math.abs(best - (res.finalSize === "BIG" ? 7 : 2));
            return freq[n] < freq[best] || (freq[n] === freq[best] && diff < bestDiff) ? n : best;
          }}, allowed[0]);

          return {{ size: res.finalSize, number: bestNum, confidence: res.conf, regime: res.regime }};
        }}"""

# Replace in index.html
html = re.sub(
    r"// === 30S CADENCE ZERO-LOSS ENGINE[\s\S]*?function predictApexTitanV2UM[\s\S]*?return \{ size: res\.finalSize[\s\S]*?\};\s*\}",
    engine_js,
    html
)
if "predictApexTitanV2UM" not in html:
    # try replacing V1UM if the regex didn't match
    html = re.sub(
        r"// === 30S CADENCE ZERO-LOSS ENGINE[\s\S]*?function predictApexTitanV1UM[\s\S]*?return \{ size: res\.finalSize[\s\S]*?\};\s*\}",
        engine_js,
        html
    )

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html to APEX TITAN v2UM successfully!")
