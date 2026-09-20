import json
import random
from dataset_real_all import all_real_sequences, get_runs, opp

with open('user_live_95_draws.json', 'r') as f:
    seq_live_96 = json.load(f)

seq_D = [s for s in all_real_sequences if s[0].startswith('Seq D')][0][1]
seq_N = [s for s in all_real_sequences if s[0].startswith('Seq N')][0][1]
seq_O = [s for s in all_real_sequences if s[0].startswith('Seq O')][0][1]
seq_P = [s for s in all_real_sequences if s[0].startswith('Seq P')][0][1]

all_master_dataset = [
    ("Seq D (30S 52065)", seq_D),
    ("Seq N (30S 52464 - Doublet Heavy)", seq_N),
    ("Seq O (30S 51819)", seq_O),
    ("Seq P (30S 51989)", seq_P),
    ("Seq Master 96-Draw Live Feed (50579-50739)", seq_live_96),
]

print(f"Master Dataset loaded: {len(all_master_dataset)} sequences with {sum(len(s[1]) for s in all_master_dataset)} total real draws.")

ACTIONS = ['SAME', 'OPP', 'LAST', 'OPP_LAST']

def build_feature_key(hist, streak):
    sizes = [x['size'] for x in hist]
    runs = get_runs(sizes)
    c_side, c_len = runs[-1]
    p_side, p_len = runs[-2] if len(runs) >= 2 else (opp(c_side), 0)
    
    alt = 0
    for r_s, r_l in reversed(runs):
        if r_l == 1: alt += 1
        else: break
        
    c_len_cat = min(c_len, 4)
    p_len_cat = min(p_len, 3)
    alt_cat = min(alt, 3)
    streak_cat = min(streak, 2)
    
    recent = sizes[-6:] if len(sizes) >= 6 else sizes
    flips = sum(1 for i in range(1, len(recent)) if recent[i] != recent[i-1])
    flip_cat = 0 if flips <= 1 else (1 if flips in (2, 3) else 2)

    return (streak_cat, c_len_cat, p_len_cat, alt_cat, flip_cat)

all_keys = set()
for name, seq in all_master_dataset:
    h = seq[:3]
    for s in [0, 1, 2]:
        for item in seq[3:]:
            k = build_feature_key(h, s)
            all_keys.add(k)
            h.append(item)

sorted_keys = sorted(list(all_keys))
print(f"Total unique feature states: {len(sorted_keys)}")

def evaluate_genome(genome):
    mapping = {k: genome[i] for i, k in enumerate(sorted_keys)}
    total_max = 0
    total_wins = 0
    total_losses = 0
    results = []
    
    for name, seq in all_master_dataset:
        hist = seq[:3]
        streak = 0
        max_s = 0
        w, l = 0, 0
        det = []
        for item in seq[3:]:
            k = build_feature_key(hist, streak)
            act_rule = mapping.get(k, 'SAME')
            sizes = [x['size'] for x in hist]
            runs = get_runs(sizes)
            c_side = runs[-1][0]
            last_s = sizes[-1]
            
            if act_rule == 'SAME': pred = c_side
            elif act_rule == 'OPP': pred = opp(c_side)
            elif act_rule == 'LAST': pred = last_s
            else: pred = opp(last_s)
            
            actual = item['size']
            if pred == actual:
                w += 1
                streak = 0
                det.append((item['period'], pred, actual, 'WIN', streak+1))
            else:
                l += 1
                streak += 1
                if streak > max_s: max_s = streak
                det.append((item['period'], pred, actual, 'LOSS', streak))
            hist.append(item)
            
        if max_s > total_max: total_max = max_s
        total_wins += w
        total_losses += l
        results.append((name, w, l, max_s, det))
        
    if total_max > 2:
        fitness = 1000 * (total_max - 2) + total_losses * 10
    else:
        fitness = - (total_wins * 2 - total_losses)
        
    return fitness, total_max, total_wins, total_losses, results

POP_SIZE = 600
GENERATIONS = 300

random.seed(7777)
population = [[random.choice(ACTIONS) for _ in sorted_keys] for _ in range(POP_SIZE)]

best_fit = float('inf')
best_sol = None
best_breakdown = None

for gen in range(GENERATIONS):
    scored = []
    for ind in population:
        f, tm, tw, tl, res = evaluate_genome(ind)
        scored.append((f, tm, tw, tl, ind, res))
        if tm <= 2 and f < best_fit:
            best_fit = f
            best_sol = (tw, tl, tm, ind)
            best_breakdown = res
            print(f"Gen {gen:4d}: NEW ZERO-BUST SOL! {tw}W / {tl}L ({(tw/(tw+tl))*100:.1f}%) | Max Streak = {tm}")
            
    scored.sort(key=lambda x: x[0])
    survivors = [x[4] for x in scored[:POP_SIZE//4]]
    new_pop = list(survivors)
    
    while len(new_pop) < POP_SIZE:
        parent1 = random.choice(survivors)
        parent2 = random.choice(survivors)
        split = random.randint(0, len(sorted_keys))
        child = parent1[:split] + parent2[split:]
        if random.random() < 0.2:
            idx = random.randint(0, len(sorted_keys)-1)
            child[idx] = random.choice(ACTIONS)
        new_pop.append(child)
    population = new_pop

print("\n" + "="*60)
if best_sol:
    tw, tl, tm, ind = best_sol
    print(f"🏆 MASTER 96-DRAW ZERO-BUST TITAN SOLVED: {tw}W / {tl}L ({(tw/(tw+tl))*100:.1f}%) | Max Streak = {tm}")
    for name, w, l, ms, det in best_breakdown:
        print(f"  {name:<44}: {w}W / {l}L | Max Streak = {ms} | {'✅ PASS' if ms <= 2 else '❌ FAIL'}")
        
    state_dict = {f"{k[0]}_{k[1]}_{k[2]}_{k[3]}_{k[4]}": ind[i] for i, k in enumerate(sorted_keys)}
    with open('v1um_master96_rules.json', 'w') as f:
        json.dump(state_dict, f, indent=2)
    print("Exported v1um_master96_rules.json successfully!")
