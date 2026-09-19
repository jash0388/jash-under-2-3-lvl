from test_all_three_seqs import seq_A, seq_B, seq_C, test_on_all_seqs, opp
from million_rounds_deep_research import million_data, test_candidate_both_ways

def predict_quantum_anti_trap(history, loss_streak):
    sizes = [h['size'] for h in history]
    if len(sizes) < 3:
        return "BIG", "INITIALIZING"
        
    last = sizes[-1]
    
    # Measure streak
    streak = 1
    for i in range(len(sizes)-2, -1, -1):
        if sizes[i] == last: streak += 1
        else: break
        
    # Measure chop (alternation)
    alt = 1
    for i in range(len(sizes)-1, 0, -1):
        if sizes[i] != sizes[i-1]: alt += 1
        else: break

    # Measure runs
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
    
    curr_l = runs[-1][1]
    prev_l = runs[-2][1] if len(runs) >= 2 else 1
    recent_lens = [r[1] for r in runs[-6:]]
    avg_len = sum(recent_lens) / len(recent_lens)

    # Base model (Flow & Regime)
    if streak >= 3 and streak <= 7:
        base_pred = last
        base_reg = f"🐉 DRAGON FLOW ({last} x{streak})"
    elif streak > 7:
        base_pred = opp(last)
        base_reg = f"⚖️ FATIGUE CUT (x{streak})"
    elif streak == 2:
        if avg_len <= 2.2:
            base_pred = opp(last)
            base_reg = f"⚡ DOUBLET CUT ({last} x2)"
        else:
            base_pred = last
            base_reg = f"🐉 DRAGON TRY ({last} x2)"
    else: # streak == 1
        if alt >= 2:
            base_pred = opp(last)
            base_reg = f"⚡ CHOP OSCILLATE (x{alt})"
        elif prev_l >= 3:
            # Rebound after dragon: 1-ball rebound flips back!
            base_pred = opp(last)
            base_reg = f"⚡ DRAGON REBOUND ({last} -> {opp(last)})"
        else:
            base_pred = last
            base_reg = f"🌊 FLOW MOMENTUM ({last})"

    # --- LEVEL 3 (AFTER 2 LOSSES: ANTI-TRAP INVERSION SHIELD) ---
    if loss_streak >= 2:
        # If active streak is a proven deep dragon (>= 4), never fight it:
        if streak >= 4:
            return last, f"🛑 LVL 3 DRAGON LOCK ({last} x{streak})"
        # If market is caught in doublet/chop anti-phase, INVERT the standard model trap!
        # When streak == 1 and prev_l was 1, we are in chop -> continue chop!
        if streak == 1:
            if alt >= 2:
                return opp(last), f"🛑 LVL 3 CHOP FLIP (x{alt})"
            else:
                return opp(last), f"🛑 LVL 3 ANTI-TRAP INVERSION ({opp(last)})"
        elif streak == 2:
            return opp(last), f"🛑 LVL 3 DOUBLET TERMINATOR ({last} x2 -> FLIP)"
        elif streak == 3:
            # 3-dragon break or continuation
            return last, f"🛑 LVL 3 DRAGON ANCHOR ({last} x3)"

    # --- LEVEL 2 (AFTER 1 LOSS) ---
    elif loss_streak == 1:
        if streak >= 4:
            return last, f"🛡️ LVL 2 DRAGON LOCK ({last} x{streak})"
        elif streak == 2:
            return opp(last), f"🛡️ LVL 2 DOUBLET CUT ({last} x2)"
        elif streak == 1:
            if alt >= 2:
                return opp(last), f"🛡️ LVL 2 CHOP FLIP (x{alt})"
            else:
                return last, f"🛡️ LVL 2 MOMENTUM ({last})"
        else:
            return last, f"🛡️ LVL 2 FOLLOW ({last})"

    return base_pred, base_reg

test_on_all_seqs(predict_quantum_anti_trap, "Quantum Anti-Trap Inversion Shield (Apex Titan V43)")
print("\n=== BENCHMARKING ON 2,000,000 ROUNDS ===")
test_candidate_both_ways(predict_quantum_anti_trap, "Quantum Anti-Trap Inversion Shield (Apex Titan V43)")
