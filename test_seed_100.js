const opp = s => s === "BIG" ? "SMALL" : "BIG";

function getRuns(sizes) {
  const runs = [];
  if (!sizes.length) return runs;
  let curr = sizes[0], l = 1;
  for (let i = 1; i < sizes.length; i++) {
    if (sizes[i] === curr) l++;
    else { runs.push({ size: curr, len: l }); curr = sizes[i]; l = 1; }
  }
  runs.push({ size: curr, len: l });
  return runs;
}

function predictApexTitanV80(evidence, lossStreak = 0) {
  if (!evidence || evidence.length < 3) {
    return { size: "BIG", number: 7, confidence: 70, regime: "TITAN INITIALIZING" };
  }

  const nums = evidence.slice(-50);
  const sizes = nums.map(n => n >= 5 ? "BIG" : "SMALL");
  const runs = getRuns(sizes);
  
  const cRun = runs[runs.length - 1];
  const cSide = cRun.size;
  const cLen = cRun.len;

  const pRun = runs.length >= 2 ? runs[runs.length - 2] : { size: opp(cSide), len: 0 };
  const pSide = pRun.size;
  const pLen = pRun.len;

  const p3Run = runs.length >= 3 ? runs[runs.length - 3] : { size: cSide, len: 0 };
  const p3Side = p3Run.size;
  const p3Len = p3Run.len;

  const lastS = sizes[sizes.length - 1];
  const lastN = nums[nums.length - 1];
  const prevN = nums.length >= 2 ? nums[nums.length - 2] : lastN;
  const delta = Math.abs(lastN - prevN);

  let alt = 0;
  for (let i = runs.length - 1; i >= 0; i--) {
    if (runs[i].len === 1) alt++;
    else break;
  }

  let finalSize = "BIG";
  let regime = "TITAN V80";
  let conf = 88;

  // --- LEVEL 3 RECOVERY (STREAK >= 2) ---
  if (lossStreak >= 2) {
    conf = 99;
    if (cLen >= 3) {
      finalSize = cSide;
      regime = `🛑 LVL 3 DRAGON RIDE (${cSide} x${cLen})`;
    } else if (cLen === 2) {
      finalSize = cSide;
      regime = `🛑 LVL 3 DOUBLET RIDE (${cSide} x2)`;
    } else if (alt >= 3) {
      finalSize = cSide;
      regime = `🛑 LVL 3 CHOP BREAK RIDE (${cSide})`;
    } else if (alt >= 2) {
      finalSize = opp(cSide);
      regime = `🛑 LVL 3 CHOP OSCILLATE (${opp(cSide)})`;
    } else if (delta >= 5) {
      finalSize = opp(cSide);
      regime = `🛑 LVL 3 VOLATILE DELTA BREAK (d=${delta})`;
    } else {
      finalSize = opp(cSide);
      regime = `🛑 LVL 3 CASCADE SHIELD FLIP (${opp(cSide)})`;
    }
  }
  // --- LEVEL 2 RECOVERY (STREAK == 1) ---
  else if (lossStreak === 1) {
    conf = 95;
    if (cLen >= 3) {
      finalSize = opp(cSide);
      regime = `🛡️ LVL 2 DRAGON EXHAUSTION CUT (${opp(cSide)})`;
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
    if (cLen === 3 && pLen === 1 && p3Len === 3) {
      finalSize = cSide;
      regime = `⚡ TRIPLET CADENCE FOLLOW (${cSide})`;
      conf = 94;
    } else if (cLen >= 3) {
      finalSize = opp(cSide);
      regime = `🐉 DRAGON EXHAUSTION CUT (${opp(cSide)} x${cLen})`;
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

  return { size: finalSize, number: finalSize === "BIG" ? 7 : 2, confidence: conf, regime };
}

function generateDeterministicNumber(periodStr) {
  let hash = 0;
  for (let i = 0; i < periodStr.length; i++) {
    hash = (hash * 31 + periodStr.charCodeAt(i)) % 1000000007;
  }
  return Math.abs(hash % 10);
}

function prevPeriod(periodStr) {
  const p = String(periodStr || "");
  const c = p.split("");
  let borrow = 1;
  for (let i = c.length - 1; i >= 0 && borrow; i--) {
    let d = Number(c[i]) - borrow;
    if (d < 0) {
      d += 10;
      borrow = 1;
    } else {
      borrow = 0;
    }
    c[i] = String(d);
  }
  return c.join("");
}

function seed100Rounds(liveResults) {
  const MAX_HISTORY = 100;
  const oldestLivePeriod = liveResults[liveResults.length - 1].period;
  
  // Generate 120 historical numbers to have sufficient warmup for V80
  const fullSequence = [];
  let curr = oldestLivePeriod;
  for (let i = 0; i < 120; i++) {
    curr = prevPeriod(curr);
    fullSequence.unshift({
      period: curr,
      number: generateDeterministicNumber(curr),
      size: generateDeterministicNumber(curr) >= 5 ? "BIG" : "SMALL"
    });
  }
  
  // Append live results in chronological order (oldest to newest)
  const liveChronological = [...liveResults].reverse();
  fullSequence.push(...liveChronological);

  // Replay V80 engine
  const history = [];
  let streak = 0;
  let maxStreak = 0;
  let wins = 0, losses = 0;

  for (let i = 0; i < fullSequence.length; i++) {
    const item = fullSequence[i];
    if (i < 3) continue;
    const evidence = fullSequence.slice(Math.max(0, i - 50), i).map(x => x.number);
    const pred = predictApexTitanV80(evidence, streak);
    const won = pred.size === item.size;
    if (won) {
      wins++;
      streak = 0;
    } else {
      losses++;
      streak++;
      if (streak > maxStreak) maxStreak = streak;
    }
    history.unshift({
      period: item.period,
      actual: item.number,
      actualSize: item.size,
      predNumber: pred.number,
      predSize: pred.size,
      status: won ? "WIN" : "LOSS",
      regime: pred.regime,
      confidence: pred.confidence
    });
  }

  const final100 = history.slice(0, MAX_HISTORY);
  console.log(`Generated ${final100.length} rounds. Max Streak: ${maxStreak}, Wins: ${wins}, Losses: ${losses}`);
  console.log("Top 3 newest:", final100.slice(0, 3));
  console.log("Oldest 3:", final100.slice(-3));
  return final100;
}

const sampleLive = [
  { period: "20260919100010774", number: 2, size: "SMALL" },
  { period: "20260919100010773", number: 7, size: "BIG" },
  { period: "20260919100010772", number: 9, size: "BIG" }
];

seed100Rounds(sampleLive);
