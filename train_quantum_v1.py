import json
import pandas as pd
import numpy as np
import random
import time

print("=" * 70)
print("🚀 TITAN QUANTUM v1.0 — 10,000+ DRAW MODEL TRAINING")
print("=" * 70)

# 1. Load Kaggle & GitHub 10,000 dataset
df = pd.read_csv('/Users/jashwanthsingh/Downloads/Win-Go.csv.csv')
df = df.iloc[::-1].reset_index(drop=True) # Chronological (oldest to newest)
kaggle_draws = [{'period': str(row['Period']), 'number': int(row['Number']), 'size': ('BIG' if row['Number'] >= 5 else 'SMALL')} for _, row in df.iterrows()]

# 2. Load active AR-Lottery live dataset
with open('/Users/jashwanthsingh/Downloads/jashvip/dataset_full_master.json') as f:
    live_draws = json.load(f)

# Merge datasets: kaggle draws followed by live draws
# Ensure uniqueness by period
seen = set()
all_draws = []
for d in kaggle_draws + live_draws:
    p = str(d['period'])
    if p not in seen:
        seen.add(p)
        all_draws.append(d)

print(f"Total merged dataset draws: {len(all_draws)}")

sizes = [d['size'] for d in all_draws]
nums = [d['number'] for d in all_draws]

def opp(s): return 'SMALL' if s == 'BIG' else 'BIG'

def get_runs(sizes):
    runs = []
    if not sizes: return runs
    curr = sizes[0]; l = 1
    for s in sizes[1:]:
        if s == curr: l += 1
        else:
            runs.append({'size': curr, 'len': l})
            curr = s; l = 1
    runs.append({'size': curr, 'len': l})
    return runs

def extract_features9(sizes, nums, streak):
    runs = get_runs(sizes)
    c_run = runs[-1]
    c_side = c_run['size']
    c_len = c_run['len']
    p_run = runs[-2] if len(runs) >= 2 else {'size': opp(c_side), 'len': 0}
    p2_run = runs[-3] if len(runs) >= 3 else {'size': c_side, 'len': 0}
    last_s = sizes[-1]
    last_n = nums[-1] if len(nums) > 0 else (7 if last_s == 'BIG' else 2)
    prev_n = nums[-2] if len(nums) >= 2 else last_n
    
    alt = 0
    for r in reversed(runs):
        if r['len'] == 1: alt += 1
        else: break
        
    c_len_cat = min(c_len, 4)
    p_len_cat = min(p_run['len'], 3)
    p2_len_cat = min(p2_run['len'], 3)
    alt_cat = min(alt, 3)
    streak_cat = min(streak, 2)
    
    recent = sizes[-6:]
    flips = sum(1 for i in range(1, len(recent)) if recent[i] != recent[i-1])
    flip_cat = 0 if flips <= 1 else (1 if (flips in [2, 3]) else 2)
    c_side_bit = 1 if c_side == 'BIG' else 0
    parity_bit = abs(last_n) % 2
    harmonic_bit = abs(last_n + prev_n) % 2
    
    key = f'{streak_cat}_{c_len_cat}_{p_len_cat}_{p2_len_cat}_{alt_cat}_{flip_cat}_{c_side_bit}_{parity_bit}_{harmonic_bit}'
    return key, c_side, last_s, c_len, alt

# Load baseline rules as starting point
with open('/Users/jashwanthsingh/Downloads/jashvip/v9um_apex_titan_supreme_9feature_rules.json') as f:
    rules = json.load(f)

# Precalculate features for evaluation window (use last 2,000 draws + live draws for high-density training)
sample_window = min(2500, len(sizes))
eval_sizes = sizes[-sample_window:]
eval_nums = nums[-sample_window:]

precalc = []
all_keys = set()
for i in range(3, len(eval_sizes)):
    s_hist = eval_sizes[:i]
    n_hist = eval_nums[:i]
    target = eval_sizes[i]
    feats = {}
    for st in [0, 1, 2]:
        f_info = extract_features9(s_hist, n_hist, st)
        feats[st] = f_info
        all_keys.add(f_info[0])
    precalc.append((feats, target))

print(f"Precalculated {len(precalc)} evaluation rounds.")
print(f"Total distinct state keys in window: {len(all_keys)}")

def evaluate(r_dict):
    streak = 0
    max_streak = 0
    wins = 0
    busts = 0
    l1_wins = 0
    l2_wins = 0
    l3_wins = 0
    
    for feats, target in precalc:
        st_cat = min(streak, 2)
        key, c_side, last_s, c_len, alt = feats[st_cat]
        fallback = c_side if c_len >= 2 else (opp(last_s) if alt >= 2 else c_side)
        act = r_dict.get(key, fallback)
        
        if act == 'SAME': pred = c_side
        elif act == 'OPP': pred = opp(c_side)
        elif act == 'LAST': pred = last_s
        elif act == 'OPP_LAST': pred = opp(last_s)
        elif act in ['BIG', 'SMALL']: pred = act
        else: pred = c_side
        
        if pred == target:
            wins += 1
            if streak == 0: l1_wins += 1
            elif streak == 1: l2_wins += 1
            else: l3_wins += 1
            streak = 0
        else:
            streak += 1
            if streak > max_streak: max_streak = streak
            if streak >= 3: busts += 1
            
    # Objective function: heavily penalize busts (streak >= 3)
    score = (wins * 10) - (busts * 1000000) - (max_streak * 5000) + (l1_wins * 5)
    return score, wins, max_streak, busts, l1_wins, l2_wins, l3_wins

initial_score, init_wins, init_max, init_busts, *_ = evaluate(rules)
print(f"Initial Baseline: Score={initial_score}, Wins={init_wins}/{len(precalc)} ({init_wins/len(precalc)*100:.1f}%), MaxStreak={init_max}, Busts={init_busts}")

# Optimization Loop using Simulated Annealing on Key Actions
best_rules = dict(rules)
best_score = initial_score
actions = ['SAME', 'OPP', 'LAST', 'OPP_LAST', 'BIG', 'SMALL']

t0 = time.time()
improvements = 0

for iteration in range(1500):
    # Pick a random key from all_keys
    k = random.choice(list(all_keys))
    orig_act = best_rules.get(k, 'SAME')
    new_act = random.choice([a for a in actions if a != orig_act])
    
    best_rules[k] = new_act
    score, wins, max_st, busts, l1, l2, l3 = evaluate(best_rules)
    
    if score >= best_score:
        best_score = score
        improvements += 1
        if busts == 0 and max_st <= 2:
            print(f"🎯 Iteration {iteration}: Perfect Zero-Bust (MaxStreak={max_st}, Busts=0, Wins={wins}, Score={score})")
            break
    else:
        # Revert
        best_rules[k] = orig_act

score, wins, max_st, busts, l1, l2, l3 = evaluate(best_rules)
print("=" * 70)
print(f"OPTIMIZATION COMPLETE in {time.time()-t0:.2f}s")
print(f"Wins: {wins}/{len(precalc)} ({wins/len(precalc)*100:.2f}%)")
print(f"Max Loss Streak: {max_st} (Target: <= 2)")
print(f"Total Busts: {busts}")
print(f"L1 Wins: {l1} | L2 Wins: {l2} | L3 Wins: {l3}")
print("=" * 70)

# Save the trained quantum v1 rules
with open('/Users/jashwanthsingh/Downloads/jashvip/quantum_v1_rules.json', 'w') as f:
    json.dump(best_rules, f, indent=2)

print(f"Saved {len(best_rules)} rules to quantum_v1_rules.json")
