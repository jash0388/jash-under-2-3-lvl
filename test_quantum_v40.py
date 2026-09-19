from test_harness_ab import seq_A, seq_B, test_strategy_on_seqs, opp
from million_rounds_deep_research import million_data, evaluate_strategy, test_candidate_both_ways

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

def predict_v40_cadence_quantum(history, loss_streak):
    sizes = [h['size'] for h in history[-30:]]
    last = sizes[-1]
    
    runs = get_runs(sizes)
    curr_s, curr_l = runs[-1]
    prev_s, prev_l = runs[-2] if len(runs) >= 2 else (opp(curr_s), 1)
    prev2_s, prev2_l = runs[-3] if len(runs) >= 3 else (curr_s, 1)
    
    streak = curr_l
    recent_lens = [r[1] for r in runs[-6:]]
    avg_len = sum(recent_lens) / len(recent_lens)
    
    # Active alternation count (consecutive 1-balls)
    alt = 0
    for s, l in reversed(runs):
        if l == 1: alt += 1
        else: break

    # Dominant size in last 10 rounds
    last10 = sizes[-10:]
    dominant = "BIG" if last10.count("BIG") >= 6 else ("SMALL" if last10.count("SMALL") >= 6 else None)

    # --- LEVEL 3 (AFTER 2 LOSSES - EMERGENCY ZERO-LOSS SHIELD) ---
    if loss_streak >= 2:
        # If long dragon >= 3, always lock dragon
        if streak >= 3:
            return last, f'🛑 LVL 3 DRAGON LOCK ({last} x{streak})'
        # If streak == 2:
        elif streak == 2:
            if avg_len <= 2.0:
                return opp(last), f'🛑 LVL 3 DOUBLET CUT ({last} x2 -> FLIP)'
            return last, f'🛑 LVL 3 DRAGON TRY ({last} x2)'
        # If streak == 1:
        else:
            # If alt >= 2 (e.g. S -> B or B -> S), this is an active 1-1 chop -> FLIP!
            if alt >= 2:
                return opp(last), f'🛑 LVL 3 CHOP FLIP (x{alt})'
            # If previous was a dragon >= 3, follow reversion/dominant
            elif prev_l >= 3:
                return last, f'🛑 LVL 3 DRAGON REVERSAL ({last})'
            elif dominant:
                return dominant, f'🛑 LVL 3 DOMINANT RECOVERY ({dominant})'
            else:
                return opp(last), f'🛑 LVL 3 ANTI-TRAP FLIP ({opp(last)})'

    # --- LEVEL 2 (AFTER 1 LOSS) ---
    elif loss_streak == 1:
        if streak >= 3:
            return last, f'🛡️ LVL 2 DRAGON LOCK ({last} x{streak})'
        elif streak == 2:
            if avg_len <= 2.0:
                return opp(last), f'🛡️ LVL 2 DOUBLET CUT ({last} x2)'
            return last, f'🛡️ LVL 2 DRAGON TRY ({last} x2)'
        else: # streak == 1
            if alt >= 2:
                return opp(last), f'🛡️ LVL 2 CHOP FLIP (x{alt})'
            elif prev_l >= 3:
                return last, f'🛡️ LVL 2 BREAKOUT MOMENTUM ({last})'
            elif dominant:
                return dominant, f'🛡️ LVL 2 DOMINANT MOMENTUM ({dominant})'
            else:
                return opp(last), f'🛡️ LVL 2 ADAPTIVE FLIP ({opp(last)})'

    # --- LEVEL 1 (NORMAL FLOW) ---
    else:
        if streak >= 3 and streak <= 7:
            return last, f'🐉 DRAGON FLOW ({last} x{streak})'
        elif streak > 7:
            return opp(last), f'⚖️ FATIGUE CUT (x{streak})'
        elif streak == 2:
            if avg_len <= 2.0:
                return opp(last), f'⚡ DOUBLET FLIP ({last} x2)'
            return last, f'🐉 DRAGON TRY ({last} x2)'
        else: # streak == 1
            if alt >= 2:
                return opp(last), f'⚡ CHOP OSCILLATE (x{alt})'
            elif dominant:
                return dominant, f'🌊 DOMINANT FLOW ({dominant})'
            else:
                return last, f'🌊 FLOW MOMENTUM ({last})'

test_strategy_on_seqs(predict_v40_cadence_quantum, "Apex Titan Quantum V40")

print("\n=== BENCHMARK ON 2,000,000 ROUNDS ===")
test_candidate_both_ways(predict_v40_cadence_quantum, "Apex Titan Quantum V40")
