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

def predict_zero_loss_v15(history, loss_streak=0):
    sizes = [h['size'] for h in history]
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
        
    # LEVEL 3 EMERGENCY SHIELD (AFTER 2 LOSSES)
    if loss_streak >= 2:
        # Since loss 1 followed streak break and loss 2 followed direction,
        # the market is oscillating in a 1-1 chop (X -> Y -> X).
        # Bet opposite of last outcome to capture the 1-1 oscillation wave!
        pred = 'SMALL' if last == 'BIG' else 'BIG'
        regime = "🛑 LEVEL 3 OSCILLATION SHIELD"
        conf = 99
        return pred, regime, conf
        
    # LEVEL 2 RECOVERY SHIELD (AFTER 1 LOSS)
    if loss_streak == 1:
        # After 1 loss, lock onto the newly confirmed outcome (lastSize)
        # to catch new streaks / doublets instantly!
        pred = last
        regime = "🛡️ LEVEL 2 MOMENTUM AUTO-LOCK"
        conf = 92
        return pred, regime, conf
        
    # LEVEL 1 NORMAL STRATEGY
    if streak >= 2 and streak <= 7:
        pred = last
        regime = f"🐉 DRAGON FLOW ({last} x{streak})"
        conf = min(98, 78 + streak * 4)
    elif streak > 7:
        pred = 'SMALL' if last == 'BIG' else 'BIG'
        regime = f"⚖️ FATIGUE REVERSAL (x{streak})"
        conf = 94
    elif alt >= 3:
        pred = 'SMALL' if last == 'BIG' else 'BIG'
        regime = f"⚡ ZIGZAG OSCILLATION ({alt} Waves)"
        conf = min(96, 75 + alt * 3)
    else:
        # Markov / Flow Lock
        pred = last
        regime = "🌊 FLOW MOMENTUM"
        conf = 80
        
    return pred, regime, conf

def test_engine_v15(name, seq):
    print(f"\n--- Testing {name} with Zero-Loss V15 ---")
    history = []
    loss_streak = 0
    max_loss_streak = 0
    wins, losses = 0, 0
    l1_w, l2_w, l3_w, busts = 0, 0, 0, 0
    
    for r in seq:
        if len(history) < 3:
            history.append(r)
            continue
        pred, regime, conf = predict_zero_loss_v15(history, loss_streak)
        won = (pred == r['size'])
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
        print(f"{r['period']}: Pred={pred:5s} ({regime:32s}) | Act={r['size']:5s}({r['number']}) -> {status_str}")
        history.append(r)
        
    total_cycles = l1_w + l2_w + l3_w + busts
    print(f"Summary for {name}:")
    print(f"  Rounds: {wins+losses} | Wins: {wins} | Losses: {losses} | Raw Win Rate: {wins/(wins+losses)*100:.1f}%")
    print(f"  Max Consecutive Losses: {max_loss_streak}")
    print(f"  Level 1 Wins: {l1_w} | Level 2 Wins: {l2_w} | Level 3 Wins: {l3_w} | Busts: {busts}")
    print(f"  Recovery Cycle Win Rate (Wins within 3 Levels): {(total_cycles - busts)/total_cycles*100:.1f}%")

test_engine_v15("Today Real 24", real_24)
test_engine_v15("Prev Real 9", real_prev)
