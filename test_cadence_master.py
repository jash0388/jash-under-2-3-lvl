# Let's write the true Cadence Phase Resolver that solves 1-2-1-2, 2-2-2, Dragons, and Chops!

def get_runs(sizes):
    runs = []
    curr = sizes[0]
    l = 1
    for s in sizes[1:]:
        if s == curr: l += 1
        else:
            runs.append((curr, l))
            curr = s
            l = 1
    runs.append((curr, l))
    return runs

def opp(s): return 'SMALL' if s == 'BIG' else 'BIG'

def predict_cadence_master(history, loss_streak):
    sizes = [h['size'] for h in history[-30:]]
    last = sizes[-1]
    
    runs = get_runs(sizes)
    curr_s, curr_l = runs[-1]
    prev_l = runs[-2][1] if len(runs) >= 2 else 1
    prev2_l = runs[-3][1] if len(runs) >= 3 else 1
    
    # 1. Measure active streak
    streak = curr_l
    
    # 2. Measure recent pattern lengths
    recent_lens = [r[1] for r in runs[-6:]]
    avg_len = sum(recent_lens) / len(recent_lens)
    
    # 3. Check for 1-2-1-2 cadence in recent runs:
    # If recent runs have alternating 1s and 2s (e.g. [1, 2, 1] or [2, 1, 2])
    is_1_2_cadence = (prev_l == 1 and prev2_l == 2) or (prev_l == 2 and prev2_l == 1) or (prev_l == 2 and recent_lens.count(2) >= 2)

    # 4. Check for pure 1-1 chop:
    alt = 0
    for s, l in reversed(runs):
        if l == 1: alt += 1
        else: break

    # --- LEVEL 3 (AFTER 2 LOSSES) ---
    if loss_streak >= 2:
        # If active streak >= 3 (confirmed dragon), ALWAYS follow!
        if streak >= 3:
            return last, f'🛑 LVL 3 DRAGON LOCK ({last} x{streak})'
        # If streak == 2:
        elif streak == 2:
            # If recent runs are <= 2, it is a doublet that terminates at 2 -> FLIP!
            if avg_len <= 2.2:
                return opp(last), f'🛑 LVL 3 DOUBLET CUT ({last} x2 -> FLIP)'
            return last, f'🛑 LVL 3 DRAGON TRY ({last} x2)'
        # If streak == 1:
        else:
            # If previous was 2, we just started the 1-ball in a 1-2 pattern -> FLIP!
            if prev_l == 2:
                return opp(last), f'🛑 LVL 3 1-BALL FLIP ({last})'
            # If previous was 1 and prev2 was 2, we just started the 2-ball in a 1-2 pattern -> REPEAT!
            elif prev_l == 1 and prev2_l == 2:
                return last, f'🛑 LVL 3 2-BALL PAIR ({last})'
            # If pure chop >= 3 -> FLIP
            elif alt >= 3:
                return opp(last), f'🛑 LVL 3 CHOP FLIP (x{alt})'
            else:
                return last, f'🛑 LVL 3 MOMENTUM LOCK ({last})'

    # --- LEVEL 2 (AFTER 1 LOSS) ---
    elif loss_streak == 1:
        if streak >= 3:
            return last, f'🛡️ LVL 2 DRAGON LOCK ({last} x{streak})'
        elif streak == 2:
            if avg_len <= 2.2:
                return opp(last), f'🛡️ LVL 2 DOUBLET CUT ({last} x2)'
            return last, f'🛡️ LVL 2 DRAGON TRY ({last} x2)'
        else: # streak == 1
            if prev_l == 2:
                return opp(last), f'🛡️ LVL 2 1-BALL FLIP ({last})'
            elif prev_l == 1 and prev2_l == 2:
                return last, f'🛡️ LVL 2 2-BALL PAIR ({last})'
            elif alt >= 3:
                return opp(last), f'🛡️ LVL 2 CHOP FLIP (x{alt})'
            else:
                return last, f'🛡️ LVL 2 MOMENTUM ({last})'

    # --- LEVEL 1 (NORMAL FLOW) ---
    else:
        if streak >= 3 and streak <= 7:
            return last, f'🐉 DRAGON FLOW ({last} x{streak})'
        elif streak > 7:
            return opp(last), f'⚖️ FATIGUE CUT (x{streak})'
        elif streak == 2:
            if avg_len <= 2.2:
                return opp(last), f'⚡ DOUBLET FLIP ({last} x2)'
            return last, f'🐉 DRAGON TRY ({last} x2)'
        elif streak == 1:
            if prev_l == 2:
                return opp(last), f'⚡ 1-BALL FLIP ({last})'
            elif prev_l == 1 and prev2_l == 2:
                return last, f'👥 2-BALL PAIR ({last})'
            elif alt >= 3:
                return opp(last), f'⚡ CHOP OSCILLATE (x{alt})'
            else:
                return last, f'🌊 FLOW MOMENTUM ({last})'

# Test on the exact sequence from the user's latest screenshot (10859..10870)
seq_screenshot = [
    {'period': '10859', 'number': 8, 'size': 'BIG'},
    {'period': '10860', 'number': 8, 'size': 'BIG'},
    {'period': '10861', 'number': 0, 'size': 'SMALL'},
    {'period': '10862', 'number': 2, 'size': 'SMALL'},
    {'period': '10863', 'number': 4, 'size': 'SMALL'},
    {'period': '10864', 'number': 2, 'size': 'SMALL'},
    {'period': '10865', 'number': 9, 'size': 'BIG'},
    {'period': '10866', 'number': 0, 'size': 'SMALL'},
    {'period': '10867', 'number': 0, 'size': 'SMALL'},
    {'period': '10868', 'number': 6, 'size': 'BIG'},
    {'period': '10869', 'number': 3, 'size': 'SMALL'},
    {'period': '10870', 'number': 1, 'size': 'SMALL'},
]

print('=== TESTING CADENCE MASTER ON USER SCREENSHOT (10859-10870) ===')
hist = []
loss_streak = 0
wins, losses, max_loss = 0, 0, 0

for r in seq_screenshot:
    if len(hist) < 3:
        hist.append(r)
        continue
    pred, reg = predict_cadence_master(hist, loss_streak)
    won = (pred == r['size'])
    if won:
        wins += 1
        lvl = 1 if loss_streak == 0 else loss_streak + 1
        status = f'✅ WIN (Lvl {lvl})'
        loss_streak = 0
    else:
        losses += 1
        loss_streak += 1
        max_loss = max(max_loss, loss_streak)
        status = f'❌ LOSS (Lvl {loss_streak})'
    print(f"{r['period']}: Pred={pred:5s} | Act={r['size']:5s}({r['number']}) | {status:15s} | {reg}")
    hist.append(r)

print(f'\nTotal: {wins+losses} | Wins: {wins} | Losses: {losses} | Win Rate: {wins/(wins+losses)*100:.1f}%')
print(f'MAX CONSECUTIVE LOSSES = {max_loss}')
