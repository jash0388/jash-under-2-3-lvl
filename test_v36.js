function getRuns(sizes) {
  const runs = [];
  let curr = sizes[0];
  let l = 1;
  for (let i = 1; i < sizes.length; i++) {
    if (sizes[i] === curr) {
      l++;
    } else {
      runs.push({ size: curr, len: l });
      curr = sizes[i];
      l = 1;
    }
  }
  runs.push({ size: curr, len: l });
  return runs;
}

const opp = s => (s === "BIG" ? "SMALL" : "BIG");
const counts = nums => nums.reduce((o, n) => { o[n] = (o[n] || 0) + 1; return o; }, Array(10).fill(0));

function predictApexTitanV36(evidence, lossStreak = 0) {
  if (!evidence || evidence.length < 3) {
    return { size: "BIG", number: 7, confidence: 70, regime: "TITAN INITIALIZING" };
  }

  const nums = evidence.slice(-50);
  const sizes = nums.map(n => (n >= 5 ? "BIG" : "SMALL"));
  const last = sizes.at(-1);

  const runs = getRuns(sizes);
  const currRun = runs.at(-1);
  const currL = currRun.len;
  const prevL = runs.length >= 2 ? runs.at(-2).len : 1;

  // Measure recent alternation density in last 6 runs
  const recentRuns = runs.slice(-6);
  const avgLen = recentRuns.reduce((a, r) => a + r.len, 0) / recentRuns.length;
  const altRunsCount = recentRuns.filter(r => r.len === 1).length;
  const isChopRegime = altRunsCount >= 3;

  // Active alternation count at the very end
  let alt = 0;
  for (let i = runs.length - 1; i >= 0; i--) {
    if (runs[i].len === 1) alt++;
    else break;
  }

  let finalSize = "BIG";
  let regime = "TITAN FLOW";
  let conf = 85;

  // --- LEVEL 3 EMERGENCY RECOVERY SHIELD (lossStreak >= 2) ---
  if (lossStreak >= 2) {
    conf = 99;
    if (currL >= 2) {
      finalSize = last;
      regime = `🛑 LVL 3 DRAGON FOLLOW (${last} x${currL})`;
    } else if (alt >= 2) {
      finalSize = opp(last);
      regime = `🛑 LVL 3 CHOP FLIP (x${alt})`;
    } else {
      finalSize = last;
      regime = `🛑 LVL 3 MOMENTUM SYNC (${last})`;
    }
  }
  // --- LEVEL 2 RECOVERY SHIELD (lossStreak === 1) ---
  else if (lossStreak === 1) {
    conf = 94;
    if (currL >= 3) {
      finalSize = last;
      regime = `🛡️ LVL 2 DRAGON PERSIST (${last} x${currL})`;
    } else if (currL === 2) {
      if (isChopRegime) {
        finalSize = opp(last);
        regime = `🛡️ LVL 2 DOUBLET CUT (${last} x2)`;
      } else {
        finalSize = last;
        regime = `🛡️ LVL 2 DRAGON TRY (${last} x2)`;
      }
    } else if (alt >= 2) {
      finalSize = opp(last);
      regime = `🛡️ LVL 2 CHOP FLIP (x${alt})`;
    } else {
      finalSize = last;
      regime = `🛡️ LVL 2 MOMENTUM (${last})`;
    }
  }
  // --- LEVEL 1 NORMAL FLOW ---
  else {
    if (currL >= 3) {
      if (currL > 7) {
        finalSize = opp(last);
        regime = `⚖️ FATIGUE CUT (x${currL})`;
        conf = 92;
      } else {
        finalSize = last;
        regime = `🐉 DRAGON FLOW (${last} x${currL})`;
        conf = Math.min(98, 82 + currL * 3);
      }
    } else if (currL === 2) {
      if (avgLen >= 2.5) {
        finalSize = last;
        regime = `🐉 DRAGON EXPAND (${last} x2)`;
        conf = 88;
      } else if (isChopRegime) {
        finalSize = opp(last);
        regime = `⚡ DOUBLET FLIP (${last} x2)`;
        conf = 88;
      } else {
        finalSize = last;
        regime = `🐉 DRAGON TRY (${last} x2)`;
        conf = 84;
      }
    } else if (alt >= 3) {
      finalSize = opp(last);
      regime = `⚡ CHOP OSCILLATE (x${alt})`;
      conf = Math.min(96, 78 + alt * 3);
    } else if (currL === 1 && prevL === 2 && !isChopRegime) {
      finalSize = last;
      regime = `👥 DOUBLET 2ND (${last})`;
      conf = 86;
    } else {
      finalSize = last;
      regime = `🌊 FLOW MOMENTUM (${last})`;
      conf = 80;
    }
  }

  // Harmonic Lucky Ball Selector
  const allowed = finalSize === "BIG" ? [5, 6, 7, 8, 9] : [0, 1, 2, 3, 4];
  const freq = counts(nums.slice(-20));
  const bestNum = allowed.reduce((best, n) => {
    const diff = Math.abs(n - (finalSize === "BIG" ? 7 : 2));
    const bestDiff = Math.abs(best - (finalSize === "BIG" ? 7 : 2));
    return freq[n] < freq[best] || (freq[n] === freq[best] && diff < bestDiff) ? n : best;
  }, allowed[0]);

  return { size: finalSize, number: bestNum, confidence: conf, regime };
}

console.log("V36 JavaScript code parsed successfully!");
