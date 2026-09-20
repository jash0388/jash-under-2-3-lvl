import os
import re

print("=== Fixing History Ingestion & Removing My History Scraping ===")

with open('build_script.py', 'r') as f:
    code = f.read()

# Replace scrapeScreenGameHistory and balls scraper with strict Game History table only
clean_history_ingest = '''  // ── 3. STRICT CLEAN LOTTERY DRAW STREAM ─────────────────
  let LIVE_API_HISTORY = [];
  let DOM_SCRAPED_HISTORY = [];
  let LOCAL_DRAW_BUFFER = [];

  function mergeIntoBuffer(newRows) {
    if (!Array.isArray(newRows) || newRows.length === 0) return;
    const map = new Map();
    [...LOCAL_DRAW_BUFFER, ...newRows].forEach(item => {
      if (item && item.period && /^2026\\d{10,16}$/.test(String(item.period).trim()) && Number.isInteger(item.number)) {
        map.set(String(item.period).trim(), {
          period: String(item.period).trim(),
          number: parseInt(item.number),
          size: sizeFor(parseInt(item.number))
        });
      }
    });
    LOCAL_DRAW_BUFFER = Array.from(map.values()).sort((a, b) => {
      try { return BigInt(b.period) > BigInt(a.period) ? 1 : -1; } catch (e) { return 0; }
    }).slice(0, 100);
  }

  // Intercept game network JSON responses for clean draw history
  const origFetch = window.fetch;
  window.fetch = async function (...args) {
    const response = await origFetch.apply(this, args);
    try {
      const clone = response.clone();
      clone.json().then(data => {
        try {
          const list = data?.data?.list || data?.data?.rows || data?.data?.issues || (Array.isArray(data?.data) ? data.data : null);
          if (Array.isArray(list) && list.length > 0) {
            const parsed = list.map(item => {
              const p = String(item.issueNumber || item.period || item.issue || '').trim();
              const n = parseInt(item.number != null ? item.number : item.num);
              return { period: p, number: n, size: sizeFor(n) };
            }).filter(x => /^2026\\d{10,16}$/.test(x.period) && Number.isInteger(x.number));
            if (parsed.length > 0) {
              mergeIntoBuffer(parsed);
              updateHud();
            }
          }
        } catch (e) {}
      }).catch(() => {});
    } catch (e) {}
    return response;
  };

  // Scrape ONLY Game History tab (Never My History or Bet Orders)
  function scrapeScreenGameHistory() {
    try {
      // Find game history table specifically
      const rows = Array.from(document.querySelectorAll('table tbody tr, .van-table__row, [class*="record"] tr')).filter(e => {
        if (e.closest('#jash-hud')) return false;
        const txt = (e.textContent || '').trim();
        // STRICTLY IGNORE My History / Bet Orders
        if (/Purchase|Amount|Order|Tax|Failed|Succeed|Detail|Unpaid|Quantity/i.test(txt)) return false;
        return true;
      });

      const parsed = [];
      for (const r of rows) {
        const txt = (r.textContent || '').trim();
        const pMatch = txt.match(/\\b(2026\\d{10,14})\\b/);
        if (pMatch) {
          const p = pMatch[1];
          let numVal = null;
          const numCell = r.querySelector('.num, .number, .ball, [class*="ball"], td:nth-child(2), td:nth-child(3)');
          if (numCell) {
            const cTxt = (numCell.textContent || '').trim();
            if (/^[0-9]$/.test(cTxt)) numVal = parseInt(cTxt);
          }
          if (numVal == null) {
            const numMatches = Array.from(txt.matchAll(/\\b([0-9])\\b/g));
            if (numMatches.length === 1) { // Exactly 1 single digit for the ball
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
          }).filter(x => /^2026\\d{10,16}$/.test(x.period) && Number.isInteger(x.number));
          if (parsed.length > 0) {
            LIVE_API_HISTORY = parsed;
            mergeIntoBuffer(parsed);
            updateHud();
          }
        }
      }
    } catch (e) {}
  }
  setInterval(fetchLiveLotteryHistoryDirectly, 800);
  fetchLiveLotteryHistoryDirectly();'''

# Replace the entire history section in build_script.py
code = re.sub(
    r'// ── 3\. NETWORK INTERCEPTION & SCREEN SCRAPER ─────────────.*?(?=// ── 3\.2 100% STRICT /PRED WEB SIGNAL BRIDGE)',
    lambda m: clean_history_ingest + '\n\n  ',
    code,
    flags=re.DOTALL
)

# Update getMergedResults to filter strictly real periods
clean_get_merged = '''  function getMergedResults() {
    const map = new Map();
    [...LIVE_API_HISTORY, ...LOCAL_DRAW_BUFFER, ...DOM_SCRAPED_HISTORY].forEach(item => {
      if (item && item.period && /^2026\\d{10,16}$/.test(String(item.period).trim()) && Number.isInteger(item.number)) {
        map.set(String(item.period).trim(), {
          period: String(item.period).trim(),
          number: parseInt(item.number),
          size: sizeFor(parseInt(item.number))
        });
      }
    });
    return Array.from(map.values()).sort((a, b) => {
      try { return BigInt(b.period) > BigInt(a.period) ? 1 : -1; } catch (e) { return 0; }
    });
  }'''

code = re.sub(
    r'function getMergedResults\(\) \{.*?\n  \}',
    lambda m: clean_get_merged,
    code,
    flags=re.DOTALL
)

# Bump version to v21.0
code = code.replace('@version      20.0', '@version      21.0')
code = code.replace('v20.0', 'v21.0')

with open('build_script.py', 'w') as f:
    f.write(code)

print("Updated build_script.py with strict Game History filter and v21.0.")
os.system('python3 build_script.py')
print("Successfully compiled all v21.0 userscripts.")
