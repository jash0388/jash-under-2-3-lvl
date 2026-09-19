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

# Let's define the discrete parameter space for structural patterns:
l1_drag4 = ['RIDE', 'CUT']        # c_len >= 4
l1_drag3 = ['CUT', 'RIDE']        # c_len == 3
l1_trip  = ['CUT', 'RIDE']        # 3-1-3-1 cadence
l1_drag2 = ['MOM', 'CUT']         # c_len == 2
l1_chop3 = ['OSC', 'BREAK']       # alt >= 3
l1_chop2 = ['OSC', 'STAB']        # alt == 2

l2_drag4 = ['RIDE', 'CUT']        # c_len >= 4
l2_drag3 = ['RIDE', 'CUT']        # c_len == 3
l2_drag2 = ['RIDE', 'CUT']        # c_len == 2
l2_chop3 = ['FLIP', 'RIDE']       # alt >= 3
l2_chop2 = ['STAB', 'OSC']        # alt == 2
l2_len1  = ['RIDE', 'CUT']        # c_len == 1

l3_drag4 = ['RIDE', 'CUT']        # c_len >= 4
l3_drag3 = ['RIDE', 'CUT']        # c_len == 3
l3_drag2 = ['RIDE', 'CUT']        # c_len == 2
l3_chop3 = ['OSC', 'BREAK']       # alt >= 3
l3_chop2 = ['OSC', 'STAB']        # alt == 2
l3_len1  = ['RIDE', 'CUT']        # c_len == 1

winning = []
count = 0

for p in itertools.product(
    l1_drag4, l1_drag3, l1_trip, l1_drag2, l1_chop3, l1_chop2,
    l2_drag4, l2_drag3, l2_drag2, l2_chop3, l2_chop2, l2_len1,
    l3_drag4, l3_drag3, l3_drag2, l3_chop3, l3_chop2, l3_len1
):
    count += 1
    (
        g_l1_d4, g_l1_d3, g_l1_tr, g_l1_d2, g_l1_c3, g_l1_c2,
        g_l2_d4, g_l2_d3, g_l2_d2, g_l2_c3, g_l2_c2, g_l2_l1,
        g_l3_d4, g_l3_d3, g_l3_d2, g_l3_c3, g_l3_c2, g_l3_l1
    ) = p

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

            if streak >= 2: # L3 Zero Loss Shield
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

            elif streak == 1: # L2 Recovery
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

            else: # L1 Base
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
    if max_s <= 2:
        winning.append((tw, tl, max_s, p, bk))

print(f"Total evaluated: {count} parameter combinations.")
print(f"Winning engines with MAX CONSECUTIVE LOSSES <= 2 on ALL 17 SEQUENCES: {len(winning)}")

if winning:
    winning.sort(key=lambda x: x[0], reverse=True)
    best_w, best_l, best_m, best_p, best_bk = winning[0]
    print("\n" + "="*80)
    print(f"🏆 TOP WINNING ENGINE: {best_w}W / {best_l}L ({(best_w/(best_w+best_l))*100:.1f}%) | Max Streak = {best_m}")
    labels = [
        'l1_drag4', 'l1_drag3', 'l1_trip', 'l1_drag2', 'l1_chop3', 'l1_chop2',
        'l2_drag4', 'l2_drag3', 'l2_drag2', 'l2_chop3', 'l2_chop2', 'l2_len1',
        'l3_drag4', 'l3_drag3', 'l3_drag2', 'l3_chop3', 'l3_chop2', 'l3_len1'
    ]
    for k, v in zip(labels, best_p):
        print(f"  {k}: {v}")
    print("\nDetailed Sequence Breakdown:")
    for name, w, l, ms, det in best_bk:
        print(f"  {name:<38}: {w}W/{l}L | Max Streak: {ms} | {'✅ PASS' if ms <= 2 else '❌ FAIL'}")
