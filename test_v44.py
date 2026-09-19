from test_all_three_seqs import seq_A, seq_B, seq_C, test_on_all_seqs, opp
from million_rounds_deep_research import million_data, test_candidate_both_ways

def predict_v44_apex_master(history, loss_streak):
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
    
    recent_lens = [r[1] for r in runs[-6:]]
    avg_len = sum(recent_lens) / len(recent_lens)
    
    # Active alternation count (runs of len 1)
    alt = 0
    for s, l in reversed(runs):
        if l == 1: alt += 1
        else: break

    # --- LEVEL 3 (AFTER 2 LOSSES - MAXIMUM RECOVERY SHIELD) ---
    if loss_streak >= 2:
        if curr_l >= 4:
            return last, f"🛑 LVL 3 DEEP DRAGON ({last} x{curr_l})"
        elif curr_l == 2:
            return opp(last), f"🛑 LVL 3 DOUBLET TERMINATOR ({last} x2 -> FLIP)"
        elif curr_l == 1:
            # If previous was a dragon (>=3), the 1st counter-ball starts a pair -> REPEAT!
            if prev_l >= 3:
                return last, f"🛑 LVL 3 DRAGON COUNTER-PAIR ({last})"
            # If active chop >= 2 -> FLIP!
            elif alt >= 2:
                return opp(last), f"🛑 LVL 3 CHOP FLIP (x{alt})"
            else:
                return opp(last), f"🛑 LVL 3 ANTI-TRAP FLIP ({opp(last)})"
        else:
            return opp(last), f"🛑 LVL 3 3-DRAGON CUT ({opp(last)})"

    # --- LEVEL 2 (AFTER 1 LOSS) ---
    elif loss_streak == 1:
        if curr_l >= 4:
            return last, f"🛡️ LVL 2 DEEP DRAGON ({last} x{curr_l})"
        elif curr_l == 2:
            return opp(last), f"🛡️ LVL 2 DOUBLET CUT ({last} x2)"
        elif curr_l == 1:
            if prev_l >= 3:
                return last, f"🛡️ LVL 2 DRAGON COUNTER-PAIR ({last})"
            elif alt >= 2:
                return opp(last), f"🛡️ LVL 2 CHOP FLIP (x{alt})"
            else:
                return opp(last), f"🛡️ LVL 2 ADAPTIVE FLIP ({opp(last)})"
        else:
            return last, f"🛡️ LVL 2 DRAGON TRY ({last} x{curr_l})"

    # --- LEVEL 1 (NORMAL FLOW) ---
    else:
        if curr_l >= 3 and curr_l <= 7:
            return last, f"🐉 DRAGON FLOW ({last} x{curr_l})"
        elif curr_l > 7:
            return opp(last), f"⚖️ FATIGUE CUT (x{curr_l})"
        elif curr_l == 2:
            return opp(last), f"⚡ DOUBLET FLIP ({last} x2)"
        else: # curr_l == 1
            if prev_l >= 3:
                # Breakout ball after dragon often pairs up to 2
                return last, f"👥 DRAGON COUNTER-PAIR ({last})"
            elif alt >= 2:
                return opp(last), f"⚡ CHOP OSCILLATE (x{alt})"
            else:
                return opp(last), f"⚡ 1-BALL FLIP ({opp(last)})"

test_on_all_seqs(predict_v44_apex_master, "Apex Titan V44 Master Cadence Shield")
print("\n=== BENCHMARKING ON 2,000,000 ROUNDS ===")
test_candidate_both_ways(predict_v44_apex_master, "Apex Titan V44 Master Cadence Shield")
