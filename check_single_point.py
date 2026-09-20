import json

with open('all_master_combined_574.json') as f:
    new_dataset = json.load(f)

with open('v9um_apex_titan_supreme_8feature_rules.json') as f:
    rules = json.load(f)

def opp(s): return 'SMALL' if s == 'BIG' else 'BIG'

def get_runs(sizes):
    if not sizes: return []
    runs = []
    curr = sizes[0]; l = 1
    for s in sizes[1:]:
        if s == curr: l += 1
        else: runs.append({'size': curr, 'len': l}); curr = s; l = 1
    runs.append({'size': curr, 'len': l})
    return runs

def extract_features_8(sizes, nums, streak):
    runs = get_runs(sizes)
    c_run = runs[-1]
    c_side = c_run['size']
    c_len = c_run['len']
    p_run = runs[-2] if len(runs) >= 2 else {'size': opp(c_side), 'len': 0}
    p2_run = runs[-3] if len(runs) >= 3 else {'size': c_side, 'len': 0}
    last_s = sizes[-1]
    last_n = nums[-1]

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
    parity_bit = last_n % 2

    key = f'{streak_cat}_{c_len_cat}_{p_len_cat}_{p2_len_cat}_{alt_cat}_{flip_cat}_{c_side_bit}_{parity_bit}'
    return key, c_side, last_s, c_len, alt, p_run['len']

for name, data in new_dataset:
    sizes = [d['size'] for d in data]
    nums = [d['number'] for d in data]
    periods = [d['period'] for d in data]
    streak = 0
    for i in range(3, len(sizes)):
        key, c_side, last_s, c_len, alt, p_len = extract_features_8(sizes[:i], nums[:i], streak)
        if streak >= 2: fallback = c_side if c_len >= 2 else (opp(last_s) if alt >= 2 else c_side)
        elif streak == 1: fallback = c_side if c_len >= 2 else (opp(last_s) if alt >= 2 else opp(c_side))
        else: fallback = c_side if c_len >= 3 else (opp(c_side) if c_len == 2 else (opp(last_s) if alt >= 2 else c_side))
        act_rule = rules.get(key, fallback)
        if act_rule == 'SAME': pred = c_side
        elif act_rule == 'OPP': pred = opp(c_side)
        elif act_rule == 'LAST': pred = last_s
        elif act_rule == 'OPP_LAST': pred = opp(last_s)
        else: pred = c_side
        actual = sizes[i]
        if pred == actual: streak = 0
        else:
            streak += 1
            if streak >= 3:
                print(f'{name} at period {periods[i]} (num {nums[i]}, act {actual}): Streak={streak}, Key={key}, ActRule={act_rule}, Pred={pred}')
