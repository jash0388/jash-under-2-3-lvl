# Complete test of Universal Pattern State Machine for 1M & 30S

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

def predict_universal_titan_v22(history, loss_streak=0):
    if len(history) < 3:
        return 'BIG', 7, 70, 'INIT'
        
    sizes = [h['size'] for h in history[-40:]]
    nums = [h['number'] for h in history[-40:]]
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
    
    curr_streak = blocks[-1][1]
    prev_len = blocks[-2][1] if len(blocks) >= 2 else 1
    prev_prev_len = blocks[-3][1] if len(blocks) >= 3 else 1
    
    # 2. Alternation Tracker
    alt = 1
    for i in range(len(sizes)-1, 0, -1):
        if sizes[i] != sizes[i-1]: alt += 1
        else: break
        
    # Detect Doublet Regime: if recent blocks had 2s
    recent_lens = [b[1] for b in blocks[-4:-1]]
    is_doublet_context = (2 in recent_lens) or (prev_len == 2)
    
    final_size = "BIG"
    conf = 80
    regime = "TITAN FLOW"
    
    # --- LEVEL 3 EMERGENCY SHIELD (AFTER 2 LOSSES) ---
    if loss_streak >= 2:
        if curr_streak >= 2:
            # Confirmed streak -> follow
            final_size = last
            regime = f"🛑 LVL 3 DRAGON SHIELD (Follow x{curr_streak})"
            conf = 99
        else:
            # streak == 1 -> Invert alternation
            final_size = 'SMALL' if last == 'BIG' else 'BIG'
            regime = f"🛑 LVL 3 ALTERNATION SHIELD (Invert x{alt})"
            conf = 99
            
    # --- LEVEL 2 RECOVERY SHIELD (AFTER 1 LOSS) ---
    elif loss_streak == 1:
        # If we lost, did we lose because a 2-block doubled up or flipped?
        if curr_streak == 2 and is_doublet_context:
            final_size = 'SMALL' if last == 'BIG' else 'BIG'
            regime = "🛡️ LVL 2 DOUBLET FLIP"
            conf = 92
        elif curr_streak >= 2:
            final_size = last
            regime = f"🛡️ LVL 2 DRAGON PERSIST (x{curr_streak})"
            conf = 94
        else:
            final_size = last
            regime = f"🛡️ LVL 2 MOMENTUM LOCK ({last})"
            conf = 92
            
    # --- LEVEL 1 NORMAL STRATEGY ---
    else:
        # A. Dragon (streak >= 3)
        if curr_streak >= 3 and curr_streak <= 7:
            final_size = last
            regime = f"🐉 DRAGON FLOW ({last} x{curr_streak})"
            conf = min(98, 80 + curr_streak * 3)
            
        # B. Streak Fatigue (> 7)
        elif curr_streak > 7:
            final_size = 'SMALL' if last == 'BIG' else 'BIG'
            regime = f"⚖️ FATIGUE REVERSAL (x{curr_streak})"
            conf = 94
            
        # C. Streak == 2: Check if Doublet Regime
        elif curr_streak == 2:
            if is_doublet_context:
                final_size = 'SMALL' if last == 'BIG' else 'BIG'
                regime = "🧬 2-2 DOUBLET FLIP (2nd->Flip)"
                conf = 88
            else:
                final_size = last
                regime = f"🐉 DRAGON EXPANSION ({last} x2)"
                conf = 84
                
        # D. Streak == 1:
        elif curr_streak == 1:
            if prev_len == 2:
                # Previous was 2, now 1st of new block -> expect 2nd!
                final_size = last
                regime = "🧬 2-2 DOUBLET SYNC (1st->2nd)"
                conf = 89
            elif alt >= 3:
                # 1-1 Chop active
                final_size = 'SMALL' if last == 'BIG' else 'BIG'
                regime = f"⚡ ZIGZAG OSCILLATION ({alt} Waves)"
                conf = min(96, 76 + alt * 3)
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

def test_engine(name, seq):
    print(f"\n==================== TESTING {name} WITH UNIVERSAL V22 ====================")
    history = []
    loss_streak = 0
    max_loss_streak = 0
    wins, losses = 0, 0
    l1_w, l2_w, l3_w, busts = 0, 0, 0, 0
    
    for r in seq:
        if len(history) < 3:
            history.append(r)
            continue
        pred_size, pred_num, conf, regime = predict_universal_titan_v22(history, loss_streak)
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
    print(f"  Recovery Cycle Win Rate: {(total_cycles - busts)/total_cycles*100:.1f}%")

test_engine("WinGo 1M Screenshot (10722-10741)", seq_1m)
test_engine("WinGo 30S Latest (1406-1417)", seq_30s_latest)
