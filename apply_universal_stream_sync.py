import os
import json
import re

print("=== Applying Universal Stream Sequential Simulation Sync ===")

# 1. Update api/live-signal.js
api_code = '''const fs = require('fs');
const path = require('path');

const SIGNAL_FILE = path.join('/tmp', 'jash_live_signal.json');

// In-memory signal state
let MEMORY_SIGNAL = {
  '30S': { period: '', size: 'BIG', number: 7, balls: [7, 8], conf: 92, regime: 'TITAN SUPREME v18.0', updatedAt: 0 },
  '1M': { period: '', size: 'BIG', number: 7, balls: [7, 8], conf: 92, regime: 'TITAN SUPREME v18.0', updatedAt: 0 }
};

function loadSignals() {
  try {
    if (fs.existsSync(SIGNAL_FILE)) {
      const data = JSON.parse(fs.readFileSync(SIGNAL_FILE, 'utf8'));
      if (data && typeof data === 'object') return data;
    }
  } catch (e) {}
  return MEMORY_SIGNAL;
}

function saveSignals(sig) {
  try {
    fs.writeFileSync(SIGNAL_FILE, JSON.stringify(sig), 'utf8');
    MEMORY_SIGNAL = sig;
  } catch (e) {
    MEMORY_SIGNAL = sig;
  }
}

// 9-Feature Rules Table
let TITAN_RULES_30S = {};
let TITAN_RULES_1M = {};
try {
  TITAN_RULES_30S = require('../v9um_apex_titan_supreme_9feature_rules.json');
} catch (e) {
  try {
    TITAN_RULES_30S = JSON.parse(fs.readFileSync(path.join(process.cwd(), 'v9um_apex_titan_supreme_9feature_rules.json'), 'utf8'));
  } catch (e2) {}
}

try {
  TITAN_RULES_1M = require('../v9um_apex_titan_supreme_9feature_1m_rules.json');
} catch (e) {
  try {
    TITAN_RULES_1M = JSON.parse(fs.readFileSync(path.join(process.cwd(), 'v9um_apex_titan_supreme_9feature_1m_rules.json'), 'utf8'));
  } catch (e2) {}
}

function opp(s) { return s === 'BIG' ? 'SMALL' : 'BIG'; }

function getRuns(sizes) {
  if (!sizes || !sizes.length) return [];
  const runs = [];
  let curr = sizes[0], l = 1;
  for (let i = 1; i < sizes.length; i++) {
    if (sizes[i] === curr) l++;
    else { runs.push({ size: curr, len: l }); curr = sizes[i]; l = 1; }
  }
  runs.push({ size: curr, len: l });
  return runs;
}

function extractFeatures9(sizes, nums, streak) {
  const runs = getRuns(sizes);
  const cRun = runs[runs.length - 1];
  const cSide = cRun.size;
  const cLen = cRun.len;
  const pRun = runs.length >= 2 ? runs[runs.length - 2] : { size: opp(cSide), len: 0 };
  const p2Run = runs.length >= 3 ? runs[runs.length - 3] : { size: cSide, len: 0 };
  const lastS = sizes[sizes.length - 1];
  const lastN = nums[nums.length - 1] !== undefined ? nums[nums.length - 1] : (lastS === 'BIG' ? 7 : 2);
  const prevN = nums.length >= 2 ? nums[nums.length - 2] : lastN;

  let alt = 0;
  for (let i = runs.length - 1; i >= 0; i--) {
    if (runs[i].len === 1) alt++;
    else break;
  }

  const cLenCat = Math.min(cLen, 4);
  const pLenCat = Math.min(pRun.len, 3);
  const p2LenCat = Math.min(p2Run.len, 3);
  const altCat = Math.min(alt, 3);
  const streakCat = Math.min(streak, 2);

  const recent = sizes.slice(-6);
  let flips = 0;
  for (let i = 1; i < recent.length; i++) {
    if (recent[i] !== recent[i - 1]) flips++;
  }
  const flipCat = flips <= 1 ? 0 : ((flips === 2 || flips === 3) ? 1 : 2);
  const cSideBit = cSide === 'BIG' ? 1 : 0;
  const parityBit = Math.abs(lastN) % 2;
  const harmonicBit = Math.abs(lastN + prevN) % 2;

  const key = `${streakCat}_${cLenCat}_${pLenCat}_${p2LenCat}_${altCat}_${flipCat}_${cSideBit}_${parityBit}_${harmonicBit}`;
  return { key, cSide, lastS, cLen, alt };
}

function predictApexTitan(sizes, nums, streak, mode) {
  const { key, cSide, lastS, cLen, alt } = extractFeatures9(sizes, nums, streak);

  let fallback = 'SAME';
  if (streak >= 2) fallback = cLen >= 2 ? cSide : (alt >= 2 ? opp(lastS) : cSide);
  else if (streak === 1) fallback = cLen >= 2 ? cSide : (alt >= 2 ? opp(lastS) : opp(cSide));
  else fallback = cLen >= 3 ? cSide : (cLen === 2 ? opp(cSide) : (alt >= 2 ? opp(lastS) : cSide));

  const table = (mode === '1M') ? TITAN_RULES_1M : TITAN_RULES_30S;
  const actRule = table[key] || fallback;

  let finalSize = cSide;
  if (actRule === 'SAME') finalSize = cSide;
  else if (actRule === 'OPP') finalSize = opp(cSide);
  else if (actRule === 'LAST') finalSize = lastS;
  else if (actRule === 'OPP_LAST') finalSize = opp(lastS);
  else if (actRule === 'BIG' || actRule === 'SMALL') finalSize = actRule;

  const conf = streak >= 2 ? 99 : (streak === 1 ? 96 : 92);
  const regimeTag = streak >= 2 ? `🛑 L3 RECOVERY (${actRule})` : (streak === 1 ? `🛡️ L2 RECOVERY (${actRule})` : `🌊 L1 APEX (${actRule})`);
  return { finalSize, regime: `${regimeTag} [${finalSize}]`, conf };
}

function simulateSequentialStream(drawsList, mode) {
  if (!drawsList || drawsList.length < 3) return { finalSize: 'BIG', number: 7, balls: [7, 8], conf: 92, regime: 'INITIALIZING', lossStreak: 0 };
  
  const sorted = [...drawsList].sort((a, b) => {
    try { return BigInt(a.period) > BigInt(b.period) ? 1 : -1; } catch (e) { return 0; }
  });

  let runningLossStreak = 0;
  const startIndex = Math.max(3, sorted.length - 30);
  for (let i = startIndex; i < sorted.length; i++) {
    const prev = sorted.slice(0, i);
    const pred = predictApexTitan(prev.map(r => r.size), prev.map(r => r.number), runningLossStreak, mode);
    const actual = sorted[i];
    if (pred.finalSize === actual.size) runningLossStreak = 0;
    else runningLossStreak++;
  }

  const nextPred = predictApexTitan(sorted.map(r => r.size), sorted.map(r => r.number), runningLossStreak, mode);
  const bestNum = nextPred.finalSize === 'BIG' ? 7 : 2;
  const secNum = nextPred.finalSize === 'BIG' ? 8 : 3;

  return {
    size: nextPred.finalSize,
    number: bestNum,
    balls: [bestNum, secNum],
    conf: nextPred.conf,
    regime: nextPred.regime,
    lossStreak: runningLossStreak
  };
}

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate');

  if (req.method === 'OPTIONS') return res.status(200).end();

  const signals = loadSignals();

  // POST: Web page (/pred) publishes its exact live prediction
  if (req.method === 'POST') {
    const body = req.body || {};
    const mode = (body.mode === '1M') ? '1M' : '30S';
    if (body.period && body.size) {
      signals[mode] = {
        period: String(body.period).trim(),
        size: String(body.size).trim().toUpperCase(),
        number: body.number != null ? parseInt(body.number) : (body.size === 'BIG' ? 7 : 2),
        balls: Array.isArray(body.balls) ? body.balls : (body.size === 'BIG' ? [7, 8] : [2, 3]),
        conf: body.conf || body.confidence || 92,
        regime: body.regime || 'TITAN SUPREME v18.0',
        updatedAt: Date.now(),
        source: 'WEB_TERMINAL'
      };
      saveSignals(signals);
      return res.status(200).json({ success: true, signal: signals[mode] });
    }
  }

  // GET: Phone Bot queries live signal
  const mode = (req.query?.mode === '1M') ? '1M' : '30S';
  let cur = signals[mode] || {};

  // If signal is older than 25s or empty, compute server-side with sequential stream replay
  if (!cur.period || (Date.now() - (cur.updatedAt || 0) > 25000)) {
    try {
      const url = (mode === '30S')
        ? 'https://draw.ar-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json'
        : 'https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json';
      const apiRes = await fetch(`${url}?_t=${Date.now()}`);
      if (apiRes.ok) {
        const payload = await apiRes.json();
        const list = payload?.data?.list || [];
        if (list.length >= 3) {
          const rows = list.map(item => ({
            period: String(item.issueNumber || item.period).trim(),
            number: parseInt(item.number),
            size: parseInt(item.number) >= 5 ? 'BIG' : 'SMALL'
          }));
          const targetPeriod = (BigInt(rows[0].period) + 1n).toString();
          const pred = simulateSequentialStream(rows, mode);

          cur = {
            period: targetPeriod,
            size: pred.size,
            number: pred.number,
            balls: pred.balls,
            conf: pred.conf,
            regime: pred.regime,
            updatedAt: Date.now(),
            source: 'SERVER_SEQUENTIAL_REPLAY'
          };
          signals[mode] = cur;
          saveSignals(signals);
        }
      }
    } catch (e) {}
  }

  return res.status(200).json({ success: true, mode, signal: cur });
};
'''

with open('api/live-signal.js', 'w') as f:
    f.write(api_code)
print("Updated api/live-signal.js with Sequential Stream Replay.")

# 2. Update build_script.py
with open('build_script.py', 'r') as f:
    bs = f.read()

# Replace computeMasterPrediction and local prediction in build_script.py
new_pred_logic = '''  function simulateSequentialStream(drawsList, mode) {
    if (!drawsList || drawsList.length < 3) return { size: 'BIG', number: 7, balls: [7, 8], conf: 92, mode: 'INITIALIZING' };
    
    const sorted = [...drawsList].sort((a, b) => {
      try { return BigInt(a.period) > BigInt(b.period) ? 1 : -1; } catch (e) { return 0; }
    });

    let runningLossStreak = 0;
    const startIndex = Math.max(3, sorted.length - 30);
    for (let i = startIndex; i < sorted.length; i++) {
      const prev = sorted.slice(0, i);
      const olderSizes = prev.map(r => r.size);
      const olderNums = prev.map(r => r.number);
      const pred = (mode === '1M')
        ? predictApexTitan1M(olderSizes, olderNums, runningLossStreak)
        : predictApexTitan30S(olderSizes, olderNums, runningLossStreak);
      const actual = sorted[i];
      if (pred.finalSize === actual.size) runningLossStreak = 0;
      else runningLossStreak++;
    }

    const fullSizes = sorted.map(r => r.size);
    const fullNums = sorted.map(r => r.number);
    const nextPred = (mode === '1M')
      ? predictApexTitan1M(fullSizes, fullNums, runningLossStreak)
      : predictApexTitan30S(fullSizes, fullNums, runningLossStreak);
    const bestNum = nextPred.finalSize === 'BIG' ? 7 : 2;
    const secNum = nextPred.finalSize === 'BIG' ? 8 : 3;

    return {
      size: nextPred.finalSize,
      number: bestNum,
      balls: [bestNum, secNum],
      conf: nextPred.conf,
      mode: nextPred.regime,
      lossStreak: runningLossStreak
    };
  }

  function computeMasterPrediction() {
    // 1. STRICTLY FOLLOW LIVE /PRED WEB SIGNAL IF AVAILABLE
    if (LIVE_WEB_SIGNAL && LIVE_WEB_SIGNAL.size) {
      const bestN = LIVE_WEB_SIGNAL.number != null ? LIVE_WEB_SIGNAL.number : (LIVE_WEB_SIGNAL.size === 'BIG' ? 7 : 2);
      const secN = LIVE_WEB_SIGNAL.size === 'BIG' ? 8 : 3;
      return {
        size: LIVE_WEB_SIGNAL.size,
        number: bestN,
        balls: LIVE_WEB_SIGNAL.balls || [bestN, secN],
        mode: `🎯 /PRED SIGNAL [${LIVE_WEB_SIGNAL.size}] (${LIVE_WEB_SIGNAL.regime || 'TITAN 9F'})`,
        conf: LIVE_WEB_SIGNAL.conf || 95
      };
    }

    // 2. Deterministic Sequential Stream Simulation (100% Identical to /pred)
    const results = getMergedResults();
    if (!results || results.length === 0) {
      return { size: 'BIG', balls: [7, 8], number: 7, mode: '👑 JASH VIP · CALIBRATING', conf: 90 };
    }

    const sim = simulateSequentialStream(results, GAME_MODE);
    return {
      size: sim.size,
      number: sim.number,
      balls: sim.balls,
      mode: sim.mode,
      conf: sim.conf
    };
  }'''

# Replace old computeMasterPrediction block
bs = re.sub(
    r'function computeMasterPrediction\(\) \{.*?\n  \}\n\n  // ── 6\. WIN/LOSS RESOLUTION SCANNER',
    new_pred_logic + '\n\n  // ── 6. WIN/LOSS RESOLUTION SCANNER',
    bs,
    flags=re.DOTALL
)

with open('build_script.py', 'w') as f:
    f.write(bs)
print("Updated build_script.py with simulateSequentialStream.")

# 3. Rebuild all userscripts
os.system('python3 build_script.py')
print("Rebuilt all userscripts.")
