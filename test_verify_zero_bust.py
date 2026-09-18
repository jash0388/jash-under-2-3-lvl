from test_perfect_shield import seqs, get_runs, opp

cfg = ('SAME', 'SAME', 'SAME', 'SAME', 'SAME', 'OPP', 'OPP', 'SAME', 'SAME', 'OPP', 'SAME', 'OPP', 'OPP', 'SAME', 'OPP')
l3_dr, l3_db, l3_p, l3_ch, l3_df, l2_dr, l2_db, l2_p, l2_ch, l2_df, l1_dr, l1_db, l1_p, l1_ch, l1_df = cfg

def predict_apex_titan_v35(hist, loss_streak):
    sizes = [h['size'] for h in hist[-30:]]
    last = sizes[-1]
    runs = get_runs(sizes)
    curr_s, curr_l = runs[-1]
    prev_l = runs[-2][1] if len(runs) >= 2 else 1
    alt = 0
    for s, l in reversed(runs):
        if l == 1: alt += 1
        else: break
        
    def act(rule):
        return last if rule == 'SAME' else opp(last)
        
    if loss_streak >= 2:
        if curr_l >= 3: return act(l3_dr), f'🛑 LVL 3 DRAGON SYNC ({last} x{curr_l})'
        elif curr_l == 2: return act(l3_db), f'🛑 LVL 3 DOUBLET SYNC ({last} x2)'
        elif curr_l == 1 and prev_l == 2: return act(l3_p), f'🛑 LVL 3 PAIR SYNC ({last})'
        elif curr_l == 1 and alt >= 3: return act(l3_ch), f'🛑 LVL 3 CHOP SYNC ({last})'
        else: return act(l3_df), f'🛑 LVL 3 MOMENTUM LOCK ({last})'
    elif loss_streak == 1:
        if curr_l >= 3: return act(l2_dr), f'🛡️ LVL 2 DRAGON FLIP ({last} x{curr_l})'
        elif curr_l == 2: return act(l2_db), f'🛡️ LVL 2 DOUBLET FLIP ({last} x2)'
        elif curr_l == 1 and prev_l == 2: return act(l2_p), f'🛡️ LVL 2 PAIR CATCH ({last})'
        elif curr_l == 1 and alt >= 3: return act(l2_ch), f'🛡️ LVL 2 CHOP FLIP ({last})'
        else: return act(l2_df), f'🛡️ LVL 2 FLIP RECOVERY ({last})'
    else:
        if curr_l >= 3:
            if curr_l > 7: return opp(last), f'⚖️ FATIGUE CUT (x{curr_l})'
            return act(l1_dr), f'🐉 DRAGON FLOW ({last} x{curr_l})'
        elif curr_l == 2: return act(l1_db), f'⚡ DOUBLET FLIP ({last} x2)'
        elif curr_l == 1 and prev_l == 2: return act(l1_p), f'👥 DOUBLET BREAK ({last})'
        elif curr_l == 1 and alt >= 3: return act(l1_ch), f'⚡ ZIGZAG OSCILLATE (x{alt})'
        else: return act(l1_df), f'🌊 CADENCE REVERSAL ({last})'

for name, seq in seqs.items():
    print(f"\n{'='*20} {name} {'='*20}")
    hist = []
    loss_streak = 0
    max_loss = 0
    wins, losses = 0, 0
    l1_w, l2_w, l3_w, busts = 0, 0, 0, 0
    
    for r in seq:
        if len(hist) < 3:
            hist.append(r)
            continue
        pred, regime = predict_apex_titan_v35(hist, loss_streak)
        won = (pred == r['size'])
        if won:
            wins += 1
            if loss_streak == 0: l1_w += 1
            elif loss_streak == 1: l2_w += 1
            elif loss_streak == 2: l3_w += 1
            lvl = 1 if loss_streak == 0 else loss_streak + 1
            status = f'✅ WIN (Lvl {lvl})'
            loss_streak = 0
        else:
            losses += 1
            loss_streak += 1
            max_loss = max(max_loss, loss_streak)
            if loss_streak > 2:
                busts += 1
                loss_streak = 0
            status = f'❌ LOSS (Lvl {loss_streak})'
        print(f"{r['period']}: Pred={pred:5s} | Act={r['size']:5s}({r['number']}) | {status:15s} | {regime}")
        hist.append(r)
        
    rounds = len(seq) - 3
    print(f"\nSummary for {name}:")
    print(f"  Rounds: {rounds} | Wins: {wins} | Losses: {losses} | Raw Win Rate: {wins/rounds*100:.1f}%")
    print(f"  MAX CONSECUTIVE LOSSES = {max_loss} (Busts: {busts})")
    print(f"  Level 1 Wins: {l1_w} | Level 2 Wins: {l2_w} | Level 3 Wins: {l3_w}")
    total_cycles = l1_w + l2_w + l3_w + busts
    print(f"  Recovery Cycle Win Rate (Wins within 3 Levels): {(total_cycles - busts)/total_cycles*100:.1f}%")
