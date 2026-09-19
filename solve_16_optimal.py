from dataset_real_all import all_real_sequences, get_runs, opp
import itertools

def evaluate(pred_fn):
    total_max = 0
    total_wins = 0
    total_losses = 0
    results = []
    
    for name, seq in all_real_sequences:
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

# Let's search parameter space for L1, L2, L3
l1_d3_opts = ['CUT', 'RIDE']
l1_d4_opts = ['RIDE', 'CUT']
l1_d2_opts = ['CUT', 'RIDE']
l1_c2_opts = ['OSC', 'STAB']
l1_c3_opts = ['OSC', 'BREAK']

l2_d3_opts = ['RIDE', 'CUT']
l2_d4_opts = ['RIDE', 'CUT']
l2_d2_opts = ['CUT', 'RIDE']
l2_c2_opts = ['STAB', 'OSC']
l2_c3_opts = ['FLIP', 'RIDE']
l2_d1_opts = ['RIDE', 'CUT']

l3_d3_opts = ['RIDE', 'CUT']
l3_d4_opts = ['RIDE', 'CUT']
l3_d2_opts = ['RIDE', 'CUT']
l3_c2_opts = ['OSC', 'STAB']
l3_c3_opts = ['BREAK', 'OSC']
l3_d1_opts = ['RIDE', 'CUT']

winning = []
count = 0

for p in itertools.product(
    l1_d3_opts, l1_d4_opts, l1_d2_opts, l1_c2_opts, l1_c3_opts,
    l2_d3_opts, l2_d4_opts, l2_d2_opts, l2_c2_opts, l2_c3_opts, l2_d1_opts,
    l3_d3_opts, l3_d4_opts, l3_d2_opts, l3_c2_opts, l3_c3_opts, l3_d1_opts
):
    count += 1
    (l1_d3, l1_d4, l1_d2, l1_c2, l1_c3,
     l2_d3, l2_d4, l2_d2, l2_c2, l2_c3, l2_d1,
     l3_d3, l3_d4, l3_d2, l3_c2, l3_c3, l3_d1) = p

    def make_fn(p_tuple):
        (l1_d3, l1_d4, l1_d2, l1_c2, l1_c3,
         l2_d3, l2_d4, l2_d2, l2_c2, l2_c3, l2_d1,
         l3_d3, l3_d4, l3_d2, l3_c2, l3_c3, l3_d1) = p_tuple

        def pred_fn(hist, streak):
            sizes = [x['size'] for x in hist]
            runs = get_runs(sizes)
            c_side, c_len = runs[-1]
            last_s = sizes[-1]

            alt = 0
            for r_s, r_l in reversed(runs):
                if r_l == 1: alt += 1
                else: break

            if streak >= 2: # L3
                if c_len >= 4:
                    return (c_side if l3_d4 == 'RIDE' else opp(c_side)), "L3_D4"
                elif c_len == 3:
                    return (opp(c_side) if l3_d3 == 'CUT' else c_side), "L3_D3"
                elif c_len == 2:
                    return (c_side if l3_d2 == 'RIDE' else opp(c_side)), "L3_D2"
                elif alt >= 3:
                    return (c_side if l3_c3 == 'BREAK' else opp(last_s)), "L3_C3"
                elif alt >= 2:
                    return (opp(last_s) if l3_c2 == 'OSC' else last_s), "L3_C2"
                elif c_len == 1:
                    return (c_side if l3_d1 == 'RIDE' else opp(c_side)), "L3_D1"
                return c_side, "L3_MOM"

            elif streak == 1: # L2
                if c_len >= 4:
                    return (c_side if l2_d4 == 'RIDE' else opp(c_side)), "L2_D4"
                elif c_len == 3:
                    return (c_side if l2_d3 == 'RIDE' else opp(c_side)), "L2_D3"
                elif c_len == 2:
                    return (opp(c_side) if l2_d2 == 'CUT' else c_side), "L2_D2"
                elif alt >= 3:
                    return (opp(last_s) if l2_c3 == 'FLIP' else last_s), "L2_C3"
                elif alt >= 2:
                    return (last_s if l2_c2 == 'STAB' else opp(last_s)), "L2_C2"
                elif c_len == 1:
                    return (c_side if l2_d1 == 'RIDE' else opp(c_side)), "L2_D1"
                return c_side, "L2_MOM"

            else: # L1
                if c_len >= 4:
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
    if max_s <= 2:
        winning.append((tw, tl, max_s, p, bk))

print(f"Searched {count} combinations. Total winning with max_streak <= 2 on ALL 16 sequences: {len(winning)}")
if winning:
    winning.sort(key=lambda x: x[0], reverse=True)
    best_w, best_l, best_m, best_p, best_bk = winning[0]
    print(f"\nTOP WINNING ENGINE: {best_w}W / {best_l}L ({(best_w/(best_w+best_l))*100:.1f}%) | Max Streak = {best_m}")
    labels = [
        'l1_d3', 'l1_d4', 'l1_d2', 'l1_c2', 'l1_c3',
        'l2_d3', 'l2_d4', 'l2_d2', 'l2_c2', 'l2_c3', 'l2_d1',
        'l3_d3', 'l3_d4', 'l3_d2', 'l3_c2', 'l3_c3', 'l3_d1'
    ]
    for k, v in zip(labels, best_p):
        print(f"  {k}: {v}")
    print("\nSequence Breakdown:")
    for name, w, l, ms, det in best_bk:
        print(f"  {name:<35}: {w}W/{l}L | Max Streak: {ms}")
