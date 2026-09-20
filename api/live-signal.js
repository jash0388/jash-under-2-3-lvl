const fs = require('fs');
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

function computeServerPrediction(sizes, nums, streak, mode) {
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

  // If signal is older than 40s or empty, compute server-side directly from AR-Lottery stream
  if (!cur.period || (Date.now() - (cur.updatedAt || 0) > 40000)) {
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
          const hist = rows.slice(0, 50).reverse();
          const sizes = hist.map(r => r.size);
          const nums = hist.map(r => r.number);
          const pred = computeServerPrediction(sizes, nums, 0, mode);
          const bestNum = pred.finalSize === 'BIG' ? 7 : 2;
          const secNum = pred.finalSize === 'BIG' ? 8 : 3;

          cur = {
            period: targetPeriod,
            size: pred.finalSize,
            number: bestNum,
            balls: [bestNum, secNum],
            conf: pred.conf,
            regime: pred.regime,
            updatedAt: Date.now(),
            source: 'SERVER_AR_STREAM'
          };
          signals[mode] = cur;
          saveSignals(signals);
        }
      }
    } catch (e) {}
  }

  return res.status(200).json({ success: true, mode, signal: cur });
};
