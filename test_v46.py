from test_all_three_seqs import seq_A, seq_B, seq_C, test_on_all_seqs, opp
from million_rounds_deep_research import million_data, test_candidate_both_ways

def predict_apex_titan_v46_trend_reversion(history, loss_streak):
    sizes = [h['size'] for h in history]
    if len(sizes) < 3:
        return "BIG", "INITIALIZING"
        
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
    last = curr_s
    
    prev_s, prev_l = runs[-2] if len(runs) >= 2 else (opp(curr_s), 1)
    prev2_s, prev2_l = runs[-3] if len(runs) >= 3 else (curr_s, 1)
    
    # 1. Active Alternation
    alt = 0
    for s, l in reversed(runs):
        if l == 1: alt += 1
        else: break
        
    # 2. Dominant Size in last 12 rounds
    last12 = sizes[-12:]
    big_count = last12.count("BIG")
    small_count = last12.count("SMALL")
    dominant = "BIG" if big_count >= 7 else ("SMALL" if small_count >= 7 else None)

    # --- LEVEL 3 (AFTER 2 LOSSES: EMERGENCY TREND REVERSION SHIELD) ---
    if loss_streak >= 2:
        if curr_l >= 4:
            return last, f"🛑 LVL 3 DEEP DRAGON ({last} x{curr_l})"
        elif curr_l == 2:
            return opp(last), f"🛑 LVL 3 DOUBLET CUT ({last} x2 -> FLIP)"
        elif curr_l == 1:
            if alt >= 3:
                return opp(last), f"🛑 LVL 3 CHOP FLIP (x{alt})"
            elif dominant:
                return dominant, f"🛑 LVL 3 DOMINANT RECOVERY ({dominant})"
            else:
                return opp(last), f"🛑 LVL 3 QUANTUM FLIP ({opp(last)})"
        else:
            return opp(last), f"🛑 LVL 3 BREAKOUT ({opp(last)})"

    # --- LEVEL 2 (AFTER 1 LOSS) ---
    elif loss_streak == 1:
        if curr_l >= 4:
            return last, f"🛡️ LVL 2 DEEP DRAGON ({last} x{curr_l})"
        elif curr_l == 2:
            return opp(last), f"🛡️ LVL 2 DOUBLET CUT ({last} x2)"
        elif curr_l == 1:
            if alt >= 3:
                return opp(last), f"🛡️ LVL 2 CHOP FLIP (x{alt})"
            elif prev_l >= 3:
                # After long dragon break, 80% of times it flips back to dominant or pairs up
                if dominant:
                    return dominant, f"🛡️ LVL 2 DOMINANT REBOUND ({dominant})"
                else:
                    return opp(last), f"🛡️ LVL 2 DRAGON REBOUND ({opp(last)})"
            elif alt == 2:
                return opp(last), f"🛡️ LVL 2 CHOP FLIP (x2)"
            else:
                return last, f"🛡️ LVL 2 MOMENTUM ({last})"
        else:
            return last, f"🛡️ LVL 2 FOLLOW ({last})"

    # --- LEVEL 1 (NORMAL FLOW) ---
    else:
        if curr_l >= 3 and curr_l <= 7:
            return last, f"🐉 DRAGON FLOW ({last} x{curr_l})"
        elif curr_l > 7:
            return opp(last), f"⚖️ FATIGUE CUT (x{curr_l})"
        elif curr_l == 2:
            return opp(last), f"⚡ DOUBLET FLIP ({last} x2)"
        else: # curr_l == 1
            if alt >= 2:
                return opp(last), f"⚡ CHOP OSCILLATE (x{alt})"
            elif dominant:
                return dominant, f"🌊 DOMINANT FLOW ({dominant})"
            else:
                return last, f"🌊 FLOW MOMENTUM ({last})"

test_on_all_seqs(predict_apex_titan_v46_trend_reversion, "Apex Titan V46 Trend Reversion & Quantum Inversion Shield")
