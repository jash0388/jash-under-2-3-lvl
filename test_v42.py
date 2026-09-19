from test_all_three_seqs import seq_A, seq_B, seq_C, test_on_all_seqs, opp
from million_rounds_deep_research import million_data, test_candidate_both_ways

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

def predict_adaptive_cadence_v42(history, loss_streak):
    sizes = [h['size'] for h in history]
    if len(sizes) < 3:
        return "BIG", "INITIALIZING"
        
    runs = get_runs(sizes)
    curr_s, curr_l = runs[-1]
    last = curr_s
    
    prev_s, prev_l = runs[-2] if len(runs) >= 2 else (opp(curr_s), 1)
    prev2_s, prev2_l = runs[-3] if len(runs) >= 3 else (curr_s, 1)
    
    # Recent regime cadence measure (last 6 runs)
    recent_runs = runs[-6:]
    recent_lens = [r[1] for r in recent_runs]
    avg_len = sum(recent_lens) / len(recent_lens)
    
    # Active alternation count (consecutive runs of length 1)
    alt = 0
    for s, l in reversed(runs):
        if l == 1: alt += 1
        else: break
        
    # Is the market currently chopping (mostly 1s)?
    is_chop_dominant = (avg_len <= 1.6) or (alt >= 2)

    # --- LEVEL 3 (AFTER 2 LOSSES) ---
    if loss_streak >= 2:
        if curr_l >= 3:
            return last, f"🛑 LVL 3 DRAGON LOCK ({last} x{curr_l})"
        elif curr_l == 2:
            return opp(last), f"🛑 LVL 3 DOUBLET FLIP ({last} x2 -> FLIP)"
        else: # curr_l == 1
            if is_chop_dominant:
                return opp(last), f"🛑 LVL 3 CHOP FLIP (x{alt})"
            else:
                if prev_l >= 2:
                    return last, f"🛑 LVL 3 PAIR TRY ({last})"
                else:
                    return opp(last), f"🛑 LVL 3 ANTI-TRAP ({opp(last)})"

    # --- LEVEL 2 (AFTER 1 LOSS) ---
    elif loss_streak == 1:
        if curr_l >= 3:
            return last, f"🛡️ LVL 2 DRAGON LOCK ({last} x{curr_l})"
        elif curr_l == 2:
            return opp(last), f"🛡️ LVL 2 DOUBLET CUT ({last} x2)"
        else: # curr_l == 1
            if is_chop_dominant:
                return opp(last), f"🛡️ LVL 2 CHOP FLIP (x{alt})"
            else:
                if prev_l >= 2:
                    return last, f"🛡️ LVL 2 PAIR REPEAT ({last})"
                else:
                    return opp(last), f"🛡️ LVL 2 OSCILLATE ({opp(last)})"

    # --- LEVEL 1 (NORMAL FLOW) ---
    else:
        if curr_l >= 3 and curr_l <= 7:
            return last, f"🐉 DRAGON FLOW ({last} x{curr_l})"
        elif curr_l > 7:
            return opp(last), f"⚖️ FATIGUE CUT (x{curr_l})"
        elif curr_l == 2:
            return opp(last), f"⚡ DOUBLET CUT ({last} x2)"
        else: # curr_l == 1
            if is_chop_dominant:
                return opp(last), f"⚡ CHOP OSCILLATE (x{alt})"
            else:
                if prev_l >= 2:
                    return last, f"👥 PAIR ATTEMPT ({last})"
                else:
                    return opp(last), f"⚡ OSCILLATE ({opp(last)})"

test_on_all_seqs(predict_adaptive_cadence_v42, "Apex Titan Adaptive Cadence V42")
print("\n=== BENCHMARKING ON 2,000,000 ROUNDS ===")
test_candidate_both_ways(predict_adaptive_cadence_v42, "Apex Titan Adaptive Cadence V42")
