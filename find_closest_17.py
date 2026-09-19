from dataset_17 import all_17_seqs, get_runs, opp
import itertools

def evaluate(pred_fn):
    total_max = 0
    total_wins = 0
    total_losses = 0
    results = []
    
    for name, seq in all_17_seqs:
        history = seq[:3]
        streak = 0
        max_streak = 0
        wins, losses = 0, 0
        details = []
        
        for item in seq[3:]:
            pred, tag = pred_fn(history, streak)
            act = item['size']
            if pred == act:
                wins += 1
                details.append((item['period'], pred, act, item['number'], 'WIN', streak + 1, tag))
                streak = 0
            else:
                losses += 1
                streak += 1
                if streak > max_streak:
                    max_streak = streak
                details.append((item['period'], pred, act, item['number'], 'LOSS', streak, tag))
            history.append(item)
            
        if max_streak > total_max:
            total_max = max_streak
        total_wins += wins
        total_losses += losses
        results.append((name, wins, losses, max_streak, details))
        
    return total_max, total_wins, total_losses, results

# Let's inspect the best combinations found by max_streak and total wins
models = []

l1_drag4 = ['RIDE', 'CUT']
l1_drag3 = ['CUT', 'RIDE']
l1_trip  = ['CUT', 'RIDE']
l1_drag2 = ['MOM', 'CUT']
l1_chop3 = ['OSC', 'BREAK']
l1_chop2 = ['OSC', 'STAB']

l2_drag4 = ['RIDE', 'CUT']
l2_drag3 = ['RIDE', 'CUT']
l2_drag2 = ['RIDE', 'CUT']
l2_chop3 = ['FLIP', 'RIDE']
l2_chop2 = ['STAB', 'OSC']
l2_len1  = ['RIDE', 'CUT']

l3_drag4 = ['RIDE', 'CUT']
l3_drag3 = ['RIDE', 'CUT']
l3_drag2 = ['RIDE', 'CUT']
l3_chop3 = ['OSC', 'BREAK']
l3_chop2 = ['OSC', 'STAB']
l3_len1  = ['RIDE', 'CUT']

import random
random.seed(42)

for trial in range(30000):
    p = (
        random.choice(l1_drag4), random.choice(l1_drag3), random.choice(l1_trip),
        random.choice(l1_drag2), random.choice(l1_chop3), random.choice(l1_chop2),
        random.choice(l2_drag4), random.choice(l2_drag3), random.choice(l2_drag2),
        random.choice(l2_chop3), random.choice(l2_chop2), random.choice(l2_len1),
        random.choice(l3_drag4), random.choice(l3_drag3), random.choice(l3_drag2),
        random.choice(l3_chop3), random.choice(l3_chop2), random.choice(l3_len1)
    )

    def make_fn(params):
        (
            l1_d4, l1_d3, l1_tr, l1_d2, l1_c3, l1_c2,
            l2_d4, l2_d3, l2_d2, l2_c3, l2_c2, l2_l1,
            l3_d4, l3_d3, l3_d2, l3_c3, l3_c2, l3_l1
        ) = params

        def pred_fn(hist, streak):
            sizes = [x['size'] for x in hist]
            runs = get_runs(sizes)
            c_side, c_len = runs[-1]
            p_side, p_len = runs[-2] if len(runs) >= 2 else (opp(c_side), 0)
            p3_side, p3_len = runs[-3] if len(runs) >= 3 else (c_side, 0)
            last_s = sizes[-1]

            alt = 0
            for r_s, r_l in reversed(runs):
                if r_l == 1: alt += 1
                else: break

            if streak >= 2: # L3
                if c_len >= 4:
                    return (c_side if l3_d4 == 'RIDE' else opp(c_side)), "L3_D4"
                elif c_len == 3:
                    return (c_side if l3_d3 == 'RIDE' else opp(c_side)), "L3_D3"
                elif c_len == 2:
                    return (c_side if l3_d2 == 'RIDE' else opp(c_side)), "L3_D2"
                elif alt >= 3:
                    return (opp(last_s) if l3_c3 == 'OSC' else c_side), "L3_C3"
                elif alt >= 2:
                    return (opp(last_s) if l3_c2 == 'OSC' else last_s), "L3_C2"
                elif c_len == 1:
                    return (c_side if l3_l1 == 'RIDE' else opp(c_side)), "L3_L1"
                return c_side, "L3_MOM"

            elif streak == 1: # L2
                if c_len >= 4:
                    return (c_side if l2_d4 == 'RIDE' else opp(c_side)), "L2_D4"
                elif c_len == 3:
                    return (c_side if l2_d3 == 'RIDE' else opp(c_side)), "L2_D3"
                elif c_len == 2:
                    return (c_side if l2_d2 == 'RIDE' else opp(c_side)), "L2_D2"
                elif alt >= 3:
                    return (opp(last_s) if l2_c3 == 'FLIP' else last_s), "L2_C3"
                elif alt >= 2:
                    return (last_s if l2_c2 == 'STAB' else opp(last_s)), "L2_C2"
                elif c_len == 1:
                    return (c_side if l2_l1 == 'RIDE' else opp(c_side)), "L2_L1"
                return c_side, "L2_MOM"

            else: # L1
                if c_len == 3 and p_len == 1 and p3_len == 3:
                    return (opp(c_side) if l1_tr == 'CUT' else c_side), "L1_TRIP"
                elif c_len >= 4:
                    return (c_side if l1_d4 == 'RIDE' else opp(c_side)), "L1_D4"
                elif c_len == 3:
                    return (opp(c_side) if l1_d3 == 'CUT' else c_side), "L1_D3"
                elif c_len == 2:
                    return (opp(c_side) if l1_d2 == 'CUT' else c_side), "L1_D2"
                elif alt >= 3:
                    return (opp(last_s) if l1_c3 == 'OSC' else c_side), "L1_C3"
                elif alt >= 2:
                    return (opp(last_s) if l1_c2 == 'OSC' else last_s), "L1_C2"
                return c_side, "L1_MOM"

        return pred_fn

    fn = make_fn(p)
    max_s, tw, tl, bk = evaluate(fn)
    models.append((max_s, tw, tl, p, bk))

models.sort(key=lambda x: (x[0], -x[1]))
best_m, best_w, best_l, best_p, best_bk = models[0]

print("\n" + "="*80)
print(f"CLOSEST ENGINE: {best_w}W / {best_l}L ({(best_w/(best_w+best_l))*100:.1f}%) | Max Consecutive Losses = {best_m}")
labels = [
    'l1_drag4', 'l1_drag3', 'l1_trip', 'l1_drag2', 'l1_chop3', 'l1_chop2',
    'l2_drag4', 'l2_drag3', 'l2_drag2', 'l2_chop3', 'l2_chop2', 'l2_len1',
    'l3_drag4', 'l3_drag3', 'l3_drag2', 'l3_chop3', 'l3_chop2', 'l3_len1'
]
for k, v in zip(labels, best_p):
    print(f"  {k}: {v}")
print("\nSequence Breakdown:")
for name, w, l, ms, det in best_bk:
    print(f"  {name:<38}: {w}W/{l}L | Max Streak: {ms} | {'✅ PASS' if ms <= 2 else '❌ FAIL'}")
