from test_master_ensemble import all_seqs, get_runs, opp

def predict_adaptive_regime(hist, loss_streak):
    sizes = [h['size'] for h in hist[-30:]]
    last = sizes[-1]
    runs = get_runs(sizes)
    curr_l = runs[-1][1]
    prev_l = runs[-2][1] if len(runs) >= 2 else 1
    
    # Measure recent alternation density in last 8 runs
    recent_runs = runs[-6:]
    avg_len = sum(r[1] for r in recent_runs) / len(recent_runs)
    alt_runs_count = sum(1 for r in recent_runs if r[1] == 1)
    is_chop_regime = (alt_runs_count >= 3)
    
    # Active alternation count at the very end
    alt = 0
    for s, l in reversed(runs):
        if l == 1: alt += 1
        else: break

    # --- LEVEL 3 EMERGENCY RECOVERY SHIELD ---
    if loss_streak >= 2:
        # After 2 losses:
        # If dragon is established (curr_l >= 2), NEVER bet against it -> follow dragon!
        if curr_l >= 2:
            return last, f'🛑 LVL 3 DRAGON FOLLOW ({last} x{curr_l})'
        # If active 1-1 chop (alt >= 2), oscillate:
        elif alt >= 2:
            return opp(last), f'🛑 LVL 3 CHOP FLIP (x{alt})'
        # Default: Sync with last actual ball
        else:
            return last, f'🛑 LVL 3 MOMENTUM SYNC ({last})'

    # --- LEVEL 2 RECOVERY SHIELD ---
    elif loss_streak == 1:
        if curr_l >= 3:
            return last, f'🛡️ LVL 2 DRAGON PERSIST ({last} x{curr_l})'
        elif curr_l == 2:
            if is_chop_regime:
                return opp(last), f'🛡️ LVL 2 DOUBLET CUT ({last} x2)'
            return last, f'🛡️ LVL 2 DRAGON TRY ({last} x2)'
        elif alt >= 2:
            return opp(last), f'🛡️ LVL 2 CHOP FLIP (x{alt})'
        else:
            return last, f'🛡️ LVL 2 MOMENTUM ({last})'

    # --- LEVEL 1 NORMAL FLOW ---
    else:
        if curr_l >= 3:
            if curr_l > 7: return opp(last), f'⚖️ FATIGUE CUT (x{curr_l})'
            return last, f'🐉 DRAGON FLOW ({last} x{curr_l})'
        elif curr_l == 2:
            # If recent market has long runs, follow to 3
            if avg_len >= 2.5:
                return last, f'🐉 DRAGON EXPAND ({last} x2)'
            # If chop/doublet market, flip at 2
            elif is_chop_regime:
                return opp(last), f'⚡ DOUBLET FLIP ({last} x2)'
            return last, f'🐉 DRAGON TRY ({last} x2)'
        elif alt >= 3:
            return opp(last), f'⚡ CHOP OSCILLATE (x{alt})'
        elif curr_l == 1 and prev_l == 2 and not is_chop_regime:
            return last, f'👥 DOUBLET 2ND ({last})'
        else:
            return last, f'🌊 FLOW MOMENTUM ({last})'

for name, seq in all_seqs.items():
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
        pred, regime = predict_adaptive_regime(hist, loss_streak)
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
