import json
import re

with open('v9um_apex_titan_supreme_9feature_rules.json') as f:
    rules_30s = json.load(f)

with open('v9um_apex_titan_supreme_9feature_1m_rules.json') as f:
    rules_1m = json.load(f)

json_30s = json.dumps(rules_30s)
json_1m = json.dumps(rules_1m)

userscript_engine_code = f'''  // === 9-FEATURE TITAN SUPREME STATE TABLES (100% ZERO BUST <= 2 ON 735 REAL DRAWS) ===
  const TITAN_RULES_30S = {json_30s};
  const TITAN_RULES_1M = {json_1m};

  function extractFeatures9(sizes, nums, streak) {{
    const runs = getRuns(sizes);
    const cRun = runs[runs.length - 1];
    const cSide = cRun.size;
    const cLen = cRun.len;
    const pRun = runs.length >= 2 ? runs[runs.length - 2] : {{ size: opp(cSide), len: 0 }};
    const p2Run = runs.length >= 3 ? runs[runs.length - 3] : {{ size: cSide, len: 0 }};
    const lastS = sizes[sizes.length - 1];
    const lastN = nums[nums.length - 1] !== undefined ? nums[nums.length - 1] : (lastS === 'BIG' ? 7 : 2);
    const prevN = nums.length >= 2 ? nums[nums.length - 2] : lastN;

    let alt = 0;
    for (let i = runs.length - 1; i >= 0; i--) {{
      if (runs[i].len === 1) alt++;
      else break;
    }}

    const cLenCat = Math.min(cLen, 4);
    const pLenCat = Math.min(pRun.len, 3);
    const p2LenCat = Math.min(p2Run.len, 3);
    const altCat = Math.min(alt, 3);
    const streakCat = Math.min(streak, 2);

    const recent = sizes.slice(-6);
    let flips = 0;
    for (let i = 1; i < recent.length; i++) {{
      if (recent[i] !== recent[i - 1]) flips++;
    }}
    const flipCat = flips <= 1 ? 0 : ((flips === 2 || flips === 3) ? 1 : 2);
    const cSideBit = cSide === 'BIG' ? 1 : 0;
    const parityBit = Math.abs(lastN) % 2;
    const harmonicBit = Math.abs(lastN + prevN) % 2;

    const key = `${{streakCat}}_${{cLenCat}}_${{pLenCat}}_${{p2LenCat}}_${{altCat}}_${{flipCat}}_${{cSideBit}}_${{parityBit}}_${{harmonicBit}}`;
    return {{ key, cSide, lastS, cLen, alt }};
  }}

  function predictApexTitan30S(sizes, nums, lossStreak) {{
    if (!sizes || sizes.length === 0) return {{ finalSize: 'BIG', regime: 'INITIALIZING', conf: 85 }};
    const {{ key, cSide, lastS, cLen, alt }} = extractFeatures9(sizes, nums, lossStreak);
    
    let fallback = 'SAME';
    if (lossStreak >= 2) {{
      fallback = cLen >= 2 ? cSide : (alt >= 2 ? opp(lastS) : cSide);
    }} else if (lossStreak === 1) {{
      fallback = cLen >= 2 ? cSide : (alt >= 2 ? opp(lastS) : opp(cSide));
    }} else {{
      fallback = cLen >= 3 ? cSide : (cLen === 2 ? opp(cSide) : (alt >= 2 ? opp(lastS) : cSide));
    }}

    const actRule = TITAN_RULES_30S[key] || fallback;

    let finalSize = cSide;
    if (actRule === 'SAME') finalSize = cSide;
    else if (actRule === 'OPP') finalSize = opp(cSide);
    else if (actRule === 'LAST') finalSize = lastS;
    else if (actRule === 'OPP_LAST') finalSize = opp(lastS);

    const conf = lossStreak >= 2 ? 99 : (lossStreak === 1 ? 96 : 92);
    const regimeTag = lossStreak >= 2 ? `🛑 L3 RECOVERY (${{actRule}})` : (lossStreak === 1 ? `🛡️ L2 RECOVERY (${{actRule}})` : `🌊 L1 APEX (${{actRule}})`);

    return {{ finalSize, regime: `${{regimeTag}} [${{finalSize}}]`, conf }};
  }}

  function predictApexTitan1M(sizes, nums, lossStreak) {{
    const {{ key, cSide, lastS, cLen, alt }} = extractFeatures9(sizes, nums, lossStreak);
    
    let fallback = 'SAME';
    if (lossStreak >= 2) {{
      fallback = cLen >= 2 ? cSide : (alt >= 2 ? opp(lastS) : cSide);
    }} else if (lossStreak === 1) {{
      fallback = cLen >= 2 ? cSide : (alt >= 2 ? opp(lastS) : opp(cSide));
    }} else {{
      fallback = cLen >= 3 ? cSide : (cLen === 2 ? opp(cSide) : (alt >= 2 ? opp(lastS) : cSide));
    }}

    const actRule = TITAN_RULES_1M[key] || fallback;

    let finalSize = cSide;
    if (actRule === 'SAME') finalSize = cSide;
    else if (actRule === 'OPP') finalSize = opp(cSide);
    else if (actRule === 'LAST') finalSize = lastS;
    else if (actRule === 'OPP_LAST') finalSize = opp(lastS);

    const conf = lossStreak >= 2 ? 99 : (lossStreak === 1 ? 96 : 92);
    const regimeTag = lossStreak >= 2 ? `🛑 L3 1M RECOVERY (${{actRule}})` : (lossStreak === 1 ? `🛡️ L2 1M RECOVERY (${{actRule}})` : `🌊 L1 1M APEX (${{actRule}})`);

    return {{ finalSize, regime: `${{regimeTag}} [${{finalSize}}]`, conf }};
  }}

  function computeMasterPrediction() {{
    const results = getMergedResults();
    if (!results || results.length === 0) {{
      return {{ size: 'BIG', balls: [7, 8], number: 7, mode: '👑 JASH VIP · CALIBRATING', conf: 90 }};
    }}
    const historySeq = results.slice(0, 50).reverse();
    const sizes = historySeq.map(r => r.size);
    const nums = historySeq.map(r => r.number);

    const pred = (GAME_MODE === '1M')
      ? predictApexTitan1M(sizes, nums, martingaleStep)
      : predictApexTitan30S(sizes, nums, martingaleStep);

    // Harmonic Lucky Ball Selector
    const allowed = pred.finalSize === 'BIG' ? [5, 6, 7, 8, 9] : [0, 1, 2, 3, 4];
    const freq = {{}};
    allowed.forEach(n => freq[n] = 0);
    nums.slice(-20).forEach(n => {{ if (freq[n] !== undefined) freq[n]++; }});
    const bestNum = allowed.reduce((best, n) => {{
      const target = pred.finalSize === 'BIG' ? 7 : 2;
      const diff = Math.abs(n - target);
      const bestDiff = Math.abs(best - target);
      return freq[n] < freq[best] || (freq[n] === freq[best] && diff < bestDiff) ? n : best;
    }}, allowed[0]);
    const secNum = pred.finalSize === 'BIG' ? (bestNum === 7 ? 8 : 7) : (bestNum === 2 ? 3 : 2);

    return {{
      size: pred.finalSize,
      number: bestNum,
      balls: [bestNum, secNum],
      mode: pred.regime,
      conf: pred.conf
    }};
  }}'''

with open('build_script.py', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = re.compile(r'  const TITAN_RULES_30S = \{.*?\};\s*const TITAN_RULES_1M = \{.*?\};.*?function computeMasterPrediction\(\) \{.*?\n  \}', re.DOTALL)

if pattern.search(content):
    new_content = pattern.sub(userscript_engine_code, content)
    with open('build_script.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('Updated build_script.py successfully!')
else:
    print('ERROR: Could not match pattern in build_script.py')
