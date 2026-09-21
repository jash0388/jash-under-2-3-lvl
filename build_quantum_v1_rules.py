import json
from collections import defaultdict

# 1. Load active 674 zero-bust rules (perfect accuracy on current AR-Lottery sequence)
with open('/Users/jashwanthsingh/Downloads/jashvip/v9um_apex_titan_supreme_9feature_rules.json') as f:
    active_rules = json.load(f)

# 2. Load 10,000 Kaggle dataset to compute state confidence probabilities
import pandas as pd
df = pd.read_csv('/Users/jashwanthsingh/Downloads/Win-Go.csv.csv')
df = df.iloc[::-1].reset_index(drop=True)
sizes = [('BIG' if n >= 5 else 'SMALL') for n in df['Number']]
nums = df['Number'].tolist()

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

# Calculate state counts
state_counts = defaultdict(lambda: {'total': 0, 'BIG': 0, 'SMALL': 0})
for i in range(10, len(sizes)):
    s_hist = sizes[:i]
    n_hist = nums[:i]
    target = sizes[i]
    for st in [0, 1, 2]:
        k = extract_features9(s_hist, n_hist, st)[0]
        state_counts[k]['total'] += 1
        state_counts[k][target] += 1

print(f"Computed statistics for {len(state_counts)} distinct states from 10k draws.")

# Combine active zero-bust rules with 10k empirical Bayesian fallback
quantum_v1_rules = dict(active_rules)

# Add any keys from 10k dataset that aren't in active_rules
added_keys = 0
for k, counts in state_counts.items():
    if k not in quantum_v1_rules:
        # Pick best action based on empirical data
        if counts['BIG'] > counts['SMALL']:
            quantum_v1_rules[k] = 'BIG'
        elif counts['SMALL'] > counts['BIG']:
            quantum_v1_rules[k] = 'SMALL'
        else:
            quantum_v1_rules[k] = 'SAME'
        added_keys += 1

print(f"Total Quantum v1.0 rules: {len(quantum_v1_rules)} (Added {added_keys} generalized state keys)")

with open('/Users/jashwanthsingh/Downloads/jashvip/quantum_v1_rules.json', 'w') as f:
    json.dump(quantum_v1_rules, f, indent=2)

print("Saved to /Users/jashwanthsingh/Downloads/jashvip/quantum_v1_rules.json")
