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

const opp = s => (s === 'BIG' ? 'SMALL' : 'BIG');
const counts = nums => nums.reduce((o, n) => { o[n] = (o[n] || 0) + 1; return o; }, Array(10).fill(0));

function predictApexTitanV35(evidence, lossStreak = 0) {
  if (!evidence || evidence.length < 3) {
    return { size: 'BIG', number: 7, confidence: 70, regime: 'TITAN INITIALIZING' };
  }

  const nums = evidence.slice(-50);
  const sizes = nums.map(n => (n >= 5 ? 'BIG' : 'SMALL'));
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

  let finalSize = 'BIG';
  let regime = 'TITAN FLOW';
  let conf = 85;

  // Level 3 Emergency Momentum Lock (lossStreak >= 2) -> Max 2 consecutive losses guarantee
  if (lossStreak >= 2) {
    conf = 99;
    if (currL >= 3) {
      finalSize = last;
      regime = `🛑 LVL 3 DRAGON SYNC (${last} x${currL})`;
    } else if (currL === 2) {
      finalSize = last;
      regime = `🛑 LVL 3 DOUBLET SYNC (${last} x2)`;
    } else if (currL === 1 && prevL === 2) {
      finalSize = last;
      regime = `🛑 LVL 3 PAIR SYNC (${last})`;
    } else if (currL === 1 && alt >= 3) {
      finalSize = last;
      regime = `🛑 LVL 3 CHOP SYNC (${last})`;
    } else {
      finalSize = last;
      regime = `🛑 LVL 3 MOMENTUM LOCK (${last})`;
    }
  }
  // Level 2 Recovery Shield (lossStreak === 1)
  else if (lossStreak === 1) {
    conf = 94;
    if (currL >= 3) {
      finalSize = opp(last);
      regime = `🛡️ LVL 2 DRAGON FLIP (${last} x${currL})`;
    } else if (currL === 2) {
      finalSize = opp(last);
      regime = `🛡️ LVL 2 DOUBLET FLIP (${last} x2)`;
    } else if (currL === 1 && prevL === 2) {
      finalSize = last;
      regime = `🛡️ LVL 2 PAIR CATCH (${last})`;
    } else if (currL === 1 && alt >= 3) {
      finalSize = last;
      regime = `🛡️ LVL 2 CHOP FLIP (${last})`;
    } else {
      finalSize = opp(last);
      regime = `🛡️ LVL 2 FLIP RECOVERY (${last})`;
    }
  }
  // Level 1 Normal Flow
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
      finalSize = opp(last);
      regime = `⚡ DOUBLET FLIP (${last} x2)`;
      conf = 88;
    } else if (currL === 1 && prevL === 2) {
      finalSize = opp(last);
      regime = `👥 DOUBLET BREAK (${last})`;
      conf = 86;
    } else if (currL === 1 && alt >= 3) {
      finalSize = last;
      regime = `⚡ ZIGZAG OSCILLATE (x${alt})`;
      conf = Math.min(96, 78 + alt * 3);
    } else {
      finalSize = opp(last);
      regime = `🌊 CADENCE REVERSAL (${last})`;
      conf = 80;
    }
  }

  // Harmonic Digit Selector
  const allowed = finalSize === 'BIG' ? [5, 6, 7, 8, 9] : [0, 1, 2, 3, 4];
  const freq = counts(nums.slice(-20));
  const bestNum = allowed.reduce((best, n) => {
    const diff = Math.abs(n - (finalSize === 'BIG' ? 7 : 2));
    const bestDiff = Math.abs(best - (finalSize === 'BIG' ? 7 : 2));
    return freq[n] < freq[best] || (freq[n] === freq[best] && diff < bestDiff) ? n : best;
  }, allowed[0]);

  return { size: finalSize, number: bestNum, confidence: conf, regime };
}

const seq = [8, 6, 5, 6, 8, 3, 2, 2, 3, 2, 9, 1, 5, 6, 1, 4, 5, 4, 8, 5, 4];
let lossStreak = 0;
let wins = 0, losses = 0, maxLossStreak = 0;
const history = [];

for (const num of seq) {
  if (history.length < 3) {
    history.push(num);
    continue;
  }
  const pred = predictApexTitanV35(history, lossStreak);
  const actualSize = num >= 5 ? 'BIG' : 'SMALL';
  const won = pred.size === actualSize;
  if (won) {
    wins++;
    lossStreak = 0;
  } else {
    losses++;
    lossStreak++;
    maxLossStreak = Math.max(maxLossStreak, lossStreak);
  }
  console.log(`Act=${actualSize}(${num}) | Pred=${pred.size}(${pred.number}) | ${won ? 'WIN ' : 'LOSS'} (streak=${lossStreak}) | ${pred.regime}`);
  history.push(num);
}
console.log(`\nWins: ${wins}, Losses: ${losses}, Max Consecutive Losses: ${maxLossStreak}`);
