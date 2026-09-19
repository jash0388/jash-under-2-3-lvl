from test_harness_ab import seq_A, seq_B, test_strategy_on_seqs, opp
from million_rounds_deep_research import million_data, test_candidate_both_ways

def predict_apex_titan_v40(history, loss_streak):
    sizes = [h['size'] for h in history]
    if len(sizes) < 3:
        return "BIG", "INITIALIZING"
        
    last = sizes[-1]
    
    # 1. Multi-scale Training on Recent Session (up to 100 rounds)
    train = sizes[-100:]
    p3 = tuple(sizes[-3:]) if len(sizes) >= 3 else None
    p2 = tuple(sizes[-2:]) if len(sizes) >= 2 else None
    p1 = sizes[-1]
    
    c3 = {"BIG": 0, "SMALL": 0}
    c2 = {"BIG": 0, "SMALL": 0}
    c1 = {"BIG": 0, "SMALL": 0}
    
    for i in range(len(train) - 1):
        nxt = train[i+1]
        if p3 and i >= 2 and (train[i-2], train[i-1], train[i]) == p3:
            c3[nxt] += 1
        if p2 and i >= 1 and (train[i-1], train[i]) == p2:
            c2[nxt] += 1
        if train[i] == p1:
            c1[nxt] += 1
            
    # 2. Run length & cadence analysis
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
    
    curr_s, curr_l = runs[-1]
    prev_l = runs[-2][1] if len(runs) >= 2 else 1
    prev2_l = runs[-3][1] if len(runs) >= 3 else 1
    recent_lens = [r[1] for r in runs[-6:]]
    avg_len = sum(recent_lens) / len(recent_lens)
    
    # Alternation count
    alt = 0
    for s, l in reversed(runs):
        if l == 1: alt += 1
        else: break

    # 3. Dynamic Probability Scoring
    score_big = 0.0
    score_small = 0.0
    
    # N-gram signals
    tot3 = c3["BIG"] + c3["SMALL"]
    if tot3 >= 2:
        score_big += (c3["BIG"] / tot3) * 3.5
        score_small += (c3["SMALL"] / tot3) * 3.5
        
    tot2 = c2["BIG"] + c2["SMALL"]
    if tot2 >= 3:
        score_big += (c2["BIG"] / tot2) * 2.5
        score_small += (c2["SMALL"] / tot2) * 2.5
        
    tot1 = c1["BIG"] + c1["SMALL"]
    if tot1 >= 5:
        score_big += (c1["BIG"] / tot1) * 1.5
        score_small += (c1["SMALL"] / tot1) * 1.5

    # Cadence / Structure signals
    if curr_l >= 3 and curr_l <= 7:
        if last == "BIG": score_big += 3.0
        else: score_small += 3.0
    elif curr_l > 7:
        if last == "BIG": score_small += 3.0
        else: score_big += 3.0
    elif curr_l == 2 and avg_len <= 2.0:
        if last == "BIG": score_small += 2.5
        else: score_big += 2.5

    # Base recommendation
    if score_big > score_small:
        base_pred = "BIG"
    elif score_small > score_big:
        base_pred = "SMALL"
    else:
        base_pred = last

    # 4. Martingale Level Recovery Overrides
    if loss_streak >= 2:
        # EMERGENCY LEVEL 3
        if curr_l >= 3:
            return last, f'🛑 LVL 3 DRAGON ANCHOR ({last} x{curr_l})'
        elif curr_l == 2 and avg_len <= 2.0:
            return opp(last), f'🛑 LVL 3 DOUBLET CUT ({last} x2 -> FLIP)'
        else:
            return base_pred, f'🛑 LVL 3 MARKOV BRAIN ({base_pred})'
    elif loss_streak == 1:
        if curr_l >= 3:
            return last, f'🛡️ LVL 2 DRAGON ANCHOR ({last} x{curr_l})'
        elif curr_l == 2 and avg_len <= 2.0:
            return opp(last), f'🛡️ LVL 2 DOUBLET CUT ({last} x2)'
        else:
            return base_pred, f'🛡️ LVL 2 MARKOV BRAIN ({base_pred})'
    else:
        if curr_l >= 3 and curr_l <= 7:
            return last, f'🐉 DRAGON FLOW ({last} x{curr_l})'
        elif curr_l > 7:
            return opp(last), f'⚖️ FATIGUE CUT (x{curr_l})'
        elif curr_l == 2 and avg_len <= 2.0:
            return opp(last), f'⚡ DOUBLET FLIP ({last} x2)'
        else:
            return base_pred, f'🧠 MARKOV FLOW ({base_pred})'

test_strategy_on_seqs(predict_apex_titan_v40, "Apex Titan V40 Self-Learning Hybrid")

print("\n=== BENCHMARKING ON 2,000,000 ROUNDS ===")
test_candidate_both_ways(predict_apex_titan_v40, "Apex Titan V40 Self-Learning Hybrid")
