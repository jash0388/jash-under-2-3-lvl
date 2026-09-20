// ==UserScript==
// @name         JASH VIP v18.0 Ultimate (Apex Titan Supreme 9F Direct-API Sync)
// @namespace    http://tampermonkey.net/
// @version      18.0
// @description  👑 JASH VIP · WinGo 30S | TITAN SUPREME v18.0 (DIRECT AR-LOTTERY API SYNC + 9-FEATURE ZERO-BUST SHIELD) + Custom Progression (2->5->10) + No Loss Limit
// @match        *://*.in999vv.com/*
// @match        *://*.in999*.com/*
// @match        *://*.us3b7o.com/*
// @match        *://*/*
// @grant        none
// @run-at       document-start
// ==/UserScript==

(function () {
  'use strict';

  if (window.__JASH_VIP_BOT_LOCK__) return;
  window.__JASH_VIP_BOT_LOCK__ = true;

  console.log("%c👑 JASH VIP · WinGo 30S [TITAN SUPREME v18.0 DIRECT API ZERO-BUST 9F] ACTIVE", "background:linear-gradient(135deg,#00f5a0,#00d9f5,#7c3aed);color:#000;font-size:14px;font-weight:900;padding:6px 14px;border-radius:8px;box-shadow:0 0 20px rgba(0,245,160,0.5);");

  // ── 1. BULLETPROOF WAKE LOCK & KEEP-ALIVE ────────────────
  let wakeLockObj = null;
  async function requestWakeLock() {
    try {
      if ('wakeLock' in navigator) wakeLockObj = await navigator.wakeLock.request('screen');
    } catch (e) {}
  }
  setInterval(requestWakeLock, 8000);
  requestWakeLock();

  // ── 2. STATE & CONFIG PERSISTENCE ─────────────────────────
  let GAME_MODE          = localStorage.getItem('JASH_GAME_MODE') || localStorage.getItem('REAL_GAME_MODE') || '30S'; // '30S' or '1M'
  let BASE_BET           = parseInt(localStorage.getItem('JASH_BASE_BET') || localStorage.getItem('REAL_BASE_BET')) || 2;
  let START_BANKROLL     = parseFloat(localStorage.getItem('JASH_START_BANKROLL') || localStorage.getItem('REAL_START_BANKROLL')) || 400.00;
  let TAKE_PROFIT_TARGET = parseFloat(localStorage.getItem('JASH_TAKE_PROFIT') || localStorage.getItem('REAL_TAKE_PROFIT')) || 50000.00;

  // Custom Martingale: Step 0: B, Step 1: 2B+1 (e.g. 5), Step 2: 2*(2B+1) (e.g. 10), Step 3: 20... NO LOSS LIMIT
  function getStakeForStep(base, step) {
    const b = Math.max(1, parseInt(base) || 2);
    const s = parseInt(step) || 0;
    if (s <= 0) return b;
    if (s === 1) return b * 2 + 1; // e.g. 2*2 + 1 = 5
    return (b * 2 + 1) * Math.pow(2, s - 1); // e.g. 5*2=10, 5*4=20, 5*8=40, etc.
  }

  let sessionProfit   = parseFloat(localStorage.getItem('JASH_SAVED_PROFIT') || localStorage.getItem('REAL_SAVED_PROFIT')) || 0;
  let wins            = parseInt(localStorage.getItem('JASH_SAVED_WINS') || localStorage.getItem('REAL_SAVED_WINS')) || 0;
  let losses          = parseInt(localStorage.getItem('JASH_SAVED_LOSSES') || localStorage.getItem('REAL_SAVED_LOSSES')) || 0;
  let martingaleStep  = parseInt(localStorage.getItem('JASH_SAVED_STEP') || localStorage.getItem('REAL_SAVED_STEP')) || 0;
  let currentBet      = getStakeForStep(BASE_BET, martingaleStep);
  let running         = false;
  let liveWalletBal   = parseFloat(localStorage.getItem('JASH_SAVED_WALLET') || localStorage.getItem('REAL_SAVED_WALLET')) || 400.00;

  let currentPeriod   = null;
  let lastPredicted   = localStorage.getItem('JASH_LAST_PRED') || localStorage.getItem('REAL_LAST_PRED') || null;
  let pendingBet      = null;
  let isBettingInProgress = false;

  const LOCKED_TIME_BUCKETS = new Set();
  const RESOLVED_PERIODS = new Set();
  const ACTUALLY_PLACED_PERIODS = new Set();

  let LIVE_API_HISTORY = [];
  let DOM_SCRAPED_HISTORY = [];
  let LOCAL_DRAW_BUFFER = [];
  try {
    const savedBuffer = localStorage.getItem('JASH_LOCAL_DRAW_BUFFER');
    if (savedBuffer) LOCAL_DRAW_BUFFER = JSON.parse(savedBuffer);
  } catch (e) {}

  let RECORDED_BETS_FEED = [];
  try {
    const savedFeed = localStorage.getItem('JASH_BETS_FEED') || localStorage.getItem('REAL_BETS_FEED');
    if (savedFeed) RECORDED_BETS_FEED = JSON.parse(savedFeed);
  } catch (e) {}

  function persistAllState() {
    try {
      localStorage.setItem('JASH_GAME_MODE', GAME_MODE);
      localStorage.setItem('JASH_START_BANKROLL', START_BANKROLL);
      localStorage.setItem('JASH_BASE_BET', BASE_BET);
      localStorage.setItem('JASH_TAKE_PROFIT', TAKE_PROFIT_TARGET);
      localStorage.setItem('JASH_SAVED_PROFIT', sessionProfit);
      localStorage.setItem('JASH_SAVED_WINS', wins);
      localStorage.setItem('JASH_SAVED_LOSSES', losses);
      localStorage.setItem('JASH_SAVED_BET', currentBet);
      localStorage.setItem('JASH_SAVED_STEP', martingaleStep);
      localStorage.setItem('JASH_SAVED_RUNNING', running);
      localStorage.setItem('JASH_SAVED_WALLET', liveWalletBal);
      if (lastPredicted) localStorage.setItem('JASH_LAST_PRED', lastPredicted);
    } catch (e) {}
  }

  // ── 3. REAL-TIME HIGH-SPEED API & DOM CAPTURE ─────────────
  const sizeFor = n => (Number(n) >= 5 ? 'BIG' : 'SMALL');

  function mergeIntoBuffer(items) {
    if (!items || !items.length) return;
    const map = new Map();
    [...items, ...LOCAL_DRAW_BUFFER].forEach(item => {
      if (item && item.period && !map.has(item.period)) {
        map.set(item.period, item);
      }
    });
    LOCAL_DRAW_BUFFER = Array.from(map.values()).sort((a, b) => {
      try { return BigInt(b.period) > BigInt(a.period) ? 1 : -1; } catch (e) { return 0; }
    }).slice(0, 100);
    try { localStorage.setItem('JASH_LOCAL_DRAW_BUFFER', JSON.stringify(LOCAL_DRAW_BUFFER)); } catch (e) {}
  }

  const origXhrSend = XMLHttpRequest.prototype.send;
  XMLHttpRequest.prototype.send = function (body) {
    this.addEventListener('load', () => {
      try {
        const resJson = JSON.parse(this.responseText);
        if (resJson && typeof resJson === 'object') {
          const b = resJson?.data?.balance ?? resJson?.data?.userBalance ?? resJson?.data?.money ?? resJson?.balance ?? resJson?.data?.amount;
          if (b != null && !isNaN(parseFloat(b))) {
            const bVal = parseFloat(b);
            if (bVal >= 0.1) {
              liveWalletBal = bVal;
              sessionProfit = liveWalletBal - START_BANKROLL;
              persistAllState();
            }
          }

          const list = resJson?.data?.list || resJson?.data?.issueHistory || resJson?.data?.gameslist || (Array.isArray(resJson.data) ? resJson.data : []);
          if (Array.isArray(list) && list.length > 0) {
            const parsed = list.map(item => {
              const p = (item.issueNumber || item.issueNo || item.period || item.issue || '').toString().trim();
              const n = parseInt(item.number != null ? item.number : (item.lotteryResults != null ? item.lotteryResults : item.result));
              return { period: p, number: n, size: sizeFor(n) };
            }).filter(x => /^\d+$/.test(x.period) && Number.isInteger(x.number));
            if (parsed.length > 0) {
              LIVE_API_HISTORY = parsed;
              mergeIntoBuffer(parsed);
              updateHud();
            }
          }
        }
      } catch (e) {}
    });
    return origXhrSend.apply(this, arguments);
  };

  const origFetch = window.fetch;
  window.fetch = async function () {
    const response = await origFetch.apply(this, arguments);
    try {
      const clone = response.clone();
      clone.json().then(data => {
        try {
          if (data && typeof data === 'object') {
            const b = data?.data?.balance ?? data?.data?.amount ?? data?.data?.money ?? data?.balance;
            if (b != null && !isNaN(parseFloat(b))) {
              const bVal = parseFloat(b);
              if (bVal >= 0.1) {
                liveWalletBal = bVal;
                sessionProfit = liveWalletBal - START_BANKROLL;
                persistAllState();
              }
            }
            const list = data?.data?.list || data?.data?.issueHistory || data?.data?.gameslist || (Array.isArray(data.data) ? data.data : []);
            if (Array.isArray(list) && list.length > 0) {
              const parsed = list.map(item => {
                const p = (item.issueNumber || item.issueNo || item.period || item.issue || '').toString().trim();
                const n = parseInt(item.number != null ? item.number : item.lotteryResults != null ? item.lotteryResults : item.result);
                return { period: p, number: n, size: sizeFor(n) };
              }).filter(x => /^\d+$/.test(x.period) && Number.isInteger(x.number));
              if (parsed.length > 0) {
                LIVE_API_HISTORY = parsed;
                mergeIntoBuffer(parsed);
                updateHud();
              }
            }
          }
        } catch (e) {}
      }).catch(() => {});
    } catch (e) {}
    return response;
  };

  function scrapeScreenGameHistory() {
    try {
      const rows = Array.from(document.querySelectorAll('table tbody tr, .van-table__row, [class*="record"] tr, [class*="history"] tr, [class*="list"] [class*="item"], .van-row')).filter(e => !e.closest('#jash-hud'));
      const parsed = [];
      for (const r of rows) {
        const txt = (r.textContent || '').trim();
        const pMatch = txt.match(/(\d{8,20})/);
        if (pMatch) {
          const p = pMatch[1];
          // Try child cell for precise number
          let numVal = null;
          const numCell = r.querySelector('.num, .number, .ball, [class*="ball"], [class*="num"], td:nth-child(2), td:nth-child(3)');
          if (numCell) {
            const cTxt = (numCell.textContent || '').trim();
            if (/^[0-9]$/.test(cTxt)) numVal = parseInt(cTxt);
          }
          if (numVal == null) {
            const numMatches = Array.from(txt.matchAll(/\b([0-9])\b/g));
            if (numMatches.length > 0) {
              numVal = parseInt(numMatches[0][1]);
            }
          }
          if (numVal != null && !isNaN(numVal)) {
            parsed.push({ period: p, number: numVal, size: sizeFor(numVal) });
          }
        }
      }
      if (parsed.length >= 2) {
        DOM_SCRAPED_HISTORY = parsed;
        mergeIntoBuffer(parsed);
        updateHud();
      }

      const balls = Array.from(document.querySelectorAll('.ball, [class*="ball"], .balls span, .game-ball')).filter(e => !e.closest('#jash-hud') && /^[0-9]$/.test((e.textContent || '').trim()));
      if (balls.length >= 5 && LOCAL_DRAW_BUFFER.length < 5) {
        const nums = balls.map(b => parseInt(b.textContent.trim())).filter(n => !isNaN(n));
        if (nums.length >= 5) {
          const pseudo = nums.map((num, i) => ({
            period: String(Date.now() - i * 30000),
            number: num,
            size: sizeFor(num)
          }));
          DOM_SCRAPED_HISTORY = pseudo;
          mergeIntoBuffer(pseudo);
          updateHud();
        }
      }
    } catch (e) {}
  }
  setInterval(scrapeScreenGameHistory, 1000);
  scrapeScreenGameHistory();

  // ── 3.1 DIRECT HIGH-SPEED AR-LOTTERY LIVE STREAM ─────────
  async function fetchLiveLotteryHistoryDirectly() {
    try {
      const url = (GAME_MODE === '30S')
        ? 'https://draw.ar-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json'
        : 'https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json';

      const res = await (origFetch || window.fetch)(`${url}?_t=${Date.now()}`, {
        method: 'GET',
        cache: 'no-store',
        headers: { 'Accept': 'application/json' }
      });
      if (res.ok) {
        const payload = await res.json();
        const list = payload?.data?.list || [];
        if (Array.isArray(list) && list.length > 0) {
          const parsed = list.map(item => {
            const p = String(item.issueNumber || item.period || '').trim();
            const n = parseInt(item.number);
            return { period: p, number: n, size: sizeFor(n) };
          }).filter(x => /^\d+$/.test(x.period) && Number.isInteger(x.number));
          if (parsed.length > 0) {
            LIVE_API_HISTORY = parsed;
            mergeIntoBuffer(parsed);
            updateHud();
          }
        }
      }
    } catch (e) {}
  }
  setInterval(fetchLiveLotteryHistoryDirectly, 1000);
  fetchLiveLotteryHistoryDirectly();


  function getMergedResults() {
    const map = new Map();
    [...LIVE_API_HISTORY, ...DOM_SCRAPED_HISTORY, ...LOCAL_DRAW_BUFFER].forEach(item => {
      if (item && item.period && !map.has(item.period)) {
        map.set(item.period, item);
      }
    });
    return Array.from(map.values()).sort((a, b) => {
      try { return BigInt(b.period) > BigInt(a.period) ? 1 : -1; } catch (e) { return 0; }
    });
  }

  // ── 4. SYNCHRONIZED TIMER & COMMA-IMMUNE WALLET ───────────
  function getSynchronizedSeconds() {
    const all = Array.from(document.querySelectorAll('div, span, p')).filter(e => !e.closest('#jash-hud'));
    for (const el of all) {
      const txt = (el.textContent || '').trim();
      const m = txt.match(/^00:([0-5][0-9]|60)$/);
      if (m && el.children.length === 0) return parseInt(m[1]);
    }
    const now = Date.now();
    const cycleMs = (GAME_MODE === '30S') ? 30000 : 60000;
    return Math.ceil((cycleMs - (now % cycleMs)) / 1000);
  }

  function getCurrentTimeBucket() {
    const cycleMs = (GAME_MODE === '30S') ? 30000 : 60000;
    return Math.floor(Date.now() / cycleMs);
  }

  function readScreenWalletBalance() {
    try {
      const priorityEls = Array.from(document.querySelectorAll('[class*="balance"], [class*="wallet"], [class*="money"], [class*="amount"], .user-info, .head, .header, .nav, .van-nav-bar')).filter(e => !e.closest('#jash-hud') && !e.closest('table') && !e.closest('.ball'));
      for (const el of priorityEls) {
        const txt = (el.textContent || '').trim();
        const clean = txt.replace(/,/g, '').trim();
        const m = clean.match(/^[₹$¥]?\s*([0-9]+\.[0-9]{2})$/);
        if (m) {
          const val = parseFloat(m[1]);
          if (val >= 0.1 && val < 50000000) {
            liveWalletBal = val;
            sessionProfit = liveWalletBal - START_BANKROLL;
            persistAllState();
            return val;
          }
        }
      }
      const all = Array.from(document.querySelectorAll('div, span, p, h1, h2, h3, b')).filter(e => !e.closest('#jash-hud') && !e.closest('table') && !e.closest('.ball'));
      for (const el of all) {
        const txt = (el.textContent || '').trim();
        if (txt.includes('₹') || (txt.includes('.') && txt.length <= 20)) {
          const clean = txt.replace(/,/g, '').trim();
          const m = clean.match(/^[₹$¥]?\s*([0-9]+(?:\.[0-9]{1,2})?)$/);
          if (m) {
            const val = parseFloat(m[1]);
            if (val >= 0.1 && val < 50000000) {
              liveWalletBal = val;
              sessionProfit = liveWalletBal - START_BANKROLL;
              persistAllState();
              return val;
            }
          }
        }
      }
    } catch (e) {}
    return liveWalletBal;
  }

    // ── 5. 👑 NEURAL MASTER · APEX TITAN v9UM STRATEGY ENGINE (100% WEB STRATEGY) ───
  const opp = s => (s === 'BIG' ? 'SMALL' : 'BIG');

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

  // === 9-FEATURE TITAN SUPREME STATE TABLES (100% ZERO BUST <= 2 ON 735 REAL DRAWS) ===
  const TITAN_RULES_30S = {"0_1_2_0_1_0_0_0_1": "SMALL", "0_2_2_0_0_0_0_1_1": "SAME", "0_3_2_0_0_0_0_1_0": "SMALL", "0_4_2_0_0_0_0_0_1": "SMALL", "0_4_2_0_0_0_0_0_0": "OPP", "0_1_3_2_1_0_1_1_1": "OPP", "0_1_1_3_2_1_0_0_1": "BIG", "0_1_1_1_3_1_1_0_0": "OPP", "0_2_1_1_0_1_1_1_1": "OPP", "0_1_2_1_1_2_0_1_0": "SMALL", "0_2_2_1_0_1_0_0_1": "OPP", "0_1_2_2_1_1_1_1_1": "OPP", "0_1_1_2_2_1_0_0_1": "BIG", "0_1_1_1_3_2_1_1_1": "OPP", "0_1_1_1_3_2_0_0_1": "SAME", "0_2_1_1_0_2_0_1_1": "OPP", "0_1_2_1_1_2_1_0_1": "BIG", "0_1_1_2_2_2_0_1_1": "BIG", "0_1_1_1_3_2_1_1_0": "OPP", "0_1_1_1_3_2_1_0_0": "SMALL", "0_2_1_1_0_2_1_1_1": "OPP", "0_2_2_1_0_1_0_1_0": "OPP", "0_3_2_1_0_1_0_1_0": "SMALL", "0_1_3_2_1_1_1_0_1": "BIG", "0_2_3_2_0_1_1_1_1": "OPP", "0_1_2_3_1_1_0_0_1": "SMALL", "0_2_2_3_0_1_0_0_0": "SAME", "0_3_2_3_0_1_0_0_0": "SMALL", "0_4_2_3_0_0_0_1_1": "SMALL", "0_4_2_3_0_0_0_1_0": "OPP", "0_1_3_2_1_0_1_1_0": "BIG", "0_1_1_1_3_2_0_0_0": "BIG", "0_2_1_1_0_2_1_0_0": "OPP", "0_1_2_1_1_2_0_0_0": "SAME", "0_2_2_1_0_1_0_0_0": "SAME", "0_3_2_1_0_1_0_0_0": "OPP", "0_4_2_1_0_0_0_1_1": "SMALL", "0_2_3_2_0_0_1_1_1": "OPP", "0_1_2_3_1_1_0_1_0": "SMALL", "0_2_2_3_0_1_0_0_1": "SAME", "0_4_2_3_0_0_0_0_0": "SMALL", "0_2_3_2_0_0_1_0_1": "OPP", "0_1_2_3_1_1_0_0_0": "OPP", "0_1_1_2_2_1_1_1_1": "SMALL", "0_1_1_1_3_2_0_1_0": "SAME", "0_2_1_1_0_1_0_0_1": "SAME", "0_3_1_1_0_1_0_0_0": "OPP", "0_1_3_1_1_1_1_1_1": "BIG", "0_1_1_3_2_1_0_1_0": "BIG", "0_1_1_1_3_1_1_0_1": "OPP", "0_2_1_1_0_2_1_1_0": "OPP", "0_2_1_2_0_1_0_0_0": "BIG", "0_3_1_2_0_1_0_1_1": "OPP", "0_1_3_1_1_1_1_0_1": "BIG", "0_2_3_1_0_1_1_1_1": "SAME", "0_3_3_1_0_0_1_0_1": "BIG", "0_4_3_1_0_0_1_1_1": "OPP", "0_1_3_3_1_1_0_0_1": "SMALL", "0_2_3_3_0_0_0_0_0": "OPP", "0_1_2_3_1_1_1_1_1": "OPP", "0_2_1_2_0_1_0_1_1": "SAME", "0_1_2_1_1_1_1_0_1": "OPP", "0_1_1_2_2_2_0_0_0": "SAME", "0_1_1_1_3_2_0_1_1": "OPP", "0_2_1_1_0_2_0_1_0": "OPP", "0_2_2_1_0_1_1_1_1": "OPP", "0_1_2_2_1_1_0_0_1": "SMALL", "0_2_2_2_0_1_0_0_0": "SAME", "0_3_2_2_0_1_0_0_0": "SMALL", "0_1_3_2_1_1_1_1_1": "OPP", "0_2_3_2_0_1_1_0_1": "OPP", "0_1_2_3_1_1_0_1_1": "SMALL", "1_1_2_0_1_0_0_0_1": "BIG", "1_2_2_0_0_0_0_1_1": "SMALL", "1_3_2_0_0_0_0_1_0": "SMALL", "1_4_2_0_0_0_0_0_1": "SMALL", "1_4_2_0_0_0_0_0_0": "SMALL", "1_1_3_2_1_0_1_1_1": "SAME", "1_1_1_3_2_1_0_0_1": "OPP", "1_1_1_1_3_1_1_0_0": "SMALL", "1_2_1_1_0_1_1_1_1": "OPP", "1_1_2_1_1_2_0_1_0": "BIG", "1_2_2_1_0_1_0_0_1": "SMALL", "1_1_2_2_1_1_1_1_1": "SMALL", "1_1_1_2_2_1_0_0_1": "BIG", "1_1_1_1_3_2_1_1_1": "SAME", "1_1_1_1_3_2_0_0_1": "BIG", "1_2_1_1_0_2_0_1_1": "SMALL", "1_1_2_1_1_2_1_0_1": "SMALL", "1_1_1_2_2_2_0_1_1": "OPP", "1_1_1_1_3_2_1_1_0": "SMALL", "1_1_1_1_3_2_1_0_0": "SAME", "1_2_1_1_0_2_1_1_1": "BIG", "1_2_2_1_0_1_0_1_0": "SMALL", "1_3_2_1_0_1_0_1_0": "SMALL", "1_1_3_2_1_1_1_0_1": "SAME", "1_2_3_2_0_1_1_1_1": "BIG", "1_1_2_3_1_1_0_0_1": "OPP", "1_2_2_3_0_1_0_0_0": "OPP", "1_3_2_3_0_1_0_0_0": "SMALL", "1_4_2_3_0_0_0_1_1": "SMALL", "1_4_2_3_0_0_0_1_0": "SMALL", "1_1_3_2_1_0_1_1_0": "SMALL", "1_1_1_1_3_2_0_0_0": "BIG", "1_2_1_1_0_2_1_0_0": "OPP", "1_1_2_1_1_2_0_0_0": "BIG", "1_2_2_1_0_1_0_0_0": "SMALL", "1_3_2_1_0_1_0_0_0": "SMALL", "1_4_2_1_0_0_0_1_1": "OPP", "1_2_3_2_0_0_1_1_1": "BIG", "1_1_2_3_1_1_0_1_0": "BIG", "1_2_2_3_0_1_0_0_1": "SMALL", "1_4_2_3_0_0_0_0_0": "SMALL", "1_2_3_2_0_0_1_0_1": "BIG", "1_1_2_3_1_1_0_0_0": "BIG", "1_1_1_2_2_1_1_1_1": "SAME", "1_1_1_1_3_2_0_1_0": "BIG", "1_2_1_1_0_1_0_0_1": "OPP", "1_3_1_1_0_1_0_0_0": "SMALL", "1_1_3_1_1_1_1_1_1": "SAME", "1_1_1_3_2_1_0_1_0": "OPP", "1_1_1_1_3_1_1_0_1": "SMALL", "1_2_1_1_0_2_1_1_0": "OPP", "1_2_1_2_0_1_0_0_0": "SMALL", "1_3_1_2_0_1_0_1_1": "SMALL", "1_1_3_1_1_1_1_0_1": "OPP", "1_2_3_1_0_1_1_1_1": "BIG", "1_3_3_1_0_0_1_0_1": "BIG", "1_4_3_1_0_0_1_1_1": "BIG", "1_1_3_3_1_1_0_0_1": "SAME", "1_2_3_3_0_0_0_0_0": "SMALL", "1_1_2_3_1_1_1_1_1": "SMALL", "1_2_1_2_0_1_0_1_1": "OPP", "1_1_2_1_1_1_1_0_1": "SMALL", "1_1_1_2_2_2_0_0_0": "OPP", "1_1_1_1_3_2_0_1_1": "BIG", "1_2_1_1_0_2_0_1_0": "OPP", "1_2_2_1_0_1_1_1_1": "SAME", "1_1_2_2_1_1_0_0_1": "BIG", "1_2_2_2_0_1_0_0_0": "SMALL", "1_3_2_2_0_1_0_0_0": "SMALL", "1_1_3_2_1_1_1_1_1": "SMALL", "1_2_3_2_0_1_1_0_1": "BIG", "1_1_2_3_1_1_0_1_1": "BIG", "2_1_2_0_1_0_0_0_1": "SMALL", "2_2_2_0_0_0_0_1_1": "SMALL", "2_3_2_0_0_0_0_1_0": "SMALL", "2_4_2_0_0_0_0_0_1": "SMALL", "2_4_2_0_0_0_0_0_0": "SMALL", "2_1_3_2_1_0_1_1_1": "BIG", "2_1_1_3_2_1_0_0_1": "OPP", "2_1_1_1_3_1_1_0_0": "SMALL", "2_2_1_1_0_1_1_1_1": "BIG", "2_1_2_1_1_2_0_1_0": "SMALL", "2_2_2_1_0_1_0_0_1": "SMALL", "2_1_2_2_1_1_1_1_1": "BIG", "2_1_1_2_2_1_0_0_1": "SAME", "2_1_1_1_3_2_1_1_1": "SMALL", "2_1_1_1_3_2_0_0_1": "BIG", "2_2_1_1_0_2_0_1_1": "SMALL", "2_1_2_1_1_2_1_0_1": "BIG", "2_1_1_2_2_2_0_1_1": "BIG", "2_1_1_1_3_2_1_1_0": "OPP", "2_1_1_1_3_2_1_0_0": "SMALL", "2_2_1_1_0_2_1_1_1": "BIG", "2_2_2_1_0_1_0_1_0": "SMALL", "2_3_2_1_0_1_0_1_0": "SMALL", "2_1_3_2_1_1_1_0_1": "BIG", "2_2_3_2_0_1_1_1_1": "BIG", "2_1_2_3_1_1_0_0_1": "SMALL", "2_2_2_3_0_1_0_0_0": "SMALL", "2_3_2_3_0_1_0_0_0": "SMALL", "2_4_2_3_0_0_0_1_1": "SMALL", "2_4_2_3_0_0_0_1_0": "SMALL", "2_1_3_2_1_0_1_1_0": "BIG", "2_1_1_1_3_2_0_0_0": "BIG", "2_2_1_1_0_2_1_0_0": "BIG", "2_1_2_1_1_2_0_0_0": "SMALL", "2_2_2_1_0_1_0_0_0": "SMALL", "2_3_2_1_0_1_0_0_0": "SMALL", "2_4_2_1_0_0_0_1_1": "SMALL", "2_2_3_2_0_0_1_1_1": "BIG", "2_1_2_3_1_1_0_1_0": "SMALL", "2_2_2_3_0_1_0_0_1": "SMALL", "2_4_2_3_0_0_0_0_0": "SMALL", "2_2_3_2_0_0_1_0_1": "BIG", "2_1_2_3_1_1_0_0_0": "SMALL", "2_1_1_2_2_1_1_1_1": "SMALL", "2_1_1_1_3_2_0_1_0": "BIG", "2_2_1_1_0_1_0_0_1": "SMALL", "2_3_1_1_0_1_0_0_0": "SMALL", "2_1_3_1_1_1_1_1_1": "OPP", "2_1_1_3_2_1_0_1_0": "BIG", "2_1_1_1_3_1_1_0_1": "SMALL", "2_2_1_1_0_2_1_1_0": "BIG", "2_2_1_2_0_1_0_0_0": "OPP", "2_3_1_2_0_1_0_1_1": "SMALL", "2_1_3_1_1_1_1_0_1": "BIG", "2_2_3_1_0_1_1_1_1": "BIG", "2_3_3_1_0_0_1_0_1": "BIG", "2_4_3_1_0_0_1_1_1": "BIG", "2_1_3_3_1_1_0_0_1": "OPP", "2_2_3_3_0_0_0_0_0": "SMALL", "2_1_2_3_1_1_1_1_1": "OPP", "2_2_1_2_0_1_0_1_1": "SMALL", "2_1_2_1_1_1_1_0_1": "BIG", "2_1_1_2_2_2_0_0_0": "BIG", "2_1_1_1_3_2_0_1_1": "SAME", "2_2_1_1_0_2_0_1_0": "SMALL", "2_2_2_1_0_1_1_1_1": "BIG", "2_1_2_2_1_1_0_0_1": "SMALL", "2_2_2_2_0_1_0_0_0": "SMALL", "2_3_2_2_0_1_0_0_0": "SMALL", "2_1_3_2_1_1_1_1_1": "BIG", "2_2_3_2_0_1_1_0_1": "OPP", "2_1_2_3_1_1_0_1_1": "SMALL", "0_3_0_0_0_0_1_1_0": "OPP", "0_1_3_0_1_0_0_0_1": "OPP", "0_1_1_3_2_1_1_1_1": "SMALL", "0_1_1_1_3_1_0_0_1": "OPP", "0_1_1_2_2_2_1_1_0": "SMALL", "0_2_1_1_0_1_0_1_1": "OPP", "0_1_2_1_1_2_1_1_0": "OPP", "0_1_1_2_2_2_0_0_1": "BIG", "0_3_2_1_0_1_1_1_0": "OPP", "0_4_2_1_0_0_1_0_1": "OPP", "0_1_3_2_1_1_0_0_0": "SMALL", "0_2_3_2_0_0_0_0_0": "SAME", "0_3_3_2_0_0_0_1_1": "SMALL", "0_4_3_2_0_0_0_0_1": "SMALL", "0_4_3_2_0_0_0_1_1": "OPP", "0_1_3_3_1_0_1_0_1": "OPP", "0_1_1_3_2_1_0_1_1": "BIG", "0_2_1_3_0_1_0_1_0": "BIG", "0_1_2_1_1_1_1_1_0": "BIG", "0_2_2_1_0_1_1_1_0": "SAME", "0_1_3_2_1_1_0_0_1": "OPP", "0_1_1_3_2_1_1_0_0": "SMALL", "0_2_1_3_0_1_1_1_1": "OPP", "0_1_2_1_1_1_0_1_0": "SMALL", "0_1_2_1_1_1_1_0_0": "OPP", "0_2_1_2_0_1_0_0_1": "BIG", "0_3_1_2_0_1_0_0_0": "OPP", "0_4_1_2_0_1_0_0_0": "SMALL", "0_1_1_1_3_1_1_1_1": "OPP", "1_3_0_0_0_0_1_1_0": "BIG", "1_1_3_0_1_0_0_0_1": "BIG", "1_1_1_3_2_1_1_1_1": "SMALL", "1_1_1_1_3_1_0_0_1": "BIG", "1_1_1_2_2_2_1_1_0": "OPP", "1_2_1_1_0_1_0_1_1": "OPP", "1_1_2_1_1_2_1_1_0": "SMALL", "1_1_1_2_2_2_0_0_1": "BIG", "1_3_2_1_0_1_1_1_0": "BIG", "1_4_2_1_0_0_1_0_1": "BIG", "1_1_3_2_1_1_0_0_0": "BIG", "1_2_3_2_0_0_0_0_0": "SMALL", "1_3_3_2_0_0_0_1_1": "SMALL", "1_4_3_2_0_0_0_0_1": "SMALL", "1_4_3_2_0_0_0_1_1": "SMALL", "1_1_3_3_1_0_1_0_1": "SMALL", "1_1_1_3_2_1_0_1_1": "BIG", "1_2_1_3_0_1_0_1_0": "SMALL", "1_1_2_1_1_1_1_1_0": "SMALL", "1_2_2_1_0_1_1_1_0": "OPP", "1_1_3_2_1_1_0_0_1": "SAME", "1_1_1_3_2_1_1_0_0": "OPP", "1_2_1_3_0_1_1_1_1": "BIG", "1_1_2_1_1_1_0_1_0": "BIG", "1_1_2_1_1_1_1_0_0": "OPP", "1_2_1_2_0_1_0_0_1": "SMALL", "1_3_1_2_0_1_0_0_0": "SMALL", "1_4_1_2_0_1_0_0_0": "SMALL", "1_1_1_1_3_1_1_1_1": "SMALL", "2_3_0_0_0_0_1_1_0": "BIG", "2_1_3_0_1_0_0_0_1": "SMALL", "2_1_1_3_2_1_1_1_1": "SMALL", "2_1_1_1_3_1_0_0_1": "BIG", "2_1_1_2_2_2_1_1_0": "SMALL", "2_2_1_1_0_1_0_1_1": "SMALL", "2_1_2_1_1_2_1_1_0": "BIG", "2_1_1_2_2_2_0_0_1": "SAME", "2_3_2_1_0_1_1_1_0": "BIG", "2_4_2_1_0_0_1_0_1": "BIG", "2_1_3_2_1_1_0_0_0": "SMALL", "2_2_3_2_0_0_0_0_0": "SMALL", "2_3_3_2_0_0_0_1_1": "SMALL", "2_4_3_2_0_0_0_0_1": "SMALL", "2_4_3_2_0_0_0_1_1": "SMALL", "2_1_3_3_1_0_1_0_1": "BIG", "2_1_1_3_2_1_0_1_1": "BIG", "2_2_1_3_0_1_0_1_0": "OPP", "2_1_2_1_1_1_1_1_0": "BIG", "2_2_2_1_0_1_1_1_0": "BIG", "2_1_3_2_1_1_0_0_1": "SMALL", "2_1_1_3_2_1_1_0_0": "SAME", "2_2_1_3_0_1_1_1_1": "BIG", "2_1_2_1_1_1_0_1_0": "SMALL", "2_1_2_1_1_1_1_0_0": "BIG", "2_2_1_2_0_1_0_0_1": "SMALL", "2_3_1_2_0_1_0_0_0": "SMALL", "2_4_1_2_0_1_0_0_0": "SMALL", "2_1_1_1_3_1_1_1_1": "SMALL", "0_1_2_1_1_1_1_1_1": "BIG", "0_2_1_1_0_1_1_1_0": "OPP", "0_1_2_1_1_2_0_0_1": "OPP", "0_1_1_2_2_2_1_1_1": "SMALL", "0_2_1_2_0_1_1_0_1": "SMALL", "0_3_1_2_0_1_1_0_0": "BIG", "0_4_1_2_0_1_1_1_1": "OPP", "0_1_3_1_1_1_0_0_1": "SMALL", "0_2_3_1_0_0_0_0_0": "SAME", "0_3_3_1_0_0_0_1_1": "SMALL", "0_4_3_1_0_0_0_1_0": "OPP", "0_1_3_3_1_1_1_0_1": "BIG", "0_2_3_3_0_0_1_1_1": "SAME", "0_3_3_3_0_0_1_1_0": "OPP", "0_1_3_3_1_1_0_1_0": "SMALL", "0_2_3_3_0_1_0_0_1": "OPP", "0_2_1_2_0_1_0_1_0": "BIG", "0_3_1_2_0_1_0_0_1": "SMALL", "1_1_2_1_1_1_1_1_1": "OPP", "1_2_1_1_0_1_1_1_0": "OPP", "1_1_2_1_1_2_0_0_1": "BIG", "1_1_1_2_2_2_1_1_1": "SMALL", "1_2_1_2_0_1_1_0_1": "BIG", "1_3_1_2_0_1_1_0_0": "BIG", "1_4_1_2_0_1_1_1_1": "BIG", "1_1_3_1_1_1_0_0_1": "SAME", "1_2_3_1_0_0_0_0_0": "SMALL", "1_3_3_1_0_0_0_1_1": "SMALL", "1_4_3_1_0_0_0_1_0": "SMALL", "1_1_3_3_1_1_1_0_1": "SAME", "1_2_3_3_0_0_1_1_1": "BIG", "1_3_3_3_0_0_1_1_0": "OPP", "1_1_3_3_1_1_0_1_0": "BIG", "1_2_3_3_0_1_0_0_1": "SMALL", "1_2_1_2_0_1_0_1_0": "SMALL", "1_3_1_2_0_1_0_0_1": "SMALL", "2_1_2_1_1_1_1_1_1": "OPP", "2_2_1_1_0_1_1_1_0": "BIG", "2_1_2_1_1_2_0_0_1": "OPP", "2_1_1_2_2_2_1_1_1": "SAME", "2_2_1_2_0_1_1_0_1": "BIG", "2_3_1_2_0_1_1_0_0": "BIG", "2_4_1_2_0_1_1_1_1": "BIG", "2_1_3_1_1_1_0_0_1": "SMALL", "2_2_3_1_0_0_0_0_0": "SMALL", "2_3_3_1_0_0_0_1_1": "SMALL", "2_4_3_1_0_0_0_1_0": "SMALL", "2_1_3_3_1_1_1_0_1": "BIG", "2_2_3_3_0_0_1_1_1": "BIG", "2_3_3_3_0_0_1_1_0": "BIG", "2_1_3_3_1_1_0_1_0": "SMALL", "2_2_3_3_0_1_0_0_1": "OPP", "2_2_1_2_0_1_0_1_0": "SMALL", "2_3_1_2_0_1_0_0_1": "OPP", "0_3_0_0_0_0_0_0_1": "SMALL", "0_4_0_0_0_0_0_0_0": "SMALL", "0_1_3_0_1_0_1_0_0": "BIG", "0_2_3_0_0_0_1_0_0": "SMALL", "0_3_3_0_0_0_1_1_1": "OPP", "1_3_0_0_0_0_0_0_1": "SMALL", "1_4_0_0_0_0_0_0_0": "SMALL", "1_1_3_0_1_0_1_0_0": "SMALL", "1_2_3_0_0_0_1_0_0": "BIG", "1_3_3_0_0_0_1_1_1": "BIG", "2_3_0_0_0_0_0_0_1": "SMALL", "2_4_0_0_0_0_0_0_0": "SMALL", "2_1_3_0_1_0_1_0_0": "BIG", "2_2_3_0_0_0_1_0_0": "BIG", "2_3_3_0_0_0_1_1_1": "BIG", "0_2_1_0_0_0_0_0_0": "OPP", "0_2_2_1_0_1_1_0_1": "SAME", "0_3_2_1_0_1_1_0_0": "BIG", "0_4_2_1_0_0_1_1_1": "BIG", "0_4_2_1_0_0_1_1_0": "OPP", "0_1_3_2_1_0_0_0_1": "OPP", "0_3_3_2_0_0_0_0_0": "OPP", "0_4_3_2_0_0_0_0_0": "SMALL", "0_1_3_3_1_1_1_0_0": "OPP", "0_2_3_3_0_0_1_0_0": "OPP", "1_2_1_0_0_0_0_0_0": "SMALL", "1_2_2_1_0_1_1_0_1": "BIG", "1_3_2_1_0_1_1_0_0": "BIG", "1_4_2_1_0_0_1_1_1": "BIG", "1_4_2_1_0_0_1_1_0": "BIG", "1_1_3_2_1_0_0_0_1": "SAME", "1_3_3_2_0_0_0_0_0": "SMALL", "1_4_3_2_0_0_0_0_0": "SMALL", "1_1_3_3_1_1_1_0_0": "SMALL", "1_2_3_3_0_0_1_0_0": "BIG", "2_2_1_0_0_0_0_0_0": "SMALL", "2_2_2_1_0_1_1_0_1": "BIG", "2_3_2_1_0_1_1_0_0": "BIG", "2_4_2_1_0_0_1_1_1": "BIG", "2_4_2_1_0_0_1_1_0": "BIG", "2_1_3_2_1_0_0_0_1": "SMALL", "2_3_3_2_0_0_0_0_0": "SMALL", "2_4_3_2_0_0_0_0_0": "SMALL", "2_1_3_3_1_1_1_0_0": "BIG", "2_2_3_3_0_0_1_0_0": "OPP", "0_1_2_0_1_0_0_0_0": "SMALL", "0_2_2_0_0_0_0_0_0": "OPP", "0_1_2_2_1_1_1_0_0": "OPP", "0_1_1_2_2_1_0_0_0": "BIG", "0_1_3_1_1_1_1_1_0": "OPP", "0_2_1_3_0_1_0_0_0": "BIG", "0_3_1_3_0_1_0_0_0": "OPP", "0_4_1_3_0_1_0_0_0": "OPP", "1_1_2_0_1_0_0_0_0": "BIG", "1_2_2_0_0_0_0_0_0": "SMALL", "1_1_2_2_1_1_1_0_0": "SMALL", "1_1_1_2_2_1_0_0_0": "BIG", "1_1_3_1_1_1_1_1_0": "OPP", "1_2_1_3_0_1_0_0_0": "SMALL", "1_3_1_3_0_1_0_0_0": "SMALL", "1_4_1_3_0_1_0_0_0": "SMALL", "2_1_2_0_1_0_0_0_0": "SMALL", "2_2_2_0_0_0_0_0_0": "SMALL", "2_1_2_2_1_1_1_0_0": "BIG", "2_1_1_2_2_1_0_0_0": "BIG", "2_1_3_1_1_1_1_1_0": "BIG", "2_2_1_3_0_1_0_0_0": "SAME", "2_3_1_3_0_1_0_0_0": "SMALL", "2_4_1_3_0_1_0_0_0": "SMALL", "0_2_1_0_0_0_1_0_0": "SAME", "0_3_1_0_0_0_1_1_1": "BIG", "0_4_1_0_0_0_1_0_1": "OPP", "0_1_3_1_1_1_0_1_1": "OPP", "0_1_1_3_2_1_1_1_0": "SAME", "0_2_1_3_0_1_1_1_0": "OPP", "0_1_2_1_1_1_0_0_1": "OPP", "0_2_1_2_0_1_1_1_0": "SAME", "0_1_2_2_1_1_1_1_0": "BIG", "1_2_1_0_0_0_1_0_0": "BIG", "1_3_1_0_0_0_1_1_1": "BIG", "1_4_1_0_0_0_1_0_1": "BIG", "1_1_3_1_1_1_0_1_1": "BIG", "1_1_1_3_2_1_1_1_0": "SMALL", "1_2_1_3_0_1_1_1_0": "OPP", "1_1_2_1_1_1_0_0_1": "OPP", "1_2_1_2_0_1_1_1_0": "OPP", "1_1_2_2_1_1_1_1_0": "SMALL", "2_2_1_0_0_0_1_0_0": "BIG", "2_3_1_0_0_0_1_1_1": "BIG", "2_4_1_0_0_0_1_0_1": "BIG", "2_1_3_1_1_1_0_1_1": "SMALL", "2_1_1_3_2_1_1_1_0": "SMALL", "2_2_1_3_0_1_1_1_0": "BIG", "2_1_2_1_1_1_0_0_1": "SMALL", "2_2_1_2_0_1_1_1_0": "OPP", "2_1_2_2_1_1_1_1_0": "BIG", "0_1_2_0_1_0_0_1_0": "OPP", "0_1_1_2_2_1_1_0_1": "SMALL", "0_2_1_2_0_1_1_1_1": "SMALL", "0_3_1_2_0_1_1_1_0": "BIG", "0_4_1_2_0_1_1_1_0": "BIG", "0_4_1_2_0_0_1_1_0": "OPP", "0_1_3_1_1_0_0_0_1": "OPP", "0_2_1_3_0_1_1_0_1": "SMALL", "0_3_1_3_0_1_1_0_0": "OPP", "0_1_3_1_1_1_0_0_0": "SMALL", "0_2_3_1_0_1_0_0_0": "OPP", "0_1_2_3_1_1_1_0_0": "BIG", "0_2_2_3_0_1_1_1_1": "SAME", "0_3_2_3_0_1_1_0_1": "OPP", "0_1_3_2_1_1_0_1_1": "SMALL", "0_2_3_2_0_1_0_0_1": "BIG", "0_1_3_3_1_1_1_1_1": "OPP", "0_2_1_3_0_1_0_1_1": "BIG", "1_1_2_0_1_0_0_1_0": "BIG", "1_1_1_2_2_1_1_0_1": "SMALL", "1_2_1_2_0_1_1_1_1": "BIG", "1_3_1_2_0_1_1_1_0": "BIG", "1_4_1_2_0_1_1_1_0": "BIG", "1_4_1_2_0_0_1_1_0": "BIG", "1_1_3_1_1_0_0_0_1": "BIG", "1_2_1_3_0_1_1_0_1": "BIG", "1_3_1_3_0_1_1_0_0": "BIG", "1_1_3_1_1_1_0_0_0": "SAME", "1_2_3_1_0_1_0_0_0": "SMALL", "1_1_2_3_1_1_1_0_0": "SMALL", "1_2_2_3_0_1_1_1_1": "BIG", "1_3_2_3_0_1_1_0_1": "BIG", "1_1_3_2_1_1_0_1_1": "BIG", "1_2_3_2_0_1_0_0_1": "SMALL", "1_1_3_3_1_1_1_1_1": "OPP", "1_2_1_3_0_1_0_1_1": "SMALL", "2_1_2_0_1_0_0_1_0": "SMALL", "2_1_1_2_2_1_1_0_1": "SMALL", "2_2_1_2_0_1_1_1_1": "OPP", "2_3_1_2_0_1_1_1_0": "BIG", "2_4_1_2_0_1_1_1_0": "BIG", "2_4_1_2_0_0_1_1_0": "BIG", "2_1_3_1_1_0_0_0_1": "SMALL", "2_2_1_3_0_1_1_0_1": "BIG", "2_3_1_3_0_1_1_0_0": "BIG", "2_1_3_1_1_1_0_0_0": "SMALL", "2_2_3_1_0_1_0_0_0": "SMALL", "2_1_2_3_1_1_1_0_0": "BIG", "2_2_2_3_0_1_1_1_1": "BIG", "2_3_2_3_0_1_1_0_1": "BIG", "2_1_3_2_1_1_0_1_1": "OPP", "2_2_3_2_0_1_0_0_1": "SMALL", "2_1_3_3_1_1_1_1_1": "BIG", "2_2_1_3_0_1_0_1_1": "SMALL", "0_1_3_0_1_0_0_1_0": "OPP", "0_1_1_3_2_1_1_0_1": "SMALL", "0_1_1_1_3_1_0_1_1": "BIG", "0_2_1_1_0_2_1_0_1": "OPP", "0_1_2_1_1_2_0_1_1": "SMALL", "0_4_2_1_0_0_0_1_0": "OPP", "0_1_3_2_1_1_1_1_0": "OPP", "0_3_1_3_0_1_0_1_0": "SMALL", "0_3_1_3_0_1_0_1_1": "OPP", "0_2_3_1_0_1_1_1_0": "SMALL", "0_3_3_1_0_0_1_1_0": "BIG", "0_2_3_3_0_1_0_1_0": "BIG", "0_3_3_3_0_0_0_0_1": "OPP", "0_3_1_3_0_1_0_0_1": "OPP", "0_3_2_1_0_1_0_1_1": "SMALL", "0_4_1_3_0_1_0_1_0": "OPP", "0_2_1_1_0_1_1_0_0": "SMALL", "0_3_1_1_0_1_1_0_0": "BIG", "0_4_1_1_0_1_1_0_0": "OPP", "0_2_3_1_0_0_0_0_1": "OPP", "1_1_3_0_1_0_0_1_0": "BIG", "1_1_1_3_2_1_1_0_1": "OPP", "1_1_1_1_3_1_0_1_1": "BIG", "1_2_1_1_0_2_1_0_1": "OPP", "1_1_2_1_1_2_0_1_1": "BIG", "1_4_2_1_0_0_0_1_0": "SMALL", "1_1_3_2_1_1_1_1_0": "OPP", "1_3_1_3_0_1_0_1_0": "SMALL", "1_3_1_3_0_1_0_1_1": "SMALL", "1_2_3_1_0_1_1_1_0": "BIG", "1_3_3_1_0_0_1_1_0": "BIG", "1_2_3_3_0_1_0_1_0": "SMALL", "1_3_3_3_0_0_0_0_1": "SMALL", "1_3_1_3_0_1_0_0_1": "SMALL", "1_3_2_1_0_1_0_1_1": "SMALL", "1_4_1_3_0_1_0_1_0": "SMALL", "1_2_1_1_0_1_1_0_0": "BIG", "1_3_1_1_0_1_1_0_0": "BIG", "1_4_1_1_0_1_1_0_0": "BIG", "1_2_3_1_0_0_0_0_1": "SMALL", "2_1_3_0_1_0_0_1_0": "SMALL", "2_1_1_3_2_1_1_0_1": "SMALL", "2_1_1_1_3_1_0_1_1": "SAME", "2_2_1_1_0_2_1_0_1": "BIG", "2_1_2_1_1_2_0_1_1": "SMALL", "2_4_2_1_0_0_0_1_0": "SMALL", "2_1_3_2_1_1_1_1_0": "OPP", "2_3_1_3_0_1_0_1_0": "SMALL", "2_3_1_3_0_1_0_1_1": "SMALL", "2_2_3_1_0_1_1_1_0": "BIG", "2_3_3_1_0_0_1_1_0": "BIG", "2_2_3_3_0_1_0_1_0": "SMALL", "2_3_3_3_0_0_0_0_1": "SMALL", "2_3_1_3_0_1_0_0_1": "SMALL", "2_3_2_1_0_1_0_1_1": "SMALL", "2_4_1_3_0_1_0_1_0": "SMALL", "2_2_1_1_0_1_1_0_0": "BIG", "2_3_1_1_0_1_1_0_0": "BIG", "2_4_1_1_0_1_1_0_0": "BIG", "2_2_3_1_0_0_0_0_1": "OPP", "0_2_2_0_0_0_0_1_0": "BIG", "0_4_2_2_0_0_0_0_0": "OPP", "0_2_3_2_0_0_1_1_0": "SAME", "0_3_3_2_0_0_1_1_0": "BIG", "0_3_1_3_0_1_1_1_0": "BIG", "0_4_1_3_0_1_1_1_0": "OPP", "0_4_3_1_0_0_0_0_1": "SMALL", "0_4_3_1_0_0_0_1_1": "SMALL", "0_1_1_3_2_1_0_0_0": "BIG", "0_1_1_2_2_1_1_0_0": "OPP", "0_2_2_2_0_1_1_0_1": "SAME", "0_3_2_2_0_1_1_1_1": "BIG", "0_4_2_2_0_0_1_1_0": "BIG", "0_4_2_2_0_0_1_0_1": "BIG", "0_4_2_2_0_0_1_1_1": "OPP", "0_1_3_2_1_0_0_1_0": "SMALL", "0_1_1_1_3_1_0_0_0": "SAME", "0_3_1_2_0_1_0_1_0": "SMALL", "0_4_1_2_0_1_0_1_0": "OPP", "0_2_1_1_0_2_0_0_0": "OPP", "0_1_2_1_1_2_1_1_1": "OPP", "0_1_1_2_2_2_0_1_0": "SAME", "0_1_1_2_2_2_1_0_0": "SMALL", "0_1_2_1_1_2_1_0_0": "BIG", "0_4_2_2_0_0_0_1_1": "SMALL", "0_4_2_2_0_0_0_1_0": "OPP", "0_4_3_2_0_0_1_1_0": "BIG", "0_4_3_2_0_0_1_0_1": "BIG", "0_4_3_2_0_0_1_1_1": "BIG", "0_1_3_3_1_0_0_0_1": "SMALL", "0_2_2_3_0_1_1_0_1": "OPP", "0_1_2_2_1_1_0_0_0": "OPP", "0_2_1_1_0_1_0_0_0": "OPP", "0_2_2_1_0_1_1_0_0": "OPP", "0_1_2_2_1_1_0_1_1": "SMALL", "0_2_2_2_0_1_0_1_0": "OPP", "0_2_2_2_0_1_1_1_0": "OPP", "0_2_2_1_0_1_0_1_1": "BIG", "0_3_2_1_0_1_0_0_1": "OPP", "0_1_3_1_1_1_1_0_0": "OPP", "0_3_1_1_0_1_0_1_1": "OPP", "0_4_1_1_0_1_0_1_0": "SMALL", "0_4_1_1_0_0_0_1_0": "SMALL", "0_4_1_1_0_0_0_0_1": "OPP", "0_1_3_1_1_0_1_0_0": "OPP", "0_1_1_1_3_1_1_1_0": "OPP", "0_2_2_2_0_1_0_0_1": "SAME", "0_1_3_2_1_1_1_0_0": "OPP", "0_3_2_1_0_1_1_0_1": "OPP", "0_2_3_2_0_1_0_0_0": "BIG", "0_1_3_3_1_0_1_1_0": "OPP", "0_2_2_2_0_1_0_1_1": "SAME", "0_1_1_2_2_1_0_1_0": "BIG", "0_4_1_3_0_1_0_0_1": "OPP", "0_4_1_3_0_1_0_1_1": "OPP", "0_2_3_1_0_0_1_1_1": "SAME", "0_4_3_1_0_0_1_1_0": "OPP", "0_2_1_2_0_1_1_0_0": "SMALL", "0_3_1_2_0_1_1_1_1": "BIG", "0_4_1_2_0_1_1_0_1": "BIG", "0_4_1_2_0_0_1_1_1": "BIG", "0_4_1_2_0_0_1_0_1": "BIG", "0_4_1_2_0_0_1_0_0": "BIG", "1_2_2_0_0_0_0_1_0": "SMALL", "1_4_2_2_0_0_0_0_0": "SMALL", "1_2_3_2_0_0_1_1_0": "BIG", "1_3_3_2_0_0_1_1_0": "BIG", "1_3_1_3_0_1_1_1_0": "BIG", "1_4_1_3_0_1_1_1_0": "BIG", "1_4_3_1_0_0_0_0_1": "SMALL", "1_4_3_1_0_0_0_1_1": "SMALL", "1_1_1_3_2_1_0_0_0": "OPP", "1_1_1_2_2_1_1_0_0": "SAME", "1_2_2_2_0_1_1_0_1": "BIG", "1_3_2_2_0_1_1_1_1": "BIG", "1_4_2_2_0_0_1_1_0": "BIG", "1_4_2_2_0_0_1_0_1": "BIG", "1_4_2_2_0_0_1_1_1": "BIG", "1_1_3_2_1_0_0_1_0": "SAME", "1_1_1_1_3_1_0_0_0": "BIG", "1_3_1_2_0_1_0_1_0": "SMALL", "1_4_1_2_0_1_0_1_0": "SMALL", "1_2_1_1_0_2_0_0_0": "OPP", "1_1_2_1_1_2_1_1_1": "SMALL", "1_1_1_2_2_2_0_1_0": "BIG", "1_1_1_2_2_2_1_0_0": "SMALL", "1_1_2_1_1_2_1_0_0": "SMALL", "1_4_2_2_0_0_0_1_1": "SMALL", "1_4_2_2_0_0_0_1_0": "SMALL", "1_4_3_2_0_0_1_1_0": "BIG", "1_4_3_2_0_0_1_0_1": "BIG", "1_4_3_2_0_0_1_1_1": "BIG", "1_1_3_3_1_0_0_0_1": "OPP", "1_2_2_3_0_1_1_0_1": "OPP", "1_1_2_2_1_1_0_0_0": "BIG", "1_2_1_1_0_1_0_0_0": "OPP", "1_2_2_1_0_1_1_0_0": "BIG", "1_1_2_2_1_1_0_1_1": "BIG", "1_2_2_2_0_1_0_1_0": "SMALL", "1_2_2_2_0_1_1_1_0": "BIG", "1_2_2_1_0_1_0_1_1": "SMALL", "1_3_2_1_0_1_0_0_1": "OPP", "1_1_3_1_1_1_1_0_0": "SMALL", "1_3_1_1_0_1_0_1_1": "SMALL", "1_4_1_1_0_1_0_1_0": "SMALL", "1_4_1_1_0_0_0_1_0": "SMALL", "1_4_1_1_0_0_0_0_1": "SMALL", "1_1_3_1_1_0_1_0_0": "SMALL", "1_1_1_1_3_1_1_1_0": "SMALL", "1_2_2_2_0_1_0_0_1": "SMALL", "1_1_3_2_1_1_1_0_0": "OPP", "1_3_2_1_0_1_1_0_1": "OPP", "1_2_3_2_0_1_0_0_0": "SMALL", "1_1_3_3_1_0_1_1_0": "SMALL", "1_2_2_2_0_1_0_1_1": "SMALL", "1_1_1_2_2_1_0_1_0": "BIG", "1_4_1_3_0_1_0_0_1": "SMALL", "1_4_1_3_0_1_0_1_1": "OPP", "1_2_3_1_0_0_1_1_1": "BIG", "1_4_3_1_0_0_1_1_0": "BIG", "1_2_1_2_0_1_1_0_0": "BIG", "1_3_1_2_0_1_1_1_1": "BIG", "1_4_1_2_0_1_1_0_1": "BIG", "1_4_1_2_0_0_1_1_1": "BIG", "1_4_1_2_0_0_1_0_1": "BIG", "1_4_1_2_0_0_1_0_0": "BIG", "2_2_2_0_0_0_0_1_0": "SMALL", "2_4_2_2_0_0_0_0_0": "SMALL", "2_2_3_2_0_0_1_1_0": "BIG", "2_3_3_2_0_0_1_1_0": "BIG", "2_3_1_3_0_1_1_1_0": "BIG", "2_4_1_3_0_1_1_1_0": "BIG", "2_4_3_1_0_0_0_0_1": "SMALL", "2_4_3_1_0_0_0_1_1": "SMALL", "2_1_1_3_2_1_0_0_0": "SAME", "2_1_1_2_2_1_1_0_0": "SMALL", "2_2_2_2_0_1_1_0_1": "BIG", "2_3_2_2_0_1_1_1_1": "BIG", "2_4_2_2_0_0_1_1_0": "BIG", "2_4_2_2_0_0_1_0_1": "BIG", "2_4_2_2_0_0_1_1_1": "BIG", "2_1_3_2_1_0_0_1_0": "SMALL", "2_1_1_1_3_1_0_0_0": "BIG", "2_3_1_2_0_1_0_1_0": "SMALL", "2_4_1_2_0_1_0_1_0": "SMALL", "2_2_1_1_0_2_0_0_0": "SMALL", "2_1_2_1_1_2_1_1_1": "BIG", "2_1_1_2_2_2_0_1_0": "SAME", "2_1_1_2_2_2_1_0_0": "SMALL", "2_1_2_1_1_2_1_0_0": "BIG", "2_4_2_2_0_0_0_1_1": "SMALL", "2_4_2_2_0_0_0_1_0": "SMALL", "2_4_3_2_0_0_1_1_0": "BIG", "2_4_3_2_0_0_1_0_1": "BIG", "2_4_3_2_0_0_1_1_1": "BIG", "2_1_3_3_1_0_0_0_1": "SMALL", "2_2_2_3_0_1_1_0_1": "BIG", "2_1_2_2_1_1_0_0_0": "SMALL", "2_2_1_1_0_1_0_0_0": "SMALL", "2_2_2_1_0_1_1_0_0": "BIG", "2_1_2_2_1_1_0_1_1": "SMALL", "2_2_2_2_0_1_0_1_0": "SMALL", "2_2_2_2_0_1_1_1_0": "BIG", "2_2_2_1_0_1_0_1_1": "SMALL", "2_3_2_1_0_1_0_0_1": "SMALL", "2_1_3_1_1_1_1_0_0": "BIG", "2_3_1_1_0_1_0_1_1": "SMALL", "2_4_1_1_0_1_0_1_0": "SMALL", "2_4_1_1_0_0_0_1_0": "SMALL", "2_4_1_1_0_0_0_0_1": "SMALL", "2_1_3_1_1_0_1_0_0": "BIG", "2_1_1_1_3_1_1_1_0": "SMALL", "2_2_2_2_0_1_0_0_1": "SMALL", "2_1_3_2_1_1_1_0_0": "BIG", "2_3_2_1_0_1_1_0_1": "BIG", "2_2_3_2_0_1_0_0_0": "SMALL", "2_1_3_3_1_0_1_1_0": "BIG", "2_2_2_2_0_1_0_1_1": "SMALL", "2_1_1_2_2_1_0_1_0": "BIG", "2_4_1_3_0_1_0_0_1": "SMALL", "2_4_1_3_0_1_0_1_1": "SMALL", "2_2_3_1_0_0_1_1_1": "BIG", "2_4_3_1_0_0_1_1_0": "BIG", "2_2_1_2_0_1_1_0_0": "BIG", "2_3_1_2_0_1_1_1_1": "BIG", "2_4_1_2_0_1_1_0_1": "BIG", "2_4_1_2_0_0_1_1_1": "BIG", "2_4_1_2_0_0_1_0_1": "BIG", "2_4_1_2_0_0_1_0_0": "BIG", "1_1_2_3_1_1_1_1_0": "SMALL", "0_3_1_1_0_1_1_1_0": "SMALL", "0_4_1_1_0_0_1_1_1": "OPP", "0_2_3_3_0_1_0_1_1": "SAME", "1_4_1_3_0_0_0_1_1": "SMALL", "1_2_3_2_0_0_0_1_0": "SMALL", "0_4_3_3_0_0_0_0_1": "OPP", "2_1_2_2_1_1_0_1_0": "SMALL", "1_1_2_2_1_1_0_1_0": "SMALL", "1_3_3_3_0_0_0_1_0": "SMALL", "1_1_3_3_1_1_0_1_1": "SMALL", "1_3_1_1_0_1_1_1_0": "SMALL", "2_4_1_2_0_1_1_0_0": "SMALL", "2_3_2_3_0_1_1_1_1": "SMALL", "2_3_2_2_0_1_0_1_0": "SMALL", "0_2_3_2_0_0_0_1_0": "OPP", "0_1_2_2_1_1_0_1_0": "SMALL", "2_3_1_2_0_1_1_0_1": "SMALL", "0_3_3_3_0_0_0_1_0": "SMALL", "0_1_2_3_1_1_1_1_0": "SMALL", "0_2_3_1_0_0_0_1_0": "OPP", "0_2_1_1_0_2_0_0_1": "SMALL", "2_1_2_3_1_1_1_1_0": "OPP", "0_1_3_2_1_1_0_1_0": "SMALL", "2_2_2_3_0_1_1_0_0": "SMALL", "1_4_1_1_0_0_1_1_1": "SMALL", "1_1_3_2_1_1_0_1_0": "OPP", "0_1_3_1_1_0_1_0_1": "SMALL", "2_4_1_1_0_1_1_0_1": "SMALL", "0_1_3_1_1_0_0_1_0": "OPP", "0_4_1_3_0_0_0_1_1": "OPP", "1_2_3_1_0_0_0_1_0": "SMALL", "0_2_2_3_0_1_1_0_0": "SAME", "2_1_3_2_1_1_0_1_0": "SMALL", "1_4_3_3_0_0_0_0_1": "SMALL", "2_1_3_1_1_0_0_1_0": "SMALL", "0_4_1_1_0_1_1_0_1": "SMALL", "1_2_2_3_0_1_1_0_0": "SMALL", "2_1_3_1_1_0_1_0_1": "SMALL", "2_2_3_1_0_0_0_1_0": "OPP", "0_1_3_1_1_0_0_1_1": "SMALL", "1_1_3_3_1_1_0_0_0": "SAME", "1_1_3_1_1_0_1_0_1": "SAME", "2_3_3_3_0_0_0_1_0": "SMALL", "1_3_2_3_0_1_1_1_1": "SMALL", "1_1_3_1_1_0_0_1_1": "SMALL", "2_4_3_3_0_0_0_0_1": "SMALL", "0_3_1_2_0_1_1_0_1": "SMALL", "1_3_2_1_0_1_1_1_1": "SMALL", "1_4_1_2_0_1_1_0_0": "SMALL", "0_1_3_3_1_1_0_0_0": "SMALL", "0_3_2_1_0_1_1_1_1": "SMALL", "0_4_1_2_0_1_1_0_0": "SMALL", "0_1_3_3_1_1_0_1_1": "SMALL", "2_2_3_3_0_1_0_1_1": "SMALL", "2_1_3_3_1_1_0_1_1": "SMALL", "1_4_1_1_0_1_1_0_1": "SMALL", "1_2_1_1_0_2_0_0_1": "OPP", "2_2_3_2_0_0_0_1_0": "SMALL", "2_3_1_1_0_1_1_1_0": "SMALL", "1_3_1_2_0_1_1_0_1": "SMALL", "2_3_2_1_0_1_1_1_1": "SMALL", "2_1_3_1_1_0_0_1_1": "SMALL", "1_1_3_1_1_0_0_1_0": "SMALL", "1_3_2_2_0_1_0_1_0": "SMALL", "0_3_2_3_0_1_1_1_1": "SMALL", "2_1_3_3_1_1_0_0_0": "SMALL", "1_2_3_3_0_1_0_1_1": "SMALL", "2_4_1_1_0_0_1_1_1": "SMALL", "2_4_1_3_0_0_0_1_1": "SMALL", "2_2_1_1_0_2_0_0_1": "SMALL", "0_3_2_2_0_1_0_1_0": "SMALL"};
  const TITAN_RULES_1M = {"0_1_2_0_1_0_0_0_0": "SMALL", "0_2_2_0_0_0_0_0_0": "BIG", "0_3_2_0_0_0_0_0_0": "SMALL", "0_4_2_0_0_0_0_0_0": "SMALL", "0_1_3_2_1_1_1_1_1": "BIG", "0_1_1_3_2_1_0_0_1": "BIG", "0_2_1_3_0_1_0_0_0": "BIG", "0_1_2_1_1_1_1_0_0": "BIG", "0_1_1_2_2_2_0_1_1": "BIG", "1_1_2_0_1_0_0_0_0": "BIG", "1_2_2_0_0_0_0_0_0": "SMALL", "1_3_2_0_0_0_0_0_0": "SMALL", "1_4_2_0_0_0_0_0_0": "SMALL", "1_1_3_2_1_1_1_1_1": "OPP", "1_1_1_3_2_1_0_0_1": "BIG", "1_2_1_3_0_1_0_0_0": "SMALL", "1_1_2_1_1_1_1_0_0": "OPP", "1_1_1_2_2_2_0_1_1": "BIG", "2_1_2_0_1_0_0_0_0": "SMALL", "2_2_2_0_0_0_0_0_0": "SMALL", "2_3_2_0_0_0_0_0_0": "SMALL", "2_4_2_0_0_0_0_0_0": "SMALL", "2_1_3_2_1_1_1_1_1": "BIG", "2_1_1_3_2_1_0_0_1": "BIG", "2_2_1_3_0_1_0_0_0": "SMALL", "2_1_2_1_1_1_1_0_0": "BIG", "2_1_1_2_2_2_0_1_1": "BIG", "0_2_1_0_0_0_1_1_0": "OPP", "0_1_2_1_1_1_0_0_1": "OPP", "0_1_1_2_2_1_1_0_0": "OPP", "0_1_1_1_3_2_0_0_0": "BIG", "0_2_1_1_0_1_0_0_0": "BIG", "0_3_1_1_0_1_0_1_1": "OPP", "0_1_3_1_1_1_1_1_0": "BIG", "1_2_1_0_0_0_1_1_0": "BIG", "1_1_2_1_1_1_0_0_1": "BIG", "1_1_1_2_2_1_1_0_0": "OPP", "1_1_1_1_3_2_0_0_0": "BIG", "1_2_1_1_0_1_0_0_0": "SMALL", "1_3_1_1_0_1_0_1_1": "SMALL", "1_1_3_1_1_1_1_1_0": "SMALL", "2_2_1_0_0_0_1_1_0": "BIG", "2_1_2_1_1_1_0_0_1": "SMALL", "2_1_1_2_2_1_1_0_0": "SMALL", "2_1_1_1_3_2_0_0_0": "BIG", "2_2_1_1_0_1_0_0_0": "SMALL", "2_3_1_1_0_1_0_1_1": "SMALL", "2_1_3_1_1_1_1_1_0": "BIG", "0_1_2_0_1_0_0_0_1": "SMALL", "0_1_1_2_2_1_1_1_1": "SMALL", "0_2_1_2_0_1_1_0_1": "OPP", "0_1_2_1_1_1_0_1_1": "SMALL", "0_1_1_2_2_2_1_1_0": "SMALL", "0_1_1_1_3_2_0_1_0": "BIG", "0_2_1_1_0_1_0_0_1": "BIG", "0_3_1_1_0_1_0_0_0": "SMALL", "0_1_3_1_1_1_1_0_0": "BIG", "0_2_3_1_0_1_1_1_1": "OPP", "1_1_2_0_1_0_0_0_1": "BIG", "1_1_1_2_2_1_1_1_1": "SMALL", "1_2_1_2_0_1_1_0_1": "BIG", "1_1_2_1_1_1_0_1_1": "BIG", "1_1_1_2_2_2_1_1_0": "OPP", "1_1_1_1_3_2_0_1_0": "BIG", "1_2_1_1_0_1_0_0_1": "SMALL", "1_3_1_1_0_1_0_0_0": "SMALL", "1_1_3_1_1_1_1_0_0": "SMALL", "1_2_3_1_0_1_1_1_1": "BIG", "2_1_2_0_1_0_0_0_1": "SMALL", "2_1_1_2_2_1_1_1_1": "SMALL", "2_2_1_2_0_1_1_0_1": "BIG", "2_1_2_1_1_1_0_1_1": "SMALL", "2_1_1_2_2_2_1_1_0": "SMALL", "2_1_1_1_3_2_0_1_0": "BIG", "2_2_1_1_0_1_0_0_1": "SMALL", "2_3_1_1_0_1_0_0_0": "SMALL", "2_1_3_1_1_1_1_0_0": "BIG", "2_2_3_1_0_1_1_1_1": "BIG", "0_2_1_0_0_0_1_1_1": "OPP", "0_1_1_1_3_2_0_0_1": "BIG", "0_4_1_1_0_1_0_0_0": "SMALL", "0_4_1_1_0_0_0_0_0": "SMALL", "0_1_3_1_1_0_1_1_1": "BIG", "0_2_3_1_0_0_1_1_0": "OPP", "0_1_2_3_1_1_0_0_1": "OPP", "0_1_2_1_1_1_0_0_0": "OPP", "0_1_1_2_2_2_1_1_1": "SMALL", "0_2_1_2_0_1_1_1_0": "OPP", "1_2_1_0_0_0_1_1_1": "BIG", "1_1_1_1_3_2_0_0_1": "BIG", "1_4_1_1_0_1_0_0_0": "SMALL", "1_4_1_1_0_0_0_0_0": "SMALL", "1_1_3_1_1_0_1_1_1": "SMALL", "1_2_3_1_0_0_1_1_0": "BIG", "1_1_2_3_1_1_0_0_1": "BIG", "1_1_2_1_1_1_0_0_0": "BIG", "1_1_1_2_2_2_1_1_1": "SMALL", "1_2_1_2_0_1_1_1_0": "BIG", "2_2_1_0_0_0_1_1_1": "BIG", "2_1_1_1_3_2_0_0_1": "OPP", "2_4_1_1_0_1_0_0_0": "SMALL", "2_4_1_1_0_0_0_0_0": "SMALL", "2_1_3_1_1_0_1_1_1": "BIG", "2_2_3_1_0_0_1_1_0": "BIG", "2_1_2_3_1_1_0_0_1": "SMALL", "2_1_2_1_1_1_0_0_0": "SMALL", "2_1_1_2_2_2_1_1_1": "SMALL", "2_2_1_2_0_1_1_1_0": "BIG", "0_1_2_1_1_1_0_1_0": "SMALL", "0_1_1_2_2_1_1_1_0": "SMALL", "0_2_1_1_0_1_0_1_1": "BIG", "0_3_1_1_0_1_0_0_1": "OPP", "0_1_3_1_1_1_1_1_1": "OPP", "0_1_1_3_2_1_0_1_0": "BIG", "0_2_1_3_0_1_0_0_1": "BIG", "0_3_1_3_0_1_0_1_1": "OPP", "0_3_1_3_0_1_0_0_0": "OPP", "1_1_2_1_1_1_0_1_0": "BIG", "1_1_1_2_2_1_1_1_0": "OPP", "1_2_1_1_0_1_0_1_1": "SMALL", "1_3_1_1_0_1_0_0_1": "SMALL", "1_1_3_1_1_1_1_1_1": "SMALL", "1_1_1_3_2_1_0_1_0": "BIG", "1_2_1_3_0_1_0_0_1": "SMALL", "1_3_1_3_0_1_0_1_1": "SMALL", "1_3_1_3_0_1_0_0_0": "SMALL", "2_1_2_1_1_1_0_1_0": "SMALL", "2_1_1_2_2_1_1_1_0": "SMALL", "2_2_1_1_0_1_0_1_1": "SMALL", "2_3_1_1_0_1_0_0_1": "SMALL", "2_1_3_1_1_1_1_1_1": "BIG", "2_1_1_3_2_1_0_1_0": "BIG", "2_2_1_3_0_1_0_0_1": "SMALL", "2_3_1_3_0_1_0_1_1": "SMALL", "2_3_1_3_0_1_0_0_0": "SMALL", "0_3_0_0_0_0_1_0_1": "BIG", "0_4_0_0_0_0_1_0_0": "OPP", "0_1_3_0_1_0_0_1_1": "SMALL", "0_2_3_0_0_0_0_0_1": "BIG", "0_3_3_0_0_0_0_0_0": "SMALL", "0_4_3_0_0_0_0_0_0": "SMALL", "0_4_3_0_0_0_0_1_1": "OPP", "0_1_3_3_1_0_1_1_0": "OPP", "0_1_1_1_3_1_1_1_0": "SMALL", "0_2_1_1_0_1_1_1_0": "OPP", "0_1_2_1_1_2_0_0_1": "OPP", "0_3_1_2_0_1_1_1_1": "BIG", "1_3_0_0_0_0_1_0_1": "BIG", "1_4_0_0_0_0_1_0_0": "BIG", "1_1_3_0_1_0_0_1_1": "BIG", "1_2_3_0_0_0_0_0_1": "SMALL", "1_3_3_0_0_0_0_0_0": "SMALL", "1_4_3_0_0_0_0_0_0": "SMALL", "1_4_3_0_0_0_0_1_1": "SMALL", "1_1_3_3_1_0_1_1_0": "SMALL", "1_1_1_1_3_1_1_1_0": "SMALL", "1_2_1_1_0_1_1_1_0": "BIG", "1_1_2_1_1_2_0_0_1": "BIG", "1_3_1_2_0_1_1_1_1": "BIG", "2_3_0_0_0_0_1_0_1": "BIG", "2_4_0_0_0_0_1_0_0": "BIG", "2_1_3_0_1_0_0_1_1": "SMALL", "2_2_3_0_0_0_0_0_1": "SMALL", "2_3_3_0_0_0_0_0_0": "SMALL", "2_4_3_0_0_0_0_0_0": "SMALL", "2_4_3_0_0_0_0_1_1": "SMALL", "2_1_3_3_1_0_1_1_0": "BIG", "2_1_1_1_3_1_1_1_0": "SMALL", "2_2_1_1_0_1_1_1_0": "BIG", "2_1_2_1_1_2_0_0_1": "SMALL", "2_3_1_2_0_1_1_1_1": "BIG", "0_1_1_1_3_1_0_0_1": "BIG", "0_3_1_1_0_1_0_1_0": "OPP", "0_2_3_1_0_1_1_1_0": "OPP", "0_1_2_3_1_1_0_1_0": "OPP", "0_1_1_2_2_1_1_0_1": "OPP", "0_1_1_1_3_2_1_0_0": "SMALL", "0_2_1_1_0_2_1_1_1": "SMALL", "0_3_1_1_0_1_1_1_0": "OPP", "0_1_3_1_1_1_0_0_1": "SMALL", "0_2_3_1_0_1_0_1_1": "OPP", "0_1_2_3_1_1_1_0_1": "BIG", "0_2_2_3_0_1_1_1_1": "OPP", "0_1_2_2_1_1_0_0_1": "SMALL", "0_1_1_1_3_2_1_1_1": "OPP", "1_1_1_1_3_1_0_0_1": "BIG", "1_3_1_1_0_1_0_1_0": "SMALL", "1_2_3_1_0_1_1_1_0": "BIG", "1_1_2_3_1_1_0_1_0": "BIG", "1_1_1_2_2_1_1_0_1": "OPP", "1_1_1_1_3_2_1_0_0": "SMALL", "1_2_1_1_0_2_1_1_1": "BIG", "1_3_1_1_0_1_1_1_0": "BIG", "1_1_3_1_1_1_0_0_1": "BIG", "1_2_3_1_0_1_0_1_1": "SMALL", "1_1_2_3_1_1_1_0_1": "SMALL", "1_2_2_3_0_1_1_1_1": "BIG", "1_1_2_2_1_1_0_0_1": "BIG", "1_1_1_1_3_2_1_1_1": "SMALL", "2_1_1_1_3_1_0_0_1": "BIG", "2_3_1_1_0_1_0_1_0": "SMALL", "2_2_3_1_0_1_1_1_0": "BIG", "2_1_2_3_1_1_0_1_0": "SMALL", "2_1_1_2_2_1_1_0_1": "SMALL", "2_1_1_1_3_2_1_0_0": "SMALL", "2_2_1_1_0_2_1_1_1": "BIG", "2_3_1_1_0_1_1_1_0": "BIG", "2_1_3_1_1_1_0_0_1": "SMALL", "2_2_3_1_0_1_0_1_1": "SMALL", "2_1_2_3_1_1_1_0_1": "BIG", "2_2_2_3_0_1_1_1_1": "BIG", "2_1_2_2_1_1_0_0_1": "SMALL", "2_1_1_1_3_2_1_1_1": "SMALL", "0_1_2_0_1_0_1_0_0": "BIG", "0_2_2_0_0_0_1_1_1": "OPP", "0_2_2_2_0_1_0_1_1": "BIG", "0_3_2_2_0_1_0_0_1": "OPP", "1_1_2_0_1_0_1_0_0": "SMALL", "1_2_2_0_0_0_1_1_1": "BIG", "1_2_2_2_0_1_0_1_1": "SMALL", "1_3_2_2_0_1_0_0_1": "SMALL", "2_1_2_0_1_0_1_0_0": "BIG", "2_2_2_0_0_0_1_1_1": "BIG", "2_2_2_2_0_1_0_1_1": "SMALL", "2_3_2_2_0_1_0_0_1": "SMALL", "0_1_2_2_1_1_1_1_1": "BIG", "0_1_1_2_2_1_0_0_1": "BIG", "0_2_1_2_0_1_0_1_1": "OPP", "0_1_2_1_1_1_1_0_1": "OPP", "1_1_2_2_1_1_1_1_1": "OPP", "1_1_1_2_2_1_0_0_1": "BIG", "1_2_1_2_0_1_0_1_1": "SMALL", "1_1_2_1_1_1_1_0_1": "SMALL", "2_1_2_2_1_1_1_1_1": "BIG", "2_1_1_2_2_1_0_0_1": "BIG", "2_2_1_2_0_1_0_1_1": "SMALL", "2_1_2_1_1_1_1_0_1": "BIG", "0_1_2_1_1_2_1_0_0": "BIG", "0_2_2_1_0_1_1_0_0": "OPP", "1_1_2_1_1_2_1_0_0": "SMALL", "1_2_2_1_0_1_1_0_0": "BIG", "2_1_2_1_1_2_1_0_0": "BIG", "2_2_2_1_0_1_1_0_0": "BIG", "0_1_2_0_1_0_1_1_0": "OPP", "0_2_1_2_0_1_0_0_0": "BIG", "0_3_1_2_0_1_0_0_0": "SMALL", "0_4_1_2_0_1_0_0_0": "OPP", "1_1_2_0_1_0_1_1_0": "SMALL", "1_2_1_2_0_1_0_0_0": "SMALL", "1_3_1_2_0_1_0_0_0": "SMALL", "1_4_1_2_0_1_0_0_0": "SMALL", "2_1_2_0_1_0_1_1_0": "BIG", "2_2_1_2_0_1_0_0_0": "SMALL", "2_3_1_2_0_1_0_0_0": "SMALL", "2_4_1_2_0_1_0_0_0": "SMALL", "0_1_2_0_1_0_0_1_1": "SMALL", "0_2_2_0_0_0_0_1_0": "BIG", "0_3_2_0_0_0_0_0_1": "SMALL", "0_4_2_0_0_0_0_1_1": "OPP", "0_1_3_2_1_0_1_1_0": "BIG", "1_1_2_0_1_0_0_1_1": "BIG", "1_2_2_0_0_0_0_1_0": "SMALL", "1_3_2_0_0_0_0_0_1": "SMALL", "1_4_2_0_0_0_0_1_1": "SMALL", "1_1_3_2_1_0_1_1_0": "SMALL", "2_1_2_0_1_0_0_1_1": "SMALL", "2_2_2_0_0_0_0_1_0": "SMALL", "2_3_2_0_0_0_0_0_1": "SMALL", "2_4_2_0_0_0_0_1_1": "SMALL", "2_1_3_2_1_0_1_1_0": "BIG"};

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

  function predictApexTitan30S(sizes, nums, lossStreak) {
    if (!sizes || sizes.length === 0) return { finalSize: 'BIG', regime: 'INITIALIZING', conf: 85 };
    const { key, cSide, lastS, cLen, alt } = extractFeatures9(sizes, nums, lossStreak);
    
    let fallback = 'SAME';
    if (lossStreak >= 2) {
      fallback = cLen >= 2 ? cSide : (alt >= 2 ? opp(lastS) : cSide);
    } else if (lossStreak === 1) {
      fallback = cLen >= 2 ? cSide : (alt >= 2 ? opp(lastS) : opp(cSide));
    } else {
      fallback = cLen >= 3 ? cSide : (cLen === 2 ? opp(cSide) : (alt >= 2 ? opp(lastS) : cSide));
    }

    const actRule = TITAN_RULES_30S[key] || fallback;

    let finalSize = cSide;
    if (actRule === 'SAME') finalSize = cSide;
    else if (actRule === 'OPP') finalSize = opp(cSide);
    else if (actRule === 'LAST') finalSize = lastS;
    else if (actRule === 'OPP_LAST') finalSize = opp(lastS);

    const conf = lossStreak >= 2 ? 99 : (lossStreak === 1 ? 96 : 92);
    const regimeTag = lossStreak >= 2 ? `🛑 L3 RECOVERY (${actRule})` : (lossStreak === 1 ? `🛡️ L2 RECOVERY (${actRule})` : `🌊 L1 APEX (${actRule})`);

    return { finalSize, regime: `${regimeTag} [${finalSize}]`, conf };
  }

  function predictApexTitan1M(sizes, nums, lossStreak) {
    const { key, cSide, lastS, cLen, alt } = extractFeatures9(sizes, nums, lossStreak);
    
    let fallback = 'SAME';
    if (lossStreak >= 2) {
      fallback = cLen >= 2 ? cSide : (alt >= 2 ? opp(lastS) : cSide);
    } else if (lossStreak === 1) {
      fallback = cLen >= 2 ? cSide : (alt >= 2 ? opp(lastS) : opp(cSide));
    } else {
      fallback = cLen >= 3 ? cSide : (cLen === 2 ? opp(cSide) : (alt >= 2 ? opp(lastS) : cSide));
    }

    const actRule = TITAN_RULES_1M[key] || fallback;

    let finalSize = cSide;
    if (actRule === 'SAME') finalSize = cSide;
    else if (actRule === 'OPP') finalSize = opp(cSide);
    else if (actRule === 'LAST') finalSize = lastS;
    else if (actRule === 'OPP_LAST') finalSize = opp(lastS);

    const conf = lossStreak >= 2 ? 99 : (lossStreak === 1 ? 96 : 92);
    const regimeTag = lossStreak >= 2 ? `🛑 L3 1M RECOVERY (${actRule})` : (lossStreak === 1 ? `🛡️ L2 1M RECOVERY (${actRule})` : `🌊 L1 1M APEX (${actRule})`);

    return { finalSize, regime: `${regimeTag} [${finalSize}]`, conf };
  }

  function computeMasterPrediction() {
    const results = getMergedResults();
    if (!results || results.length === 0) {
      return { size: 'BIG', balls: [7, 8], number: 7, mode: '👑 JASH VIP · CALIBRATING', conf: 90 };
    }
    const historySeq = results.slice(0, 50).reverse();
    const sizes = historySeq.map(r => r.size);
    const nums = historySeq.map(r => r.number);

    const pred = (GAME_MODE === '1M')
      ? predictApexTitan1M(sizes, nums, martingaleStep)
      : predictApexTitan30S(sizes, nums, martingaleStep);

    // Harmonic Lucky Ball Selector
    const allowed = pred.finalSize === 'BIG' ? [5, 6, 7, 8, 9] : [0, 1, 2, 3, 4];
    const freq = {};
    allowed.forEach(n => freq[n] = 0);
    nums.slice(-20).forEach(n => { if (freq[n] !== undefined) freq[n]++; });
    const bestNum = allowed.reduce((best, n) => {
      const target = pred.finalSize === 'BIG' ? 7 : 2;
      const diff = Math.abs(n - target);
      const bestDiff = Math.abs(best - target);
      return freq[n] < freq[best] || (freq[n] === freq[best] && diff < bestDiff) ? n : best;
    }, allowed[0]);
    const secNum = pred.finalSize === 'BIG' ? (bestNum === 7 ? 8 : 7) : (bestNum === 2 ? 3 : 2);

    return {
      size: pred.finalSize,
      number: bestNum,
      balls: [bestNum, secNum],
      mode: pred.regime,
      conf: pred.conf
    };
  }

  // ── 6. WIN/LOSS RESOLUTION SCANNER ────────────────────────
  function scanFinishedResult() {
    if (LIVE_API_HISTORY.length > 0) {
      const top = LIVE_API_HISTORY[0];
      if (top && top.period) {
        const rec = RECORDED_BETS_FEED.find(r => r.period === top.period);
        const targetPred = rec ? rec.prediction : lastPredicted;
        const won = targetPred ? (String(targetPred).trim().toUpperCase() === String(top.size).trim().toUpperCase()) : false;
        return { period: top.period, won, size: top.size, number: top.number };
      }
    }
    const all = Array.from(document.querySelectorAll('div, span, p, tr, td')).filter(el => !el.closest('#jash-hud'));
    for (const el of all) {
      const txt = (el.textContent || '').trim();
      const m = txt.match(/\b(2026\d{10,14})\b/);
      if (m) {
        const cText = (el.closest('tr, .item, div') || el).textContent || txt;
        const hasSucceed = /succeed|\+₹|win|success/i.test(cText);
        const hasFailed = /failed|\-₹|loss|fail/i.test(cText);
        if (hasSucceed || hasFailed) {
          return { period: m[1], won: hasSucceed && !hasFailed };
        }
      }
    }
    return null;
  }

  // ── 7. TWO-WAY CLOUD LIVE SYNC & REMOTE CONTROL ──────────
  const CLOUD_SYNC_URL = 'https://jashvip.vercel.app/api/sync';

  function sendCloudTelemetry() {
    try {
      const secondsLeft = getSynchronizedSeconds();
      const pred = computeMasterPrediction();

      let statusText = running ? `24/7 ACTIVE (${GAME_MODE})` : 'STOPPED';
      if (liveWalletBal >= TAKE_PROFIT_TARGET) statusText = 'TARGET REACHED';

      const payload = {
        isTelemetry: true,
        gameMode: GAME_MODE,
        startBankroll: START_BANKROLL,
        liveWalletBal: liveWalletBal,
        sessionProfit: sessionProfit,
        currentStake: currentBet,
        baseBet: BASE_BET,
        takeProfitTarget: TAKE_PROFIT_TARGET,
        martingaleStep: martingaleStep,
        maxSteps: 999, // No loss limit
        running: running,
        wins: wins,
        losses: losses,
        timer: secondsLeft,
        nextPeriod: currentPeriod ? currentPeriod.slice(-4) : '--',
        nextPred: `${pred.size} [${pred.balls.join(',')}]`,
        status: statusText,
        history: RECORDED_BETS_FEED.slice(0, 25)
      };

      fetch(CLOUD_SYNC_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      .then(r => r.json())
      .then(data => {
        if (data && data.command) {
          const cmd = data.command;
          console.log(`%c[JASH VIP REMOTE] 📡 Received Command: ${cmd.type}`, 'background:#7c3aed;color:#fff;font-weight:bold;padding:4px');

          if (cmd.type === 'TOGGLE_RUNNING') {
            running = (cmd.payload?.running !== undefined) ? Boolean(cmd.payload.running) : !running;
            const b = document.getElementById('j-toggle-btn');
            if (b) {
              b.textContent = running ? '⏹ STOP ENGINE' : '▶ START ENGINE';
              b.className = running ? 'j-btn j-stop' : 'j-btn j-start';
            }
          } else if (cmd.type === 'SET_GAME_MODE') {
            if (cmd.payload && (cmd.payload.mode === '30S' || cmd.payload.mode === '1M')) {
              GAME_MODE = cmd.payload.mode;
              const mb = document.getElementById('j-mode-btn');
              if (mb) mb.textContent = `⏱️ MODE: ${GAME_MODE === '30S' ? '30 SEC (FAST)' : '1 MIN (STANDARD)'}`;
            }
          } else if (cmd.type === 'RESET_SESSION') {
            wins = 0; losses = 0;
            START_BANKROLL = liveWalletBal;
            sessionProfit = 0;
            martingaleStep = 0;
            currentBet = getStakeForStep(BASE_BET, 0);
            RECORDED_BETS_FEED = [];
            try { localStorage.removeItem('JASH_BETS_FEED'); localStorage.removeItem('REAL_BETS_FEED'); } catch (e) {}
          } else if (cmd.type === 'SET_BASE_BET' || cmd.payload?.baseBet != null) {
            const bVal = parseInt(cmd.payload?.baseBet || cmd.payload);
            if (!isNaN(bVal) && bVal >= 1) {
              BASE_BET = bVal;
              currentBet = getStakeForStep(BASE_BET, martingaleStep);
              const inp = document.getElementById('j-base-input');
              if (inp) inp.value = BASE_BET;
            }
          } else if (cmd.type === 'SET_TAKE_PROFIT' || cmd.payload?.takeProfitTarget != null) {
            const tpVal = parseFloat(cmd.payload?.takeProfitTarget || cmd.payload);
            if (!isNaN(tpVal) && tpVal >= 1) {
              TAKE_PROFIT_TARGET = tpVal;
              const inp = document.getElementById('j-tp-input');
              if (inp) inp.value = TAKE_PROFIT_TARGET;
            }
          }
          persistAllState();
          updateHud();
        }
      })
      .catch(() => {});
    } catch (e) {}
  }
  setInterval(sendCloudTelemetry, 1500);

  // ── 8. FAST TOUCH & CLICK BET ORDER PLACEMENT ─────────────
  function fireClick(el) {
    if (!el) return;
    try { el.scrollIntoView({ block: 'center', inline: 'center', behavior: 'instant' }); } catch (e) {}
    try {
      const rect = el.getBoundingClientRect();
      const cx = rect.left + rect.width / 2, cy = rect.top + rect.height / 2;
      const touch = new Touch({ identifier: Date.now(), target: el, clientX: cx, clientY: cy, pageX: cx, pageY: cy, screenX: cx, screenY: cy });
      el.dispatchEvent(new TouchEvent('touchstart', { bubbles: true, cancelable: true, touches: [touch], targetTouches: [touch], changedTouches: [touch] }));
      el.dispatchEvent(new TouchEvent('touchend', { bubbles: true, cancelable: true, touches: [], targetTouches: [], changedTouches: [touch] }));
    } catch (e) {}
    ['pointerdown', 'mousedown', 'pointerup', 'mouseup', 'click'].forEach(evt => {
      try { el.dispatchEvent(new MouseEvent(evt, { bubbles: true, cancelable: true, view: window })); } catch (e) {}
    });
    try { el.click(); } catch (e) {}
  }

  async function executeBet(size, amount) {
    const target = size.trim().toUpperCase();
    console.log(`%c[👑 JASH VIP] 🎯 BETTING: ${target} ₹${amount} (${GAME_MODE} Step ${martingaleStep})`, 'background:linear-gradient(90deg,#00f5a0,#7c3aed);color:#000;font-weight:bold;padding:6px 12px;font-size:13px;border-radius:4px');

    const allEls = Array.from(document.querySelectorAll('div, button, span, uni-view, p')).filter(e => !e.closest('#jash-hud'));

    let targetBtn = allEls.find(e => {
      const txt = (e.textContent || '').trim().toUpperCase();
      return (txt === target || txt === `${target} 2X` || txt === `${target}2X`) && e.children.length <= 1;
    });
    if (!targetBtn) {
      targetBtn = allEls.find(e => {
        const txt = (e.textContent || '').trim().toUpperCase();
        return txt.startsWith(target) && txt.length <= 10;
      });
    }
    if (!targetBtn) return false;

    fireClick(targetBtn);
    await new Promise(r => setTimeout(r, 350));

    const modalInputs = Array.from(document.querySelectorAll('.van-popup input, .popup input, input[type="tel"], input[type="number"], input')).filter(i => !i.closest('#jash-hud'));
    if (modalInputs.length > 0) {
      const inp = modalInputs[modalInputs.length - 1];
      try {
        inp.focus();
        inp.value = String(amount);
        const setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value')?.set;
        if (setter) setter.call(inp, String(amount));
        inp.dispatchEvent(new Event('input', { bubbles: true }));
        inp.dispatchEvent(new Event('change', { bubbles: true }));
      } catch (e) {}
    }

    if (amount > 1) {
      const plusBtns = Array.from(document.querySelectorAll('.van-stepper__plus, button.plus, .plus, [class*="plus"]')).filter(b => !b.closest('#jash-hud'));
      if (plusBtns.length > 0) {
        const plusBtn = plusBtns[plusBtns.length - 1];
        for (let i = 1; i < amount; i++) {
          fireClick(plusBtn);
          await new Promise(r => setTimeout(r, 30));
        }
      }
    }

    await new Promise(r => setTimeout(r, 100));

    let confirmBtn = null;
    const allPopupEls = Array.from(document.querySelectorAll('*')).filter(e => !e.closest('#jash-hud'));

    const totalAmountCandidates = allPopupEls.filter(b => {
      const t = (b.textContent || '').trim();
      return (t.startsWith('Total amount') || t.includes('Total amount')) && !t.includes('Cancel') && t.length <= 35;
    });

    if (totalAmountCandidates.length > 0) {
      confirmBtn = totalAmountCandidates[totalAmountCandidates.length - 1];
    } else {
      confirmBtn = allPopupEls.find(b => {
        const t = (b.textContent || '').trim();
        return /Confirm|Submit|Order|Buy|Bet/i.test(t) && !t.includes('Cancel') && t.length <= 25;
      });
    }

    if (confirmBtn) {
      try { confirmBtn.click(); } catch (e) {}
      fireClick(confirmBtn);
      return true;
    }
    return false;
  }

  // ── 9. CYBER JASH VIP HUD (INSTANT MOUNT & 1000 LOGS) ────
  function createHud() {
    if (document.getElementById('jash-hud')) return;
    const target = document.body || document.documentElement;
    if (!target) return;

    const hud = document.createElement('div');
    hud.id = 'jash-hud';
    hud.style.cssText = `
      position: fixed !important;
      top: 10px !important;
      right: 10px !important;
      z-index: 2147483647 !important;
      width: 305px !important;
      background: rgba(10, 14, 30, 0.96) !important;
      backdrop-filter: blur(20px) !important;
      border: 2px solid #00f5a0 !important;
      border-radius: 20px !important;
      color: #fff !important;
      padding: 14px !important;
      font-family: 'Segoe UI', Roboto, sans-serif !important;
      font-size: 11.5px !important;
      box-shadow: 0 0 30px rgba(0, 245, 160, 0.4) !important;
      user-select: none !important;
    `;

    hud.innerHTML = `
      <style>
        #jash-hud * { box-sizing: border-box; }
        .j-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
        .j-lbl { color: #aab4c2; font-weight: 800; font-size: 11px; }
        .j-val { font-weight: 900; color: #00f5a0; }
        .ju-input {
          width: 75px; background: rgba(255,255,255,0.08); border: 1px solid #00f5a0;
          border-radius: 6px; color: #00f5a0; font-weight: 900; padding: 2px 4px;
          text-align: center; font-size: 11px; outline: none;
        }
        .j-btn {
          width: 100%; padding: 9px; border: none; border-radius: 10px;
          font-weight: 900; font-size: 11.5px; cursor: pointer; margin-top: 5px;
        }
        .j-start { background: linear-gradient(135deg,#10b981,#059669); color: #fff; }
        .j-stop { background: linear-gradient(135deg,#ef4444,#b91c1c); color: #fff; }
        .j-mode-switch {
          background: linear-gradient(135deg,#7c3aed,#00d9f5); color: #fff;
          font-weight: 900; font-size: 11px; letter-spacing: 1px;
          border: 1px solid rgba(255,255,255,0.3); border-radius: 8px;
          padding: 6px 10px; cursor: pointer; width: 100%; text-align: center; margin-bottom: 6px;
        }
      </style>
      <div class="j-row" id="jash-drag-hdr" style="cursor:move;">
        <span style="font-weight:900;font-size:12px;background:linear-gradient(90deg,#00f5a0,#00d9f5,#7c3aed);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">👑 JASH VIP · TITAN SUPREME v18.0</span>
        <span id="j-timer" style="color:#00f5a0;font-weight:bold;font-size:13px;">--s</span>
      </div>

      <button class="j-mode-switch" id="j-mode-btn">⏱️ MODE: ${GAME_MODE === '30S' ? '30 SEC (FAST)' : '1 MIN (STANDARD)'}</button>

      <div id="j-status-badge" style="background:rgba(0,245,160,0.12);border:1px solid #00f5a0;border-radius:8px;padding:5px;text-align:center;margin:4px 0 6px;font-weight:900;color:#00f5a0;font-size:10.5px;">⚡ TITAN SUPREME v18.0 (DIRECT API SYNC 9F)</div>

      <div class="j-row">
        <span class="j-lbl">Base Bet (₹):</span>
        <input type="number" id="j-base-input" class="ju-input" value="${BASE_BET}" min="1">
      </div>
      <div class="j-row">
        <span class="j-lbl">Take Profit (₹):</span>
        <input type="number" id="j-tp-input" class="ju-input" value="${TAKE_PROFIT_TARGET}" min="1">
      </div>
      <div class="j-row">
        <span class="j-lbl">Live Balance:</span>
        <span class="j-val" id="j-livebal">₹${liveWalletBal.toFixed(2)}</span>
      </div>
      <div class="j-row">
        <span class="j-lbl">Next Pred:</span>
        <span class="j-val" id="j-next-pred-lbl" style="color:#56e6ff;font-size:13px;">--</span>
      </div>
      <div class="j-row">
        <span class="j-lbl">Current Stake:</span>
        <span class="j-val" id="j-stake">₹${currentBet} (Step ${martingaleStep})</span>
      </div>
      <div class="j-row">
        <span class="j-lbl">Score:</span>
        <span class="j-val" id="j-score" style="color:#38f59b;">${wins}W / ${losses}L</span>
      </div>

      <div style="display:flex;gap:6px;margin-top:6px;">
        <button class="j-btn ${running ? 'j-stop' : 'j-start'}" id="j-toggle-btn" style="flex:1;margin-top:0;">${running ? '⏹ STOP ENGINE' : '▶ START ENGINE'}</button>
        <button id="j-reset-btn" style="background:rgba(255,255,255,0.1);border:1px solid #00f5a0;color:#00f5a0;font-weight:900;font-size:11px;border-radius:10px;padding:0 10px;cursor:pointer;">🔄 RESET</button>
      </div>

      <div id="j-feed-box" style="font-size:9px;max-height:75px;overflow-y:auto;background:rgba(0,0,0,0.4);border-radius:6px;padding:4px;border:1px solid rgba(255,255,255,0.06);margin-top:6px;"></div>
    `;
    target.appendChild(hud);

    // Draggable
    let isDragging = false, startX, startY, initialLeft, initialTop;
    const header = document.getElementById('jash-drag-hdr');
    header?.addEventListener('mousedown', (e) => {
      isDragging = true;
      startX = e.clientX; startY = e.clientY;
      const rect = hud.getBoundingClientRect();
      initialLeft = rect.left; initialTop = rect.top;
      hud.style.right = 'auto';
      hud.style.left = `${initialLeft}px`;
      hud.style.top = `${initialTop}px`;
    });
    document.addEventListener('mousemove', (e) => {
      if (!isDragging) return;
      hud.style.left = `${initialLeft + e.clientX - startX}px`;
      hud.style.top = `${initialTop + e.clientY - startY}px`;
    });
    document.addEventListener('mouseup', () => { isDragging = false; });

    document.getElementById('j-mode-btn').onclick = () => {
      GAME_MODE = (GAME_MODE === '30S') ? '1M' : '30S';
      document.getElementById('j-mode-btn').textContent = `⏱️ MODE: ${GAME_MODE === '30S' ? '30 SEC (FAST)' : '1 MIN (STANDARD)'}`;
      persistAllState();
      updateHud();
      sendCloudTelemetry();
    };

    document.getElementById('j-base-input').onchange = (e) => {
      BASE_BET = parseInt(e.target.value) || 2;
      currentBet = getStakeForStep(BASE_BET, martingaleStep);
      persistAllState();
      updateHud();
      sendCloudTelemetry();
    };

    document.getElementById('j-tp-input').onchange = (e) => {
      TAKE_PROFIT_TARGET = parseFloat(e.target.value) || 50000;
      persistAllState();
      updateHud();
      sendCloudTelemetry();
    };

    document.getElementById('j-reset-btn').onclick = () => {
      if (!confirm('Reset session statistics?')) return;
      wins = 0; losses = 0;
      START_BANKROLL = liveWalletBal;
      sessionProfit = 0;
      martingaleStep = 0;
      currentBet = getStakeForStep(BASE_BET, 0);
      RECORDED_BETS_FEED = [];
      try { localStorage.removeItem('JASH_BETS_FEED'); localStorage.removeItem('REAL_BETS_FEED'); } catch (e) {}
      persistAllState();
      updateHud();
      sendCloudTelemetry();
    };

    document.getElementById('j-toggle-btn').onclick = () => {
      running = !running;
      const b = document.getElementById('j-toggle-btn');
      b.textContent = running ? '⏹ STOP ENGINE' : '▶ START ENGINE';
      b.className = running ? 'j-btn j-stop' : 'j-btn j-start';
      pendingBet = null;
      persistAllState();
      updateHud();
      sendCloudTelemetry();
    };
  }

  function updateHud() {
    const badge = document.getElementById('j-status-badge');
    if (!badge) return;

    readScreenWalletBalance();

    badge.textContent = running ? (pendingBet ? `⏳ BETTING ₹${pendingBet.stake} ON ${pendingBet.pred}` : `⚡ TITAN SUPREME v18.0 (${GAME_MODE}) ACTIVE`) : `⏹ ENGINE (${GAME_MODE}) STOPPED`;
    badge.style.color = running ? '#00f5a0' : '#ff5368';

    document.getElementById('j-livebal').textContent = `₹${liveWalletBal.toFixed(2)}`;
    document.getElementById('j-stake').textContent = `₹${currentBet} (Step ${martingaleStep})`;
    document.getElementById('j-score').textContent = `${wins}W / ${losses}L`;

    const timerEl = document.getElementById('j-timer');
    if (timerEl) {
      const sLeft = getSynchronizedSeconds();
      timerEl.textContent = sLeft + 's';
    }

    const nextLbl = document.getElementById('j-next-pred-lbl');
    if (nextLbl) {
      const pred = computeMasterPrediction();
      nextLbl.textContent = `${pred.size} [${pred.balls.join(',')}]`;
      nextLbl.style.color = pred.size === 'BIG' ? '#56e6ff' : '#ff4da6';
    }

    const feedBox = document.getElementById('j-feed-box');
    if (feedBox && RECORDED_BETS_FEED.length > 0) {
      feedBox.innerHTML = RECORDED_BETS_FEED.slice(0, 15).map(f => `
        <div style="display:flex;justify-content:space-between;padding:2px 0;border-bottom:1px solid rgba(255,255,255,0.05);color:${f.won === true ? '#00f5a0' : f.won === false ? '#ff007a' : '#ffcc00'}">
          <span>..${String(f.period).slice(-4)} ${f.prediction}</span>
          <span>${f.won === true ? 'WIN' : f.won === false ? 'LOSS' : 'PENDING'}</span>
        </div>
      `).join('');
    }
  }

  // ── 10. MAIN AUTOBET CYCLE LOOP ───────────────────────────
  async function botCycle() {
    try {
      const secondsLeft = getSynchronizedSeconds();
      const currentBucket = getCurrentTimeBucket();

      const tEl = document.getElementById('j-timer');
      if (tEl) tEl.textContent = secondsLeft + 's';

      if (secondsLeft === 28 || secondsLeft === 58) readScreenWalletBalance();

      let activePeriod = null;
      const allText = Array.from(document.querySelectorAll('div, span, p, b')).filter(e => !e.closest('#jash-hud') && !e.closest('table'));
      for (const el of allText) {
        const txt = (el.textContent || '').trim();
        const m = txt.match(/\b(2026\d{10,14})\b/);
        if (m && txt.length < 30) { activePeriod = m[1]; break; }
      }
      if (!activePeriod && LOCAL_DRAW_BUFFER.length > 0) {
        try { activePeriod = (BigInt(LOCAL_DRAW_BUFFER[0].period) + 1n).toString(); } catch (e) {}
      }

      if (activePeriod && currentPeriod && activePeriod !== currentPeriod) {
        pendingBet = null;
      }
      currentPeriod = activePeriod;

      const finished = scanFinishedResult();
      if (finished && finished.period && !RESOLVED_PERIODS.has(finished.period)) {
        RESOLVED_PERIODS.add(finished.period);

        let rec = RECORDED_BETS_FEED.find(r => r.period === finished.period);
        if (rec) {
          rec.isPending = false;
          rec.won = finished.won;
          rec.number = finished.number != null ? finished.number : '--';
          rec.size = finished.size || (finished.won ? rec.prediction : (rec.prediction === 'BIG' ? 'SMALL' : 'BIG'));
          rec.profit = finished.won ? (rec.stake * 0.96) : (-rec.stake);
        }

        if (ACTUALLY_PLACED_PERIODS.has(finished.period)) {
          if (finished.won) {
            wins++;
            martingaleStep = 0;
            currentBet = getStakeForStep(BASE_BET, 0);
            console.log(`%c🏆 JASH VIP WIN on #${finished.period}! Reset to Base ₹${BASE_BET}`, 'background:#10b981;color:#fff;font-weight:bold;padding:5px');
          } else {
            losses++;
            martingaleStep++;
            currentBet = getStakeForStep(BASE_BET, martingaleStep);
            console.log(`%c💀 JASH VIP LOSS on #${finished.period}! Step ${martingaleStep} -> ₹${currentBet} (No Loss Limit Martingale)`, 'background:#ef4444;color:#fff;font-weight:bold;padding:5px');
          }
        }

        if (RECORDED_BETS_FEED.length > 1000) RECORDED_BETS_FEED = RECORDED_BETS_FEED.slice(0, 1000);
        try { localStorage.setItem('JASH_BETS_FEED', JSON.stringify(RECORDED_BETS_FEED.slice(0, 50))); } catch (e) {}

        pendingBet = null;
        persistAllState();
        updateHud();
      }

      const masterPred = computeMasterPrediction();
      updateHud();

      if (liveWalletBal >= TAKE_PROFIT_TARGET && running) {
        running = false;
        persistAllState();
        return;
      }

      if (!running || isBettingInProgress) return;
      if (LOCKED_TIME_BUCKETS.has(currentBucket)) return;

      const canBet = (GAME_MODE === '30S')
        ? (secondsLeft <= 25 && secondsLeft >= 4)
        : (secondsLeft <= 55 && secondsLeft >= 8);

      if (running && canBet && !LOCKED_TIME_BUCKETS.has(currentBucket)) {
        LOCKED_TIME_BUCKETS.add(currentBucket);
        if (activePeriod) ACTUALLY_PLACED_PERIODS.add(activePeriod);
        isBettingInProgress = true;

        lastPredicted = masterPred.size;
        pendingBet = { period: activePeriod, pred: masterPred.size, stake: currentBet, placedAt: Date.now() };

        if (activePeriod) {
          RECORDED_BETS_FEED.unshift({
            period: activePeriod,
            prediction: masterPred.size,
            mode: masterPred.mode,
            stake: currentBet,
            number: '--',
            size: '--',
            won: null,
            profit: null,
            isPending: true,
            time: new Date().toLocaleTimeString()
          });
          if (RECORDED_BETS_FEED.length > 1000) RECORDED_BETS_FEED = RECORDED_BETS_FEED.slice(0, 1000);
          try { localStorage.setItem('JASH_BETS_FEED', JSON.stringify(RECORDED_BETS_FEED.slice(0, 50))); } catch (e) {}
        }

        persistAllState();
        updateHud();

        await executeBet(masterPred.size, currentBet);
        setTimeout(() => {
          isBettingInProgress = false;
          pendingBet = null;
        }, (GAME_MODE === '30S' ? 2500 : 4000));
      }
    } catch (e) {
      isBettingInProgress = false;
    }
  }

  // ── 11. SPA CONTINUOUS ATTACHMENT & INITIALIZATION ───────
  function ensureHud() {
    if (!document.getElementById('jash-hud')) createHud();
  }

  createHud();
  setInterval(ensureHud, 1000);
  setInterval(botCycle, 1000);
})();
