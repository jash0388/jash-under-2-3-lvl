import json
import re
import os

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace MAX_HISTORY = 100 with 1000
html = html.replace('const MAX_HISTORY = 100;', 'const MAX_HISTORY = 1000;')

# Update history header title
html = html.replace(
    '<span class="history-title">LAST ${savedHistory.length} PREDICTIONS (${GAME_MODES[currentMode].name})</span>',
    '<span class="history-title">SESSION LOG · ${savedHistory.length}/1000 STORED (${GAME_MODES[currentMode].name})</span>'
)

# Replace loadHistory and countdown timers with ultra-fast sub-second burst engine
timing_block_old = re.search(r"// === LOAD DATA ===[\s\S]*?checkSavedSession\(\);\s*\}\)\(\);", html)
if timing_block_old:
    new_timing_block = """// === LOAD DATA & ULTRA-FAST HYPER-BURST SYNC ENGINE ===
        let isHyperBurstActive = false;
        let hyperBurstTimer = null;
        let lastKnownPeriod = "";

        async function loadHistory({ silent = false, fast = false } = {}) {
          if (!isAuthenticated || requestInFlight) return;
          const reqMode = currentMode;
          requestInFlight = true;
          state.error = "";
          if (!silent) { state.loading = true; render(); }
          let changed = false;
          const cfg = GAME_MODES[reqMode];
          try {
            if (activeAbortController) {
              try { activeAbortController.abort(); } catch {}
            }
            activeAbortController = new AbortController();
            const controller = activeAbortController;
            const timeoutMs = fast ? 2000 : 5000;
            const timeout = setTimeout(() => controller.abort(), timeoutMs);
            const response = await fetch(`${cfg.url}?_t=${Date.now()}`, {
              method: "GET",
              cache: "no-store",
              headers: { Accept: "application/json", "Cache-Control": "no-cache" },
              signal: controller.signal
            });
            clearTimeout(timeout);
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            const payload = await response.json();
            
            // Discard if user switched mode while request was in-flight
            if (reqMode !== currentMode || !isAuthenticated) return;

            const rows = normalise(payload);
            if (!rows.length) throw new Error("No results returned");
            const signature = rows.slice(0, 10).map(r => `${r.period}:${r.number}`).join("|");
            changed = signature !== state.dataSignature;
            
            const isNewPeriod = lastKnownPeriod && rows[0].period !== lastKnownPeriod;
            lastKnownPeriod = rows[0].period;

            state.results = rows;
            state.dataSignature = signature;
            state.targetPeriod = nextDecimal(rows[0].period);
            const apiDrift = Number(payload.serviceTime || Date.now()) - Date.now();
            state.serverOffset = Math.abs(apiDrift) <= 3000 ? apiDrift : 0;
            state.synced = true;
            state.updatedAt = new Date(Date.now() + state.serverOffset).toLocaleTimeString([], { hour:"2-digit", minute:"2-digit", second:"2-digit" });

            // Reconcile and backfill history STRICTLY for reqMode up to 1000 items!
            reconcileHistory(rows, reqMode);

            // Snapshot the NEW prediction for the upcoming period
            snapshotPendingPrediction(nextDecimal(rows[0].period), rows, reqMode);

            // If a new period was just delivered, throttle down hyper-burst
            if (isNewPeriod && isHyperBurstActive && state.seconds > 4 && state.seconds < cfg.cycleSeconds - 4) {
              stopHyperBurst();
            }

            updateCountdown();
          } catch (error) {
            if (reqMode !== currentMode || !isAuthenticated) return;
            if (error.name !== "AbortError") {
              state.synced = false;
              state.error = `Feed error: ${error.message}`;
            }
          } finally {
            if (reqMode === currentMode && isAuthenticated) {
              requestInFlight = false;
              state.loading = false;
              if (!silent || changed || state.error) render();
            }
          }
        }

        function startHyperBurst() {
          if (isHyperBurstActive) return;
          isHyperBurstActive = true;
          if (hyperBurstTimer) clearInterval(hyperBurstTimer);
          // Hyper-speed 300ms polling burst at draw boundary
          hyperBurstTimer = setInterval(() => {
            if (!isAuthenticated) { stopHyperBurst(); return; }
            loadHistory({ silent: true, fast: true });
          }, 300);
          loadHistory({ silent: true, fast: true });
        }

        function stopHyperBurst() {
          isHyperBurstActive = false;
          if (hyperBurstTimer) {
            clearInterval(hyperBurstTimer);
            hyperBurstTimer = null;
          }
        }

        function updateCountdown() {
          if (!isAuthenticated) return;
          const cfg = GAME_MODES[currentMode];
          const cycleMs = cfg.cycleSeconds * 1000;
          const serverNow = Date.now() + state.serverOffset;
          const remainder = cycleMs - (serverNow % cycleMs);
          const oldSec = state.seconds;
          state.seconds = Math.max(1, Math.min(cfg.cycleSeconds, Math.ceil(remainder / 1000)));

          if (oldSec !== state.seconds) {
            const cd = app.querySelector(".countdown span");
            if (cd) cd.innerHTML = `${state.seconds}s<small>LEFT</small>`;
            const cdEl = app.querySelector(".countdown");
            if (cdEl) {
              if (state.seconds <= 5) cdEl.classList.add("urgent");
              else cdEl.classList.remove("urgent");
            }
          }

          // HYPER-BURST TRIGGER:
          // When 3s or less remain, or right after 0s (when remainder is near cycleMs), activate 300ms Hyper-Burst!
          const nearBoundary = state.seconds <= 3 || state.seconds >= cfg.cycleSeconds - 4;
          if (nearBoundary && !isHyperBurstActive) {
            startHyperBurst();
          } else if (!nearBoundary && isHyperBurstActive) {
            stopHyperBurst();
          }
        }

        // High-precision millisecond tick (every 100ms)
        setInterval(() => {
          if (!isAuthenticated) return;
          updateCountdown();
        }, 100);

        // Steady-State Keep-Alive Polling (every 2.5s)
        setInterval(() => {
          if (!isAuthenticated || isHyperBurstActive) return;
          loadHistory({ silent: true, fast: false });
        }, 2500);

        // Initial Session Check
        checkSavedSession();
      })();"""
    html = html[:timing_block_old.start()] + new_timing_block + html[timing_block_old.end():]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html with Ultra-Fast 300ms Burst Sync and 1000 Results Storage successfully!")

# 2. Update all userscripts
files = [
    "/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V4UM_AUTOBET.user.js",
    "/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V3UM_AUTOBET.user.js",
    "/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V2UM_AUTOBET.user.js",
    "/Users/jashwanthsingh/Downloads/signal_top1_follower.user.js",
    "/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V1UM_AUTOBET.user.js",
    "/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V100_AUTOBET.user.js",
    "/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V90_AUTOBET.user.js",
    "/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V80_AUTOBET.user.js",
    "/Users/jashwanthsingh/Downloads/JASH_VIP_APEX_TITAN_V70_AUTOBET.user.js",
    "/Users/jashwanthsingh/Downloads/JASH_BOT.user.js",
    "/Users/jashwanthsingh/Downloads/jash_perc_win.user.js"
]

for path in files:
    if not os.path.exists(path): continue
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()

    # Boost fetch interval to 800ms / burst
    src = src.replace("setInterval(fetchSignalAPI, 3000);", "setInterval(fetchSignalAPI, 1000);")
    src = src.replace("setInterval(fetchSignalAPI, 2500);", "setInterval(fetchSignalAPI, 1000);")
    src = src.replace("setInterval(fetchSignalAPI, 2000);", "setInterval(fetchSignalAPI, 1000);")

    # Increase history buffer to 1000
    src = re.sub(r"const SIGNAL_HISTORY_MAX\s*=\s*\d+;", "const SIGNAL_HISTORY_MAX = 1000;", src)
    src = re.sub(r"const MAX_HISTORY\s*=\s*\d+;", "const MAX_HISTORY = 1000;", src)

    with open(path, "w", encoding="utf-8") as f:
        f.write(src)
    print(f"Updated fast-poll & 1000-history for: {path}")

print("All files updated successfully!")
