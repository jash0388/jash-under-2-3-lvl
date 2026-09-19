const { execSync } = require('child_process');

const all_12_seqs = [
  ["Seq A (10859-10870 1M)", [
    { period: '10859', number: 8, size: 'BIG' },
    { period: '10860', number: 8, size: 'BIG' },
    { period: '10861', number: 0, size: 'SMALL' },
    { period: '10862', number: 2, size: 'SMALL' },
    { period: '10863', number: 4, size: 'SMALL' },
    { period: '10864', number: 2, size: 'SMALL' },
    { period: '10865', number: 9, size: 'BIG' },
    { period: '10866', number: 0, size: 'SMALL' },
    { period: '10867', number: 0, size: 'SMALL' },
    { period: '10868', number: 6, size: 'BIG' },
    { period: '10869', number: 3, size: 'SMALL' },
    { period: '10870', number: 1, size: 'SMALL' },
  ]],
  ["Seq B (10954-10963 1M)", [
    { period: '10954', number: 2, size: 'SMALL' },
    { period: '10955', number: 5, size: 'BIG' },
    { period: '10956', number: 9, size: 'BIG' },
    { period: '10957', number: 4, size: 'SMALL' },
    { period: '10958', number: 8, size: 'BIG' },
    { period: '10959', number: 2, size: 'SMALL' },
    { period: '10960', number: 4, size: 'SMALL' },
    { period: '10961', number: 3, size: 'SMALL' },
    { period: '10962', number: 5, size: 'BIG' },
    { period: '10963', number: 4, size: 'SMALL' },
  ]],
  ["Seq C (11015-11027 1M)", [
    { period: '11015', number: 9, size: 'BIG' },
    { period: '11016', number: 7, size: 'BIG' },
    { period: '11017', number: 2, size: 'SMALL' },
    { period: '11018', number: 9, size: 'BIG' },
    { period: '11019', number: 8, size: 'BIG' },
    { period: '11020', number: 3, size: 'SMALL' },
    { period: '11021', number: 9, size: 'BIG' },
    { period: '11022', number: 3, size: 'SMALL' },
    { period: '11023', number: 0, size: 'SMALL' },
    { period: '11024', number: 0, size: 'SMALL' },
    { period: '11025', number: 8, size: 'BIG' },
    { period: '11026', number: 7, size: 'BIG' },
    { period: '11027', number: 2, size: 'SMALL' },
  ]],
  ["Seq D (52065-52074 30S)", [
    { period: '52065', number: 1, size: 'SMALL' },
    { period: '52066', number: 3, size: 'SMALL' },
    { period: '52067', number: 2, size: 'SMALL' },
    { period: '52068', number: 0, size: 'SMALL' },
    { period: '52069', number: 4, size: 'SMALL' },
    { period: '52070', number: 0, size: 'SMALL' },
    { period: '52071', number: 8, size: 'BIG' },
    { period: '52072', number: 6, size: 'BIG' },
    { period: '52073', number: 7, size: 'BIG' },
    { period: '52074', number: 2, size: 'SMALL' },
  ]],
  ["Seq E (11034-11053 1M)", [
    { period: '11034', number: 0, size: 'SMALL' },
    { period: '11035', number: 6, size: 'BIG' },
    { period: '11036', number: 7, size: 'BIG' },
    { period: '11037', number: 4, size: 'SMALL' },
    { period: '11038', number: 5, size: 'BIG' },
    { period: '11039', number: 4, size: 'SMALL' },
    { period: '11040', number: 2, size: 'SMALL' },
    { period: '11041', number: 0, size: 'SMALL' },
    { period: '11042', number: 0, size: 'SMALL' },
    { period: '11043', number: 4, size: 'SMALL' },
    { period: '11044', number: 4, size: 'SMALL' },
    { period: '11045', number: 7, size: 'BIG' },
    { period: '11046', number: 9, size: 'BIG' },
    { period: '11047', number: 2, size: 'SMALL' },
    { period: '11048', number: 5, size: 'BIG' },
    { period: '11049', number: 8, size: 'BIG' },
    { period: '11050', number: 4, size: 'SMALL' },
    { period: '11051', number: 5, size: 'BIG' },
    { period: '11052', number: 5, size: 'BIG' },
    { period: '11053', number: 1, size: 'SMALL' },
  ]],
  ["Seq F (11058-11075 1M)", [
    { period: '11058', number: 3, size: 'SMALL' },
    { period: '11059', number: 8, size: 'BIG' },
    { period: '11060', number: 9, size: 'BIG' },
    { period: '11061', number: 1, size: 'SMALL' },
    { period: '11062', number: 5, size: 'BIG' },
    { period: '11063', number: 0, size: 'SMALL' },
    { period: '11064', number: 1, size: 'SMALL' },
    { period: '11065', number: 2, size: 'SMALL' },
    { period: '11066', number: 5, size: 'BIG' },
    { period: '11067', number: 1, size: 'SMALL' },
    { period: '11068', number: 2, size: 'SMALL' },
    { period: '11069', number: 3, size: 'SMALL' },
    { period: '11070', number: 9, size: 'BIG' },
    { period: '11071', number: 0, size: 'SMALL' },
    { period: '11072', number: 2, size: 'SMALL' },
    { period: '11073', number: 0, size: 'SMALL' },
    { period: '11074', number: 6, size: 'BIG' },
    { period: '11075', number: 6, size: 'BIG' },
  ]],
  ["Seq G (11080-11099 1M)", [
    { period: '11080', number: 7, size: 'BIG' },
    { period: '11081', number: 7, size: 'BIG' },
    { period: '11082', number: 8, size: 'BIG' },
    { period: '11083', number: 6, size: 'BIG' },
    { period: '11084', number: 3, size: 'SMALL' },
    { period: '11085', number: 4, size: 'SMALL' },
    { period: '11086', number: 0, size: 'SMALL' },
    { period: '11087', number: 2, size: 'SMALL' },
    { period: '11088', number: 4, size: 'SMALL' },
    { period: '11089', number: 2, size: 'SMALL' },
    { period: '11090', number: 1, size: 'SMALL' },
    { period: '11091', number: 9, size: 'BIG' },
    { period: '11092', number: 1, size: 'SMALL' },
    { period: '11093', number: 7, size: 'BIG' },
    { period: '11094', number: 9, size: 'BIG' },
    { period: '11095', number: 2, size: 'SMALL' },
    { period: '11096', number: 7, size: 'BIG' },
    { period: '11097', number: 8, size: 'BIG' },
    { period: '11098', number: 7, size: 'BIG' },
    { period: '11099', number: 4, size: 'SMALL' },
  ]],
  ["Seq H (11119-11141 1M)", [
    { period: '11119', number: 3, size: 'SMALL' },
    { period: '11120', number: 9, size: 'BIG' },
    { period: '11121', number: 0, size: 'SMALL' },
    { period: '11122', number: 3, size: 'SMALL' },
    { period: '11123', number: 1, size: 'SMALL' },
    { period: '11124', number: 9, size: 'BIG' },
    { period: '11125', number: 5, size: 'BIG' },
    { period: '11126', number: 1, size: 'SMALL' },
    { period: '11127', number: 6, size: 'BIG' },
    { period: '11128', number: 0, size: 'SMALL' },
    { period: '11129', number: 8, size: 'BIG' },
    { period: '11130', number: 7, size: 'BIG' },
    { period: '11131', number: 5, size: 'BIG' },
    { period: '11132', number: 2, size: 'SMALL' },
    { period: '11133', number: 3, size: 'SMALL' },
    { period: '11134', number: 6, size: 'BIG' },
    { period: '11135', number: 7, size: 'BIG' },
    { period: '11136', number: 4, size: 'SMALL' },
    { period: '11137', number: 9, size: 'BIG' },
    { period: '11138', number: 4, size: 'SMALL' },
    { period: '11139', number: 7, size: 'BIG' },
    { period: '11140', number: 0, size: 'SMALL' },
    { period: '11141', number: 7, size: 'BIG' },
  ]],
  ["Seq I (10385-10392 1M - Screenshot 1)", [
    { period: '10385', number: 3, size: 'SMALL' },
    { period: '10386', number: 4, size: 'SMALL' },
    { period: '10387', number: 6, size: 'BIG' },
    { period: '10388', number: 5, size: 'BIG' },
    { period: '10389', number: 0, size: 'SMALL' },
    { period: '10390', number: 1, size: 'SMALL' },
    { period: '10391', number: 4, size: 'SMALL' },
    { period: '10392', number: 9, size: 'BIG' },
  ]],
  ["Seq J (10410-10418 1M - Screenshot 1)", [
    { period: '10410', number: 8, size: 'BIG' },
    { period: '10411', number: 7, size: 'BIG' },
    { period: '10412', number: 0, size: 'SMALL' },
    { period: '10413', number: 2, size: 'SMALL' },
    { period: '10414', number: 9, size: 'BIG' },
    { period: '10415', number: 2, size: 'SMALL' },
    { period: '10416', number: 1, size: 'SMALL' },
    { period: '10417', number: 8, size: 'BIG' },
    { period: '10418', number: 4, size: 'SMALL' },
  ]],
  ["Seq K (10548-10556 1M - Screenshot 1)", [
    { period: '10548', number: 7, size: 'BIG' },
    { period: '10549', number: 8, size: 'BIG' },
    { period: '10550', number: 2, size: 'SMALL' },
    { period: '10551', number: 9, size: 'BIG' },
    { period: '10552', number: 0, size: 'SMALL' },
    { period: '10553', number: 4, size: 'SMALL' },
    { period: '10554', number: 6, size: 'BIG' },
    { period: '10555', number: 6, size: 'BIG' },
    { period: '10556', number: 4, size: 'SMALL' },
  ]],
  ["Seq L (10720-10729 1M - Screenshot 2)", [
    { period: '10720', number: 2, size: 'SMALL' },
    { period: '10721', number: 1, size: 'SMALL' },
    { period: '10722', number: 7, size: 'BIG' },
    { period: '10723', number: 0, size: 'SMALL' },
    { period: '10724', number: 4, size: 'SMALL' },
    { period: '10725', number: 2, size: 'SMALL' },
    { period: '10726', number: 0, size: 'SMALL' },
    { period: '10727', number: 7, size: 'BIG' },
    { period: '10728', number: 0, size: 'SMALL' },
    { period: '10729', number: 9, size: 'BIG' },
  ]]
];

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
  let regime = "APEX TITAN V80";
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

let totalMaxStreak = 0;
console.log("================ JS V80 SIMULATION ================");
all_12_seqs.forEach(([name, seq]) => {
  const history = seq.slice(0, 3);
  let streak = 0;
  let maxStreak = 0;
  let wins = 0, losses = 0;
  
  for (let i = 3; i < seq.length; i++) {
    const item = seq[i];
    const evidence = history.map(h => h.number);
    const pred = predictApexTitanV80(evidence, streak);
    const act = item.size;
    if (pred.size === act) {
      wins++;
      streak = 0;
    } else {
      losses++;
      streak++;
      if (streak > maxStreak) maxStreak = streak;
    }
    history.push(item);
  }
  if (maxStreak > totalMaxStreak) totalMaxStreak = maxStreak;
  const pass = maxStreak <= 2 ? "✅ PASS" : "❌ FAIL";
  console.log(`${name}: ${wins}W/${losses}L | Max Streak: ${maxStreak} | ${pass}`);
});

console.log(`\nJS V80 TOTAL MAX CONSECUTIVE LOSSES = ${totalMaxStreak}`);
