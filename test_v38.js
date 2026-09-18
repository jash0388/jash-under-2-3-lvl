function getRuns(sizes) {
  const runs = [];
  if (!sizes.length) return runs;
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

const opp = s => s === "BIG" ? "SMALL" : "BIG";

function predictApexTitanV38(evidence, lossStreak = 0) {
  if (!evidence || evidence.length < 3) {
    return { size: "BIG", number: 7, confidence: 70, regime: "TITAN INITIALIZING" };
  }

  const nums = evidence.slice(-50);
  const sizes = nums.map(n => n >= 5 ? "BIG" : "SMALL");
  const last = sizes.at(-1);

  const runs = getRuns(sizes);
  const currRun = runs.at(-1);
  const streak = currRun.len;
  const prevLen = runs.length >= 2 ? runs.at(-2).len : 1;
  const prev2Len = runs.length >= 3 ? runs.at(-3).len : 1;

  const recentRuns = runs.slice(-6);
  const avgLen = recentRuns.reduce((acc, r) => acc + r.len, 0) / recentRuns.length;

  let alt = 0;
  for (let i = runs.length - 1; i >= 0; i--) {
    if (runs[i].len === 1) alt++;
    else break;
  }

  let finalSize = "BIG";
  let regime = "TITAN FLOW";
  let conf = 85;

  // --- LEVEL 3 (AFTER 2 LOSSES) ---
  if (lossStreak >= 2) {
    conf = 99;
    if (streak >= 3) {
      finalSize = last;
      regime = `🛑 LVL 3 DRAGON LOCK (${last} x${streak})`;
    } else if (streak === 2) {
      if (avgLen <= 2.0) {
        finalSize = opp(last);
        regime = `🛑 LVL 3 DOUBLET CUT (${last} x2 -> FLIP)`;
      } else {
        finalSize = last;
        regime = `🛑 LVL 3 DRAGON TRY (${last} x2)`;
      }
    } else { // streak === 1
      if (prevLen === 1 && prev2Len === 2) {
        finalSize = last;
        regime = `🛑 LVL 3 2-BALL PAIR (${last})`;
      } else if (alt >= 3) {
        finalSize = opp(last);
        regime = `🛑 LVL 3 CHOP FLIP (x${alt})`;
      } else {
        finalSize = last;
        regime = `🛑 LVL 3 MOMENTUM LOCK (${last})`;
      }
    }
  }
  // --- LEVEL 2 (AFTER 1 LOSS) ---
  else if (lossStreak === 1) {
    conf = 94;
    if (streak >= 3) {
      finalSize = last;
      regime = `🛡️ LVL 2 DRAGON LOCK (${last} x${streak})`;
    } else if (streak === 2) {
      if (avgLen <= 2.0) {
        finalSize = opp(last);
        regime = `🛡️ LVL 2 DOUBLET CUT (${last} x2)`;
      } else {
        finalSize = last;
        regime = `🛡️ LVL 2 DRAGON TRY (${last} x2)`;
      }
    } else { // streak === 1
      if (prevLen === 1 && prev2Len === 2) {
        finalSize = last;
        regime = `🛡️ LVL 2 2-BALL PAIR (${last})`;
      } else if (alt >= 3) {
        finalSize = opp(last);
        regime = `🛡️ LVL 2 CHOP FLIP (x${alt})`;
      } else {
        finalSize = last;
        regime = `🛡️ LVL 2 MOMENTUM (${last})`;
      }
    }
  }
  // --- LEVEL 1 (NORMAL FLOW) ---
  else {
    if (streak >= 3 && streak <= 7) {
      finalSize = last;
      regime = `🐉 DRAGON FLOW (${last} x${streak})`;
      conf = Math.min(98, 84 + streak * 2);
    } else if (streak > 7) {
      finalSize = opp(last);
      regime = `⚖️ FATIGUE CUT (x${streak})`;
      conf = 92;
    } else if (streak === 2) {
      if (avgLen <= 2.0) {
        finalSize = opp(last);
        regime = `⚡ DOUBLET FLIP (${last} x2)`;
        conf = 90;
      } else {
        finalSize = last;
        regime = `🐉 DRAGON TRY (${last} x2)`;
        conf = 86;
      }
    } else { // streak === 1
      if (prevLen === 1 && prev2Len === 2) {
        finalSize = last;
        regime = `👥 2-BALL PAIR (${last})`;
        conf = 88;
      } else if (alt >= 3) {
        finalSize = opp(last);
        regime = `⚡ CHOP OSCILLATE (x${alt})`;
        conf = Math.min(96, 80 + alt * 3);
      } else {
        finalSize = last;
        regime = `🌊 FLOW MOMENTUM (${last})`;
        conf = 82;
      }
    }
  }

  // Harmonic Lucky Ball Selector
  const counts = nums => nums.reduce((o,n) => { o[n]=(o[n]||0)+1; return o; }, Array(10).fill(0));
  const allowed = finalSize === "BIG" ? [5, 6, 7, 8, 9] : [0, 1, 2, 3, 4];
  const freq = counts(nums.slice(-20));
  const bestNum = allowed.reduce((best, n) => {
    const diff = Math.abs(n - (finalSize === "BIG" ? 7 : 2));
    const bestDiff = Math.abs(best - (finalSize === "BIG" ? 7 : 2));
    return freq[n] < freq[best] || (freq[n] === freq[best] && diff < bestDiff) ? n : best;
  }, allowed[0]);

  return { size: finalSize, number: bestNum, confidence: conf, regime };
}

// Test on screenshot sequence
const seq = [
  { period: '10859', number: 8 },
  { period: '10860', number: 8 },
  { period: '10861', number: 0 },
  { period: '10862', number: 2 },
  { period: '10863', number: 4 },
  { period: '10864', number: 2 },
  { period: '10865', number: 9 },
  { period: '10866', number: 0 },
  { period: '10867', number: 0 },
  { period: '10868', number: 6 },
  { period: '10869', number: 3 },
  { period: '10870', number: 1 },
];

let hist = [];
let lossStreak = 0;
let wins = 0, losses = 0, maxLoss = 0;

for (const r of seq) {
  if (hist.length < 3) {
    hist.push(r.number);
    continue;
  }
  const pred = predictApexTitanV38(hist, lossStreak);
  const actSize = r.number >= 5 ? 'BIG' : 'SMALL';
  const won = pred.size === actSize;
  if (won) {
    wins++;
    lossStreak = 0;
    console.log(`${r.period}: Pred=${pred.size} | Act=${actSize}(${r.number}) | WIN (Lvl ${lossStreak + 1}) | ${pred.regime}`);
  } else {
    losses++;
    lossStreak++;
    maxLoss = Math.max(maxLoss, lossStreak);
    console.log(`${r.period}: Pred=${pred.size} | Act=${actSize}(${r.number}) | LOSS (Lvl ${lossStreak}) | ${pred.regime}`);
  }
  hist.push(r.number);
}

console.log(`\nMax Consecutive Losses: ${maxLoss}`);
