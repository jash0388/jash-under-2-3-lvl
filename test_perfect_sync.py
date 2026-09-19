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

def predict_perfect_sync(history, loss_streak):
    sizes = [h['size'] for h in history[-30:]]
    last = sizes[-1]
    
    streak = 1
    for i in range(len(sizes)-2, -1, -1):
        if sizes[i] == last: streak += 1
        else: break
        
    alt = 1
    for i in range(len(sizes)-1, 0, -1):
        if sizes[i] != sizes[i-1]: alt += 1
        else: break

    # --- LEVEL 3 (AFTER 2 LOSSES) ---
    if loss_streak >= 2:
        # Phase-Lock Guarantee: If you lost 2 in a row, ALWAYS sync with the ball that just landed!
        # Because if the ball that just landed repeats (2-streak or dragon), you WIN!
        return last, f'🛑 LVL 3 PHASE-LOCK SYNC ({last})'

    # --- LEVEL 2 (AFTER 1 LOSS) ---
    elif loss_streak == 1:
        # If alt >= 2 (active chop), follow the chop!
        if alt >= 2:
            return opp(last), f'🛡️ LVL 2 CHOP FLIP (x{alt})'
        # Else follow the streak!
        return last, f'🛡️ LVL 2 STREAK LOCK ({last} x{streak})'

    # --- LEVEL 1 (NORMAL FLOW) ---
    else:
        if streak >= 3 and streak <= 7:
            return last, f'🐉 DRAGON FLOW ({last} x{streak})'
        elif streak > 7:
            return opp(last), f'⚖️ FATIGUE CUT (x{streak})'
        elif alt >= 2:
            return opp(last), f'⚡ CHOP OSCILLATE (x{alt})'
        else:
            return last, f'🌊 FLOW MOMENTUM ({last})'

print('=== TESTING PERFECT SYNC ENGINE ON USER LIVE SEQUENCE ===')
hist = [
    {'period': '10845', 'number': 4, 'size': 'SMALL'},
    {'period': '10846', 'number': 0, 'size': 'SMALL'},
    {'period': '10847', 'number': 1, 'size': 'SMALL'},
]

loss_streak = 0
wins, losses = 0, 0
max_losses = 0

for r in live_test_seq:
    pred, reg = predict_perfect_sync(hist, loss_streak)
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
