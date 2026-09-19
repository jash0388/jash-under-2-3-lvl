import itertools
from research_cascade_breaker import all_12_seqs, get_runs, opp

def run_simulation(predictor_fn):
    total_max = 0
    results = []
    for name, seq in all_12_seqs:
        history = seq[:3]
        streak = 0
        max_streak = 0
        wins, losses = 0, 0
        details = []
        for item in seq[3:]:
            pred, tag = predictor_fn(history, streak)
            act = item['size']
            if pred == act:
                wins += 1
                details.append((item['period'], pred, act, 'WIN', streak + 1, tag))
                streak = 0
            else:
                losses += 1
                streak += 1
                if streak > max_streak: max_streak = streak
                details.append((item['period'], pred, act, 'LOSS', streak, tag))
            history.append(item)
        total_max = max(total_max, max_streak)
        results.append((name, wins, losses, max_streak, details))
    return total_max, results

# Let's define flexible component generators
def build_engine(
    l1_chop_len,      # 2, 3
    l1_dragon_len,    # 2, 3
    l1_doublet_mode,  # True, False
    l2_strategy,      # 'follow_last', 'anti_last', 'ride_run_else_chop', 'smart_run'
    l3_strategy,      # 'follow_last', 'anti_last', 'ride_run_else_chop', 'smart_run', 'flip_on_chop'
    weight_decay,     # 1.3, 1.5, 1.8
):
    def predictor(history, loss_streak):
        sizes = [x['size'] for x in history]
        nums = [x['number'] for x in history]
        runs = get_runs(sizes)
        c_side, c_len = runs[-1]
        p_side, p_len = runs[-2] if len(runs) >= 2 else (opp(c_side), 0)
        p3_side, p3_len = runs[-3] if len(runs) >= 3 else (c_side, 0)
        last_s = sizes[-1]
        last_n = nums[-1]
        prev_n = nums[-2] if len(nums) >= 2 else last_n

        alt = 0
        for r_s, r_l in reversed(runs):
            if r_l == 1: alt += 1
            else: break

        # Level 3 Recovery
        if loss_streak >= 2:
            if l3_strategy == 'follow_last':
                return last_s, f"L3 FOLLOW ({last_s})"
            elif l3_strategy == 'anti_last':
                return opp(last_s), f"L3 ANTI ({opp(last_s)})"
            elif l3_strategy == 'ride_run_else_chop':
                if c_len >= 2: return c_side, f"L3 RIDE RUN ({c_side})"
                if alt >= 2: return opp(last_s), f"L3 CHOP FLIP ({opp(last_s)})"
                return last_s, f"L3 MOMENTUM ({last_s})"
            elif l3_strategy == 'smart_run':
                if c_len >= 2: return c_side, f"L3 RIDE RUN ({c_side})"
                if alt >= 3: return opp(last_s), f"L3 CHOP FLIP ({opp(last_s)})"
                return last_s, f"L3 MOMENTUM ({last_s})"
            elif l3_strategy == 'flip_on_chop':
                if alt >= 2: return opp(last_s), f"L3 CHOP FLIP ({opp(last_s)})"
                return last_s, f"L3 MOMENTUM ({last_s})"

        # Level 2 Recovery
        elif loss_streak == 1:
            if l2_strategy == 'follow_last':
                return last_s, f"L2 FOLLOW ({last_s})"
            elif l2_strategy == 'anti_last':
                return opp(last_s), f"L2 ANTI ({opp(last_s)})"
            elif l2_strategy == 'ride_run_else_chop':
                if c_len >= 2: return c_side, f"L2 RIDE RUN ({c_side})"
                if alt >= 2: return opp(last_s), f"L2 CHOP FLIP ({opp(last_s)})"
                return last_s, f"L2 MOMENTUM ({last_s})"
            elif l2_strategy == 'smart_run':
                if c_len >= 2: return c_side, f"L2 RIDE RUN ({c_side})"
                if alt >= 3: return opp(last_s), f"L2 CHOP FLIP ({opp(last_s)})"
                return last_s, f"L2 MOMENTUM ({last_s})"

        # Level 1 Base Prediction
        else:
            if c_len >= l1_dragon_len:
                return c_side, f"L1 DRAGON ({c_side} x{c_len})"
            if l1_doublet_mode and c_len == 1 and p_len == 2 and p3_len == 1:
                return p_side, f"L1 DOUBLET ({p_side})"
            if alt >= l1_chop_len:
                return opp(last_s), f"L1 CHOP ({opp(last_s)})"
            
            # Micro-trend / recency weighting
            w = sizes[-5:]
            b_score = sum(weight_decay**i for i, s in enumerate(w) if s == "BIG")
            s_score = sum(weight_decay**i for i, s in enumerate(w) if s == "SMALL")
            if b_score > s_score: return "BIG", "L1 TREND BIG"
            elif s_score > b_score: return "SMALL", "L1 TREND SMALL"
            else: return last_s, f"L1 MOMENTUM ({last_s})"

    return predictor

# Search
best_configs = []
for l1_chop in [2, 3]:
    for l1_drag in [2, 3, 4]:
        for l1_doub in [True, False]:
            for l2_strat in ['follow_last', 'anti_last', 'ride_run_else_chop', 'smart_run']:
                for l3_strat in ['follow_last', 'anti_last', 'ride_run_else_chop', 'smart_run', 'flip_on_chop']:
                    for w_dec in [1.3, 1.5, 1.8, 2.0]:
                        fn = build_engine(l1_chop, l1_drag, l1_doub, l2_strat, l3_strat, w_dec)
                        tot_max, results = run_simulation(fn)
                        if tot_max <= 2:
                            best_configs.append((tot_max, (l1_chop, l1_drag, l1_doub, l2_strat, l3_strat, w_dec), results))

print(f"Total configurations with max consecutive loss <= 2: {len(best_configs)}")
if best_configs:
    best_configs.sort(key=lambda x: sum(r[1] for r in x[2]), reverse=True) # Sort by total wins
    for tot_max, cfg, results in best_configs[:10]:
        total_wins = sum(r[1] for r in results)
        total_losses = sum(r[2] for r in results)
        win_rate = total_wins / (total_wins + total_losses) * 100
        print(f"Config {cfg} -> Total Wins: {total_wins}/{total_wins+total_losses} ({win_rate:.1f}%), Max Loss: {tot_max}")
