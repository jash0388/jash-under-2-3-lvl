import json
import re
import os

with open('v9um_apex_titan_supreme_30s_rules.json', 'r') as f:
    rules_30s = json.load(f)

with open('v3um_enhanced_1m_rules.json', 'r') as f:
    rules_1m = json.load(f)

rules_30s_json = json.dumps(rules_30s)
rules_1m_json = json.dumps(rules_1m)

template_path = '/Users/jashwanthsingh/Downloads/signal_top1_follower.user.js'
with open(template_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Build Triple-Redundant XHR + Fetch + DOM Result Ingestion Engine
network_engine = r"""  // ════════════════════════════════════════════════════════════
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
      const rows = Array.from(document.querySelectorAll('table tbody tr, .van-table__row, [class*="record"] tr, [class*="history"] tr, [class*="list"] [class*="item"]')).filter(e => !e.closest('#jash-v1UM-hud'));
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
      const ballEls = Array.from(document.querySelectorAll('.ball, [class*="ball"], .van-col, .balls span, .game-ball')).filter(e => !e.closest('#jash-v1UM-hud') && /^[0-9]$/.test((e.textContent || '').trim()));
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
  }"""

# Replace lines 426 to 525 in code using lambda
pattern = r"// ═+\s*// 5\. GAME MODE & API FETCHER[\s\S]*?function getMergedResults\(\) \{[\s\S]*?return Array\.from\(map\.values\(\)\)\.sort\([\s\S]*?\};\s*\}"
code = re.sub(pattern, lambda m: network_engine, code)

period_detector = r"""  function getScreenActivePeriod(fallbackLatest) {
    try {
      // 1. Direct Period Display on WinGo Game Screen (e.g., 2026092010005...)
      const all = Array.from(document.querySelectorAll('div, span, p, h1, h2, h3, b')).filter(e => !e.closest('#jash-v1UM-hud') && !e.closest('table'));
      for (const el of all) {
        const txt = (el.textContent || '').trim();
        const m = txt.match(/^(202\d{10,18}|\d{12,20})$/);
        if (m) return m[1];
      }
      for (const el of all) {
        const txt = (el.textContent || '').trim();
        const m = txt.match(/(?:Period|Issue|期号|No\.)\s*[:\s]?\s*(202\d{10,18}|\d{10,20})/i);
        if (m) return m[1];
      }
    } catch (e) {}
    if (fallbackLatest && /^\d+$/.test(fallbackLatest)) {
      try { return String(BigInt(fallbackLatest) + 1n); } catch (e) {}
    }
    return null;
  }"""

pattern_period = r"function getScreenActivePeriod\(fallbackLatest\) \{[\s\S]*?return null;\s*\}"
code = re.sub(pattern_period, lambda m: period_detector, code)

# Ensure HUD displays v9UM and OTA status
code = code.replace('v1UM', 'v9UM')
code = code.replace('V1UM', 'V9UM')
code = code.replace('JASH OVERNIGHT v9UM', 'JASH VIP APEX v9UM')

def generate_script(script_name):
    clean_name = script_name.replace('.user.js', '')
    url_name = script_name
    
    header_block = f"""// ==UserScript==
// @name         {clean_name} — Apex Titan v9UM (Auto-Updating Zero-Bust Master)
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
// @updateURL    https://jashvip.vercel.app/{url_name}
// @downloadURL  https://jashvip.vercel.app/{url_name}
// @run-at       document-start
// ==/UserScript=="""

    res = re.sub(r'// ==UserScript==[\s\S]*?// ==/UserScript==', lambda m: header_block, code, count=1)
    res = res.replace('Apex Titan v9UM (v70.4)', 'Apex Titan v9UM (v70.5)')
    return res

target_scripts = [
    'signal_top1_follower.user.js',
    'jash_perc_win.user.js',
    'JASH_VIP_APEX_TITAN_V9UM_AUTOBET.user.js',
    'JASH_BOT.user.js',
]

for s in target_scripts:
    content = generate_script(s)
    local_path = os.path.join('/Users/jashwanthsingh/Downloads', s)
    public_path = os.path.join('/Users/jashwanthsingh/Downloads/jashvip/public', s)
    root_path = os.path.join('/Users/jashwanthsingh/Downloads/jashvip', s)
    
    with open(local_path, 'w', encoding='utf-8') as f:
        f.write(content)
    with open(public_path, 'w', encoding='utf-8') as f:
        f.write(content)
    with open(root_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f'Upgraded with Full-Redundancy Network + DOM Engine: {s}')

print('\nAll scripts upgraded to v70.5 with XHR + Fetch + DOM scraper!')
