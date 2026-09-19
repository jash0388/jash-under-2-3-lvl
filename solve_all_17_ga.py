from dataset_17 import all_17_seqs, get_runs, opp
import random

# Feature vector for each state
def evaluate_individual(genes):
    total_max = 0
    total_wins = 0
    total_losses = 0
    
    for name, seq in all_17_seqs:
        history = seq[:3]
        streak = 0
        max_streak = 0
        wins, losses = 0, 0
        
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

            recent_runs = runs[-4:]
            recent_doublets = sum(1 for r in recent_runs if r[1] == 2)
            recent_dragons = sum(1 for r in recent_runs if r[1] >= 3)
            is_doublet_env = (recent_doublets >= 2 or (p_len == 2 and alt <= 1))
            is_dragon_env = (recent_dragons >= 2 or p_len >= 4)

            # Determine decision
            if streak >= 2: # L3
                if alt >= 3: act = genes['l3_alt3']
                elif alt == 2: act = genes['l3_alt2']
                elif c_len >= 4: act = genes['l3_drag4']
                elif c_len == 3:
                    if p_len == 1 and p3_len == 3: act = genes['l3_trip']
                    else: act = genes['l3_drag3']
                elif c_len == 2:
                    if is_doublet_env: act = genes['l3_d2_dbl']
                    else: act = genes['l3_d2_mom']
                elif c_len == 1:
                    if is_doublet_env: act = genes['l3_d1_dbl']
                    elif is_dragon_env and p_len >= 4: act = genes['l3_d1_rev']
                    else: act = genes['l3_d1_mom']
                else: act = genes['l3_default']
            elif streak == 1: # L2
                if alt >= 3: act = genes['l2_alt3']
                elif alt == 2: act = genes['l2_alt2']
                elif c_len >= 4: act = genes['l2_drag4']
                elif c_len == 3:
                    if p_len == 1 and p3_len == 3: act = genes['l2_trip']
                    else: act = genes['l2_drag3']
                elif c_len == 2:
                    if is_doublet_env: act = genes['l2_d2_dbl']
                    else: act = genes['l2_d2_mom']
                elif c_len == 1:
                    if is_doublet_env: act = genes['l2_d1_dbl']
                    elif is_dragon_env and p_len >= 4: act = genes['l2_d1_rev']
                    else: act = genes['l2_d1_mom']
                else: act = genes['l2_default']
            else: # L1
                if alt >= 3: act = genes['l1_alt3']
                elif alt == 2: act = genes['l1_alt2']
                elif c_len >= 4: act = genes['l1_drag4']
                elif c_len == 3:
                    if p_len == 1 and p3_len == 3: act = genes['l1_trip']
                    else: act = genes['l1_drag3']
                elif c_len == 2:
                    if is_doublet_env: act = genes['l1_d2_dbl']
                    else: act = genes['l1_d2_mom']
                elif c_len == 1:
                    if is_doublet_env: act = genes['l1_d1_dbl']
                    elif is_dragon_env and p_len >= 4: act = genes['l1_d1_rev']
                    else: act = genes['l1_d1_mom']
                else: act = genes['l1_default']

            if act == 'C': pred = c_side
            elif act == 'O': pred = opp(c_side)
            elif act == 'OSC': pred = opp(last_s)
            elif act == 'STAB': pred = last_s
            else: pred = c_side

            act_size = item['size']
            if pred == act_size:
                wins += 1
                streak = 0
            else:
                losses += 1
                streak += 1
                if streak > max_streak:
                    max_streak = streak
            history.append(item)
            
        if max_streak > total_max:
            total_max = max_streak
        total_wins += wins
        total_losses += losses
        
    return total_max, total_wins, total_losses

gene_keys = [
    'l1_alt3', 'l1_alt2', 'l1_drag4', 'l1_drag3', 'l1_trip', 'l1_d2_dbl', 'l1_d2_mom', 'l1_d1_dbl', 'l1_d1_rev', 'l1_d1_mom', 'l1_default',
    'l2_alt3', 'l2_alt2', 'l2_drag4', 'l2_drag3', 'l2_trip', 'l2_d2_dbl', 'l2_d2_mom', 'l2_d1_dbl', 'l2_d1_rev', 'l2_d1_mom', 'l2_default',
    'l3_alt3', 'l3_alt2', 'l3_drag4', 'l3_drag3', 'l3_trip', 'l3_d2_dbl', 'l3_d2_mom', 'l3_d1_dbl', 'l3_d1_rev', 'l3_d1_mom', 'l3_default',
]

gene_options = {
    'l1_alt3': ['OSC', 'C'], 'l1_alt2': ['OSC', 'STAB'], 'l1_drag4': ['C', 'O'], 'l1_drag3': ['O', 'C'], 'l1_trip': ['O', 'C'],
    'l1_d2_dbl': ['O', 'C'], 'l1_d2_mom': ['C', 'O'], 'l1_d1_dbl': ['C', 'O'], 'l1_d1_rev': ['C', 'O'], 'l1_d1_mom': ['C', 'O'], 'l1_default': ['C', 'O'],

    'l2_alt3': ['OSC', 'C'], 'l2_alt2': ['STAB', 'OSC'], 'l2_drag4': ['C', 'O'], 'l2_drag3': ['C', 'O'], 'l2_trip': ['O', 'C'],
    'l2_d2_dbl': ['O', 'C'], 'l2_d2_mom': ['C', 'O'], 'l2_d1_dbl': ['C', 'O'], 'l2_d1_rev': ['C', 'O'], 'l2_d1_mom': ['C', 'O'], 'l2_default': ['C', 'O'],

    'l3_alt3': ['OSC', 'C'], 'l3_alt2': ['OSC', 'STAB'], 'l3_drag4': ['C', 'O'], 'l3_drag3': ['O', 'C'], 'l3_trip': ['O', 'C'],
    'l3_d2_dbl': ['O', 'C'], 'l3_d2_mom': ['C', 'O'], 'l3_d1_dbl': ['C', 'O'], 'l3_d1_rev': ['C', 'O'], 'l3_d1_mom': ['C', 'O'], 'l3_default': ['C', 'O'],
}

print("Running Genetic Search across all 17 sequences...")
random.seed(42)
winning = []

for iteration in range(200000):
    ind = {k: random.choice(gene_options[k]) for k in gene_keys}
    tm, tw, tl = evaluate_individual(ind)
    if tm <= 2:
        winning.append((tw, tl, tm, ind))
        print(f"🔥 FOUND WINNING MODEL #{len(winning)} (iter {iteration}): Max Streak = {tm}, Wins = {tw}/{tw+tl} ({(tw/(tw+tl))*100:.1f}%)")
        if len(winning) >= 10:
            break

if winning:
    winning.sort(key=lambda x: x[0], reverse=True)
    best_w, best_l, best_m, best_ind = winning[0]
    print("\n" + "="*80)
    print(f"🏆 TOP WINNING MODEL: {best_w}W / {best_l}L ({(best_w/(best_w+best_l))*100:.1f}%) | Max Streak = {best_m}")
    print("GENES:")
    for k, v in best_ind.items():
        print(f"  '{k}': '{v}',")
    print("="*80)
else:
    print("Search done.")
