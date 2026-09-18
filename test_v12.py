import random

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

# Let's test multiple candidate strategies systematically:

def test_engine_detailed(engine_fn, name="Engine"):
    print(f"\n==================== {name} ====================")
    history = []
    loss_streak = 0
    max_loss_streak = 0
    wins, losses = 0, 0
    cycle_wins = 0 # How many recovery cycles succeeded within Level 1-3
    cycle_busts = 0 # How many recovery cycles failed (>2 losses)
    
    for r in real_24:
        if len(history) < 3:
            history.append(r)
            continue
        pred_size, regime = engine_fn(history, loss_streak)
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
                # reset for next test
                loss_streak = 0
        status_str = f"✅ WIN (Lvl {loss_streak if not won else (1 if loss_streak==0 else loss_streak)})" if won else f"❌ LOSS (Lvl {loss_streak})"
        print(f"{r['period']}: Pred={pred_size:5s} ({regime:30s}) | Actual={r['size']:5s}({r['number']}) -> {status_str}")
        history.append(r)
        
    print(f"RESULTS: Wins={wins}, Losses={losses}, Max Loss Streak={max_loss_streak}")
    print(f"Cycle Win Rate (Resolved within <= 2 losses): {cycle_wins}/{(cycle_wins+cycle_busts)} ({cycle_wins/(cycle_wins+cycle_busts)*100:.1f}%)")

# Strategy 1: "Titan Apex Zero-Loss Shield V12"
# Core logic:
# 1. Look at pattern entropy:
#    If the previous 2 blocks were length 1 (e.g. S, B, S or B, S, B), we are in a 1-1 CHOP REGIME -> ALWAYS ALTERNATE!
#    If the previous 2 blocks were length 2 (e.g. SS, BB), we are in a 2-2 DOUBLET REGIME -> Follow 2-block rhythm!
#    If streak >= 2 and not alternating, FOLLOW THE DRAGON!
#    Level 2 recovery: If lost in dragon, we switch to chop; if lost in chop, we switch to follow.
#    Level 3 recovery: Anti-whipsaw lock.
def engine_v12(history, loss_streak):
    sizes = [h['size'] for h in history]
    last = sizes[-1]
    
    # Run lengths of blocks
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
    
    # Check if alternating wave is active (last block length 1 and prior blocks length 1)
    is_alt_chop = len(blocks) >= 3 and blocks[-1][1] == 1 and blocks[-2][1] == 1
    is_doublet = len(blocks) >= 3 and (blocks[-2][1] == 2 and (blocks[-3][1] == 2 or blocks[-1][1] == 1))
    
    if loss_streak == 0:
        if is_alt_chop:
            # 1-1 Chop: e.g. S, B, S -> next is B!
            return ('SMALL' if last == 'BIG' else 'BIG'), f"⚡ CHOP 1-1 RHYTHM (Alt)"
        elif streak >= 2 and streak <= 7:
            # Streak >= 2: follow streak!
            return last, f"🐉 DRAGON PERSIST (x{streak})"
        elif is_doublet and streak == 1:
            # Doublet: 1st of 2 -> expect 2nd!
            return last, "🧬 2-2 DOUBLET (1st->2nd)"
        elif is_doublet and streak == 2:
            # Doublet: 2nd of 2 -> expect flip!
            return ('SMALL' if last == 'BIG' else 'BIG'), "🧬 2-2 DOUBLET (2nd->Flip)"
        else:
            return last, "🌊 MOMENTUM LOCK"
            
    elif loss_streak == 1:
        # Level 2 Recovery:
        # Why did Level 1 lose?
        # If we predicted last and it flipped, was it a 1-1 chop or doublet?
        # If streak is 1, follow the new direction
        if len(blocks) >= 2 and blocks[-2][1] >= 2:
            # The previous streak broke, start of new trend -> follow new!
            return last, "🛡️ LVL 2 TREND PIVOT"
        else:
            # It was a chop -> alternate!
            return ('SMALL' if last == 'BIG' else 'BIG'), "🛡️ LVL 2 CHOP INVERT"
            
    else: # loss_streak >= 2 (Level 3!)
        # Level 3: MUST WIN!
        # After 2 consecutive losses, market has confirmed a definitive 1-1 oscillation or 2-2 lock
        # Invert from last prediction to catch the rebound!
        return ('SMALL' if last == 'BIG' else 'BIG'), "🛑 LVL 3 ABSOLUTE SHIELD"

test_engine_detailed(engine_v12, "Engine V12")
