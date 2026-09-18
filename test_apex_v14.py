real_24 = [
    {'period': '1361', 'number': 0, 'size': 'SMALL'},
    {'period': '1362', 'number': 8, 'size': 'BIG'},
    {'period': '1363', 'number': 7, 'size': 'BIG'},
    {'period': '1364', 'number': 1, 'size': 'SMALL'},
    {'period': '1365', 'number': 4, 'size': 'SMALL'},
    {'period': '1366', 'number': 1, 'size': 'SMALL'},
    {'period': '1367', 'number': 1, 'size': 'SMALL'},
    {'period': '1368', 'number': 6, 'size': 'BIG'},
    {'period': '1369', 'number': 6, 'size': 'BIG'},
    {'period': '1370', 'number': 8, 'size': 'BIG'},
    {'period': '1371', 'number': 1, 'size': 'SMALL'},
    {'period': '1372', 'number': 2, 'size': 'SMALL'},
    {'period': '1373', 'number': 0, 'size': 'SMALL'},
    {'period': '1374', 'number': 6, 'size': 'BIG'},
    {'period': '1375', 'number': 0, 'size': 'SMALL'},
    {'period': '1376', 'number': 2, 'size': 'SMALL'},
    {'period': '1377', 'number': 8, 'size': 'BIG'},
    {'period': '1378', 'number': 6, 'size': 'BIG'},
    {'period': '1379', 'number': 0, 'size': 'SMALL'},
    {'period': '1380', 'number': 9, 'size': 'BIG'},
    {'period': '1381', 'number': 3, 'size': 'SMALL'},
    {'period': '1382', 'number': 7, 'size': 'BIG'},
    {'period': '1383', 'number': 5, 'size': 'BIG'},
    {'period': '1384', 'number': 0, 'size': 'SMALL'},
]

real_prev = [
    {'period': '1097', 'number': 8, 'size': 'BIG'},
    {'period': '1098', 'number': 1, 'size': 'SMALL'},
    {'period': '1099', 'number': 9, 'size': 'BIG'},
    {'period': '1100', 'number': 4, 'size': 'SMALL'},
    {'period': '1101', 'number': 1, 'size': 'SMALL'},
    {'period': '1102', 'number': 2, 'size': 'SMALL'},
    {'period': '1103', 'number': 2, 'size': 'SMALL'},
    {'period': '1104', 'number': 7, 'size': 'BIG'},
    {'period': '1105', 'number': 6, 'size': 'BIG'},
]

def engine_apex_v14(history, loss_streak):
    sizes = [h['size'] for h in history]
    last = sizes[-1]
    
    # 1. Blocks & Streak tracking
    blocks = []
    curr = sizes[0]
    l = 1
    for s in sizes[1:]:
        if s == curr: l += 1
        else:
            blocks.append((curr, l))
            curr = s
            l = 1
    blocks.append((curr, l))
    
    curr_streak = blocks[-1][1]
    prev_streak = blocks[-2][1] if len(blocks) >= 2 else 1
    prev_prev_streak = blocks[-3][1] if len(blocks) >= 3 else 1
    
    # 2. Alternation count
    alt = 1
    for i in range(len(sizes)-1, 0, -1):
        if sizes[i] != sizes[i-1]: alt += 1
        else: break
        
    # --- LEVEL 3 EMERGENCY OVERRIDE (AFTER 2 LOSSES) ---
    # After 2 consecutive losses:
    # If loss 1 was at streak break, and loss 2 was at single chop,
    # then sequence is in a Doublet (2-2) or Alternation (1-1).
    if loss_streak >= 2:
        # If current streak is 1, it's the 1st of a block -> bet same (to catch doublet)
        # If current streak is 2, it's the 2nd of a block -> bet opposite (to catch flip)
        if curr_streak == 1:
            return last, "🛑 LEVEL 3 DOUBLET LOCK (1st->2nd)"
        else:
            return ('SMALL' if last == 'BIG' else 'BIG'), "🛑 LEVEL 3 DOUBLET FLIP (2nd->Flip)"

    # --- LEVEL 2 RECOVERY (AFTER 1 LOSS) ---
    if loss_streak == 1:
        # We lost 1 round. Why?
        # Case A: We followed a dragon of length >= 3 and it just broke (curr_streak == 1, prev_streak >= 3).
        # In WinGo, a dragon break frequently produces a "pullback" (false breakout) back to the dragon side!
        # OR it starts a 2-2 pattern.
        if prev_streak >= 3 and curr_streak == 1:
            # Rebound back to previous dragon side!
            return blocks[-2][0], "🛡️ LEVEL 2 DRAGON PULLBACK"
        # Case B: We were in 1-1 chop and it doubled up (curr_streak == 2).
        elif curr_streak == 2:
            return last, "🛡️ LEVEL 2 MOMENTUM SYNC"
        else:
            return last, "🛡️ LEVEL 2 AUTO-SHIELD"

    # --- LEVEL 1 (NORMAL PLAY) ---
    # 1. Active 1-1 Alternation Wave (alt >= 3)
    if alt >= 3:
        return ('SMALL' if last == 'BIG' else 'BIG'), f"⚡ ZIGZAG OSCILLATION ({alt} Waves)"
        
    # 2. Dragon Persistence (streak >= 2 and <= 7)
    if curr_streak >= 2 and curr_streak <= 7:
        return last, f"🐉 DRAGON FLOW ({last} x{curr_streak})"
        
    # 3. Extreme Fatigue Reversal (> 7)
    if curr_streak > 7:
        return ('SMALL' if last == 'BIG' else 'BIG'), f"⚖️ FATIGUE REVERSAL (x{curr_streak})"
        
    # 4. If previous was 2-2 doublet sequence
    if prev_streak == 2 and prev_prev_streak == 2 and curr_streak == 1:
        return last, "🧬 2-2 DOUBLET SYNC"
        
    # 5. Default: Follow Last Momentum
    return last, "🌊 FLOW MOMENTUM"

print("\n================== TESTING ENGINE APEX V14 ON TODAY REAL 24 ==================")
history = []
loss_streak = 0
max_loss_streak = 0
wins, losses = 0, 0
cycle_wins, cycle_busts = 0, 0
l1_w, l2_w, l3_w = 0, 0, 0

for r in real_24:
    if len(history) < 3:
        history.append(r)
        continue
    pred_size, regime = engine_apex_v14(history, loss_streak)
    won = (pred_size == r['size'])
    if won:
        wins += 1
        cycle_wins += 1
        if loss_streak == 0: l1_w += 1
        elif loss_streak == 1: l2_w += 1
        elif loss_streak == 2: l3_w += 1
        loss_streak = 0
    else:
        losses += 1
        loss_streak += 1
        max_loss_streak = max(max_loss_streak, loss_streak)
        if loss_streak > 2:
            cycle_busts += 1
            loss_streak = 0
    status_str = f"✅ WIN (Lvl {1 if loss_streak==0 and won and max_loss_streak==0 else (loss_streak if not won else loss_streak+1)})" if won else f"❌ LOSS (Lvl {loss_streak})"
    print(f"{r['period']}: Pred={pred_size:5s} ({regime:35s}) | Actual={r['size']:5s}({r['number']}) -> {status_str}")
    history.append(r)

print(f"\nRESULTS:")
print(f"  Total: Wins={wins}, Losses={losses} | Hit Rate={wins/(wins+losses)*100:.1f}%")
print(f"  MAX CONSECUTIVE LOSSES = {max_loss_streak}")
print(f"  Level 1 Wins: {l1_w} | Level 2 Wins: {l2_w} | Level 3 Wins: {l3_w}")
print(f"  Cycle Success Rate: {cycle_wins}/{cycle_wins+cycle_busts} ({cycle_wins/(cycle_wins+cycle_busts)*100:.1f}%)")
print(f"  Busts (> 2 losses): {cycle_busts}")

print("\n================== TESTING ENGINE APEX V14 ON PREV REAL 9 ==================")
history = []
loss_streak = 0
max_loss_streak = 0
wins, losses = 0, 0
cycle_wins, cycle_busts = 0, 0

for r in real_prev:
    if len(history) < 3:
        history.append(r)
        continue
    pred_size, regime = engine_apex_v14(history, loss_streak)
    won = (pred_size == r['size'])
    if won:
        wins += 1
        cycle_wins += 1
        loss_streak = 0
    else:
        losses += 1
        loss_streak += 1
        max_loss_streak = max(max_loss_streak, loss_streak)
        if loss_streak > 2:
            cycle_busts += 1
            loss_streak = 0
    status_str = f"✅ WIN" if won else f"❌ LOSS"
    print(f"{r['period']}: Pred={pred_size:5s} ({regime:35s}) | Actual={r['size']:5s}({r['number']}) -> {status_str}")
    history.append(r)

print(f"PREV RESULTS: Wins={wins}, Losses={losses}, Max Consecutive Losses={max_loss_streak}")
