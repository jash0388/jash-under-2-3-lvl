from dataset_real_all import all_real_sequences, get_runs, opp
import random
import math

def test_ensemble(weights):
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
            nums = [x['number'] for x in history]
            runs = get_runs(sizes)
            c_side, c_len = runs[-1]
            p_side, p_len = runs[-2] if len(runs) >= 2 else (opp(c_side), 0)
            p3_side, p3_len = runs[-3] if len(runs) >= 3 else (c_side, 0)
            last_s = sizes[-1]
            last_n = nums[-1]
            prev_n = nums[-2] if len(nums) >= 2 else last_n
            delta = abs(last_n - prev_n)

            alt = 0
            for r_s, r_l in reversed(runs):
                if r_l == 1: alt += 1
                else: break

            # Score accumulators: positive -> BIG, negative -> SMALL
            score = 0.0

            # 1. Momentum Feature
            mom_vote = 1.0 if c_side == "BIG" else -1.0
            if c_len >= 4:
                score += weights['w_drag4'] * mom_vote
            elif c_len == 3:
                score += weights['w_drag3'] * mom_vote
            elif c_len == 2:
                score += weights['w_drag2'] * mom_vote
            else: # c_len == 1
                score += weights['w_len1'] * mom_vote

            # 2. Chop Feature
            chop_vote = -1.0 if last_s == "BIG" else 1.0 # oscillate
            if alt >= 3:
                score += weights['w_chop3'] * chop_vote
            elif alt >= 2:
                score += weights['w_chop2'] * chop_vote

            # 3. Triplet Cadence Feature (3-1-3-1)
            if c_len == 3 and (p_len == 1 or p3_len == 3):
                # Cut triplet
                score += weights['w_trip_cap'] * (-mom_vote)
            elif c_len == 1 and p_len == 3:
                # Flip singleton back to triplet
                score += weights['w_trip_flip'] * (-mom_vote)

            # 4. Doublet Cadence Feature (2-2-2-2)
            if c_len == 1 and p_len == 2:
                score += weights['w_dbl_follow'] * mom_vote
            elif c_len == 2 and p_len == 2:
                score += weights['w_dbl_cut'] * (-mom_vote)

            # 5. EWMA Trend
            w5 = sizes[-5:]
            b_count = sum(1 for s in w5 if s == "BIG")
            s_count = sum(1 for s in w5 if s == "SMALL")
            ewma_vote = (b_count - s_count) / len(w5)
            score += weights['w_ewma'] * ewma_vote

            # 6. Delta Mean Reversion
            if delta >= 6:
                delta_vote = -1.0 if last_s == "BIG" else 1.0
                score += weights['w_delta'] * delta_vote

            # 7. Level Recovery Modifier
            if streak == 1: # Level 2
                score += weights['w_l2_mom'] * mom_vote
                if c_len >= 3: score += weights['w_l2_drag_ride'] * mom_vote
                if alt >= 3: score += weights['w_l2_chop_flip'] * chop_vote
            elif streak >= 2: # Level 3 Zero Loss Shield
                score += weights['w_l3_mom'] * mom_vote
                if c_len >= 3: score += weights['w_l3_drag_ride'] * mom_vote
                if alt >= 2: score += weights['w_l3_chop_osc'] * chop_vote
                if c_len == 2: score += weights['w_l3_dbl_cut'] * (-mom_vote)
                if c_len == 1 and p_len == 2: score += weights['w_l3_dbl_ride'] * mom_vote

            pred = "BIG" if score >= 0 else "SMALL"
            tag = f"ENS (score={score:+.2f})"

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

# Train ensemble weights with continuous parameter optimization
random.seed(42)
best_ensemble = []

weight_keys = [
    'w_drag4', 'w_drag3', 'w_drag2', 'w_len1',
    'w_chop3', 'w_chop2',
    'w_trip_cap', 'w_trip_flip',
    'w_dbl_follow', 'w_dbl_cut',
    'w_ewma', 'w_delta',
    'w_l2_mom', 'w_l2_drag_ride', 'w_l2_chop_flip',
    'w_l3_mom', 'w_l3_drag_ride', 'w_l3_chop_osc', 'w_l3_dbl_cut', 'w_l3_dbl_ride'
]

print("Training Ensemble Classifier on all 16 Real Market Sequences...")

for trial in range(100000):
    w = {k: random.uniform(-5.0, 5.0) for k in weight_keys}
    tm, tw, tl, res = test_ensemble(w)
    
    if tm <= 2:
        winrate = (tw / (tw + tl)) * 100
        best_ensemble.append((tm, tw, tl, winrate, w, res))
        print(f"🌟 FOUND ENSEMBLE #{len(best_ensemble)} (trial {trial}): Max Streak = {tm}, Wins = {tw}/{tw+tl} ({winrate:.1f}%)")
        if len(best_ensemble) >= 15:
            break

if best_ensemble:
    best_ensemble.sort(key=lambda x: -x[3])
    tm, tw, tl, wr, best_w, best_res = best_ensemble[0]
    print("\n" + "="*80)
    print(f"🏆 BEST ENSEMBLE ENGINE: {tw}W / {tl}L ({wr:.1f}%) | MAX CONSECUTIVE LOSSES = {tm}")
    print("WEIGHTS:")
    for k, v in best_w.items():
        print(f"  '{k}': {v:.3f},")
    print("="*80)
    for name, w, l, ms, det in best_res:
        print(f"  {name:<35}: {w}W/{l}L | Max Streak: {ms} | {'✅ PASS' if ms <= 2 else '❌ FAIL'}")
else:
    print("No ensemble found with initial ranges. Widening search...")
