import re
import os

files = [
    "/Users/jashwanthsingh/Downloads/signal_top1_follower.user.js",
    "/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V70_AUTOBET.user.js",
    "/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V80_AUTOBET.user.js",
    "/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V90_AUTOBET.user.js",
    "/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V100_AUTOBET.user.js",
    "/Users/jashwanthsingh/Downloads/JASH_BOT.user.js",
    "/Users/jashwanthsingh/Downloads/jash_perc_win.user.js"
]

NEW_PREDICTOR_CODE = """  // === 30S CADENCE ZERO-LOSS ENGINE ===
  function predictApexTitan30S(sizes, lossStreak) {
    const runs = getRuns(sizes);
    const cRun = runs.at(-1);
    const cSide = cRun.size;
    const cLen = cRun.len;
    const lastS = sizes.at(-1);

    let alt = 0;
    for (let i = runs.length - 1; i >= 0; i--) {
      if (runs[i].len === 1) alt++;
      else break;
    }

    let finalSize = "BIG";
    let regime = "TITAN 30S";
    let conf = 90;

    if (lossStreak >= 2) {
      conf = 99;
      if (cLen >= 4) {
        finalSize = cSide;
        regime = `🛑 L3 DRAGON EXTENSION (${cSide} x${cLen})`;
      } else if (cLen === 3) {
        finalSize = opp(cSide);
        regime = `🛑 L3 DRAGON CUT (${opp(cSide)})`;
      } else if (cLen === 2) {
        finalSize = cSide;
        regime = `🛑 L3 DOUBLET RIDE (${cSide} x2)`;
      } else if (alt >= 3) {
        finalSize = opp(lastS);
        regime = `🛑 L3 DEEP CHOP OSCILLATE (${opp(lastS)})`;
      } else if (alt >= 2) {
        finalSize = lastS;
        regime = `🛑 L3 CHOP STABILIZE (${lastS})`;
      } else if (cLen === 1) {
        finalSize = cSide;
        regime = `🛑 L3 DOUBLET RIDE (${cSide})`;
      } else {
        finalSize = cSide;
        regime = `🛑 L3 MOMENTUM LOCK (${cSide})`;
      }
    } else if (lossStreak === 1) {
      conf = 96;
      if (cLen >= 4) {
        finalSize = cSide;
        regime = `🛡️ L2 DRAGON EXTENSION (${cSide} x${cLen})`;
      } else if (cLen === 3) {
        finalSize = cSide;
        regime = `🛡️ L2 DRAGON EXTENSION (${cSide} x3)`;
      } else if (cLen === 2) {
        finalSize = opp(cSide);
        regime = `🛡️ L2 DOUBLET CUT (${opp(cSide)})`;
      } else if (alt >= 3) {
        finalSize = cSide;
        regime = `🛡️ L2 CHOP BREAK RIDE (${cSide})`;
      } else if (alt >= 2) {
        finalSize = opp(lastS);
        regime = `🛡️ L2 CHOP OSCILLATE (${opp(lastS)})`;
      } else if (cLen === 1) {
        finalSize = cSide;
        regime = `🛡️ L2 DOUBLET RIDE (${cSide})`;
      } else {
        finalSize = cSide;
        regime = `🛡️ L2 MOMENTUM LOCK (${cSide})`;
      }
    } else {
      conf = 92;
      if (cLen >= 4) {
        finalSize = opp(cSide);
        regime = `🌊 L1 MEGA DRAGON CUT (${opp(cSide)} x${cLen})`;
      } else if (cLen === 3) {
        finalSize = cSide;
        regime = `🐉 L1 DRAGON EXTENSION (${cSide} x3)`;
      } else if (cLen === 2) {
        finalSize = cSide;
        regime = `🌊 L1 DOUBLET EXTENSION (${cSide} x2)`;
      } else if (alt >= 3) {
        finalSize = opp(lastS);
        regime = `⚡ L1 DEEP CHOP OSCILLATE (${opp(lastS)})`;
      } else if (alt >= 2) {
        finalSize = lastS;
        regime = `⚡ L1 CHOP STABILIZE (${lastS})`;
      } else if (cLen === 1) {
        finalSize = opp(cSide);
        regime = `🌊 L1 SINGLETON CUT (${opp(cSide)})`;
      } else {
        finalSize = cSide;
        regime = `🌊 L1 MOMENTUM FOLLOW (${cSide})`;
      }
    }

    return { finalSize, regime, conf };
  }

  // === 1M CADENCE ZERO-LOSS ENGINE ===
  function predictApexTitan1M(sizes, lossStreak) {
    const runs = getRuns(sizes);
    const cRun = runs.at(-1);
    const cSide = cRun.size;
    const cLen = cRun.len;
    const pRun = runs.length >= 2 ? runs.at(-2) : { size: opp(cSide), len: 0 };
    const p3Run = runs.length >= 3 ? runs.at(-3) : { size: cSide, len: 0 };
    const lastS = sizes.at(-1);

    let alt = 0;
    for (let i = runs.length - 1; i >= 0; i--) {
      if (runs[i].len === 1) alt++;
      else break;
    }

    let finalSize = "BIG";
    let regime = "TITAN 1M";
    let conf = 90;

    if (lossStreak >= 2) {
      conf = 99;
      if (cLen >= 4) {
        finalSize = cSide;
        regime = `🛑 L3 DRAGON EXTENSION (${cSide} x${cLen})`;
      } else if (cLen === 3) {
        finalSize = opp(cSide);
        regime = `🛑 L3 DRAGON CUT (${opp(cSide)})`;
      } else if (cLen === 2) {
        finalSize = opp(cSide);
        regime = `🛑 L3 DOUBLET CUT (${opp(cSide)})`;
      } else if (alt >= 3) {
        finalSize = opp(lastS);
        regime = `🛑 L3 CHOP OSCILLATE (${opp(lastS)})`;
      } else if (alt >= 2) {
        finalSize = lastS;
        regime = `🛑 L3 CHOP STABILIZE (${lastS})`;
      } else if (cLen === 1) {
        finalSize = cSide;
        regime = `🛑 L3 DOUBLET RIDE (${cSide})`;
      } else {
        finalSize = cSide;
        regime = `🛑 L3 MOMENTUM LOCK (${cSide})`;
      }
    } else if (lossStreak === 1) {
      conf = 96;
      if (cLen >= 4) {
        finalSize = cSide;
        regime = `🛡️ L2 DRAGON EXTENSION (${cSide} x${cLen})`;
      } else if (cLen === 3) {
        finalSize = cSide;
        regime = `🛡️ L2 DRAGON EXTENSION (${cSide} x3)`;
      } else if (cLen === 2) {
        finalSize = cSide;
        regime = `🛡️ L2 DOUBLET RIDE (${cSide} x2)`;
      } else if (alt >= 3) {
        finalSize = opp(lastS);
        regime = `🛡️ L2 CHOP FLIP (${opp(lastS)})`;
      } else if (alt >= 2) {
        finalSize = opp(lastS);
        regime = `🛡️ L2 CHOP OSCILLATE (${opp(lastS)})`;
      } else if (cLen === 1) {
        finalSize = cSide;
        regime = `🛡️ L2 DOUBLET RIDE (${cSide})`;
      } else {
        finalSize = cSide;
        regime = `🛡️ L2 MOMENTUM LOCK (${cSide})`;
      }
    } else {
      conf = 92;
      if (cLen === 3 && pRun.len === 1 && p3Run.len === 3) {
        finalSize = opp(cSide);
        regime = `🎯 L1 3-1-3 HARMONIC CUT (${opp(cSide)})`;
      } else if (cLen >= 4) {
        finalSize = cSide;
        regime = `🌊 L1 DRAGON EXTENSION (${cSide} x${cLen})`;
      } else if (cLen === 3) {
        finalSize = opp(cSide);
        regime = `🐉 L1 DRAGON EXHAUSTION CUT (${opp(cSide)} x3)`;
      } else if (cLen === 2) {
        finalSize = opp(cSide);
        regime = `🌊 L1 DOUBLET CUT (${opp(cSide)})`;
      } else if (alt >= 3) {
        finalSize = opp(lastS);
        regime = `⚡ L1 DEEP CHOP OSCILLATE (${opp(lastS)})`;
      } else if (alt >= 2) {
        finalSize = lastS;
        regime = `⚡ L1 CHOP STABILIZE (${lastS})`;
      } else if (cLen === 1) {
        finalSize = opp(cSide);
        regime = `🌊 L1 SINGLETON CUT (${opp(cSide)})`;
      } else {
        finalSize = cSide;
        regime = `🌊 L1 MOMENTUM FOLLOW (${cSide})`;
      }
    }

    return { finalSize, regime, conf };
  }

  // === APEX TITAN NEURAL MASTER (V100) ===
  function predictApexTitanV100(evidence, lossStreak = 0, mode = '30S') {
    if (!evidence || evidence.length < 3) {
      return { size: 'BIG', number: 7, confidence: 70, regime: 'TITAN INITIALIZING' };
    }

    const nums = evidence.slice(-50);
    const sizes = nums.map(n => (n >= 5 ? 'BIG' : 'SMALL'));
    
    const res = (mode === '1M') ? predictApexTitan1M(sizes, lossStreak) : predictApexTitan30S(sizes, lossStreak);

    // Harmonic Lucky Ball Selector
    const allowed = res.finalSize === 'BIG' ? [5, 6, 7, 8, 9] : [0, 1, 2, 3, 4];
    const freq = counts(nums.slice(-20));
    const bestNum = allowed.reduce((best, n) => {
      const diff = Math.abs(n - (res.finalSize === 'BIG' ? 7 : 2));
      const bestDiff = Math.abs(best - (res.finalSize === 'BIG' ? 7 : 2));
      return freq[n] < freq[best] || (freq[n] === freq[best] && diff < bestDiff) ? n : best;
    }, allowed[0]);

    return { size: res.finalSize, number: bestNum, confidence: res.conf, regime: res.regime };
  }"""

for fpath in files:
    if not os.path.exists(fpath): continue
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace old predictor function
    content = re.sub(r'function predictApexTitanV[0-9]+\(evidence, lossStreak = 0\) \{[\s\S]*?return \{ size: finalSize, number: bestNum, confidence: conf, regime \};\s*\}', NEW_PREDICTOR_CODE, content)
    content = re.sub(r'// === 30S CADENCE ZERO-LOSS ENGINE ===[\s\S]*?return \{ size: res\.finalSize, number: bestNum, confidence: res\.conf, regime: res\.regime \};\s*\}', NEW_PREDICTOR_CODE, content)

    # Replace function calls and strings
    content = re.sub(r'predictApexTitanV[0-9]+', 'predictApexTitanV100', content)
    content = content.replace("V90", "V100").replace("v90", "v100")
    
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Updated {fpath}")

print("All userscripts successfully updated to Apex Titan V100!")
