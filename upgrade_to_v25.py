import re
import os
import json

with open('build_script.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update version to 25.0
code = re.sub(r'// @version\s+[0-9.]+', '// @version      25.0', code)
code = re.sub(r'// @name\s+.*', '// @name         JASH VIP v25.0 ULTRA (100% Strict /pred Sync)', code)
code = re.sub(r'v2[0-4]\.0', 'v25.0', code)

# 2. Add isPeriodMatch helper if not present
if 'function isPeriodMatch' not in code:
    helper = """
  function isPeriodMatch(p1, p2) {
    if (!p1 || !p2) return false;
    const s1 = String(p1).replace(/\\D/g, '');
    const s2 = String(p2).replace(/\\D/g, '');
    if (s1 === s2) return true;
    if (s1.length >= 4 && s2.length >= 4) {
      return s1.slice(-5) === s2.slice(-5);
    }
    return false;
  }
"""
    code = code.replace("const opp = s =>", helper + "\n  const opp = s =>")

# 3. Update computeMasterPrediction
old_cmp = """  function computeMasterPrediction() {
    // 1. STRICTLY FOLLOW LIVE /PRED WEB SIGNAL IF AVAILABLE
    if (LIVE_WEB_SIGNAL && LIVE_WEB_SIGNAL.size) {
      const bestN = LIVE_WEB_SIGNAL.number != null ? LIVE_WEB_SIGNAL.number : (LIVE_WEB_SIGNAL.size === 'BIG' ? 7 : 2);
      const secN = LIVE_WEB_SIGNAL.size === 'BIG' ? 8 : 3;
      return {
        size: LIVE_WEB_SIGNAL.size,
        number: bestN,
        balls: LIVE_WEB_SIGNAL.balls || [bestN, secN],
        mode: `🎯 /PRED SIGNAL [${LIVE_WEB_SIGNAL.size}] (${LIVE_WEB_SIGNAL.regime || 'TITAN 9F'})`,
        conf: LIVE_WEB_SIGNAL.conf || 95
      };
    }"""

new_cmp = """  function computeMasterPrediction(targetPeriod) {
    // 1. STRICTLY FOLLOW LIVE /PRED WEB SIGNAL IF MATCHING CURRENT PERIOD
    if (LIVE_WEB_SIGNAL && LIVE_WEB_SIGNAL.size) {
      if (!targetPeriod || isPeriodMatch(LIVE_WEB_SIGNAL.period, targetPeriod)) {
        const bestN = LIVE_WEB_SIGNAL.number != null ? LIVE_WEB_SIGNAL.number : (LIVE_WEB_SIGNAL.size === 'BIG' ? 7 : 2);
        const secN = LIVE_WEB_SIGNAL.size === 'BIG' ? 8 : 3;
        return {
          size: LIVE_WEB_SIGNAL.size,
          number: bestN,
          balls: LIVE_WEB_SIGNAL.balls || [bestN, secN],
          mode: `🎯 /PRED SIGNAL [${LIVE_WEB_SIGNAL.size}] (#${String(LIVE_WEB_SIGNAL.period).slice(-5)})`,
          conf: LIVE_WEB_SIGNAL.conf || 95,
          isSynced: true
        };
      }
    }"""

code = code.replace(old_cmp, new_cmp)

# 4. In fetchLiveWebPredictionSignal, change interval to 250ms
code = code.replace("setInterval(fetchLiveWebPredictionSignal, 600);", "setInterval(fetchLiveWebPredictionSignal, 250);")

# 5. Remove DOM_SCRAPED_HISTORY ball scraper
code = re.sub(
    r'const balls = Array\.from\(document\.querySelectorAll\(\'\.ball.*?\n\s*setInterval\(scrapeScreenGameHistory, 1000\);\n\s*scrapeScreenGameHistory\(\);',
    '// DOM scraped history removed to prevent ball button poisoning',
    code,
    flags=re.DOTALL
)

# 6. In executeBet, filter out history/table containers
old_bet_filter = "const allEls = Array.from(document.querySelectorAll('div, button, span, uni-view, p')).filter(e => !e.closest('#jash-hud'));"
new_bet_filter = """const allEls = Array.from(document.querySelectorAll('div, button, span, uni-view, p')).filter(e => {
      if (e.closest('#jash-hud')) return false;
      if (e.closest('.history, [class*="history"], [class*="record"], table, .list, [class*="list"], .record-list, .tab-content, .my-history')) return false;
      return true;
    });"""
code = code.replace(old_bet_filter, new_bet_filter)

# 7. In botCycle, ensure targetPeriod is passed and add stale-signal waiting guard
old_bot_pred = "const masterPred = computeMasterPrediction();"
new_bot_pred = "const masterPred = computeMasterPrediction(activePeriod);"
code = code.replace(old_bot_pred, new_bot_pred)

# Update the call in updateHud
code = code.replace("const pred = computeMasterPrediction();", "const pred = computeMasterPrediction(currentPeriod);")

# Update telemetry call
code = code.replace("const pred = computeMasterPrediction();", "const pred = computeMasterPrediction(activePeriod);")

# Add the waiting guard in botCycle before betting
old_bet_check = """      const canBet = (GAME_MODE === '30S')
        ? (secondsLeft <= 25 && secondsLeft >= 4)
        : (secondsLeft <= 55 && secondsLeft >= 8);

      if (running && canBet && !LOCKED_TIME_BUCKETS.has(currentBucket)) {"""

new_bet_check = """      const canBet = (GAME_MODE === '30S')
        ? (secondsLeft <= 25 && secondsLeft >= 3)
        : (secondsLeft <= 55 && secondsLeft >= 6);

      // CRITICAL ZERO-DESYNC GUARD:
      // If web signal is from an OLD period, WAIT for the new period's signal up to 4s left!
      const hasMatchingWebSignal = LIVE_WEB_SIGNAL && isPeriodMatch(LIVE_WEB_SIGNAL.period, activePeriod);
      if (running && !hasMatchingWebSignal && secondsLeft > 4) {
        // Wait for /pred signal of THIS active period to arrive
        return;
      }

      if (running && canBet && !LOCKED_TIME_BUCKETS.has(currentBucket)) {"""

code = code.replace(old_bet_check, new_bet_check)

# 8. Add root 30sec_win_v1.user.js to output_paths
if "'/Users/jashwanthsingh/Downloads/jashvip/30sec_win_v1.user.js'" not in code:
    code = code.replace(
        "'/Users/jashwanthsingh/Downloads/jashvip/signal_top1_follower.user.js',",
        "'/Users/jashwanthsingh/Downloads/jashvip/30sec_win_v1.user.js',\n    '/Users/jashwanthsingh/Downloads/jashvip/signal_top1_follower.user.js',"
    )

with open('build_script.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("build_script.py successfully upgraded to v25.0!")
