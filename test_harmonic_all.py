from dataset_real_all import all_real_sequences, get_runs, opp

def test_harmonic_engine(pred_fn):
    total_max = 0
    total_wins = 0
    total_losses = 0
    results = []
    
    for name, seq in all_real_sequences:
        history = seq[:3]
        streak = 0
        max_streak = 0
        wins, losses = 0, 0
        details = []
        
        for item in seq[3:]:
            pred, tag = pred_fn(history, streak)
            act = item['size']
            if pred == act:
                wins += 1
                streak = 0
                details.append((item['period'], pred, act, item['number'], 'WIN', streak + 1, tag))
            else:
                losses += 1
                streak += 1
                if streak > max_streak:
                    max_streak = streak
                details.append((item['period'], pred, act, item['number'], 'LOSS', streak, tag))
            history.append(item)
            
        if max_streak > total_max:
            total_max = max_streak
        total_wins += wins
        total_losses += losses
        results.append((name, wins, losses, max_streak, details))
        
    return total_max, total_wins, total_losses, results

# Let's write the Harmonic Doublet & Multi-Regime Master Engine
def predict_harmonic_v100(history, loss_streak=0):
    sizes = [x['size'] for x in history]
    nums = [x['number'] for x in history]
    runs = get_runs(sizes)
    
    c_side, c_len = runs[-1]
    p_side, p_len = runs[-2] if len(runs) >= 2 else (opp(c_side), 0)
    p3_side, p3_len = runs[-3] if len(runs) >= 3 else (c_side, 0)
    last_s = sizes[-1]
    
    # Analyze recent run lengths in window
    recent_run_lens = [r[1] for r in runs[-5:]]
    avg_run_len = sum(recent_run_lens) / len(recent_run_lens) if recent_run_lens else 1.5
    
    # Alternation streak (chop 1-1-1-1)
    alt = 0
    for r_s, r_l in reversed(runs):
        if r_l == 1: alt += 1
        else: break

    # Check for Doublet Cadence (e.g. recent runs are length 2)
    is_doublet_cadence = (p_len == 2 or (len(runs) >= 3 and runs[-3][1] == 2))

    # --- LEVEL 3 RECOVERY (ZERO-LOSS CASCADE SHIELD) ---
    if loss_streak >= 2:
        # If we lost 2 in a row, break the phase trap!
        if c_len == 1:
            # New run just started: ride it into a 2-run
            return c_side, "L3_NEW_RUN_RIDE"
        elif c_len == 2:
            # 2-run completed: cut it
            return opp(c_side), "L3_DOUBLET_CUT"
        elif c_len >= 3:
            # Dragon: ride the dragon
            return c_side, "L3_DRAGON_RIDE"
        elif alt >= 2:
            return opp(last_s), "L3_CHOP_OSC"
        else:
            return c_side, "L3_MOM_LOCK"

    # --- LEVEL 2 RECOVERY (1 LOSS) ---
    elif loss_streak == 1:
        if c_len == 1:
            # Follow momentum into doublet
            return c_side, "L2_DOUBLET_FOLLOW"
        elif c_len == 2:
            # Doublet complete -> flip
            return opp(c_side), "L2_DOUBLET_FLIP"
        elif c_len >= 3:
            return c_side, "L2_DRAGON_RIDE"
        elif alt >= 3:
            return opp(last_s), "L2_CHOP_FLIP"
        elif alt >= 2:
            return last_s, "L2_CHOP_STAB"
        else:
            return c_side, "L2_MOM"

    # --- LEVEL 1 BASE PREDICTION (0 LOSSES) ---
    else:
        if c_len == 1:
            # If in deep chop (alt >= 3), continue oscillating
            if alt >= 3:
                return opp(last_s), "L1_CHOP_OSC"
            # Otherwise, ride into 2-length doublet/trend
            return c_side, "L1_MOM_RIDE"
        elif c_len == 2:
            # If doublet pattern is active, flip
            return opp(c_side), "L1_DOUBLET_CUT"
        elif c_len == 3:
            # Dragon length 3: test cut or ride
            if is_doublet_cadence:
                return opp(c_side), "L1_DRAGON_CUT_3"
            return c_side, "L1_DRAGON_RIDE_3"
        elif c_len >= 4:
            # Strong dragon: ride
            return c_side, "L1_DRAGON_RIDE_4+"
        else:
            return c_side, "L1_MOM"

tot_max, tot_w, tot_l, res = test_harmonic_engine(predict_harmonic_v100)
print("="*80)
print(f"HARMONIC V100 TEST RESULTS ACROSS ALL {len(all_real_sequences)} REAL SEQUENCES:")
print(f"TOTAL: {tot_w}W / {tot_l}L ({(tot_w/(tot_w+tot_l))*100:.1f}%) | MAX CONSECUTIVE LOSSES = {tot_max}")
print("="*80)
for name, w, l, ms, det in res:
    pass_str = "✅ PASS" if ms <= 2 else f"❌ FAIL ({ms} losses)"
    print(f"{name:<35}: {w}W/{l}L | Max Streak: {ms} | {pass_str}")
