from dataset_real_all import all_real_sequences, get_runs, opp

def test_pure_antichop_correct():
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

            # LEVEL 3 ZERO LOSS SHIELD
            if streak >= 2:
                if alt >= 2:
                    pred = opp(last_s)
                    tag = "🛑 L3_CHOP_SHIELD"
                else:
                    pred = c_side
                    tag = "🛑 L3_MOM_LOCK"

            elif streak == 1: # Level 2
                if alt >= 2:
                    pred = opp(last_s)
                    tag = "🛡️ L2_CHOP_OSC"
                else:
                    pred = c_side
                    tag = "🛡️ L2_MOM"

            else: # Level 1 Base
                if alt >= 2:
                    pred = opp(last_s)
                    tag = "⚡ L1_CHOP_OSC"
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

tm, tw, tl, res = test_pure_antichop_correct()
print("="*80)
print(f"CORRECT ANTI-CHOP RESULTS: {tw}W / {tl}L ({(tw/(tw+tl))*100:.1f}%) | MAX CONSECUTIVE LOSSES = {tm}")
print("="*80)
for name, w, l, ms, det in res:
    print(f"  {name:<35}: {w}W/{l}L | Max Streak: {ms} | {'✅ PASS' if ms <= 2 else f'❌ FAIL ({ms})'}")
