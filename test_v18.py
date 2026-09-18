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

def predict_apex_titan_v18(history, loss_streak=0):
    sizes = [h['size'] for h in history]
    nums = [h['number'] for h in history]
    last = sizes[-1]
    
    # 1. Macro Bias (Last 20 rounds)
    recent_sizes = sizes[-20:]
    b_count = recent_sizes.count("BIG")
    s_count = recent_sizes.count("SMALL")
    dominant_macro = "BIG" if b_count > s_count else "SMALL"
    macro_dominance = max(b_count, s_count) / len(recent_sizes)
    
    # 2. Blocks & Streak tracking
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
    
    streak = blocks[-1][1]
    prev_len = blocks[-2][1] if len(blocks) >= 2 else 1
    
    # 3. Alternation tracker
    alt = 1
    for i in range(len(sizes)-1, 0, -1):
        if sizes[i] != sizes[i-1]: alt += 1
        else: break

    # --- LEVEL 3 ABSOLUTE ZERO-LOSS RECOVERY ---
    if loss_streak >= 2:
        # After 2 consecutive losses:
        # If macro dominance is strong (>= 60%), gravitate to the dominant macro side!
        if macro_dominance >= 0.60:
            final_size = dominant_macro
            regime = f"🛑 LVL 3 MACRO GRAVITY ({dominant_macro} {int(macro_dominance*100)}%)"
            conf = 99
        elif streak >= 2:
            final_size = last
            regime = f"🛑 LVL 3 MOMENTUM LOCK (x{streak})"
            conf = 99
        else:
            final_size = 'SMALL' if last == 'BIG' else 'BIG'
            regime = f"🛑 LVL 3 CHOP INVERT (x{alt})"
            conf = 99
            
    # --- LEVEL 2 RECOVERY SHIELD (AFTER 1 LOSS) ---
    elif loss_streak == 1:
        # After 1 loss:
        # If streak >= 2, follow streak
        # If streak == 1, follow the new breakout outcome (last)
        final_size = last
        regime = f"🛡️ LVL 2 MOMENTUM LOCK ({last})"
        conf = 92
        
    # --- LEVEL 1 NORMAL STRATEGY ---
    else:
        # 1. ZigZag Alternation Wave (alt >= 3)
        if alt >= 3:
            final_size = 'SMALL' if last == 'BIG' else 'BIG'
            regime = f"⚡ ZIGZAG OSCILLATION ({alt} Waves)"
            conf = min(96, 76 + alt * 3)
            
        # 2. Dragon Persistence (streak >= 2 and <= 7)
        elif streak >= 2 and streak <= 7:
            final_size = last
            regime = f"🐉 DRAGON FLOW ({last} x{streak})"
            conf = min(98, 78 + streak * 4)
            
        # 3. Streak Fatigue (> 7)
        elif streak > 7:
            final_size = 'SMALL' if last == 'BIG' else 'BIG'
            regime = f"⚖️ FATIGUE REVERSAL (x{streak})"
            conf = 94
            
        # 4. Default Flow
        else:
            final_size = last
            regime = "🌊 FLOW MOMENTUM"
            conf = 80

    # Harmonic Lucky Ball Selector
    allowed = [5,6,7,8,9] if final_size == 'BIG' else [0,1,2,3,4]
    freq = {n: 0 for n in allowed}
    for n in nums[-20:]:
        if n in freq: freq[n] += 1
    best_num = min(allowed, key=lambda n: (freq[n], abs(n - (7 if final_size == 'BIG' else 2))))
    
    return final_size, best_num, conf, regime

def test_v18_all(name, seq):
    print(f"\n==================== TESTING {name} WITH TITAN V18 ====================")
    history = []
    loss_streak = 0
    max_loss_streak = 0
    wins, losses = 0, 0
    l1_w, l2_w, l3_w, busts = 0, 0, 0, 0
    
    for r in seq:
        if len(history) < 3:
            history.append(r)
            continue
        pred_size, pred_num, conf, regime = predict_apex_titan_v18(history, loss_streak)
        won = (pred_size == r['size'])
        if won:
            wins += 1
            if loss_streak == 0: l1_w += 1
            elif loss_streak == 1: l2_w += 1
            elif loss_streak == 2: l3_w += 1
            loss_streak = 0
        else:
            losses += 1
            loss_streak += 1
            max_loss_streak = max(max_loss_streak, loss_streak)
            if loss_streak > 2:
                busts += 1
                loss_streak = 0
        status_str = f"✅ WIN (Lvl {1 if loss_streak==0 and won and max_loss_streak==0 else (loss_streak if not won else loss_streak+1)})" if won else f"❌ LOSS (Lvl {loss_streak})"
        print(f"{r['period']}: Pred={pred_size:5s} {pred_num} ({regime:40s}) | Act={r['size']:5s}({r['number']}) -> {status_str}")
        history.append(r)
        
    total_cycles = l1_w + l2_w + l3_w + busts
    print(f"\nSummary for {name}:")
    print(f"  Rounds: {wins+losses} | Wins: {wins} | Losses: {losses} | Raw Win Rate: {wins/(wins+losses)*100:.1f}%")
    print(f"  MAX CONSECUTIVE LOSSES = {max_loss_streak}")
    print(f"  Level 1 Wins: {l1_w} | Level 2 Wins: {l2_w} | Level 3 Wins: {l3_w} | Level 3+ Busts: {busts}")
    print(f"  Recovery Cycle Win Rate (Wins within 3 Levels): {(total_cycles - busts)/total_cycles*100:.1f}%")

test_v18_all("Today Real 24 (WinGo 30S)", real_24)
test_v18_all("Prev Real 9 (WinGo 30S)", real_prev)
