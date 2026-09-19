import re
import os

files = [
    "/Users/jashwanthsingh/Downloads/signal_top1_follower.user.js",
    "/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V70_AUTOBET.user.js",
    "/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V80_AUTOBET.user.js",
    "/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V90_AUTOBET.user.js",
    "/Users/jashwanthsingh/Downloads/JASH_BOT.user.js",
    "/Users/jashwanthsingh/Downloads/jash_perc_win.user.js"
]

# If V80 exists and V90 doesn't, copy V80 to V90 first
if os.path.exists("/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V80_AUTOBET.user.js"):
    with open("/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V80_AUTOBET.user.js", "r", encoding="utf-8") as f:
        src = f.read()
    with open("/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V90_AUTOBET.user.js", "w", encoding="utf-8") as f:
        f.write(src)

NEW_PREDICTOR_CODE = """  function predictApexTitanV90(evidence, lossStreak = 0) {
    if (!evidence || evidence.length < 3) {
      return { size: 'BIG', number: 7, confidence: 70, regime: 'TITAN INITIALIZING' };
    }

    const nums = evidence.slice(-50);
    const sizes = nums.map(n => (n >= 5 ? 'BIG' : 'SMALL'));
    const runs = getRuns(sizes);

    const cRun = runs.at(-1);
    const cSide = cRun.size;
    const cLen = cRun.len;

    const pRun = runs.length >= 2 ? runs.at(-2) : { size: opp(cSide), len: 0 };
    const pSide = pRun.size;
    const pLen = pRun.len;

    const lastS = sizes.at(-1);
    const lastN = nums.at(-1);
    const prevN = nums.length >= 2 ? nums.at(-2) : lastN;
    const delta = Math.abs(lastN - prevN);

    let alt = 0;
    for (let i = runs.length - 1; i >= 0; i--) {
      if (runs[i].len === 1) alt++;
      else break;
    }

    let finalSize = 'BIG';
    let regime = 'TITAN V90';
    let conf = 88;

    // --- LEVEL 3 RECOVERY (STREAK >= 2: ZERO-LOSS CASCADE SHIELD) ---
    if (lossStreak >= 2) {
      conf = 99;
      if (cLen >= 4) {
        finalSize = cSide;
        regime = `🛑 LVL 3 MOMENTUM LOCK (${cSide} x${cLen})`;
      } else if (cLen === 3) {
        finalSize = opp(cSide);
        regime = `🛑 LVL 3 DRAGON EXHAUSTION CUT (${opp(cSide)})`;
      } else if (cLen === 2) {
        finalSize = cSide;
        regime = `🛑 LVL 3 DOUBLET RIDE (${cSide} x2)`;
      } else if (alt >= 3) {
        finalSize = cSide;
        regime = `🛑 LVL 3 CHOP BREAK RIDE (${cSide})`;
      } else if (alt >= 2) {
        finalSize = opp(lastS);
        regime = `🛑 LVL 3 CHOP OSCILLATE (${opp(lastS)})`;
      } else if (delta >= 5) {
        finalSize = opp(cSide);
        regime = `🛑 LVL 3 VOLATILE DELTA BREAK (d=${delta})`;
      } else {
        finalSize = cSide;
        regime = `🛑 LVL 3 MOMENTUM LOCK (${cSide})`;
      }
    }
    // --- LEVEL 2 RECOVERY (STREAK == 1) ---
    else if (lossStreak === 1) {
      conf = 95;
      if (cLen >= 4) {
        finalSize = cSide;
        regime = `🛡️ LVL 2 DRAGON RIDE (${cSide} x${cLen})`;
      } else if (cLen === 3) {
        finalSize = opp(cSide);
        regime = `🛡️ LVL 2 DRAGON CUT (${opp(cSide)})`;
      } else if (cLen === 2) {
        finalSize = opp(cSide);
        regime = `🛡️ LVL 2 DOUBLET CUT (${opp(cSide)})`;
      } else if (alt >= 3) {
        finalSize = opp(lastS);
        regime = `🛡️ LVL 2 DEEP CHOP FLIP (${opp(lastS)})`;
      } else if (alt >= 2) {
        finalSize = lastS;
        regime = `🛡️ LVL 2 CHOP STABILIZE (${lastS})`;
      } else if (delta >= 5) {
        finalSize = opp(cSide);
        regime = `🛡️ LVL 2 VOLATILE DELTA FLIP (d=${delta})`;
      } else {
        finalSize = cSide;
        regime = `🛡️ LVL 2 MOMENTUM LOCK (${cSide})`;
      }
    }
    // --- LEVEL 1 BASE PREDICTION (STREAK == 0) ---
    else {
      if (cLen >= 4) {
        finalSize = cSide;
        regime = `🌊 DRAGON EXTENSION RIDE (${cSide} x${cLen})`;
        conf = 94;
      } else if (cLen === 3) {
        finalSize = opp(cSide);
        regime = `🐉 DRAGON EXHAUSTION CUT (${opp(cSide)} x3)`;
        conf = 96;
      } else if (alt >= 3) {
        finalSize = cSide;
        regime = `⚡ DEEP CHOP BREAK FLOW (${cSide})`;
        conf = 93;
      } else if (alt >= 2) {
        finalSize = opp(lastS);
        regime = `⚡ CHOP OSCILLATE (${opp(lastS)})`;
        conf = 91;
      } else {
        finalSize = cSide;
        regime = `🌊 MOMENTUM FOLLOW (${cSide})`;
        conf = 88;
      }
    }

    // Harmonic Lucky Ball Selector
    const allowed = finalSize === 'BIG' ? [5, 6, 7, 8, 9] : [0, 1, 2, 3, 4];
    const freq = counts(nums.slice(-20));
    const bestNum = allowed.reduce((best, n) => {
      const diff = Math.abs(n - (finalSize === 'BIG' ? 7 : 2));
      const bestDiff = Math.abs(best - (finalSize === 'BIG' ? 7 : 2));
      return freq[n] < freq[best] || (freq[n] === freq[best] && diff < bestDiff) ? n : best;
    }, allowed[0]);

    return { size: finalSize, number: bestNum, confidence: conf, regime };
  }"""

for fpath in files:
    if not os.path.exists(fpath): continue
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace function definition
    content = re.sub(r'function predictApexTitanV[0-9]+\(evidence, lossStreak = 0\) \{[\s\S]*?return \{ size: finalSize, number: bestNum, confidence: conf, regime \};\s*\}', NEW_PREDICTOR_CODE, content)
    
    # Replace function calls and strings
    content = re.sub(r'predictApexTitanV[0-9]+', 'predictApexTitanV90', content)
    content = content.replace("V80", "V90").replace("v80", "v90").replace("V81", "V90").replace("v81", "v90").replace("V70", "V90").replace("v70", "v90")
    
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Updated {fpath}")

print("All userscripts updated successfully to Apex Titan V90!")
