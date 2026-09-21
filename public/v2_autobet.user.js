// ==UserScript==
// @name         JASH VIP v2.0 TITAN (30-Trend Studocu Markov Engine)
// @namespace    http://tampermonkey.net/
// @version      2.0
// @description  ⚡ JASH VIP v2.0 TITAN · Powered by Studocu 30-Trend Markov Connection Engine | Dragon-Lock Protection | Strict 2-Level Shield
// @match        *://*.in999vv.com/*
// @match        *://*.in999*.com/*
// @match        *://*.us3b7o.com/*
// @match        *://*.dmfirst0.com/*
// @match        *://*.dmfirst*.com/*
// @match        *://*/*
// @grant        none
// @run-at       document-start
// ==/UserScript==

(function () {
  'use strict';

  if (window.__JASH_VIP_V2_LOCK__) return;
  window.__JASH_VIP_V2_LOCK__ = true;

  console.log("%c⚡ JASH VIP v2.0 TITAN · 30-TREND STUDOCU MARKOV ENGINE ACTIVE", "background:linear-gradient(135deg,#00d9f5,#a855f7,#00f5a0);color:#000;font-size:15px;font-weight:900;padding:8px 16px;border-radius:8px;box-shadow:0 0 25px rgba(0,217,245,0.6);");

  // 1. WAKE LOCK
  let wakeLockObj = null;
  async function requestWakeLock() {
    try {
      if ('wakeLock' in navigator) wakeLockObj = await navigator.wakeLock.request('screen');
    } catch (e) {}
  }
  setInterval(requestWakeLock, 8000);
  requestWakeLock();

  // 2. CONFIG & STATE
  let GAME_MODE          = localStorage.getItem('J2_MODE') || '30S';
  let BASE_BET           = parseInt(localStorage.getItem('J2_BASE_BET')) || 2;
  let START_BANKROLL     = parseFloat(localStorage.getItem('J2_START_BANKROLL')) || 400.00;
  let TAKE_PROFIT_TARGET = parseFloat(localStorage.getItem('J2_TAKE_PROFIT')) || 50000.00;
  let MAX_LOSS_LEVEL     = 2; // Strict 2-level shield

  function getStakeForStep(base, step) {
    const b = Math.max(1, parseInt(base) || 2);
    if (step <= 0) return b; // ₹2
    if (step === 1) return b * 2; // ₹4
    return 0; // Virtual mode if >= 2
  }

  let AUTOBET_ACTIVE  = (localStorage.getItem('J2_AUTOBET') === 'true');
  let LOSS_STREAK     = 0;
  let IS_VIRTUAL_MODE = false;
  let TOTAL_WINS      = 0;
  let TOTAL_LOSSES    = 0;
  let SHIELD_SAVES    = 0;

  // 3. 30 STUDOCU TRENDS CATALOG
  const TRENDS = {
    1:  { name: "6-BIG DRAGON", pat: ["BIG","BIG","BIG","BIG","BIG","BIG"], next: 2 },
    2:  { name: "6-SMALL DRAGON", pat: ["SMALL","SMALL","SMALL","SMALL","SMALL","SMALL"], next: 3 },
    3:  { name: "1-1 ZIGZAG (B)", pat: ["BIG","SMALL","BIG","SMALL","BIG","SMALL"], next: 4 },
    4:  { name: "1-1 ZIGZAG (S)", pat: ["SMALL","BIG","SMALL","BIG","SMALL","BIG"], next: 5 },
    5:  { name: "2-1 RHYTHM (B)", pat: ["BIG","BIG","SMALL","BIG","BIG","SMALL"], next: 6 },
    6:  { name: "2-1 RHYTHM (S)", pat: ["SMALL","SMALL","BIG","SMALL","SMALL","BIG"], next: 7 },
    7:  { name: "3-3 MIRROR (B)", pat: ["BIG","BIG","BIG","SMALL","SMALL","SMALL"], next: 8 },
    8:  { name: "3-3 MIRROR (S)", pat: ["SMALL","SMALL","SMALL","BIG","BIG","BIG"], next: 9 },
    9:  { name: "1-2 RHYTHM (B)", pat: ["BIG","SMALL","SMALL","BIG","SMALL","SMALL"], next: 10 },
    10: { name: "1-2 RHYTHM (S)", pat: ["SMALL","BIG","BIG","SMALL","BIG","BIG"], next: 11 },
    11: { name: "2-2 RHYTHM (B)", pat: ["BIG","BIG","SMALL","SMALL","BIG","BIG"], next: 12 },
    12: { name: "2-2 RHYTHM (S)", pat: ["SMALL","SMALL","BIG","BIG","SMALL","SMALL"], next: 13 },
    13: { name: "ALT-DOUBLE (B)", pat: ["BIG","SMALL","BIG","BIG","SMALL","BIG"], next: 14 },
    14: { name: "ALT-DOUBLE (S)", pat: ["SMALL","BIG","SMALL","SMALL","BIG","SMALL"], next: 15 },
    15: { name: "4-2 SHIFT (B)", pat: ["BIG","BIG","BIG","BIG","SMALL","SMALL"], next: 16 },
    16: { name: "4-2 SHIFT (S)", pat: ["SMALL","SMALL","SMALL","SMALL","BIG","BIG"], next: 17 },
    17: { name: "CHOPPER-LOCK (B)", pat: ["BIG","SMALL","BIG","SMALL","SMALL","BIG"], next: 18 },
    18: { name: "CHOPPER-LOCK (S)", pat: ["SMALL","BIG","SMALL","BIG","BIG","SMALL"], next: 19 },
    19: { name: "1-3-2 PULSE (B)", pat: ["BIG","SMALL","SMALL","SMALL","BIG","BIG"], next: 20 },
    20: { name: "1-3-2 PULSE (S)", pat: ["SMALL","BIG","BIG","BIG","SMALL","SMALL"], next: 21 },
    21: { name: "2-3-1 FLIP (B)", pat: ["BIG","BIG","SMALL","SMALL","SMALL","BIG"], next: 22 },
    22: { name: "1-3-1-1 FLIP (S)", pat: ["SMALL","BIG","BIG","BIG","SMALL","BIG"], next: 23 },
    23: { name: "1-1-3-1 FLIP (B)", pat: ["BIG","SMALL","BIG","BIG","BIG","SMALL"], next: 24 },
    24: { name: "2-1-1-1-1 S-RUN", pat: ["SMALL","SMALL","BIG","SMALL","BIG","SMALL"], next: 25 },
    25: { name: "1-4-1 DRAGON-END (B)", pat: ["BIG","SMALL","SMALL","SMALL","SMALL","BIG"], next: 26 },
    26: { name: "1-4-1 DRAGON-END (S)", pat: ["SMALL","BIG","BIG","BIG","BIG","SMALL"], next: 27 },
    27: { name: "3-1-1-1 SURGE (B)", pat: ["BIG","BIG","BIG","SMALL","BIG","SMALL"], next: 28 },
    28: { name: "3-1-1-1 SURGE (S)", pat: ["SMALL","SMALL","SMALL","BIG","SMALL","BIG"], next: 29 },
    29: { name: "1-1-1-3 SURGE (B)", pat: ["BIG","SMALL","BIG","SMALL","SMALL","SMALL"], next: 30 },
    30: { name: "1-1-1-3 SURGE (S)", pat: ["SMALL","BIG","SMALL","BIG","BIG","BIG"], next: 1 }
  };

  const CHAINS = {};
  for (const [tid, tinfo] of Object.entries(TRENDS)) {
    const nxtId = tinfo.next;
    CHAINS[tid] = {
      name: tinfo.name,
      next_name: TRENDS[nxtId].name,
      next_id: nxtId,
      full_chain: [...tinfo.pat, ...TRENDS[nxtId].pat]
    };
  }

  function predictV2(sizes) {
    if (!sizes || sizes.length === 0) return { finalSize: 'BIG', regime: 'INIT' };
    const lastSide = sizes[sizes.length - 1];
    let streakLen = 1;
    for (let i = sizes.length - 2; i >= 0; i--) {
      if (sizes[i] === lastSide) streakLen++;
      else break;
    }

    if (streakLen >= 3 && streakLen < 6) {
      return { finalSize: lastSide, regime: `DRAGON MOMENTUM [${streakLen}]` };
    }

    for (const k of [6, 5, 4, 3, 2]) {
      const sub = sizes.slice(-k);
      const matches = [];
      for (const [tid, cinfo] of Object.entries(CHAINS)) {
        const chain = cinfo.full_chain;
        for (let pos = 0; pos <= chain.length - k - 1; pos++) {
          let match = true;
          for (let j = 0; j < k; j++) {
            if (chain[pos + j] !== sub[j]) { match = false; break; }
          }
          if (match) matches.push(chain[pos + k]);
        }
      }
      if (matches.length > 0) {
        const counts = {};
        matches.forEach(m => counts[m] = (counts[m] || 0) + 1);
        const topPred = Object.keys(counts).reduce((a, b) => counts[a] >= counts[b] ? a : b);
        return { finalSize: topPred, regime: `TREND LOCK [K=${k}]` };
      }
    }

    return { finalSize: lastSide, regime: 'CONTINUITY SYNC' };
  }

  window.JashVIP_v2 = {
    predict: predictV2,
    trends: TRENDS
  };

  console.log("%c✓ JASH VIP v2.0 Engine ready", "color:#00f5a0;font-weight:bold");
})();
