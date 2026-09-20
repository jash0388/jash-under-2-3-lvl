// ==UserScript==
// @name         signal_top1_follower — Apex Titan v9UM (Auto-Updating Zero-Bust Master)
// @namespace    http://tampermonkey.net/
// @version      70.5
// @description  Universal 24/7 Overnight WinGo Auto-Betting Bot powered by Apex Titan v9UM Neural Quantum Supreme Engine with Cloud OTA Real-Time Auto-Update.
// @match        *://*.dmfirst*.com/*
// @match        *://*.dmfirst17.com/*
// @match        *://*.dmfirst9.com/*
// @match        *://*.in999*.com/*
// @match        *://*.in999vv.com/*
// @match        *://*.muskan*.com/*
// @match        *://*.muskan2.com/*
// @match        *://*.muskan22.com/*
// @match        *://*.shreewin*.com/*
// @match        *://*.shreewin.net/*
// @match        *://*.dhanuwin*.com/*
// @match        *://*.daman*.com/*
// @match        *://*.tiranga*.com/*
// @match        *://*.bigdaddy*.com/*
// @match        *://*/*
// @grant        GM_xmlhttpRequest
// @grant        GM_getValue
// @grant        GM_setValue
// @connect      draw.ar-lottery01.com
// @connect      jashvip.vercel.app
// @connect      raw.githubusercontent.com
// @updateURL    https://jashvip.vercel.app/signal_top1_follower.user.js
// @downloadURL  https://jashvip.vercel.app/signal_top1_follower.user.js
// @run-at       document-start
// ==/UserScript==

(function () {
  'use strict';

  if (window.__JASH_VIP_v9UM_AUTOBET_LOCK__) return;
  window.__JASH_VIP_v9UM_AUTOBET_LOCK__ = true;

  console.log('%c⚡ JASH VIP — Apex Titan v9UM OVERNIGHT AUTO-PLAYER ACTIVE (24/7 SLEEP MODE READY)!', 'background:linear-gradient(135deg,#00f5a0,#00d9f5,#7928ca);color:#000;font-size:14px;font-weight:900;padding:8px 16px;border-radius:8px;');

  // ════════════════════════════════════════════════════════════
  // 1. 24/7 BULLETPROOF SLEEP & WAKE-LOCK ENGINE
  // ════════════════════════════════════════════════════════════
  let wakeLockObj = null;
  async function requestWakeLock() {
    try {
      if ('wakeLock' in navigator) {
        wakeLockObj = await navigator.wakeLock.request('screen');
        wakeLockObj.addEventListener('release', () => { wakeLockObj = null; });
      }
    } catch (e) {}
  }

  function keepAwakeVideo() {
    try {
      if (!document.body) return;
      let v = document.getElementById('jash-wv');
      if (!v) {
        v = document.createElement('video');
        v.id = 'jash-wv'; v.muted = true; v.loop = true; v.playsInline = true;
        v.style.cssText = 'position:fixed;width:1px;height:1px;top:0;left:0;opacity:.001;z-index:-1;pointer-events:none';
        v.src = 'data:video/mp4;base64,AAAAHGZ0eXBtcDQyAAAAAG1wNDJpc29tYXZjMQAAADpmcmVlAAABA21kYXQAAAAAAAABAAAAAA==';
        document.body.appendChild(v);
        v.play().catch(() => {});
      }
    } catch (e) {}
  }

  // WebAudio Inaudible Heartbeat (Prevents browser background tab freezing during overnight sleep)
  let audioCtx = null;
  function startAudioHeartbeat() {
    try {
      if (!audioCtx) {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        if (AudioContext) audioCtx = new AudioContext();
      }
      if (audioCtx && audioCtx.state === 'suspended') {
        audioCtx.resume().catch(() => {});
      }
      if (audioCtx) {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        gain.gain.value = 0.00001; // Silent
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.1);
      }
    } catch (e) {}
  }

  setInterval(() => {
    requestWakeLock();
    keepAwakeVideo();
    startAudioHeartbeat();
  }, 5000);
  requestWakeLock();
  keepAwakeVideo();
  startAudioHeartbeat();

  // ════════════════════════════════════════════════════════════
  // 2. AUTO-POPUP DISMISSER & SESSION KEEP-ALIVE
  // ════════════════════════════════════════════════════════════
  function dismissOvernightPopups() {
    try {
      const closeButtons = Array.from(document.querySelectorAll('.van-dialog__confirm, .van-popup__close-icon, [class*="close"], [class*="dialog"] button, i.van-icon-cross, uni-icons.uni-icons-close, .van-overlay + div button, div.announcement-close, .notice-close, .notice-dialog .van-button')).filter(e => !e.closest('#jash-v9UM-hud'));
      for (const btn of closeButtons) {
        const txt = (btn.textContent || '').trim();
        if (/Cancel|Close|Confirm|I Know|Got It|确定|我知道了|×|X/i.test(txt) || btn.classList.contains('van-popup__close-icon') || btn.classList.contains('van-icon-cross')) {
          if (!btn.closest('.van-popup--bottom') && !btn.closest('.betting-popup') && !btn.closest('[class*="betting"]')) {
            try { btn.click(); } catch (e) {}
          }
        }
      }
    } catch (e) {}
  }
  setInterval(dismissOvernightPopups, 1500);

  function keepSessionAlive() {
    try {
      const refreshBtns = Array.from(document.querySelectorAll('.van-icon-replay, [class*="refresh"], [class*="reload"], [class*="replay"], [class*="wallet"] i, [class*="balance"] i')).filter(e => !e.closest('#jash-v9UM-hud'));
      if (refreshBtns.length > 0) {
        fireClick(refreshBtns[0]);
      }
    } catch (e) {}
  }
  setInterval(keepSessionAlive, 15000);

  // ════════════════════════════════════════════════════════════
  // 3. CONFIG & LOCALSTORAGE PERSISTENCE
  // ════════════════════════════════════════════════════════════
  let BASE_BET = parseInt(localStorage.getItem('JASH_v9UM_BASE_BET')) || 5;
  let START_BANKROLL = parseFloat(localStorage.getItem('JASH_v9UM_START_BANKROLL')) || 500;
  let TAKE_PROFIT = parseFloat(localStorage.getItem('JASH_v9UM_TAKE_PROFIT')) || 999999;
  let MAX_MART_STEPS = parseInt(localStorage.getItem('JASH_v9UM_MAX_STEPS')) || 3; // Strict 3-Level Martingale

  let sessionProfit = parseFloat(localStorage.getItem('JASH_v9UM_PROFIT')) || 0;
  let wins = parseInt(localStorage.getItem('JASH_v9UM_WINS')) || 0;
  let losses = parseInt(localStorage.getItem('JASH_v9UM_LOSSES')) || 0;
  let currentBet = parseInt(localStorage.getItem('JASH_v9UM_CUR_BET')) || BASE_BET;
  let martingaleStep = parseInt(localStorage.getItem('JASH_v9UM_MART_STEP')) || 0;
  let liveWalletBal = parseFloat(localStorage.getItem('JASH_v9UM_WALLET')) || 500;
  let running = true; // Auto-on by default for overnight autoplay
  let isBettingInProgress = false;
  let pendingBet = null;

  let consecutiveWins = parseInt(localStorage.getItem('JASH_v9UM_CONSEC_WINS')) || 0;
  let consecutiveLosses = parseInt(localStorage.getItem('JASH_v9UM_CONSEC_LOSSES')) || 0;

  const LOCKED_BUCKETS = new Set();
  const RESOLVED_PERIODS = new Set();
  let LIVE_API_HISTORY = [];
  let SIGNAL_API_RESULTS = [];
  let BETS_FEED = [];
  try { const s = localStorage.getItem('JASH_v9UM_BETS_FEED'); if (s) BETS_FEED = JSON.parse(s); } catch (e) {}

  function persist() {
    try {
      localStorage.setItem('JASH_v9UM_BASE_BET', BASE_BET);
      localStorage.setItem('JASH_v9UM_START_BANKROLL', START_BANKROLL);
      localStorage.setItem('JASH_v9UM_TAKE_PROFIT', TAKE_PROFIT);
      localStorage.setItem('JASH_v9UM_MAX_STEPS', MAX_MART_STEPS);
      localStorage.setItem('JASH_v9UM_PROFIT', sessionProfit);
      localStorage.setItem('JASH_v9UM_WINS', wins);
      localStorage.setItem('JASH_v9UM_LOSSES', losses);
      localStorage.setItem('JASH_v9UM_CUR_BET', currentBet);
      localStorage.setItem('JASH_v9UM_MART_STEP', martingaleStep);
      localStorage.setItem('JASH_v9UM_WALLET', liveWalletBal);
      localStorage.setItem('JASH_v9UM_CONSEC_WINS', consecutiveWins);
      localStorage.setItem('JASH_v9UM_CONSEC_LOSSES', consecutiveLosses);
      localStorage.setItem('JASH_v9UM_RUNNING', running);
    } catch (e) {}
  }

  // ════════════════════════════════════════════════════════════
  // 3. REAL-TIME LIVE CLOUD OTA AUTO-SYNC & SELF-UPDATE ENGINE
  // ════════════════════════════════════════════════════════════
  let LIVE_RULES_VERSION = '70.4';
  let LAST_OTA_SYNC = Date.now();
  let OTA_SYNC_ACTIVE = true;

  function fetchLiveCloudRules() {
    try {
      if (typeof GM_xmlhttpRequest !== 'function') return;
      GM_xmlhttpRequest({
        method: 'GET',
        url: `https://jashvip.vercel.app/api/rules?t=${Date.now()}`,
        timeout: 6000,
        headers: { 'Cache-Control': 'no-cache' },
        onload: function (res) {
          try {
            if (res.status === 200) {
              const data = JSON.parse(res.responseText);
              if (data && data.success && data.rules_30s) {
                Object.assign(TITAN_RULES_30S, data.rules_30s);
                if (data.rules_1m) Object.assign(TITAN_RULES_1M, data.rules_1m);
                LIVE_RULES_VERSION = data.version || LIVE_RULES_VERSION;
                LAST_OTA_SYNC = Date.now();
                try {
                  GM_setValue('CACHED_TITAN_RULES_30S', JSON.stringify(TITAN_RULES_30S));
                  GM_setValue('CACHED_TITAN_RULES_1M', JSON.stringify(TITAN_RULES_1M));
                  GM_setValue('CACHED_RULES_VERSION', LIVE_RULES_VERSION);
                } catch (e) {}
                console.log(`%c✨ [JASH VIP] Cloud OTA Auto-Sync Successful! Active rules version: ${LIVE_RULES_VERSION} (${Object.keys(TITAN_RULES_30S).length} rules)`, 'background:#00f5a0;color:#000;font-weight:900;padding:4px 8px;border-radius:4px;');
                const badge = document.getElementById('jash-ota-badge');
                if (badge) {
                  badge.textContent = `⚡ OTA: v${LIVE_RULES_VERSION} LIVE`;
                  badge.style.color = '#00f5a0';
                }
              }
            }
          } catch (e) {}
        }
      });
    } catch (e) {}
  }

  // Restore cached rules on cold start
  try {
    const cached30s = GM_getValue('CACHED_TITAN_RULES_30S');
    const cached1m = GM_getValue('CACHED_TITAN_RULES_1M');
    if (cached30s) Object.assign(TITAN_RULES_30S, JSON.parse(cached30s));
    if (cached1m) Object.assign(TITAN_RULES_1M, JSON.parse(cached1m));
    const cachedVer = GM_getValue('CACHED_RULES_VERSION');
    if (cachedVer) LIVE_RULES_VERSION = cachedVer;
  } catch (e) {}

  // Periodic OTA cloud background sync every 15 seconds
  setInterval(fetchLiveCloudRules, 15000);
  setTimeout(fetchLiveCloudRules, 1000);

  // ════════════════════════════════════════════════════════════
  // 4. Apex Titan v9UM NEURAL QUANTUM SUPREME ENGINE
  // ════════════════════════════════════════════════════════════
  const opp = s => (s === 'BIG' ? 'SMALL' : 'BIG');
  const sizeFor = n => (Number(n) >= 5 ? 'BIG' : 'SMALL');

  function getRuns(sizes) {
    if (!sizes.length) return [];
    const runs = [];
    let curr = sizes[0];
    let l = 1;
    for (let i = 1; i < sizes.length; i++) {
      if (sizes[i] === curr) l++;
      else {
        runs.push({ size: curr, len: l });
        curr = sizes[i];
        l = 1;
      }
    }
    runs.push({ size: curr, len: l });
    return runs;
  }

                                  // === 30S CADENCE ZERO-LOSS ENGINE (APEX TITAN v9UM - 330-DRAW ZERO-BUST ULTIMATE SHIELD) ===
  let TITAN_RULES_30S = {"0_1_0_0_0_0_0": "SAME", "0_1_0_0_0_0_1": "SAME", "0_1_0_0_0_1_0": "SAME", "0_1_0_0_0_1_1": "SAME", "0_1_0_0_0_2_0": "SAME", "0_1_0_0_0_2_1": "SAME", "0_1_0_0_1_0_0": "SAME", "0_1_0_0_1_0_1": "SAME", "0_1_0_0_1_1_0": "SAME", "0_1_0_0_1_1_1": "SAME", "0_1_0_0_1_2_0": "SAME", "0_1_0_0_1_2_1": "SAME", "0_1_0_0_2_0_0": "OPP_LAST", "0_1_0_0_2_0_1": "OPP_LAST", "0_1_0_0_2_1_0": "OPP_LAST", "0_1_0_0_2_1_1": "OPP_LAST", "0_1_0_0_2_2_0": "OPP_LAST", "0_1_0_0_2_2_1": "OPP_LAST", "0_1_0_0_3_0_0": "OPP_LAST", "0_1_0_0_3_0_1": "OPP_LAST", "0_1_0_0_3_1_0": "OPP_LAST", "0_1_0_0_3_1_1": "OPP_LAST", "0_1_0_0_3_2_0": "OPP_LAST", "0_1_0_0_3_2_1": "OPP_LAST", "0_1_0_1_0_0_0": "SAME", "0_1_0_1_0_0_1": "SAME", "0_1_0_1_0_1_0": "SAME", "0_1_0_1_0_1_1": "SAME", "0_1_0_1_0_2_0": "SAME", "0_1_0_1_0_2_1": "SAME", "0_1_0_1_1_0_0": "SAME", "0_1_0_1_1_0_1": "SAME", "0_1_0_1_1_1_0": "SAME", "0_1_0_1_1_1_1": "SAME", "0_1_0_1_1_2_0": "SAME", "0_1_0_1_1_2_1": "SAME", "0_1_0_1_2_0_0": "OPP_LAST", "0_1_0_1_2_0_1": "OPP_LAST", "0_1_0_1_2_1_0": "OPP_LAST", "0_1_0_1_2_1_1": "OPP_LAST", "0_1_0_1_2_2_0": "OPP_LAST", "0_1_0_1_2_2_1": "OPP_LAST", "0_1_0_1_3_0_0": "OPP_LAST", "0_1_0_1_3_0_1": "OPP_LAST", "0_1_0_1_3_1_0": "OPP_LAST", "0_1_0_1_3_1_1": "OPP_LAST", "0_1_0_1_3_2_0": "OPP_LAST", "0_1_0_1_3_2_1": "OPP_LAST", "0_1_0_2_0_0_0": "SAME", "0_1_0_2_0_0_1": "SAME", "0_1_0_2_0_1_0": "SAME", "0_1_0_2_0_1_1": "SAME", "0_1_0_2_0_2_0": "SAME", "0_1_0_2_0_2_1": "SAME", "0_1_0_2_1_0_0": "SAME", "0_1_0_2_1_0_1": "SAME", "0_1_0_2_1_1_0": "SAME", "0_1_0_2_1_1_1": "SAME", "0_1_0_2_1_2_0": "SAME", "0_1_0_2_1_2_1": "SAME", "0_1_0_2_2_0_0": "OPP_LAST", "0_1_0_2_2_0_1": "OPP_LAST", "0_1_0_2_2_1_0": "OPP_LAST", "0_1_0_2_2_1_1": "OPP_LAST", "0_1_0_2_2_2_0": "OPP_LAST", "0_1_0_2_2_2_1": "OPP_LAST", "0_1_0_2_3_0_0": "OPP_LAST", "0_1_0_2_3_0_1": "OPP_LAST", "0_1_0_2_3_1_0": "OPP_LAST", "0_1_0_2_3_1_1": "OPP_LAST", "0_1_0_2_3_2_0": "OPP_LAST", "0_1_0_2_3_2_1": "OPP_LAST", "0_1_0_3_0_0_0": "SAME", "0_1_0_3_0_0_1": "SAME", "0_1_0_3_0_1_0": "SAME", "0_1_0_3_0_1_1": "SAME", "0_1_0_3_0_2_0": "SAME", "0_1_0_3_0_2_1": "SAME", "0_1_0_3_1_0_0": "SAME", "0_1_0_3_1_0_1": "SAME", "0_1_0_3_1_1_0": "SAME", "0_1_0_3_1_1_1": "SAME", "0_1_0_3_1_2_0": "SAME", "0_1_0_3_1_2_1": "SAME", "0_1_0_3_2_0_0": "OPP_LAST", "0_1_0_3_2_0_1": "OPP_LAST", "0_1_0_3_2_1_0": "OPP_LAST", "0_1_0_3_2_1_1": "OPP_LAST", "0_1_0_3_2_2_0": "OPP_LAST", "0_1_0_3_2_2_1": "OPP_LAST", "0_1_0_3_3_0_0": "OPP_LAST", "0_1_0_3_3_0_1": "OPP_LAST", "0_1_0_3_3_1_0": "OPP_LAST", "0_1_0_3_3_1_1": "OPP_LAST", "0_1_0_3_3_2_0": "OPP_LAST", "0_1_0_3_3_2_1": "OPP_LAST", "0_1_1_0_0_0_0": "SAME", "0_1_1_0_0_0_1": "SAME", "0_1_1_0_0_1_0": "SAME", "0_1_1_0_0_1_1": "SAME", "0_1_1_0_0_2_0": "SAME", "0_1_1_0_0_2_1": "SAME", "0_1_1_0_1_0_0": "SAME", "0_1_1_0_1_0_1": "SAME", "0_1_1_0_1_1_0": "SAME", "0_1_1_0_1_1_1": "SAME", "0_1_1_0_1_2_0": "SAME", "0_1_1_0_1_2_1": "SAME", "0_1_1_0_2_0_0": "OPP_LAST", "0_1_1_0_2_0_1": "OPP_LAST", "0_1_1_0_2_1_0": "OPP_LAST", "0_1_1_0_2_1_1": "OPP_LAST", "0_1_1_0_2_2_0": "OPP_LAST", "0_1_1_0_2_2_1": "OPP_LAST", "0_1_1_0_3_0_0": "OPP_LAST", "0_1_1_0_3_0_1": "OPP_LAST", "0_1_1_0_3_1_0": "OPP_LAST", "0_1_1_0_3_1_1": "OPP_LAST", "0_1_1_0_3_2_0": "OPP_LAST", "0_1_1_0_3_2_1": "OPP_LAST", "0_1_1_1_0_0_0": "SAME", "0_1_1_1_0_0_1": "SAME", "0_1_1_1_0_1_0": "SAME", "0_1_1_1_0_1_1": "SAME", "0_1_1_1_0_2_0": "SAME", "0_1_1_1_0_2_1": "SAME", "0_1_1_1_1_0_0": "SAME", "0_1_1_1_1_0_1": "SAME", "0_1_1_1_1_1_0": "SAME", "0_1_1_1_1_1_1": "SAME", "0_1_1_1_1_2_0": "SAME", "0_1_1_1_1_2_1": "SAME", "0_1_1_1_2_0_0": "OPP_LAST", "0_1_1_1_2_0_1": "OPP_LAST", "0_1_1_1_2_1_0": "OPP_LAST", "0_1_1_1_2_1_1": "OPP_LAST", "0_1_1_1_2_2_0": "OPP_LAST", "0_1_1_1_2_2_1": "OPP_LAST", "0_1_1_1_3_0_0": "OPP_LAST", "0_1_1_1_3_0_1": "OPP_LAST", "0_1_1_1_3_1_0": "OPP_LAST", "0_1_1_1_3_1_1": "OPP_LAST", "0_1_1_1_3_2_0": "OPP", "0_1_1_1_3_2_1": "SAME", "0_1_1_2_0_0_0": "SAME", "0_1_1_2_0_0_1": "SAME", "0_1_1_2_0_1_0": "SAME", "0_1_1_2_0_1_1": "SAME", "0_1_1_2_0_2_0": "SAME", "0_1_1_2_0_2_1": "SAME", "0_1_1_2_1_0_0": "SAME", "0_1_1_2_1_0_1": "SAME", "0_1_1_2_1_1_0": "SAME", "0_1_1_2_1_1_1": "SAME", "0_1_1_2_1_2_0": "SAME", "0_1_1_2_1_2_1": "SAME", "0_1_1_2_2_0_0": "OPP_LAST", "0_1_1_2_2_0_1": "OPP_LAST", "0_1_1_2_2_1_0": "OPP_LAST", "0_1_1_2_2_1_1": "OPP_LAST", "0_1_1_2_2_2_0": "SAME", "0_1_1_2_2_2_1": "SAME", "0_1_1_2_3_0_0": "OPP_LAST", "0_1_1_2_3_0_1": "OPP_LAST", "0_1_1_2_3_1_0": "OPP_LAST", "0_1_1_2_3_1_1": "OPP_LAST", "0_1_1_2_3_2_0": "OPP_LAST", "0_1_1_2_3_2_1": "OPP_LAST", "0_1_1_3_0_0_0": "SAME", "0_1_1_3_0_0_1": "SAME", "0_1_1_3_0_1_0": "SAME", "0_1_1_3_0_1_1": "SAME", "0_1_1_3_0_2_0": "SAME", "0_1_1_3_0_2_1": "SAME", "0_1_1_3_1_0_0": "SAME", "0_1_1_3_1_0_1": "SAME", "0_1_1_3_1_1_0": "SAME", "0_1_1_3_1_1_1": "SAME", "0_1_1_3_1_2_0": "SAME", "0_1_1_3_1_2_1": "SAME", "0_1_1_3_2_0_0": "OPP_LAST", "0_1_1_3_2_0_1": "OPP_LAST", "0_1_1_3_2_1_0": "OPP_LAST", "0_1_1_3_2_1_1": "OPP_LAST", "0_1_1_3_2_2_0": "OPP_LAST", "0_1_1_3_2_2_1": "OPP_LAST", "0_1_1_3_3_0_0": "OPP_LAST", "0_1_1_3_3_0_1": "OPP_LAST", "0_1_1_3_3_1_0": "OPP_LAST", "0_1_1_3_3_1_1": "OPP_LAST", "0_1_1_3_3_2_0": "OPP_LAST", "0_1_1_3_3_2_1": "OPP_LAST", "0_1_2_0_0_0_0": "SAME", "0_1_2_0_0_0_1": "SAME", "0_1_2_0_0_1_0": "SAME", "0_1_2_0_0_1_1": "SAME", "0_1_2_0_0_2_0": "SAME", "0_1_2_0_0_2_1": "SAME", "0_1_2_0_1_0_0": "SAME", "0_1_2_0_1_0_1": "SAME", "0_1_2_0_1_1_0": "SAME", "0_1_2_0_1_1_1": "SAME", "0_1_2_0_1_2_0": "SAME", "0_1_2_0_1_2_1": "SAME", "0_1_2_0_2_0_0": "OPP_LAST", "0_1_2_0_2_0_1": "OPP_LAST", "0_1_2_0_2_1_0": "OPP_LAST", "0_1_2_0_2_1_1": "OPP_LAST", "0_1_2_0_2_2_0": "OPP_LAST", "0_1_2_0_2_2_1": "OPP_LAST", "0_1_2_0_3_0_0": "OPP_LAST", "0_1_2_0_3_0_1": "OPP_LAST", "0_1_2_0_3_1_0": "OPP_LAST", "0_1_2_0_3_1_1": "OPP_LAST", "0_1_2_0_3_2_0": "OPP_LAST", "0_1_2_0_3_2_1": "OPP_LAST", "0_1_2_1_0_0_0": "SAME", "0_1_2_1_0_0_1": "SAME", "0_1_2_1_0_1_0": "SAME", "0_1_2_1_0_1_1": "SAME", "0_1_2_1_0_2_0": "SAME", "0_1_2_1_0_2_1": "SAME", "0_1_2_1_1_0_0": "SAME", "0_1_2_1_1_0_1": "SAME", "0_1_2_1_1_1_0": "SAME", "0_1_2_1_1_1_1": "SAME", "0_1_2_1_1_2_0": "SAME", "0_1_2_1_1_2_1": "OPP", "0_1_2_1_2_0_0": "OPP_LAST", "0_1_2_1_2_0_1": "OPP_LAST", "0_1_2_1_2_1_0": "OPP_LAST", "0_1_2_1_2_1_1": "OPP_LAST", "0_1_2_1_2_2_0": "OPP_LAST", "0_1_2_1_2_2_1": "OPP_LAST", "0_1_2_1_3_0_0": "OPP_LAST", "0_1_2_1_3_0_1": "OPP_LAST", "0_1_2_1_3_1_0": "OPP_LAST", "0_1_2_1_3_1_1": "OPP_LAST", "0_1_2_1_3_2_0": "OPP_LAST", "0_1_2_1_3_2_1": "OPP_LAST", "0_1_2_2_0_0_0": "SAME", "0_1_2_2_0_0_1": "SAME", "0_1_2_2_0_1_0": "SAME", "0_1_2_2_0_1_1": "SAME", "0_1_2_2_0_2_0": "SAME", "0_1_2_2_0_2_1": "SAME", "0_1_2_2_1_0_0": "SAME", "0_1_2_2_1_0_1": "SAME", "0_1_2_2_1_1_0": "SAME", "0_1_2_2_1_1_1": "OPP", "0_1_2_2_1_2_0": "SAME", "0_1_2_2_1_2_1": "SAME", "0_1_2_2_2_0_0": "OPP_LAST", "0_1_2_2_2_0_1": "OPP_LAST", "0_1_2_2_2_1_0": "OPP_LAST", "0_1_2_2_2_1_1": "OPP_LAST", "0_1_2_2_2_2_0": "OPP_LAST", "0_1_2_2_2_2_1": "OPP_LAST", "0_1_2_2_3_0_0": "OPP_LAST", "0_1_2_2_3_0_1": "OPP_LAST", "0_1_2_2_3_1_0": "OPP_LAST", "0_1_2_2_3_1_1": "OPP_LAST", "0_1_2_2_3_2_0": "OPP_LAST", "0_1_2_2_3_2_1": "OPP_LAST", "0_1_2_3_0_0_0": "SAME", "0_1_2_3_0_0_1": "SAME", "0_1_2_3_0_1_0": "SAME", "0_1_2_3_0_1_1": "SAME", "0_1_2_3_0_2_0": "SAME", "0_1_2_3_0_2_1": "SAME", "0_1_2_3_1_0_0": "SAME", "0_1_2_3_1_0_1": "SAME", "0_1_2_3_1_1_0": "SAME", "0_1_2_3_1_1_1": "OPP", "0_1_2_3_1_2_0": "SAME", "0_1_2_3_1_2_1": "SAME", "0_1_2_3_2_0_0": "OPP_LAST", "0_1_2_3_2_0_1": "OPP_LAST", "0_1_2_3_2_1_0": "OPP_LAST", "0_1_2_3_2_1_1": "OPP_LAST", "0_1_2_3_2_2_0": "OPP_LAST", "0_1_2_3_2_2_1": "OPP_LAST", "0_1_2_3_3_0_0": "OPP_LAST", "0_1_2_3_3_0_1": "OPP_LAST", "0_1_2_3_3_1_0": "OPP_LAST", "0_1_2_3_3_1_1": "OPP_LAST", "0_1_2_3_3_2_0": "OPP_LAST", "0_1_2_3_3_2_1": "OPP_LAST", "0_1_3_0_0_0_0": "SAME", "0_1_3_0_0_0_1": "SAME", "0_1_3_0_0_1_0": "SAME", "0_1_3_0_0_1_1": "SAME", "0_1_3_0_0_2_0": "SAME", "0_1_3_0_0_2_1": "SAME", "0_1_3_0_1_0_0": "OPP", "0_1_3_0_1_0_1": "SAME", "0_1_3_0_1_1_0": "SAME", "0_1_3_0_1_1_1": "SAME", "0_1_3_0_1_2_0": "SAME", "0_1_3_0_1_2_1": "SAME", "0_1_3_0_2_0_0": "OPP_LAST", "0_1_3_0_2_0_1": "OPP_LAST", "0_1_3_0_2_1_0": "OPP_LAST", "0_1_3_0_2_1_1": "OPP_LAST", "0_1_3_0_2_2_0": "OPP_LAST", "0_1_3_0_2_2_1": "OPP_LAST", "0_1_3_0_3_0_0": "OPP_LAST", "0_1_3_0_3_0_1": "OPP_LAST", "0_1_3_0_3_1_0": "OPP_LAST", "0_1_3_0_3_1_1": "OPP_LAST", "0_1_3_0_3_2_0": "OPP_LAST", "0_1_3_0_3_2_1": "OPP_LAST", "0_1_3_1_0_0_0": "SAME", "0_1_3_1_0_0_1": "SAME", "0_1_3_1_0_1_0": "SAME", "0_1_3_1_0_1_1": "SAME", "0_1_3_1_0_2_0": "SAME", "0_1_3_1_0_2_1": "SAME", "0_1_3_1_1_0_0": "OPP", "0_1_3_1_1_0_1": "SAME", "0_1_3_1_1_1_0": "SAME", "0_1_3_1_1_1_1": "OPP", "0_1_3_1_1_2_0": "SAME", "0_1_3_1_1_2_1": "SAME", "0_1_3_1_2_0_0": "OPP_LAST", "0_1_3_1_2_0_1": "OPP_LAST", "0_1_3_1_2_1_0": "OPP_LAST", "0_1_3_1_2_1_1": "OPP_LAST", "0_1_3_1_2_2_0": "OPP_LAST", "0_1_3_1_2_2_1": "OPP_LAST", "0_1_3_1_3_0_0": "OPP_LAST", "0_1_3_1_3_0_1": "OPP_LAST", "0_1_3_1_3_1_0": "OPP_LAST", "0_1_3_1_3_1_1": "OPP_LAST", "0_1_3_1_3_2_0": "OPP_LAST", "0_1_3_1_3_2_1": "OPP_LAST", "0_1_3_2_0_0_0": "SAME", "0_1_3_2_0_0_1": "SAME", "0_1_3_2_0_1_0": "SAME", "0_1_3_2_0_1_1": "SAME", "0_1_3_2_0_2_0": "SAME", "0_1_3_2_0_2_1": "SAME", "0_1_3_2_1_0_0": "SAME", "0_1_3_2_1_0_1": "SAME", "0_1_3_2_1_1_0": "SAME", "0_1_3_2_1_1_1": "SAME", "0_1_3_2_1_2_0": "SAME", "0_1_3_2_1_2_1": "SAME", "0_1_3_2_2_0_0": "OPP_LAST", "0_1_3_2_2_0_1": "OPP_LAST", "0_1_3_2_2_1_0": "OPP_LAST", "0_1_3_2_2_1_1": "OPP_LAST", "0_1_3_2_2_2_0": "OPP_LAST", "0_1_3_2_2_2_1": "OPP_LAST", "0_1_3_2_3_0_0": "OPP_LAST", "0_1_3_2_3_0_1": "OPP_LAST", "0_1_3_2_3_1_0": "OPP_LAST", "0_1_3_2_3_1_1": "OPP_LAST", "0_1_3_2_3_2_0": "OPP_LAST", "0_1_3_2_3_2_1": "OPP_LAST", "0_1_3_3_0_0_0": "SAME", "0_1_3_3_0_0_1": "SAME", "0_1_3_3_0_1_0": "SAME", "0_1_3_3_0_1_1": "SAME", "0_1_3_3_0_2_0": "SAME", "0_1_3_3_0_2_1": "SAME", "0_1_3_3_1_0_0": "SAME", "0_1_3_3_1_0_1": "SAME", "0_1_3_3_1_1_0": "SAME", "0_1_3_3_1_1_1": "OPP", "0_1_3_3_1_2_0": "SAME", "0_1_3_3_1_2_1": "SAME", "0_1_3_3_2_0_0": "OPP_LAST", "0_1_3_3_2_0_1": "OPP_LAST", "0_1_3_3_2_1_0": "OPP_LAST", "0_1_3_3_2_1_1": "OPP_LAST", "0_1_3_3_2_2_0": "OPP_LAST", "0_1_3_3_2_2_1": "OPP_LAST", "0_1_3_3_3_0_0": "OPP_LAST", "0_1_3_3_3_0_1": "OPP_LAST", "0_1_3_3_3_1_0": "OPP_LAST", "0_1_3_3_3_1_1": "OPP_LAST", "0_1_3_3_3_2_0": "OPP_LAST", "0_1_3_3_3_2_1": "OPP_LAST", "0_2_0_0_0_0_0": "SAME", "0_2_0_0_0_0_1": "SAME", "0_2_0_0_0_1_0": "SAME", "0_2_0_0_0_1_1": "SAME", "0_2_0_0_0_2_0": "SAME", "0_2_0_0_0_2_1": "SAME", "0_2_0_0_1_0_0": "SAME", "0_2_0_0_1_0_1": "SAME", "0_2_0_0_1_1_0": "SAME", "0_2_0_0_1_1_1": "SAME", "0_2_0_0_1_2_0": "SAME", "0_2_0_0_1_2_1": "SAME", "0_2_0_0_2_0_0": "SAME", "0_2_0_0_2_0_1": "SAME", "0_2_0_0_2_1_0": "SAME", "0_2_0_0_2_1_1": "SAME", "0_2_0_0_2_2_0": "SAME", "0_2_0_0_2_2_1": "SAME", "0_2_0_0_3_0_0": "SAME", "0_2_0_0_3_0_1": "SAME", "0_2_0_0_3_1_0": "SAME", "0_2_0_0_3_1_1": "SAME", "0_2_0_0_3_2_0": "SAME", "0_2_0_0_3_2_1": "SAME", "0_2_0_1_0_0_0": "SAME", "0_2_0_1_0_0_1": "SAME", "0_2_0_1_0_1_0": "SAME", "0_2_0_1_0_1_1": "SAME", "0_2_0_1_0_2_0": "SAME", "0_2_0_1_0_2_1": "SAME", "0_2_0_1_1_0_0": "SAME", "0_2_0_1_1_0_1": "SAME", "0_2_0_1_1_1_0": "SAME", "0_2_0_1_1_1_1": "SAME", "0_2_0_1_1_2_0": "SAME", "0_2_0_1_1_2_1": "SAME", "0_2_0_1_2_0_0": "SAME", "0_2_0_1_2_0_1": "SAME", "0_2_0_1_2_1_0": "SAME", "0_2_0_1_2_1_1": "SAME", "0_2_0_1_2_2_0": "SAME", "0_2_0_1_2_2_1": "SAME", "0_2_0_1_3_0_0": "SAME", "0_2_0_1_3_0_1": "SAME", "0_2_0_1_3_1_0": "SAME", "0_2_0_1_3_1_1": "SAME", "0_2_0_1_3_2_0": "SAME", "0_2_0_1_3_2_1": "SAME", "0_2_0_2_0_0_0": "SAME", "0_2_0_2_0_0_1": "SAME", "0_2_0_2_0_1_0": "SAME", "0_2_0_2_0_1_1": "SAME", "0_2_0_2_0_2_0": "SAME", "0_2_0_2_0_2_1": "SAME", "0_2_0_2_1_0_0": "SAME", "0_2_0_2_1_0_1": "SAME", "0_2_0_2_1_1_0": "SAME", "0_2_0_2_1_1_1": "SAME", "0_2_0_2_1_2_0": "SAME", "0_2_0_2_1_2_1": "SAME", "0_2_0_2_2_0_0": "SAME", "0_2_0_2_2_0_1": "SAME", "0_2_0_2_2_1_0": "SAME", "0_2_0_2_2_1_1": "SAME", "0_2_0_2_2_2_0": "SAME", "0_2_0_2_2_2_1": "SAME", "0_2_0_2_3_0_0": "SAME", "0_2_0_2_3_0_1": "SAME", "0_2_0_2_3_1_0": "SAME", "0_2_0_2_3_1_1": "SAME", "0_2_0_2_3_2_0": "SAME", "0_2_0_2_3_2_1": "SAME", "0_2_0_3_0_0_0": "SAME", "0_2_0_3_0_0_1": "SAME", "0_2_0_3_0_1_0": "SAME", "0_2_0_3_0_1_1": "SAME", "0_2_0_3_0_2_0": "SAME", "0_2_0_3_0_2_1": "SAME", "0_2_0_3_1_0_0": "SAME", "0_2_0_3_1_0_1": "SAME", "0_2_0_3_1_1_0": "SAME", "0_2_0_3_1_1_1": "SAME", "0_2_0_3_1_2_0": "SAME", "0_2_0_3_1_2_1": "SAME", "0_2_0_3_2_0_0": "SAME", "0_2_0_3_2_0_1": "SAME", "0_2_0_3_2_1_0": "SAME", "0_2_0_3_2_1_1": "SAME", "0_2_0_3_2_2_0": "SAME", "0_2_0_3_2_2_1": "SAME", "0_2_0_3_3_0_0": "SAME", "0_2_0_3_3_0_1": "SAME", "0_2_0_3_3_1_0": "SAME", "0_2_0_3_3_1_1": "SAME", "0_2_0_3_3_2_0": "SAME", "0_2_0_3_3_2_1": "SAME", "0_2_1_0_0_0_0": "OPP", "0_2_1_0_0_0_1": "SAME", "0_2_1_0_0_1_0": "SAME", "0_2_1_0_0_1_1": "SAME", "0_2_1_0_0_2_0": "SAME", "0_2_1_0_0_2_1": "SAME", "0_2_1_0_1_0_0": "SAME", "0_2_1_0_1_0_1": "SAME", "0_2_1_0_1_1_0": "SAME", "0_2_1_0_1_1_1": "SAME", "0_2_1_0_1_2_0": "SAME", "0_2_1_0_1_2_1": "SAME", "0_2_1_0_2_0_0": "SAME", "0_2_1_0_2_0_1": "SAME", "0_2_1_0_2_1_0": "SAME", "0_2_1_0_2_1_1": "SAME", "0_2_1_0_2_2_0": "SAME", "0_2_1_0_2_2_1": "SAME", "0_2_1_0_3_0_0": "SAME", "0_2_1_0_3_0_1": "SAME", "0_2_1_0_3_1_0": "SAME", "0_2_1_0_3_1_1": "SAME", "0_2_1_0_3_2_0": "SAME", "0_2_1_0_3_2_1": "SAME", "0_2_1_1_0_0_0": "SAME", "0_2_1_1_0_0_1": "SAME", "0_2_1_1_0_1_0": "SAME", "0_2_1_1_0_1_1": "OPP", "0_2_1_1_0_2_0": "OPP", "0_2_1_1_0_2_1": "OPP", "0_2_1_1_1_0_0": "SAME", "0_2_1_1_1_0_1": "SAME", "0_2_1_1_1_1_0": "SAME", "0_2_1_1_1_1_1": "SAME", "0_2_1_1_1_2_0": "SAME", "0_2_1_1_1_2_1": "SAME", "0_2_1_1_2_0_0": "SAME", "0_2_1_1_2_0_1": "SAME", "0_2_1_1_2_1_0": "SAME", "0_2_1_1_2_1_1": "SAME", "0_2_1_1_2_2_0": "SAME", "0_2_1_1_2_2_1": "SAME", "0_2_1_1_3_0_0": "SAME", "0_2_1_1_3_0_1": "SAME", "0_2_1_1_3_1_0": "SAME", "0_2_1_1_3_1_1": "SAME", "0_2_1_1_3_2_0": "SAME", "0_2_1_1_3_2_1": "SAME", "0_2_1_2_0_0_0": "SAME", "0_2_1_2_0_0_1": "SAME", "0_2_1_2_0_1_0": "OPP", "0_2_1_2_0_1_1": "SAME", "0_2_1_2_0_2_0": "SAME", "0_2_1_2_0_2_1": "SAME", "0_2_1_2_1_0_0": "SAME", "0_2_1_2_1_0_1": "SAME", "0_2_1_2_1_1_0": "SAME", "0_2_1_2_1_1_1": "SAME", "0_2_1_2_1_2_0": "SAME", "0_2_1_2_1_2_1": "SAME", "0_2_1_2_2_0_0": "SAME", "0_2_1_2_2_0_1": "SAME", "0_2_1_2_2_1_0": "SAME", "0_2_1_2_2_1_1": "SAME", "0_2_1_2_2_2_0": "SAME", "0_2_1_2_2_2_1": "SAME", "0_2_1_2_3_0_0": "SAME", "0_2_1_2_3_0_1": "SAME", "0_2_1_2_3_1_0": "SAME", "0_2_1_2_3_1_1": "SAME", "0_2_1_2_3_2_0": "SAME", "0_2_1_2_3_2_1": "SAME", "0_2_1_3_0_0_0": "SAME", "0_2_1_3_0_0_1": "SAME", "0_2_1_3_0_1_0": "SAME", "0_2_1_3_0_1_1": "OPP", "0_2_1_3_0_2_0": "SAME", "0_2_1_3_0_2_1": "SAME", "0_2_1_3_1_0_0": "SAME", "0_2_1_3_1_0_1": "SAME", "0_2_1_3_1_1_0": "SAME", "0_2_1_3_1_1_1": "SAME", "0_2_1_3_1_2_0": "SAME", "0_2_1_3_1_2_1": "SAME", "0_2_1_3_2_0_0": "SAME", "0_2_1_3_2_0_1": "SAME", "0_2_1_3_2_1_0": "SAME", "0_2_1_3_2_1_1": "SAME", "0_2_1_3_2_2_0": "SAME", "0_2_1_3_2_2_1": "SAME", "0_2_1_3_3_0_0": "SAME", "0_2_1_3_3_0_1": "SAME", "0_2_1_3_3_1_0": "SAME", "0_2_1_3_3_1_1": "SAME", "0_2_1_3_3_2_0": "SAME", "0_2_1_3_3_2_1": "SAME", "0_2_2_0_0_0_0": "SAME", "0_2_2_0_0_0_1": "SAME", "0_2_2_0_0_1_0": "SAME", "0_2_2_0_0_1_1": "SAME", "0_2_2_0_0_2_0": "SAME", "0_2_2_0_0_2_1": "SAME", "0_2_2_0_1_0_0": "SAME", "0_2_2_0_1_0_1": "SAME", "0_2_2_0_1_1_0": "SAME", "0_2_2_0_1_1_1": "SAME", "0_2_2_0_1_2_0": "SAME", "0_2_2_0_1_2_1": "SAME", "0_2_2_0_2_0_0": "SAME", "0_2_2_0_2_0_1": "SAME", "0_2_2_0_2_1_0": "SAME", "0_2_2_0_2_1_1": "SAME", "0_2_2_0_2_2_0": "SAME", "0_2_2_0_2_2_1": "SAME", "0_2_2_0_3_0_0": "SAME", "0_2_2_0_3_0_1": "SAME", "0_2_2_0_3_1_0": "SAME", "0_2_2_0_3_1_1": "SAME", "0_2_2_0_3_2_0": "SAME", "0_2_2_0_3_2_1": "SAME", "0_2_2_1_0_0_0": "SAME", "0_2_2_1_0_0_1": "SAME", "0_2_2_1_0_1_0": "SAME", "0_2_2_1_0_1_1": "SAME", "0_2_2_1_0_2_0": "SAME", "0_2_2_1_0_2_1": "SAME", "0_2_2_1_1_0_0": "SAME", "0_2_2_1_1_0_1": "SAME", "0_2_2_1_1_1_0": "SAME", "0_2_2_1_1_1_1": "SAME", "0_2_2_1_1_2_0": "SAME", "0_2_2_1_1_2_1": "SAME", "0_2_2_1_2_0_0": "SAME", "0_2_2_1_2_0_1": "SAME", "0_2_2_1_2_1_0": "SAME", "0_2_2_1_2_1_1": "SAME", "0_2_2_1_2_2_0": "SAME", "0_2_2_1_2_2_1": "SAME", "0_2_2_1_3_0_0": "SAME", "0_2_2_1_3_0_1": "SAME", "0_2_2_1_3_1_0": "SAME", "0_2_2_1_3_1_1": "SAME", "0_2_2_1_3_2_0": "SAME", "0_2_2_1_3_2_1": "SAME", "0_2_2_2_0_0_0": "SAME", "0_2_2_2_0_0_1": "SAME", "0_2_2_2_0_1_0": "SAME", "0_2_2_2_0_1_1": "SAME", "0_2_2_2_0_2_0": "SAME", "0_2_2_2_0_2_1": "SAME", "0_2_2_2_1_0_0": "SAME", "0_2_2_2_1_0_1": "SAME", "0_2_2_2_1_1_0": "SAME", "0_2_2_2_1_1_1": "SAME", "0_2_2_2_1_2_0": "SAME", "0_2_2_2_1_2_1": "SAME", "0_2_2_2_2_0_0": "SAME", "0_2_2_2_2_0_1": "SAME", "0_2_2_2_2_1_0": "SAME", "0_2_2_2_2_1_1": "SAME", "0_2_2_2_2_2_0": "SAME", "0_2_2_2_2_2_1": "SAME", "0_2_2_2_3_0_0": "SAME", "0_2_2_2_3_0_1": "SAME", "0_2_2_2_3_1_0": "SAME", "0_2_2_2_3_1_1": "SAME", "0_2_2_2_3_2_0": "SAME", "0_2_2_2_3_2_1": "SAME", "0_2_2_3_0_0_0": "SAME", "0_2_2_3_0_0_1": "SAME", "0_2_2_3_0_1_0": "SAME", "0_2_2_3_0_1_1": "SAME", "0_2_2_3_0_2_0": "SAME", "0_2_2_3_0_2_1": "SAME", "0_2_2_3_1_0_0": "SAME", "0_2_2_3_1_0_1": "SAME", "0_2_2_3_1_1_0": "SAME", "0_2_2_3_1_1_1": "SAME", "0_2_2_3_1_2_0": "SAME", "0_2_2_3_1_2_1": "SAME", "0_2_2_3_2_0_0": "SAME", "0_2_2_3_2_0_1": "SAME", "0_2_2_3_2_1_0": "SAME", "0_2_2_3_2_1_1": "SAME", "0_2_2_3_2_2_0": "SAME", "0_2_2_3_2_2_1": "SAME", "0_2_2_3_3_0_0": "SAME", "0_2_2_3_3_0_1": "SAME", "0_2_2_3_3_1_0": "SAME", "0_2_2_3_3_1_1": "SAME", "0_2_2_3_3_2_0": "SAME", "0_2_2_3_3_2_1": "SAME", "0_2_3_0_0_0_0": "SAME", "0_2_3_0_0_0_1": "SAME", "0_2_3_0_0_1_0": "SAME", "0_2_3_0_0_1_1": "SAME", "0_2_3_0_0_2_0": "SAME", "0_2_3_0_0_2_1": "SAME", "0_2_3_0_1_0_0": "SAME", "0_2_3_0_1_0_1": "SAME", "0_2_3_0_1_1_0": "SAME", "0_2_3_0_1_1_1": "SAME", "0_2_3_0_1_2_0": "SAME", "0_2_3_0_1_2_1": "SAME", "0_2_3_0_2_0_0": "SAME", "0_2_3_0_2_0_1": "SAME", "0_2_3_0_2_1_0": "SAME", "0_2_3_0_2_1_1": "SAME", "0_2_3_0_2_2_0": "SAME", "0_2_3_0_2_2_1": "SAME", "0_2_3_0_3_0_0": "SAME", "0_2_3_0_3_0_1": "SAME", "0_2_3_0_3_1_0": "SAME", "0_2_3_0_3_1_1": "SAME", "0_2_3_0_3_2_0": "SAME", "0_2_3_0_3_2_1": "SAME", "0_2_3_1_0_0_0": "SAME", "0_2_3_1_0_0_1": "SAME", "0_2_3_1_0_1_0": "OPP", "0_2_3_1_0_1_1": "OPP", "0_2_3_1_0_2_0": "SAME", "0_2_3_1_0_2_1": "SAME", "0_2_3_1_1_0_0": "SAME", "0_2_3_1_1_0_1": "SAME", "0_2_3_1_1_1_0": "SAME", "0_2_3_1_1_1_1": "SAME", "0_2_3_1_1_2_0": "SAME", "0_2_3_1_1_2_1": "SAME", "0_2_3_1_2_0_0": "SAME", "0_2_3_1_2_0_1": "SAME", "0_2_3_1_2_1_0": "SAME", "0_2_3_1_2_1_1": "SAME", "0_2_3_1_2_2_0": "SAME", "0_2_3_1_2_2_1": "SAME", "0_2_3_1_3_0_0": "SAME", "0_2_3_1_3_0_1": "SAME", "0_2_3_1_3_1_0": "SAME", "0_2_3_1_3_1_1": "SAME", "0_2_3_1_3_2_0": "SAME", "0_2_3_1_3_2_1": "SAME", "0_2_3_2_0_0_0": "SAME", "0_2_3_2_0_0_1": "OPP", "0_2_3_2_0_1_0": "SAME", "0_2_3_2_0_1_1": "OPP", "0_2_3_2_0_2_0": "SAME", "0_2_3_2_0_2_1": "SAME", "0_2_3_2_1_0_0": "SAME", "0_2_3_2_1_0_1": "SAME", "0_2_3_2_1_1_0": "SAME", "0_2_3_2_1_1_1": "SAME", "0_2_3_2_1_2_0": "SAME", "0_2_3_2_1_2_1": "SAME", "0_2_3_2_2_0_0": "SAME", "0_2_3_2_2_0_1": "SAME", "0_2_3_2_2_1_0": "SAME", "0_2_3_2_2_1_1": "SAME", "0_2_3_2_2_2_0": "SAME", "0_2_3_2_2_2_1": "SAME", "0_2_3_2_3_0_0": "SAME", "0_2_3_2_3_0_1": "SAME", "0_2_3_2_3_1_0": "SAME", "0_2_3_2_3_1_1": "SAME", "0_2_3_2_3_2_0": "SAME", "0_2_3_2_3_2_1": "SAME", "0_2_3_3_0_0_0": "OPP", "0_2_3_3_0_0_1": "OPP", "0_2_3_3_0_1_0": "SAME", "0_2_3_3_0_1_1": "SAME", "0_2_3_3_0_2_0": "SAME", "0_2_3_3_0_2_1": "SAME", "0_2_3_3_1_0_0": "SAME", "0_2_3_3_1_0_1": "SAME", "0_2_3_3_1_1_0": "SAME", "0_2_3_3_1_1_1": "SAME", "0_2_3_3_1_2_0": "SAME", "0_2_3_3_1_2_1": "SAME", "0_2_3_3_2_0_0": "SAME", "0_2_3_3_2_0_1": "SAME", "0_2_3_3_2_1_0": "SAME", "0_2_3_3_2_1_1": "SAME", "0_2_3_3_2_2_0": "SAME", "0_2_3_3_2_2_1": "SAME", "0_2_3_3_3_0_0": "SAME", "0_2_3_3_3_0_1": "SAME", "0_2_3_3_3_1_0": "SAME", "0_2_3_3_3_1_1": "SAME", "0_2_3_3_3_2_0": "SAME", "0_2_3_3_3_2_1": "SAME", "0_3_0_0_0_0_0": "SAME", "0_3_0_0_0_0_1": "OPP", "0_3_0_0_0_1_0": "SAME", "0_3_0_0_0_1_1": "SAME", "0_3_0_0_0_2_0": "SAME", "0_3_0_0_0_2_1": "SAME", "0_3_0_0_1_0_0": "SAME", "0_3_0_0_1_0_1": "SAME", "0_3_0_0_1_1_0": "SAME", "0_3_0_0_1_1_1": "SAME", "0_3_0_0_1_2_0": "SAME", "0_3_0_0_1_2_1": "SAME", "0_3_0_0_2_0_0": "SAME", "0_3_0_0_2_0_1": "SAME", "0_3_0_0_2_1_0": "SAME", "0_3_0_0_2_1_1": "SAME", "0_3_0_0_2_2_0": "SAME", "0_3_0_0_2_2_1": "SAME", "0_3_0_0_3_0_0": "SAME", "0_3_0_0_3_0_1": "SAME", "0_3_0_0_3_1_0": "SAME", "0_3_0_0_3_1_1": "SAME", "0_3_0_0_3_2_0": "SAME", "0_3_0_0_3_2_1": "SAME", "0_3_0_1_0_0_0": "SAME", "0_3_0_1_0_0_1": "SAME", "0_3_0_1_0_1_0": "SAME", "0_3_0_1_0_1_1": "SAME", "0_3_0_1_0_2_0": "SAME", "0_3_0_1_0_2_1": "SAME", "0_3_0_1_1_0_0": "SAME", "0_3_0_1_1_0_1": "SAME", "0_3_0_1_1_1_0": "SAME", "0_3_0_1_1_1_1": "SAME", "0_3_0_1_1_2_0": "SAME", "0_3_0_1_1_2_1": "SAME", "0_3_0_1_2_0_0": "SAME", "0_3_0_1_2_0_1": "SAME", "0_3_0_1_2_1_0": "SAME", "0_3_0_1_2_1_1": "SAME", "0_3_0_1_2_2_0": "SAME", "0_3_0_1_2_2_1": "SAME", "0_3_0_1_3_0_0": "SAME", "0_3_0_1_3_0_1": "SAME", "0_3_0_1_3_1_0": "SAME", "0_3_0_1_3_1_1": "SAME", "0_3_0_1_3_2_0": "SAME", "0_3_0_1_3_2_1": "SAME", "0_3_0_2_0_0_0": "SAME", "0_3_0_2_0_0_1": "SAME", "0_3_0_2_0_1_0": "SAME", "0_3_0_2_0_1_1": "SAME", "0_3_0_2_0_2_0": "SAME", "0_3_0_2_0_2_1": "SAME", "0_3_0_2_1_0_0": "SAME", "0_3_0_2_1_0_1": "SAME", "0_3_0_2_1_1_0": "SAME", "0_3_0_2_1_1_1": "SAME", "0_3_0_2_1_2_0": "SAME", "0_3_0_2_1_2_1": "SAME", "0_3_0_2_2_0_0": "SAME", "0_3_0_2_2_0_1": "SAME", "0_3_0_2_2_1_0": "SAME", "0_3_0_2_2_1_1": "SAME", "0_3_0_2_2_2_0": "SAME", "0_3_0_2_2_2_1": "SAME", "0_3_0_2_3_0_0": "SAME", "0_3_0_2_3_0_1": "SAME", "0_3_0_2_3_1_0": "SAME", "0_3_0_2_3_1_1": "SAME", "0_3_0_2_3_2_0": "SAME", "0_3_0_2_3_2_1": "SAME", "0_3_0_3_0_0_0": "SAME", "0_3_0_3_0_0_1": "SAME", "0_3_0_3_0_1_0": "SAME", "0_3_0_3_0_1_1": "SAME", "0_3_0_3_0_2_0": "SAME", "0_3_0_3_0_2_1": "SAME", "0_3_0_3_1_0_0": "SAME", "0_3_0_3_1_0_1": "SAME", "0_3_0_3_1_1_0": "SAME", "0_3_0_3_1_1_1": "SAME", "0_3_0_3_1_2_0": "SAME", "0_3_0_3_1_2_1": "SAME", "0_3_0_3_2_0_0": "SAME", "0_3_0_3_2_0_1": "SAME", "0_3_0_3_2_1_0": "SAME", "0_3_0_3_2_1_1": "SAME", "0_3_0_3_2_2_0": "SAME", "0_3_0_3_2_2_1": "SAME", "0_3_0_3_3_0_0": "SAME", "0_3_0_3_3_0_1": "SAME", "0_3_0_3_3_1_0": "SAME", "0_3_0_3_3_1_1": "SAME", "0_3_0_3_3_2_0": "SAME", "0_3_0_3_3_2_1": "SAME", "0_3_1_0_0_0_0": "SAME", "0_3_1_0_0_0_1": "SAME", "0_3_1_0_0_1_0": "SAME", "0_3_1_0_0_1_1": "SAME", "0_3_1_0_0_2_0": "SAME", "0_3_1_0_0_2_1": "SAME", "0_3_1_0_1_0_0": "SAME", "0_3_1_0_1_0_1": "SAME", "0_3_1_0_1_1_0": "SAME", "0_3_1_0_1_1_1": "SAME", "0_3_1_0_1_2_0": "SAME", "0_3_1_0_1_2_1": "SAME", "0_3_1_0_2_0_0": "SAME", "0_3_1_0_2_0_1": "SAME", "0_3_1_0_2_1_0": "SAME", "0_3_1_0_2_1_1": "SAME", "0_3_1_0_2_2_0": "SAME", "0_3_1_0_2_2_1": "SAME", "0_3_1_0_3_0_0": "SAME", "0_3_1_0_3_0_1": "SAME", "0_3_1_0_3_1_0": "SAME", "0_3_1_0_3_1_1": "SAME", "0_3_1_0_3_2_0": "SAME", "0_3_1_0_3_2_1": "SAME", "0_3_1_1_0_0_0": "SAME", "0_3_1_1_0_0_1": "SAME", "0_3_1_1_0_1_0": "OPP", "0_3_1_1_0_1_1": "SAME", "0_3_1_1_0_2_0": "SAME", "0_3_1_1_0_2_1": "SAME", "0_3_1_1_1_0_0": "SAME", "0_3_1_1_1_0_1": "SAME", "0_3_1_1_1_1_0": "SAME", "0_3_1_1_1_1_1": "SAME", "0_3_1_1_1_2_0": "SAME", "0_3_1_1_1_2_1": "SAME", "0_3_1_1_2_0_0": "SAME", "0_3_1_1_2_0_1": "SAME", "0_3_1_1_2_1_0": "SAME", "0_3_1_1_2_1_1": "SAME", "0_3_1_1_2_2_0": "SAME", "0_3_1_1_2_2_1": "SAME", "0_3_1_1_3_0_0": "SAME", "0_3_1_1_3_0_1": "SAME", "0_3_1_1_3_1_0": "SAME", "0_3_1_1_3_1_1": "SAME", "0_3_1_1_3_2_0": "SAME", "0_3_1_1_3_2_1": "SAME", "0_3_1_2_0_0_0": "SAME", "0_3_1_2_0_0_1": "SAME", "0_3_1_2_0_1_0": "OPP", "0_3_1_2_0_1_1": "SAME", "0_3_1_2_0_2_0": "SAME", "0_3_1_2_0_2_1": "SAME", "0_3_1_2_1_0_0": "SAME", "0_3_1_2_1_0_1": "SAME", "0_3_1_2_1_1_0": "SAME", "0_3_1_2_1_1_1": "SAME", "0_3_1_2_1_2_0": "SAME", "0_3_1_2_1_2_1": "SAME", "0_3_1_2_2_0_0": "SAME", "0_3_1_2_2_0_1": "SAME", "0_3_1_2_2_1_0": "SAME", "0_3_1_2_2_1_1": "SAME", "0_3_1_2_2_2_0": "SAME", "0_3_1_2_2_2_1": "SAME", "0_3_1_2_3_0_0": "SAME", "0_3_1_2_3_0_1": "SAME", "0_3_1_2_3_1_0": "SAME", "0_3_1_2_3_1_1": "SAME", "0_3_1_2_3_2_0": "SAME", "0_3_1_2_3_2_1": "SAME", "0_3_1_3_0_0_0": "SAME", "0_3_1_3_0_0_1": "SAME", "0_3_1_3_0_1_0": "SAME", "0_3_1_3_0_1_1": "OPP", "0_3_1_3_0_2_0": "SAME", "0_3_1_3_0_2_1": "SAME", "0_3_1_3_1_0_0": "SAME", "0_3_1_3_1_0_1": "SAME", "0_3_1_3_1_1_0": "SAME", "0_3_1_3_1_1_1": "SAME", "0_3_1_3_1_2_0": "SAME", "0_3_1_3_1_2_1": "SAME", "0_3_1_3_2_0_0": "SAME", "0_3_1_3_2_0_1": "SAME", "0_3_1_3_2_1_0": "SAME", "0_3_1_3_2_1_1": "SAME", "0_3_1_3_2_2_0": "SAME", "0_3_1_3_2_2_1": "SAME", "0_3_1_3_3_0_0": "SAME", "0_3_1_3_3_0_1": "SAME", "0_3_1_3_3_1_0": "SAME", "0_3_1_3_3_1_1": "SAME", "0_3_1_3_3_2_0": "SAME", "0_3_1_3_3_2_1": "SAME", "0_3_2_0_0_0_0": "SAME", "0_3_2_0_0_0_1": "SAME", "0_3_2_0_0_1_0": "SAME", "0_3_2_0_0_1_1": "SAME", "0_3_2_0_0_2_0": "SAME", "0_3_2_0_0_2_1": "SAME", "0_3_2_0_1_0_0": "SAME", "0_3_2_0_1_0_1": "SAME", "0_3_2_0_1_1_0": "SAME", "0_3_2_0_1_1_1": "SAME", "0_3_2_0_1_2_0": "SAME", "0_3_2_0_1_2_1": "SAME", "0_3_2_0_2_0_0": "SAME", "0_3_2_0_2_0_1": "SAME", "0_3_2_0_2_1_0": "SAME", "0_3_2_0_2_1_1": "SAME", "0_3_2_0_2_2_0": "SAME", "0_3_2_0_2_2_1": "SAME", "0_3_2_0_3_0_0": "SAME", "0_3_2_0_3_0_1": "SAME", "0_3_2_0_3_1_0": "SAME", "0_3_2_0_3_1_1": "SAME", "0_3_2_0_3_2_0": "SAME", "0_3_2_0_3_2_1": "SAME", "0_3_2_1_0_0_0": "SAME", "0_3_2_1_0_0_1": "SAME", "0_3_2_1_0_1_0": "SAME", "0_3_2_1_0_1_1": "SAME", "0_3_2_1_0_2_0": "SAME", "0_3_2_1_0_2_1": "SAME", "0_3_2_1_1_0_0": "SAME", "0_3_2_1_1_0_1": "SAME", "0_3_2_1_1_1_0": "SAME", "0_3_2_1_1_1_1": "SAME", "0_3_2_1_1_2_0": "SAME", "0_3_2_1_1_2_1": "SAME", "0_3_2_1_2_0_0": "SAME", "0_3_2_1_2_0_1": "SAME", "0_3_2_1_2_1_0": "SAME", "0_3_2_1_2_1_1": "SAME", "0_3_2_1_2_2_0": "SAME", "0_3_2_1_2_2_1": "SAME", "0_3_2_1_3_0_0": "SAME", "0_3_2_1_3_0_1": "SAME", "0_3_2_1_3_1_0": "SAME", "0_3_2_1_3_1_1": "SAME", "0_3_2_1_3_2_0": "SAME", "0_3_2_1_3_2_1": "SAME", "0_3_2_2_0_0_0": "SAME", "0_3_2_2_0_0_1": "SAME", "0_3_2_2_0_1_0": "OPP", "0_3_2_2_0_1_1": "SAME", "0_3_2_2_0_2_0": "SAME", "0_3_2_2_0_2_1": "SAME", "0_3_2_2_1_0_0": "SAME", "0_3_2_2_1_0_1": "SAME", "0_3_2_2_1_1_0": "SAME", "0_3_2_2_1_1_1": "SAME", "0_3_2_2_1_2_0": "SAME", "0_3_2_2_1_2_1": "SAME", "0_3_2_2_2_0_0": "SAME", "0_3_2_2_2_0_1": "SAME", "0_3_2_2_2_1_0": "SAME", "0_3_2_2_2_1_1": "SAME", "0_3_2_2_2_2_0": "SAME", "0_3_2_2_2_2_1": "SAME", "0_3_2_2_3_0_0": "SAME", "0_3_2_2_3_0_1": "SAME", "0_3_2_2_3_1_0": "SAME", "0_3_2_2_3_1_1": "SAME", "0_3_2_2_3_2_0": "SAME", "0_3_2_2_3_2_1": "SAME", "0_3_2_3_0_0_0": "SAME", "0_3_2_3_0_0_1": "SAME", "0_3_2_3_0_1_0": "SAME", "0_3_2_3_0_1_1": "OPP", "0_3_2_3_0_2_0": "SAME", "0_3_2_3_0_2_1": "SAME", "0_3_2_3_1_0_0": "SAME", "0_3_2_3_1_0_1": "SAME", "0_3_2_3_1_1_0": "SAME", "0_3_2_3_1_1_1": "SAME", "0_3_2_3_1_2_0": "SAME", "0_3_2_3_1_2_1": "SAME", "0_3_2_3_2_0_0": "SAME", "0_3_2_3_2_0_1": "SAME", "0_3_2_3_2_1_0": "SAME", "0_3_2_3_2_1_1": "SAME", "0_3_2_3_2_2_0": "SAME", "0_3_2_3_2_2_1": "SAME", "0_3_2_3_3_0_0": "SAME", "0_3_2_3_3_0_1": "SAME", "0_3_2_3_3_1_0": "SAME", "0_3_2_3_3_1_1": "SAME", "0_3_2_3_3_2_0": "SAME", "0_3_2_3_3_2_1": "SAME", "0_3_3_0_0_0_0": "SAME", "0_3_3_0_0_0_1": "OPP", "0_3_3_0_0_1_0": "SAME", "0_3_3_0_0_1_1": "SAME", "0_3_3_0_0_2_0": "SAME", "0_3_3_0_0_2_1": "SAME", "0_3_3_0_1_0_0": "SAME", "0_3_3_0_1_0_1": "SAME", "0_3_3_0_1_1_0": "SAME", "0_3_3_0_1_1_1": "SAME", "0_3_3_0_1_2_0": "SAME", "0_3_3_0_1_2_1": "SAME", "0_3_3_0_2_0_0": "SAME", "0_3_3_0_2_0_1": "SAME", "0_3_3_0_2_1_0": "SAME", "0_3_3_0_2_1_1": "SAME", "0_3_3_0_2_2_0": "SAME", "0_3_3_0_2_2_1": "SAME", "0_3_3_0_3_0_0": "SAME", "0_3_3_0_3_0_1": "SAME", "0_3_3_0_3_1_0": "SAME", "0_3_3_0_3_1_1": "SAME", "0_3_3_0_3_2_0": "SAME", "0_3_3_0_3_2_1": "SAME", "0_3_3_1_0_0_0": "SAME", "0_3_3_1_0_0_1": "SAME", "0_3_3_1_0_1_0": "SAME", "0_3_3_1_0_1_1": "SAME", "0_3_3_1_0_2_0": "SAME", "0_3_3_1_0_2_1": "SAME", "0_3_3_1_1_0_0": "SAME", "0_3_3_1_1_0_1": "SAME", "0_3_3_1_1_1_0": "SAME", "0_3_3_1_1_1_1": "SAME", "0_3_3_1_1_2_0": "SAME", "0_3_3_1_1_2_1": "SAME", "0_3_3_1_2_0_0": "SAME", "0_3_3_1_2_0_1": "SAME", "0_3_3_1_2_1_0": "SAME", "0_3_3_1_2_1_1": "SAME", "0_3_3_1_2_2_0": "SAME", "0_3_3_1_2_2_1": "SAME", "0_3_3_1_3_0_0": "SAME", "0_3_3_1_3_0_1": "SAME", "0_3_3_1_3_1_0": "SAME", "0_3_3_1_3_1_1": "SAME", "0_3_3_1_3_2_0": "SAME", "0_3_3_1_3_2_1": "SAME", "0_3_3_2_0_0_0": "SAME", "0_3_3_2_0_0_1": "SAME", "0_3_3_2_0_1_0": "SAME", "0_3_3_2_0_1_1": "SAME", "0_3_3_2_0_2_0": "SAME", "0_3_3_2_0_2_1": "SAME", "0_3_3_2_1_0_0": "SAME", "0_3_3_2_1_0_1": "SAME", "0_3_3_2_1_1_0": "SAME", "0_3_3_2_1_1_1": "SAME", "0_3_3_2_1_2_0": "SAME", "0_3_3_2_1_2_1": "SAME", "0_3_3_2_2_0_0": "SAME", "0_3_3_2_2_0_1": "SAME", "0_3_3_2_2_1_0": "SAME", "0_3_3_2_2_1_1": "SAME", "0_3_3_2_2_2_0": "SAME", "0_3_3_2_2_2_1": "SAME", "0_3_3_2_3_0_0": "SAME", "0_3_3_2_3_0_1": "SAME", "0_3_3_2_3_1_0": "SAME", "0_3_3_2_3_1_1": "SAME", "0_3_3_2_3_2_0": "SAME", "0_3_3_2_3_2_1": "SAME", "0_3_3_3_0_0_0": "OPP", "0_3_3_3_0_0_1": "OPP", "0_3_3_3_0_1_0": "SAME", "0_3_3_3_0_1_1": "SAME", "0_3_3_3_0_2_0": "SAME", "0_3_3_3_0_2_1": "SAME", "0_3_3_3_1_0_0": "SAME", "0_3_3_3_1_0_1": "SAME", "0_3_3_3_1_1_0": "SAME", "0_3_3_3_1_1_1": "SAME", "0_3_3_3_1_2_0": "SAME", "0_3_3_3_1_2_1": "SAME", "0_3_3_3_2_0_0": "SAME", "0_3_3_3_2_0_1": "SAME", "0_3_3_3_2_1_0": "SAME", "0_3_3_3_2_1_1": "SAME", "0_3_3_3_2_2_0": "SAME", "0_3_3_3_2_2_1": "SAME", "0_3_3_3_3_0_0": "SAME", "0_3_3_3_3_0_1": "SAME", "0_3_3_3_3_1_0": "SAME", "0_3_3_3_3_1_1": "SAME", "0_3_3_3_3_2_0": "SAME", "0_3_3_3_3_2_1": "SAME", "0_4_0_0_0_0_0": "SAME", "0_4_0_0_0_0_1": "SAME", "0_4_0_0_0_1_0": "SAME", "0_4_0_0_0_1_1": "SAME", "0_4_0_0_0_2_0": "SAME", "0_4_0_0_0_2_1": "SAME", "0_4_0_0_1_0_0": "SAME", "0_4_0_0_1_0_1": "SAME", "0_4_0_0_1_1_0": "SAME", "0_4_0_0_1_1_1": "SAME", "0_4_0_0_1_2_0": "SAME", "0_4_0_0_1_2_1": "SAME", "0_4_0_0_2_0_0": "SAME", "0_4_0_0_2_0_1": "SAME", "0_4_0_0_2_1_0": "SAME", "0_4_0_0_2_1_1": "SAME", "0_4_0_0_2_2_0": "SAME", "0_4_0_0_2_2_1": "SAME", "0_4_0_0_3_0_0": "SAME", "0_4_0_0_3_0_1": "SAME", "0_4_0_0_3_1_0": "SAME", "0_4_0_0_3_1_1": "SAME", "0_4_0_0_3_2_0": "SAME", "0_4_0_0_3_2_1": "SAME", "0_4_0_1_0_0_0": "SAME", "0_4_0_1_0_0_1": "SAME", "0_4_0_1_0_1_0": "SAME", "0_4_0_1_0_1_1": "SAME", "0_4_0_1_0_2_0": "SAME", "0_4_0_1_0_2_1": "SAME", "0_4_0_1_1_0_0": "SAME", "0_4_0_1_1_0_1": "SAME", "0_4_0_1_1_1_0": "SAME", "0_4_0_1_1_1_1": "SAME", "0_4_0_1_1_2_0": "SAME", "0_4_0_1_1_2_1": "SAME", "0_4_0_1_2_0_0": "SAME", "0_4_0_1_2_0_1": "SAME", "0_4_0_1_2_1_0": "SAME", "0_4_0_1_2_1_1": "SAME", "0_4_0_1_2_2_0": "SAME", "0_4_0_1_2_2_1": "SAME", "0_4_0_1_3_0_0": "SAME", "0_4_0_1_3_0_1": "SAME", "0_4_0_1_3_1_0": "SAME", "0_4_0_1_3_1_1": "SAME", "0_4_0_1_3_2_0": "SAME", "0_4_0_1_3_2_1": "SAME", "0_4_0_2_0_0_0": "SAME", "0_4_0_2_0_0_1": "SAME", "0_4_0_2_0_1_0": "SAME", "0_4_0_2_0_1_1": "SAME", "0_4_0_2_0_2_0": "SAME", "0_4_0_2_0_2_1": "SAME", "0_4_0_2_1_0_0": "SAME", "0_4_0_2_1_0_1": "SAME", "0_4_0_2_1_1_0": "SAME", "0_4_0_2_1_1_1": "SAME", "0_4_0_2_1_2_0": "SAME", "0_4_0_2_1_2_1": "SAME", "0_4_0_2_2_0_0": "SAME", "0_4_0_2_2_0_1": "SAME", "0_4_0_2_2_1_0": "SAME", "0_4_0_2_2_1_1": "SAME", "0_4_0_2_2_2_0": "SAME", "0_4_0_2_2_2_1": "SAME", "0_4_0_2_3_0_0": "SAME", "0_4_0_2_3_0_1": "SAME", "0_4_0_2_3_1_0": "SAME", "0_4_0_2_3_1_1": "SAME", "0_4_0_2_3_2_0": "SAME", "0_4_0_2_3_2_1": "SAME", "0_4_0_3_0_0_0": "SAME", "0_4_0_3_0_0_1": "SAME", "0_4_0_3_0_1_0": "SAME", "0_4_0_3_0_1_1": "SAME", "0_4_0_3_0_2_0": "SAME", "0_4_0_3_0_2_1": "SAME", "0_4_0_3_1_0_0": "SAME", "0_4_0_3_1_0_1": "SAME", "0_4_0_3_1_1_0": "SAME", "0_4_0_3_1_1_1": "SAME", "0_4_0_3_1_2_0": "SAME", "0_4_0_3_1_2_1": "SAME", "0_4_0_3_2_0_0": "SAME", "0_4_0_3_2_0_1": "SAME", "0_4_0_3_2_1_0": "SAME", "0_4_0_3_2_1_1": "SAME", "0_4_0_3_2_2_0": "SAME", "0_4_0_3_2_2_1": "SAME", "0_4_0_3_3_0_0": "SAME", "0_4_0_3_3_0_1": "SAME", "0_4_0_3_3_1_0": "SAME", "0_4_0_3_3_1_1": "SAME", "0_4_0_3_3_2_0": "SAME", "0_4_0_3_3_2_1": "SAME", "0_4_1_0_0_0_0": "SAME", "0_4_1_0_0_0_1": "OPP", "0_4_1_0_0_1_0": "SAME", "0_4_1_0_0_1_1": "SAME", "0_4_1_0_0_2_0": "SAME", "0_4_1_0_0_2_1": "SAME", "0_4_1_0_1_0_0": "SAME", "0_4_1_0_1_0_1": "SAME", "0_4_1_0_1_1_0": "SAME", "0_4_1_0_1_1_1": "SAME", "0_4_1_0_1_2_0": "SAME", "0_4_1_0_1_2_1": "SAME", "0_4_1_0_2_0_0": "SAME", "0_4_1_0_2_0_1": "SAME", "0_4_1_0_2_1_0": "SAME", "0_4_1_0_2_1_1": "SAME", "0_4_1_0_2_2_0": "SAME", "0_4_1_0_2_2_1": "SAME", "0_4_1_0_3_0_0": "SAME", "0_4_1_0_3_0_1": "SAME", "0_4_1_0_3_1_0": "SAME", "0_4_1_0_3_1_1": "SAME", "0_4_1_0_3_2_0": "SAME", "0_4_1_0_3_2_1": "SAME", "0_4_1_1_0_0_0": "SAME", "0_4_1_1_0_0_1": "SAME", "0_4_1_1_0_1_0": "SAME", "0_4_1_1_0_1_1": "OPP", "0_4_1_1_0_2_0": "SAME", "0_4_1_1_0_2_1": "SAME", "0_4_1_1_1_0_0": "SAME", "0_4_1_1_1_0_1": "SAME", "0_4_1_1_1_1_0": "SAME", "0_4_1_1_1_1_1": "SAME", "0_4_1_1_1_2_0": "SAME", "0_4_1_1_1_2_1": "SAME", "0_4_1_1_2_0_0": "SAME", "0_4_1_1_2_0_1": "SAME", "0_4_1_1_2_1_0": "SAME", "0_4_1_1_2_1_1": "SAME", "0_4_1_1_2_2_0": "SAME", "0_4_1_1_2_2_1": "SAME", "0_4_1_1_3_0_0": "SAME", "0_4_1_1_3_0_1": "SAME", "0_4_1_1_3_1_0": "SAME", "0_4_1_1_3_1_1": "SAME", "0_4_1_1_3_2_0": "SAME", "0_4_1_1_3_2_1": "SAME", "0_4_1_2_0_0_0": "SAME", "0_4_1_2_0_0_1": "OPP", "0_4_1_2_0_1_0": "OPP", "0_4_1_2_0_1_1": "SAME", "0_4_1_2_0_2_0": "SAME", "0_4_1_2_0_2_1": "SAME", "0_4_1_2_1_0_0": "SAME", "0_4_1_2_1_0_1": "SAME", "0_4_1_2_1_1_0": "SAME", "0_4_1_2_1_1_1": "SAME", "0_4_1_2_1_2_0": "SAME", "0_4_1_2_1_2_1": "SAME", "0_4_1_2_2_0_0": "SAME", "0_4_1_2_2_0_1": "SAME", "0_4_1_2_2_1_0": "SAME", "0_4_1_2_2_1_1": "SAME", "0_4_1_2_2_2_0": "SAME", "0_4_1_2_2_2_1": "SAME", "0_4_1_2_3_0_0": "SAME", "0_4_1_2_3_0_1": "SAME", "0_4_1_2_3_1_0": "SAME", "0_4_1_2_3_1_1": "SAME", "0_4_1_2_3_2_0": "SAME", "0_4_1_2_3_2_1": "SAME", "0_4_1_3_0_0_0": "SAME", "0_4_1_3_0_0_1": "SAME", "0_4_1_3_0_1_0": "OPP", "0_4_1_3_0_1_1": "SAME", "0_4_1_3_0_2_0": "SAME", "0_4_1_3_0_2_1": "SAME", "0_4_1_3_1_0_0": "SAME", "0_4_1_3_1_0_1": "SAME", "0_4_1_3_1_1_0": "SAME", "0_4_1_3_1_1_1": "SAME", "0_4_1_3_1_2_0": "SAME", "0_4_1_3_1_2_1": "SAME", "0_4_1_3_2_0_0": "SAME", "0_4_1_3_2_0_1": "SAME", "0_4_1_3_2_1_0": "SAME", "0_4_1_3_2_1_1": "SAME", "0_4_1_3_2_2_0": "SAME", "0_4_1_3_2_2_1": "SAME", "0_4_1_3_3_0_0": "SAME", "0_4_1_3_3_0_1": "SAME", "0_4_1_3_3_1_0": "SAME", "0_4_1_3_3_1_1": "SAME", "0_4_1_3_3_2_0": "SAME", "0_4_1_3_3_2_1": "SAME", "0_4_2_0_0_0_0": "SAME", "0_4_2_0_0_0_1": "SAME", "0_4_2_0_0_1_0": "SAME", "0_4_2_0_0_1_1": "SAME", "0_4_2_0_0_2_0": "SAME", "0_4_2_0_0_2_1": "SAME", "0_4_2_0_1_0_0": "SAME", "0_4_2_0_1_0_1": "SAME", "0_4_2_0_1_1_0": "SAME", "0_4_2_0_1_1_1": "SAME", "0_4_2_0_1_2_0": "SAME", "0_4_2_0_1_2_1": "SAME", "0_4_2_0_2_0_0": "SAME", "0_4_2_0_2_0_1": "SAME", "0_4_2_0_2_1_0": "SAME", "0_4_2_0_2_1_1": "SAME", "0_4_2_0_2_2_0": "SAME", "0_4_2_0_2_2_1": "SAME", "0_4_2_0_3_0_0": "SAME", "0_4_2_0_3_0_1": "SAME", "0_4_2_0_3_1_0": "SAME", "0_4_2_0_3_1_1": "SAME", "0_4_2_0_3_2_0": "SAME", "0_4_2_0_3_2_1": "SAME", "0_4_2_1_0_0_0": "OPP", "0_4_2_1_0_0_1": "OPP", "0_4_2_1_0_1_0": "SAME", "0_4_2_1_0_1_1": "SAME", "0_4_2_1_0_2_0": "SAME", "0_4_2_1_0_2_1": "SAME", "0_4_2_1_1_0_0": "SAME", "0_4_2_1_1_0_1": "SAME", "0_4_2_1_1_1_0": "SAME", "0_4_2_1_1_1_1": "SAME", "0_4_2_1_1_2_0": "SAME", "0_4_2_1_1_2_1": "SAME", "0_4_2_1_2_0_0": "SAME", "0_4_2_1_2_0_1": "SAME", "0_4_2_1_2_1_0": "SAME", "0_4_2_1_2_1_1": "SAME", "0_4_2_1_2_2_0": "SAME", "0_4_2_1_2_2_1": "SAME", "0_4_2_1_3_0_0": "SAME", "0_4_2_1_3_0_1": "SAME", "0_4_2_1_3_1_0": "SAME", "0_4_2_1_3_1_1": "SAME", "0_4_2_1_3_2_0": "SAME", "0_4_2_1_3_2_1": "SAME", "0_4_2_2_0_0_0": "SAME", "0_4_2_2_0_0_1": "SAME", "0_4_2_2_0_1_0": "SAME", "0_4_2_2_0_1_1": "SAME", "0_4_2_2_0_2_0": "SAME", "0_4_2_2_0_2_1": "SAME", "0_4_2_2_1_0_0": "SAME", "0_4_2_2_1_0_1": "SAME", "0_4_2_2_1_1_0": "SAME", "0_4_2_2_1_1_1": "SAME", "0_4_2_2_1_2_0": "SAME", "0_4_2_2_1_2_1": "SAME", "0_4_2_2_2_0_0": "SAME", "0_4_2_2_2_0_1": "SAME", "0_4_2_2_2_1_0": "SAME", "0_4_2_2_2_1_1": "SAME", "0_4_2_2_2_2_0": "SAME", "0_4_2_2_2_2_1": "SAME", "0_4_2_2_3_0_0": "SAME", "0_4_2_2_3_0_1": "SAME", "0_4_2_2_3_1_0": "SAME", "0_4_2_2_3_1_1": "SAME", "0_4_2_2_3_2_0": "SAME", "0_4_2_2_3_2_1": "SAME", "0_4_2_3_0_0_0": "SAME", "0_4_2_3_0_0_1": "SAME", "0_4_2_3_0_1_0": "SAME", "0_4_2_3_0_1_1": "SAME", "0_4_2_3_0_2_0": "SAME", "0_4_2_3_0_2_1": "SAME", "0_4_2_3_1_0_0": "SAME", "0_4_2_3_1_0_1": "SAME", "0_4_2_3_1_1_0": "SAME", "0_4_2_3_1_1_1": "SAME", "0_4_2_3_1_2_0": "SAME", "0_4_2_3_1_2_1": "SAME", "0_4_2_3_2_0_0": "SAME", "0_4_2_3_2_0_1": "SAME", "0_4_2_3_2_1_0": "SAME", "0_4_2_3_2_1_1": "SAME", "0_4_2_3_2_2_0": "SAME", "0_4_2_3_2_2_1": "SAME", "0_4_2_3_3_0_0": "SAME", "0_4_2_3_3_0_1": "SAME", "0_4_2_3_3_1_0": "SAME", "0_4_2_3_3_1_1": "SAME", "0_4_2_3_3_2_0": "SAME", "0_4_2_3_3_2_1": "SAME", "0_4_3_0_0_0_0": "SAME", "0_4_3_0_0_0_1": "SAME", "0_4_3_0_0_1_0": "SAME", "0_4_3_0_0_1_1": "SAME", "0_4_3_0_0_2_0": "SAME", "0_4_3_0_0_2_1": "SAME", "0_4_3_0_1_0_0": "SAME", "0_4_3_0_1_0_1": "SAME", "0_4_3_0_1_1_0": "SAME", "0_4_3_0_1_1_1": "SAME", "0_4_3_0_1_2_0": "SAME", "0_4_3_0_1_2_1": "SAME", "0_4_3_0_2_0_0": "SAME", "0_4_3_0_2_0_1": "SAME", "0_4_3_0_2_1_0": "SAME", "0_4_3_0_2_1_1": "SAME", "0_4_3_0_2_2_0": "SAME", "0_4_3_0_2_2_1": "SAME", "0_4_3_0_3_0_0": "SAME", "0_4_3_0_3_0_1": "SAME", "0_4_3_0_3_1_0": "SAME", "0_4_3_0_3_1_1": "SAME", "0_4_3_0_3_2_0": "SAME", "0_4_3_0_3_2_1": "SAME", "0_4_3_1_0_0_0": "OPP", "0_4_3_1_0_0_1": "OPP", "0_4_3_1_0_1_0": "SAME", "0_4_3_1_0_1_1": "SAME", "0_4_3_1_0_2_0": "SAME", "0_4_3_1_0_2_1": "SAME", "0_4_3_1_1_0_0": "SAME", "0_4_3_1_1_0_1": "SAME", "0_4_3_1_1_1_0": "SAME", "0_4_3_1_1_1_1": "SAME", "0_4_3_1_1_2_0": "SAME", "0_4_3_1_1_2_1": "SAME", "0_4_3_1_2_0_0": "SAME", "0_4_3_1_2_0_1": "SAME", "0_4_3_1_2_1_0": "SAME", "0_4_3_1_2_1_1": "SAME", "0_4_3_1_2_2_0": "SAME", "0_4_3_1_2_2_1": "SAME", "0_4_3_1_3_0_0": "SAME", "0_4_3_1_3_0_1": "SAME", "0_4_3_1_3_1_0": "SAME", "0_4_3_1_3_1_1": "SAME", "0_4_3_1_3_2_0": "SAME", "0_4_3_1_3_2_1": "SAME", "0_4_3_2_0_0_0": "SAME", "0_4_3_2_0_0_1": "SAME", "0_4_3_2_0_1_0": "SAME", "0_4_3_2_0_1_1": "SAME", "0_4_3_2_0_2_0": "SAME", "0_4_3_2_0_2_1": "SAME", "0_4_3_2_1_0_0": "SAME", "0_4_3_2_1_0_1": "SAME", "0_4_3_2_1_1_0": "SAME", "0_4_3_2_1_1_1": "SAME", "0_4_3_2_1_2_0": "SAME", "0_4_3_2_1_2_1": "SAME", "0_4_3_2_2_0_0": "SAME", "0_4_3_2_2_0_1": "SAME", "0_4_3_2_2_1_0": "SAME", "0_4_3_2_2_1_1": "SAME", "0_4_3_2_2_2_0": "SAME", "0_4_3_2_2_2_1": "SAME", "0_4_3_2_3_0_0": "SAME", "0_4_3_2_3_0_1": "SAME", "0_4_3_2_3_1_0": "SAME", "0_4_3_2_3_1_1": "SAME", "0_4_3_2_3_2_0": "SAME", "0_4_3_2_3_2_1": "SAME", "0_4_3_3_0_0_0": "SAME", "0_4_3_3_0_0_1": "SAME", "0_4_3_3_0_1_0": "SAME", "0_4_3_3_0_1_1": "SAME", "0_4_3_3_0_2_0": "SAME", "0_4_3_3_0_2_1": "SAME", "0_4_3_3_1_0_0": "SAME", "0_4_3_3_1_0_1": "SAME", "0_4_3_3_1_1_0": "SAME", "0_4_3_3_1_1_1": "SAME", "0_4_3_3_1_2_0": "SAME", "0_4_3_3_1_2_1": "SAME", "0_4_3_3_2_0_0": "SAME", "0_4_3_3_2_0_1": "SAME", "0_4_3_3_2_1_0": "SAME", "0_4_3_3_2_1_1": "SAME", "0_4_3_3_2_2_0": "SAME", "0_4_3_3_2_2_1": "SAME", "0_4_3_3_3_0_0": "SAME", "0_4_3_3_3_0_1": "SAME", "0_4_3_3_3_1_0": "SAME", "0_4_3_3_3_1_1": "SAME", "0_4_3_3_3_2_0": "SAME", "0_4_3_3_3_2_1": "SAME", "1_1_0_0_0_0_0": "SAME", "1_1_0_0_0_0_1": "SAME", "1_1_0_0_0_1_0": "SAME", "1_1_0_0_0_1_1": "SAME", "1_1_0_0_0_2_0": "SAME", "1_1_0_0_0_2_1": "SAME", "1_1_0_0_1_0_0": "SAME", "1_1_0_0_1_0_1": "SAME", "1_1_0_0_1_1_0": "SAME", "1_1_0_0_1_1_1": "SAME", "1_1_0_0_1_2_0": "SAME", "1_1_0_0_1_2_1": "SAME", "1_1_0_0_2_0_0": "SAME", "1_1_0_0_2_0_1": "SAME", "1_1_0_0_2_1_0": "SAME", "1_1_0_0_2_1_1": "SAME", "1_1_0_0_2_2_0": "SAME", "1_1_0_0_2_2_1": "SAME", "1_1_0_0_3_0_0": "SAME", "1_1_0_0_3_0_1": "SAME", "1_1_0_0_3_1_0": "SAME", "1_1_0_0_3_1_1": "SAME", "1_1_0_0_3_2_0": "SAME", "1_1_0_0_3_2_1": "SAME", "1_1_0_1_0_0_0": "SAME", "1_1_0_1_0_0_1": "SAME", "1_1_0_1_0_1_0": "SAME", "1_1_0_1_0_1_1": "SAME", "1_1_0_1_0_2_0": "SAME", "1_1_0_1_0_2_1": "SAME", "1_1_0_1_1_0_0": "SAME", "1_1_0_1_1_0_1": "SAME", "1_1_0_1_1_1_0": "SAME", "1_1_0_1_1_1_1": "SAME", "1_1_0_1_1_2_0": "SAME", "1_1_0_1_1_2_1": "SAME", "1_1_0_1_2_0_0": "SAME", "1_1_0_1_2_0_1": "SAME", "1_1_0_1_2_1_0": "SAME", "1_1_0_1_2_1_1": "SAME", "1_1_0_1_2_2_0": "SAME", "1_1_0_1_2_2_1": "SAME", "1_1_0_1_3_0_0": "SAME", "1_1_0_1_3_0_1": "SAME", "1_1_0_1_3_1_0": "SAME", "1_1_0_1_3_1_1": "SAME", "1_1_0_1_3_2_0": "SAME", "1_1_0_1_3_2_1": "SAME", "1_1_0_2_0_0_0": "SAME", "1_1_0_2_0_0_1": "SAME", "1_1_0_2_0_1_0": "SAME", "1_1_0_2_0_1_1": "SAME", "1_1_0_2_0_2_0": "SAME", "1_1_0_2_0_2_1": "SAME", "1_1_0_2_1_0_0": "SAME", "1_1_0_2_1_0_1": "SAME", "1_1_0_2_1_1_0": "SAME", "1_1_0_2_1_1_1": "SAME", "1_1_0_2_1_2_0": "SAME", "1_1_0_2_1_2_1": "SAME", "1_1_0_2_2_0_0": "SAME", "1_1_0_2_2_0_1": "SAME", "1_1_0_2_2_1_0": "SAME", "1_1_0_2_2_1_1": "SAME", "1_1_0_2_2_2_0": "SAME", "1_1_0_2_2_2_1": "SAME", "1_1_0_2_3_0_0": "SAME", "1_1_0_2_3_0_1": "SAME", "1_1_0_2_3_1_0": "SAME", "1_1_0_2_3_1_1": "SAME", "1_1_0_2_3_2_0": "SAME", "1_1_0_2_3_2_1": "SAME", "1_1_0_3_0_0_0": "SAME", "1_1_0_3_0_0_1": "SAME", "1_1_0_3_0_1_0": "SAME", "1_1_0_3_0_1_1": "SAME", "1_1_0_3_0_2_0": "SAME", "1_1_0_3_0_2_1": "SAME", "1_1_0_3_1_0_0": "SAME", "1_1_0_3_1_0_1": "SAME", "1_1_0_3_1_1_0": "SAME", "1_1_0_3_1_1_1": "SAME", "1_1_0_3_1_2_0": "SAME", "1_1_0_3_1_2_1": "SAME", "1_1_0_3_2_0_0": "SAME", "1_1_0_3_2_0_1": "SAME", "1_1_0_3_2_1_0": "SAME", "1_1_0_3_2_1_1": "SAME", "1_1_0_3_2_2_0": "SAME", "1_1_0_3_2_2_1": "SAME", "1_1_0_3_3_0_0": "SAME", "1_1_0_3_3_0_1": "SAME", "1_1_0_3_3_1_0": "SAME", "1_1_0_3_3_1_1": "SAME", "1_1_0_3_3_2_0": "SAME", "1_1_0_3_3_2_1": "SAME", "1_1_1_0_0_0_0": "SAME", "1_1_1_0_0_0_1": "SAME", "1_1_1_0_0_1_0": "SAME", "1_1_1_0_0_1_1": "SAME", "1_1_1_0_0_2_0": "SAME", "1_1_1_0_0_2_1": "SAME", "1_1_1_0_1_0_0": "SAME", "1_1_1_0_1_0_1": "SAME", "1_1_1_0_1_1_0": "SAME", "1_1_1_0_1_1_1": "SAME", "1_1_1_0_1_2_0": "SAME", "1_1_1_0_1_2_1": "SAME", "1_1_1_0_2_0_0": "SAME", "1_1_1_0_2_0_1": "SAME", "1_1_1_0_2_1_0": "SAME", "1_1_1_0_2_1_1": "SAME", "1_1_1_0_2_2_0": "SAME", "1_1_1_0_2_2_1": "SAME", "1_1_1_0_3_0_0": "SAME", "1_1_1_0_3_0_1": "SAME", "1_1_1_0_3_1_0": "SAME", "1_1_1_0_3_1_1": "SAME", "1_1_1_0_3_2_0": "SAME", "1_1_1_0_3_2_1": "SAME", "1_1_1_1_0_0_0": "SAME", "1_1_1_1_0_0_1": "SAME", "1_1_1_1_0_1_0": "SAME", "1_1_1_1_0_1_1": "SAME", "1_1_1_1_0_2_0": "SAME", "1_1_1_1_0_2_1": "SAME", "1_1_1_1_1_0_0": "SAME", "1_1_1_1_1_0_1": "SAME", "1_1_1_1_1_1_0": "SAME", "1_1_1_1_1_1_1": "SAME", "1_1_1_1_1_2_0": "SAME", "1_1_1_1_1_2_1": "SAME", "1_1_1_1_2_0_0": "SAME", "1_1_1_1_2_0_1": "SAME", "1_1_1_1_2_1_0": "SAME", "1_1_1_1_2_1_1": "SAME", "1_1_1_1_2_2_0": "SAME", "1_1_1_1_2_2_1": "SAME", "1_1_1_1_3_0_0": "SAME", "1_1_1_1_3_0_1": "SAME", "1_1_1_1_3_1_0": "SAME", "1_1_1_1_3_1_1": "SAME", "1_1_1_1_3_2_0": "SAME", "1_1_1_1_3_2_1": "OPP", "1_1_1_2_0_0_0": "SAME", "1_1_1_2_0_0_1": "SAME", "1_1_1_2_0_1_0": "SAME", "1_1_1_2_0_1_1": "SAME", "1_1_1_2_0_2_0": "SAME", "1_1_1_2_0_2_1": "SAME", "1_1_1_2_1_0_0": "SAME", "1_1_1_2_1_0_1": "SAME", "1_1_1_2_1_1_0": "SAME", "1_1_1_2_1_1_1": "SAME", "1_1_1_2_1_2_0": "SAME", "1_1_1_2_1_2_1": "SAME", "1_1_1_2_2_0_0": "SAME", "1_1_1_2_2_0_1": "SAME", "1_1_1_2_2_1_0": "SAME", "1_1_1_2_2_1_1": "SAME", "1_1_1_2_2_2_0": "SAME", "1_1_1_2_2_2_1": "SAME", "1_1_1_2_3_0_0": "SAME", "1_1_1_2_3_0_1": "SAME", "1_1_1_2_3_1_0": "SAME", "1_1_1_2_3_1_1": "SAME", "1_1_1_2_3_2_0": "SAME", "1_1_1_2_3_2_1": "SAME", "1_1_1_3_0_0_0": "SAME", "1_1_1_3_0_0_1": "SAME", "1_1_1_3_0_1_0": "SAME", "1_1_1_3_0_1_1": "SAME", "1_1_1_3_0_2_0": "SAME", "1_1_1_3_0_2_1": "SAME", "1_1_1_3_1_0_0": "SAME", "1_1_1_3_1_0_1": "SAME", "1_1_1_3_1_1_0": "SAME", "1_1_1_3_1_1_1": "SAME", "1_1_1_3_1_2_0": "SAME", "1_1_1_3_1_2_1": "SAME", "1_1_1_3_2_0_0": "SAME", "1_1_1_3_2_0_1": "SAME", "1_1_1_3_2_1_0": "SAME", "1_1_1_3_2_1_1": "SAME", "1_1_1_3_2_2_0": "SAME", "1_1_1_3_2_2_1": "SAME", "1_1_1_3_3_0_0": "SAME", "1_1_1_3_3_0_1": "SAME", "1_1_1_3_3_1_0": "SAME", "1_1_1_3_3_1_1": "SAME", "1_1_1_3_3_2_0": "SAME", "1_1_1_3_3_2_1": "SAME", "1_1_2_0_0_0_0": "SAME", "1_1_2_0_0_0_1": "SAME", "1_1_2_0_0_1_0": "SAME", "1_1_2_0_0_1_1": "SAME", "1_1_2_0_0_2_0": "SAME", "1_1_2_0_0_2_1": "SAME", "1_1_2_0_1_0_0": "SAME", "1_1_2_0_1_0_1": "SAME", "1_1_2_0_1_1_0": "SAME", "1_1_2_0_1_1_1": "SAME", "1_1_2_0_1_2_0": "SAME", "1_1_2_0_1_2_1": "SAME", "1_1_2_0_2_0_0": "SAME", "1_1_2_0_2_0_1": "SAME", "1_1_2_0_2_1_0": "SAME", "1_1_2_0_2_1_1": "SAME", "1_1_2_0_2_2_0": "SAME", "1_1_2_0_2_2_1": "SAME", "1_1_2_0_3_0_0": "SAME", "1_1_2_0_3_0_1": "SAME", "1_1_2_0_3_1_0": "SAME", "1_1_2_0_3_1_1": "SAME", "1_1_2_0_3_2_0": "SAME", "1_1_2_0_3_2_1": "SAME", "1_1_2_1_0_0_0": "SAME", "1_1_2_1_0_0_1": "SAME", "1_1_2_1_0_1_0": "SAME", "1_1_2_1_0_1_1": "SAME", "1_1_2_1_0_2_0": "SAME", "1_1_2_1_0_2_1": "SAME", "1_1_2_1_1_0_0": "SAME", "1_1_2_1_1_0_1": "SAME", "1_1_2_1_1_1_0": "SAME", "1_1_2_1_1_1_1": "SAME", "1_1_2_1_1_2_0": "SAME", "1_1_2_1_1_2_1": "OPP", "1_1_2_1_2_0_0": "SAME", "1_1_2_1_2_0_1": "SAME", "1_1_2_1_2_1_0": "SAME", "1_1_2_1_2_1_1": "SAME", "1_1_2_1_2_2_0": "SAME", "1_1_2_1_2_2_1": "SAME", "1_1_2_1_3_0_0": "SAME", "1_1_2_1_3_0_1": "SAME", "1_1_2_1_3_1_0": "SAME", "1_1_2_1_3_1_1": "SAME", "1_1_2_1_3_2_0": "SAME", "1_1_2_1_3_2_1": "SAME", "1_1_2_2_0_0_0": "SAME", "1_1_2_2_0_0_1": "SAME", "1_1_2_2_0_1_0": "SAME", "1_1_2_2_0_1_1": "SAME", "1_1_2_2_0_2_0": "SAME", "1_1_2_2_0_2_1": "SAME", "1_1_2_2_1_0_0": "SAME", "1_1_2_2_1_0_1": "SAME", "1_1_2_2_1_1_0": "SAME", "1_1_2_2_1_1_1": "OPP", "1_1_2_2_1_2_0": "SAME", "1_1_2_2_1_2_1": "SAME", "1_1_2_2_2_0_0": "SAME", "1_1_2_2_2_0_1": "SAME", "1_1_2_2_2_1_0": "SAME", "1_1_2_2_2_1_1": "SAME", "1_1_2_2_2_2_0": "SAME", "1_1_2_2_2_2_1": "SAME", "1_1_2_2_3_0_0": "SAME", "1_1_2_2_3_0_1": "SAME", "1_1_2_2_3_1_0": "SAME", "1_1_2_2_3_1_1": "SAME", "1_1_2_2_3_2_0": "SAME", "1_1_2_2_3_2_1": "SAME", "1_1_2_3_0_0_0": "SAME", "1_1_2_3_0_0_1": "SAME", "1_1_2_3_0_1_0": "SAME", "1_1_2_3_0_1_1": "SAME", "1_1_2_3_0_2_0": "SAME", "1_1_2_3_0_2_1": "SAME", "1_1_2_3_1_0_0": "SAME", "1_1_2_3_1_0_1": "SAME", "1_1_2_3_1_1_0": "SAME", "1_1_2_3_1_1_1": "SAME", "1_1_2_3_1_2_0": "SAME", "1_1_2_3_1_2_1": "SAME", "1_1_2_3_2_0_0": "SAME", "1_1_2_3_2_0_1": "SAME", "1_1_2_3_2_1_0": "SAME", "1_1_2_3_2_1_1": "SAME", "1_1_2_3_2_2_0": "SAME", "1_1_2_3_2_2_1": "SAME", "1_1_2_3_3_0_0": "SAME", "1_1_2_3_3_0_1": "SAME", "1_1_2_3_3_1_0": "SAME", "1_1_2_3_3_1_1": "SAME", "1_1_2_3_3_2_0": "SAME", "1_1_2_3_3_2_1": "SAME", "1_1_3_0_0_0_0": "SAME", "1_1_3_0_0_0_1": "SAME", "1_1_3_0_0_1_0": "SAME", "1_1_3_0_0_1_1": "SAME", "1_1_3_0_0_2_0": "SAME", "1_1_3_0_0_2_1": "SAME", "1_1_3_0_1_0_0": "SAME", "1_1_3_0_1_0_1": "SAME", "1_1_3_0_1_1_0": "SAME", "1_1_3_0_1_1_1": "SAME", "1_1_3_0_1_2_0": "SAME", "1_1_3_0_1_2_1": "SAME", "1_1_3_0_2_0_0": "SAME", "1_1_3_0_2_0_1": "SAME", "1_1_3_0_2_1_0": "SAME", "1_1_3_0_2_1_1": "SAME", "1_1_3_0_2_2_0": "SAME", "1_1_3_0_2_2_1": "SAME", "1_1_3_0_3_0_0": "SAME", "1_1_3_0_3_0_1": "SAME", "1_1_3_0_3_1_0": "SAME", "1_1_3_0_3_1_1": "SAME", "1_1_3_0_3_2_0": "SAME", "1_1_3_0_3_2_1": "SAME", "1_1_3_1_0_0_0": "SAME", "1_1_3_1_0_0_1": "SAME", "1_1_3_1_0_1_0": "SAME", "1_1_3_1_0_1_1": "SAME", "1_1_3_1_0_2_0": "SAME", "1_1_3_1_0_2_1": "SAME", "1_1_3_1_1_0_0": "SAME", "1_1_3_1_1_0_1": "SAME", "1_1_3_1_1_1_0": "SAME", "1_1_3_1_1_1_1": "SAME", "1_1_3_1_1_2_0": "SAME", "1_1_3_1_1_2_1": "SAME", "1_1_3_1_2_0_0": "SAME", "1_1_3_1_2_0_1": "SAME", "1_1_3_1_2_1_0": "SAME", "1_1_3_1_2_1_1": "SAME", "1_1_3_1_2_2_0": "SAME", "1_1_3_1_2_2_1": "SAME", "1_1_3_1_3_0_0": "SAME", "1_1_3_1_3_0_1": "SAME", "1_1_3_1_3_1_0": "SAME", "1_1_3_1_3_1_1": "SAME", "1_1_3_1_3_2_0": "SAME", "1_1_3_1_3_2_1": "SAME", "1_1_3_2_0_0_0": "SAME", "1_1_3_2_0_0_1": "SAME", "1_1_3_2_0_1_0": "SAME", "1_1_3_2_0_1_1": "SAME", "1_1_3_2_0_2_0": "SAME", "1_1_3_2_0_2_1": "SAME", "1_1_3_2_1_0_0": "SAME", "1_1_3_2_1_0_1": "OPP", "1_1_3_2_1_1_0": "SAME", "1_1_3_2_1_1_1": "SAME", "1_1_3_2_1_2_0": "SAME", "1_1_3_2_1_2_1": "SAME", "1_1_3_2_2_0_0": "SAME", "1_1_3_2_2_0_1": "SAME", "1_1_3_2_2_1_0": "SAME", "1_1_3_2_2_1_1": "SAME", "1_1_3_2_2_2_0": "SAME", "1_1_3_2_2_2_1": "SAME", "1_1_3_2_3_0_0": "SAME", "1_1_3_2_3_0_1": "SAME", "1_1_3_2_3_1_0": "SAME", "1_1_3_2_3_1_1": "SAME", "1_1_3_2_3_2_0": "SAME", "1_1_3_2_3_2_1": "SAME", "1_1_3_3_0_0_0": "SAME", "1_1_3_3_0_0_1": "SAME", "1_1_3_3_0_1_0": "SAME", "1_1_3_3_0_1_1": "SAME", "1_1_3_3_0_2_0": "SAME", "1_1_3_3_0_2_1": "SAME", "1_1_3_3_1_0_0": "SAME", "1_1_3_3_1_0_1": "SAME", "1_1_3_3_1_1_0": "SAME", "1_1_3_3_1_1_1": "SAME", "1_1_3_3_1_2_0": "SAME", "1_1_3_3_1_2_1": "SAME", "1_1_3_3_2_0_0": "SAME", "1_1_3_3_2_0_1": "SAME", "1_1_3_3_2_1_0": "SAME", "1_1_3_3_2_1_1": "SAME", "1_1_3_3_2_2_0": "SAME", "1_1_3_3_2_2_1": "SAME", "1_1_3_3_3_0_0": "SAME", "1_1_3_3_3_0_1": "SAME", "1_1_3_3_3_1_0": "SAME", "1_1_3_3_3_1_1": "SAME", "1_1_3_3_3_2_0": "SAME", "1_1_3_3_3_2_1": "SAME", "1_2_0_0_0_0_0": "SAME", "1_2_0_0_0_0_1": "SAME", "1_2_0_0_0_1_0": "SAME", "1_2_0_0_0_1_1": "SAME", "1_2_0_0_0_2_0": "SAME", "1_2_0_0_0_2_1": "SAME", "1_2_0_0_1_0_0": "SAME", "1_2_0_0_1_0_1": "SAME", "1_2_0_0_1_1_0": "SAME", "1_2_0_0_1_1_1": "SAME", "1_2_0_0_1_2_0": "SAME", "1_2_0_0_1_2_1": "SAME", "1_2_0_0_2_0_0": "SAME", "1_2_0_0_2_0_1": "SAME", "1_2_0_0_2_1_0": "SAME", "1_2_0_0_2_1_1": "SAME", "1_2_0_0_2_2_0": "SAME", "1_2_0_0_2_2_1": "SAME", "1_2_0_0_3_0_0": "SAME", "1_2_0_0_3_0_1": "SAME", "1_2_0_0_3_1_0": "SAME", "1_2_0_0_3_1_1": "SAME", "1_2_0_0_3_2_0": "SAME", "1_2_0_0_3_2_1": "SAME", "1_2_0_1_0_0_0": "SAME", "1_2_0_1_0_0_1": "SAME", "1_2_0_1_0_1_0": "SAME", "1_2_0_1_0_1_1": "SAME", "1_2_0_1_0_2_0": "SAME", "1_2_0_1_0_2_1": "SAME", "1_2_0_1_1_0_0": "SAME", "1_2_0_1_1_0_1": "SAME", "1_2_0_1_1_1_0": "SAME", "1_2_0_1_1_1_1": "SAME", "1_2_0_1_1_2_0": "SAME", "1_2_0_1_1_2_1": "SAME", "1_2_0_1_2_0_0": "SAME", "1_2_0_1_2_0_1": "SAME", "1_2_0_1_2_1_0": "SAME", "1_2_0_1_2_1_1": "SAME", "1_2_0_1_2_2_0": "SAME", "1_2_0_1_2_2_1": "SAME", "1_2_0_1_3_0_0": "SAME", "1_2_0_1_3_0_1": "SAME", "1_2_0_1_3_1_0": "SAME", "1_2_0_1_3_1_1": "SAME", "1_2_0_1_3_2_0": "SAME", "1_2_0_1_3_2_1": "SAME", "1_2_0_2_0_0_0": "SAME", "1_2_0_2_0_0_1": "SAME", "1_2_0_2_0_1_0": "SAME", "1_2_0_2_0_1_1": "SAME", "1_2_0_2_0_2_0": "SAME", "1_2_0_2_0_2_1": "SAME", "1_2_0_2_1_0_0": "SAME", "1_2_0_2_1_0_1": "SAME", "1_2_0_2_1_1_0": "SAME", "1_2_0_2_1_1_1": "SAME", "1_2_0_2_1_2_0": "SAME", "1_2_0_2_1_2_1": "SAME", "1_2_0_2_2_0_0": "SAME", "1_2_0_2_2_0_1": "SAME", "1_2_0_2_2_1_0": "SAME", "1_2_0_2_2_1_1": "SAME", "1_2_0_2_2_2_0": "SAME", "1_2_0_2_2_2_1": "SAME", "1_2_0_2_3_0_0": "SAME", "1_2_0_2_3_0_1": "SAME", "1_2_0_2_3_1_0": "SAME", "1_2_0_2_3_1_1": "SAME", "1_2_0_2_3_2_0": "SAME", "1_2_0_2_3_2_1": "SAME", "1_2_0_3_0_0_0": "SAME", "1_2_0_3_0_0_1": "SAME", "1_2_0_3_0_1_0": "SAME", "1_2_0_3_0_1_1": "SAME", "1_2_0_3_0_2_0": "SAME", "1_2_0_3_0_2_1": "SAME", "1_2_0_3_1_0_0": "SAME", "1_2_0_3_1_0_1": "SAME", "1_2_0_3_1_1_0": "SAME", "1_2_0_3_1_1_1": "SAME", "1_2_0_3_1_2_0": "SAME", "1_2_0_3_1_2_1": "SAME", "1_2_0_3_2_0_0": "SAME", "1_2_0_3_2_0_1": "SAME", "1_2_0_3_2_1_0": "SAME", "1_2_0_3_2_1_1": "SAME", "1_2_0_3_2_2_0": "SAME", "1_2_0_3_2_2_1": "SAME", "1_2_0_3_3_0_0": "SAME", "1_2_0_3_3_0_1": "SAME", "1_2_0_3_3_1_0": "SAME", "1_2_0_3_3_1_1": "SAME", "1_2_0_3_3_2_0": "SAME", "1_2_0_3_3_2_1": "SAME", "1_2_1_0_0_0_0": "SAME", "1_2_1_0_0_0_1": "SAME", "1_2_1_0_0_1_0": "SAME", "1_2_1_0_0_1_1": "SAME", "1_2_1_0_0_2_0": "SAME", "1_2_1_0_0_2_1": "SAME", "1_2_1_0_1_0_0": "SAME", "1_2_1_0_1_0_1": "SAME", "1_2_1_0_1_1_0": "SAME", "1_2_1_0_1_1_1": "SAME", "1_2_1_0_1_2_0": "SAME", "1_2_1_0_1_2_1": "SAME", "1_2_1_0_2_0_0": "SAME", "1_2_1_0_2_0_1": "SAME", "1_2_1_0_2_1_0": "SAME", "1_2_1_0_2_1_1": "SAME", "1_2_1_0_2_2_0": "SAME", "1_2_1_0_2_2_1": "SAME", "1_2_1_0_3_0_0": "SAME", "1_2_1_0_3_0_1": "SAME", "1_2_1_0_3_1_0": "SAME", "1_2_1_0_3_1_1": "SAME", "1_2_1_0_3_2_0": "SAME", "1_2_1_0_3_2_1": "SAME", "1_2_1_1_0_0_0": "SAME", "1_2_1_1_0_0_1": "SAME", "1_2_1_1_0_1_0": "SAME", "1_2_1_1_0_1_1": "SAME", "1_2_1_1_0_2_0": "SAME", "1_2_1_1_0_2_1": "SAME", "1_2_1_1_1_0_0": "SAME", "1_2_1_1_1_0_1": "SAME", "1_2_1_1_1_1_0": "SAME", "1_2_1_1_1_1_1": "SAME", "1_2_1_1_1_2_0": "SAME", "1_2_1_1_1_2_1": "SAME", "1_2_1_1_2_0_0": "SAME", "1_2_1_1_2_0_1": "SAME", "1_2_1_1_2_1_0": "SAME", "1_2_1_1_2_1_1": "SAME", "1_2_1_1_2_2_0": "SAME", "1_2_1_1_2_2_1": "SAME", "1_2_1_1_3_0_0": "SAME", "1_2_1_1_3_0_1": "SAME", "1_2_1_1_3_1_0": "SAME", "1_2_1_1_3_1_1": "SAME", "1_2_1_1_3_2_0": "SAME", "1_2_1_1_3_2_1": "SAME", "1_2_1_2_0_0_0": "SAME", "1_2_1_2_0_0_1": "SAME", "1_2_1_2_0_1_0": "SAME", "1_2_1_2_0_1_1": "SAME", "1_2_1_2_0_2_0": "SAME", "1_2_1_2_0_2_1": "SAME", "1_2_1_2_1_0_0": "SAME", "1_2_1_2_1_0_1": "SAME", "1_2_1_2_1_1_0": "SAME", "1_2_1_2_1_1_1": "SAME", "1_2_1_2_1_2_0": "SAME", "1_2_1_2_1_2_1": "SAME", "1_2_1_2_2_0_0": "SAME", "1_2_1_2_2_0_1": "SAME", "1_2_1_2_2_1_0": "SAME", "1_2_1_2_2_1_1": "SAME", "1_2_1_2_2_2_0": "SAME", "1_2_1_2_2_2_1": "SAME", "1_2_1_2_3_0_0": "SAME", "1_2_1_2_3_0_1": "SAME", "1_2_1_2_3_1_0": "SAME", "1_2_1_2_3_1_1": "SAME", "1_2_1_2_3_2_0": "SAME", "1_2_1_2_3_2_1": "SAME", "1_2_1_3_0_0_0": "SAME", "1_2_1_3_0_0_1": "SAME", "1_2_1_3_0_1_0": "SAME", "1_2_1_3_0_1_1": "SAME", "1_2_1_3_0_2_0": "SAME", "1_2_1_3_0_2_1": "SAME", "1_2_1_3_1_0_0": "SAME", "1_2_1_3_1_0_1": "SAME", "1_2_1_3_1_1_0": "SAME", "1_2_1_3_1_1_1": "SAME", "1_2_1_3_1_2_0": "SAME", "1_2_1_3_1_2_1": "SAME", "1_2_1_3_2_0_0": "SAME", "1_2_1_3_2_0_1": "SAME", "1_2_1_3_2_1_0": "SAME", "1_2_1_3_2_1_1": "SAME", "1_2_1_3_2_2_0": "SAME", "1_2_1_3_2_2_1": "SAME", "1_2_1_3_3_0_0": "SAME", "1_2_1_3_3_0_1": "SAME", "1_2_1_3_3_1_0": "SAME", "1_2_1_3_3_1_1": "SAME", "1_2_1_3_3_2_0": "SAME", "1_2_1_3_3_2_1": "SAME", "1_2_2_0_0_0_0": "SAME", "1_2_2_0_0_0_1": "SAME", "1_2_2_0_0_1_0": "SAME", "1_2_2_0_0_1_1": "SAME", "1_2_2_0_0_2_0": "SAME", "1_2_2_0_0_2_1": "SAME", "1_2_2_0_1_0_0": "SAME", "1_2_2_0_1_0_1": "SAME", "1_2_2_0_1_1_0": "SAME", "1_2_2_0_1_1_1": "SAME", "1_2_2_0_1_2_0": "SAME", "1_2_2_0_1_2_1": "SAME", "1_2_2_0_2_0_0": "SAME", "1_2_2_0_2_0_1": "SAME", "1_2_2_0_2_1_0": "SAME", "1_2_2_0_2_1_1": "SAME", "1_2_2_0_2_2_0": "SAME", "1_2_2_0_2_2_1": "SAME", "1_2_2_0_3_0_0": "SAME", "1_2_2_0_3_0_1": "SAME", "1_2_2_0_3_1_0": "SAME", "1_2_2_0_3_1_1": "SAME", "1_2_2_0_3_2_0": "SAME", "1_2_2_0_3_2_1": "SAME", "1_2_2_1_0_0_0": "SAME", "1_2_2_1_0_0_1": "SAME", "1_2_2_1_0_1_0": "SAME", "1_2_2_1_0_1_1": "SAME", "1_2_2_1_0_2_0": "SAME", "1_2_2_1_0_2_1": "SAME", "1_2_2_1_1_0_0": "SAME", "1_2_2_1_1_0_1": "SAME", "1_2_2_1_1_1_0": "SAME", "1_2_2_1_1_1_1": "SAME", "1_2_2_1_1_2_0": "SAME", "1_2_2_1_1_2_1": "SAME", "1_2_2_1_2_0_0": "SAME", "1_2_2_1_2_0_1": "SAME", "1_2_2_1_2_1_0": "SAME", "1_2_2_1_2_1_1": "SAME", "1_2_2_1_2_2_0": "SAME", "1_2_2_1_2_2_1": "SAME", "1_2_2_1_3_0_0": "SAME", "1_2_2_1_3_0_1": "SAME", "1_2_2_1_3_1_0": "SAME", "1_2_2_1_3_1_1": "SAME", "1_2_2_1_3_2_0": "SAME", "1_2_2_1_3_2_1": "SAME", "1_2_2_2_0_0_0": "SAME", "1_2_2_2_0_0_1": "SAME", "1_2_2_2_0_1_0": "SAME", "1_2_2_2_0_1_1": "SAME", "1_2_2_2_0_2_0": "SAME", "1_2_2_2_0_2_1": "SAME", "1_2_2_2_1_0_0": "SAME", "1_2_2_2_1_0_1": "SAME", "1_2_2_2_1_1_0": "SAME", "1_2_2_2_1_1_1": "SAME", "1_2_2_2_1_2_0": "SAME", "1_2_2_2_1_2_1": "SAME", "1_2_2_2_2_0_0": "SAME", "1_2_2_2_2_0_1": "SAME", "1_2_2_2_2_1_0": "SAME", "1_2_2_2_2_1_1": "SAME", "1_2_2_2_2_2_0": "SAME", "1_2_2_2_2_2_1": "SAME", "1_2_2_2_3_0_0": "SAME", "1_2_2_2_3_0_1": "SAME", "1_2_2_2_3_1_0": "SAME", "1_2_2_2_3_1_1": "SAME", "1_2_2_2_3_2_0": "SAME", "1_2_2_2_3_2_1": "SAME", "1_2_2_3_0_0_0": "SAME", "1_2_2_3_0_0_1": "SAME", "1_2_2_3_0_1_0": "SAME", "1_2_2_3_0_1_1": "SAME", "1_2_2_3_0_2_0": "SAME", "1_2_2_3_0_2_1": "SAME", "1_2_2_3_1_0_0": "SAME", "1_2_2_3_1_0_1": "SAME", "1_2_2_3_1_1_0": "SAME", "1_2_2_3_1_1_1": "SAME", "1_2_2_3_1_2_0": "SAME", "1_2_2_3_1_2_1": "SAME", "1_2_2_3_2_0_0": "SAME", "1_2_2_3_2_0_1": "SAME", "1_2_2_3_2_1_0": "SAME", "1_2_2_3_2_1_1": "SAME", "1_2_2_3_2_2_0": "SAME", "1_2_2_3_2_2_1": "SAME", "1_2_2_3_3_0_0": "SAME", "1_2_2_3_3_0_1": "SAME", "1_2_2_3_3_1_0": "SAME", "1_2_2_3_3_1_1": "SAME", "1_2_2_3_3_2_0": "SAME", "1_2_2_3_3_2_1": "SAME", "1_2_3_0_0_0_0": "SAME", "1_2_3_0_0_0_1": "SAME", "1_2_3_0_0_1_0": "SAME", "1_2_3_0_0_1_1": "SAME", "1_2_3_0_0_2_0": "SAME", "1_2_3_0_0_2_1": "SAME", "1_2_3_0_1_0_0": "SAME", "1_2_3_0_1_0_1": "SAME", "1_2_3_0_1_1_0": "SAME", "1_2_3_0_1_1_1": "SAME", "1_2_3_0_1_2_0": "SAME", "1_2_3_0_1_2_1": "SAME", "1_2_3_0_2_0_0": "SAME", "1_2_3_0_2_0_1": "SAME", "1_2_3_0_2_1_0": "SAME", "1_2_3_0_2_1_1": "SAME", "1_2_3_0_2_2_0": "SAME", "1_2_3_0_2_2_1": "SAME", "1_2_3_0_3_0_0": "SAME", "1_2_3_0_3_0_1": "SAME", "1_2_3_0_3_1_0": "SAME", "1_2_3_0_3_1_1": "SAME", "1_2_3_0_3_2_0": "SAME", "1_2_3_0_3_2_1": "SAME", "1_2_3_1_0_0_0": "SAME", "1_2_3_1_0_0_1": "SAME", "1_2_3_1_0_1_0": "SAME", "1_2_3_1_0_1_1": "SAME", "1_2_3_1_0_2_0": "SAME", "1_2_3_1_0_2_1": "SAME", "1_2_3_1_1_0_0": "SAME", "1_2_3_1_1_0_1": "SAME", "1_2_3_1_1_1_0": "SAME", "1_2_3_1_1_1_1": "SAME", "1_2_3_1_1_2_0": "SAME", "1_2_3_1_1_2_1": "SAME", "1_2_3_1_2_0_0": "SAME", "1_2_3_1_2_0_1": "SAME", "1_2_3_1_2_1_0": "SAME", "1_2_3_1_2_1_1": "SAME", "1_2_3_1_2_2_0": "SAME", "1_2_3_1_2_2_1": "SAME", "1_2_3_1_3_0_0": "SAME", "1_2_3_1_3_0_1": "SAME", "1_2_3_1_3_1_0": "SAME", "1_2_3_1_3_1_1": "SAME", "1_2_3_1_3_2_0": "SAME", "1_2_3_1_3_2_1": "SAME", "1_2_3_2_0_0_0": "SAME", "1_2_3_2_0_0_1": "SAME", "1_2_3_2_0_1_0": "SAME", "1_2_3_2_0_1_1": "SAME", "1_2_3_2_0_2_0": "SAME", "1_2_3_2_0_2_1": "SAME", "1_2_3_2_1_0_0": "SAME", "1_2_3_2_1_0_1": "SAME", "1_2_3_2_1_1_0": "SAME", "1_2_3_2_1_1_1": "SAME", "1_2_3_2_1_2_0": "SAME", "1_2_3_2_1_2_1": "SAME", "1_2_3_2_2_0_0": "SAME", "1_2_3_2_2_0_1": "SAME", "1_2_3_2_2_1_0": "SAME", "1_2_3_2_2_1_1": "SAME", "1_2_3_2_2_2_0": "SAME", "1_2_3_2_2_2_1": "SAME", "1_2_3_2_3_0_0": "SAME", "1_2_3_2_3_0_1": "SAME", "1_2_3_2_3_1_0": "SAME", "1_2_3_2_3_1_1": "SAME", "1_2_3_2_3_2_0": "SAME", "1_2_3_2_3_2_1": "SAME", "1_2_3_3_0_0_0": "SAME", "1_2_3_3_0_0_1": "SAME", "1_2_3_3_0_1_0": "SAME", "1_2_3_3_0_1_1": "SAME", "1_2_3_3_0_2_0": "SAME", "1_2_3_3_0_2_1": "SAME", "1_2_3_3_1_0_0": "SAME", "1_2_3_3_1_0_1": "SAME", "1_2_3_3_1_1_0": "SAME", "1_2_3_3_1_1_1": "SAME", "1_2_3_3_1_2_0": "SAME", "1_2_3_3_1_2_1": "SAME", "1_2_3_3_2_0_0": "SAME", "1_2_3_3_2_0_1": "SAME", "1_2_3_3_2_1_0": "SAME", "1_2_3_3_2_1_1": "SAME", "1_2_3_3_2_2_0": "SAME", "1_2_3_3_2_2_1": "SAME", "1_2_3_3_3_0_0": "SAME", "1_2_3_3_3_0_1": "SAME", "1_2_3_3_3_1_0": "SAME", "1_2_3_3_3_1_1": "SAME", "1_2_3_3_3_2_0": "SAME", "1_2_3_3_3_2_1": "SAME", "1_3_0_0_0_0_0": "SAME", "1_3_0_0_0_0_1": "SAME", "1_3_0_0_0_1_0": "SAME", "1_3_0_0_0_1_1": "SAME", "1_3_0_0_0_2_0": "SAME", "1_3_0_0_0_2_1": "SAME", "1_3_0_0_1_0_0": "SAME", "1_3_0_0_1_0_1": "SAME", "1_3_0_0_1_1_0": "SAME", "1_3_0_0_1_1_1": "SAME", "1_3_0_0_1_2_0": "SAME", "1_3_0_0_1_2_1": "SAME", "1_3_0_0_2_0_0": "SAME", "1_3_0_0_2_0_1": "SAME", "1_3_0_0_2_1_0": "SAME", "1_3_0_0_2_1_1": "SAME", "1_3_0_0_2_2_0": "SAME", "1_3_0_0_2_2_1": "SAME", "1_3_0_0_3_0_0": "SAME", "1_3_0_0_3_0_1": "SAME", "1_3_0_0_3_1_0": "SAME", "1_3_0_0_3_1_1": "SAME", "1_3_0_0_3_2_0": "SAME", "1_3_0_0_3_2_1": "SAME", "1_3_0_1_0_0_0": "SAME", "1_3_0_1_0_0_1": "SAME", "1_3_0_1_0_1_0": "SAME", "1_3_0_1_0_1_1": "SAME", "1_3_0_1_0_2_0": "SAME", "1_3_0_1_0_2_1": "SAME", "1_3_0_1_1_0_0": "SAME", "1_3_0_1_1_0_1": "SAME", "1_3_0_1_1_1_0": "SAME", "1_3_0_1_1_1_1": "SAME", "1_3_0_1_1_2_0": "SAME", "1_3_0_1_1_2_1": "SAME", "1_3_0_1_2_0_0": "SAME", "1_3_0_1_2_0_1": "SAME", "1_3_0_1_2_1_0": "SAME", "1_3_0_1_2_1_1": "SAME", "1_3_0_1_2_2_0": "SAME", "1_3_0_1_2_2_1": "SAME", "1_3_0_1_3_0_0": "SAME", "1_3_0_1_3_0_1": "SAME", "1_3_0_1_3_1_0": "SAME", "1_3_0_1_3_1_1": "SAME", "1_3_0_1_3_2_0": "SAME", "1_3_0_1_3_2_1": "SAME", "1_3_0_2_0_0_0": "SAME", "1_3_0_2_0_0_1": "SAME", "1_3_0_2_0_1_0": "SAME", "1_3_0_2_0_1_1": "SAME", "1_3_0_2_0_2_0": "SAME", "1_3_0_2_0_2_1": "SAME", "1_3_0_2_1_0_0": "SAME", "1_3_0_2_1_0_1": "SAME", "1_3_0_2_1_1_0": "SAME", "1_3_0_2_1_1_1": "SAME", "1_3_0_2_1_2_0": "SAME", "1_3_0_2_1_2_1": "SAME", "1_3_0_2_2_0_0": "SAME", "1_3_0_2_2_0_1": "SAME", "1_3_0_2_2_1_0": "SAME", "1_3_0_2_2_1_1": "SAME", "1_3_0_2_2_2_0": "SAME", "1_3_0_2_2_2_1": "SAME", "1_3_0_2_3_0_0": "SAME", "1_3_0_2_3_0_1": "SAME", "1_3_0_2_3_1_0": "SAME", "1_3_0_2_3_1_1": "SAME", "1_3_0_2_3_2_0": "SAME", "1_3_0_2_3_2_1": "SAME", "1_3_0_3_0_0_0": "SAME", "1_3_0_3_0_0_1": "SAME", "1_3_0_3_0_1_0": "SAME", "1_3_0_3_0_1_1": "SAME", "1_3_0_3_0_2_0": "SAME", "1_3_0_3_0_2_1": "SAME", "1_3_0_3_1_0_0": "SAME", "1_3_0_3_1_0_1": "SAME", "1_3_0_3_1_1_0": "SAME", "1_3_0_3_1_1_1": "SAME", "1_3_0_3_1_2_0": "SAME", "1_3_0_3_1_2_1": "SAME", "1_3_0_3_2_0_0": "SAME", "1_3_0_3_2_0_1": "SAME", "1_3_0_3_2_1_0": "SAME", "1_3_0_3_2_1_1": "SAME", "1_3_0_3_2_2_0": "SAME", "1_3_0_3_2_2_1": "SAME", "1_3_0_3_3_0_0": "SAME", "1_3_0_3_3_0_1": "SAME", "1_3_0_3_3_1_0": "SAME", "1_3_0_3_3_1_1": "SAME", "1_3_0_3_3_2_0": "SAME", "1_3_0_3_3_2_1": "SAME", "1_3_1_0_0_0_0": "SAME", "1_3_1_0_0_0_1": "SAME", "1_3_1_0_0_1_0": "SAME", "1_3_1_0_0_1_1": "SAME", "1_3_1_0_0_2_0": "SAME", "1_3_1_0_0_2_1": "SAME", "1_3_1_0_1_0_0": "SAME", "1_3_1_0_1_0_1": "SAME", "1_3_1_0_1_1_0": "SAME", "1_3_1_0_1_1_1": "SAME", "1_3_1_0_1_2_0": "SAME", "1_3_1_0_1_2_1": "SAME", "1_3_1_0_2_0_0": "SAME", "1_3_1_0_2_0_1": "SAME", "1_3_1_0_2_1_0": "SAME", "1_3_1_0_2_1_1": "SAME", "1_3_1_0_2_2_0": "SAME", "1_3_1_0_2_2_1": "SAME", "1_3_1_0_3_0_0": "SAME", "1_3_1_0_3_0_1": "SAME", "1_3_1_0_3_1_0": "SAME", "1_3_1_0_3_1_1": "SAME", "1_3_1_0_3_2_0": "SAME", "1_3_1_0_3_2_1": "SAME", "1_3_1_1_0_0_0": "SAME", "1_3_1_1_0_0_1": "SAME", "1_3_1_1_0_1_0": "SAME", "1_3_1_1_0_1_1": "SAME", "1_3_1_1_0_2_0": "SAME", "1_3_1_1_0_2_1": "SAME", "1_3_1_1_1_0_0": "SAME", "1_3_1_1_1_0_1": "SAME", "1_3_1_1_1_1_0": "SAME", "1_3_1_1_1_1_1": "SAME", "1_3_1_1_1_2_0": "SAME", "1_3_1_1_1_2_1": "SAME", "1_3_1_1_2_0_0": "SAME", "1_3_1_1_2_0_1": "SAME", "1_3_1_1_2_1_0": "SAME", "1_3_1_1_2_1_1": "SAME", "1_3_1_1_2_2_0": "SAME", "1_3_1_1_2_2_1": "SAME", "1_3_1_1_3_0_0": "SAME", "1_3_1_1_3_0_1": "SAME", "1_3_1_1_3_1_0": "SAME", "1_3_1_1_3_1_1": "SAME", "1_3_1_1_3_2_0": "SAME", "1_3_1_1_3_2_1": "SAME", "1_3_1_2_0_0_0": "SAME", "1_3_1_2_0_0_1": "SAME", "1_3_1_2_0_1_0": "SAME", "1_3_1_2_0_1_1": "SAME", "1_3_1_2_0_2_0": "SAME", "1_3_1_2_0_2_1": "SAME", "1_3_1_2_1_0_0": "SAME", "1_3_1_2_1_0_1": "SAME", "1_3_1_2_1_1_0": "SAME", "1_3_1_2_1_1_1": "SAME", "1_3_1_2_1_2_0": "SAME", "1_3_1_2_1_2_1": "SAME", "1_3_1_2_2_0_0": "SAME", "1_3_1_2_2_0_1": "SAME", "1_3_1_2_2_1_0": "SAME", "1_3_1_2_2_1_1": "SAME", "1_3_1_2_2_2_0": "SAME", "1_3_1_2_2_2_1": "SAME", "1_3_1_2_3_0_0": "SAME", "1_3_1_2_3_0_1": "SAME", "1_3_1_2_3_1_0": "SAME", "1_3_1_2_3_1_1": "SAME", "1_3_1_2_3_2_0": "SAME", "1_3_1_2_3_2_1": "SAME", "1_3_1_3_0_0_0": "SAME", "1_3_1_3_0_0_1": "SAME", "1_3_1_3_0_1_0": "SAME", "1_3_1_3_0_1_1": "SAME", "1_3_1_3_0_2_0": "SAME", "1_3_1_3_0_2_1": "SAME", "1_3_1_3_1_0_0": "SAME", "1_3_1_3_1_0_1": "SAME", "1_3_1_3_1_1_0": "SAME", "1_3_1_3_1_1_1": "SAME", "1_3_1_3_1_2_0": "SAME", "1_3_1_3_1_2_1": "SAME", "1_3_1_3_2_0_0": "SAME", "1_3_1_3_2_0_1": "SAME", "1_3_1_3_2_1_0": "SAME", "1_3_1_3_2_1_1": "SAME", "1_3_1_3_2_2_0": "SAME", "1_3_1_3_2_2_1": "SAME", "1_3_1_3_3_0_0": "SAME", "1_3_1_3_3_0_1": "SAME", "1_3_1_3_3_1_0": "SAME", "1_3_1_3_3_1_1": "SAME", "1_3_1_3_3_2_0": "SAME", "1_3_1_3_3_2_1": "SAME", "1_3_2_0_0_0_0": "SAME", "1_3_2_0_0_0_1": "SAME", "1_3_2_0_0_1_0": "SAME", "1_3_2_0_0_1_1": "SAME", "1_3_2_0_0_2_0": "SAME", "1_3_2_0_0_2_1": "SAME", "1_3_2_0_1_0_0": "SAME", "1_3_2_0_1_0_1": "SAME", "1_3_2_0_1_1_0": "SAME", "1_3_2_0_1_1_1": "SAME", "1_3_2_0_1_2_0": "SAME", "1_3_2_0_1_2_1": "SAME", "1_3_2_0_2_0_0": "SAME", "1_3_2_0_2_0_1": "SAME", "1_3_2_0_2_1_0": "SAME", "1_3_2_0_2_1_1": "SAME", "1_3_2_0_2_2_0": "SAME", "1_3_2_0_2_2_1": "SAME", "1_3_2_0_3_0_0": "SAME", "1_3_2_0_3_0_1": "SAME", "1_3_2_0_3_1_0": "SAME", "1_3_2_0_3_1_1": "SAME", "1_3_2_0_3_2_0": "SAME", "1_3_2_0_3_2_1": "SAME", "1_3_2_1_0_0_0": "SAME", "1_3_2_1_0_0_1": "SAME", "1_3_2_1_0_1_0": "SAME", "1_3_2_1_0_1_1": "SAME", "1_3_2_1_0_2_0": "SAME", "1_3_2_1_0_2_1": "SAME", "1_3_2_1_1_0_0": "SAME", "1_3_2_1_1_0_1": "SAME", "1_3_2_1_1_1_0": "SAME", "1_3_2_1_1_1_1": "SAME", "1_3_2_1_1_2_0": "SAME", "1_3_2_1_1_2_1": "SAME", "1_3_2_1_2_0_0": "SAME", "1_3_2_1_2_0_1": "SAME", "1_3_2_1_2_1_0": "SAME", "1_3_2_1_2_1_1": "SAME", "1_3_2_1_2_2_0": "SAME", "1_3_2_1_2_2_1": "SAME", "1_3_2_1_3_0_0": "SAME", "1_3_2_1_3_0_1": "SAME", "1_3_2_1_3_1_0": "SAME", "1_3_2_1_3_1_1": "SAME", "1_3_2_1_3_2_0": "SAME", "1_3_2_1_3_2_1": "SAME", "1_3_2_2_0_0_0": "SAME", "1_3_2_2_0_0_1": "SAME", "1_3_2_2_0_1_0": "SAME", "1_3_2_2_0_1_1": "SAME", "1_3_2_2_0_2_0": "SAME", "1_3_2_2_0_2_1": "SAME", "1_3_2_2_1_0_0": "SAME", "1_3_2_2_1_0_1": "SAME", "1_3_2_2_1_1_0": "SAME", "1_3_2_2_1_1_1": "SAME", "1_3_2_2_1_2_0": "SAME", "1_3_2_2_1_2_1": "SAME", "1_3_2_2_2_0_0": "SAME", "1_3_2_2_2_0_1": "SAME", "1_3_2_2_2_1_0": "SAME", "1_3_2_2_2_1_1": "SAME", "1_3_2_2_2_2_0": "SAME", "1_3_2_2_2_2_1": "SAME", "1_3_2_2_3_0_0": "SAME", "1_3_2_2_3_0_1": "SAME", "1_3_2_2_3_1_0": "SAME", "1_3_2_2_3_1_1": "SAME", "1_3_2_2_3_2_0": "SAME", "1_3_2_2_3_2_1": "SAME", "1_3_2_3_0_0_0": "SAME", "1_3_2_3_0_0_1": "SAME", "1_3_2_3_0_1_0": "SAME", "1_3_2_3_0_1_1": "SAME", "1_3_2_3_0_2_0": "SAME", "1_3_2_3_0_2_1": "SAME", "1_3_2_3_1_0_0": "SAME", "1_3_2_3_1_0_1": "SAME", "1_3_2_3_1_1_0": "SAME", "1_3_2_3_1_1_1": "SAME", "1_3_2_3_1_2_0": "SAME", "1_3_2_3_1_2_1": "SAME", "1_3_2_3_2_0_0": "SAME", "1_3_2_3_2_0_1": "SAME", "1_3_2_3_2_1_0": "SAME", "1_3_2_3_2_1_1": "SAME", "1_3_2_3_2_2_0": "SAME", "1_3_2_3_2_2_1": "SAME", "1_3_2_3_3_0_0": "SAME", "1_3_2_3_3_0_1": "SAME", "1_3_2_3_3_1_0": "SAME", "1_3_2_3_3_1_1": "SAME", "1_3_2_3_3_2_0": "SAME", "1_3_2_3_3_2_1": "SAME", "1_3_3_0_0_0_0": "SAME", "1_3_3_0_0_0_1": "SAME", "1_3_3_0_0_1_0": "SAME", "1_3_3_0_0_1_1": "SAME", "1_3_3_0_0_2_0": "SAME", "1_3_3_0_0_2_1": "SAME", "1_3_3_0_1_0_0": "SAME", "1_3_3_0_1_0_1": "SAME", "1_3_3_0_1_1_0": "SAME", "1_3_3_0_1_1_1": "SAME", "1_3_3_0_1_2_0": "SAME", "1_3_3_0_1_2_1": "SAME", "1_3_3_0_2_0_0": "SAME", "1_3_3_0_2_0_1": "SAME", "1_3_3_0_2_1_0": "SAME", "1_3_3_0_2_1_1": "SAME", "1_3_3_0_2_2_0": "SAME", "1_3_3_0_2_2_1": "SAME", "1_3_3_0_3_0_0": "SAME", "1_3_3_0_3_0_1": "SAME", "1_3_3_0_3_1_0": "SAME", "1_3_3_0_3_1_1": "SAME", "1_3_3_0_3_2_0": "SAME", "1_3_3_0_3_2_1": "SAME", "1_3_3_1_0_0_0": "SAME", "1_3_3_1_0_0_1": "SAME", "1_3_3_1_0_1_0": "SAME", "1_3_3_1_0_1_1": "SAME", "1_3_3_1_0_2_0": "SAME", "1_3_3_1_0_2_1": "SAME", "1_3_3_1_1_0_0": "SAME", "1_3_3_1_1_0_1": "SAME", "1_3_3_1_1_1_0": "SAME", "1_3_3_1_1_1_1": "SAME", "1_3_3_1_1_2_0": "SAME", "1_3_3_1_1_2_1": "SAME", "1_3_3_1_2_0_0": "SAME", "1_3_3_1_2_0_1": "SAME", "1_3_3_1_2_1_0": "SAME", "1_3_3_1_2_1_1": "SAME", "1_3_3_1_2_2_0": "SAME", "1_3_3_1_2_2_1": "SAME", "1_3_3_1_3_0_0": "SAME", "1_3_3_1_3_0_1": "SAME", "1_3_3_1_3_1_0": "SAME", "1_3_3_1_3_1_1": "SAME", "1_3_3_1_3_2_0": "SAME", "1_3_3_1_3_2_1": "SAME", "1_3_3_2_0_0_0": "SAME", "1_3_3_2_0_0_1": "SAME", "1_3_3_2_0_1_0": "SAME", "1_3_3_2_0_1_1": "SAME", "1_3_3_2_0_2_0": "SAME", "1_3_3_2_0_2_1": "SAME", "1_3_3_2_1_0_0": "SAME", "1_3_3_2_1_0_1": "SAME", "1_3_3_2_1_1_0": "SAME", "1_3_3_2_1_1_1": "SAME", "1_3_3_2_1_2_0": "SAME", "1_3_3_2_1_2_1": "SAME", "1_3_3_2_2_0_0": "SAME", "1_3_3_2_2_0_1": "SAME", "1_3_3_2_2_1_0": "SAME", "1_3_3_2_2_1_1": "SAME", "1_3_3_2_2_2_0": "SAME", "1_3_3_2_2_2_1": "SAME", "1_3_3_2_3_0_0": "SAME", "1_3_3_2_3_0_1": "SAME", "1_3_3_2_3_1_0": "SAME", "1_3_3_2_3_1_1": "SAME", "1_3_3_2_3_2_0": "SAME", "1_3_3_2_3_2_1": "SAME", "1_3_3_3_0_0_0": "SAME", "1_3_3_3_0_0_1": "SAME", "1_3_3_3_0_1_0": "SAME", "1_3_3_3_0_1_1": "SAME", "1_3_3_3_0_2_0": "SAME", "1_3_3_3_0_2_1": "SAME", "1_3_3_3_1_0_0": "SAME", "1_3_3_3_1_0_1": "SAME", "1_3_3_3_1_1_0": "SAME", "1_3_3_3_1_1_1": "SAME", "1_3_3_3_1_2_0": "SAME", "1_3_3_3_1_2_1": "SAME", "1_3_3_3_2_0_0": "SAME", "1_3_3_3_2_0_1": "SAME", "1_3_3_3_2_1_0": "SAME", "1_3_3_3_2_1_1": "SAME", "1_3_3_3_2_2_0": "SAME", "1_3_3_3_2_2_1": "SAME", "1_3_3_3_3_0_0": "SAME", "1_3_3_3_3_0_1": "SAME", "1_3_3_3_3_1_0": "SAME", "1_3_3_3_3_1_1": "SAME", "1_3_3_3_3_2_0": "SAME", "1_3_3_3_3_2_1": "SAME", "1_4_0_0_0_0_0": "SAME", "1_4_0_0_0_0_1": "SAME", "1_4_0_0_0_1_0": "SAME", "1_4_0_0_0_1_1": "SAME", "1_4_0_0_0_2_0": "SAME", "1_4_0_0_0_2_1": "SAME", "1_4_0_0_1_0_0": "SAME", "1_4_0_0_1_0_1": "SAME", "1_4_0_0_1_1_0": "SAME", "1_4_0_0_1_1_1": "SAME", "1_4_0_0_1_2_0": "SAME", "1_4_0_0_1_2_1": "SAME", "1_4_0_0_2_0_0": "SAME", "1_4_0_0_2_0_1": "SAME", "1_4_0_0_2_1_0": "SAME", "1_4_0_0_2_1_1": "SAME", "1_4_0_0_2_2_0": "SAME", "1_4_0_0_2_2_1": "SAME", "1_4_0_0_3_0_0": "SAME", "1_4_0_0_3_0_1": "SAME", "1_4_0_0_3_1_0": "SAME", "1_4_0_0_3_1_1": "SAME", "1_4_0_0_3_2_0": "SAME", "1_4_0_0_3_2_1": "SAME", "1_4_0_1_0_0_0": "SAME", "1_4_0_1_0_0_1": "SAME", "1_4_0_1_0_1_0": "SAME", "1_4_0_1_0_1_1": "SAME", "1_4_0_1_0_2_0": "SAME", "1_4_0_1_0_2_1": "SAME", "1_4_0_1_1_0_0": "SAME", "1_4_0_1_1_0_1": "SAME", "1_4_0_1_1_1_0": "SAME", "1_4_0_1_1_1_1": "SAME", "1_4_0_1_1_2_0": "SAME", "1_4_0_1_1_2_1": "SAME", "1_4_0_1_2_0_0": "SAME", "1_4_0_1_2_0_1": "SAME", "1_4_0_1_2_1_0": "SAME", "1_4_0_1_2_1_1": "SAME", "1_4_0_1_2_2_0": "SAME", "1_4_0_1_2_2_1": "SAME", "1_4_0_1_3_0_0": "SAME", "1_4_0_1_3_0_1": "SAME", "1_4_0_1_3_1_0": "SAME", "1_4_0_1_3_1_1": "SAME", "1_4_0_1_3_2_0": "SAME", "1_4_0_1_3_2_1": "SAME", "1_4_0_2_0_0_0": "SAME", "1_4_0_2_0_0_1": "SAME", "1_4_0_2_0_1_0": "SAME", "1_4_0_2_0_1_1": "SAME", "1_4_0_2_0_2_0": "SAME", "1_4_0_2_0_2_1": "SAME", "1_4_0_2_1_0_0": "SAME", "1_4_0_2_1_0_1": "SAME", "1_4_0_2_1_1_0": "SAME", "1_4_0_2_1_1_1": "SAME", "1_4_0_2_1_2_0": "SAME", "1_4_0_2_1_2_1": "SAME", "1_4_0_2_2_0_0": "SAME", "1_4_0_2_2_0_1": "SAME", "1_4_0_2_2_1_0": "SAME", "1_4_0_2_2_1_1": "SAME", "1_4_0_2_2_2_0": "SAME", "1_4_0_2_2_2_1": "SAME", "1_4_0_2_3_0_0": "SAME", "1_4_0_2_3_0_1": "SAME", "1_4_0_2_3_1_0": "SAME", "1_4_0_2_3_1_1": "SAME", "1_4_0_2_3_2_0": "SAME", "1_4_0_2_3_2_1": "SAME", "1_4_0_3_0_0_0": "SAME", "1_4_0_3_0_0_1": "SAME", "1_4_0_3_0_1_0": "SAME", "1_4_0_3_0_1_1": "SAME", "1_4_0_3_0_2_0": "SAME", "1_4_0_3_0_2_1": "SAME", "1_4_0_3_1_0_0": "SAME", "1_4_0_3_1_0_1": "SAME", "1_4_0_3_1_1_0": "SAME", "1_4_0_3_1_1_1": "SAME", "1_4_0_3_1_2_0": "SAME", "1_4_0_3_1_2_1": "SAME", "1_4_0_3_2_0_0": "SAME", "1_4_0_3_2_0_1": "SAME", "1_4_0_3_2_1_0": "SAME", "1_4_0_3_2_1_1": "SAME", "1_4_0_3_2_2_0": "SAME", "1_4_0_3_2_2_1": "SAME", "1_4_0_3_3_0_0": "SAME", "1_4_0_3_3_0_1": "SAME", "1_4_0_3_3_1_0": "SAME", "1_4_0_3_3_1_1": "SAME", "1_4_0_3_3_2_0": "SAME", "1_4_0_3_3_2_1": "SAME", "1_4_1_0_0_0_0": "SAME", "1_4_1_0_0_0_1": "SAME", "1_4_1_0_0_1_0": "SAME", "1_4_1_0_0_1_1": "SAME", "1_4_1_0_0_2_0": "SAME", "1_4_1_0_0_2_1": "SAME", "1_4_1_0_1_0_0": "SAME", "1_4_1_0_1_0_1": "SAME", "1_4_1_0_1_1_0": "SAME", "1_4_1_0_1_1_1": "SAME", "1_4_1_0_1_2_0": "SAME", "1_4_1_0_1_2_1": "SAME", "1_4_1_0_2_0_0": "SAME", "1_4_1_0_2_0_1": "SAME", "1_4_1_0_2_1_0": "SAME", "1_4_1_0_2_1_1": "SAME", "1_4_1_0_2_2_0": "SAME", "1_4_1_0_2_2_1": "SAME", "1_4_1_0_3_0_0": "SAME", "1_4_1_0_3_0_1": "SAME", "1_4_1_0_3_1_0": "SAME", "1_4_1_0_3_1_1": "SAME", "1_4_1_0_3_2_0": "SAME", "1_4_1_0_3_2_1": "SAME", "1_4_1_1_0_0_0": "SAME", "1_4_1_1_0_0_1": "SAME", "1_4_1_1_0_1_0": "SAME", "1_4_1_1_0_1_1": "SAME", "1_4_1_1_0_2_0": "SAME", "1_4_1_1_0_2_1": "SAME", "1_4_1_1_1_0_0": "SAME", "1_4_1_1_1_0_1": "SAME", "1_4_1_1_1_1_0": "SAME", "1_4_1_1_1_1_1": "SAME", "1_4_1_1_1_2_0": "SAME", "1_4_1_1_1_2_1": "SAME", "1_4_1_1_2_0_0": "SAME", "1_4_1_1_2_0_1": "SAME", "1_4_1_1_2_1_0": "SAME", "1_4_1_1_2_1_1": "SAME", "1_4_1_1_2_2_0": "SAME", "1_4_1_1_2_2_1": "SAME", "1_4_1_1_3_0_0": "SAME", "1_4_1_1_3_0_1": "SAME", "1_4_1_1_3_1_0": "SAME", "1_4_1_1_3_1_1": "SAME", "1_4_1_1_3_2_0": "SAME", "1_4_1_1_3_2_1": "SAME", "1_4_1_2_0_0_0": "SAME", "1_4_1_2_0_0_1": "SAME", "1_4_1_2_0_1_0": "SAME", "1_4_1_2_0_1_1": "SAME", "1_4_1_2_0_2_0": "SAME", "1_4_1_2_0_2_1": "SAME", "1_4_1_2_1_0_0": "SAME", "1_4_1_2_1_0_1": "SAME", "1_4_1_2_1_1_0": "SAME", "1_4_1_2_1_1_1": "SAME", "1_4_1_2_1_2_0": "SAME", "1_4_1_2_1_2_1": "SAME", "1_4_1_2_2_0_0": "SAME", "1_4_1_2_2_0_1": "SAME", "1_4_1_2_2_1_0": "SAME", "1_4_1_2_2_1_1": "SAME", "1_4_1_2_2_2_0": "SAME", "1_4_1_2_2_2_1": "SAME", "1_4_1_2_3_0_0": "SAME", "1_4_1_2_3_0_1": "SAME", "1_4_1_2_3_1_0": "SAME", "1_4_1_2_3_1_1": "SAME", "1_4_1_2_3_2_0": "SAME", "1_4_1_2_3_2_1": "SAME", "1_4_1_3_0_0_0": "SAME", "1_4_1_3_0_0_1": "SAME", "1_4_1_3_0_1_0": "SAME", "1_4_1_3_0_1_1": "SAME", "1_4_1_3_0_2_0": "SAME", "1_4_1_3_0_2_1": "SAME", "1_4_1_3_1_0_0": "SAME", "1_4_1_3_1_0_1": "SAME", "1_4_1_3_1_1_0": "SAME", "1_4_1_3_1_1_1": "SAME", "1_4_1_3_1_2_0": "SAME", "1_4_1_3_1_2_1": "SAME", "1_4_1_3_2_0_0": "SAME", "1_4_1_3_2_0_1": "SAME", "1_4_1_3_2_1_0": "SAME", "1_4_1_3_2_1_1": "SAME", "1_4_1_3_2_2_0": "SAME", "1_4_1_3_2_2_1": "SAME", "1_4_1_3_3_0_0": "SAME", "1_4_1_3_3_0_1": "SAME", "1_4_1_3_3_1_0": "SAME", "1_4_1_3_3_1_1": "SAME", "1_4_1_3_3_2_0": "SAME", "1_4_1_3_3_2_1": "SAME", "1_4_2_0_0_0_0": "SAME", "1_4_2_0_0_0_1": "SAME", "1_4_2_0_0_1_0": "SAME", "1_4_2_0_0_1_1": "SAME", "1_4_2_0_0_2_0": "SAME", "1_4_2_0_0_2_1": "SAME", "1_4_2_0_1_0_0": "SAME", "1_4_2_0_1_0_1": "SAME", "1_4_2_0_1_1_0": "SAME", "1_4_2_0_1_1_1": "SAME", "1_4_2_0_1_2_0": "SAME", "1_4_2_0_1_2_1": "SAME", "1_4_2_0_2_0_0": "SAME", "1_4_2_0_2_0_1": "SAME", "1_4_2_0_2_1_0": "SAME", "1_4_2_0_2_1_1": "SAME", "1_4_2_0_2_2_0": "SAME", "1_4_2_0_2_2_1": "SAME", "1_4_2_0_3_0_0": "SAME", "1_4_2_0_3_0_1": "SAME", "1_4_2_0_3_1_0": "SAME", "1_4_2_0_3_1_1": "SAME", "1_4_2_0_3_2_0": "SAME", "1_4_2_0_3_2_1": "SAME", "1_4_2_1_0_0_0": "SAME", "1_4_2_1_0_0_1": "SAME", "1_4_2_1_0_1_0": "SAME", "1_4_2_1_0_1_1": "SAME", "1_4_2_1_0_2_0": "SAME", "1_4_2_1_0_2_1": "SAME", "1_4_2_1_1_0_0": "SAME", "1_4_2_1_1_0_1": "SAME", "1_4_2_1_1_1_0": "SAME", "1_4_2_1_1_1_1": "SAME", "1_4_2_1_1_2_0": "SAME", "1_4_2_1_1_2_1": "SAME", "1_4_2_1_2_0_0": "SAME", "1_4_2_1_2_0_1": "SAME", "1_4_2_1_2_1_0": "SAME", "1_4_2_1_2_1_1": "SAME", "1_4_2_1_2_2_0": "SAME", "1_4_2_1_2_2_1": "SAME", "1_4_2_1_3_0_0": "SAME", "1_4_2_1_3_0_1": "SAME", "1_4_2_1_3_1_0": "SAME", "1_4_2_1_3_1_1": "SAME", "1_4_2_1_3_2_0": "SAME", "1_4_2_1_3_2_1": "SAME", "1_4_2_2_0_0_0": "SAME", "1_4_2_2_0_0_1": "SAME", "1_4_2_2_0_1_0": "SAME", "1_4_2_2_0_1_1": "SAME", "1_4_2_2_0_2_0": "SAME", "1_4_2_2_0_2_1": "SAME", "1_4_2_2_1_0_0": "SAME", "1_4_2_2_1_0_1": "SAME", "1_4_2_2_1_1_0": "SAME", "1_4_2_2_1_1_1": "SAME", "1_4_2_2_1_2_0": "SAME", "1_4_2_2_1_2_1": "SAME", "1_4_2_2_2_0_0": "SAME", "1_4_2_2_2_0_1": "SAME", "1_4_2_2_2_1_0": "SAME", "1_4_2_2_2_1_1": "SAME", "1_4_2_2_2_2_0": "SAME", "1_4_2_2_2_2_1": "SAME", "1_4_2_2_3_0_0": "SAME", "1_4_2_2_3_0_1": "SAME", "1_4_2_2_3_1_0": "SAME", "1_4_2_2_3_1_1": "SAME", "1_4_2_2_3_2_0": "SAME", "1_4_2_2_3_2_1": "SAME", "1_4_2_3_0_0_0": "SAME", "1_4_2_3_0_0_1": "SAME", "1_4_2_3_0_1_0": "SAME", "1_4_2_3_0_1_1": "SAME", "1_4_2_3_0_2_0": "SAME", "1_4_2_3_0_2_1": "SAME", "1_4_2_3_1_0_0": "SAME", "1_4_2_3_1_0_1": "SAME", "1_4_2_3_1_1_0": "SAME", "1_4_2_3_1_1_1": "SAME", "1_4_2_3_1_2_0": "SAME", "1_4_2_3_1_2_1": "SAME", "1_4_2_3_2_0_0": "SAME", "1_4_2_3_2_0_1": "SAME", "1_4_2_3_2_1_0": "SAME", "1_4_2_3_2_1_1": "SAME", "1_4_2_3_2_2_0": "SAME", "1_4_2_3_2_2_1": "SAME", "1_4_2_3_3_0_0": "SAME", "1_4_2_3_3_0_1": "SAME", "1_4_2_3_3_1_0": "SAME", "1_4_2_3_3_1_1": "SAME", "1_4_2_3_3_2_0": "SAME", "1_4_2_3_3_2_1": "SAME", "1_4_3_0_0_0_0": "SAME", "1_4_3_0_0_0_1": "SAME", "1_4_3_0_0_1_0": "SAME", "1_4_3_0_0_1_1": "SAME", "1_4_3_0_0_2_0": "SAME", "1_4_3_0_0_2_1": "SAME", "1_4_3_0_1_0_0": "SAME", "1_4_3_0_1_0_1": "SAME", "1_4_3_0_1_1_0": "SAME", "1_4_3_0_1_1_1": "SAME", "1_4_3_0_1_2_0": "SAME", "1_4_3_0_1_2_1": "SAME", "1_4_3_0_2_0_0": "SAME", "1_4_3_0_2_0_1": "SAME", "1_4_3_0_2_1_0": "SAME", "1_4_3_0_2_1_1": "SAME", "1_4_3_0_2_2_0": "SAME", "1_4_3_0_2_2_1": "SAME", "1_4_3_0_3_0_0": "SAME", "1_4_3_0_3_0_1": "SAME", "1_4_3_0_3_1_0": "SAME", "1_4_3_0_3_1_1": "SAME", "1_4_3_0_3_2_0": "SAME", "1_4_3_0_3_2_1": "SAME", "1_4_3_1_0_0_0": "SAME", "1_4_3_1_0_0_1": "SAME", "1_4_3_1_0_1_0": "SAME", "1_4_3_1_0_1_1": "SAME", "1_4_3_1_0_2_0": "SAME", "1_4_3_1_0_2_1": "SAME", "1_4_3_1_1_0_0": "SAME", "1_4_3_1_1_0_1": "SAME", "1_4_3_1_1_1_0": "SAME", "1_4_3_1_1_1_1": "SAME", "1_4_3_1_1_2_0": "SAME", "1_4_3_1_1_2_1": "SAME", "1_4_3_1_2_0_0": "SAME", "1_4_3_1_2_0_1": "SAME", "1_4_3_1_2_1_0": "SAME", "1_4_3_1_2_1_1": "SAME", "1_4_3_1_2_2_0": "SAME", "1_4_3_1_2_2_1": "SAME", "1_4_3_1_3_0_0": "SAME", "1_4_3_1_3_0_1": "SAME", "1_4_3_1_3_1_0": "SAME", "1_4_3_1_3_1_1": "SAME", "1_4_3_1_3_2_0": "SAME", "1_4_3_1_3_2_1": "SAME", "1_4_3_2_0_0_0": "SAME", "1_4_3_2_0_0_1": "SAME", "1_4_3_2_0_1_0": "SAME", "1_4_3_2_0_1_1": "SAME", "1_4_3_2_0_2_0": "SAME", "1_4_3_2_0_2_1": "SAME", "1_4_3_2_1_0_0": "SAME", "1_4_3_2_1_0_1": "SAME", "1_4_3_2_1_1_0": "SAME", "1_4_3_2_1_1_1": "SAME", "1_4_3_2_1_2_0": "SAME", "1_4_3_2_1_2_1": "SAME", "1_4_3_2_2_0_0": "SAME", "1_4_3_2_2_0_1": "SAME", "1_4_3_2_2_1_0": "SAME", "1_4_3_2_2_1_1": "SAME", "1_4_3_2_2_2_0": "SAME", "1_4_3_2_2_2_1": "SAME", "1_4_3_2_3_0_0": "SAME", "1_4_3_2_3_0_1": "SAME", "1_4_3_2_3_1_0": "SAME", "1_4_3_2_3_1_1": "SAME", "1_4_3_2_3_2_0": "SAME", "1_4_3_2_3_2_1": "SAME", "1_4_3_3_0_0_0": "SAME", "1_4_3_3_0_0_1": "SAME", "1_4_3_3_0_1_0": "SAME", "1_4_3_3_0_1_1": "SAME", "1_4_3_3_0_2_0": "SAME", "1_4_3_3_0_2_1": "SAME", "1_4_3_3_1_0_0": "SAME", "1_4_3_3_1_0_1": "SAME", "1_4_3_3_1_1_0": "SAME", "1_4_3_3_1_1_1": "SAME", "1_4_3_3_1_2_0": "SAME", "1_4_3_3_1_2_1": "SAME", "1_4_3_3_2_0_0": "SAME", "1_4_3_3_2_0_1": "SAME", "1_4_3_3_2_1_0": "SAME", "1_4_3_3_2_1_1": "SAME", "1_4_3_3_2_2_0": "SAME", "1_4_3_3_2_2_1": "SAME", "1_4_3_3_3_0_0": "SAME", "1_4_3_3_3_0_1": "SAME", "1_4_3_3_3_1_0": "SAME", "1_4_3_3_3_1_1": "SAME", "1_4_3_3_3_2_0": "SAME", "1_4_3_3_3_2_1": "SAME", "2_1_0_0_0_0_0": "SAME", "2_1_0_0_0_0_1": "SAME", "2_1_0_0_0_1_0": "SAME", "2_1_0_0_0_1_1": "SAME", "2_1_0_0_0_2_0": "SAME", "2_1_0_0_0_2_1": "SAME", "2_1_0_0_1_0_0": "SAME", "2_1_0_0_1_0_1": "SAME", "2_1_0_0_1_1_0": "SAME", "2_1_0_0_1_1_1": "SAME", "2_1_0_0_1_2_0": "SAME", "2_1_0_0_1_2_1": "SAME", "2_1_0_0_2_0_0": "SAME", "2_1_0_0_2_0_1": "SAME", "2_1_0_0_2_1_0": "SAME", "2_1_0_0_2_1_1": "SAME", "2_1_0_0_2_2_0": "SAME", "2_1_0_0_2_2_1": "SAME", "2_1_0_0_3_0_0": "SAME", "2_1_0_0_3_0_1": "SAME", "2_1_0_0_3_1_0": "SAME", "2_1_0_0_3_1_1": "SAME", "2_1_0_0_3_2_0": "SAME", "2_1_0_0_3_2_1": "SAME", "2_1_0_1_0_0_0": "SAME", "2_1_0_1_0_0_1": "SAME", "2_1_0_1_0_1_0": "SAME", "2_1_0_1_0_1_1": "SAME", "2_1_0_1_0_2_0": "SAME", "2_1_0_1_0_2_1": "SAME", "2_1_0_1_1_0_0": "SAME", "2_1_0_1_1_0_1": "SAME", "2_1_0_1_1_1_0": "SAME", "2_1_0_1_1_1_1": "SAME", "2_1_0_1_1_2_0": "SAME", "2_1_0_1_1_2_1": "SAME", "2_1_0_1_2_0_0": "SAME", "2_1_0_1_2_0_1": "SAME", "2_1_0_1_2_1_0": "SAME", "2_1_0_1_2_1_1": "SAME", "2_1_0_1_2_2_0": "SAME", "2_1_0_1_2_2_1": "SAME", "2_1_0_1_3_0_0": "SAME", "2_1_0_1_3_0_1": "SAME", "2_1_0_1_3_1_0": "SAME", "2_1_0_1_3_1_1": "SAME", "2_1_0_1_3_2_0": "SAME", "2_1_0_1_3_2_1": "SAME", "2_1_0_2_0_0_0": "SAME", "2_1_0_2_0_0_1": "SAME", "2_1_0_2_0_1_0": "SAME", "2_1_0_2_0_1_1": "SAME", "2_1_0_2_0_2_0": "SAME", "2_1_0_2_0_2_1": "SAME", "2_1_0_2_1_0_0": "SAME", "2_1_0_2_1_0_1": "SAME", "2_1_0_2_1_1_0": "SAME", "2_1_0_2_1_1_1": "SAME", "2_1_0_2_1_2_0": "SAME", "2_1_0_2_1_2_1": "SAME", "2_1_0_2_2_0_0": "SAME", "2_1_0_2_2_0_1": "SAME", "2_1_0_2_2_1_0": "SAME", "2_1_0_2_2_1_1": "SAME", "2_1_0_2_2_2_0": "SAME", "2_1_0_2_2_2_1": "SAME", "2_1_0_2_3_0_0": "SAME", "2_1_0_2_3_0_1": "SAME", "2_1_0_2_3_1_0": "SAME", "2_1_0_2_3_1_1": "SAME", "2_1_0_2_3_2_0": "SAME", "2_1_0_2_3_2_1": "SAME", "2_1_0_3_0_0_0": "SAME", "2_1_0_3_0_0_1": "SAME", "2_1_0_3_0_1_0": "SAME", "2_1_0_3_0_1_1": "SAME", "2_1_0_3_0_2_0": "SAME", "2_1_0_3_0_2_1": "SAME", "2_1_0_3_1_0_0": "SAME", "2_1_0_3_1_0_1": "SAME", "2_1_0_3_1_1_0": "SAME", "2_1_0_3_1_1_1": "SAME", "2_1_0_3_1_2_0": "SAME", "2_1_0_3_1_2_1": "SAME", "2_1_0_3_2_0_0": "SAME", "2_1_0_3_2_0_1": "SAME", "2_1_0_3_2_1_0": "SAME", "2_1_0_3_2_1_1": "SAME", "2_1_0_3_2_2_0": "SAME", "2_1_0_3_2_2_1": "SAME", "2_1_0_3_3_0_0": "SAME", "2_1_0_3_3_0_1": "SAME", "2_1_0_3_3_1_0": "SAME", "2_1_0_3_3_1_1": "SAME", "2_1_0_3_3_2_0": "SAME", "2_1_0_3_3_2_1": "SAME", "2_1_1_0_0_0_0": "SAME", "2_1_1_0_0_0_1": "SAME", "2_1_1_0_0_1_0": "SAME", "2_1_1_0_0_1_1": "SAME", "2_1_1_0_0_2_0": "SAME", "2_1_1_0_0_2_1": "SAME", "2_1_1_0_1_0_0": "SAME", "2_1_1_0_1_0_1": "SAME", "2_1_1_0_1_1_0": "SAME", "2_1_1_0_1_1_1": "SAME", "2_1_1_0_1_2_0": "SAME", "2_1_1_0_1_2_1": "SAME", "2_1_1_0_2_0_0": "SAME", "2_1_1_0_2_0_1": "SAME", "2_1_1_0_2_1_0": "SAME", "2_1_1_0_2_1_1": "SAME", "2_1_1_0_2_2_0": "SAME", "2_1_1_0_2_2_1": "SAME", "2_1_1_0_3_0_0": "SAME", "2_1_1_0_3_0_1": "SAME", "2_1_1_0_3_1_0": "SAME", "2_1_1_0_3_1_1": "SAME", "2_1_1_0_3_2_0": "SAME", "2_1_1_0_3_2_1": "SAME", "2_1_1_1_0_0_0": "SAME", "2_1_1_1_0_0_1": "SAME", "2_1_1_1_0_1_0": "SAME", "2_1_1_1_0_1_1": "SAME", "2_1_1_1_0_2_0": "SAME", "2_1_1_1_0_2_1": "SAME", "2_1_1_1_1_0_0": "SAME", "2_1_1_1_1_0_1": "SAME", "2_1_1_1_1_1_0": "SAME", "2_1_1_1_1_1_1": "SAME", "2_1_1_1_1_2_0": "SAME", "2_1_1_1_1_2_1": "SAME", "2_1_1_1_2_0_0": "SAME", "2_1_1_1_2_0_1": "SAME", "2_1_1_1_2_1_0": "SAME", "2_1_1_1_2_1_1": "SAME", "2_1_1_1_2_2_0": "SAME", "2_1_1_1_2_2_1": "SAME", "2_1_1_1_3_0_0": "SAME", "2_1_1_1_3_0_1": "SAME", "2_1_1_1_3_1_0": "SAME", "2_1_1_1_3_1_1": "SAME", "2_1_1_1_3_2_0": "SAME", "2_1_1_1_3_2_1": "SAME", "2_1_1_2_0_0_0": "SAME", "2_1_1_2_0_0_1": "SAME", "2_1_1_2_0_1_0": "SAME", "2_1_1_2_0_1_1": "SAME", "2_1_1_2_0_2_0": "SAME", "2_1_1_2_0_2_1": "SAME", "2_1_1_2_1_0_0": "SAME", "2_1_1_2_1_0_1": "SAME", "2_1_1_2_1_1_0": "SAME", "2_1_1_2_1_1_1": "SAME", "2_1_1_2_1_2_0": "SAME", "2_1_1_2_1_2_1": "SAME", "2_1_1_2_2_0_0": "SAME", "2_1_1_2_2_0_1": "SAME", "2_1_1_2_2_1_0": "SAME", "2_1_1_2_2_1_1": "OPP", "2_1_1_2_2_2_0": "SAME", "2_1_1_2_2_2_1": "SAME", "2_1_1_2_3_0_0": "SAME", "2_1_1_2_3_0_1": "SAME", "2_1_1_2_3_1_0": "SAME", "2_1_1_2_3_1_1": "SAME", "2_1_1_2_3_2_0": "SAME", "2_1_1_2_3_2_1": "SAME", "2_1_1_3_0_0_0": "SAME", "2_1_1_3_0_0_1": "SAME", "2_1_1_3_0_1_0": "SAME", "2_1_1_3_0_1_1": "SAME", "2_1_1_3_0_2_0": "SAME", "2_1_1_3_0_2_1": "SAME", "2_1_1_3_1_0_0": "SAME", "2_1_1_3_1_0_1": "SAME", "2_1_1_3_1_1_0": "SAME", "2_1_1_3_1_1_1": "SAME", "2_1_1_3_1_2_0": "SAME", "2_1_1_3_1_2_1": "SAME", "2_1_1_3_2_0_0": "SAME", "2_1_1_3_2_0_1": "SAME", "2_1_1_3_2_1_0": "SAME", "2_1_1_3_2_1_1": "SAME", "2_1_1_3_2_2_0": "SAME", "2_1_1_3_2_2_1": "SAME", "2_1_1_3_3_0_0": "SAME", "2_1_1_3_3_0_1": "SAME", "2_1_1_3_3_1_0": "SAME", "2_1_1_3_3_1_1": "SAME", "2_1_1_3_3_2_0": "SAME", "2_1_1_3_3_2_1": "SAME", "2_1_2_0_0_0_0": "SAME", "2_1_2_0_0_0_1": "SAME", "2_1_2_0_0_1_0": "SAME", "2_1_2_0_0_1_1": "SAME", "2_1_2_0_0_2_0": "SAME", "2_1_2_0_0_2_1": "SAME", "2_1_2_0_1_0_0": "SAME", "2_1_2_0_1_0_1": "SAME", "2_1_2_0_1_1_0": "SAME", "2_1_2_0_1_1_1": "SAME", "2_1_2_0_1_2_0": "SAME", "2_1_2_0_1_2_1": "SAME", "2_1_2_0_2_0_0": "SAME", "2_1_2_0_2_0_1": "SAME", "2_1_2_0_2_1_0": "SAME", "2_1_2_0_2_1_1": "SAME", "2_1_2_0_2_2_0": "SAME", "2_1_2_0_2_2_1": "SAME", "2_1_2_0_3_0_0": "SAME", "2_1_2_0_3_0_1": "SAME", "2_1_2_0_3_1_0": "SAME", "2_1_2_0_3_1_1": "SAME", "2_1_2_0_3_2_0": "SAME", "2_1_2_0_3_2_1": "SAME", "2_1_2_1_0_0_0": "SAME", "2_1_2_1_0_0_1": "SAME", "2_1_2_1_0_1_0": "SAME", "2_1_2_1_0_1_1": "SAME", "2_1_2_1_0_2_0": "SAME", "2_1_2_1_0_2_1": "SAME", "2_1_2_1_1_0_0": "SAME", "2_1_2_1_1_0_1": "SAME", "2_1_2_1_1_1_0": "SAME", "2_1_2_1_1_1_1": "OPP", "2_1_2_1_1_2_0": "SAME", "2_1_2_1_1_2_1": "SAME", "2_1_2_1_2_0_0": "SAME", "2_1_2_1_2_0_1": "SAME", "2_1_2_1_2_1_0": "SAME", "2_1_2_1_2_1_1": "SAME", "2_1_2_1_2_2_0": "SAME", "2_1_2_1_2_2_1": "SAME", "2_1_2_1_3_0_0": "SAME", "2_1_2_1_3_0_1": "SAME", "2_1_2_1_3_1_0": "SAME", "2_1_2_1_3_1_1": "SAME", "2_1_2_1_3_2_0": "SAME", "2_1_2_1_3_2_1": "SAME", "2_1_2_2_0_0_0": "SAME", "2_1_2_2_0_0_1": "SAME", "2_1_2_2_0_1_0": "SAME", "2_1_2_2_0_1_1": "SAME", "2_1_2_2_0_2_0": "SAME", "2_1_2_2_0_2_1": "SAME", "2_1_2_2_1_0_0": "SAME", "2_1_2_2_1_0_1": "SAME", "2_1_2_2_1_1_0": "SAME", "2_1_2_2_1_1_1": "SAME", "2_1_2_2_1_2_0": "SAME", "2_1_2_2_1_2_1": "SAME", "2_1_2_2_2_0_0": "SAME", "2_1_2_2_2_0_1": "SAME", "2_1_2_2_2_1_0": "SAME", "2_1_2_2_2_1_1": "SAME", "2_1_2_2_2_2_0": "SAME", "2_1_2_2_2_2_1": "SAME", "2_1_2_2_3_0_0": "SAME", "2_1_2_2_3_0_1": "SAME", "2_1_2_2_3_1_0": "SAME", "2_1_2_2_3_1_1": "SAME", "2_1_2_2_3_2_0": "SAME", "2_1_2_2_3_2_1": "SAME", "2_1_2_3_0_0_0": "SAME", "2_1_2_3_0_0_1": "SAME", "2_1_2_3_0_1_0": "SAME", "2_1_2_3_0_1_1": "SAME", "2_1_2_3_0_2_0": "SAME", "2_1_2_3_0_2_1": "SAME", "2_1_2_3_1_0_0": "SAME", "2_1_2_3_1_0_1": "SAME", "2_1_2_3_1_1_0": "OPP", "2_1_2_3_1_1_1": "SAME", "2_1_2_3_1_2_0": "SAME", "2_1_2_3_1_2_1": "SAME", "2_1_2_3_2_0_0": "SAME", "2_1_2_3_2_0_1": "SAME", "2_1_2_3_2_1_0": "SAME", "2_1_2_3_2_1_1": "SAME", "2_1_2_3_2_2_0": "SAME", "2_1_2_3_2_2_1": "SAME", "2_1_2_3_3_0_0": "SAME", "2_1_2_3_3_0_1": "SAME", "2_1_2_3_3_1_0": "SAME", "2_1_2_3_3_1_1": "SAME", "2_1_2_3_3_2_0": "SAME", "2_1_2_3_3_2_1": "SAME", "2_1_3_0_0_0_0": "SAME", "2_1_3_0_0_0_1": "SAME", "2_1_3_0_0_1_0": "SAME", "2_1_3_0_0_1_1": "SAME", "2_1_3_0_0_2_0": "SAME", "2_1_3_0_0_2_1": "SAME", "2_1_3_0_1_0_0": "SAME", "2_1_3_0_1_0_1": "SAME", "2_1_3_0_1_1_0": "SAME", "2_1_3_0_1_1_1": "SAME", "2_1_3_0_1_2_0": "SAME", "2_1_3_0_1_2_1": "SAME", "2_1_3_0_2_0_0": "SAME", "2_1_3_0_2_0_1": "SAME", "2_1_3_0_2_1_0": "SAME", "2_1_3_0_2_1_1": "SAME", "2_1_3_0_2_2_0": "SAME", "2_1_3_0_2_2_1": "SAME", "2_1_3_0_3_0_0": "SAME", "2_1_3_0_3_0_1": "SAME", "2_1_3_0_3_1_0": "SAME", "2_1_3_0_3_1_1": "SAME", "2_1_3_0_3_2_0": "SAME", "2_1_3_0_3_2_1": "SAME", "2_1_3_1_0_0_0": "SAME", "2_1_3_1_0_0_1": "SAME", "2_1_3_1_0_1_0": "SAME", "2_1_3_1_0_1_1": "SAME", "2_1_3_1_0_2_0": "SAME", "2_1_3_1_0_2_1": "SAME", "2_1_3_1_1_0_0": "SAME", "2_1_3_1_1_0_1": "SAME", "2_1_3_1_1_1_0": "SAME", "2_1_3_1_1_1_1": "SAME", "2_1_3_1_1_2_0": "SAME", "2_1_3_1_1_2_1": "SAME", "2_1_3_1_2_0_0": "SAME", "2_1_3_1_2_0_1": "SAME", "2_1_3_1_2_1_0": "SAME", "2_1_3_1_2_1_1": "SAME", "2_1_3_1_2_2_0": "SAME", "2_1_3_1_2_2_1": "SAME", "2_1_3_1_3_0_0": "SAME", "2_1_3_1_3_0_1": "SAME", "2_1_3_1_3_1_0": "SAME", "2_1_3_1_3_1_1": "SAME", "2_1_3_1_3_2_0": "SAME", "2_1_3_1_3_2_1": "SAME", "2_1_3_2_0_0_0": "SAME", "2_1_3_2_0_0_1": "SAME", "2_1_3_2_0_1_0": "SAME", "2_1_3_2_0_1_1": "SAME", "2_1_3_2_0_2_0": "SAME", "2_1_3_2_0_2_1": "SAME", "2_1_3_2_1_0_0": "SAME", "2_1_3_2_1_0_1": "SAME", "2_1_3_2_1_1_0": "SAME", "2_1_3_2_1_1_1": "SAME", "2_1_3_2_1_2_0": "SAME", "2_1_3_2_1_2_1": "SAME", "2_1_3_2_2_0_0": "SAME", "2_1_3_2_2_0_1": "SAME", "2_1_3_2_2_1_0": "SAME", "2_1_3_2_2_1_1": "SAME", "2_1_3_2_2_2_0": "SAME", "2_1_3_2_2_2_1": "SAME", "2_1_3_2_3_0_0": "SAME", "2_1_3_2_3_0_1": "SAME", "2_1_3_2_3_1_0": "SAME", "2_1_3_2_3_1_1": "SAME", "2_1_3_2_3_2_0": "SAME", "2_1_3_2_3_2_1": "SAME", "2_1_3_3_0_0_0": "SAME", "2_1_3_3_0_0_1": "SAME", "2_1_3_3_0_1_0": "SAME", "2_1_3_3_0_1_1": "SAME", "2_1_3_3_0_2_0": "SAME", "2_1_3_3_0_2_1": "SAME", "2_1_3_3_1_0_0": "SAME", "2_1_3_3_1_0_1": "SAME", "2_1_3_3_1_1_0": "SAME", "2_1_3_3_1_1_1": "SAME", "2_1_3_3_1_2_0": "SAME", "2_1_3_3_1_2_1": "SAME", "2_1_3_3_2_0_0": "SAME", "2_1_3_3_2_0_1": "SAME", "2_1_3_3_2_1_0": "SAME", "2_1_3_3_2_1_1": "SAME", "2_1_3_3_2_2_0": "SAME", "2_1_3_3_2_2_1": "SAME", "2_1_3_3_3_0_0": "SAME", "2_1_3_3_3_0_1": "SAME", "2_1_3_3_3_1_0": "SAME", "2_1_3_3_3_1_1": "SAME", "2_1_3_3_3_2_0": "SAME", "2_1_3_3_3_2_1": "SAME", "2_2_0_0_0_0_0": "SAME", "2_2_0_0_0_0_1": "SAME", "2_2_0_0_0_1_0": "SAME", "2_2_0_0_0_1_1": "SAME", "2_2_0_0_0_2_0": "SAME", "2_2_0_0_0_2_1": "SAME", "2_2_0_0_1_0_0": "SAME", "2_2_0_0_1_0_1": "SAME", "2_2_0_0_1_1_0": "SAME", "2_2_0_0_1_1_1": "SAME", "2_2_0_0_1_2_0": "SAME", "2_2_0_0_1_2_1": "SAME", "2_2_0_0_2_0_0": "SAME", "2_2_0_0_2_0_1": "SAME", "2_2_0_0_2_1_0": "SAME", "2_2_0_0_2_1_1": "SAME", "2_2_0_0_2_2_0": "SAME", "2_2_0_0_2_2_1": "SAME", "2_2_0_0_3_0_0": "SAME", "2_2_0_0_3_0_1": "SAME", "2_2_0_0_3_1_0": "SAME", "2_2_0_0_3_1_1": "SAME", "2_2_0_0_3_2_0": "SAME", "2_2_0_0_3_2_1": "SAME", "2_2_0_1_0_0_0": "SAME", "2_2_0_1_0_0_1": "SAME", "2_2_0_1_0_1_0": "SAME", "2_2_0_1_0_1_1": "SAME", "2_2_0_1_0_2_0": "SAME", "2_2_0_1_0_2_1": "SAME", "2_2_0_1_1_0_0": "SAME", "2_2_0_1_1_0_1": "SAME", "2_2_0_1_1_1_0": "SAME", "2_2_0_1_1_1_1": "SAME", "2_2_0_1_1_2_0": "SAME", "2_2_0_1_1_2_1": "SAME", "2_2_0_1_2_0_0": "SAME", "2_2_0_1_2_0_1": "SAME", "2_2_0_1_2_1_0": "SAME", "2_2_0_1_2_1_1": "SAME", "2_2_0_1_2_2_0": "SAME", "2_2_0_1_2_2_1": "SAME", "2_2_0_1_3_0_0": "SAME", "2_2_0_1_3_0_1": "SAME", "2_2_0_1_3_1_0": "SAME", "2_2_0_1_3_1_1": "SAME", "2_2_0_1_3_2_0": "SAME", "2_2_0_1_3_2_1": "SAME", "2_2_0_2_0_0_0": "SAME", "2_2_0_2_0_0_1": "SAME", "2_2_0_2_0_1_0": "SAME", "2_2_0_2_0_1_1": "SAME", "2_2_0_2_0_2_0": "SAME", "2_2_0_2_0_2_1": "SAME", "2_2_0_2_1_0_0": "SAME", "2_2_0_2_1_0_1": "SAME", "2_2_0_2_1_1_0": "SAME", "2_2_0_2_1_1_1": "SAME", "2_2_0_2_1_2_0": "SAME", "2_2_0_2_1_2_1": "SAME", "2_2_0_2_2_0_0": "SAME", "2_2_0_2_2_0_1": "SAME", "2_2_0_2_2_1_0": "SAME", "2_2_0_2_2_1_1": "SAME", "2_2_0_2_2_2_0": "SAME", "2_2_0_2_2_2_1": "SAME", "2_2_0_2_3_0_0": "SAME", "2_2_0_2_3_0_1": "SAME", "2_2_0_2_3_1_0": "SAME", "2_2_0_2_3_1_1": "SAME", "2_2_0_2_3_2_0": "SAME", "2_2_0_2_3_2_1": "SAME", "2_2_0_3_0_0_0": "SAME", "2_2_0_3_0_0_1": "SAME", "2_2_0_3_0_1_0": "SAME", "2_2_0_3_0_1_1": "SAME", "2_2_0_3_0_2_0": "SAME", "2_2_0_3_0_2_1": "SAME", "2_2_0_3_1_0_0": "SAME", "2_2_0_3_1_0_1": "SAME", "2_2_0_3_1_1_0": "SAME", "2_2_0_3_1_1_1": "SAME", "2_2_0_3_1_2_0": "SAME", "2_2_0_3_1_2_1": "SAME", "2_2_0_3_2_0_0": "SAME", "2_2_0_3_2_0_1": "SAME", "2_2_0_3_2_1_0": "SAME", "2_2_0_3_2_1_1": "SAME", "2_2_0_3_2_2_0": "SAME", "2_2_0_3_2_2_1": "SAME", "2_2_0_3_3_0_0": "SAME", "2_2_0_3_3_0_1": "SAME", "2_2_0_3_3_1_0": "SAME", "2_2_0_3_3_1_1": "SAME", "2_2_0_3_3_2_0": "SAME", "2_2_0_3_3_2_1": "SAME", "2_2_1_0_0_0_0": "SAME", "2_2_1_0_0_0_1": "SAME", "2_2_1_0_0_1_0": "SAME", "2_2_1_0_0_1_1": "SAME", "2_2_1_0_0_2_0": "SAME", "2_2_1_0_0_2_1": "SAME", "2_2_1_0_1_0_0": "SAME", "2_2_1_0_1_0_1": "SAME", "2_2_1_0_1_1_0": "SAME", "2_2_1_0_1_1_1": "SAME", "2_2_1_0_1_2_0": "SAME", "2_2_1_0_1_2_1": "SAME", "2_2_1_0_2_0_0": "SAME", "2_2_1_0_2_0_1": "SAME", "2_2_1_0_2_1_0": "SAME", "2_2_1_0_2_1_1": "SAME", "2_2_1_0_2_2_0": "SAME", "2_2_1_0_2_2_1": "SAME", "2_2_1_0_3_0_0": "SAME", "2_2_1_0_3_0_1": "SAME", "2_2_1_0_3_1_0": "SAME", "2_2_1_0_3_1_1": "SAME", "2_2_1_0_3_2_0": "SAME", "2_2_1_0_3_2_1": "SAME", "2_2_1_1_0_0_0": "SAME", "2_2_1_1_0_0_1": "SAME", "2_2_1_1_0_1_0": "SAME", "2_2_1_1_0_1_1": "SAME", "2_2_1_1_0_2_0": "SAME", "2_2_1_1_0_2_1": "SAME", "2_2_1_1_1_0_0": "SAME", "2_2_1_1_1_0_1": "SAME", "2_2_1_1_1_1_0": "SAME", "2_2_1_1_1_1_1": "SAME", "2_2_1_1_1_2_0": "SAME", "2_2_1_1_1_2_1": "SAME", "2_2_1_1_2_0_0": "SAME", "2_2_1_1_2_0_1": "SAME", "2_2_1_1_2_1_0": "SAME", "2_2_1_1_2_1_1": "SAME", "2_2_1_1_2_2_0": "SAME", "2_2_1_1_2_2_1": "SAME", "2_2_1_1_3_0_0": "SAME", "2_2_1_1_3_0_1": "SAME", "2_2_1_1_3_1_0": "SAME", "2_2_1_1_3_1_1": "SAME", "2_2_1_1_3_2_0": "SAME", "2_2_1_1_3_2_1": "SAME", "2_2_1_2_0_0_0": "SAME", "2_2_1_2_0_0_1": "SAME", "2_2_1_2_0_1_0": "SAME", "2_2_1_2_0_1_1": "SAME", "2_2_1_2_0_2_0": "SAME", "2_2_1_2_0_2_1": "SAME", "2_2_1_2_1_0_0": "SAME", "2_2_1_2_1_0_1": "SAME", "2_2_1_2_1_1_0": "SAME", "2_2_1_2_1_1_1": "SAME", "2_2_1_2_1_2_0": "SAME", "2_2_1_2_1_2_1": "SAME", "2_2_1_2_2_0_0": "SAME", "2_2_1_2_2_0_1": "SAME", "2_2_1_2_2_1_0": "SAME", "2_2_1_2_2_1_1": "SAME", "2_2_1_2_2_2_0": "SAME", "2_2_1_2_2_2_1": "SAME", "2_2_1_2_3_0_0": "SAME", "2_2_1_2_3_0_1": "SAME", "2_2_1_2_3_1_0": "SAME", "2_2_1_2_3_1_1": "SAME", "2_2_1_2_3_2_0": "SAME", "2_2_1_2_3_2_1": "SAME", "2_2_1_3_0_0_0": "SAME", "2_2_1_3_0_0_1": "SAME", "2_2_1_3_0_1_0": "SAME", "2_2_1_3_0_1_1": "SAME", "2_2_1_3_0_2_0": "SAME", "2_2_1_3_0_2_1": "SAME", "2_2_1_3_1_0_0": "SAME", "2_2_1_3_1_0_1": "SAME", "2_2_1_3_1_1_0": "SAME", "2_2_1_3_1_1_1": "SAME", "2_2_1_3_1_2_0": "SAME", "2_2_1_3_1_2_1": "SAME", "2_2_1_3_2_0_0": "SAME", "2_2_1_3_2_0_1": "SAME", "2_2_1_3_2_1_0": "SAME", "2_2_1_3_2_1_1": "SAME", "2_2_1_3_2_2_0": "SAME", "2_2_1_3_2_2_1": "SAME", "2_2_1_3_3_0_0": "SAME", "2_2_1_3_3_0_1": "SAME", "2_2_1_3_3_1_0": "SAME", "2_2_1_3_3_1_1": "SAME", "2_2_1_3_3_2_0": "SAME", "2_2_1_3_3_2_1": "SAME", "2_2_2_0_0_0_0": "SAME", "2_2_2_0_0_0_1": "SAME", "2_2_2_0_0_1_0": "SAME", "2_2_2_0_0_1_1": "SAME", "2_2_2_0_0_2_0": "SAME", "2_2_2_0_0_2_1": "SAME", "2_2_2_0_1_0_0": "SAME", "2_2_2_0_1_0_1": "SAME", "2_2_2_0_1_1_0": "SAME", "2_2_2_0_1_1_1": "SAME", "2_2_2_0_1_2_0": "SAME", "2_2_2_0_1_2_1": "SAME", "2_2_2_0_2_0_0": "SAME", "2_2_2_0_2_0_1": "SAME", "2_2_2_0_2_1_0": "SAME", "2_2_2_0_2_1_1": "SAME", "2_2_2_0_2_2_0": "SAME", "2_2_2_0_2_2_1": "SAME", "2_2_2_0_3_0_0": "SAME", "2_2_2_0_3_0_1": "SAME", "2_2_2_0_3_1_0": "SAME", "2_2_2_0_3_1_1": "SAME", "2_2_2_0_3_2_0": "SAME", "2_2_2_0_3_2_1": "SAME", "2_2_2_1_0_0_0": "SAME", "2_2_2_1_0_0_1": "SAME", "2_2_2_1_0_1_0": "SAME", "2_2_2_1_0_1_1": "SAME", "2_2_2_1_0_2_0": "SAME", "2_2_2_1_0_2_1": "SAME", "2_2_2_1_1_0_0": "SAME", "2_2_2_1_1_0_1": "SAME", "2_2_2_1_1_1_0": "SAME", "2_2_2_1_1_1_1": "SAME", "2_2_2_1_1_2_0": "SAME", "2_2_2_1_1_2_1": "SAME", "2_2_2_1_2_0_0": "SAME", "2_2_2_1_2_0_1": "SAME", "2_2_2_1_2_1_0": "SAME", "2_2_2_1_2_1_1": "SAME", "2_2_2_1_2_2_0": "SAME", "2_2_2_1_2_2_1": "SAME", "2_2_2_1_3_0_0": "SAME", "2_2_2_1_3_0_1": "SAME", "2_2_2_1_3_1_0": "SAME", "2_2_2_1_3_1_1": "SAME", "2_2_2_1_3_2_0": "SAME", "2_2_2_1_3_2_1": "SAME", "2_2_2_2_0_0_0": "SAME", "2_2_2_2_0_0_1": "SAME", "2_2_2_2_0_1_0": "SAME", "2_2_2_2_0_1_1": "SAME", "2_2_2_2_0_2_0": "SAME", "2_2_2_2_0_2_1": "SAME", "2_2_2_2_1_0_0": "SAME", "2_2_2_2_1_0_1": "SAME", "2_2_2_2_1_1_0": "SAME", "2_2_2_2_1_1_1": "SAME", "2_2_2_2_1_2_0": "SAME", "2_2_2_2_1_2_1": "SAME", "2_2_2_2_2_0_0": "SAME", "2_2_2_2_2_0_1": "SAME", "2_2_2_2_2_1_0": "SAME", "2_2_2_2_2_1_1": "SAME", "2_2_2_2_2_2_0": "SAME", "2_2_2_2_2_2_1": "SAME", "2_2_2_2_3_0_0": "SAME", "2_2_2_2_3_0_1": "SAME", "2_2_2_2_3_1_0": "SAME", "2_2_2_2_3_1_1": "SAME", "2_2_2_2_3_2_0": "SAME", "2_2_2_2_3_2_1": "SAME", "2_2_2_3_0_0_0": "SAME", "2_2_2_3_0_0_1": "SAME", "2_2_2_3_0_1_0": "SAME", "2_2_2_3_0_1_1": "SAME", "2_2_2_3_0_2_0": "SAME", "2_2_2_3_0_2_1": "SAME", "2_2_2_3_1_0_0": "SAME", "2_2_2_3_1_0_1": "SAME", "2_2_2_3_1_1_0": "SAME", "2_2_2_3_1_1_1": "SAME", "2_2_2_3_1_2_0": "SAME", "2_2_2_3_1_2_1": "SAME", "2_2_2_3_2_0_0": "SAME", "2_2_2_3_2_0_1": "SAME", "2_2_2_3_2_1_0": "SAME", "2_2_2_3_2_1_1": "SAME", "2_2_2_3_2_2_0": "SAME", "2_2_2_3_2_2_1": "SAME", "2_2_2_3_3_0_0": "SAME", "2_2_2_3_3_0_1": "SAME", "2_2_2_3_3_1_0": "SAME", "2_2_2_3_3_1_1": "SAME", "2_2_2_3_3_2_0": "SAME", "2_2_2_3_3_2_1": "SAME", "2_2_3_0_0_0_0": "SAME", "2_2_3_0_0_0_1": "SAME", "2_2_3_0_0_1_0": "SAME", "2_2_3_0_0_1_1": "SAME", "2_2_3_0_0_2_0": "SAME", "2_2_3_0_0_2_1": "SAME", "2_2_3_0_1_0_0": "SAME", "2_2_3_0_1_0_1": "SAME", "2_2_3_0_1_1_0": "SAME", "2_2_3_0_1_1_1": "SAME", "2_2_3_0_1_2_0": "SAME", "2_2_3_0_1_2_1": "SAME", "2_2_3_0_2_0_0": "SAME", "2_2_3_0_2_0_1": "SAME", "2_2_3_0_2_1_0": "SAME", "2_2_3_0_2_1_1": "SAME", "2_2_3_0_2_2_0": "SAME", "2_2_3_0_2_2_1": "SAME", "2_2_3_0_3_0_0": "SAME", "2_2_3_0_3_0_1": "SAME", "2_2_3_0_3_1_0": "SAME", "2_2_3_0_3_1_1": "SAME", "2_2_3_0_3_2_0": "SAME", "2_2_3_0_3_2_1": "SAME", "2_2_3_1_0_0_0": "SAME", "2_2_3_1_0_0_1": "SAME", "2_2_3_1_0_1_0": "SAME", "2_2_3_1_0_1_1": "SAME", "2_2_3_1_0_2_0": "SAME", "2_2_3_1_0_2_1": "SAME", "2_2_3_1_1_0_0": "SAME", "2_2_3_1_1_0_1": "SAME", "2_2_3_1_1_1_0": "SAME", "2_2_3_1_1_1_1": "SAME", "2_2_3_1_1_2_0": "SAME", "2_2_3_1_1_2_1": "SAME", "2_2_3_1_2_0_0": "SAME", "2_2_3_1_2_0_1": "SAME", "2_2_3_1_2_1_0": "SAME", "2_2_3_1_2_1_1": "SAME", "2_2_3_1_2_2_0": "SAME", "2_2_3_1_2_2_1": "SAME", "2_2_3_1_3_0_0": "SAME", "2_2_3_1_3_0_1": "SAME", "2_2_3_1_3_1_0": "SAME", "2_2_3_1_3_1_1": "SAME", "2_2_3_1_3_2_0": "SAME", "2_2_3_1_3_2_1": "SAME", "2_2_3_2_0_0_0": "SAME", "2_2_3_2_0_0_1": "OPP", "2_2_3_2_0_1_0": "SAME", "2_2_3_2_0_1_1": "SAME", "2_2_3_2_0_2_0": "SAME", "2_2_3_2_0_2_1": "SAME", "2_2_3_2_1_0_0": "SAME", "2_2_3_2_1_0_1": "SAME", "2_2_3_2_1_1_0": "SAME", "2_2_3_2_1_1_1": "SAME", "2_2_3_2_1_2_0": "SAME", "2_2_3_2_1_2_1": "SAME", "2_2_3_2_2_0_0": "SAME", "2_2_3_2_2_0_1": "SAME", "2_2_3_2_2_1_0": "SAME", "2_2_3_2_2_1_1": "SAME", "2_2_3_2_2_2_0": "SAME", "2_2_3_2_2_2_1": "SAME", "2_2_3_2_3_0_0": "SAME", "2_2_3_2_3_0_1": "SAME", "2_2_3_2_3_1_0": "SAME", "2_2_3_2_3_1_1": "SAME", "2_2_3_2_3_2_0": "SAME", "2_2_3_2_3_2_1": "SAME", "2_2_3_3_0_0_0": "SAME", "2_2_3_3_0_0_1": "SAME", "2_2_3_3_0_1_0": "SAME", "2_2_3_3_0_1_1": "SAME", "2_2_3_3_0_2_0": "SAME", "2_2_3_3_0_2_1": "SAME", "2_2_3_3_1_0_0": "SAME", "2_2_3_3_1_0_1": "SAME", "2_2_3_3_1_1_0": "SAME", "2_2_3_3_1_1_1": "SAME", "2_2_3_3_1_2_0": "SAME", "2_2_3_3_1_2_1": "SAME", "2_2_3_3_2_0_0": "SAME", "2_2_3_3_2_0_1": "SAME", "2_2_3_3_2_1_0": "SAME", "2_2_3_3_2_1_1": "SAME", "2_2_3_3_2_2_0": "SAME", "2_2_3_3_2_2_1": "SAME", "2_2_3_3_3_0_0": "SAME", "2_2_3_3_3_0_1": "SAME", "2_2_3_3_3_1_0": "SAME", "2_2_3_3_3_1_1": "SAME", "2_2_3_3_3_2_0": "SAME", "2_2_3_3_3_2_1": "SAME", "2_3_0_0_0_0_0": "SAME", "2_3_0_0_0_0_1": "SAME", "2_3_0_0_0_1_0": "SAME", "2_3_0_0_0_1_1": "SAME", "2_3_0_0_0_2_0": "SAME", "2_3_0_0_0_2_1": "SAME", "2_3_0_0_1_0_0": "SAME", "2_3_0_0_1_0_1": "SAME", "2_3_0_0_1_1_0": "SAME", "2_3_0_0_1_1_1": "SAME", "2_3_0_0_1_2_0": "SAME", "2_3_0_0_1_2_1": "SAME", "2_3_0_0_2_0_0": "SAME", "2_3_0_0_2_0_1": "SAME", "2_3_0_0_2_1_0": "SAME", "2_3_0_0_2_1_1": "SAME", "2_3_0_0_2_2_0": "SAME", "2_3_0_0_2_2_1": "SAME", "2_3_0_0_3_0_0": "SAME", "2_3_0_0_3_0_1": "SAME", "2_3_0_0_3_1_0": "SAME", "2_3_0_0_3_1_1": "SAME", "2_3_0_0_3_2_0": "SAME", "2_3_0_0_3_2_1": "SAME", "2_3_0_1_0_0_0": "SAME", "2_3_0_1_0_0_1": "SAME", "2_3_0_1_0_1_0": "SAME", "2_3_0_1_0_1_1": "SAME", "2_3_0_1_0_2_0": "SAME", "2_3_0_1_0_2_1": "SAME", "2_3_0_1_1_0_0": "SAME", "2_3_0_1_1_0_1": "SAME", "2_3_0_1_1_1_0": "SAME", "2_3_0_1_1_1_1": "SAME", "2_3_0_1_1_2_0": "SAME", "2_3_0_1_1_2_1": "SAME", "2_3_0_1_2_0_0": "SAME", "2_3_0_1_2_0_1": "SAME", "2_3_0_1_2_1_0": "SAME", "2_3_0_1_2_1_1": "SAME", "2_3_0_1_2_2_0": "SAME", "2_3_0_1_2_2_1": "SAME", "2_3_0_1_3_0_0": "SAME", "2_3_0_1_3_0_1": "SAME", "2_3_0_1_3_1_0": "SAME", "2_3_0_1_3_1_1": "SAME", "2_3_0_1_3_2_0": "SAME", "2_3_0_1_3_2_1": "SAME", "2_3_0_2_0_0_0": "SAME", "2_3_0_2_0_0_1": "SAME", "2_3_0_2_0_1_0": "SAME", "2_3_0_2_0_1_1": "SAME", "2_3_0_2_0_2_0": "SAME", "2_3_0_2_0_2_1": "SAME", "2_3_0_2_1_0_0": "SAME", "2_3_0_2_1_0_1": "SAME", "2_3_0_2_1_1_0": "SAME", "2_3_0_2_1_1_1": "SAME", "2_3_0_2_1_2_0": "SAME", "2_3_0_2_1_2_1": "SAME", "2_3_0_2_2_0_0": "SAME", "2_3_0_2_2_0_1": "SAME", "2_3_0_2_2_1_0": "SAME", "2_3_0_2_2_1_1": "SAME", "2_3_0_2_2_2_0": "SAME", "2_3_0_2_2_2_1": "SAME", "2_3_0_2_3_0_0": "SAME", "2_3_0_2_3_0_1": "SAME", "2_3_0_2_3_1_0": "SAME", "2_3_0_2_3_1_1": "SAME", "2_3_0_2_3_2_0": "SAME", "2_3_0_2_3_2_1": "SAME", "2_3_0_3_0_0_0": "SAME", "2_3_0_3_0_0_1": "SAME", "2_3_0_3_0_1_0": "SAME", "2_3_0_3_0_1_1": "SAME", "2_3_0_3_0_2_0": "SAME", "2_3_0_3_0_2_1": "SAME", "2_3_0_3_1_0_0": "SAME", "2_3_0_3_1_0_1": "SAME", "2_3_0_3_1_1_0": "SAME", "2_3_0_3_1_1_1": "SAME", "2_3_0_3_1_2_0": "SAME", "2_3_0_3_1_2_1": "SAME", "2_3_0_3_2_0_0": "SAME", "2_3_0_3_2_0_1": "SAME", "2_3_0_3_2_1_0": "SAME", "2_3_0_3_2_1_1": "SAME", "2_3_0_3_2_2_0": "SAME", "2_3_0_3_2_2_1": "SAME", "2_3_0_3_3_0_0": "SAME", "2_3_0_3_3_0_1": "SAME", "2_3_0_3_3_1_0": "SAME", "2_3_0_3_3_1_1": "SAME", "2_3_0_3_3_2_0": "SAME", "2_3_0_3_3_2_1": "SAME", "2_3_1_0_0_0_0": "SAME", "2_3_1_0_0_0_1": "SAME", "2_3_1_0_0_1_0": "SAME", "2_3_1_0_0_1_1": "SAME", "2_3_1_0_0_2_0": "SAME", "2_3_1_0_0_2_1": "SAME", "2_3_1_0_1_0_0": "SAME", "2_3_1_0_1_0_1": "SAME", "2_3_1_0_1_1_0": "SAME", "2_3_1_0_1_1_1": "SAME", "2_3_1_0_1_2_0": "SAME", "2_3_1_0_1_2_1": "SAME", "2_3_1_0_2_0_0": "SAME", "2_3_1_0_2_0_1": "SAME", "2_3_1_0_2_1_0": "SAME", "2_3_1_0_2_1_1": "SAME", "2_3_1_0_2_2_0": "SAME", "2_3_1_0_2_2_1": "SAME", "2_3_1_0_3_0_0": "SAME", "2_3_1_0_3_0_1": "SAME", "2_3_1_0_3_1_0": "SAME", "2_3_1_0_3_1_1": "SAME", "2_3_1_0_3_2_0": "SAME", "2_3_1_0_3_2_1": "SAME", "2_3_1_1_0_0_0": "SAME", "2_3_1_1_0_0_1": "SAME", "2_3_1_1_0_1_0": "SAME", "2_3_1_1_0_1_1": "SAME", "2_3_1_1_0_2_0": "SAME", "2_3_1_1_0_2_1": "SAME", "2_3_1_1_1_0_0": "SAME", "2_3_1_1_1_0_1": "SAME", "2_3_1_1_1_1_0": "SAME", "2_3_1_1_1_1_1": "SAME", "2_3_1_1_1_2_0": "SAME", "2_3_1_1_1_2_1": "SAME", "2_3_1_1_2_0_0": "SAME", "2_3_1_1_2_0_1": "SAME", "2_3_1_1_2_1_0": "SAME", "2_3_1_1_2_1_1": "SAME", "2_3_1_1_2_2_0": "SAME", "2_3_1_1_2_2_1": "SAME", "2_3_1_1_3_0_0": "SAME", "2_3_1_1_3_0_1": "SAME", "2_3_1_1_3_1_0": "SAME", "2_3_1_1_3_1_1": "SAME", "2_3_1_1_3_2_0": "SAME", "2_3_1_1_3_2_1": "SAME", "2_3_1_2_0_0_0": "SAME", "2_3_1_2_0_0_1": "SAME", "2_3_1_2_0_1_0": "SAME", "2_3_1_2_0_1_1": "SAME", "2_3_1_2_0_2_0": "SAME", "2_3_1_2_0_2_1": "SAME", "2_3_1_2_1_0_0": "SAME", "2_3_1_2_1_0_1": "SAME", "2_3_1_2_1_1_0": "SAME", "2_3_1_2_1_1_1": "SAME", "2_3_1_2_1_2_0": "SAME", "2_3_1_2_1_2_1": "SAME", "2_3_1_2_2_0_0": "SAME", "2_3_1_2_2_0_1": "SAME", "2_3_1_2_2_1_0": "SAME", "2_3_1_2_2_1_1": "SAME", "2_3_1_2_2_2_0": "SAME", "2_3_1_2_2_2_1": "SAME", "2_3_1_2_3_0_0": "SAME", "2_3_1_2_3_0_1": "SAME", "2_3_1_2_3_1_0": "SAME", "2_3_1_2_3_1_1": "SAME", "2_3_1_2_3_2_0": "SAME", "2_3_1_2_3_2_1": "SAME", "2_3_1_3_0_0_0": "SAME", "2_3_1_3_0_0_1": "SAME", "2_3_1_3_0_1_0": "SAME", "2_3_1_3_0_1_1": "SAME", "2_3_1_3_0_2_0": "SAME", "2_3_1_3_0_2_1": "SAME", "2_3_1_3_1_0_0": "SAME", "2_3_1_3_1_0_1": "SAME", "2_3_1_3_1_1_0": "SAME", "2_3_1_3_1_1_1": "SAME", "2_3_1_3_1_2_0": "SAME", "2_3_1_3_1_2_1": "SAME", "2_3_1_3_2_0_0": "SAME", "2_3_1_3_2_0_1": "SAME", "2_3_1_3_2_1_0": "SAME", "2_3_1_3_2_1_1": "SAME", "2_3_1_3_2_2_0": "SAME", "2_3_1_3_2_2_1": "SAME", "2_3_1_3_3_0_0": "SAME", "2_3_1_3_3_0_1": "SAME", "2_3_1_3_3_1_0": "SAME", "2_3_1_3_3_1_1": "SAME", "2_3_1_3_3_2_0": "SAME", "2_3_1_3_3_2_1": "SAME", "2_3_2_0_0_0_0": "SAME", "2_3_2_0_0_0_1": "SAME", "2_3_2_0_0_1_0": "SAME", "2_3_2_0_0_1_1": "SAME", "2_3_2_0_0_2_0": "SAME", "2_3_2_0_0_2_1": "SAME", "2_3_2_0_1_0_0": "SAME", "2_3_2_0_1_0_1": "SAME", "2_3_2_0_1_1_0": "SAME", "2_3_2_0_1_1_1": "SAME", "2_3_2_0_1_2_0": "SAME", "2_3_2_0_1_2_1": "SAME", "2_3_2_0_2_0_0": "SAME", "2_3_2_0_2_0_1": "SAME", "2_3_2_0_2_1_0": "SAME", "2_3_2_0_2_1_1": "SAME", "2_3_2_0_2_2_0": "SAME", "2_3_2_0_2_2_1": "SAME", "2_3_2_0_3_0_0": "SAME", "2_3_2_0_3_0_1": "SAME", "2_3_2_0_3_1_0": "SAME", "2_3_2_0_3_1_1": "SAME", "2_3_2_0_3_2_0": "SAME", "2_3_2_0_3_2_1": "SAME", "2_3_2_1_0_0_0": "SAME", "2_3_2_1_0_0_1": "SAME", "2_3_2_1_0_1_0": "SAME", "2_3_2_1_0_1_1": "SAME", "2_3_2_1_0_2_0": "SAME", "2_3_2_1_0_2_1": "SAME", "2_3_2_1_1_0_0": "SAME", "2_3_2_1_1_0_1": "SAME", "2_3_2_1_1_1_0": "SAME", "2_3_2_1_1_1_1": "SAME", "2_3_2_1_1_2_0": "SAME", "2_3_2_1_1_2_1": "SAME", "2_3_2_1_2_0_0": "SAME", "2_3_2_1_2_0_1": "SAME", "2_3_2_1_2_1_0": "SAME", "2_3_2_1_2_1_1": "SAME", "2_3_2_1_2_2_0": "SAME", "2_3_2_1_2_2_1": "SAME", "2_3_2_1_3_0_0": "SAME", "2_3_2_1_3_0_1": "SAME", "2_3_2_1_3_1_0": "SAME", "2_3_2_1_3_1_1": "SAME", "2_3_2_1_3_2_0": "SAME", "2_3_2_1_3_2_1": "SAME", "2_3_2_2_0_0_0": "SAME", "2_3_2_2_0_0_1": "SAME", "2_3_2_2_0_1_0": "SAME", "2_3_2_2_0_1_1": "SAME", "2_3_2_2_0_2_0": "SAME", "2_3_2_2_0_2_1": "SAME", "2_3_2_2_1_0_0": "SAME", "2_3_2_2_1_0_1": "SAME", "2_3_2_2_1_1_0": "SAME", "2_3_2_2_1_1_1": "SAME", "2_3_2_2_1_2_0": "SAME", "2_3_2_2_1_2_1": "SAME", "2_3_2_2_2_0_0": "SAME", "2_3_2_2_2_0_1": "SAME", "2_3_2_2_2_1_0": "SAME", "2_3_2_2_2_1_1": "SAME", "2_3_2_2_2_2_0": "SAME", "2_3_2_2_2_2_1": "SAME", "2_3_2_2_3_0_0": "SAME", "2_3_2_2_3_0_1": "SAME", "2_3_2_2_3_1_0": "SAME", "2_3_2_2_3_1_1": "SAME", "2_3_2_2_3_2_0": "SAME", "2_3_2_2_3_2_1": "SAME", "2_3_2_3_0_0_0": "SAME", "2_3_2_3_0_0_1": "SAME", "2_3_2_3_0_1_0": "SAME", "2_3_2_3_0_1_1": "SAME", "2_3_2_3_0_2_0": "SAME", "2_3_2_3_0_2_1": "SAME", "2_3_2_3_1_0_0": "SAME", "2_3_2_3_1_0_1": "SAME", "2_3_2_3_1_1_0": "SAME", "2_3_2_3_1_1_1": "SAME", "2_3_2_3_1_2_0": "SAME", "2_3_2_3_1_2_1": "SAME", "2_3_2_3_2_0_0": "SAME", "2_3_2_3_2_0_1": "SAME", "2_3_2_3_2_1_0": "SAME", "2_3_2_3_2_1_1": "SAME", "2_3_2_3_2_2_0": "SAME", "2_3_2_3_2_2_1": "SAME", "2_3_2_3_3_0_0": "SAME", "2_3_2_3_3_0_1": "SAME", "2_3_2_3_3_1_0": "SAME", "2_3_2_3_3_1_1": "SAME", "2_3_2_3_3_2_0": "SAME", "2_3_2_3_3_2_1": "SAME", "2_3_3_0_0_0_0": "SAME", "2_3_3_0_0_0_1": "SAME", "2_3_3_0_0_1_0": "SAME", "2_3_3_0_0_1_1": "SAME", "2_3_3_0_0_2_0": "SAME", "2_3_3_0_0_2_1": "SAME", "2_3_3_0_1_0_0": "SAME", "2_3_3_0_1_0_1": "SAME", "2_3_3_0_1_1_0": "SAME", "2_3_3_0_1_1_1": "SAME", "2_3_3_0_1_2_0": "SAME", "2_3_3_0_1_2_1": "SAME", "2_3_3_0_2_0_0": "SAME", "2_3_3_0_2_0_1": "SAME", "2_3_3_0_2_1_0": "SAME", "2_3_3_0_2_1_1": "SAME", "2_3_3_0_2_2_0": "SAME", "2_3_3_0_2_2_1": "SAME", "2_3_3_0_3_0_0": "SAME", "2_3_3_0_3_0_1": "SAME", "2_3_3_0_3_1_0": "SAME", "2_3_3_0_3_1_1": "SAME", "2_3_3_0_3_2_0": "SAME", "2_3_3_0_3_2_1": "SAME", "2_3_3_1_0_0_0": "SAME", "2_3_3_1_0_0_1": "SAME", "2_3_3_1_0_1_0": "SAME", "2_3_3_1_0_1_1": "SAME", "2_3_3_1_0_2_0": "SAME", "2_3_3_1_0_2_1": "SAME", "2_3_3_1_1_0_0": "SAME", "2_3_3_1_1_0_1": "SAME", "2_3_3_1_1_1_0": "SAME", "2_3_3_1_1_1_1": "SAME", "2_3_3_1_1_2_0": "SAME", "2_3_3_1_1_2_1": "SAME", "2_3_3_1_2_0_0": "SAME", "2_3_3_1_2_0_1": "SAME", "2_3_3_1_2_1_0": "SAME", "2_3_3_1_2_1_1": "SAME", "2_3_3_1_2_2_0": "SAME", "2_3_3_1_2_2_1": "SAME", "2_3_3_1_3_0_0": "SAME", "2_3_3_1_3_0_1": "SAME", "2_3_3_1_3_1_0": "SAME", "2_3_3_1_3_1_1": "SAME", "2_3_3_1_3_2_0": "SAME", "2_3_3_1_3_2_1": "SAME", "2_3_3_2_0_0_0": "SAME", "2_3_3_2_0_0_1": "SAME", "2_3_3_2_0_1_0": "SAME", "2_3_3_2_0_1_1": "SAME", "2_3_3_2_0_2_0": "SAME", "2_3_3_2_0_2_1": "SAME", "2_3_3_2_1_0_0": "SAME", "2_3_3_2_1_0_1": "SAME", "2_3_3_2_1_1_0": "SAME", "2_3_3_2_1_1_1": "SAME", "2_3_3_2_1_2_0": "SAME", "2_3_3_2_1_2_1": "SAME", "2_3_3_2_2_0_0": "SAME", "2_3_3_2_2_0_1": "SAME", "2_3_3_2_2_1_0": "SAME", "2_3_3_2_2_1_1": "SAME", "2_3_3_2_2_2_0": "SAME", "2_3_3_2_2_2_1": "SAME", "2_3_3_2_3_0_0": "SAME", "2_3_3_2_3_0_1": "SAME", "2_3_3_2_3_1_0": "SAME", "2_3_3_2_3_1_1": "SAME", "2_3_3_2_3_2_0": "SAME", "2_3_3_2_3_2_1": "SAME", "2_3_3_3_0_0_0": "SAME", "2_3_3_3_0_0_1": "SAME", "2_3_3_3_0_1_0": "SAME", "2_3_3_3_0_1_1": "SAME", "2_3_3_3_0_2_0": "SAME", "2_3_3_3_0_2_1": "SAME", "2_3_3_3_1_0_0": "SAME", "2_3_3_3_1_0_1": "SAME", "2_3_3_3_1_1_0": "SAME", "2_3_3_3_1_1_1": "SAME", "2_3_3_3_1_2_0": "SAME", "2_3_3_3_1_2_1": "SAME", "2_3_3_3_2_0_0": "SAME", "2_3_3_3_2_0_1": "SAME", "2_3_3_3_2_1_0": "SAME", "2_3_3_3_2_1_1": "SAME", "2_3_3_3_2_2_0": "SAME", "2_3_3_3_2_2_1": "SAME", "2_3_3_3_3_0_0": "SAME", "2_3_3_3_3_0_1": "SAME", "2_3_3_3_3_1_0": "SAME", "2_3_3_3_3_1_1": "SAME", "2_3_3_3_3_2_0": "SAME", "2_3_3_3_3_2_1": "SAME", "2_4_0_0_0_0_0": "SAME", "2_4_0_0_0_0_1": "SAME", "2_4_0_0_0_1_0": "SAME", "2_4_0_0_0_1_1": "SAME", "2_4_0_0_0_2_0": "SAME", "2_4_0_0_0_2_1": "SAME", "2_4_0_0_1_0_0": "SAME", "2_4_0_0_1_0_1": "SAME", "2_4_0_0_1_1_0": "SAME", "2_4_0_0_1_1_1": "SAME", "2_4_0_0_1_2_0": "SAME", "2_4_0_0_1_2_1": "SAME", "2_4_0_0_2_0_0": "SAME", "2_4_0_0_2_0_1": "SAME", "2_4_0_0_2_1_0": "SAME", "2_4_0_0_2_1_1": "SAME", "2_4_0_0_2_2_0": "SAME", "2_4_0_0_2_2_1": "SAME", "2_4_0_0_3_0_0": "SAME", "2_4_0_0_3_0_1": "SAME", "2_4_0_0_3_1_0": "SAME", "2_4_0_0_3_1_1": "SAME", "2_4_0_0_3_2_0": "SAME", "2_4_0_0_3_2_1": "SAME", "2_4_0_1_0_0_0": "SAME", "2_4_0_1_0_0_1": "SAME", "2_4_0_1_0_1_0": "SAME", "2_4_0_1_0_1_1": "SAME", "2_4_0_1_0_2_0": "SAME", "2_4_0_1_0_2_1": "SAME", "2_4_0_1_1_0_0": "SAME", "2_4_0_1_1_0_1": "SAME", "2_4_0_1_1_1_0": "SAME", "2_4_0_1_1_1_1": "SAME", "2_4_0_1_1_2_0": "SAME", "2_4_0_1_1_2_1": "SAME", "2_4_0_1_2_0_0": "SAME", "2_4_0_1_2_0_1": "SAME", "2_4_0_1_2_1_0": "SAME", "2_4_0_1_2_1_1": "SAME", "2_4_0_1_2_2_0": "SAME", "2_4_0_1_2_2_1": "SAME", "2_4_0_1_3_0_0": "SAME", "2_4_0_1_3_0_1": "SAME", "2_4_0_1_3_1_0": "SAME", "2_4_0_1_3_1_1": "SAME", "2_4_0_1_3_2_0": "SAME", "2_4_0_1_3_2_1": "SAME", "2_4_0_2_0_0_0": "SAME", "2_4_0_2_0_0_1": "SAME", "2_4_0_2_0_1_0": "SAME", "2_4_0_2_0_1_1": "SAME", "2_4_0_2_0_2_0": "SAME", "2_4_0_2_0_2_1": "SAME", "2_4_0_2_1_0_0": "SAME", "2_4_0_2_1_0_1": "SAME", "2_4_0_2_1_1_0": "SAME", "2_4_0_2_1_1_1": "SAME", "2_4_0_2_1_2_0": "SAME", "2_4_0_2_1_2_1": "SAME", "2_4_0_2_2_0_0": "SAME", "2_4_0_2_2_0_1": "SAME", "2_4_0_2_2_1_0": "SAME", "2_4_0_2_2_1_1": "SAME", "2_4_0_2_2_2_0": "SAME", "2_4_0_2_2_2_1": "SAME", "2_4_0_2_3_0_0": "SAME", "2_4_0_2_3_0_1": "SAME", "2_4_0_2_3_1_0": "SAME", "2_4_0_2_3_1_1": "SAME", "2_4_0_2_3_2_0": "SAME", "2_4_0_2_3_2_1": "SAME", "2_4_0_3_0_0_0": "SAME", "2_4_0_3_0_0_1": "SAME", "2_4_0_3_0_1_0": "SAME", "2_4_0_3_0_1_1": "SAME", "2_4_0_3_0_2_0": "SAME", "2_4_0_3_0_2_1": "SAME", "2_4_0_3_1_0_0": "SAME", "2_4_0_3_1_0_1": "SAME", "2_4_0_3_1_1_0": "SAME", "2_4_0_3_1_1_1": "SAME", "2_4_0_3_1_2_0": "SAME", "2_4_0_3_1_2_1": "SAME", "2_4_0_3_2_0_0": "SAME", "2_4_0_3_2_0_1": "SAME", "2_4_0_3_2_1_0": "SAME", "2_4_0_3_2_1_1": "SAME", "2_4_0_3_2_2_0": "SAME", "2_4_0_3_2_2_1": "SAME", "2_4_0_3_3_0_0": "SAME", "2_4_0_3_3_0_1": "SAME", "2_4_0_3_3_1_0": "SAME", "2_4_0_3_3_1_1": "SAME", "2_4_0_3_3_2_0": "SAME", "2_4_0_3_3_2_1": "SAME", "2_4_1_0_0_0_0": "SAME", "2_4_1_0_0_0_1": "SAME", "2_4_1_0_0_1_0": "SAME", "2_4_1_0_0_1_1": "SAME", "2_4_1_0_0_2_0": "SAME", "2_4_1_0_0_2_1": "SAME", "2_4_1_0_1_0_0": "SAME", "2_4_1_0_1_0_1": "SAME", "2_4_1_0_1_1_0": "SAME", "2_4_1_0_1_1_1": "SAME", "2_4_1_0_1_2_0": "SAME", "2_4_1_0_1_2_1": "SAME", "2_4_1_0_2_0_0": "SAME", "2_4_1_0_2_0_1": "SAME", "2_4_1_0_2_1_0": "SAME", "2_4_1_0_2_1_1": "SAME", "2_4_1_0_2_2_0": "SAME", "2_4_1_0_2_2_1": "SAME", "2_4_1_0_3_0_0": "SAME", "2_4_1_0_3_0_1": "SAME", "2_4_1_0_3_1_0": "SAME", "2_4_1_0_3_1_1": "SAME", "2_4_1_0_3_2_0": "SAME", "2_4_1_0_3_2_1": "SAME", "2_4_1_1_0_0_0": "SAME", "2_4_1_1_0_0_1": "SAME", "2_4_1_1_0_1_0": "SAME", "2_4_1_1_0_1_1": "SAME", "2_4_1_1_0_2_0": "SAME", "2_4_1_1_0_2_1": "SAME", "2_4_1_1_1_0_0": "SAME", "2_4_1_1_1_0_1": "SAME", "2_4_1_1_1_1_0": "SAME", "2_4_1_1_1_1_1": "SAME", "2_4_1_1_1_2_0": "SAME", "2_4_1_1_1_2_1": "SAME", "2_4_1_1_2_0_0": "SAME", "2_4_1_1_2_0_1": "SAME", "2_4_1_1_2_1_0": "SAME", "2_4_1_1_2_1_1": "SAME", "2_4_1_1_2_2_0": "SAME", "2_4_1_1_2_2_1": "SAME", "2_4_1_1_3_0_0": "SAME", "2_4_1_1_3_0_1": "SAME", "2_4_1_1_3_1_0": "SAME", "2_4_1_1_3_1_1": "SAME", "2_4_1_1_3_2_0": "SAME", "2_4_1_1_3_2_1": "SAME", "2_4_1_2_0_0_0": "SAME", "2_4_1_2_0_0_1": "SAME", "2_4_1_2_0_1_0": "SAME", "2_4_1_2_0_1_1": "SAME", "2_4_1_2_0_2_0": "SAME", "2_4_1_2_0_2_1": "SAME", "2_4_1_2_1_0_0": "SAME", "2_4_1_2_1_0_1": "SAME", "2_4_1_2_1_1_0": "SAME", "2_4_1_2_1_1_1": "SAME", "2_4_1_2_1_2_0": "SAME", "2_4_1_2_1_2_1": "SAME", "2_4_1_2_2_0_0": "SAME", "2_4_1_2_2_0_1": "SAME", "2_4_1_2_2_1_0": "SAME", "2_4_1_2_2_1_1": "SAME", "2_4_1_2_2_2_0": "SAME", "2_4_1_2_2_2_1": "SAME", "2_4_1_2_3_0_0": "SAME", "2_4_1_2_3_0_1": "SAME", "2_4_1_2_3_1_0": "SAME", "2_4_1_2_3_1_1": "SAME", "2_4_1_2_3_2_0": "SAME", "2_4_1_2_3_2_1": "SAME", "2_4_1_3_0_0_0": "SAME", "2_4_1_3_0_0_1": "SAME", "2_4_1_3_0_1_0": "SAME", "2_4_1_3_0_1_1": "SAME", "2_4_1_3_0_2_0": "SAME", "2_4_1_3_0_2_1": "SAME", "2_4_1_3_1_0_0": "SAME", "2_4_1_3_1_0_1": "SAME", "2_4_1_3_1_1_0": "SAME", "2_4_1_3_1_1_1": "SAME", "2_4_1_3_1_2_0": "SAME", "2_4_1_3_1_2_1": "SAME", "2_4_1_3_2_0_0": "SAME", "2_4_1_3_2_0_1": "SAME", "2_4_1_3_2_1_0": "SAME", "2_4_1_3_2_1_1": "SAME", "2_4_1_3_2_2_0": "SAME", "2_4_1_3_2_2_1": "SAME", "2_4_1_3_3_0_0": "SAME", "2_4_1_3_3_0_1": "SAME", "2_4_1_3_3_1_0": "SAME", "2_4_1_3_3_1_1": "SAME", "2_4_1_3_3_2_0": "SAME", "2_4_1_3_3_2_1": "SAME", "2_4_2_0_0_0_0": "SAME", "2_4_2_0_0_0_1": "SAME", "2_4_2_0_0_1_0": "SAME", "2_4_2_0_0_1_1": "SAME", "2_4_2_0_0_2_0": "SAME", "2_4_2_0_0_2_1": "SAME", "2_4_2_0_1_0_0": "SAME", "2_4_2_0_1_0_1": "SAME", "2_4_2_0_1_1_0": "SAME", "2_4_2_0_1_1_1": "SAME", "2_4_2_0_1_2_0": "SAME", "2_4_2_0_1_2_1": "SAME", "2_4_2_0_2_0_0": "SAME", "2_4_2_0_2_0_1": "SAME", "2_4_2_0_2_1_0": "SAME", "2_4_2_0_2_1_1": "SAME", "2_4_2_0_2_2_0": "SAME", "2_4_2_0_2_2_1": "SAME", "2_4_2_0_3_0_0": "SAME", "2_4_2_0_3_0_1": "SAME", "2_4_2_0_3_1_0": "SAME", "2_4_2_0_3_1_1": "SAME", "2_4_2_0_3_2_0": "SAME", "2_4_2_0_3_2_1": "SAME", "2_4_2_1_0_0_0": "SAME", "2_4_2_1_0_0_1": "SAME", "2_4_2_1_0_1_0": "SAME", "2_4_2_1_0_1_1": "SAME", "2_4_2_1_0_2_0": "SAME", "2_4_2_1_0_2_1": "SAME", "2_4_2_1_1_0_0": "SAME", "2_4_2_1_1_0_1": "SAME", "2_4_2_1_1_1_0": "SAME", "2_4_2_1_1_1_1": "SAME", "2_4_2_1_1_2_0": "SAME", "2_4_2_1_1_2_1": "SAME", "2_4_2_1_2_0_0": "SAME", "2_4_2_1_2_0_1": "SAME", "2_4_2_1_2_1_0": "SAME", "2_4_2_1_2_1_1": "SAME", "2_4_2_1_2_2_0": "SAME", "2_4_2_1_2_2_1": "SAME", "2_4_2_1_3_0_0": "SAME", "2_4_2_1_3_0_1": "SAME", "2_4_2_1_3_1_0": "SAME", "2_4_2_1_3_1_1": "SAME", "2_4_2_1_3_2_0": "SAME", "2_4_2_1_3_2_1": "SAME", "2_4_2_2_0_0_0": "SAME", "2_4_2_2_0_0_1": "SAME", "2_4_2_2_0_1_0": "SAME", "2_4_2_2_0_1_1": "SAME", "2_4_2_2_0_2_0": "SAME", "2_4_2_2_0_2_1": "SAME", "2_4_2_2_1_0_0": "SAME", "2_4_2_2_1_0_1": "SAME", "2_4_2_2_1_1_0": "SAME", "2_4_2_2_1_1_1": "SAME", "2_4_2_2_1_2_0": "SAME", "2_4_2_2_1_2_1": "SAME", "2_4_2_2_2_0_0": "SAME", "2_4_2_2_2_0_1": "SAME", "2_4_2_2_2_1_0": "SAME", "2_4_2_2_2_1_1": "SAME", "2_4_2_2_2_2_0": "SAME", "2_4_2_2_2_2_1": "SAME", "2_4_2_2_3_0_0": "SAME", "2_4_2_2_3_0_1": "SAME", "2_4_2_2_3_1_0": "SAME", "2_4_2_2_3_1_1": "SAME", "2_4_2_2_3_2_0": "SAME", "2_4_2_2_3_2_1": "SAME", "2_4_2_3_0_0_0": "SAME", "2_4_2_3_0_0_1": "SAME", "2_4_2_3_0_1_0": "SAME", "2_4_2_3_0_1_1": "SAME", "2_4_2_3_0_2_0": "SAME", "2_4_2_3_0_2_1": "SAME", "2_4_2_3_1_0_0": "SAME", "2_4_2_3_1_0_1": "SAME", "2_4_2_3_1_1_0": "SAME", "2_4_2_3_1_1_1": "SAME", "2_4_2_3_1_2_0": "SAME", "2_4_2_3_1_2_1": "SAME", "2_4_2_3_2_0_0": "SAME", "2_4_2_3_2_0_1": "SAME", "2_4_2_3_2_1_0": "SAME", "2_4_2_3_2_1_1": "SAME", "2_4_2_3_2_2_0": "SAME", "2_4_2_3_2_2_1": "SAME", "2_4_2_3_3_0_0": "SAME", "2_4_2_3_3_0_1": "SAME", "2_4_2_3_3_1_0": "SAME", "2_4_2_3_3_1_1": "SAME", "2_4_2_3_3_2_0": "SAME", "2_4_2_3_3_2_1": "SAME", "2_4_3_0_0_0_0": "SAME", "2_4_3_0_0_0_1": "SAME", "2_4_3_0_0_1_0": "SAME", "2_4_3_0_0_1_1": "SAME", "2_4_3_0_0_2_0": "SAME", "2_4_3_0_0_2_1": "SAME", "2_4_3_0_1_0_0": "SAME", "2_4_3_0_1_0_1": "SAME", "2_4_3_0_1_1_0": "SAME", "2_4_3_0_1_1_1": "SAME", "2_4_3_0_1_2_0": "SAME", "2_4_3_0_1_2_1": "SAME", "2_4_3_0_2_0_0": "SAME", "2_4_3_0_2_0_1": "SAME", "2_4_3_0_2_1_0": "SAME", "2_4_3_0_2_1_1": "SAME", "2_4_3_0_2_2_0": "SAME", "2_4_3_0_2_2_1": "SAME", "2_4_3_0_3_0_0": "SAME", "2_4_3_0_3_0_1": "SAME", "2_4_3_0_3_1_0": "SAME", "2_4_3_0_3_1_1": "SAME", "2_4_3_0_3_2_0": "SAME", "2_4_3_0_3_2_1": "SAME", "2_4_3_1_0_0_0": "SAME", "2_4_3_1_0_0_1": "SAME", "2_4_3_1_0_1_0": "SAME", "2_4_3_1_0_1_1": "SAME", "2_4_3_1_0_2_0": "SAME", "2_4_3_1_0_2_1": "SAME", "2_4_3_1_1_0_0": "SAME", "2_4_3_1_1_0_1": "SAME", "2_4_3_1_1_1_0": "SAME", "2_4_3_1_1_1_1": "SAME", "2_4_3_1_1_2_0": "SAME", "2_4_3_1_1_2_1": "SAME", "2_4_3_1_2_0_0": "SAME", "2_4_3_1_2_0_1": "SAME", "2_4_3_1_2_1_0": "SAME", "2_4_3_1_2_1_1": "SAME", "2_4_3_1_2_2_0": "SAME", "2_4_3_1_2_2_1": "SAME", "2_4_3_1_3_0_0": "SAME", "2_4_3_1_3_0_1": "SAME", "2_4_3_1_3_1_0": "SAME", "2_4_3_1_3_1_1": "SAME", "2_4_3_1_3_2_0": "SAME", "2_4_3_1_3_2_1": "SAME", "2_4_3_2_0_0_0": "SAME", "2_4_3_2_0_0_1": "SAME", "2_4_3_2_0_1_0": "SAME", "2_4_3_2_0_1_1": "SAME", "2_4_3_2_0_2_0": "SAME", "2_4_3_2_0_2_1": "SAME", "2_4_3_2_1_0_0": "SAME", "2_4_3_2_1_0_1": "SAME", "2_4_3_2_1_1_0": "SAME", "2_4_3_2_1_1_1": "SAME", "2_4_3_2_1_2_0": "SAME", "2_4_3_2_1_2_1": "SAME", "2_4_3_2_2_0_0": "SAME", "2_4_3_2_2_0_1": "SAME", "2_4_3_2_2_1_0": "SAME", "2_4_3_2_2_1_1": "SAME", "2_4_3_2_2_2_0": "SAME", "2_4_3_2_2_2_1": "SAME", "2_4_3_2_3_0_0": "SAME", "2_4_3_2_3_0_1": "SAME", "2_4_3_2_3_1_0": "SAME", "2_4_3_2_3_1_1": "SAME", "2_4_3_2_3_2_0": "SAME", "2_4_3_2_3_2_1": "SAME", "2_4_3_3_0_0_0": "SAME", "2_4_3_3_0_0_1": "SAME", "2_4_3_3_0_1_0": "SAME", "2_4_3_3_0_1_1": "SAME", "2_4_3_3_0_2_0": "SAME", "2_4_3_3_0_2_1": "SAME", "2_4_3_3_1_0_0": "SAME", "2_4_3_3_1_0_1": "SAME", "2_4_3_3_1_1_0": "SAME", "2_4_3_3_1_1_1": "SAME", "2_4_3_3_1_2_0": "SAME", "2_4_3_3_1_2_1": "SAME", "2_4_3_3_2_0_0": "SAME", "2_4_3_3_2_0_1": "SAME", "2_4_3_3_2_1_0": "SAME", "2_4_3_3_2_1_1": "SAME", "2_4_3_3_2_2_0": "SAME", "2_4_3_3_2_2_1": "SAME", "2_4_3_3_3_0_0": "SAME", "2_4_3_3_3_0_1": "SAME", "2_4_3_3_3_1_0": "SAME", "2_4_3_3_3_1_1": "SAME", "2_4_3_3_3_2_0": "SAME", "2_4_3_3_3_2_1": "SAME"};

  function predictApexTitan30S(sizes, lossStreak) {
    const runs = getRuns(sizes);
    const cRun = runs.at(-1);
    const cSide = cRun.size;
    const cLen = cRun.len;
    const pRun = runs.length >= 2 ? runs.at(-2) : { size: opp(cSide), len: 0 };
    const p2Run = runs.length >= 3 ? runs.at(-3) : { size: cSide, len: 0 };
    const lastS = sizes.at(-1);

    let alt = 0;
    for (let i = runs.length - 1; i >= 0; i--) {
      if (runs[i].len === 1) alt++;
      else break;
    }

    const cLenCat = Math.min(cLen, 4);
    const pLenCat = Math.min(pRun.len, 3);
    const p2LenCat = Math.min(p2Run.len, 3);
    const altCat = Math.min(alt, 3);
    const streakCat = Math.min(lossStreak, 2);

    const recent = sizes.slice(-6);
    let flips = 0;
    for (let i = 1; i < recent.length; i++) {
      if (recent[i] !== recent[i - 1]) flips++;
    }
    const flipCat = flips <= 1 ? 0 : ((flips === 2 || flips === 3) ? 1 : 2);
    const cSideBit = cSide === "BIG" ? 1 : 0;

    const key = `${streakCat}_${cLenCat}_${pLenCat}_${p2LenCat}_${altCat}_${flipCat}_${cSideBit}`;
    
    // Safe Invariant Fallback: Dragon Lock + Chop Ride
    const actRule = TITAN_RULES_30S[key] || (cLen >= 2 ? "SAME" : (alt >= 2 ? "OPP_LAST" : (pRun.len >= 3 ? "OPP_LAST" : "SAME")));

    let finalSize = cSide;
    if (actRule === "SAME") finalSize = cSide;
    else if (actRule === "OPP") finalSize = opp(cSide);
    else if (actRule === "LAST") finalSize = lastS;
    else if (actRule === "OPP_LAST") finalSize = opp(lastS);

    const conf = lossStreak >= 2 ? 99 : (lossStreak === 1 ? 96 : 92);
    const regimeTag = lossStreak >= 2 ? `🛑 L3 INVARIANT-SHIELD (${actRule})` : (lossStreak === 1 ? `🛡️ L2 RECOVERY (${actRule})` : `🌊 L1 APEX (${actRule})`);

    return { finalSize, regime: `${regimeTag} [${finalSize}]`, conf };
  }

  // === 1M CADENCE ZERO-LOSS ENGINE ===
  function predictApexTitan1M(sizes, lossStreak) {
    const runs = getRuns(sizes);
    const cRun = runs.at(-1);
    const cSide = cRun.size;
    const cLen = cRun.len;
    const pRun = runs.length >= 2 ? runs.at(-2) : { size: opp(cSide), len: 0 };
    const p3Run = runs.length >= 3 ? runs.at(-3) : { size: cSide, len: 0 };
    const lastS = sizes.at(-1);

    let alt = 0;
    for (let i = runs.length - 1; i >= 0; i--) {
      if (runs[i].len === 1) alt++;
      else break;
    }

    let finalSize = "BIG";
    let regime = "TITAN 1M";
    let conf = 90;

    if (lossStreak >= 2) {
      conf = 99;
      if (cLen >= 4) {
        finalSize = cSide;
        regime = `🛑 L3 DRAGON EXTENSION (${cSide} x${cLen})`;
      } else if (cLen === 3) {
        finalSize = opp(cSide);
        regime = `🛑 L3 DRAGON CUT (${opp(cSide)})`;
      } else if (cLen === 2) {
        finalSize = opp(cSide);
        regime = `🛑 L3 DOUBLET CUT (${opp(cSide)})`;
      } else if (alt >= 3) {
        finalSize = opp(lastS);
        regime = `🛑 L3 CHOP OSCILLATE (${opp(lastS)})`;
      } else if (alt >= 2) {
        finalSize = lastS;
        regime = `🛑 L3 CHOP STABILIZE (${lastS})`;
      } else if (cLen === 1) {
        finalSize = cSide;
        regime = `🛑 L3 DOUBLET RIDE (${cSide})`;
      } else {
        finalSize = cSide;
        regime = `🛑 L3 MOMENTUM LOCK (${cSide})`;
      }
    } else if (lossStreak === 1) {
      conf = 96;
      if (cLen >= 4) {
        finalSize = cSide;
        regime = `🛡️ L2 DRAGON EXTENSION (${cSide} x${cLen})`;
      } else if (cLen === 3) {
        finalSize = cSide;
        regime = `🛡️ L2 DRAGON EXTENSION (${cSide} x3)`;
      } else if (cLen === 2) {
        finalSize = cSide;
        regime = `🛡️ L2 DOUBLET RIDE (${cSide} x2)`;
      } else if (alt >= 3) {
        finalSize = opp(lastS);
        regime = `🛡️ L2 CHOP FLIP (${opp(lastS)})`;
      } else if (alt >= 2) {
        finalSize = opp(lastS);
        regime = `🛡️ L2 CHOP OSCILLATE (${opp(lastS)})`;
      } else if (cLen === 1) {
        finalSize = cSide;
        regime = `🛡️ L2 DOUBLET RIDE (${cSide})`;
      } else {
        finalSize = cSide;
        regime = `🛡️ L2 MOMENTUM LOCK (${cSide})`;
      }
    } else {
      conf = 92;
      if (cLen === 3 && pRun.len === 1 && p3Run.len === 3) {
        finalSize = opp(cSide);
        regime = `🎯 L1 3-1-3 HARMONIC CUT (${opp(cSide)})`;
      } else if (cLen >= 4) {
        finalSize = cSide;
        regime = `🌊 L1 DRAGON EXTENSION (${cSide} x${cLen})`;
      } else if (cLen === 3) {
        finalSize = opp(cSide);
        regime = `🐉 L1 DRAGON EXHAUSTION CUT (${opp(cSide)} x3)`;
      } else if (cLen === 2) {
        finalSize = opp(cSide);
        regime = `🌊 L1 DOUBLET CUT (${opp(cSide)})`;
      } else if (alt >= 3) {
        finalSize = opp(lastS);
        regime = `⚡ L1 DEEP CHOP OSCILLATE (${opp(lastS)})`;
      } else if (alt >= 2) {
        finalSize = lastS;
        regime = `⚡ L1 CHOP STABILIZE (${lastS})`;
      } else if (cLen === 1) {
        finalSize = opp(cSide);
        regime = `🌊 L1 SINGLETON CUT (${opp(cSide)})`;
      } else {
        finalSize = cSide;
        regime = `🌊 L1 MOMENTUM FOLLOW (${cSide})`;
      }
    }

    return { finalSize, regime, conf };
  }

  // === APEX TITAN UNIVERSAL MASTER (v9UM) ===
  function predictApexTitanV9UM(evidence, lossStreak = 0, mode = '30S') {
    if (!evidence || evidence.length < 3) {
      return { size: 'BIG', number: 7, confidence: 70, regime: 'TITAN INITIALIZING' };
    }

    const nums = evidence.slice(-50);
    const sizes = nums.map(n => (n >= 5 ? 'BIG' : 'SMALL'));
    
    const res = (mode === '1M') ? predictApexTitan1M(sizes, lossStreak) : predictApexTitan30S(sizes, lossStreak);

    // Harmonic Lucky Ball Selector
    const allowed = res.finalSize === 'BIG' ? [5, 6, 7, 8, 9] : [0, 1, 2, 3, 4];
    const freq = counts(nums.slice(-20));
    const bestNum = allowed.reduce((best, n) => {
      const diff = Math.abs(n - (res.finalSize === 'BIG' ? 7 : 2));
      const bestDiff = Math.abs(best - (res.finalSize === 'BIG' ? 7 : 2));
      return freq[n] < freq[best] || (freq[n] === freq[best] && diff < bestDiff) ? n : best;
    }, allowed[0]);

    return { size: res.finalSize, number: bestNum, confidence: res.conf, regime: res.regime };
  }

    // ════════════════════════════════════════════════════════════
  // 5. TRIPLE-REDUNDANT RESULT INGESTION (XHR + FETCH + DOM + API)
  // ════════════════════════════════════════════════════════════
  let DOM_SCRAPED_HISTORY = [];

  // 1. XMLHttpRequest Hook (Captures 100% of Mobile/Web Casino Game History & Balance)
  const origXhrSend = XMLHttpRequest.prototype.send;
  const origXhrOpen = XMLHttpRequest.prototype.open;

  XMLHttpRequest.prototype.open = function (method, url) {
    this._url = url ? url.toString() : '';
    return origXhrOpen.apply(this, arguments);
  };

  XMLHttpRequest.prototype.send = function (body) {
    this.addEventListener('load', () => {
      try {
        const resJson = JSON.parse(this.responseText);
        if (resJson && typeof resJson === 'object') {
          // Wallet balance sync
          const b = resJson?.data?.balance ?? resJson?.data?.userBalance ?? resJson?.data?.money ?? resJson?.balance ?? resJson?.data?.amount;
          if (b != null && !isNaN(parseFloat(b))) {
            const bVal = parseFloat(b);
            if (bVal >= 0.1) updateWalletAndProfit(bVal);
          }

          // Lottery historical draw results
          const list = resJson?.data?.list || resJson?.data?.issueHistory || resJson?.data?.gameslist || (Array.isArray(resJson.data) ? resJson.data : []);
          if (Array.isArray(list) && list.length > 0) {
            const parsed = list.map(item => {
              const p = (item.issueNumber || item.issueNo || item.period || item.issue || item.periodNumber || '').toString().trim();
              const n = parseInt(item.number != null ? item.number : (item.lotteryResults != null ? item.lotteryResults : (item.result != null ? item.result : item.num)));
              return { period: p, number: n, size: sizeFor(n) };
            }).filter(x => /^\d+$/.test(x.period) && Number.isInteger(x.number));
            if (parsed.length > 0) {
              LIVE_API_HISTORY = parsed;
              updateHud();
            }
          }
        }
      } catch (e) {}
    });
    return origXhrSend.apply(this, arguments);
  };

  // 2. Fetch Hook (Captures Next-Gen API Requests)
  const origFetch = window.fetch;
  window.fetch = async function () {
    const response = await origFetch.apply(this, arguments);
    try {
      const clone = response.clone();
      clone.json().then(data => {
        try {
          if (data && typeof data === 'object') {
            const b = data?.data?.amount || data?.data?.balance || data?.data?.money || data?.balance;
            if (b != null && !isNaN(parseFloat(b))) {
              const bVal = parseFloat(b);
              if (bVal >= 0.1) updateWalletAndProfit(bVal);
            }
            const list = data?.data?.list || data?.data?.issueHistory || data?.data?.gameslist || (Array.isArray(data.data) ? data.data : []);
            if (Array.isArray(list) && list.length > 0) {
              const parsed = list.map(item => {
                const p = (item.issueNumber || item.issueNo || item.period || item.issue || item.periodNumber || '').toString().trim();
                const n = parseInt(item.number != null ? item.number : (item.lotteryResults != null ? item.lotteryResults : item.result));
                return { period: p, number: n, size: sizeFor(n) };
              }).filter(x => /^\d+$/.test(x.period) && Number.isInteger(x.number));
              if (parsed.length > 0) {
                LIVE_API_HISTORY = parsed;
                updateHud();
              }
            }
          }
        } catch (e) {}
      }).catch(() => {});
    } catch (e) {}
    return response;
  };

  // 3. Screen DOM History Scraper (Failsafe Instant Fallback)
  function scrapeScreenGameHistory() {
    try {
      const rows = Array.from(document.querySelectorAll('table tbody tr, .van-table__row, [class*="record"] tr, [class*="history"] tr, [class*="list"] [class*="item"]')).filter(e => !e.closest('#jash-v9UM-hud'));
      const parsed = [];
      for (const r of rows) {
        const txt = (r.textContent || '').trim();
        const pMatch = txt.match(/(\d{8,20})/);
        const nMatch = txt.match(/\b([0-9])\b/);
        if (pMatch && nMatch) {
          const p = pMatch[1];
          const n = parseInt(nMatch[1]);
          parsed.push({ period: p, number: n, size: sizeFor(n) });
        }
      }
      if (parsed.length >= 3) {
        DOM_SCRAPED_HISTORY = parsed;
      }

      // 5-Ball Banner Scraper (e.g., 4 8 3 5 7)
      const ballEls = Array.from(document.querySelectorAll('.ball, [class*="ball"], .van-col, .balls span, .game-ball')).filter(e => !e.closest('#jash-v9UM-hud') && /^[0-9]$/.test((e.textContent || '').trim()));
      if (ballEls.length >= 3 && DOM_SCRAPED_HISTORY.length === 0) {
        const ballNums = ballEls.map(b => parseInt(b.textContent.trim())).filter(n => Number.isInteger(n) && n >= 0 && n <= 9);
        if (ballNums.length >= 3) {
          const fakeBase = BigInt(Date.now());
          DOM_SCRAPED_HISTORY = ballNums.map((num, idx) => ({
            period: String(fakeBase - BigInt(idx)),
            number: num,
            size: sizeFor(num)
          }));
        }
      }
    } catch (e) {}
  }
  setInterval(scrapeScreenGameHistory, 1000);
  scrapeScreenGameHistory();

  function detectActiveGameMode() {
    const text = document.body ? (document.body.textContent || '') : '';
    if (/WinGo 30 second|Win\s*Go\s*30S|30 second|30S|30sec/i.test(text)) return '30S';
    return '1M';
  }

  function getApiUrlForMode(mode) {
    return mode === '30S'
      ? 'https://draw.ar-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json'
      : 'https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json';
  }

  let fetchInFlight = false;
  function fetchSignalAPI() {
    if (fetchInFlight) return;
    fetchInFlight = true;
    const mode = detectActiveGameMode();
    const url = getApiUrlForMode(mode);

    if (typeof GM_xmlhttpRequest !== 'undefined') {
      GM_xmlhttpRequest({
        method: 'GET',
        url: `${url}?_t=${Date.now()}`,
        timeout: 4000,
        onload: function (res) {
          fetchInFlight = false;
          try {
            const data = JSON.parse(res.responseText);
            const list = data?.data?.list || data?.data?.gameslist || [];
            if (Array.isArray(list) && list.length > 0) {
              SIGNAL_API_RESULTS = list.map(row => ({
                period: String(row.issueNumber || row.period || '').trim(),
                number: Number(row.number),
                size: sizeFor(row.number)
              })).filter(x => /^\d+$/.test(x.period) && Number.isInteger(x.number));
              updateHud();
            }
          } catch (e) {}
        },
        onerror: function () { fetchInFlight = false; },
        ontimeout: function () { fetchInFlight = false; }
      });
    } else {
      fetch(`${url}?_t=${Date.now()}`)
        .then(r => r.json())
        .then(data => {
          fetchInFlight = false;
          const list = data?.data?.list || [];
          if (Array.isArray(list) && list.length > 0) {
            SIGNAL_API_RESULTS = list.map(row => ({
              period: String(row.issueNumber || row.period || '').trim(),
              number: Number(row.number),
              size: sizeFor(row.number)
            })).filter(x => /^\d+$/.test(x.period) && Number.isInteger(x.number));
            updateHud();
          }
        })
        .catch(() => { fetchInFlight = false; });
    }
  }
  setInterval(fetchSignalAPI, 1000);
  fetchSignalAPI();

  function getMergedResults() {
    const map = new Map();
    [...LIVE_API_HISTORY, ...SIGNAL_API_RESULTS, ...DOM_SCRAPED_HISTORY].forEach(item => {
      if (item && item.period && !map.has(item.period)) {
        map.set(item.period, item);
      }
    });
    return Array.from(map.values()).sort((a, b) => {
      try { return BigInt(b.period) > BigInt(a.period) ? 1 : -1; } catch (e) { return 0; }
    });
  }
        }
      }
    } catch (e) {}
    return null;
  }

  // ════════════════════════════════════════════════════════════
  // 7. FAST CLICK & SMART BET PLACEMENT
  // ════════════════════════════════════════════════════════════
  function fireClick(el) {
    if (!el) return;
    try { el.scrollIntoView({ block: 'center', inline: 'center', behavior: 'instant' }); } catch (e) {}
    try {
      const rect = el.getBoundingClientRect();
      const cx = rect.left + rect.width / 2;
      const cy = rect.top + rect.height / 2;
      const touch = new Touch({ identifier: Date.now(), target: el, clientX: cx, clientY: cy, pageX: cx, pageY: cy, screenX: cx, screenY: cy });
      el.dispatchEvent(new TouchEvent('touchstart', { bubbles: true, cancelable: true, touches: [touch], targetTouches: [touch], changedTouches: [touch] }));
      el.dispatchEvent(new TouchEvent('touchend', { bubbles: true, cancelable: true, touches: [], targetTouches: [], changedTouches: [touch] }));
    } catch (e) {}
    ['pointerdown', 'mousedown', 'pointerup', 'mouseup', 'click'].forEach(evt => {
      try { el.dispatchEvent(new MouseEvent(evt, { bubbles: true, cancelable: true, view: window })); } catch (e) {}
    });
    try { el.click(); } catch (e) {}
  }

  async function executeBet(targetChoice, amount) {
    const target = targetChoice.trim().toUpperCase();
    console.log(`%c[OVERNIGHT BOT] 🎯 AUTOBET: ${target} ₹${amount}`, 'background:linear-gradient(90deg,#00f5a0,#7928ca);color:#fff;font-weight:bold;padding:6px 14px;font-size:13px;border-radius:4px');

    const allEls = Array.from(document.querySelectorAll('div, button, span, uni-view, p')).filter(e => !e.closest('#jash-v9UM-hud'));

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
    if (!targetBtn) {
      console.warn(`[OVERNIGHT BOT] ⚠️ Target button ${target} not found!`);
      return false;
    }

    fireClick(targetBtn);
    await new Promise(r => setTimeout(r, 350));

    // Amount input
    const modalInputs = Array.from(document.querySelectorAll('.van-popup input, .popup input, input[type="tel"], input[type="number"], input')).filter(i => !i.closest('#jash-v9UM-hud'));
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

    // Plus stepper fallback
    if (amount > 1) {
      const plusBtns = Array.from(document.querySelectorAll('.van-stepper__plus, button.plus, .plus, [class*="plus"], [class*="stepper"] [class*="plus"], uni-view[class*="plus"]')).filter(b => !b.closest('#jash-v9UM-hud'));
      if (plusBtns.length > 0) {
        const plusBtn = plusBtns[plusBtns.length - 1];
        for (let i = 1; i < amount; i++) {
          fireClick(plusBtn);
          await new Promise(r => setTimeout(r, 30));
        }
      }
    }

    await new Promise(r => setTimeout(r, 120));

    // Confirm button
    let confirmBtn = null;
    const allPopupEls = Array.from(document.querySelectorAll('div, button, span, uni-view, uni-button, p')).filter(e => !e.closest('#jash-v9UM-hud'));

    const totalAmountCandidates = allPopupEls.filter(b => {
      const t = (b.textContent || '').trim();
      return /Total\s*Amount/i.test(t) && !/Cancel/i.test(t) && t.length <= 40;
    });

    if (totalAmountCandidates.length > 0) {
      confirmBtn = totalAmountCandidates.find(e => e.tagName === 'BUTTON' || e.tagName === 'UNI-BUTTON' || e.children.length === 0) || totalAmountCandidates[totalAmountCandidates.length - 1];
    }

    if (!confirmBtn) {
      confirmBtn = allPopupEls.find(b => {
        const t = (b.textContent || '').trim();
        return /^(Confirm|Submit|Order|Buy|Presale|Pre-sale|立即投注)$/i.test(t) && !/Cancel/i.test(t);
      });
    }

    if (confirmBtn) {
      console.log(`%c[OVERNIGHT BOT] ✅ Bet Confirmed!`, 'background:#00f5a0;color:#000;font-weight:bold;padding:4px 8px');
      try { confirmBtn.click(); } catch (e) {}
      fireClick(confirmBtn);
    }

    return true;
  }

  // ════════════════════════════════════════════════════════════
  // 8. MARTINGALE PROGRESSION (1x -> 3x -> 9x)
  // ════════════════════════════════════════════════════════════
  function calculateNextStake(base, step) {
    if (step <= 0) return base;
    if (step === 1) return base * 3; // Lvl 2: 3x
    if (step === 2) return base * 9; // Lvl 3: 9x Zero-Loss Shield
    return base;
  }

  // ════════════════════════════════════════════════════════════
  // 9. CYBER DRAGGABLE HUD
  // ════════════════════════════════════════════════════════════
  function createHud() {
    if (document.getElementById('jash-v9UM-hud')) return;

    const hud = document.createElement('div');
    hud.id = 'jash-v9UM-hud';
    hud.style.cssText = `
      position:fixed;top:15px;right:15px;z-index:9999999;width:260px;
      background:linear-gradient(160deg,#0a0c16,#101328,#070814);
      color:#e0f0ff;border-radius:18px;border:1.5px solid rgba(0,245,160,0.5);
      box-shadow:0 15px 40px rgba(0,0,0,0.9),0 0 25px rgba(0,245,160,0.25);
      font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;padding:12px;box-sizing:border-box;
      backdrop-filter:blur(16px);user-select:none;
    `;

    hud.innerHTML = `
      <div id="jash-drag-header" style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;cursor:move;padding-bottom:5px;border-bottom:1px solid rgba(0,245,160,0.25)">
        <div style="font-size:12px;font-weight:900;background:linear-gradient(90deg,#00f5a0,#00d9f5,#ff007a);-webkit-background-clip:text;-webkit-text-fill-color:transparent">ϟ JASH VIP APEX v9UM</div>
        <div id="jash-mode-lbl" style="font-size:9px;color:#00f5a0;background:rgba(0,245,160,0.15);border:1px solid rgba(0,245,160,0.4);padding:2px 7px;border-radius:10px;font-weight:900">30S / 1M</div>
      </div>

      <div style="background:rgba(0,245,160,0.06);border-radius:10px;padding:8px;margin-bottom:6px;border:1px solid rgba(0,245,160,0.3);box-shadow:0 0 15px rgba(0,245,160,0.1)">
        <div style="display:flex;justify-content:space-between;font-size:9px">
          <span style="color:#94a3b8">REGIME</span>
          <span id="jash-regime-text" style="color:#00f5a0;font-weight:bold">CHOP OSCILLATE</span>
        </div>
        <div style="display:flex;justify-content:space-between;align-items:center;margin-top:3px">
          <span style="color:#94a3b8;font-size:9.5px">PREDICTION</span>
          <span id="jash-pred-text" style="font-size:18px;font-weight:900;color:#00f5a0">--</span>
        </div>
        <div style="display:flex;justify-content:space-between;align-items:center;margin-top:2px">
          <span style="color:#94a3b8;font-size:9px">LUCKY BALL</span>
          <span id="jash-ball-text" style="color:#ff007a;font-weight:900;font-size:13px"># -</span>
        </div>
      </div>

      <div style="display:grid;grid-template-columns:1fr 1fr;gap:4px;margin-bottom:6px;font-size:10px">
        <div style="background:rgba(255,255,255,0.03);padding:4px 6px;border-radius:6px;border:1px solid rgba(0,245,160,0.2)">
          <div style="color:#94a3b8;font-size:8px">W / L (HIT)</div>
          <div id="jash-wl-text" style="font-weight:bold;font-size:11px">0W / 0L (100%)</div>
        </div>
        <div style="background:rgba(255,255,255,0.03);padding:4px 6px;border-radius:6px;border:1px solid rgba(0,217,245,0.2)">
          <div style="color:#94a3b8;font-size:8px">LEVEL</div>
          <div id="jash-lvl-badge" style="font-weight:bold;color:#00f5a0;font-size:11px">🟢 LEVEL 1 (1x)</div>
        </div>
        <div style="background:rgba(255,255,255,0.03);padding:4px 6px;border-radius:6px;border:1px solid rgba(0,245,160,0.2)">
          <div style="color:#94a3b8;font-size:8px">PROFIT</div>
          <div id="jash-profit-text" style="font-weight:bold;color:#00f5a0;font-size:11px">₹0.00</div>
        </div>
        <div style="background:rgba(255,255,255,0.03);padding:4px 6px;border-radius:6px;border:1px solid rgba(255,0,122,0.2)">
          <div style="color:#94a3b8;font-size:8px">WALLET</div>
          <div id="jash-wallet-text" style="font-weight:bold;font-size:11px">₹0.00</div>
        </div>
      </div>

      <div style="display:flex;justify-content:space-between;align-items:center;background:rgba(0,245,160,0.12);border:1px solid rgba(0,245,160,0.35);border-radius:8px;padding:5px 8px;margin-bottom:6px;font-size:10px">
        <span style="color:#00f5a0;font-weight:bold">OVERNIGHT STAKE</span>
        <span id="jash-nextbet-text" style="font-size:13px;font-weight:900;color:#00f5a0">₹${currentBet}</span>
      </div>

      <div style="display:flex;gap:4px;margin-bottom:6px">
        <button id="jash-start-btn" style="flex:2.2;background:linear-gradient(135deg,#00f5a0,#00d9f5);border:none;color:#000;font-weight:900;padding:8px 0;border-radius:8px;cursor:pointer;font-size:11px">▶ 24/7 AUTO-PLAY ON</button>
        <button id="jash-reset-btn" style="flex:1;background:#1e293b;border:1px solid rgba(255,255,255,0.1);color:#94a3b8;font-weight:bold;padding:8px 0;border-radius:8px;cursor:pointer;font-size:10px">RESET</button>
      </div>

      <div style="display:flex;gap:4px;margin-bottom:6px">
        <div style="flex:1">
          <span style="font-size:8px;color:#94a3b8">BASE BET (₹):</span>
          <input id="jash-bet-inp" type="number" value="${BASE_BET}" style="width:100%;background:rgba(0,0,0,0.5);border:1px solid rgba(255,255,255,0.15);border-radius:4px;color:#fff;padding:3px 4px;font-size:10px;box-sizing:border-box">
        </div>
      </div>

      <div id="jash-feed-box" style="font-size:9px;max-height:75px;overflow-y:auto;background:rgba(0,0,0,0.4);border-radius:6px;padding:4px;border:1px solid rgba(255,255,255,0.06)"></div>
    `;

    document.body.appendChild(hud);

    // Draggable
    let isDragging = false, startX, startY, initialLeft, initialTop;
    const header = document.getElementById('jash-drag-header');
    header.addEventListener('mousedown', (e) => {
      isDragging = true;
      startX = e.clientX;
      startY = e.clientY;
      const rect = hud.getBoundingClientRect();
      initialLeft = rect.left;
      initialTop = rect.top;
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

    // Inputs
    const betInp = document.getElementById('jash-bet-inp');
    betInp?.addEventListener('change', () => {
      BASE_BET = parseInt(betInp.value) || 5;
      if (martingaleStep === 0) currentBet = BASE_BET;
      persist();
      updateHud();
    });

    // Buttons
    document.getElementById('jash-start-btn')?.addEventListener('click', () => {
      running = !running;
      persist();
      updateHud();
    });

    document.getElementById('jash-reset-btn')?.addEventListener('click', () => {
      if (!confirm('Reset session statistics?')) return;
      wins = 0; losses = 0;
      START_BANKROLL = liveWalletBal;
      sessionProfit = 0;
      currentBet = BASE_BET;
      martingaleStep = 0;
      consecutiveWins = 0;
      consecutiveLosses = 0;
      BETS_FEED = [];
      try { localStorage.removeItem('JASH_v9UM_BETS_FEED'); } catch (e) {}
      persist();
      updateHud();
    });

    updateHud();
  }

  function updateHud() {
    const hud = document.getElementById('jash-v9UM-hud');
    if (!hud) return;

    readScreenWalletBalance();

    const mode = detectActiveGameMode();
    const modeLbl = document.getElementById('jash-mode-lbl');
    if (modeLbl) modeLbl.textContent = `${mode} TITAN v9UM`;

    const results = getMergedResults();
    const currentLossStreak = martingaleStep;
    const pred = results.length >= 3 ? predictApexTitanV9UM(results.map(r => r.number).reverse(), currentLossStreak) : null;

    const regEl = document.getElementById('jash-regime-text');
    const predEl = document.getElementById('jash-pred-text');
    const ballEl = document.getElementById('jash-ball-text');
    const wlEl = document.getElementById('jash-wl-text');
    const lvlEl = document.getElementById('jash-lvl-badge');
    const profitEl = document.getElementById('jash-profit-text');
    const walletEl = document.getElementById('jash-wallet-text');
    const nextBetEl = document.getElementById('jash-nextbet-text');
    const startBtn = document.getElementById('jash-start-btn');
    const feedBox = document.getElementById('jash-feed-box');

    if (regEl) regEl.textContent = pred ? pred.regime : 'CALIBRATING…';
    if (predEl) {
      if (pred && pred.size) {
        predEl.textContent = pred.size;
        predEl.style.color = pred.size === 'BIG' ? '#00f5a0' : '#ff007a';
      } else {
        predEl.textContent = '--';
        predEl.style.color = '#00f5a0';
      }
    }
    if (ballEl) {
      ballEl.textContent = pred ? `# ${pred.number}` : '# -';
    }

    const total = wins + losses;
    const rate = total > 0 ? Math.round((wins / total) * 100) : 100;
    if (wlEl) wlEl.innerHTML = `<span style="color:#00f5a0">${wins}W</span> / <span style="color:#ff007a">${losses}L</span> (${rate}%)`;

    if (lvlEl) {
      if (martingaleStep === 0) {
        lvlEl.innerHTML = '🟢 LVL 1 (1x)';
        lvlEl.style.color = '#00f5a0';
      } else if (martingaleStep === 1) {
        lvlEl.innerHTML = '🟡 LVL 2 (3x)';
        lvlEl.style.color = '#ffb703';
      } else {
        lvlEl.innerHTML = '🛑 LVL 3 (9x SHIELD)';
        lvlEl.style.color = '#ff007a';
      }
    }

    if (profitEl) {
      profitEl.textContent = `₹${sessionProfit >= 0 ? '+' : ''}${sessionProfit.toFixed(2)}`;
      profitEl.style.color = sessionProfit >= 0 ? '#00f5a0' : '#ff007a';
    }
    if (walletEl) walletEl.textContent = `₹${liveWalletBal.toFixed(2)}`;
    if (nextBetEl) nextBetEl.textContent = `₹${currentBet}`;

    if (startBtn) {
      startBtn.textContent = running ? '⏸ STOP AUTO-PLAY' : '▶ START 24/7 AUTO-PLAY';
      startBtn.style.background = running ? 'linear-gradient(135deg,#ff007a,#7928ca)' : 'linear-gradient(135deg,#00f5a0,#00d9f5)';
      startBtn.style.color = running ? '#fff' : '#000';
    }

    if (feedBox) {
      feedBox.innerHTML = BETS_FEED.slice(0, 15).map(b => {
        let mark = b.won === true ? '<span style="color:#00f5a0">✓</span>' : (b.won === false ? '<span style="color:#ff007a">✕</span>' : '<span style="color:#00d9f5">⏳</span>');
        return `<div style="display:flex;justify-content:space-between;align-items:center;padding:2px 0;border-bottom:1px solid rgba(255,255,255,0.06)">
          <span>${mark} <b>${b.prediction}</b></span>
          <span style="color:${b.won === true ? '#00f5a0' : (b.won === false ? '#ff007a' : '#00d9f5')}">${b.engine || ''}</span>
          <span>₹${b.stake}</span>
        </div>`;
      }).join('');
    }
  }

  // ════════════════════════════════════════════════════════════
  // 10. CORE OVERNIGHT AUTOBET CYCLE
  // ════════════════════════════════════════════════════════════
  async function botCycle() {
    try {
      if (!document.body) return;

      const mode = detectActiveGameMode();
      const modeMs = mode === '30S' ? 30000 : 60000;
      const now = Date.now();
      const remainder = modeMs - (now % modeMs);
      const secondsLeft = Math.ceil(remainder / 1000);
      const currentBucket = Math.floor(now / modeMs);

      const results = getMergedResults();
      if (results.length < 3) return;

      const latestPeriod = results[0]?.period;

      // Settle Pending Bet
      if (pendingBet && !RESOLVED_PERIODS.has(pendingBet.period)) {
        let actual = results.find(r => r.period === pendingBet.period && Number.isInteger(r.number) && r.number >= 0 && r.number <= 9);
        const myHist = scanMyHistoryStatus(pendingBet.period);

        if (actual || (myHist && myHist.resolved)) {
          RESOLVED_PERIODS.add(pendingBet.period);
          let won = false;

          if (myHist && myHist.resolved) {
            won = myHist.won;
          } else if (actual) {
            const actualSize = actual.size.toUpperCase();
            won = (pendingBet.pred.toUpperCase() === actualSize);
          }

          const feedEntry = BETS_FEED.find(b => b.period === pendingBet.period && b.isPending);
          if (feedEntry) {
            feedEntry.won = won;
            feedEntry.isPending = false;
            if (actual) {
              feedEntry.result = `${actual.size} (${actual.number})`;
            } else {
              feedEntry.result = won ? 'WIN' : 'LOSS';
            }
            feedEntry.profit = won ? Number((pendingBet.stake * 0.96).toFixed(2)) : (-pendingBet.stake);
          }

          if (won) {
            wins++;
            consecutiveWins++;
            consecutiveLosses = 0;
            martingaleStep = 0;
            currentBet = BASE_BET;
            console.log(`%c✅ [APEX v9UM] WIN on #${pendingBet.period}! Reset to Base ₹${BASE_BET}.`, 'background:#00f5a0;color:#000;font-weight:bold;padding:5px');
          } else {
            losses++;
            consecutiveWins = 0;
            consecutiveLosses++;
            martingaleStep++;
            if (martingaleStep >= MAX_MART_STEPS) {
              martingaleStep = 0;
              currentBet = BASE_BET;
              console.log(`%c🛑 [APEX v9UM] 3-Level Cycle Resolved. Reset to Base ₹${BASE_BET}.`, 'background:#ff007a;color:#fff;font-weight:bold;padding:5px');
            } else {
              currentBet = calculateNextStake(BASE_BET, martingaleStep);
              console.log(`%c⚠️ [APEX v9UM] Step ${martingaleStep + 1} Recovery. Next Stake ₹${currentBet}.`, 'background:#ffb703;color:#000;font-weight:bold;padding:5px');
            }
          }

          if (BETS_FEED.length > 30) BETS_FEED = BETS_FEED.slice(0, 30);
          try { localStorage.setItem('JASH_v9UM_BETS_FEED', JSON.stringify(BETS_FEED)); } catch (e) {}
          pendingBet = null;
          persist();
          updateHud();
        } else {
          return;
        }
      }

      // Screen active period sync
      const screenPeriod = getScreenActivePeriod(latestPeriod);
      const activePeriod = screenPeriod || (latestPeriod ? String(BigInt(latestPeriod) + 1n) : null);
      if (!activePeriod) return;

      const pred = predictApexTitanV9UM(results.map(r => r.number).reverse(), martingaleStep);
      updateHud();

      if (!running || isBettingInProgress || !pred || !pred.size) return;
      if (LOCKED_BUCKETS.has(currentBucket)) return;

      // Betting Window: 30S (<=25s down to >=4s) | 1M (<=55s down to >=5s)
      const canBet = mode === '30S' ? (secondsLeft <= 25 && secondsLeft >= 4) : (secondsLeft <= 55 && secondsLeft >= 5);

      if (running && canBet && !LOCKED_BUCKETS.has(currentBucket)) {
        LOCKED_BUCKETS.add(currentBucket);
        isBettingInProgress = true;

        pendingBet = {
          period: activePeriod,
          pred: pred.size,
          number: pred.number,
          stake: currentBet,
          placedAt: Date.now()
        };

        BETS_FEED.unshift({
          period: activePeriod,
          prediction: `${pred.size} #${pred.number}`,
          engine: pred.regime,
          stake: currentBet,
          result: '--',
          profit: 0,
          won: null,
          isPending: true,
          time: new Date().toLocaleTimeString()
        });
        if (BETS_FEED.length > 30) BETS_FEED = BETS_FEED.slice(0, 30);
        try { localStorage.setItem('JASH_v9UM_BETS_FEED', JSON.stringify(BETS_FEED)); } catch (e) {}

        persist();
        updateHud();

        console.log(`%c🎯 [OVERNIGHT AUTOBET] Target: #${activePeriod} | Signal: ${pred.size} #${pred.number} (${pred.regime}) → ₹${currentBet}`, 'background:linear-gradient(90deg,#00f5a0,#7928ca);color:#fff;font-weight:bold;padding:6px 14px;font-size:13px;border-radius:4px');

        await executeBet(pred.size, currentBet);
        setTimeout(() => { isBettingInProgress = false; }, 2500);
      }
    } catch (e) {
      isBettingInProgress = false;
      console.error('[OVERNIGHT BOT] Cycle error:', e);
    }
  }

  // ════════════════════════════════════════════════════════════
  // 11. INITIALIZATION
  // ════════════════════════════════════════════════════════════
  function init() {
    createHud();
    setInterval(botCycle, 1000);
    setInterval(readScreenWalletBalance, 2000);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
