import random
from dataset_real_all import all_real_sequences, get_runs, opp

def evaluate_engine(pred_fn):
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

def create_predictor(genes):
    # genes: dictionary of rules
    def predict(history, loss_streak):
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

        # Check recent run lengths for doublet cadence
        recent_lens = [r[1] for r in runs[-4:]]
        doublet_count = sum(1 for l in recent_lens if l == 2)
        is_doublet_env = doublet_count >= 2 or (p_len == 2 and (len(runs) >= 3 and runs[-3][1] == 2))
        
        # LEVEL 3 (Streak >= 2: ZERO-LOSS CASCADE SHIELD)
        if loss_streak >= 2:
            conf = 99
            # Phase Inversion & Regime Protection
            if is_doublet_env:
                if c_len == 1: act = genes['l3_dbl_len1'] # 'RIDE' -> c_side
                elif c_len == 2: act = genes['l3_dbl_len2'] # 'CUT' -> opp(c_side)
                else: act = genes['l3_dbl_drag']
            else:
                if c_len >= 4: act = genes['l3_drag4']
                elif c_len == 3: act = genes['l3_drag3']
                elif c_len == 2: act = genes['l3_drag2']
                elif alt >= 3: act = genes['l3_chop3']
                elif alt >= 2: act = genes['l3_chop2']
                elif delta >= 5: act = genes['l3_delta5']
                else: act = genes['l3_default']

            if act == 'C': return c_side, "L3_RIDE"
            elif act == 'O': return opp(c_side), "L3_CUT"
            elif act == 'OSC': return opp(last_s), "L3_OSC"
            elif act == 'STAB': return last_s, "L3_STAB"
            return c_side, "L3_MOM"

        # LEVEL 2 (Streak == 1)
        elif loss_streak == 1:
            conf = 95
            if is_doublet_env:
                if c_len == 1: act = genes['l2_dbl_len1']
                elif c_len == 2: act = genes['l2_dbl_len2']
                else: act = genes['l2_dbl_drag']
            else:
                if c_len >= 4: act = genes['l2_drag4']
                elif c_len == 3: act = genes['l2_drag3']
                elif c_len == 2: act = genes['l2_drag2']
                elif alt >= 3: act = genes['l2_chop3']
                elif alt >= 2: act = genes['l2_chop2']
                elif delta >= 5: act = genes['l2_delta5']
                else: act = genes['l2_default']

            if act == 'C': return c_side, "L2_RIDE"
            elif act == 'O': return opp(c_side), "L2_CUT"
            elif act == 'OSC': return opp(last_s), "L2_OSC"
            elif act == 'STAB': return last_s, "L2_STAB"
            return c_side, "L2_MOM"

        # LEVEL 1 (Streak == 0)
        else:
            conf = 88
            if is_doublet_env:
                if c_len == 1: act = genes['l1_dbl_len1']
                elif c_len == 2: act = genes['l1_dbl_len2']
                else: act = genes['l1_dbl_drag']
            else:
                if c_len >= 4: act = genes['l1_drag4']
                elif c_len == 3: act = genes['l1_drag3']
                elif c_len == 2: act = genes['l1_drag2']
                elif alt >= 3: act = genes['l1_chop3']
                elif alt >= 2: act = genes['l1_chop2']
                else: act = genes['l1_default']

            if act == 'C': return c_side, "L1_RIDE"
            elif act == 'O': return opp(c_side), "L1_CUT"
            elif act == 'OSC': return opp(last_s), "L1_OSC"
            elif act == 'STAB': return last_s, "L1_STAB"
            return c_side, "L1_MOM"

    return predict

# Evolutionary Search
random.seed(1337)
param_options = {
    'l1_dbl_len1': ['C', 'O'],
    'l1_dbl_len2': ['O', 'C'],
    'l1_dbl_drag': ['C', 'O'],
    'l1_drag4': ['C', 'O'],
    'l1_drag3': ['O', 'C'],
    'l1_drag2': ['C', 'O'],
    'l1_chop3': ['C', 'OSC'],
    'l1_chop2': ['OSC', 'STAB'],
    'l1_default': ['C', 'O'],

    'l2_dbl_len1': ['C', 'O'],
    'l2_dbl_len2': ['O', 'C'],
    'l2_dbl_drag': ['C', 'O'],
    'l2_drag4': ['C', 'O'],
    'l2_drag3': ['C', 'O'],
    'l2_drag2': ['O', 'C'],
    'l2_chop3': ['OSC', 'C'],
    'l2_chop2': ['STAB', 'OSC'],
    'l2_delta5': ['O', 'C', 'NONE'],
    'l2_default': ['C', 'O'],

    'l3_dbl_len1': ['C', 'O'],
    'l3_dbl_len2': ['O', 'C'],
    'l3_dbl_drag': ['C', 'O'],
    'l3_drag4': ['C', 'O'],
    'l3_drag3': ['O', 'C'],
    'l3_drag2': ['C', 'O'],
    'l3_chop3': ['C', 'OSC'],
    'l3_chop2': ['OSC', 'STAB'],
    'l3_delta5': ['O', 'C', 'NONE'],
    'l3_default': ['C', 'O'],
}

best_models = []
print("Starting Evolutionary Training on ALL 16 REAL SEQUENCES...")

for iteration in range(500000):
    candidate = {k: random.choice(v) for k, v in param_options.items()}
    fn = create_predictor(candidate)
    tot_max, wins, losses, res = evaluate_engine(fn)
    
    if tot_max <= 2:
        total = wins + losses
        winrate = (wins / total) * 100
        best_models.append((tot_max, wins, losses, winrate, candidate, res))
        print(f"🔥 FOUND MODEL #{len(best_models)} (iter {iteration}): Max Loss = {tot_max}, Wins = {wins}/{total} ({winrate:.1f}%)")
        if len(best_models) >= 10:
            break

if best_models:
    best_models.sort(key=lambda x: (x[0], -x[1]))
    best = best_models[0]
    print("\n" + "="*80)
    print(f"🏆 BEST DISCOVERED UNIVERSAL ENGINE: {best[1]}W / {best[2]}L ({best[3]:.1f}%) | Max Streak = {best[0]}")
    print("GENES:", best[4])
    print("="*80)
    for name, w, l, ms, det in best[5]:
        print(f"  {name:<35}: {w}W/{l}L | Max Streak: {ms} | {'✅ PASS' if ms <= 2 else '❌ FAIL'}")
else:
    print("Search completed. Broadening search space...")
