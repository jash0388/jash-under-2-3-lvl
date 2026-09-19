from test_all_three_seqs import seq_A, seq_B, seq_C, test_on_all_seqs, opp
from million_rounds_deep_research import million_data, test_candidate_both_ways

def predict_apex_titan_v45(history, loss_streak):
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
    
    # Active alternation count (runs of len 1)
    alt = 0
    for s, l in reversed(runs):
        if l == 1: alt += 1
        else: break

    # --- LEVEL 3 (AFTER 2 LOSSES - EMERGENCY ZERO-LOSS SHIELD) ---
    if loss_streak >= 2:
        if curr_l >= 3:
            return last, f"🛑 LVL 3 DRAGON LOCK ({last} x{curr_l})"
        elif curr_l == 2:
            return opp(last), f"🛑 LVL 3 DOUBLET CUT ({last} x2 -> FLIP)"
        else: # curr_l == 1
            if prev_l == 2:
                # Previous was a doublet (e.g. SS -> B), B pairs up with B2 -> REPEAT!
                return last, f"🛑 LVL 3 DOUBLET COUNTER-PAIR ({last})"
            elif alt >= 2:
                # Active 1-1 chop -> FLIP!
                return opp(last), f"🛑 LVL 3 CHOP FLIP (x{alt})"
            else:
                return opp(last), f"🛑 LVL 3 ANTI-TRAP FLIP ({opp(last)})"

    # --- LEVEL 2 (AFTER 1 LOSS) ---
    elif loss_streak == 1:
        if curr_l >= 3:
            return last, f"🛡️ LVL 2 DRAGON LOCK ({last} x{curr_l})"
        elif curr_l == 2:
            return opp(last), f"🛡️ LVL 2 DOUBLET CUT ({last} x2)"
        else: # curr_l == 1
            if prev_l == 2:
                return last, f"🛡️ LVL 2 DOUBLET COUNTER-PAIR ({last})"
            elif alt >= 2:
                return opp(last), f"🛡️ LVL 2 CHOP FLIP (x{alt})"
            else:
                return last, f"🛡️ LVL 2 MOMENTUM ({last})"

    # --- LEVEL 1 (NORMAL FLOW) ---
    else:
        if curr_l >= 2 and curr_l <= 7:
            # At streak >= 2, follow momentum (catches dragons at L1; if it flips to doublet, L2 catches the counter-pair!)
            return last, f"🐉 DRAGON FLOW ({last} x{curr_l})"
        elif curr_l > 7:
            return opp(last), f"⚖️ FATIGUE CUT (x{curr_l})"
        else: # curr_l == 1
            if alt >= 2:
                return opp(last), f"⚡ CHOP OSCILLATE (x{alt})"
            else:
                return last, f"🌊 FLOW MOMENTUM ({last})"

test_on_all_seqs(predict_apex_titan_v45, "Apex Titan V45 Symmetrical Doublet & Dragon Resolver")

print("\n=== BENCHMARKING ON 2,000,000 ROUNDS ===")
test_candidate_both_ways(predict_apex_titan_v45, "Apex Titan V45 Symmetrical Doublet & Dragon Resolver")
