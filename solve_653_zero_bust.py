import json
import random
import time

with open('dataset_full_master.json') as f:
    data = json.load(f)

sizes = [d['size'] for d in data]
nums = [d['number'] for d in data]

with open('v9um_apex_titan_supreme_9feature_rules.json') as f:
    rules = json.load(f)

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

# Precalculate features for 653 dataset
precalc = []
all_keys = set()
for i in range(3, len(sizes)):
    s_hist = sizes[:i]
    n_hist = nums[:i]
    target = sizes[i]
    feats = {}
    for st in [0, 1, 2]:
        f_info = extract_features9(s_hist, n_hist, st)
        feats[st] = f_info
        all_keys.add(f_info[0])
    precalc.append((feats, target))

print(f'Total rounds: {len(precalc)}')
print(f'Total distinct keys: {len(all_keys)}')

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
        act = r_dict.get(key)
        if not act:
            if streak >= 2: act = c_side if c_len >= 2 else (opp(last_s) if alt >= 2 else c_side)
            elif streak == 1: act = c_side if c_len >= 2 else (opp(last_s) if alt >= 2 else opp(c_side))
            else: act = c_side if c_len >= 3 else (opp(c_side) if c_len == 2 else (opp(last_s) if alt >= 2 else c_side))
        
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
            if streak > 2: busts += 1
            if streak > max_streak: max_streak = streak
            
    score = (wins * 100) - (busts * 10000000) - (max(0, max_streak - 2) * 50000000) + (l1_wins * 20) + (l2_wins * 10)
    return score, wins, max_streak, busts, l1_wins, l2_wins, l3_wins

score, wins, max_st, busts, l1, l2, l3 = evaluate(rules)
print(f'Initial: Score={score}, Wins={wins}/{len(precalc)} ({wins/len(precalc)*100:.1f}%), MaxStreak={max_st}, Busts={busts}')

candidates = ['SAME', 'OPP', 'LAST', 'OPP_LAST', 'BIG', 'SMALL']
best_rules = dict(rules)
best_score = score
best_ms = max_st
best_busts = busts

streak_2_keys = [k for k in all_keys if k.startswith('2_')]
streak_1_keys = [k for k in all_keys if k.startswith('1_')]
streak_0_keys = [k for k in all_keys if k.startswith('0_')]

t0 = time.time()
for iteration in range(20):
    improved = False
    random.shuffle(streak_2_keys)
    round_keys = streak_2_keys + streak_1_keys + streak_0_keys
    
    for k in round_keys:
        curr_act = best_rules.get(k, 'SAME')
        best_act_for_key = curr_act
        
        for cand in candidates:
            if cand == curr_act: continue
            best_rules[k] = cand
            sc, w, ms, b, l1, l2, l3 = evaluate(best_rules)
            if sc > best_score:
                best_score = sc
                best_ms = ms
                best_busts = b
                best_act_for_key = cand
                improved = True
                print(f'Iter {iteration} Key {k} -> {cand}: Score={sc}, Wins={w}, MaxStreak={ms}, Busts={b}')
                
        best_rules[k] = best_act_for_key

    print(f'--- End of Iteration {iteration}: MaxStreak={best_ms}, Busts={best_busts}, Score={best_score} ---')
    if best_ms <= 2 and best_busts == 0:
        print('🎯 PERFECT ZERO-BUST ACHIEVED (Max Streak <= 2) on all 653 draws!')
        # Refinement passes
        for ref in range(2):
            for k in streak_0_keys + streak_1_keys:
                curr_act = best_rules.get(k, 'SAME')
                for cand in candidates:
                    if cand == curr_act: continue
                    best_rules[k] = cand
                    sc, w, ms, b, l1, l2, l3 = evaluate(best_rules)
                    if ms <= 2 and b == 0 and sc > best_score:
                        best_score = sc
                        curr_act = cand
                        print(f'Refinement: {k} -> {cand} | Wins={w}')
                best_rules[k] = curr_act
        break

t1 = time.time()
final_sc, final_w, final_ms, final_b, final_l1, final_l2, final_l3 = evaluate(best_rules)

print('=' * 70)
print(f'TRAINING ON ALL 653 DRAWS COMPLETE in {t1-t0:.2f}s')
print(f'Wins: {final_w}/{len(precalc)} ({final_w/len(precalc)*100:.2f}%)')
print(f'Max Loss Streak: {final_ms} (Target: <= 2)')
print(f'Total Busts (Streak >= 3): {final_b} (Target: 0)')
print(f'L1 Wins: {final_l1} ({final_l1/final_w*100:.1f}%)')
print(f'L2 Wins: {final_l2} ({final_l2/final_w*100:.1f}%)')
print(f'L3 Wins: {final_l3} ({final_l3/final_w*100:.1f}%)')
print('=' * 70)

with open('v9um_apex_titan_supreme_9feature_rules.json', 'w') as f:
    json.dump(best_rules, f, indent=2)

print('Updated v9um_apex_titan_supreme_9feature_rules.json with 653-draw zero-bust rules!')
