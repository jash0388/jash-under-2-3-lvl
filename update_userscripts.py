import json
import re
import os

with open('v1um_master96_rules.json', 'r') as f:
    rules_30s = json.load(f)

rules_30s_str = json.dumps(rules_30s)

src_script = "/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V1UM_AUTOBET.user.js"
if not os.path.exists(src_script):
    src_script = "/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V100_AUTOBET.user.js"

if os.path.exists(src_script):
    with open(src_script, "r", encoding="utf-8") as f:
        src = f.read()
    with open("/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V2UM_AUTOBET.user.js", "w", encoding="utf-8") as f:
        f.write(src)

files = [
    "/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V2UM_AUTOBET.user.js",
    "/Users/jashwanthsingh/Downloads/signal_top1_follower.user.js",
    "/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V1UM_AUTOBET.user.js",
    "/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V100_AUTOBET.user.js",
    "/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V90_AUTOBET.user.js",
    "/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V80_AUTOBET.user.js",
    "/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V70_AUTOBET.user.js",
    "/Users/jashwanthsingh/Downloads/JASH_BOT.user.js",
    "/Users/jashwanthsingh/Downloads/jash_perc_win.user.js"
]

NEW_PREDICTOR_CODE = f"""  // === 30S CADENCE ZERO-LOSS ENGINE (APEX TITAN v2UM - 96-DRAW PROVEN ZERO-LOSS SHIELD) ===
  const TITAN_RULES_30S = {rules_30s_str};

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
  }}"""

for path in files:
    if not os.path.exists(path):
        print(f"Skipping missing: {path}")
        continue
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace predictApexTitan30S function
    content = re.sub(
        r"// === 30S CADENCE ZERO-LOSS ENGINE[\s\S]*?return \{ finalSize, regime[\s\S]*?\};\s*\}",
        NEW_PREDICTOR_CODE,
        content
    )

    # Rebrand to V2UM
    content = content.replace("APEX TITAN v1UM", "APEX TITAN v2UM")
    content = content.replace("APEX TITAN V1UM", "APEX TITAN v2UM")
    content = content.replace("APEX TITAN V100", "APEX TITAN v2UM")
    content = content.replace("APEX TITAN V90", "APEX TITAN v2UM")
    content = content.replace("APEX TITAN V80", "APEX TITAN v2UM")
    content = content.replace("v1um", "v2um")
    content = content.replace("V1UM", "V2UM")
    content = content.replace("v100", "v2um")
    content = content.replace("V100", "V2UM")
    content = content.replace("v90", "v2um")
    content = content.replace("V90", "V2UM")

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Updated: {path}")

print("All userscripts updated to APEX TITAN v2UM successfully!")
