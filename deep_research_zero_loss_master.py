import random
from dataset_real_all import all_real_sequences, get_runs, opp
from solve_all9_zero_bust import all_9_30s

seq_V = [
    {'period': '50720', 'number': 3, 'size': 'SMALL'},
    {'period': '50721', 'number': 8, 'size': 'BIG'},
    {'period': '50722', 'number': 8, 'size': 'BIG'},
    {'period': '50723', 'number': 2, 'size': 'SMALL'},
    {'period': '50724', 'number': 1, 'size': 'SMALL'},
    {'period': '50725', 'number': 7, 'size': 'BIG'},
    {'period': '50726', 'number': 9, 'size': 'BIG'},
    {'period': '50727', 'number': 3, 'size': 'SMALL'},
    {'period': '50728', 'number': 8, 'size': 'BIG'},
    {'period': '50729', 'number': 5, 'size': 'BIG'},
    {'period': '50730', 'number': 2, 'size': 'SMALL'},
    {'period': '50731', 'number': 2, 'size': 'SMALL'},
    {'period': '50732', 'number': 4, 'size': 'SMALL'},
    {'period': '50733', 'number': 7, 'size': 'BIG'},
    {'period': '50734', 'number': 8, 'size': 'BIG'},
    {'period': '50735', 'number': 3, 'size': 'SMALL'},
]

all_10_30s = all_9_30s + [('Seq V (50720-50735 Latest Screenshot)', seq_V)]
print(f"Loaded {len(all_10_30s)} Real Market Sequences with {sum(len(s[1]) for s in all_10_30s)} total real draws.")

# Comprehensive Mathematical Evaluation
def evaluate_on_real_and_sim(pred_fn):
    # 1. Real Market Sequences
    real_max_streak = 0
    real_wins, real_losses = 0, 0
    real_results = []
    
    for name, seq in all_10_30s:
        hist = seq[:3]
        streak = 0
        max_s = 0
        w, l = 0, 0
        det = []
        for item in seq[3:]:
            pred, tag = pred_fn(hist, streak)
            act = item['size']
            if pred == act:
                w += 1
                streak = 0
                det.append((item['period'], pred, act, 'WIN', streak+1, tag))
            else:
                l += 1
                streak += 1
                if streak > max_s: max_s = streak
                det.append((item['period'], pred, act, 'LOSS', streak, tag))
            hist.append(item)
        if max_s > real_max_streak: real_max_streak = max_s
        real_wins += w
        real_losses += l
        real_results.append((name, w, l, max_s, det))
        
    return real_max_streak, real_wins, real_losses, real_results

# Let's test fundamental deterministic architectures
# Architecture: Dual-Regime Antiphase-Free Core

# Parameter space:
# L1_dragon: 'RIDE' vs 'CUT4' vs 'CUT3'
# L1_chop: 'OSC' vs 'STAB'
# L1_single_after_run: 'RIDE' (doublet attempt) vs 'BOUNCE' (chop entry)
# L1_single_after_chop: 'OSC' vs 'RIDE'

# L2_dragon: 'RIDE' vs 'CUT'
# L2_chop: 'OSC' vs 'STAB'
# L2_single_after_run: 'RIDE' vs 'BOUNCE'
# L2_single_after_chop: 'OSC' vs 'RIDE'

# L3_dragon: 'RIDE' vs 'CUT'
# L3_chop: 'OSC' vs 'STAB'
# L3_single_after_run: 'RIDE' vs 'BOUNCE'
# L3_single_after_chop: 'OSC' vs 'RIDE'

import itertools

options = {
    'l1_dragon': ['RIDE', 'CUT4', 'CUT3'],
    'l1_chop': ['OSC', 'STAB'],
    'l1_single_after_run': ['RIDE', 'BOUNCE'],
    'l1_single_after_chop': ['OSC', 'RIDE'],
    
    'l2_dragon': ['RIDE', 'CUT'],
    'l2_chop': ['OSC', 'STAB'],
    'l2_single_after_run': ['RIDE', 'BOUNCE'],
    'l2_single_after_chop': ['OSC', 'RIDE'],
    
    'l3_dragon': ['RIDE', 'CUT'],
    'l3_chop': ['OSC', 'STAB'],
    'l3_single_after_run': ['RIDE', 'BOUNCE'],
    'l3_single_after_chop': ['OSC', 'RIDE'],
}

best_solutions = []

keys = list(options.keys())
values = list(options.values())

for combination in itertools.product(*values):
    cfg = dict(zip(keys, combination))
    
    def make_pred(config):
        def pred(hist, streak):
            sizes = [x['size'] for x in hist]
            runs = get_runs(sizes)
            c_side, c_len = runs[-1]
            p_side, p_len = runs[-2] if len(runs) >= 2 else (opp(c_side), 0)
            last_s = sizes[-1]
            
            alt = 0
            for r_s, r_l in reversed(runs):
                if r_l == 1: alt += 1
                else: break
                
            if streak >= 2: # L3
                if c_len >= 2:
                    return (c_side if config['l3_dragon'] == 'RIDE' else opp(c_side)), "L3_DRAGON"
                elif alt >= 2:
                    return (opp(last_s) if config['l3_chop'] == 'OSC' else last_s), "L3_CHOP"
                else: # c_len == 1
                    if p_len >= 2:
                        return (c_side if config['l3_single_after_run'] == 'RIDE' else opp(c_side)), "L3_S_RUN"
                    else:
                        return (opp(last_s) if config['l3_single_after_chop'] == 'OSC' else last_s), "L3_S_CHOP"
                        
            elif streak == 1: # L2
                if c_len >= 2:
                    return (c_side if config['l2_dragon'] == 'RIDE' else opp(c_side)), "L2_DRAGON"
                elif alt >= 2:
                    return (opp(last_s) if config['l2_chop'] == 'OSC' else last_s), "L2_CHOP"
                else: # c_len == 1
                    if p_len >= 2:
                        return (c_side if config['l2_single_after_run'] == 'RIDE' else opp(c_side)), "L2_S_RUN"
                    else:
                        return (opp(last_s) if config['l2_single_after_chop'] == 'OSC' else last_s), "L2_S_CHOP"
                        
            else: # L1
                if c_len >= 4 and config['l1_dragon'] == 'CUT4':
                    return opp(c_side), "L1_DRAGON_CUT4"
                elif c_len >= 3 and config['l1_dragon'] == 'CUT3':
                    return opp(c_side), "L1_DRAGON_CUT3"
                elif c_len >= 2:
                    return c_side, "L1_DRAGON_RIDE"
                elif alt >= 2:
                    return (opp(last_s) if config['l1_chop'] == 'OSC' else last_s), "L1_CHOP"
                else: # c_len == 1
                    if p_len >= 2:
                        return (c_side if config['l1_single_after_run'] == 'RIDE' else opp(c_side)), "L1_S_RUN"
                    else:
                        return (opp(last_s) if config['l1_single_after_chop'] == 'OSC' else last_s), "L1_S_CHOP"
                        
        return pred

    fn = make_pred(cfg)
    ms, tw, tl, res = evaluate_on_real_and_sim(fn)
    if ms <= 2:
        best_solutions.append((tw, tl, ms, cfg, res))

print(f"\nFound {len(best_solutions)} pure deterministic architectures with MAX LOSS <= 2 across ALL 10 real sequences!")

if best_solutions:
    best_solutions.sort(key=lambda x: (-x[0], x[2]))
    for i, (tw, tl, ms, cfg, res) in enumerate(best_solutions[:3]):
        print(f"\n{'='*60}")
        print(f"🏆 ARCHITECTURE #{i+1}: {tw}W / {tl}L ({(tw/(tw+tl))*100:.1f}%) | Max Streak = {ms}")
        print("Configuration:")
        for k, v in cfg.items():
            print(f"  {k}: '{v}',")
        print("\nSequence Breakdown:")
        for name, w, l, s_ms, det in res:
            print(f"  {name:<44}: {w}W / {l}L | ms={s_ms} | {'✅ PASS' if s_ms <= 2 else '❌ FAIL'}")
else:
    print("No combination achieved max streak <= 2. Checking closest:")
