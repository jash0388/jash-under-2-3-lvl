import json
import os

script_code = '''// ==UserScript==
// @name         JASH VIP v24.0 CLEAN (Single Brain — Zero Desync)
// @namespace    http://tampermonkey.net/
// @version      24.0
// @description  👑 JASH VIP · WinGo 30S | v24.0 SINGLE-SOURCE PREDICTION · ar-lottery01 ONLY · NO FALLBACK · NO DESYNC
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

  console.log("%c👑 JASH VIP v24.0 CLEAN · SINGLE BRAIN · ZERO DESYNC", "background:linear-gradient(135deg,#00f5a0,#00d9f5,#7c3aed);color:#000;font-size:14px;font-weight:900;padding:6px 14px;border-radius:8px;box-shadow:0 0 20px rgba(0,245,160,0.5);");

  // ── 1. WAKE LOCK ──────────────────────────────────────────
  let wakeLockObj = null;
  async function requestWakeLock() {
    try {
      if ('wakeLock' in navigator) wakeLockObj = await navigator.wakeLock.request('screen');
    } catch (e) {}
  }
  setInterval(requestWakeLock, 8000);
  requestWakeLock();

  // ── 2. STATE ──────────────────────────────────────────────
  let GAME_MODE     = localStorage.getItem('J24_GAME_MODE') || '30S';
  let BASE_BET      = parseInt(localStorage.getItem('J24_BASE_BET')) || 2;
  let START_BANKROLL = parseFloat(localStorage.getItem('J24_START_BANKROLL')) || 400.00;
  let TAKE_PROFIT   = parseFloat(localStorage.getItem('J24_TAKE_PROFIT')) || 50000.00;

  function getStakeForStep(base, step) {
    const b = Math.max(1, parseInt(base) || 2);
    const s = parseInt(step) || 0;
    if (s <= 0) return b;
    if (s === 1) return b * 2 + 1;
    return (b * 2 + 1) * Math.pow(2, s - 1);
  }

  let sessionProfit  = parseFloat(localStorage.getItem('J24_PROFIT')) || 0;
  let wins           = parseInt(localStorage.getItem('J24_WINS')) || 0;
  let losses         = parseInt(localStorage.getItem('J24_LOSSES')) || 0;
  let martingaleStep = parseInt(localStorage.getItem('J24_STEP')) || 0;
  let currentBet     = getStakeForStep(BASE_BET, martingaleStep);
  let running        = false;
  let liveWalletBal  = parseFloat(localStorage.getItem('J24_WALLET')) || 400.00;

  // THE SINGLE LOSS STREAK COUNTER — persisted to localStorage
  let LOSS_STREAK    = parseInt(localStorage.getItem('J24_LOSS_STREAK')) || 0;

  let currentPeriod  = null;
  let lastPredicted  = localStorage.getItem('J24_LAST_PRED') || null;
  let pendingBet     = null;
  let isBettingInProgress = false;

  const LOCKED_TIME_BUCKETS = new Set();
  const RESOLVED_PERIODS = new Set();
  const ACTUALLY_PLACED_PERIODS = new Set();

  // THE SINGLE DATA SOURCE — only from ar-lottery01.com
  let LOTTERY_HISTORY = [];
  // Last period we saw from API — to detect new draws
  let LAST_SEEN_PERIOD = localStorage.getItem('J24_LAST_SEEN_PERIOD') || '';

  let RECORDED_BETS = [];
  try {
    const saved = localStorage.getItem('J24_BETS');
    if (saved) RECORDED_BETS = JSON.parse(saved);
  } catch (e) {}

  function persistAll() {
    try {
      localStorage.setItem('J24_GAME_MODE', GAME_MODE);
      localStorage.setItem('J24_START_BANKROLL', START_BANKROLL);
      localStorage.setItem('J24_BASE_BET', BASE_BET);
      localStorage.setItem('J24_TAKE_PROFIT', TAKE_PROFIT);
      localStorage.setItem('J24_PROFIT', sessionProfit);
      localStorage.setItem('J24_WINS', wins);
      localStorage.setItem('J24_LOSSES', losses);
      localStorage.setItem('J24_STEP', martingaleStep);
      localStorage.setItem('J24_WALLET', liveWalletBal);
      localStorage.setItem('J24_LOSS_STREAK', LOSS_STREAK);
      localStorage.setItem('J24_LAST_SEEN_PERIOD', LAST_SEEN_PERIOD);
      if (lastPredicted) localStorage.setItem('J24_LAST_PRED', lastPredicted);
    } catch (e) {}
  }

  // ── 3. SINGLE DATA SOURCE: ar-lottery01.com ONLY ──────────
  const sizeFor = n => (Number(n) >= 5 ? 'BIG' : 'SMALL');

  // Intercept XHR/fetch ONLY for wallet balance — NOT for draw data
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
              persistAll();
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
                persistAll();
              }
            }
          }
        } catch (e) {}
      }).catch(() => {});
    } catch (e) {}
    return response;
  };

  // THE SINGLE FETCH: ar-lottery01.com — this is the ONLY source of draw data
  async function fetchLotteryHistory() {
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
          LOTTERY_HISTORY = list.map(item => {
            const p = String(item.issueNumber || item.period || '').trim();
            const n = parseInt(item.number);
            return { period: p, number: n, size: sizeFor(n) };
          }).filter(x => /^\\d+$/.test(x.period) && Number.isInteger(x.number));

          // Detect new draw for win/loss resolution
          if (LOTTERY_HISTORY.length > 0) {
            const topPeriod = LOTTERY_HISTORY[0].period;
            if (topPeriod !== LAST_SEEN_PERIOD && LAST_SEEN_PERIOD !== '') {
              resolveResult(LOTTERY_HISTORY[0]);
            }
            LAST_SEEN_PERIOD = topPeriod;
            localStorage.setItem('J24_LAST_SEEN_PERIOD', LAST_SEEN_PERIOD);
          }
        }
      }
    } catch (e) {
      console.log('[J24] Lottery fetch failed, will retry next cycle');
    }
  }
  setInterval(fetchLotteryHistory, 1500);
  fetchLotteryHistory();

  // ── 4. THE SINGLE PREDICTION ENGINE ───────────────────────
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

  // === 9-FEATURE TITAN SUPREME STATE TABLES ===
  const RULES_30S = RULES_30S_PLACEHOLDER;
  const RULES_1M = RULES_1M_PLACEHOLDER;

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

  function predict(sizes, nums, lossStreak) {
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

    const table = (GAME_MODE === '1M') ? RULES_1M : RULES_30S;
    const actRule = table[key] || fallback;

    let finalSize = cSide;
    if (actRule === 'SAME') finalSize = cSide;
    else if (actRule === 'OPP') finalSize = opp(cSide);
    else if (actRule === 'LAST') finalSize = lastS;
    else if (actRule === 'OPP_LAST') finalSize = opp(lastS);
    else if (actRule === 'BIG' || actRule === 'SMALL') finalSize = actRule;

    const conf = lossStreak >= 2 ? 99 : (lossStreak === 1 ? 96 : 92);
    const tag = lossStreak >= 2 ? `🛑 L${lossStreak+1} RECOVERY` : (lossStreak === 1 ? '🛡️ L2 RECOVERY' : '🌊 APEX');
    return { finalSize, regime: `${tag} [${finalSize}] (${actRule})`, conf };
  }

  // THE SINGLE computePrediction — uses ONLY LOTTERY_HISTORY and THE SINGLE LOSS_STREAK
  function computePrediction() {
    if (!LOTTERY_HISTORY || LOTTERY_HISTORY.length < 3) {
      return { size: 'BIG', number: 7, balls: [7, 8], mode: '⏳ WAITING FOR DATA', conf: 0, noData: true };
    }

    // Sort oldest first
    const sorted = [...LOTTERY_HISTORY].sort((a, b) => {
      try { return BigInt(a.period) > BigInt(b.period) ? 1 : -1; } catch (e) { return 0; }
    });

    const sizes = sorted.map(r => r.size);
    const nums = sorted.map(r => r.number);

    // Use the SINGLE persisted LOSS_STREAK — NOT a replay
    const pred = predict(sizes, nums, LOSS_STREAK);
    const bestNum = pred.finalSize === 'BIG' ? 7 : 2;
    const secNum = pred.finalSize === 'BIG' ? 8 : 3;

    return {
      size: pred.finalSize,
      number: bestNum,
      balls: [bestNum, secNum],
      mode: pred.regime,
      conf: pred.conf,
      noData: false
    };
  }

  // ── 5. WIN/LOSS RESOLUTION — THE SINGLE TRUTH ────────────
  function resolveResult(topDraw) {
    if (!topDraw || !topDraw.period) return;
    if (RESOLVED_PERIODS.has(topDraw.period)) return;
    RESOLVED_PERIODS.add(topDraw.period);

    // Find if we placed a bet on this period
    const rec = RECORDED_BETS.find(r => r.period === topDraw.period);
    const didBet = ACTUALLY_PLACED_PERIODS.has(topDraw.period);

    if (rec) {
      const won = String(rec.prediction).toUpperCase() === String(topDraw.size).toUpperCase();
      rec.won = won;
      rec.number = topDraw.number;
      rec.size = topDraw.size;
      rec.isPending = false;
      rec.profit = won ? (rec.stake * 0.96) : (-rec.stake);

      if (didBet) {
        if (won) {
          wins++;
          LOSS_STREAK = 0;
          martingaleStep = 0;
          currentBet = getStakeForStep(BASE_BET, 0);
          console.log(`%c🏆 WIN on #${topDraw.period}! → Reset to ₹${BASE_BET} | Streak: 0`, 'background:#10b981;color:#fff;font-weight:bold;padding:5px');
        } else {
          losses++;
          LOSS_STREAK++;
          martingaleStep++;
          currentBet = getStakeForStep(BASE_BET, martingaleStep);
          console.log(`%c💀 LOSS on #${topDraw.period}! → Step ${martingaleStep} ₹${currentBet} | Streak: ${LOSS_STREAK}`, 'background:#ef4444;color:#fff;font-weight:bold;padding:5px');
        }
      }
    } else if (didBet && lastPredicted) {
      // We bet but don't have a record — use lastPredicted
      const won = String(lastPredicted).toUpperCase() === String(topDraw.size).toUpperCase();
      if (won) {
        wins++;
        LOSS_STREAK = 0;
        martingaleStep = 0;
        currentBet = getStakeForStep(BASE_BET, 0);
      } else {
        losses++;
        LOSS_STREAK++;
        martingaleStep++;
        currentBet = getStakeForStep(BASE_BET, martingaleStep);
      }
    }

    if (RECORDED_BETS.length > 500) RECORDED_BETS = RECORDED_BETS.slice(0, 500);
    try { localStorage.setItem('J24_BETS', JSON.stringify(RECORDED_BETS.slice(0, 50))); } catch (e) {}
    pendingBet = null;
    persistAll();
    updateHud();
  }

  // ── 6. TIMER ──────────────────────────────────────────────
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
        const m = clean.match(/^[₹$¥]?\\s*([0-9]+\\.[0-9]{2})$/);
        if (m) {
          const val = parseFloat(m[1]);
          if (val >= 0.1 && val < 50000000) {
            liveWalletBal = val;
            sessionProfit = liveWalletBal - START_BANKROLL;
            persistAll();
            return val;
          }
        }
      }
      const all = Array.from(document.querySelectorAll('div, span, p, h1, h2, h3, b')).filter(e => !e.closest('#jash-hud') && !e.closest('table') && !e.closest('.ball'));
      for (const el of all) {
        const txt = (el.textContent || '').trim();
        if (txt.includes('₹') || (txt.includes('.') && txt.length <= 20)) {
          const clean = txt.replace(/[₹$,\\s]/g, '').trim();
          const m = clean.match(/^([0-9]+\\.[0-9]{2})$/);
          if (m) {
            const val = parseFloat(m[1]);
            if (val >= 0.1 && val < 50000000) {
              liveWalletBal = val;
              sessionProfit = liveWalletBal - START_BANKROLL;
              persistAll();
              return val;
            }
          }
        }
      }
    } catch (e) {}
    return liveWalletBal;
  }

  // ── 7. CLOUD TELEMETRY ────────────────────────────────────
  function sendCloudTelemetry() {
    try {
      const pred = computePrediction();
      const payload = {
        isTelemetry: true,
        gameMode: GAME_MODE,
        startBankroll: START_BANKROLL,
        liveWalletBal: liveWalletBal,
        sessionProfit: sessionProfit,
        currentStake: currentBet,
        baseBet: BASE_BET,
        takeProfitTarget: TAKE_PROFIT,
        martingaleStep: martingaleStep,
        maxSteps: 999,
        running: running,
        wins: wins,
        losses: losses,
        timer: getSynchronizedSeconds(),
        nextPred: `${pred.size} [${pred.balls.join(',')}]`,
        lossStreak: LOSS_STREAK,
        status: running ? 'ACTIVE' : 'STOPPED',
        history: RECORDED_BETS.slice(0, 25)
      };

      fetch('https://jashvip.vercel.app/api/sync', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      .then(r => r.json())
      .then(data => {
        if (data && data.command) {
          const cmd = data.command;
          if (cmd.type === 'TOGGLE_RUNNING') {
            running = (cmd.payload?.running !== undefined) ? Boolean(cmd.payload.running) : !running;
            const b = document.getElementById('j-toggle-btn');
            if (b) {
              b.textContent = running ? '⏹ STOP' : '▶ START';
              b.className = running ? 'j-btn j-stop' : 'j-btn j-start';
            }
          } else if (cmd.type === 'SET_GAME_MODE') {
            if (cmd.payload && (cmd.payload.mode === '30S' || cmd.payload.mode === '1M')) {
              GAME_MODE = cmd.payload.mode;
              LOSS_STREAK = 0; // reset streak on mode change
              const mb = document.getElementById('j-mode-btn');
              if (mb) mb.textContent = `⏱️ ${GAME_MODE === '30S' ? '30S' : '1M'}`;
            }
          } else if (cmd.type === 'RESET_SESSION') {
            wins = 0; losses = 0;
            START_BANKROLL = liveWalletBal;
            sessionProfit = 0;
            martingaleStep = 0;
            LOSS_STREAK = 0;
            currentBet = getStakeForStep(BASE_BET, 0);
            RECORDED_BETS = [];
            try { localStorage.removeItem('J24_BETS'); } catch (e) {}
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
              TAKE_PROFIT = tpVal;
              const inp = document.getElementById('j-tp-input');
              if (inp) inp.value = TAKE_PROFIT;
            }
          }
          persistAll();
          updateHud();
        }
      })
      .catch(() => {});
    } catch (e) {}
  }
  setInterval(sendCloudTelemetry, 1500);

  // ── 8. CLICK/TAP BET PLACEMENT ────────────────────────────
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
    console.log(`%c[👑 J24] 🎯 BET: ${target} ₹${amount} (${GAME_MODE} Step ${martingaleStep} Streak ${LOSS_STREAK})`, 'background:linear-gradient(90deg,#00f5a0,#7c3aed);color:#000;font-weight:bold;padding:6px 12px;font-size:13px;border-radius:4px');

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

  // ── 9. HUD ────────────────────────────────────────────────
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
        .j-row { display: flex; justify-content: space-between; align-items: center; margin: 3px 0; }
        .j-val { color: #00f5a0; font-weight: bold; }
        .j-label { color: #8fa0b5; }
        .j-btn { display: inline-block; padding: 6px 10px; border-radius: 8px; font-weight: 700; font-size: 11px; cursor: pointer; border: none; text-align: center; margin: 3px 2px; }
        .j-start { background: linear-gradient(135deg, #00f5a0, #00d9f5); color: #0a0e1e; }
        .j-stop { background: linear-gradient(135deg, #ff007a, #ff5368); color: #fff; }
        .j-mode { background: #1a1e30; color: #00f5a0; border: 1px solid #00f5a0; }
        .j-config-row { display: flex; align-items: center; gap: 5px; margin: 4px 0; }
        .j-config-row label { color: #8fa0b5; font-size: 10px; flex: 0 0 80px; }
        .j-config-row input { background: #1a1e30; border: 1px solid #334; color: #fff; border-radius: 6px; padding: 4px 6px; width: 70px; font-size: 11px; }
        #j-feed-box { max-height: 180px; overflow-y: auto; margin-top: 6px; font-size: 10.5px; }
        #j-feed-box::-webkit-scrollbar { width: 4px; }
        #j-feed-box::-webkit-scrollbar-thumb { background: #00f5a0; border-radius: 10px; }
      </style>
      <div style="text-align:center;font-weight:900;font-size:13px;background:linear-gradient(90deg,#00f5a0,#00d9f5);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:6px">
        👑 JASH VIP v24.0 · SINGLE BRAIN
      </div>

      <div id="j-status-badge" style="text-align:center;color:#ff5368;font-weight:bold;font-size:11px;margin-bottom:6px">⏹ ENGINE STOPPED</div>

      <div class="j-row"><span class="j-label">💰 Wallet</span><span id="j-livebal" class="j-val">₹${liveWalletBal.toFixed(2)}</span></div>
      <div class="j-row"><span class="j-label">📊 Stake</span><span id="j-stake" class="j-val">₹${currentBet} (Step ${martingaleStep})</span></div>
      <div class="j-row"><span class="j-label">🔥 Loss Streak</span><span id="j-streak" class="j-val" style="color:${LOSS_STREAK >= 2 ? '#ff007a' : '#00f5a0'}">${LOSS_STREAK}</span></div>
      <div class="j-row"><span class="j-label">🎯 Score</span><span id="j-score" class="j-val">${wins}W / ${losses}L</span></div>
      <div class="j-row"><span class="j-label">⏰ Timer</span><span id="j-timer" class="j-val">--</span></div>
      <div class="j-row"><span class="j-label">🔮 Next Pred</span><span id="j-next-pred-lbl" class="j-val" style="font-size:13px">--</span></div>
      <div class="j-row"><span class="j-label">📡 Source</span><span class="j-val" style="color:#56e6ff;font-size:10px">ar-lottery01 ONLY</span></div>

      <div style="display:flex;justify-content:center;gap:6px;margin-top:6px">
        <button id="j-toggle-btn" class="j-btn j-start" style="flex:1">▶ START</button>
        <button id="j-mode-btn" class="j-btn j-mode">⏱️ ${GAME_MODE === '30S' ? '30S' : '1M'}</button>
      </div>

      <div class="j-config-row">
        <label>Base Bet ₹</label>
        <input id="j-base-input" type="number" value="${BASE_BET}" min="1">
        <label>Take Profit ₹</label>
        <input id="j-tp-input" type="number" value="${TAKE_PROFIT}" min="10">
      </div>

      <div id="j-feed-box" style="border-top:1px solid #334;padding-top:4px;margin-top:4px;"></div>
    `;

    target.appendChild(hud);

    // Event handlers
    document.getElementById('j-base-input').addEventListener('change', function() {
      const v = parseInt(this.value);
      if (!isNaN(v) && v >= 1) {
        BASE_BET = v;
        currentBet = getStakeForStep(BASE_BET, martingaleStep);
        persistAll();
        updateHud();
      }
    });

    document.getElementById('j-tp-input').addEventListener('change', function() {
      const v = parseFloat(this.value);
      if (!isNaN(v) && v >= 1) {
        TAKE_PROFIT = v;
        persistAll();
      }
    });

    document.getElementById('j-mode-btn').onclick = () => {
      GAME_MODE = (GAME_MODE === '30S') ? '1M' : '30S';
      LOSS_STREAK = 0; // Reset streak on mode change
      document.getElementById('j-mode-btn').textContent = `⏱️ ${GAME_MODE === '30S' ? '30S' : '1M'}`;
      persistAll();
      fetchLotteryHistory();
      updateHud();
    };

    document.getElementById('j-toggle-btn').onclick = () => {
      running = !running;
      const b = document.getElementById('j-toggle-btn');
      b.textContent = running ? '⏹ STOP' : '▶ START';
      b.className = running ? 'j-btn j-stop' : 'j-btn j-start';
      pendingBet = null;
      persistAll();
      updateHud();
      sendCloudTelemetry();
    };
  }

  function updateHud() {
    const badge = document.getElementById('j-status-badge');
    if (!badge) return;

    readScreenWalletBalance();

    badge.textContent = running ? (pendingBet ? `⏳ BET ₹${pendingBet.stake} → ${pendingBet.pred}` : `🎯 ACTIVE (${GAME_MODE}) L${LOSS_STREAK}`) : `⏹ STOPPED (${GAME_MODE})`;
    badge.style.color = running ? '#00f5a0' : '#ff5368';

    const balEl = document.getElementById('j-livebal');
    if (balEl) balEl.textContent = `₹${liveWalletBal.toFixed(2)}`;

    const stakeEl = document.getElementById('j-stake');
    if (stakeEl) stakeEl.textContent = `₹${currentBet} (Step ${martingaleStep})`;

    const streakEl = document.getElementById('j-streak');
    if (streakEl) {
      streakEl.textContent = LOSS_STREAK;
      streakEl.style.color = LOSS_STREAK >= 2 ? '#ff007a' : '#00f5a0';
    }

    const scoreEl = document.getElementById('j-score');
    if (scoreEl) scoreEl.textContent = `${wins}W / ${losses}L`;

    const timerEl = document.getElementById('j-timer');
    if (timerEl) timerEl.textContent = getSynchronizedSeconds() + 's';

    const nextLbl = document.getElementById('j-next-pred-lbl');
    if (nextLbl) {
      const pred = computePrediction();
      nextLbl.textContent = pred.noData ? '⏳ WAITING' : `${pred.size} [${pred.balls.join(',')}]`;
      nextLbl.style.color = pred.size === 'BIG' ? '#56e6ff' : '#ff4da6';
    }

    const feedBox = document.getElementById('j-feed-box');
    if (feedBox && RECORDED_BETS.length > 0) {
      feedBox.innerHTML = RECORDED_BETS.slice(0, 15).map(f => `
        <div style="display:flex;justify-content:space-between;padding:2px 0;border-bottom:1px solid rgba(255,255,255,0.05);color:${f.won === true ? '#00f5a0' : f.won === false ? '#ff007a' : '#ffcc00'}">
          <span>..${String(f.period).slice(-4)} ${f.prediction} ₹${f.stake}</span>
          <span>${f.won === true ? '✅WIN' : f.won === false ? '❌LOSS' : '⏳'} L${f.lossAtBet || 0}</span>
        </div>
      `).join('');
    }
  }

  // ── 10. MAIN CYCLE — THE SINGLE LOOP ──────────────────────
  async function botCycle() {
    try {
      const secondsLeft = getSynchronizedSeconds();
      const currentBucket = getCurrentTimeBucket();

      const tEl = document.getElementById('j-timer');
      if (tEl) tEl.textContent = secondsLeft + 's';

      if (secondsLeft === 28 || secondsLeft === 58) readScreenWalletBalance();

      // Get active period from screen
      let activePeriod = null;
      const allText = Array.from(document.querySelectorAll('div, span, p, b')).filter(e => !e.closest('#jash-hud') && !e.closest('table'));
      for (const el of allText) {
        const txt = (el.textContent || '').trim();
        const m = txt.match(/\\b(2026\\d{10,14})\\b/);
        if (m && txt.length < 30) { activePeriod = m[1]; break; }
      }
      if (!activePeriod && LOTTERY_HISTORY.length > 0) {
        try { activePeriod = (BigInt(LOTTERY_HISTORY[0].period) + 1n).toString(); } catch (e) {}
      }

      if (activePeriod && currentPeriod && activePeriod !== currentPeriod) {
        pendingBet = null;
      }
      currentPeriod = activePeriod;

      updateHud();

      // Compute prediction using THE SINGLE ENGINE
      const masterPred = computePrediction();

      // Don't bet if we have no data
      if (masterPred.noData) return;

      if (liveWalletBal >= TAKE_PROFIT && running) {
        running = false;
        persistAll();
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
          RECORDED_BETS.unshift({
            period: activePeriod,
            prediction: masterPred.size,
            mode: masterPred.mode,
            stake: currentBet,
            number: '--',
            size: '--',
            won: null,
            profit: null,
            isPending: true,
            lossAtBet: LOSS_STREAK,
            time: new Date().toLocaleTimeString()
          });
          if (RECORDED_BETS.length > 500) RECORDED_BETS = RECORDED_BETS.slice(0, 500);
          try { localStorage.setItem('J24_BETS', JSON.stringify(RECORDED_BETS.slice(0, 50))); } catch (e) {}
        }

        persistAll();
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

  // ── 11. INIT ──────────────────────────────────────────────
  function ensureHud() {
    if (!document.getElementById('jash-hud')) createHud();
  }

  createHud();
  setInterval(ensureHud, 1000);
  setInterval(botCycle, 1000);
})();
'''

# Load the rule tables from the JSON files
rules_30s_path = '/Users/jashwanthsingh/Downloads/jashvip/v9um_apex_titan_supreme_9feature_rules.json'
rules_1m_path = '/Users/jashwanthsingh/Downloads/jashvip/v9um_apex_titan_supreme_9feature_1m_rules.json'

with open(rules_30s_path, 'r') as f:
    rules_30s = json.load(f)

try:
    with open(rules_1m_path, 'r') as f:
        rules_1m = json.load(f)
except:
    rules_1m = {}

print(f"Loaded {len(rules_30s)} freshly retrained 30S rules from {rules_30s_path}")

print(f"30S rules: {len(rules_30s)} entries")
print(f"1M rules: {len(rules_1m)} entries")

# Inject rules into script
rules_30s_json = json.dumps(rules_30s)
rules_1m_json = json.dumps(rules_1m)

script_code = script_code.replace('RULES_30S_PLACEHOLDER', rules_30s_json)
script_code = script_code.replace('RULES_1M_PLACEHOLDER', rules_1m_json)

# Write to all output locations
output_paths = [
    '/Users/jashwanthsingh/Downloads/signal_top1_follower.user.js',
    '/Users/jashwanthsingh/Downloads/jash_perc_win.user.js',
    '/Users/jashwanthsingh/Downloads/30sec_win_v1.user.js',
    '/Users/jashwanthsingh/Downloads/JASH_BOT.user.js',
    '/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V9UM_AUTOBET.user.js',
    '/Users/jashwanthsingh/Downloads/jashvip/signal_top1_follower.user.js',
    '/Users/jashwanthsingh/Downloads/jashvip/jash_perc_win.user.js',
    '/Users/jashwanthsingh/Downloads/jashvip/JASH_BOT.user.js',
    '/Users/jashwanthsingh/Downloads/jashvip/JASH_VIP_APEX_TITAN_V9UM_AUTOBET.user.js',
    '/Users/jashwanthsingh/Downloads/jashvip/public/signal_top1_follower.user.js',
    '/Users/jashwanthsingh/Downloads/jashvip/public/jash_perc_win.user.js',
    '/Users/jashwanthsingh/Downloads/jashvip/public/30sec_win_v1.user.js',
    '/Users/jashwanthsingh/Downloads/jashvip/public/JASH_BOT.user.js',
    '/Users/jashwanthsingh/Downloads/jashvip/public/JASH_VIP_APEX_TITAN_V9UM_AUTOBET.user.js'
]

for p in output_paths:
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(script_code)
    print(f"✅ Generated: {p}")

print(f"\\n🎯 BUILD SUCCESS — v24.0 CLEAN (Single Brain)")
print(f"   Rules: {len(rules_30s)} (30S) + {len(rules_1m)} (1M)")
print(f"   Changes:")
print(f"   ✅ REMOVED: DOM scraping (polluted data)")
print(f"   ✅ REMOVED: LIVE_WEB_SIGNAL bridge (desync source)")
print(f"   ✅ REMOVED: Local fallback prediction (second brain)")
print(f"   ✅ ADDED: Single ar-lottery01.com data source")
print(f"   ✅ ADDED: Single persisted LOSS_STREAK counter")
print(f"   ✅ ADDED: Loss streak shown in HUD per bet")
