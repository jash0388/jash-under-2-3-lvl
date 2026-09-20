import json

with open('all_master_30s_dataset.json') as f:
    datasets = json.load(f)

def opp(s): return 'SMALL' if s == 'BIG' else 'BIG'

def get_runs(sizes):
    if not sizes: return []
    runs = []
    curr = sizes[0]
    l = 1
    for s in sizes[1:]:
        if s == curr: l += 1
        else:
            runs.append({'size': curr, 'len': l})
            curr = s
            l = 1
    runs.append({'size': curr, 'len': l})
    return runs

def extract_features(sizes, streak):
    runs = get_runs(sizes)
    c_run = runs[-1]
    c_side = c_run['size']
    c_len = c_run['len']
    p_run = runs[-2] if len(runs) >= 2 else {'size': opp(c_side), 'len': 0}
    p2_run = runs[-3] if len(runs) >= 3 else {'size': c_side, 'len': 0}
    last_s = sizes[-1]

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
    flips = 0
    for i in range(1, len(recent)):
        if recent[i] != recent[i-1]: flips += 1
    flip_cat = 0 if flips <= 1 else (1 if flips in [2, 3] else 2)
    c_side_bit = 1 if c_side == 'BIG' else 0

    key = f'{streak_cat}_{c_len_cat}_{p_len_cat}_{p2_len_cat}_{alt_cat}_{flip_cat}_{c_side_bit}'
    return key, c_side, last_s, c_len, alt, p_run['len']

def simulate(rules_dict, verbose=False):
    total_wins, total_losses = 0, 0
    total_l1_w, total_l2_w, total_l3_w = 0, 0, 0
    max_streak_all = 0
    feed_results = []

    for name, data in datasets:
        sizes = [d['size'] for d in data]
        nums = [d['number'] for d in data]
        periods = [d['period'] for d in data]
        
        streak = 0
        max_streak = 0
        wins, losses = 0, 0
        l1_w, l2_w, l3_w = 0, 0, 0
        
        for i in range(3, len(sizes)):
            key, c_side, last_s, c_len, alt, p_len = extract_features(sizes[:i], streak)
            fallback = 'SAME' if c_len >= 2 else ('OPP_LAST' if alt >= 2 else ('OPP_LAST' if p_len >= 3 else 'SAME'))
            act_rule = rules_dict.get(key, fallback)
            
            if act_rule == 'SAME': pred = c_side
            elif act_rule == 'OPP': pred = opp(c_side)
            elif act_rule == 'LAST': pred = last_s
            elif act_rule == 'OPP_LAST': pred = opp(last_s)
            else: pred = c_side

            actual = sizes[i]
            
            if pred == actual:
                wins += 1
                if streak == 0: l1_w += 1
                elif streak == 1: l2_w += 1
                elif streak == 2: l3_w += 1
                streak = 0
            else:
                losses += 1
                streak += 1
                max_streak = max(max_streak, streak)
                if verbose and streak >= 3:
                    print(f'🚨 BUST at {periods[i]} in {name}: pred={pred}, act={actual}({nums[i]}), key={key}, rule={act_rule}, streak={streak}')

        max_streak_all = max(max_streak_all, max_streak)
        total_wins += wins
        total_losses += losses
        total_l1_w += l1_w
        total_l2_w += l2_w
        total_l3_w += l3_w
        feed_results.append((name, wins, losses, max_streak, l1_w, l2_w, l3_w))

    return total_wins, total_losses, max_streak_all, total_l1_w, total_l2_w, total_l3_w, feed_results

# Generate full state space
actions = ['SAME', 'OPP', 'LAST', 'OPP_LAST']
all_keys = []
for st in range(3):
    for c in range(1, 5):
        for p in range(4):
            for p2 in range(4):
                for a in range(4):
                    for fl in range(3):
                        for cs in [0, 1]:
                            all_keys.append(f'{st}_{c}_{p}_{p2}_{a}_{fl}_{cs}')

print(f'Total possible states in 7-feature grammar: {len(all_keys)}')

# Load existing v6um rules as base
with open('v6um_perfect_30s_rules.json') as f:
    best_rules = json.load(f)

# Fill any missing keys with default invariant
for k in all_keys:
    if k not in best_rules:
        st, c, p, p2, a, fl, cs = map(int, k.split('_'))
        if c >= 2:
            best_rules[k] = 'SAME'
        elif a >= 2:
            best_rules[k] = 'OPP_LAST'
        elif p >= 3:
            best_rules[k] = 'OPP_LAST'
        else:
            best_rules[k] = 'SAME'

w, l, ms, l1, l2, l3, f_res = simulate(best_rules, verbose=True)
print(f'Baseline v6UM: Wins={w}/{w+l} ({w/(w+l)*100:.1f}%), MaxStreak={ms}, L1={l1}, L2={l2}, L3={l3}')
for fr in f_res:
    print(f'  {fr[0]}: W={fr[1]}, L={fr[2]}, MaxStreak={fr[3]}, L1={fr[4]}, L2={fr[5]}, L3={fr[6]}')

