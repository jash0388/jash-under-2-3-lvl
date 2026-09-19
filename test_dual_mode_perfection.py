from dataset_17 import all_17_seqs, get_runs, opp
import itertools

seqs_30s = [s for s in all_17_seqs if '30S' in s[0]]
seqs_1m = [s for s in all_17_seqs if '1M' in s[0]]

print(f"30S sequences: {len(seqs_30s)} sequences ({sum(len(s[1]) for s in seqs_30s)} draws)")
print(f"1M sequences: {len(seqs_1m)} sequences ({sum(len(s[1]) for s in seqs_1m)} draws)")

# =========================================================================
# 1. SOLVE 30S MODE FIRST
# =========================================================================
def evaluate_30s(pred_fn):
    total_max = 0
    total_wins = 0
    total_losses = 0
    results = []
    for name, seq in seqs_30s:
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
                streak = 0
                details.append((item['period'], pred, act, item['number'], 'WIN', streak + 1, tag))
            else:
                losses += 1
                streak += 1
                if streak > max_streak: max_streak = streak
                details.append((item['period'], pred, act, item['number'], 'LOSS', streak, tag))
            history.append(item)
        if max_streak > total_max: total_max = max_streak
        total_wins += wins
        total_losses += losses
        results.append((name, wins, losses, max_streak, details))
    return total_max, total_wins, total_losses, results

l1_d4 = ['RIDE', 'CUT']
l1_d3 = ['CUT', 'RIDE']
l1_d2 = ['CUT', 'RIDE', 'MOM']
l1_c3 = ['OSC', 'BREAK']
l1_c2 = ['OSC', 'STAB']
l1_l1 = ['RIDE', 'CUT']

l2_d4 = ['RIDE', 'CUT']
l2_d3 = ['RIDE', 'CUT']
l2_d2 = ['CUT', 'RIDE']
l2_c3 = ['FLIP', 'RIDE']
l2_c2 = ['STAB', 'OSC']
l2_l1 = ['RIDE', 'CUT']

l3_d4 = ['RIDE', 'CUT']
l3_d3 = ['CUT', 'RIDE']
l3_d2 = ['CUT', 'RIDE']
l3_c3 = ['OSC', 'BREAK']
l3_c2 = ['OSC', 'STAB']
l3_l1 = ['RIDE', 'CUT']

best_30s = []

for p in itertools.product(
    l1_d4, l1_d3, l1_d2, l1_c3, l1_c2, l1_l1,
    l2_d4, l2_d3, l2_d2, l2_c3, l2_c2, l2_l1,
    l3_d4, l3_d3, l3_d2, l3_c3, l3_c2, l3_l1
):
    (
        g1_d4, g1_d3, g1_d2, g1_c3, g1_c2, g1_l1,
        g2_d4, g2_d3, g2_d2, g2_c3, g2_c2, g2_l1,
        g3_d4, g3_d3, g3_d2, g3_c3, g3_c2, g3_l1
    ) = p

    def make_fn_30s(params):
        (
            p1_d4, p1_d3, p1_d2, p1_c3, p1_c2, p1_l1,
            p2_d4, p2_d3, p2_d2, p2_c3, p2_c2, p2_l1,
            p3_d4, p3_d3, p3_d2, p3_c3, p3_c2, p3_l1
        ) = params

        def pred_30s(hist, streak):
            sizes = [x['size'] for x in hist]
            runs = get_runs(sizes)
            c_side, c_len = runs[-1]
            last_s = sizes[-1]

            alt = 0
            for r_s, r_l in reversed(runs):
                if r_l == 1: alt += 1
                else: break

            if streak >= 2: # L3
                if c_len >= 4: return (c_side if p3_d4 == 'RIDE' else opp(c_side)), "L3_D4"
                elif c_len == 3: return (opp(c_side) if p3_d3 == 'CUT' else c_side), "L3_D3"
                elif c_len == 2: return (opp(c_side) if p3_d2 == 'CUT' else c_side), "L3_D2"
                elif alt >= 3: return (opp(last_s) if p3_c3 == 'OSC' else c_side), "L3_C3"
                elif alt >= 2: return (opp(last_s) if p3_c2 == 'OSC' else last_s), "L3_C2"
                elif c_len == 1: return (c_side if p3_l1 == 'RIDE' else opp(c_side)), "L3_L1"
                return c_side, "L3_MOM"

            elif streak == 1: # L2
                if c_len >= 4: return (c_side if p2_d4 == 'RIDE' else opp(c_side)), "L2_D4"
                elif c_len == 3: return (c_side if p2_d3 == 'RIDE' else opp(c_side)), "L2_D3"
                elif c_len == 2: return (opp(c_side) if p2_d2 == 'CUT' else c_side), "L2_D2"
                elif alt >= 3: return (opp(last_s) if p2_c3 == 'FLIP' else last_s), "L2_C3"
                elif alt >= 2: return (last_s if p2_c2 == 'STAB' else opp(last_s)), "L2_C2"
                elif c_len == 1: return (c_side if p2_l1 == 'RIDE' else opp(c_side)), "L2_L1"
                return c_side, "L2_MOM"

            else: # L1
                if c_len >= 4: return (c_side if p1_d4 == 'RIDE' else opp(c_side)), "L1_D4"
                elif c_len == 3: return (opp(c_side) if p1_d3 == 'CUT' else c_side), "L1_D3"
                elif c_len == 2:
                    if p1_d2 == 'CUT': return opp(c_side), "L1_D2_CUT"
                    elif p1_d2 == 'RIDE': return c_side, "L1_D2_RIDE"
                    return c_side, "L1_D2_MOM"
                elif alt >= 3: return (opp(last_s) if p1_c3 == 'OSC' else c_side), "L1_C3"
                elif alt >= 2: return (opp(last_s) if p1_c2 == 'OSC' else last_s), "L1_C2"
                elif c_len == 1: return (c_side if p1_l1 == 'RIDE' else opp(c_side)), "L1_L1"
                return c_side, "L1_MOM"

        return pred_30s

    fn = make_fn_30s(p)
    tm, tw, tl, bk = evaluate_30s(fn)
    if tm <= 2:
        best_30s.append((tw, tl, tm, p, bk))

print(f"\n30S MODE: Found {len(best_30s)} engines with MAX LOSS <= 2 across ALL 30S sequences!")
if best_30s:
    best_30s.sort(key=lambda x: x[0], reverse=True)
    tw, tl, tm, bp, bk = best_30s[0]
    print(f"🏆 BEST 30S ENGINE: {tw}W / {tl}L ({(tw/(tw+tl))*100:.1f}%) | Max Streak = {tm}")
    labels = [
        'l1_d4', 'l1_d3', 'l1_d2', 'l1_c3', 'l1_c2', 'l1_l1',
        'l2_d4', 'l2_d3', 'l2_d2', 'l2_c3', 'l2_c2', 'l2_l1',
        'l3_d4', 'l3_d3', 'l3_d2', 'l3_c3', 'l3_c2', 'l3_l1'
    ]
    for k, v in zip(labels, bp):
        print(f"  {k}: '{v}',")
    print("\n30S Breakdown:")
    for name, w, l, ms, det in bk:
        print(f"  {name:<38}: {w}W/{l}L | Max Streak: {ms} | {'✅ PASS' if ms <= 2 else '❌ FAIL'}")

# =========================================================================
# 2. SOLVE 1M MODE
# =========================================================================
def evaluate_1m(pred_fn):
    total_max = 0
    total_wins = 0
    total_losses = 0
    results = []
    for name, seq in seqs_1m:
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
                streak = 0
                details.append((item['period'], pred, act, item['number'], 'WIN', streak + 1, tag))
            else:
                losses += 1
                streak += 1
                if streak > max_streak: max_streak = streak
                details.append((item['period'], pred, act, item['number'], 'LOSS', streak, tag))
            history.append(item)
        if max_streak > total_max: total_max = max_streak
        total_wins += wins
        total_losses += losses
        results.append((name, wins, losses, max_streak, details))
    return total_max, total_wins, total_losses, results

l1_tr = ['CUT', 'RIDE']
best_1m = []

for p in itertools.product(
    l1_d4, l1_d3, l1_tr, l1_d2, l1_c3, l1_c2, l1_l1,
    l2_d4, l2_d3, l2_d2, l2_c3, l2_c2, l2_l1,
    l3_d4, l3_d3, l3_d2, l3_c3, l3_c2, l3_l1
):
    (
        g1_d4, g1_d3, g1_tr, g1_d2, g1_c3, g1_c2, g1_l1,
        g2_d4, g2_d3, g2_d2, g2_c3, g2_c2, g2_l1,
        g3_d4, g3_d3, g3_d2, g3_c3, g3_c2, g3_l1
    ) = p

    def make_fn_1m(params):
        (
            p1_d4, p1_d3, p1_tr, p1_d2, p1_c3, p1_c2, p1_l1,
            p2_d4, p2_d3, p2_d2, p2_c3, p2_c2, p2_l1,
            p3_d4, p3_d3, p3_d2, p3_c3, p3_c2, p3_l1
        ) = params

        def pred_1m(hist, streak):
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
                if c_len >= 4: return (c_side if p3_d4 == 'RIDE' else opp(c_side)), "L3_D4"
                elif c_len == 3: return (opp(c_side) if p3_d3 == 'CUT' else c_side), "L3_D3"
                elif c_len == 2: return (opp(c_side) if p3_d2 == 'CUT' else c_side), "L3_D2"
                elif alt >= 3: return (opp(last_s) if p3_c3 == 'OSC' else c_side), "L3_C3"
                elif alt >= 2: return (opp(last_s) if p3_c2 == 'OSC' else last_s), "L3_C2"
                elif c_len == 1: return (c_side if p3_l1 == 'RIDE' else opp(c_side)), "L3_L1"
                return c_side, "L3_MOM"

            elif streak == 1: # L2
                if c_len >= 4: return (c_side if p2_d4 == 'RIDE' else opp(c_side)), "L2_D4"
                elif c_len == 3: return (c_side if p2_d3 == 'RIDE' else opp(c_side)), "L2_D3"
                elif c_len == 2: return (opp(c_side) if p2_d2 == 'CUT' else c_side), "L2_D2"
                elif alt >= 3: return (opp(last_s) if p2_c3 == 'FLIP' else last_s), "L2_C3"
                elif alt >= 2: return (last_s if p2_c2 == 'STAB' else opp(last_s)), "L2_C2"
                elif c_len == 1: return (c_side if p2_l1 == 'RIDE' else opp(c_side)), "L2_L1"
                return c_side, "L2_MOM"

            else: # L1
                if c_len == 3 and p_len == 1 and p3_len == 3:
                    return (opp(c_side) if p1_tr == 'CUT' else c_side), "L1_TRIP"
                elif c_len >= 4: return (c_side if p1_d4 == 'RIDE' else opp(c_side)), "L1_D4"
                elif c_len == 3: return (opp(c_side) if p1_d3 == 'CUT' else c_side), "L1_D3"
                elif c_len == 2:
                    if p1_d2 == 'CUT': return opp(c_side), "L1_D2_CUT"
                    elif p1_d2 == 'RIDE': return c_side, "L1_D2_RIDE"
                    return c_side, "L1_D2_MOM"
                elif alt >= 3: return (opp(last_s) if p1_c3 == 'OSC' else c_side), "L1_C3"
                elif alt >= 2: return (opp(last_s) if p1_c2 == 'OSC' else last_s), "L1_C2"
                elif c_len == 1: return (c_side if p1_l1 == 'RIDE' else opp(c_side)), "L1_L1"
                return c_side, "L1_MOM"

        return pred_1m

    fn = make_fn_1m(p)
    tm, tw, tl, bk = evaluate_1m(fn)
    if tm <= 2:
        best_1m.append((tw, tl, tm, p, bk))
        if len(best_1m) >= 5:
            break

print(f"\n1M MODE: Found {len(best_1m)} engines with MAX LOSS <= 2 across ALL 1M sequences!")
if best_1m:
    best_1m.sort(key=lambda x: x[0], reverse=True)
    tw, tl, tm, bp, bk = best_1m[0]
    print(f"🏆 BEST 1M ENGINE: {tw}W / {tl}L ({(tw/(tw+tl))*100:.1f}%) | Max Streak = {tm}")
    labels = [
        'l1_d4', 'l1_d3', 'l1_tr', 'l1_d2', 'l1_c3', 'l1_c2', 'l1_l1',
        'l2_d4', 'l2_d3', 'l2_d2', 'l2_c3', 'l2_c2', 'l2_l1',
        'l3_d4', 'l3_d3', 'l3_d2', 'l3_c3', 'l3_c2', 'l3_l1'
    ]
    for k, v in zip(labels, bp):
        print(f"  {k}: '{v}',")
    print("\n1M Breakdown:")
    for name, w, l, ms, det in bk:
        print(f"  {name:<38}: {w}W/{l}L | Max Streak: {ms} | {'✅ PASS' if ms <= 2 else '❌ FAIL'}")
