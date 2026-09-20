import random
import itertools
from dataset_real_all import all_real_sequences
from test_regime_shield import rows

all_eval = [('User 244 Draws', rows)] + all_real_sequences

ACTIONS = ['SAME', 'OPP', 'LAST', 'OPP_LAST']
STATES = list(itertools.product([1, 2, 3], [0, 1, 2])) # 9 states

def evaluate(l1, l2, l3):
    total_wins = 0
    total_losses = 0
    max_streak = 0
    streak_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    
    for name, seq in all_eval:
        if len(seq) < 4: continue
        loss_streak = 0
        for i in range(3, len(seq)):
            hist = seq[:i]
            act = seq[i]['size']
            sizes = [x['size'] for x in hist]
            
            # Runs
            runs = []
            curr = sizes[0]; l = 1
            for s in sizes[1:]:
                if s == curr: l += 1
                else: runs.append((curr, l)); curr = s; l = 1
            runs.append((curr, l))
            
            cSide, cLen = runs[-1]
            lastS = sizes[-1]
            
            alt = 0
            for r in reversed(runs):
                if r[1] == 1: alt += 1
                else: break
                
            c_cat = min(cLen, 3)
            a_cat = min(alt, 2)
            st = (c_cat, a_cat)
            
            if loss_streak == 0: rule = l1[st]
            elif loss_streak == 1: rule = l2[st]
            else: rule = l3[st]
            
            if rule == 'SAME': pred = cSide
            elif rule == 'OPP': pred = 'SMALL' if cSide == 'BIG' else 'BIG'
            elif rule == 'LAST': pred = lastS
            elif rule == 'OPP_LAST': pred = 'SMALL' if lastS == 'BIG' else 'BIG'
            else: pred = cSide
            
            if pred == act:
                total_wins += 1
                loss_streak = 0
            else:
                total_losses += 1
                loss_streak += 1
                streak_counts[min(loss_streak, 5)] = streak_counts.get(min(loss_streak, 5), 0) + 1
                if loss_streak > max_streak: max_streak = loss_streak
                
    fitness = total_wins * 10 - (streak_counts.get(3, 0) * 500) - (streak_counts.get(4, 0) * 2000) - (streak_counts.get(5, 0) * 10000) - (max_streak * 100)
    return fitness, total_wins, total_losses, max_streak, streak_counts

# Smart baseline
l1_base = {
    (3, 0): 'SAME', (3, 1): 'SAME', (3, 2): 'SAME',
    (2, 0): 'OPP',  (2, 1): 'OPP',  (2, 2): 'OPP',
    (1, 0): 'SAME', (1, 1): 'OPP_LAST', (1, 2): 'OPP_LAST'
}
l2_base = {
    (3, 0): 'SAME', (3, 1): 'SAME', (3, 2): 'SAME',
    (2, 0): 'SAME', (2, 1): 'OPP',  (2, 2): 'OPP_LAST',
    (1, 0): 'OPP',  (1, 1): 'LAST', (1, 2): 'OPP_LAST'
}
l3_base = {
    (3, 0): 'SAME', (3, 1): 'SAME', (3, 2): 'SAME',
    (2, 0): 'SAME', (2, 1): 'SAME', (2, 2): 'OPP_LAST',
    (1, 0): 'SAME', (1, 1): 'OPP_LAST', (1, 2): 'OPP_LAST'
}

best_l1, best_l2, best_l3 = l1_base.copy(), l2_base.copy(), l3_base.copy()
best_fit, best_w, best_l, best_m, best_sc = evaluate(best_l1, best_l2, best_l3)
print(f'Starting baseline: Wins={best_w}, Losses={best_l}, MaxStreak={best_m}, Counts={best_sc}')

# Fast Simulated Annealing / Evolutionary Optimization
for gen in range(15000):
    c1, c2, c3 = best_l1.copy(), best_l2.copy(), best_l3.copy()
    target = random.choice([1, 2, 3])
    st = random.choice(STATES)
    act = random.choice(ACTIONS)
    if target == 1: c1[st] = act
    elif target == 2: c2[st] = act
    else: c3[st] = act
    
    fit, w, l, m, sc = evaluate(c1, c2, c3)
    if fit > best_fit or (m < best_m):
        best_fit = fit
        best_l1, best_l2, best_l3 = c1, c2, c3
        best_w, best_l, best_m, best_sc = w, l, m, sc
        if gen % 500 == 0 or m <= 2:
            print(f'Gen {gen}: Wins={w}, Losses={l}, MaxStreak={m}, Fit={fit}, StreakCounts={sc}')
        if m <= 2:
            print('>>> PERFECT ZERO-BUST (< 3 LOSSES) SOLUTION FOUND! <<<')
            break

print(f'\nFinal: Wins={best_w}, Losses={best_l}, WinRate={best_w/(best_w+best_l)*100:.1f}%, MaxStreak={best_m}')
print('L1 Rules:', best_l1)
print('L2 Rules:', best_l2)
print('L3 Rules:', best_l3)
