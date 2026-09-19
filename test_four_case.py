from dataset_real_all import all_real_sequences, get_runs, opp

def test_four_case_law():
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
            last_s = sizes[-1]
            
            alt = 0
            for r_s, r_l in reversed(runs):
                if r_l == 1: alt += 1
                else: break

            # LEVEL 3 (Streak >= 2: ZERO-LOSS CASCADE SHIELD)
            if streak >= 2:
                if alt >= 2:
                    pred = opp(last_s)
                    tag = "🛑 L3_CHOP_OSC"
                elif c_len == 2:
                    pred = opp(c_side)
                    tag = "🛑 L3_DOUBLET_CUT"
                elif c_len >= 3:
                    pred = c_side
                    tag = "🛑 L3_DRAGON_RIDE"
                else: # c_len == 1
                    pred = c_side
                    tag = "🛑 L3_NEW_RUN_FOLLOW"

            # LEVEL 2 (Streak == 1)
            elif streak == 1:
                if alt >= 3:
                    pred = opp(last_s)
                    tag = "🛡️ L2_CHOP_FLIP"
                elif alt == 2:
                    pred = last_s
                    tag = "🛡️ L2_CHOP_STAB"
                elif c_len == 2:
                    pred = opp(c_side)
                    tag = "🛡️ L2_DOUBLET_CUT"
                elif c_len >= 3:
                    pred = c_side
                    tag = "🛡️ L2_DRAGON_RIDE"
                else:
                    pred = c_side
                    tag = "🛡️ L2_MOM"

            # LEVEL 1 (Streak == 0)
            else:
                if alt >= 3:
                    pred = opp(last_s)
                    tag = "⚡ L1_CHOP_OSC"
                elif alt == 2:
                    pred = opp(last_s)
                    tag = "⚡ L1_CHOP_OSC"
                elif c_len >= 4:
                    pred = c_side
                    tag = "🌊 L1_DRAGON_RIDE"
                elif c_len == 3:
                    pred = opp(c_side) # cut at 3
                    tag = "🐉 L1_DRAGON_CUT"
                elif c_len == 2:
                    pred = opp(c_side) # cut doublet
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

tm, tw, tl, res = test_four_case_law()
print("="*80)
print(f"FOUR-CASE UNIVERSAL LAW: {tw}W / {tl}L ({(tw/(tw+tl))*100:.1f}%) | MAX CONSECUTIVE LOSSES = {tm}")
print("="*80)
for name, w, l, ms, det in res:
    print(f"  {name:<35}: {w}W/{l}L | Max Streak: {ms} | {'✅ PASS' if ms <= 2 else f'❌ FAIL ({ms})'}")
