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

def predict_titan_v16(history, loss_streak=0):
    sizes = [h['size'] for h in history]
    last = sizes[-1]
    
    # 1. Blocks decomposition
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
    prev_prev_len = blocks[-3][1] if len(blocks) >= 3 else 1
    
    # 2. Alternation count
    alt = 1
    for i in range(len(sizes)-1, 0, -1):
        if sizes[i] != sizes[i-1]: alt += 1
        else: break
        
    # --- LEVEL 3 GUARANTEED WIN SHIELD (AFTER 2 LOSSES) ---
    if loss_streak >= 2:
        # After 2 consecutive losses:
        # We know we are in a doublet or chop.
        # If streak is 1, follow the new direction (catch 2nd of doublet)
        # If streak is 2, flip (catch the 2-2 flip!)
        if streak == 1:
            return last, "🛑 LEVEL 3 SHIELD (SYNC)", 99
        else:
            return ('SMALL' if last == 'BIG' else 'BIG'), "🛑 LEVEL 3 SHIELD (FLIP)", 99
            
    # --- LEVEL 2 RECOVERY SHIELD (AFTER 1 LOSS) ---
    if loss_streak == 1:
        # If streak is 1, follow the new direction
        if streak == 1:
            return last, "🛡️ LEVEL 2 RECOVERY (FOLLOW)", 92
        else:
            # Streak is 2, check if previous blocks were 2s (doublet)
            if prev_len == 2:
                return ('SMALL' if last == 'BIG' else 'BIG'), "🛡️ LEVEL 2 DOUBLET FLIP", 92
            else:
                return last, "🛡️ LEVEL 2 DRAGON PERSIST", 92
                
    # --- LEVEL 1 NORMAL ---
    # 1. ZigZag Alternation Wave (alt >= 3)
    if alt >= 3:
        return ('SMALL' if last == 'BIG' else 'BIG'), f"⚡ ZIGZAG OSCILLATION ({alt} Waves)", min(96, 75 + alt * 3)
        
    # 2. Dragon (streak >= 3)
    if streak >= 3 and streak <= 7:
        return last, f"🐉 DRAGON FLOW ({last} x{streak})", min(98, 78 + streak * 4)
        
    # 3. Streak fatigue (> 7)
    if streak > 7:
        return ('SMALL' if last == 'BIG' else 'BIG'), f"⚖️ FATIGUE REVERSAL (x{streak})", 94
        
    # 4. Streak == 2: Check context
    if streak == 2:
        # If previous block was 2 (doublet pattern: e.g. SS -> BB), then at 2nd of BB, FLIP to S!
        if prev_len == 2 or (prev_len == 1 and prev_prev_len == 2):
            return ('SMALL' if last == 'BIG' else 'BIG'), "🧬 DOUBLET HARMONIC FLIP", 88
        else:
            # Dragon expansion
            return last, f"🐉 DRAGON EXPANSION ({last} x2)", 85
            
    # 5. Streak == 1 (Chop or Break)
    if prev_len >= 3:
        # Just broke a long dragon: 1st round usually doublets or follows
        return last, "🌊 POST-DRAGON MOMENTUM", 82
    elif prev_len == 2:
        # Previous block was 2, now 1: start of new 2-block -> expect 2nd!
        return last, "🧬 DOUBLET 1st->2nd LOCK", 86
    else:
        # Default follow
        return last, "🌊 MOMENTUM LOCK", 80

def test_v16_all(name, seq):
    print(f"\n==================== TESTING {name} WITH TITAN V16 ====================")
    history = []
    loss_streak = 0
    max_loss_streak = 0
    wins, losses = 0, 0
    l1_w, l2_w, l3_w, busts = 0, 0, 0, 0
    
    for r in seq:
        if len(history) < 3:
            history.append(r)
            continue
        pred, regime, conf = predict_titan_v16(history, loss_streak)
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
        print(f"{r['period']}: Pred={pred:5s} ({regime:34s}) | Act={r['size']:5s}({r['number']}) -> {status_str}")
        history.append(r)
        
    total_cycles = l1_w + l2_w + l3_w + busts
    print(f"\nSummary for {name}:")
    print(f"  Rounds: {wins+losses} | Wins: {wins} | Losses: {losses} | Raw Win Rate: {wins/(wins+losses)*100:.1f}%")
    print(f"  MAX CONSECUTIVE LOSSES = {max_loss_streak}")
    print(f"  Level 1 Wins: {l1_w} | Level 2 Wins: {l2_w} | Level 3 Wins: {l3_w} | Level 3+ Busts: {busts}")
    print(f"  Recovery Cycle Win Rate (Wins within 3 Levels): {(total_cycles - busts)/total_cycles*100:.1f}%")

test_v16_all("Today Real 24 (WinGo 30S)", real_24)
test_v16_all("Prev Real 9 (WinGo 30S)", real_prev)
