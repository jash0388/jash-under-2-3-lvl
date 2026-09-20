import re

# 1. Update pred.html files to publish snapshot to /api/live-signal
pred_files = ['pred.html', 'public/pred.html', 'pred/index.html', 'public/pred/index.html']
for p in pred_files:
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()

    old_snapshot = """        function snapshotPendingPrediction(targetPeriod, results, reqMode = currentMode) {
          if (reqMode !== currentMode) return;
          if (!targetPeriod || targetPeriod === "—" || results.length < 3) return;
          if (!isValidPeriodForMode(targetPeriod, reqMode)) return;
          const currentLossStreak = getLossStreak();
          const pred = predictApexTitanV9UM(results.map(r => r.number).reverse(), currentLossStreak, reqMode);
          if (!pred) return;
          if (pendingPrediction && pendingPrediction.period === targetPeriod && pendingPrediction.mode === reqMode) return;
          pendingPrediction = {
            mode: reqMode,
            period: targetPeriod,
            predNumber: pred.number,
            predSize: pred.size,
            regime: pred.regime,
            confidence: pred.confidence,
            lossStreak: currentLossStreak,
            timestamp: Date.now()
          };
          savePending(pendingPrediction, reqMode);
        }"""

    new_snapshot = """        function snapshotPendingPrediction(targetPeriod, results, reqMode = currentMode) {
          if (reqMode !== currentMode) return;
          if (!targetPeriod || targetPeriod === "—" || results.length < 3) return;
          if (!isValidPeriodForMode(targetPeriod, reqMode)) return;
          const currentLossStreak = getLossStreak();
          const pred = predictApexTitanV9UM(results.map(r => r.number).reverse(), currentLossStreak, reqMode);
          if (!pred) return;
          if (pendingPrediction && pendingPrediction.period === targetPeriod && pendingPrediction.mode === reqMode) return;
          pendingPrediction = {
            mode: reqMode,
            period: targetPeriod,
            predNumber: pred.number,
            predSize: pred.size,
            regime: pred.regime,
            confidence: pred.confidence,
            lossStreak: currentLossStreak,
            timestamp: Date.now()
          };
          savePending(pendingPrediction, reqMode);

          // Broadcast live signal directly to server bridge for phone bot to follow
          try {
            fetch('/api/live-signal', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                mode: reqMode,
                period: targetPeriod,
                size: pred.size,
                number: pred.number,
                confidence: pred.confidence,
                regime: pred.regime
              })
            }).catch(() => {});
          } catch (e) {}
        }"""

    if old_snapshot in content:
        content = content.replace(old_snapshot, new_snapshot)
    
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated live signal broadcaster in {p}")

# 2. Update build_script.py to strictly follow /api/live-signal
with open('build_script.py', 'r', encoding='utf-8') as f:
    b_code = f.read()

# Update version to 19.0 (Direct Web Follower)
b_code = b_code.replace('// @name         JASH VIP v18.0 Ultimate (Apex Titan Supreme 9F Direct-API Sync)',
                        '// @name         JASH VIP v19.0 Ultimate (Direct /pred Live-Signal Follower)')
b_code = b_code.replace('// @version      18.0',
                        '// @version      19.0')
b_code = b_code.replace('// @description  👑 JASH VIP · WinGo 30S | TITAN SUPREME v18.0 (DIRECT AR-LOTTERY API SYNC + 9-FEATURE ZERO-BUST SHIELD) + Custom Progression (2->5->10) + No Loss Limit',
                        '// @description  👑 JASH VIP · WinGo 30S | TITAN SUPREME v19.0 (100% STRICT /pred WEB SIGNAL FOLLOWER) + Custom Progression (2->5->10) + No Loss Limit')
b_code = b_code.replace('console.log("%c👑 JASH VIP · WinGo 30S [TITAN SUPREME v18.0 DIRECT API ZERO-BUST 9F] ACTIVE"',
                        'console.log("%c👑 JASH VIP · WinGo 30S [TITAN SUPREME v19.0 DIRECT /PRED WEB SIGNAL FOLLOWER] ACTIVE"')

# Update HUD
b_code = b_code.replace('👑 JASH VIP · TITAN SUPREME v18.0', '👑 JASH VIP · TITAN SUPREME v19.0')
b_code = b_code.replace('⚡ TITAN SUPREME v18.0 (DIRECT API SYNC 9F)', '🎯 /PRED LIVE SIGNAL FOLLOWER v19.0')
b_code = b_code.replace('⚡ TITAN SUPREME v18.0 (${GAME_MODE}) ACTIVE', '🎯 FOLLOWING /PRED (${GAME_MODE}) ACTIVE')

# Add live signal poller
poller_code = """  // ── 3.2 100% STRICT /PRED WEB SIGNAL BRIDGE ────────────────
  let LIVE_WEB_SIGNAL = null;

  async function fetchLiveWebPredictionSignal() {
    try {
      const res = await (origFetch || window.fetch)(`https://jashvip.vercel.app/api/live-signal?mode=${GAME_MODE}&_t=${Date.now()}`, {
        method: 'GET',
        cache: 'no-store',
        headers: { 'Accept': 'application/json' }
      });
      if (res.ok) {
        const data = await res.json();
        if (data && data.signal && data.signal.size) {
          LIVE_WEB_SIGNAL = data.signal;
          updateHud();
        }
      }
    } catch (e) {}
  }
  setInterval(fetchLiveWebPredictionSignal, 600);
  fetchLiveWebPredictionSignal();
"""

if 'fetchLiveWebPredictionSignal' not in b_code:
    b_code = b_code.replace('  fetchLiveLotteryHistoryDirectly();', '  fetchLiveLotteryHistoryDirectly();\n\n' + poller_code)

# Replace computeMasterPrediction to prioritize LIVE_WEB_SIGNAL
old_master_pred = """  function computeMasterPrediction() {
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
  }"""

new_master_pred = """  function computeMasterPrediction() {
    // 1. STRICTLY FOLLOW LIVE /PRED WEB SIGNAL
    if (LIVE_WEB_SIGNAL && LIVE_WEB_SIGNAL.size) {
      const bestN = LIVE_WEB_SIGNAL.number != null ? LIVE_WEB_SIGNAL.number : (LIVE_WEB_SIGNAL.size === 'BIG' ? 7 : 2);
      const secN = LIVE_WEB_SIGNAL.size === 'BIG' ? 8 : 3;
      return {
        size: LIVE_WEB_SIGNAL.size,
        number: bestN,
        balls: LIVE_WEB_SIGNAL.balls || [bestN, secN],
        mode: `🎯 /PRED SIGNAL [${LIVE_WEB_SIGNAL.size}]`,
        conf: LIVE_WEB_SIGNAL.conf || 92
      };
    }

    // 2. Fallback if offline
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

    const bestNum = pred.finalSize === 'BIG' ? 7 : 2;
    const secNum = pred.finalSize === 'BIG' ? 8 : 3;

    return {
      size: pred.finalSize,
      number: bestNum,
      balls: [bestNum, secNum],
      mode: pred.regime,
      conf: pred.conf
    };
  }"""

if old_master_pred in b_code:
    b_code = b_code.replace(old_master_pred, new_master_pred)

with open('build_script.py', 'w', encoding='utf-8') as f:
    f.write(b_code)

print("Updated build_script.py to 100% strictly follow /pred web signal.")

