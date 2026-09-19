from dataset_real_all import all_real_sequences, get_runs, opp

def test_cadence_master():
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
            sizes = [x['size'] for x in history]
            runs = get_runs(sizes)
            c_side, c_len = runs[-1]
            p_side, p_len = runs[-2] if len(runs) >= 2 else (opp(c_side), 0)
            p3_side, p3_len = runs[-3] if len(runs) >= 3 else (c_side, 0)
            last_s = sizes[-1]
            
            alt = 0
            for r_s, r_l in reversed(runs):
                if r_l == 1: alt += 1
                else: break

            # --- LEVEL 3 ZERO-LOSS SHIELD (STREAK >= 2) ---
            if streak >= 2:
                # Triplet Cadence: 3-1-3-1
                if c_len == 3 and (p_len == 1 or p3_len == 3):
                    pred = opp(c_side)
                    tag = "🛑 L3_TRIPLET_CAP"
                elif c_len == 1 and p_len == 3:
                    pred = opp(c_side)
                    tag = "🛑 L3_SINGLETON_FLIP"
                # Doublet Cadence: 2-2-2-2
                elif c_len == 1 and p_len == 2:
                    pred = c_side
                    tag = "🛑 L3_DOUBLET_RIDE"
                elif c_len == 2:
                    pred = opp(c_side)
                    tag = "🛑 L3_DOUBLET_CUT"
                # Chop Cadence: 1-1-1-1
                elif alt >= 3:
                    pred = opp(last_s)
                    tag = "🛑 L3_CHOP_OSC"
                elif alt == 2:
                    pred = opp(last_s)
                    tag = "🛑 L3_CHOP_OSC_2"
                # Dragon: 4+
                elif c_len >= 4:
                    pred = c_side
                    tag = "🛑 L3_DRAGON_RIDE"
                elif c_len == 3:
                    pred = opp(c_side)
                    tag = "🛑 L3_DRAGON_CUT"
                else:
                    pred = c_side
                    tag = "🛑 L3_MOM_LOCK"

            # --- LEVEL 2 RECOVERY (STREAK == 1) ---
            elif streak == 1:
                if c_len == 3 and (p_len == 1 or p3_len == 3):
                    pred = opp(c_side)
                    tag = "🛡️ L2_TRIPLET_CAP"
                elif c_len == 1 and p_len == 3:
                    pred = opp(c_side)
                    tag = "🛡️ L2_SINGLETON_FLIP"
                elif c_len == 1 and p_len == 2:
                    pred = c_side
                    tag = "🛡️ L2_DOUBLET_RIDE"
                elif c_len == 2:
                    pred = opp(c_side)
                    tag = "🛡️ L2_DOUBLET_CUT"
                elif alt >= 3:
                    pred = opp(last_s)
                    tag = "🛡️ L2_DEEP_CHOP_FLIP"
                elif alt == 2:
                    pred = last_s
                    tag = "🛡️ L2_CHOP_STAB"
                elif c_len >= 4:
                    pred = c_side
                    tag = "🛡️ L2_DRAGON_RIDE"
                elif c_len == 3:
                    pred = c_side
                    tag = "🛡️ L2_DRAGON_RIDE_3"
                else:
                    pred = c_side
                    tag = "🛡️ L2_MOM"

            # --- LEVEL 1 BASE PREDICTION (STREAK == 0) ---
            else:
                if c_len == 3 and p_len == 1 and p3_len == 3:
                    pred = opp(c_side)
                    tag = "⚡ L1_TRIPLET_CAP"
                elif c_len == 1 and p_len == 3:
                    pred = opp(c_side)
                    tag = "⚡ L1_SINGLETON_FLIP"
                elif c_len == 1 and p_len == 2:
                    pred = c_side
                    tag = "⚡ L1_DOUBLET_RIDE"
                elif c_len == 2 and p_len == 2:
                    pred = opp(c_side)
                    tag = "⚡ L1_DOUBLET_CUT"
                elif alt >= 3:
                    pred = opp(last_s)
                    tag = "⚡ L1_CHOP_OSC"
                elif alt == 2:
                    pred = opp(last_s)
                    tag = "⚡ L1_CHOP_OSC"
                elif c_len >= 4:
                    pred = c_side
                    tag = "🌊 L1_DRAGON_RIDE"
                elif c_len == 3:
                    pred = opp(c_side)
                    tag = "🐉 L1_DRAGON_CUT"
                elif c_len == 2:
                    pred = opp(c_side)
                    tag = "⚡ L1_DOUBLET_CUT"
                else:
                    pred = c_side
                    tag = "🌊 L1_MOM"

            act = item['size']
            if pred == act:
                wins += 1
                details.append((item['period'], pred, act, item['number'], 'WIN', streak + 1, tag))
                streak = 0
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

tm, tw, tl, res = test_cadence_master()
print("="*80)
print(f"CADENCE MASTER RESULTS: {tw}W / {tl}L ({(tw/(tw+tl))*100:.1f}%) | MAX CONSECUTIVE LOSSES = {tm}")
print("="*80)
for name, w, l, ms, det in res:
    print(f"  {name:<35}: {w}W/{l}L | Max Streak: {ms} | {'✅ PASS' if ms <= 2 else f'❌ FAIL ({ms})'}")
