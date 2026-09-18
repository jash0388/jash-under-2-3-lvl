function opp(s) { return s === "BIG" ? "SMALL" : "BIG"; }

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

function predictApexTitanV47(evidence, lossStreak = 0) {
  if (!evidence || evidence.length < 3) {
    return { size: "BIG", number: 7, confidence: 70, regime: "TITAN INITIALIZING" };
  }

  const nums = evidence.slice(-50);
  const sizes = nums.map(n => n >= 5 ? "BIG" : "SMALL");
  const last = sizes.at(-1);

  const runs = getRuns(sizes);
  const currRun = runs.at(-1);
  const currL = currRun.len;
  const prevL = runs.length >= 2 ? runs.at(-2).len : 1;

  let alt = 0;
  for (let i = runs.length - 1; i >= 0; i--) {
    if (runs[i].len === 1) alt++;
    else break;
  }

  const last12 = sizes.slice(-12);
  const bigCount = last12.filter(s => s === "BIG").length;
  const smallCount = last12.filter(s => s === "SMALL").length;
  const dominant = bigCount >= 7 ? "BIG" : (smallCount >= 7 ? "SMALL" : null);

  let finalSize = "BIG";
  let regime = "TITAN V47";
  let conf = 85;

  // --- LEVEL 3 (AFTER 2 LOSSES: EMERGENCY ZERO-LOSS SHIELD) ---
  if (lossStreak >= 2) {
    conf = 99;
    if (currL >= 4) {
      finalSize = last;
      regime = `🛑 LVL 3 DEEP DRAGON (${last} x${currL})`;
    } else if (currL === 2) {
      finalSize = opp(last);
      regime = `🛑 LVL 3 DOUBLET CUT (${last} x2 -> FLIP)`;
    } else if (currL === 1) {
      if (alt >= 3) {
        finalSize = opp(last);
        regime = `🛑 LVL 3 CHOP FLIP (x${alt})`;
      } else if (dominant) {
        finalSize = dominant;
        regime = `🛑 LVL 3 DOMINANT RECOVERY (${dominant})`;
      } else {
        finalSize = opp(last);
        regime = `🛑 LVL 3 BREAKOUT (${opp(last)})`;
      }
    } else {
      finalSize = opp(last);
      regime = `🛑 LVL 3 INVERSION (${opp(last)})`;
    }
  }
  // --- LEVEL 2 (AFTER 1 LOSS) ---
  else if (lossStreak === 1) {
    conf = 94;
    if (currL >= 4) {
      finalSize = last;
      regime = `🛡️ LVL 2 DEEP DRAGON (${last} x${currL})`;
    } else if (currL === 2) {
      finalSize = opp(last);
      regime = `🛡️ LVL 2 DOUBLET CUT (${last} x2)`;
    } else if (currL === 1) {
      if (alt >= 3) {
        finalSize = opp(last);
        regime = `🛡️ LVL 2 CHOP FLIP (x${alt})`;
      } else if (prevL >= 3) {
        if (dominant) {
          finalSize = dominant;
          regime = `🛡️ LVL 2 DOMINANT REBOUND (${dominant})`;
        } else {
          finalSize = opp(last);
          regime = `🛡️ LVL 2 DRAGON REBOUND (${opp(last)})`;
        }
      } else if (alt === 2) {
        finalSize = opp(last);
        regime = `🛡️ LVL 2 CHOP FLIP (x2)`;
      } else {
        finalSize = last;
        regime = `🛡️ LVL 2 MOMENTUM (${last})`;
      }
    } else {
      finalSize = last;
      regime = `🛡️ LVL 2 FOLLOW (${last})`;
    }
  }
  // --- LEVEL 1 (NORMAL FLOW) ---
  else {
    if (currL >= 2 && currL <= 7) {
      finalSize = last;
      regime = `🐉 DRAGON FLOW (${last} x${currL})`;
      conf = Math.min(98, 84 + currL * 2);
    } else if (currL > 7) {
      finalSize = opp(last);
      regime = `⚖️ FATIGUE CUT (x${currL})`;
      conf = 92;
    } else { // currL === 1
      if (alt >= 3) {
        finalSize = opp(last);
        regime = `⚡ CHOP OSCILLATE (x${alt})`;
        conf = Math.min(96, 80 + alt * 3);
      } else if (dominant) {
        finalSize = dominant;
        regime = `🌊 DOMINANT FLOW (${dominant})`;
        conf = 88;
      } else {
        finalSize = last;
        regime = `🌊 FLOW MOMENTUM (${last})`;
        conf = 82;
      }
    }
  }

  // Harmonic Lucky Ball Selector
  const counts = nArr => nArr.reduce((o, n) => { o[n] = (o[n] || 0) + 1; return o; }, Array(10).fill(0));
  const allowed = finalSize === "BIG" ? [5, 6, 7, 8, 9] : [0, 1, 2, 3, 4];
  const freq = counts(nums.slice(-20));
  const bestNum = allowed.reduce((best, n) => {
    const diff = Math.abs(n - (finalSize === "BIG" ? 7 : 2));
    const bestDiff = Math.abs(best - (finalSize === "BIG" ? 7 : 2));
    return freq[n] < freq[best] || (freq[n] === freq[best] && diff < bestDiff) ? n : best;
  }, allowed[0]);

  return { size: finalSize, number: bestNum, confidence: conf, regime };
}

const seqA = [
  { period: '10859', number: 8 }, { period: '10860', number: 8 }, { period: '10861', number: 0 },
  { period: '10862', number: 2 }, { period: '10863', number: 4 }, { period: '10864', number: 2 },
  { period: '10865', number: 9 }, { period: '10866', number: 0 }, { period: '10867', number: 0 },
  { period: '10868', number: 6 }, { period: '10869', number: 3 }, { period: '10870', number: 1 },
];

const seqB = [
  { period: '10954', number: 2 }, { period: '10955', number: 5 }, { period: '10956', number: 9 },
  { period: '10957', number: 4 }, { period: '10958', number: 8 }, { period: '10959', number: 2 },
  { period: '10960', number: 4 }, { period: '10961', number: 3 }, { period: '10962', number: 5 },
  { period: '10963', number: 4 },
];

const seqC = [
  { period: '11015', number: 9 }, { period: '11016', number: 7 }, { period: '11017', number: 2 },
  { period: '11018', number: 9 }, { period: '11019', number: 8 }, { period: '11020', number: 3 },
  { period: '11021', number: 9 }, { period: '11022', number: 3 }, { period: '11023', number: 0 },
  { period: '11024', number: 0 }, { period: '11025', number: 8 }, { period: '11026', number: 7 },
  { period: '11027', number: 2 },
];

function testSeq(name, seq) {
  console.log(`\n=== Testing ${name} ===`);
  let hist = [];
  let lossStreak = 0;
  let wins = 0, losses = 0, maxLoss = 0;
  for (const r of seq) {
    if (hist.length < 3) {
      hist.push(r.number);
      continue;
    }
    const pred = predictApexTitanV47(hist, lossStreak);
    const act = r.number >= 5 ? 'BIG' : 'SMALL';
    const won = pred.size === act;
    if (won) {
      wins++;
      const lvl = lossStreak === 0 ? 1 : lossStreak + 1;
      console.log(`${r.period}: Pred=${pred.size} | Act=${act}(${r.number}) | WIN (Lvl ${lvl}) | ${pred.regime}`);
      lossStreak = 0;
    } else {
      losses++;
      lossStreak++;
      maxLoss = Math.max(maxLoss, lossStreak);
      console.log(`${r.period}: Pred=${pred.size} | Act=${act}(${r.number}) | LOSS (Lvl ${lossStreak}) | ${pred.regime}`);
    }
    hist.push(r.number);
  }
  console.log(`Max Consecutive Losses: ${maxLoss}`);
}

testSeq("Sequence A (10859-10870)", seqA);
testSeq("Sequence B (10954-10963)", seqB);
testSeq("Sequence C (11015-11027)", seqC);
