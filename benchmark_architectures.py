from million_rounds_deep_research import million_data, evaluate_strategy, test_candidate_both_ways, opp

# Model 1: Apex Titan V37
def predict_v37(history, loss_streak):
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

    if loss_streak >= 2:
        if alt >= 3: return opp(last), 'L3_CHOP'
        return last, 'L3_MOMENTUM'
    elif loss_streak == 1:
        if alt >= 3: return opp(last), 'L2_CHOP'
        return last, 'L2_MOMENTUM'
    else:
        if streak >= 3 and streak <= 7: return last, 'L1_DRAGON'
        elif streak > 7: return opp(last), 'L1_FATIGUE'
        elif alt >= 3: return opp(last), 'L1_CHOP'
        else: return last, 'L1_MOMENTUM'

# Model 2: Triple-Cadence Adaptive Markov Filter
def predict_markov_cadence(history, loss_streak):
    sizes = [h['size'] for h in history[-40:]]
    last = sizes[-1]
    
    streak = 1
    for i in range(len(sizes)-2, -1, -1):
        if sizes[i] == last: streak += 1
        else: break
        
    alt = 1
    for i in range(len(sizes)-1, 0, -1):
        if sizes[i] != sizes[i-1]: alt += 1
        else: break

    p_big = 0.5
    if len(sizes) >= 6:
        k2 = (sizes[-2], sizes[-1])
        b_cnt, s_cnt = 0, 0
        for i in range(len(sizes)-2):
            if (sizes[i], sizes[i+1]) == k2:
                if sizes[i+2] == 'BIG': b_cnt += 1
                else: s_cnt += 1
        if b_cnt + s_cnt >= 2:
            p_big = b_cnt / (b_cnt + s_cnt)

    if loss_streak >= 2:
        if alt >= 3: return opp(last), 'L3_CHOP'
        elif streak >= 2: return last, 'L3_DRAGON'
        elif p_big > 0.55: return 'BIG', 'L3_MARKOV_BIG'
        elif p_big < 0.45: return 'SMALL', 'L3_MARKOV_SMALL'
        else: return last, 'L3_MOMENTUM'
    elif loss_streak == 1:
        if alt >= 3: return opp(last), 'L2_CHOP'
        elif streak >= 2: return last, 'L2_DRAGON'
        else: return last, 'L2_MOMENTUM'
    else:
        if streak >= 3 and streak <= 7: return last, 'L1_DRAGON'
        elif streak > 7: return opp(last), 'L1_FATIGUE'
        elif alt >= 3: return opp(last), 'L1_CHOP'
        elif p_big >= 0.65: return 'BIG', 'L1_MARKOV_BIG'
        elif p_big <= 0.35: return 'SMALL', 'L1_MARKOV_SMALL'
        else: return last, 'L1_MOMENTUM'

# Model 3: Anti-Phase Adaptive Guard
def predict_anti_phase(history, loss_streak):
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

    # Measure run-lengths
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
    
    prev_len = runs[-2][1] if len(runs) >= 2 else 1
    recent_lens = [r[1] for r in runs[-6:]]
    avg_len = sum(recent_lens) / len(recent_lens)

    if loss_streak >= 2:
        # If in confirmed streak, ride it
        if streak >= 2: return last, 'L3_STREAK'
        # If in confirmed chop, oscillate
        elif alt >= 3: return opp(last), 'L3_CHOP'
        # If previous was a doublet, expect second ball of doublet
        elif prev_len == 2: return last, 'L3_DOUBLET_PAIR'
        else: return last, 'L3_MOMENTUM'
    elif loss_streak == 1:
        if alt >= 3: return opp(last), 'L2_CHOP'
        elif streak >= 2: return last, 'L2_DRAGON'
        elif prev_len == 2: return last, 'L2_DOUBLET_PAIR'
        else: return last, 'L2_MOMENTUM'
    else:
        if streak >= 3 and streak <= 7: return last, 'L1_DRAGON'
        elif streak > 7: return opp(last), 'L1_FATIGUE'
        elif alt >= 3: return opp(last), 'L1_CHOP'
        elif streak == 2 and avg_len < 2.2: return opp(last), 'L1_DOUBLET_FLIP'
        elif prev_len == 2 and streak == 1: return last, 'L1_DOUBLET_PAIR'
        else: return last, 'L1_MOMENTUM'

test_candidate_both_ways(predict_v37, "Apex Titan V37 (Pure Momentum & Chop Threshold alt>=3)")
test_candidate_both_ways(predict_markov_cadence, "Markov Cadence Shield")
test_candidate_both_ways(predict_anti_phase, "Anti-Phase Doublet Guard")
