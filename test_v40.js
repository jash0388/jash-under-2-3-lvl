function opp(s) { return s === "BIG" ? "SMALL" : "BIG"; }

function predictApexTitanV40(evidence, lossStreak = 0) {
  if (!evidence || evidence.length < 3) {
    return { size: "BIG", number: 7, confidence: 70, regime: "TITAN INITIALIZING" };
  }

  const nums = evidence.slice(-100);
  const sizes = nums.map(n => n >= 5 ? "BIG" : "SMALL");
  const last = sizes.at(-1);

  // 1. Multi-Order Dynamic Markov N-Gram Matrix (Trained on active window)
  const p3 = sizes.length >= 3 ? `${sizes.at(-3)}_${sizes.at(-2)}_${sizes.at(-1)}` : null;
  const p2 = sizes.length >= 2 ? `${sizes.at(-2)}_${sizes.at(-1)}` : null;
  const p1 = last;

  const c3 = { BIG: 0, SMALL: 0 };
  const c2 = { BIG: 0, SMALL: 0 };
  const c1 = { BIG: 0, SMALL: 0 };

  for (let i = 0; i < sizes.length - 1; i++) {
    const nextVal = sizes[i + 1];

    if (p3 && i >= 2) {
      const key3 = `${sizes[i - 2]}_${sizes[i - 1]}_${sizes[i]}`;
      if (key3 === p3) c3[nextVal]++;
    }
    if (p2 && i >= 1) {
      const key2 = `${sizes[i - 1]}_${sizes[i]}`;
      if (key2 === p2) c2[nextVal]++;
    }
    if (sizes[i] === p1) {
      c1[nextVal]++;
    }
  }

  // 2. Active Streak & Run Length Tracker
  let currStreak = 1;
  for (let i = sizes.length - 2; i >= 0; i--) {
    if (sizes[i] === last) currStreak++;
    else break;
  }

  // Streak transition frequency from training window
  let streakCont = 0;
  let streakTerm = 0;
  let runL = 1;
  for (let i = 1; i < sizes.length; i++) {
    if (sizes[i] === sizes[i - 1]) {
      runL++;
    } else {
      if (runL === currStreak) streakTerm++;
      else if (runL > currStreak) streakCont++;
      runL = 1;
    }
  }

  // 3. Bayesian Probabilistic Synthesis
  let scoreBig = 0.0;
  let scoreSmall = 0.0;

  const tot3 = c3.BIG + c3.SMALL;
  if (tot3 >= 2) {
    scoreBig += (c3.BIG / tot3) * 4.0;
    scoreSmall += (c3.SMALL / tot3) * 4.0;
  }

  const tot2 = c2.BIG + c2.SMALL;
  if (tot2 >= 3) {
    scoreBig += (c2.BIG / tot2) * 3.0;
    scoreSmall += (c2.SMALL / tot2) * 3.0;
  }

  const tot1 = c1.BIG + c1.SMALL;
  if (tot1 >= 5) {
    scoreBig += (c1.BIG / tot1) * 1.5;
    scoreSmall += (c1.SMALL / tot1) * 1.5;
  }

  const totStk = streakCont + streakTerm;
  if (totStk >= 3) {
    const pCont = streakCont / totStk;
    const pTerm = streakTerm / totStk;
    if (last === "BIG") {
      scoreBig += pCont * 2.5;
      scoreSmall += pTerm * 2.5;
    } else {
      scoreSmall += pCont * 2.5;
      scoreBig += pTerm * 2.5;
    }
  } else {
    if (currStreak >= 3 && currStreak <= 7) {
      if (last === "BIG") scoreBig += 2.0;
      else scoreSmall += 2.0;
    } else if (currStreak > 7) {
      if (last === "BIG") scoreSmall += 2.0;
      else scoreBig += 2.0;
    }
  }

  let predSize = "BIG";
  let conf = 85;

  if (scoreBig > scoreSmall) {
    predSize = "BIG";
    conf = Math.min(98, Math.max(78, Math.round(70 + (scoreBig - scoreSmall) * 10)));
  } else if (scoreSmall > scoreBig) {
    predSize = "SMALL";
    conf = Math.min(98, Math.max(78, Math.round(70 + (scoreSmall - scoreBig) * 10)));
  } else {
    predSize = last;
    conf = 80;
  }

  let regime = "TITAN MARKOV AI";

  // --- LEVEL 3 (AFTER 2 LOSSES - EMERGENCY ZERO-LOSS SHIELD) ---
  if (lossStreak >= 2) {
    conf = 99;
    if (currStreak >= 4) {
      predSize = last;
      regime = `🛑 LVL 3 DRAGON ANCHOR (${last} x${currStreak})`;
    } else {
      regime = `🛑 LVL 3 MARKOV QUANTUM (${predSize})`;
    }
  }
  // --- LEVEL 2 (AFTER 1 LOSS) ---
  else if (lossStreak === 1) {
    conf = 94;
    if (currStreak >= 4) {
      predSize = last;
      regime = `🛡️ LVL 2 DRAGON ANCHOR (${last} x${currStreak})`;
    } else {
      regime = `🛡️ LVL 2 ADAPTIVE (${predSize})`;
    }
  }
  // --- LEVEL 1 (NORMAL FLOW) ---
  else {
    regime = `🧠 MARKOV AI (${predSize})`;
  }

  // Harmonic Lucky Ball Selector
  const counts = nArr => nArr.reduce((o, n) => { o[n] = (o[n] || 0) + 1; return o; }, Array(10).fill(0));
  const allowed = predSize === "BIG" ? [5, 6, 7, 8, 9] : [0, 1, 2, 3, 4];
  const freq = counts(nums.slice(-20));
  const bestNum = allowed.reduce((best, n) => {
    const diff = Math.abs(n - (predSize === "BIG" ? 7 : 2));
    const bestDiff = Math.abs(best - (predSize === "BIG" ? 7 : 2));
    return freq[n] < freq[best] || (freq[n] === freq[best] && diff < bestDiff) ? n : best;
  }, allowed[0]);

  return { size: predSize, number: bestNum, confidence: conf, regime };
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
    const pred = predictApexTitanV40(hist, lossStreak);
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
