from dataset_real_all import all_real_sequences, get_runs, opp
import itertools

# Seq Q (30S 52480 - 52494)
seq_Q = [
    {'period': '52480', 'number': 6, 'size': 'BIG'},
    {'period': '52481', 'number': 0, 'size': 'SMALL'},
    {'period': '52482', 'number': 2, 'size': 'SMALL'},
    {'period': '52483', 'number': 1, 'size': 'SMALL'},
    {'period': '52484', 'number': 7, 'size': 'BIG'},
    {'period': '52485', 'number': 7, 'size': 'BIG'},
    {'period': '52486', 'number': 8, 'size': 'BIG'},
    {'period': '52487', 'number': 4, 'size': 'SMALL'},
    {'period': '52488', 'number': 0, 'size': 'SMALL'},
    {'period': '52489', 'number': 9, 'size': 'BIG'},
    {'period': '52490', 'number': 6, 'size': 'BIG'},
    {'period': '52491', 'number': 4, 'size': 'SMALL'},
    {'period': '52492', 'number': 6, 'size': 'BIG'},
    {'period': '52493', 'number': 7, 'size': 'BIG'},
    {'period': '52494', 'number': 2, 'size': 'SMALL'},
]

# Seq R (30S 52524 - 52537)
seq_R = [
    {'period': '52524', 'number': 7, 'size': 'BIG'},
    {'period': '52525', 'number': 0, 'size': 'SMALL'},
    {'period': '52526', 'number': 5, 'size': 'BIG'},
    {'period': '52527', 'number': 7, 'size': 'BIG'},
    {'period': '52528', 'number': 2, 'size': 'SMALL'},
    {'period': '52529', 'number': 8, 'size': 'BIG'},
    {'period': '52530', 'number': 3, 'size': 'SMALL'},
    {'period': '52531', 'number': 5, 'size': 'BIG'},
    {'period': '52532', 'number': 6, 'size': 'BIG'},
    {'period': '52533', 'number': 6, 'size': 'BIG'},
    {'period': '52534', 'number': 9, 'size': 'BIG'},
    {'period': '52535', 'number': 7, 'size': 'BIG'},
    {'period': '52536', 'number': 8, 'size': 'BIG'},
    {'period': '52537', 'number': 4, 'size': 'SMALL'},
]

# Seq S (30S 52570 - 52590 Full Live Sequence)
seq_S = [
    {'period': '52570', 'number': 1, 'size': 'SMALL'},
    {'period': '52571', 'number': 4, 'size': 'SMALL'},
    {'period': '52572', 'number': 3, 'size': 'SMALL'},
    {'period': '52573', 'number': 3, 'size': 'SMALL'},
    {'period': '52574', 'number': 7, 'size': 'BIG'},
    {'period': '52575', 'number': 0, 'size': 'SMALL'},
    {'period': '52576', 'number': 5, 'size': 'BIG'},
    {'period': '52577', 'number': 7, 'size': 'BIG'},
    {'period': '52578', 'number': 2, 'size': 'SMALL'},
    {'period': '52579', 'number': 8, 'size': 'BIG'},
    {'period': '52580', 'number': 3, 'size': 'SMALL'},
    {'period': '52581', 'number': 5, 'size': 'BIG'},
    {'period': '52582', 'number': 6, 'size': 'BIG'},
    {'period': '52583', 'number': 0, 'size': 'SMALL'},
    {'period': '52584', 'number': 8, 'size': 'BIG'},
    {'period': '52585', 'number': 1, 'size': 'SMALL'},
    {'period': '52586', 'number': 2, 'size': 'SMALL'},
    {'period': '52587', 'number': 1, 'size': 'SMALL'},
    {'period': '52588', 'number': 8, 'size': 'BIG'},
    {'period': '52589', 'number': 3, 'size': 'SMALL'},
    {'period': '52590', 'number': 7, 'size': 'BIG'},
]

all_18_seqs = all_real_sequences + [
    ("Seq Q (30S 52480 - Live)", seq_Q),
    ("Seq R (30S 52524 - Live)", seq_R),
    ("Seq S (30S 52570 - Live 52590)", seq_S),
]

seqs_30s = [s for s in all_18_seqs if '30S' in s[0]]

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

# Expanded search space
l1_d4 = ['CUT', 'RIDE']
l1_d3 = ['RIDE', 'CUT']
l1_d2 = ['RIDE', 'CUT']
l1_c3 = ['OSC', 'BREAK']
l1_c2 = ['OSC', 'STAB']
l1_l1 = ['RIDE', 'CUT']

l2_d4 = ['RIDE', 'CUT']
l2_d3 = ['RIDE', 'CUT']
l2_d2 = ['RIDE', 'CUT']
l2_c3 = ['OSC', 'FLIP']
l2_c2 = ['OSC', 'STAB']
l2_l1 = ['CUT', 'RIDE']

l3_d4 = ['RIDE', 'CUT']
l3_d3 = ['CUT', 'RIDE']
l3_d2 = ['RIDE', 'CUT']
l3_c3 = ['OSC', 'BREAK']
l3_c2 = ['OSC', 'STAB']
l3_l1 = ['CUT', 'RIDE']

best_engines = []

for p in itertools.product(
    l1_d4, l1_d3, l1_d2, l1_c3, l1_c2, l1_l1,
    l2_d4, l2_d3, l2_d2, l2_c3, l2_c2, l2_l1,
    l3_d4, l3_d3, l3_d2, l3_c3, l3_c2, l3_l1
):
    (
        p1_d4, p1_d3, p1_d2, p1_c3, p1_c2, p1_l1,
        p2_d4, p2_d3, p2_d2, p2_c3, p2_c2, p2_l1,
        p3_d4, p3_d3, p3_d2, p3_c3, p3_c2, p3_l1
    ) = p

    def make_fn(params):
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
                elif c_len == 2: return (c_side if p3_d2 == 'RIDE' else opp(c_side)), "L3_D2"
                elif alt >= 3: return (opp(last_s) if p3_c3 == 'OSC' else c_side), "L3_C3"
                elif alt >= 2: return (opp(last_s) if p3_c2 == 'OSC' else last_s), "L3_C2"
                elif c_len == 1: return (opp(c_side) if p3_l1 == 'CUT' else c_side), "L3_L1"
                return c_side, "L3_MOM"

            elif streak == 1: # L2
                if c_len >= 4: return (c_side if p2_d4 == 'RIDE' else opp(c_side)), "L2_D4"
                elif c_len == 3: return (c_side if p2_d3 == 'RIDE' else opp(c_side)), "L2_D3"
                elif c_len == 2: return (c_side if p2_d2 == 'RIDE' else opp(c_side)), "L2_D2"
                elif alt >= 3: return (opp(last_s) if p2_c3 == 'OSC' else opp(last_s)), "L2_C3"
                elif alt >= 2: return (opp(last_s) if p2_c2 == 'OSC' else last_s), "L2_C2"
                elif c_len == 1: return (opp(c_side) if p2_l1 == 'CUT' else c_side), "L2_L1"
                return c_side, "L2_MOM"

            else: # L1
                if c_len >= 4: return (c_side if p1_d4 == 'RIDE' else opp(c_side)), "L1_D4"
                elif c_len == 3: return (c_side if p1_d3 == 'RIDE' else opp(c_side)), "L1_D3"
                elif c_len == 2: return (c_side if p1_d2 == 'RIDE' else opp(c_side)), "L1_D2"
                elif alt >= 3: return (opp(last_s) if p1_c3 == 'OSC' else c_side), "L1_C3"
                elif alt >= 2: return (opp(last_s) if p1_c2 == 'OSC' else last_s), "L1_C2"
                elif c_len == 1: return (c_side if p1_l1 == 'RIDE' else opp(c_side)), "L1_L1"
                return c_side, "L1_MOM"

        return pred_30s

    fn = make_fn(p)
    tm, tw, tl, bk = evaluate_30s(fn)
    if tm <= 2:
        best_engines.append((tw, tl, tm, p, bk))

print(f"Total 30S engines found with Max Loss <= 2: {len(best_engines)}")
if best_engines:
    best_engines.sort(key=lambda x: (-x[0], x[2]))
    for i, (tw, tl, tm, bp, bk) in enumerate(best_engines[:3]):
        print(f"\n🏆 RANK #{i+1}: {tw}W / {tl}L ({(tw/(tw+tl))*100:.1f}%) | Max Streak = {tm}")
        labels = [
            'l1_d4', 'l1_d3', 'l1_d2', 'l1_c3', 'l1_c2', 'l1_l1',
            'l2_d4', 'l2_d3', 'l2_d2', 'l2_c3', 'l2_c2', 'l2_l1',
            'l3_d4', 'l3_d3', 'l3_d2', 'l3_c3', 'l3_c2', 'l3_l1'
        ]
        for k, v in zip(labels, bp):
            print(f"  {k}: '{v}',")
        print("Sequence Breakdown:")
        for name, w, l, ms, det in bk:
            print(f"  {name:<38}: {w}W/{l}L | ms={ms} | {'✅ PASS' if ms <= 2 else '❌ FAIL'}")
