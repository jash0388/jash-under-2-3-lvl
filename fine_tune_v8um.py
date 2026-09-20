import json, random

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

def simulate(rules_dict):
    total_wins, total_losses = 0, 0
    total_l1_w, total_l2_w, total_l3_w = 0, 0, 0
    max_streak_all = 0
    busts = 0
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
            fallback = 'SAME' if c_len >= 2 else ('OPP_LAST' if alt >= 2 else ('SAME' if p_len >= 2 else 'SAME'))
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
                if streak >= 3:
                    busts += (streak - 2)

        max_streak_all = max(max_streak_all, max_streak)
        total_wins += wins
        total_losses += losses
        total_l1_w += l1_w
        total_l2_w += l2_w
        total_l3_w += l3_w
        feed_results.append((name, wins, losses, max_streak, l1_w, l2_w, l3_w))

    return total_wins, total_losses, max_streak_all, busts, total_l1_w, total_l2_w, total_l3_w, feed_results

def score(w, l, ms, busts, l1, l2, l3):
    return (w * 15.0) - (l * 2.0) - (busts * 500000.0) - (max(0, ms - 2) * 2000000.0) + (l1 * 10.0) + (l2 * 4.0)

with open('v8um_supreme_master_30s_rules.json') as f:
    rules = json.load(f)

actions = ['SAME', 'OPP', 'LAST', 'OPP_LAST']

# Collect active keys
active_keys = set()
for name, data in datasets:
    sizes = [d['size'] for d in data]
    for s in range(3):
        for i in range(3, len(sizes)):
            k, _, _, _, _, _ = extract_features(sizes[:i], s)
            active_keys.add(k)

w, l, ms, busts, l1, l2, l3, f_res = simulate(rules)
best_score = score(w, l, ms, busts, l1, l2, l3)
print(f'Starting Score: {best_score:.1f}, Wins={w}/{w+l} ({w/(w+l)*100:.1f}%), MaxStreak={ms}, Busts={busts}, L1={l1}, L2={l2}, L3={l3}')

# Fine-tuning passes focusing on Level 1 and Level 2 accuracy
for it in range(20):
    improved = False
    for k in sorted(active_keys):
        st, c, p, p2, a, fl, cs = map(int, k.split('_'))
        orig = rules[k]
        
        cand_actions = actions[:]
        if st >= 1 and c >= 2:
            cand_actions = ['SAME', 'LAST']
            
        for act in cand_actions:
            if act == orig: continue
            rules[k] = act
            w, l, ms, busts, l1, l2, l3, _ = simulate(rules)
            sc = score(w, l, ms, busts, l1, l2, l3)
            if sc > best_score and ms <= 2 and busts == 0:
                best_score = sc
                orig = act
                improved = True
                print(f'Fine-tune Iter {it}: {k} -> {act} | Score={sc:.1f}, W={w}/{w+l} ({w/(w+l)*100:.1f}%), L1={l1}, L2={l2}, L3={l3}')
        rules[k] = orig
    if not improved:
        break

w, l, ms, busts, l1, l2, l3, f_res = simulate(rules)
print('\n================ OPTIMAL v8UM ZERO-BUST RESULTS ================')
print(f'Total Across All 9 Feeds (274 draws): Wins={w}/{w+l} ({w/(w+l)*100:.1f}%), MaxStreak={ms}, Busts={busts}')
print(f'Distribution: L1 Wins={l1} ({l1/w*100:.1f}%), L2 Wins={l2} ({l2/w*100:.1f}%), L3 Wins={l3} ({l3/w*100:.1f}%)')
print('----------------------------------------------------------------')
for fr in f_res:
    print(f'{fr[0]}: W={fr[1]}, L={fr[2]} ({fr[1]/(fr[1]+fr[2])*100:.1f}%) | MaxStreak={fr[3]} | L1={fr[4]}, L2={fr[5]}, L3={fr[6]}')

with open('v8um_supreme_master_30s_rules.json', 'w') as f:
    json.dump(rules, f, indent=2)

print('Saved optimized v8um_supreme_master_30s_rules.json successfully.')
