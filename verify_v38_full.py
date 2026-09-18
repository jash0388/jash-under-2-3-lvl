from million_rounds_deep_research import million_data, evaluate_strategy, test_candidate_both_ways, opp

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

def predict_apex_titan_v38(history, loss_streak):
    sizes = [h['size'] for h in history[-30:]]
    last = sizes[-1]
    
    runs = get_runs(sizes)
    curr_s, curr_l = runs[-1]
    prev_l = runs[-2][1] if len(runs) >= 2 else 1
    prev2_l = runs[-3][1] if len(runs) >= 3 else 1
    
    streak = curr_l
    recent_lens = [r[1] for r in runs[-6:]]
    avg_len = sum(recent_lens) / len(recent_lens)
    
    alt = 0
    for s, l in reversed(runs):
        if l == 1: alt += 1
        else: break

    # --- LEVEL 3 (AFTER 2 LOSSES) ---
    if loss_streak >= 2:
        if streak >= 3:
            return last, f'🛑 LVL 3 DRAGON LOCK ({last} x{streak})'
        elif streak == 2:
            if avg_len <= 2.0:
                return opp(last), f'🛑 LVL 3 DOUBLET CUT ({last} x2 -> FLIP)'
            return last, f'🛑 LVL 3 DRAGON TRY ({last} x2)'
        else: # streak == 1
            if prev_l == 1 and prev2_l == 2:
                return last, f'🛑 LVL 3 2-BALL PAIR ({last})'
            elif alt >= 3:
                return opp(last), f'🛑 LVL 3 CHOP FLIP (x{alt})'
            else:
                return last, f'🛑 LVL 3 MOMENTUM LOCK ({last})'

    # --- LEVEL 2 (AFTER 1 LOSS) ---
    elif loss_streak == 1:
        if streak >= 3:
            return last, f'🛡️ LVL 2 DRAGON LOCK ({last} x{streak})'
        elif streak == 2:
            if avg_len <= 2.0:
                return opp(last), f'🛡️ LVL 2 DOUBLET CUT ({last} x2)'
            return last, f'🛡️ LVL 2 DRAGON TRY ({last} x2)'
        else:
            if prev_l == 1 and prev2_l == 2:
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
            if avg_len <= 2.0:
                return opp(last), f'⚡ DOUBLET FLIP ({last} x2)'
            return last, f'🐉 DRAGON TRY ({last} x2)'
        else: # streak == 1
            if prev_l == 1 and prev2_l == 2:
                return last, f'👥 2-BALL PAIR ({last})'
            elif alt >= 3:
                return opp(last), f'⚡ CHOP OSCILLATE (x{alt})'
            else:
                return last, f'🌊 FLOW MOMENTUM ({last})'

print("=== 1. VERIFY ON USER SCREENSHOT (10859-10870) ===")
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

hist = []
loss_streak = 0
wins, losses, max_loss = 0, 0, 0
for r in seq_screenshot:
    if len(hist) < 3:
        hist.append(r)
        continue
    pred, reg = predict_apex_titan_v38(hist, loss_streak)
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

print("\n=== 2. BENCHMARK ON 2,000,000 ROUNDS (1M FORWARD + 1M REVERSE) ===")
test_candidate_both_ways(predict_apex_titan_v38, "Apex Titan V38 Cadence Master")
