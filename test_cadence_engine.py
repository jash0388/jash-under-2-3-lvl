# Dual-Cadence Adaptive Markov Engine (V28)

seq_1m = [
    {'period': '10722', 'number': 0, 'size': 'SMALL'},
    {'period': '10723', 'number': 5, 'size': 'BIG'},
    {'period': '10724', 'number': 2, 'size': 'SMALL'},
    {'period': '10725', 'number': 5, 'size': 'BIG'},
    {'period': '10726', 'number': 6, 'size': 'BIG'},
    {'period': '10727', 'number': 0, 'size': 'SMALL'},
    {'period': '10728', 'number': 3, 'size': 'SMALL'},
    {'period': '10729', 'number': 8, 'size': 'BIG'},
    {'period': '10730', 'number': 0, 'size': 'SMALL'},
    {'period': '10731', 'number': 5, 'size': 'BIG'},
    {'period': '10732', 'number': 7, 'size': 'BIG'},
    {'period': '10733', 'number': 2, 'size': 'SMALL'},
    {'period': '10734', 'number': 5, 'size': 'BIG'},
    {'period': '10735', 'number': 2, 'size': 'SMALL'},
    {'period': '10736', 'number': 0, 'size': 'SMALL'},
    {'period': '10737', 'number': 1, 'size': 'SMALL'},
    {'period': '10738', 'number': 5, 'size': 'BIG'},
    {'period': '10739', 'number': 2, 'size': 'SMALL'},
    {'period': '10740', 'number': 1, 'size': 'SMALL'},
    {'period': '10741', 'number': 9, 'size': 'BIG'},
]

seq_30s_latest = [
    {'period': '1406', 'number': 4, 'size': 'SMALL'},
    {'period': '1407', 'number': 9, 'size': 'BIG'},
    {'period': '1408', 'number': 6, 'size': 'BIG'},
    {'period': '1409', 'number': 9, 'size': 'BIG'},
    {'period': '1410', 'number': 9, 'size': 'BIG'},
    {'period': '1411', 'number': 9, 'size': 'BIG'},
    {'period': '1412', 'number': 3, 'size': 'SMALL'},
    {'period': '1413', 'number': 5, 'size': 'BIG'},
    {'period': '1414', 'number': 2, 'size': 'SMALL'},
    {'period': '1415', 'number': 3, 'size': 'SMALL'},
    {'period': '1416', 'number': 4, 'size': 'SMALL'},
    {'period': '1417', 'number': 5, 'size': 'BIG'},
]

seq_30s_prev1 = [
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

def predict_dual_cadence_v28(history, loss_streak=0):
    if len(history) < 3:
        return 'BIG', 7, 70, 'INIT'
        
    sizes = [h['size'] for h in history[-50:]]
    nums = [h['number'] for h in history[-50:]]
    last = sizes[-1]
    
    # 1. Streak Tracker
    streak = 1
    for i in range(len(sizes)-2, -1, -1):
        if sizes[i] == last: streak += 1
        else: break
        
    # 2. Alternation Tracker
    alt = 1
    for i in range(len(sizes)-1, 0, -1):
        if sizes[i] != sizes[i-1]: alt += 1
        else: break
        
    # 3. Micro-Pattern Matcher (2-gram & 3-gram search in recent 50 rounds)
    p_big = 0.5
    if len(sizes) >= 6:
        # Check 2-gram
        k2 = (sizes[-2], sizes[-1])
        b_cnt, s_cnt = 0, 0
        for i in range(len(sizes) - 2):
            if (sizes[i], sizes[i+1]) == k2:
                if sizes[i+2] == 'BIG': b_cnt += 1
                else: s_cnt += 1
        if b_cnt + s_cnt >= 2:
            p_big = b_cnt / (b_cnt + s_cnt)

    final_size = "BIG"
    conf = 80
    regime = "CADENCE FLOW"
    
    # --- LEVEL 3 ABSOLUTE EMERGENCY SHIELD (AFTER 2 LOSSES) ---
    if loss_streak >= 2:
        # If active streak (>=2), follow it!
        if streak >= 2:
            final_size = last
            regime = f"🛑 LVL 3 DRAGON SHIELD (Follow x{streak})"
            conf = 99
        else:
            # streak == 1: Use micro-pattern transition probability
            if p_big > 0.55:
                final_size = 'BIG'
                regime = "🛑 LVL 3 PATTERN LOCK (BIG)"
                conf = 99
            elif p_big < 0.45:
                final_size = 'SMALL'
                regime = "🛑 LVL 3 PATTERN LOCK (SMALL)"
                conf = 99
            else:
                # Default: Invert alternation wave
                final_size = 'SMALL' if last == 'BIG' else 'BIG'
                regime = f"🛑 LVL 3 CHOP INVERT (x{alt})"
                conf = 99
                
    # --- LEVEL 2 RECOVERY SHIELD (AFTER 1 LOSS) ---
    elif loss_streak == 1:
        if streak >= 2:
            final_size = last
            regime = f"🛡️ LVL 2 DRAGON PERSIST ({last} x{streak})"
            conf = 94
        else:
            if p_big > 0.60:
                final_size = 'BIG'
                regime = "🛡️ LVL 2 N-GRAM LOCK (BIG)"
                conf = 92
            elif p_big < 0.40:
                final_size = 'SMALL'
                regime = "🛡️ LVL 2 N-GRAM LOCK (SMALL)"
                conf = 92
            else:
                final_size = last
                regime = f"🛡️ LVL 2 MOMENTUM LOCK ({last})"
                conf = 92
                
    # --- LEVEL 1 NORMAL FLOW ---
    else:
        # A. Strong Dragon (streak >= 3)
        if streak >= 3 and streak <= 7:
            final_size = last
            regime = f"🐉 DRAGON FLOW ({last} x{streak})"
            conf = min(98, 80 + streak * 3)
            
        # B. Streak Fatigue (> 7)
        elif streak > 7:
            final_size = 'SMALL' if last == 'BIG' else 'BIG'
            regime = f"⚖️ FATIGUE REVERSAL (x{streak})"
            conf = 94
            
        # C. ZigZag Wave (alt >= 3)
        elif alt >= 3:
            final_size = 'SMALL' if last == 'BIG' else 'BIG'
            regime = f"⚡ ZIGZAG OSCILLATION ({alt} Waves)"
            conf = min(96, 76 + alt * 3)
            
        # D. Micro-Pattern Consensus
        elif p_big >= 0.65:
            final_size = 'BIG'
            regime = "🧠 N-GRAM CADENCE (BIG)"
            conf = int(p_big * 100)
        elif p_big <= 0.35:
            final_size = 'SMALL'
            regime = "🧠 N-GRAM CADENCE (SMALL)"
            conf = int((1 - p_big) * 100)
            
        # E. Default Momentum Lock
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

def test_v28(name, seq):
    print(f"\n==================== TESTING {name} WITH DUAL-CADENCE V28 ====================")
    history = []
    loss_streak = 0
    max_loss_streak = 0
    wins, losses = 0, 0
    l1_w, l2_w, l3_w, busts = 0, 0, 0, 0
    
    for r in seq:
        if len(history) < 3:
            history.append(r)
            continue
        pred_size, pred_num, conf, regime = predict_dual_cadence_v28(history, loss_streak)
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

test_v28("WinGo 1M Screenshot (10722-10741)", seq_1m)
test_v28("WinGo 30S Latest (1406-1417)", seq_30s_latest)
test_v28("WinGo 30S (1361-1384)", seq_30s_prev1)
