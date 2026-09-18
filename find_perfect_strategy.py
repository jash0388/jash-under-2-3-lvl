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

def evaluate_engine(engine_fn):
    results = {}
    for name, seq in [("Today Real 24", real_24), ("Prev Real 9", real_prev)]:
        history = []
        loss_streak = 0
        max_loss_streak = 0
        wins, losses = 0, 0
        lvl1_w, lvl2_w, lvl3_w, busts = 0, 0, 0, 0
        last_pred = None
        for r in seq:
            if len(history) < 3:
                history.append(r)
                continue
            pred_size, regime = engine_fn(history, loss_streak, last_pred)
            last_pred = pred_size
            won = (pred_size == r['size'])
            if won:
                wins += 1
                if loss_streak == 0: lvl1_w += 1
                elif loss_streak == 1: lvl2_w += 1
                elif loss_streak == 2: lvl3_w += 1
                loss_streak = 0
            else:
                losses += 1
                loss_streak += 1
                max_loss_streak = max(max_loss_streak, loss_streak)
                if loss_streak > 3: busts += 1
            history.append(r)
        results[name] = {
            'wins': wins, 'losses': losses, 'max_loss_streak': max_loss_streak,
            'l1': lvl1_w, 'l2': lvl2_w, 'l3': lvl3_w, 'busts': busts,
            'rate': wins / (wins + losses) * 100 if (wins + losses) else 0
        }
    return results

# Let's test different approaches:

# Approach A: Pure Trend Follow with Dynamic Level 2/3 Pivot
def engine_pure_trend(history, loss_streak, last_pred):
    sizes = [h['size'] for h in history]
    last = sizes[-1]
    
    # 1. Streak
    streak = 1
    for i in range(len(sizes)-2, -1, -1):
        if sizes[i] == last: streak += 1
        else: break
        
    # 2. Alternation
    alt = 1
    for i in range(len(sizes)-1, 0, -1):
        if sizes[i] != sizes[i-1]: alt += 1
        else: break
        
    if loss_streak == 0:
        # Level 1: Ride dragon if streak >= 2, ride zigzag if alt >= 3
        if streak >= 2: return last, f"DRAGON x{streak}"
        if alt >= 3: return 'SMALL' if last == 'BIG' else 'BIG', f"ZIGZAG x{alt}"
        return last, "FOLLOW LAST"
    elif loss_streak == 1:
        # Level 2 (1 loss): 
        # We lost either because streak broke (now streak=1) or zigzag broke (now streak=2)
        # If streak is 1, it just flipped. Does it continue flipping (1-1 chop) or start a new streak?
        # If we bet last, we assume it's a new streak (or doublet).
        return last, "LEVEL 2 LOCK"
    else: # loss_streak >= 2 (Level 3!)
        # Level 3: We lost 2 times in a row!
        # Why did we lose 2 times?
        # Round -2: X. Round -1: Y (we bet X -> lost). Round 0: X (we bet Y -> lost).
        # So the sequence was X -> Y -> X!
        # Sequence is STRICTLY alternating 1-1! (X, Y, X)
        # Therefore, at Level 3, the next item in X->Y->X is ALWAYS Y! (Opposite of last!)
        return 'SMALL' if last == 'BIG' else 'BIG', "LEVEL 3 INVERT SHIELD"

print("--- Engine Pure Trend + Level 3 Invert Shield ---")
res = evaluate_engine(engine_pure_trend)
for k, v in res.items():
    print(k, v)
