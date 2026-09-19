from test_master_ensemble import all_seqs, opp

def predict_markov_level3(history, loss_streak):
    sizes = [h['size'] for h in history[-50:]]
    nums = [h['number'] for h in history[-50:]]
    last = sizes[-1]
    
    streak = 1
    for i in range(len(sizes)-2, -1, -1):
        if sizes[i] == last: streak += 1
        else: break
        
    alt = 1
    for i in range(len(sizes)-1, 0, -1):
        if sizes[i] != sizes[i-1]: alt += 1
        else: break

    # N-gram transition frequency
    p_big = 0.5
    if len(sizes) >= 6:
        k2 = (sizes[-2], sizes[-1])
        b_cnt, s_cnt = 0, 0
        for i in range(len(sizes) - 2):
            if (sizes[i], sizes[i+1]) == k2:
                if sizes[i+2] == 'BIG': b_cnt += 1
                else: s_cnt += 1
        if b_cnt + s_cnt >= 1:
            p_big = b_cnt / (b_cnt + s_cnt)

    # --- LEVEL 3 (AFTER 2 LOSSES) ---
    if loss_streak >= 2:
        if p_big >= 0.60:
            return 'BIG', f'🛑 LVL 3 N-GRAM LOCK (BIG {int(p_big*100)}%)'
        elif p_big <= 0.40:
            return 'SMALL', f'🛑 LVL 3 N-GRAM LOCK (SMALL {int((1-p_big)*100)}%)'
        elif alt >= 3:
            return opp(last), f'🛑 LVL 3 CHOP SYNC (x{alt})'
        else:
            return last, f'🛑 LVL 3 MOMENTUM LOCK ({last})'

    # --- LEVEL 2 (AFTER 1 LOSS) ---
    elif loss_streak == 1:
        if alt >= 3:
            return opp(last), f'🛡️ LVL 2 CHOP FLIP (x{alt})'
        elif p_big >= 0.65:
            return 'BIG', f'🛡️ LVL 2 N-GRAM (BIG)'
        elif p_big <= 0.35:
            return 'SMALL', f'🛡️ LVL 2 N-GRAM (SMALL)'
        else:
            return last, f'🛡️ LVL 2 MOMENTUM ({last})'

    # --- LEVEL 1 (NORMAL FLOW) ---
    else:
        if streak >= 3 and streak <= 7:
            return last, f'🐉 DRAGON FLOW ({last} x{streak})'
        elif streak > 7:
            return opp(last), f'⚖️ FATIGUE CUT (x{streak})'
        elif alt >= 3:
            return opp(last), f'⚡ CHOP OSCILLATE (x{alt})'
        elif p_big >= 0.65:
            return 'BIG', f'🧠 N-GRAM CADENCE (BIG)'
        elif p_big <= 0.35:
            return 'SMALL', f'🧠 N-GRAM CADENCE (SMALL)'
        else:
            return last, f'🌊 FLOW MOMENTUM ({last})'

for name, seq in all_seqs.items():
    print(f"\n==================== {name} ====================")
    hist = []
    loss_streak = 0
    max_loss = 0
    wins, losses = 0, 0
    l1_w, l2_w, l3_w, busts = 0, 0, 0, 0
    for r in seq:
        if len(hist) < 3:
            hist.append(r)
            continue
        pred, reg = predict_markov_level3(hist, loss_streak)
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
        print(f"{r['period']}: Pred={pred:5s} | Act={r['size']:5s}({r['number']}) | {status:15s} | {reg}")
        hist.append(r)
    rounds = len(seq) - 3
    print(f"Summary {name}: Rounds={rounds}, Wins={wins}, WinRate={wins/rounds*100:.1f}%, MAX CONSECUTIVE LOSSES = {max_loss}, Busts = {busts}")
