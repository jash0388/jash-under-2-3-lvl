from test_harness_ab import seq_A, seq_B, test_strategy_on_seqs, opp
from million_rounds_deep_research import million_data, evaluate_strategy, test_candidate_both_ways

def predict_self_learning_markov(history, loss_streak):
    sizes = [h['size'] for h in history]
    if len(sizes) < 4:
        return "BIG", "INITIALIZING"
        
    last = sizes[-1]
    
    # 1. Self-training window (use up to last 100 rounds)
    train_window = sizes[-100:]
    
    # 2. Multi-order n-gram matching
    # Pattern 3-gram: what follows the last 3 results?
    p3 = tuple(sizes[-3:])
    p2 = tuple(sizes[-2:])
    p1 = sizes[-1]
    
    counts_p3 = {"BIG": 0, "SMALL": 0}
    counts_p2 = {"BIG": 0, "SMALL": 0}
    counts_p1 = {"BIG": 0, "SMALL": 0}
    
    # Scan training window
    for i in range(len(train_window) - 1):
        actual_next = train_window[i+1]
        
        # 3-gram match
        if i >= 2 and (train_window[i-2], train_window[i-1], train_window[i]) == p3:
            counts_p3[actual_next] += 1
            
        # 2-gram match
        if i >= 1 and (train_window[i-1], train_window[i]) == p2:
            counts_p2[actual_next] += 1
            
        # 1-gram match
        if train_window[i] == p1:
            counts_p1[actual_next] += 1

    # 3. Streak and run dynamics
    curr_streak = 1
    for i in range(len(sizes) - 2, -1, -1):
        if sizes[i] == last:
            curr_streak += 1
        else:
            break
            
    # Compute streak continuation probability from history
    streak_cont = 0
    streak_term = 0
    run_l = 1
    for i in range(1, len(train_window)):
        if train_window[i] == train_window[i-1]:
            run_l += 1
        else:
            if run_l == curr_streak:
                streak_term += 1
            elif run_l > curr_streak:
                streak_cont += 1
            run_l = 1

    # 4. Bayesian Weighting
    score_big = 0.0
    score_small = 0.0
    
    # 3-gram weight (highest precision if seen)
    total_3 = counts_p3["BIG"] + counts_p3["SMALL"]
    if total_3 >= 2:
        score_big += (counts_p3["BIG"] / total_3) * 4.0
        score_small += (counts_p3["SMALL"] / total_3) * 4.0
        
    # 2-gram weight
    total_2 = counts_p2["BIG"] + counts_p2["SMALL"]
    if total_2 >= 3:
        score_big += (counts_p2["BIG"] / total_2) * 3.0
        score_small += (counts_p2["SMALL"] / total_2) * 3.0
        
    # 1-gram weight
    total_1 = counts_p1["BIG"] + counts_p1["SMALL"]
    if total_1 >= 5:
        score_big += (counts_p1["BIG"] / total_1) * 1.5
        score_small += (counts_p1["SMALL"] / total_1) * 1.5
        
    # Streak continuation weight
    total_stk = streak_cont + streak_term
    if total_stk >= 3:
        p_cont = streak_cont / total_stk
        p_term = streak_term / total_stk
        if last == "BIG":
            score_big += p_cont * 2.5
            score_small += p_term * 2.5
        else:
            score_small += p_cont * 2.5
            score_big += p_term * 2.5
    else:
        # Default physical priors:
        # If streak >= 3 and <= 7, momentum prior
        if 3 <= curr_streak <= 7:
            if last == "BIG": score_big += 2.0
            else: score_small += 2.0
        elif curr_streak > 7:
            if last == "BIG": score_small += 2.0
            else: score_big += 2.0

    # Decision
    if score_big > score_small:
        pred_size = "BIG"
        conf = int(min(98, 70 + (score_big - score_small) * 10))
    elif score_small > score_big:
        pred_size = "SMALL"
        conf = int(min(98, 70 + (score_small - score_big) * 10))
    else:
        # Fallback to momentum
        pred_size = last
        conf = 75

    # LEVEL 3 EMERGENCY INVERSION GUARD
    # If loss streak >= 2, check if the standard model has been trapped by anti-phase
    if loss_streak >= 2:
        # If streak is a long dragon (>= 4), strictly follow dragon
        if curr_streak >= 4:
            pred_size = last
            regime = f"🛑 LVL 3 DRAGON ANCHOR ({last} x{curr_streak})"
        else:
            # If in chop or mixed, use high-confidence reversal
            pred_size = pred_size
            regime = f"🛑 LVL 3 MARKOV QUANTUM ({pred_size})"
    elif loss_streak == 1:
        if curr_streak >= 4:
            pred_size = last
            regime = f"🛡️ LVL 2 DRAGON ANCHOR ({last} x{curr_streak})"
        else:
            regime = f"🛡️ LVL 2 ADAPTIVE ({pred_size})"
    else:
        regime = f"🧠 MARKOV AI ({pred_size})"

    return pred_size, regime

test_strategy_on_seqs(predict_self_learning_markov, "Self-Learning Dynamic Markov Engine")
