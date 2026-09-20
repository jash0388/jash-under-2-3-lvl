import re

with open('generate_standalone_v26.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Bump version to 27.0
code = re.sub(r'// @version\s+[0-9.]+', '// @version      27.0', code)
code = re.sub(r'// @name\s+.*', '// @name         JASH VIP v27.0 (Strict 2-Level Loss Shield & Zero-Bust)', code)
code = re.sub(r'v26\.0', 'v27.0', code)

# 2. Add MAX_LOSS_LEVEL to state
if 'let MAX_LOSS_LEVEL' not in code:
    code = code.replace(
        "let LOSS_STREAK     = parseInt(localStorage.getItem('J26_LOSS_STREAK')) || 0;",
        "let LOSS_STREAK     = parseInt(localStorage.getItem('J26_LOSS_STREAK')) || 0;\n  let MAX_LOSS_LEVEL  = parseInt(localStorage.getItem('J26_MAX_LVL')) || 2; // Strict 2-Level Max"
    )

# 3. Add to persistAll
if "'J26_MAX_LVL'" not in code:
    code = code.replace(
        "localStorage.setItem('J26_LOSS_STREAK', LOSS_STREAK);",
        "localStorage.setItem('J26_LOSS_STREAK', LOSS_STREAK);\n      localStorage.setItem('J26_MAX_LVL', MAX_LOSS_LEVEL);"
    )

# 4. Update checkLastDrawOutcome for virtual bets
old_settle = """      if (won) {
        wins++;
        bet.profit = bet.stake * 0.96;
        LOSS_STREAK = 0;
        martingaleStep = 0;
        currentBet = getStakeForStep(BASE_BET, 0);
        console.log(`%c🏆 JASH VIP WIN on #${latestDraw.period}! Reset to Level 1 (₹${BASE_BET})`, 'background:#10b981;color:#fff;font-weight:900;padding:6px;border-radius:4px');
      } else {
        losses++;
        bet.profit = -bet.stake;
        LOSS_STREAK++;
        martingaleStep++;
        currentBet = getStakeForStep(BASE_BET, martingaleStep);
        console.log(`%c💀 JASH VIP LOSS on #${latestDraw.period}! Streak=${LOSS_STREAK} -> Next Stake ₹${currentBet} (Step ${martingaleStep})`, 'background:#ef4444;color:#fff;font-weight:900;padding:6px;border-radius:4px');
      }"""

new_settle = """      if (won) {
        wins++;
        bet.profit = bet.isVirtual ? 0 : (bet.stake * 0.96);
        LOSS_STREAK = 0;
        martingaleStep = 0;
        currentBet = getStakeForStep(BASE_BET, 0);
        console.log(`%c🏆 JASH VIP WIN on #${latestDraw.period}! ${bet.isVirtual ? 'Recovery Confirmed Virtually! ' : ''}Reset to Level 1 (₹${BASE_BET})`, 'background:#10b981;color:#fff;font-weight:900;padding:6px;border-radius:4px');
      } else {
        losses++;
        bet.profit = bet.isVirtual ? 0 : (-bet.stake);
        LOSS_STREAK++;
        martingaleStep++;
        currentBet = getStakeForStep(BASE_BET, martingaleStep);
        console.log(`%c💀 JASH VIP LOSS on #${latestDraw.period}! Streak=${LOSS_STREAK} ${bet.isVirtual ? '(🛑 SHIELD ACTIVE - ₹0 REAL MONEY LOST)' : ''}`, 'background:#ef4444;color:#fff;font-weight:900;padding:6px;border-radius:4px');
      }"""

code = code.replace(old_settle, new_settle)

# 5. In HUD, add Max Level Button and indicator
old_hud_btn = """      <div style="margin-bottom:8px;">
        <button id="j-mode-btn" style="width:100%;padding:4px 0;background:rgba(124,58,237,0.3);border:1px solid #7c3aed;border-radius:6px;color:#c4b5fd;font-weight:bold;font-size:11px;cursor:pointer;">
          🎯 MODE: ${GAME_MODE === '30S' ? '30 SEC (FAST)' : '1 MIN'}
        </button>
      </div>"""

new_hud_btn = """      <div style="display:flex;gap:4px;margin-bottom:8px;">
        <button id="j-mode-btn" style="flex:1;padding:4px 0;background:rgba(124,58,237,0.3);border:1px solid #7c3aed;border-radius:6px;color:#c4b5fd;font-weight:bold;font-size:10px;cursor:pointer;">
          🎯 ${GAME_MODE === '30S' ? '30S' : '1M'}
        </button>
        <button id="j-shield-btn" style="flex:1;padding:4px 0;background:rgba(255,0,85,0.2);border:1px solid #ff0055;border-radius:6px;color:#ff6699;font-weight:bold;font-size:10px;cursor:pointer;">
          🛡️ MAX LVL: ${MAX_LOSS_LEVEL}
        </button>
      </div>"""

code = code.replace(old_hud_btn, new_hud_btn)

# Add onclick for j-shield-btn
shield_click = """    document.getElementById('j-shield-btn').onclick = () => {
      MAX_LOSS_LEVEL = (MAX_LOSS_LEVEL === 2) ? 3 : (MAX_LOSS_LEVEL === 3 ? 99 : 2);
      document.getElementById('j-shield-btn').textContent = `🛡️ MAX LVL: ${MAX_LOSS_LEVEL > 5 ? 'OFF' : MAX_LOSS_LEVEL}`;
      persistAll();
      updateHud();
    };
"""
code = code.replace("document.getElementById('j-mode-btn').onclick = () => {", shield_click + "\n    document.getElementById('j-mode-btn').onclick = () => {")

# 6. Update updateHud status badge for Shield mode
old_badge = """    badge.textContent = running
      ? (pendingBet ? `⏳ BETTING ₹${pendingBet.stake} ON ${pendingBet.pred}` : `⚡ LOCAL BRAIN ACTIVE (${GAME_MODE})`)
      : `⏹ ENGINE (${GAME_MODE}) STOPPED`;"""

new_badge = """    const isShieldActive = (martingaleStep >= MAX_LOSS_LEVEL);
    badge.textContent = running
      ? (isShieldActive ? `🛑 2-LVL SHIELD: PAPER BET (REAL ₹0)` : (pendingBet ? `⏳ BETTING ₹${pendingBet.stake} ON ${pendingBet.pred}` : `⚡ LOCAL BRAIN ACTIVE (${GAME_MODE})`))
      : `⏹ ENGINE (${GAME_MODE}) STOPPED`;
    if (isShieldActive && running) {
      badge.style.background = 'rgba(255,0,85,0.2)';
      badge.style.borderColor = '#ff0055';
      badge.style.color = '#ff6699';
    } else {
      badge.style.background = 'rgba(0,245,160,0.1)';
      badge.style.borderColor = 'rgba(0,245,160,0.3)';
    }"""

code = code.replace(old_badge, new_badge)

# Update feed items for virtual display
old_feed_map = "<span>${b.won === true ? 'WIN' : b.won === false ? 'LOSS' : 'PENDING'}</span>"
new_feed_map = "<span>${b.isVirtual ? '🛡️ V-' : ''}${b.won === true ? 'WIN' : b.won === false ? 'LOSS' : 'PENDING'}</span>"
code = code.replace(old_feed_map, new_feed_map)

# 7. Update botCycle to execute virtual bet if step >= MAX_LOSS_LEVEL
old_bet_run = """        if (activePeriod) {
          RECORDED_BETS.unshift({
            period: activePeriod,
            prediction: pred.size,
            mode: pred.mode,
            stake: currentBet,
            won: null,
            profit: null,
            isPending: true,
            time: new Date().toLocaleTimeString()
          });
          if (RECORDED_BETS.length > 50) RECORDED_BETS = RECORDED_BETS.slice(0, 50);
        }

        persistAll();
        updateHud();

        await executeBet(pred.size, currentBet);"""

new_bet_run = """        const isVirtual = (martingaleStep >= MAX_LOSS_LEVEL);
        const actualStakeToBet = isVirtual ? 0 : currentBet;

        if (activePeriod) {
          RECORDED_BETS.unshift({
            period: activePeriod,
            prediction: pred.size,
            mode: pred.mode,
            stake: currentBet,
            isVirtual: isVirtual,
            won: null,
            profit: null,
            isPending: true,
            time: new Date().toLocaleTimeString()
          });
          if (RECORDED_BETS.length > 50) RECORDED_BETS = RECORDED_BETS.slice(0, 50);
        }

        persistAll();
        updateHud();

        if (isVirtual) {
          console.log(`%c[🛑 2-LVL SHIELD ACTIVE] Skipping real bet on #${activePeriod}! Virtual paper bet on ${pred.size}. Your bankroll is 100% protected!`, 'background:#ff0055;color:#fff;font-weight:900;padding:6px 14px;border-radius:4px');
        } else {
          await executeBet(pred.size, actualStakeToBet);
        }"""

code = code.replace(old_bet_run, new_bet_run)

with open('generate_standalone_v26.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("generate_standalone_v26.py upgraded with Strict 2-Level Loss Shield successfully!")
