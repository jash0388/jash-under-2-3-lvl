from test_master_ensemble import all_seqs, get_runs, opp

def predict_apex_omega(hist, loss_streak):
    sizes = [h['size'] for h in hist[-40:]]
    nums = [h['number'] for h in hist[-40:]]
    last = sizes[-1]
    
    runs = get_runs(sizes)
    curr_l = runs[-1][1]
    prev_l = runs[-2][1] if len(runs) >= 2 else 1
    
    # 1. Markov 2-gram Transition
    p_big = 0.5
    if len(sizes) >= 6:
        k2 = (sizes[-2], sizes[-1])
        b_cnt, s_cnt = 0, 0
        for i in range(len(sizes) - 2):
            if (sizes[i], sizes[i+1]) == k2:
                if sizes[i+2] == 'BIG': b_cnt += 1
                else: s_cnt += 1
        if b_cnt + s_cnt >= 2:
            p_big = b_cnt / (b_cnt + s_cnt)
            
    # 2. Alternation count
    alt = 0
    for s, l in reversed(runs):
        if l == 1: alt += 1
        else: break
        
    # 3. Recent runs profile
    recent_lens = [r[1] for r in runs[-6:]]
    avg_len = sum(recent_lens) / len(recent_lens)
    
    # Votes from 4 independent sub-engines:
    # Engine A: Momentum / Dragon
    vote_a = last if (curr_l >= 2 and avg_len >= 2.0) or curr_l >= 4 else (opp(last) if alt >= 2 else last)
    
    # Engine B: Markov Transition
    vote_b = 'BIG' if p_big > 0.55 else ('SMALL' if p_big < 0.45 else last)
    
    # Engine C: Doublet Rhythm
    vote_c = opp(last) if (curr_l == 2 and not any(l >= 4 for l in recent_lens)) else (last if curr_l >= 3 else last)
    
    # Engine D: Trend Persistence
    vote_d = last if curr_l > 1 else (opp(last) if alt >= 3 else last)
    
    votes = [vote_a, vote_b, vote_c, vote_d]
    b_votes = votes.count('BIG')
    s_votes = votes.count('SMALL')
    
    # Level 3 Emergency Mode
    if loss_streak >= 2:
        # High-confidence consensus
        if b_votes > s_votes: pred = 'BIG'
        elif s_votes > b_votes: pred = 'SMALL'
        else: pred = last
        regime = f'🛑 LVL 3 CONSENSUS LOCK ({pred} {max(b_votes, s_votes)}/4)'
    elif loss_streak == 1:
        if b_votes >= 3: pred = 'BIG'
        elif s_votes >= 3: pred = 'SMALL'
        elif curr_l >= 2: pred = last
        else: pred = last
        regime = f'🛡️ LVL 2 RECOVERY ({pred})'
    else:
        if curr_l >= 3 and curr_l <= 7:
            pred = last
            regime = f'🐉 DRAGON FLOW ({last} x{curr_l})'
        elif curr_l > 7:
            pred = opp(last)
            regime = f'⚖️ FATIGUE CUT (x{curr_l})'
        elif alt >= 3:
            pred = opp(last)
            regime = f'⚡ CHOP OSCILLATE (x{alt})'
        elif b_votes > s_votes:
            pred = 'BIG'
            regime = f'🧠 ENSEMBLE CONSENSUS (BIG)'
        elif s_votes > b_votes:
            pred = 'SMALL'
            regime = f'🧠 ENSEMBLE CONSENSUS (SMALL)'
        else:
            pred = last
            regime = f'🌊 FLOW MOMENTUM ({last})'
            
    return pred, regime

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
        pred, regime = predict_apex_omega(hist, loss_streak)
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
