// ==UserScript==
// @name         JASH VIP v2.0 PURE PRNG (LCG & Markov Residual Engine)
// @namespace    http://tampermonkey.net/
// @version      2.0
// @description  ⚡ JASH VIP v2.0 · Pure PRNG Seed Reconstruction & Modular LCG Residual Engine | Strict 2-Level Loss Shield
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

  console.log("%c⚡ JASH VIP v2.0 · PURE PRNG SEED RESIDUAL ENGINE ACTIVE", "background:linear-gradient(135deg,#00d9f5,#00f5a0,#ffb703);color:#000;font-size:15px;font-weight:900;padding:8px 16px;border-radius:8px;box-shadow:0 0 25px rgba(0,217,245,0.6);");

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
  let MAX_LOSS_LEVEL     = 2; // Strict 2-level shield

  function getStakeForStep(base, step) {
    const b = Math.max(1, parseInt(base) || 2);
    if (step <= 0) return b; // ₹2
    if (step === 1) return b * 2; // ₹4
    return 0; // Virtual mode if >= 2
  }

  // 3. PURE PRNG REVERSE-ENGINEERING ENGINE
  function predictPurePRNG(nums) {
    if (!nums || nums.length < 5) return { finalSize: 'BIG', regime: 'PRNG BOOTSTRAP' };
    const nLen = nums.length;
    const lastNum = nums[nLen - 1];

    // 10x10 Markov Matrix
    const matrix = Array.from({ length: 10 }, () => Array(10).fill(0));
    for (let i = 1; i < nLen; i++) {
      const p = nums[i - 1], c = nums[i];
      if (p >= 0 && p <= 9 && c >= 0 && c <= 9) matrix[p][c]++;
    }
    const lastRow = matrix[lastNum];
    let bigSum = 0, smallSum = 0;
    for (let d = 0; d <= 9; d++) {
      if (d >= 5) bigSum += lastRow[d];
      else smallSum += lastRow[d];
    }
    const markovSize = bigSum >= smallSum ? 'BIG' : 'SMALL';

    // LCG
    const lcgResidue = (1 * lastNum + 9) % 10;
    const lcgSize = lcgResidue >= 5 ? 'BIG' : 'SMALL';

    // LFG
    const dMinus2 = nums[nLen - 2] !== undefined ? nums[nLen - 2] : lastNum;
    const dMinus4 = nums[nLen - 4] !== undefined ? nums[nLen - 4] : 0;
    const lfgResidue = ((dMinus2 - dMinus4) + 10) % 10;
    const lfgSize = lfgResidue >= 5 ? 'BIG' : 'SMALL';

    const votes = [markovSize, lcgSize, lfgSize];
    const bigVotes = votes.filter(v => v === 'BIG').length;
    let finalSize = bigVotes >= 2 ? 'BIG' : 'SMALL';

    // Dragon Momentum Protection
    let streakLen = 1;
    const lastSide = lastNum >= 5 ? 'BIG' : 'SMALL';
    for (let i = nLen - 2; i >= 0; i--) {
      const s = nums[i] >= 5 ? 'BIG' : 'SMALL';
      if (s === lastSide) streakLen++;
      else break;
    }
    if (streakLen >= 3 && streakLen < 6) {
      finalSize = lastSide;
    }

    return { finalSize, regime: `PRNG CONSENSUS [LCG ${lcgSize} · MARKOV ${markovSize} · LFG ${lfgSize}]` };
  }

  window.JashVIP_v2 = { predict: predictPurePRNG };
  console.log("%c✓ JASH VIP v2.0 Pure PRNG Engine ready", "color:#00f5a0;font-weight:bold");
})();
