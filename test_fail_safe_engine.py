# Let's test the Adaptive Derivative Self-Correcting Engine

# Exact sequence from user screenshot:
# 10848: BIG 9
# 10849: BIG 5
# 10850: SMALL 4
# 10851: SMALL 0
# 10852: SMALL 1
# 10853: SMALL 4
# 10854: BIG 5
# 10855: SMALL 1
# 10856: BIG 8

live_test_seq = [
    {'period': '10848', 'number': 9, 'size': 'BIG'},
    {'period': '10849', 'number': 5, 'size': 'BIG'},
    {'period': '10850', 'number': 4, 'size': 'SMALL'},
    {'period': '10851', 'number': 0, 'size': 'SMALL'},
    {'period': '10852', 'number': 1, 'size': 'SMALL'},
    {'period': '10853', 'number': 4, 'size': 'SMALL'},
    {'period': '10854', 'number': 5, 'size': 'BIG'},
    {'period': '10855', 'number': 1, 'size': 'SMALL'},
    {'period': '10856', 'number': 8, 'size': 'BIG'},
]

def opp(s): return 'SMALL' if s == 'BIG' else 'BIG'

def predict_fail_safe(history, loss_streak, last_pred_size=None):
    sizes = [h['size'] for h in history[-30:]]
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

    # --- LEVEL 3 (AFTER 2 LOSSES) ---
    if loss_streak >= 2:
        # If streak is 2, the market just stopped chopping and formed a pair -> FOLLOW
        if streak >= 2:
            return last, f'🛑 LVL 3 CONFIRMED STREAK ({last} x{streak})'
        # If alt is 2, the market just stopped repeating and started chopping -> FLIP
        elif alt >= 2:
            return opp(last), f'🛑 LVL 3 CONFIRMED CHOP (x{alt})'
        else:
            return last, f'🛑 LVL 3 MOMENTUM SYNC ({last})'

    # --- LEVEL 2 (AFTER 1 LOSS) ---
    elif loss_streak == 1:
        # If last bet was SAME and failed, the market FLIPPED -> now bet FLIP!
        # If last bet was FLIP and failed, the market REPEATED -> now bet SAME!
        if last_pred_size:
            # If our previous guess was same as previous ball (i.e. we guessed continuation), but it flipped:
            # Then we should now expect alternation -> bet OPP of current last!
            if alt >= 2:
                return opp(last), f'🛡️ LVL 2 CHOP FLIP (x{alt})'
            else:
                return last, f'🛡️ LVL 2 STREAK PERSIST ({last} x{streak})'
        else:
            if alt >= 2: return opp(last), f'🛡️ LVL 2 CHOP FLIP (x{alt})'
            return last, f'🛡️ LVL 2 MOMENTUM ({last})'

    # --- LEVEL 1 (NORMAL FLOW) ---
    else:
        # A. Established Dragon (streak >= 3)
        if streak >= 3 and streak <= 7:
            return last, f'🐉 DRAGON FLOW ({last} x{streak})'
        elif streak > 7:
            return opp(last), f'⚖️ FATIGUE CUT (x{streak})'
        # B. Active Chop (alt >= 2)
        elif alt >= 2:
            return opp(last), f'⚡ CHOP OSCILLATE (x{alt})'
        # C. Default Trend Follow
        else:
            return last, f'🌊 FLOW MOMENTUM ({last})'

# Run on the live sequence that gave 8 losses in V35:
print('=== TESTING FAIL-SAFE ADAPTIVE ENGINE ON USER LIVE SEQUENCE ===')
hist = [
    {'period': '10845', 'number': 4, 'size': 'SMALL'},
    {'period': '10846', 'number': 0, 'size': 'SMALL'},
    {'period': '10847', 'number': 1, 'size': 'SMALL'},
]

loss_streak = 0
last_pred = None
wins, losses = 0, 0
max_losses = 0

for r in live_test_seq:
    pred, reg = predict_fail_safe(hist, loss_streak, last_pred)
    last_pred = pred
    won = (pred == r['size'])
    if won:
        wins += 1
        lvl = 1 if loss_streak == 0 else loss_streak + 1
        status = f'✅ WIN (Lvl {lvl})'
        loss_streak = 0
    else:
        losses += 1
        loss_streak += 1
        max_losses = max(max_losses, loss_streak)
        status = f'❌ LOSS (Lvl {loss_streak})'
    print(f"{r['period']}: Pred={pred:5s} | Act={r['size']:5s}({r['number']}) | {status:15s} | {reg}")
    hist.append(r)

print(f'\nTotal: {wins+losses} | Wins: {wins} | Losses: {losses} | Win Rate: {wins/(wins+losses)*100:.1f}%')
print(f'MAX CONSECUTIVE LOSSES = {max_losses}')
