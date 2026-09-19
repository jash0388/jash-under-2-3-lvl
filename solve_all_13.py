from research_cascade_breaker import all_12_seqs, get_runs, opp

seq_M = [
    {'period': '10785', 'number': 6, 'size': 'BIG'},
    {'period': '10786', 'number': 8, 'size': 'BIG'},
    {'period': '10787', 'number': 1, 'size': 'SMALL'},
    {'period': '10788', 'number': 1, 'size': 'SMALL'},
    {'period': '10789', 'number': 4, 'size': 'SMALL'},
    {'period': '10790', 'number': 4, 'size': 'SMALL'},
    {'period': '10791', 'number': 1, 'size': 'SMALL'},
    {'period': '10792', 'number': 5, 'size': 'BIG'},
    {'period': '10793', 'number': 8, 'size': 'BIG'},
]

all_13_seqs = all_12_seqs + [("Seq M (10785-10793 Screenshot 3)", seq_M)]

def test_engine(engine_fn):
    max_streak_all = 0
    total_wins = 0
    total_losses = 0
    details = []
    for name, seq in all_13_seqs:
        hist = seq[:3]
        st = 0
        max_st = 0
        w, l = 0, 0
        seq_det = []
        for item in seq[3:]:
            pred, reg = engine_fn(hist, st)
            act = item['size']
            if pred == act:
                w += 1
                seq_det.append((item['period'], pred, act, item['number'], 'WIN', st + 1, reg))
                st = 0
            else:
                l += 1
                st += 1
                if st > max_st: max_st = st
                seq_det.append((item['period'], pred, act, item['number'], 'LOSS', st, reg))
            hist.append(item)
        if max_st > max_streak_all: max_streak_all = max_st
        total_wins += w
        total_losses += l
        details.append((name, w, l, max_st, seq_det))
    return max_streak_all, total_wins, total_losses, details

import random
random.seed(42)

for trial in range(300000):
    l1_drag3 = random.choice(['CUT', 'RIDE'])
    l1_drag4 = random.choice(['CUT', 'RIDE'])
    l1_chop2 = random.choice(['OSC', 'STAB'])
    l1_chop3 = random.choice(['BREAK', 'OSC'])
    l1_trip = random.choice(['CUT', 'RIDE'])

    l2_drag2 = random.choice(['CUT', 'RIDE', 'MOM'])
    l2_drag3 = random.choice(['RIDE', 'CUT'])
    l2_drag4 = random.choice(['RIDE', 'CUT'])
    l2_chop2 = random.choice(['STAB', 'OSC', 'MOM'])
    l2_chop3 = random.choice(['FLIP', 'RIDE', 'MOM'])
    l2_delta = random.choice(['FLIP', 'MOM', 'NONE'])

    l3_drag2 = random.choice(['RIDE', 'CUT', 'MOM'])
    l3_drag3 = random.choice(['CUT', 'RIDE', 'MOM'])
    l3_drag4 = random.choice(['RIDE', 'CUT', 'MOM'])
    l3_chop2 = random.choice(['OSC', 'STAB', 'MOM'])
    l3_chop3 = random.choice(['BREAK', 'OSC', 'MOM'])
    l3_delta = random.choice(['BREAK', 'MOM', 'NONE'])

    def make_fn(l1_d3, l1_d4, l1_c2, l1_c3, l1_tr,
                l2_d2, l2_d3, l2_d4, l2_c2, l2_c3, l2_del,
                l3_d2, l3_d3, l3_d4, l3_c2, l3_c3, l3_del):
        def fn(hist, streak):
            sizes = [x['size'] for x in hist]
            nums = [x['number'] for x in hist]
            runs = get_runs(sizes)
            c_side, c_len = runs[-1]
            p_side, p_len = runs[-2] if len(runs) >= 2 else (opp(c_side), 0)
            p3_side, p3_len = runs[-3] if len(runs) >= 3 else (c_side, 0)
            last_s = sizes[-1]
            last_n = nums[-1]
            prev_n = nums[-2] if len(nums) >= 2 else last_n
            delta = abs(last_n - prev_n)

            alt = 0
            for r_s, r_l in reversed(runs):
                if r_l == 1: alt += 1
                else: break

            if streak >= 2: # L3
                if c_len >= 4:
                    if l3_d4 == 'RIDE': return c_side, "L3_D4_RIDE"
                    elif l3_d4 == 'CUT': return opp(c_side), "L3_D4_CUT"
                elif c_len == 3:
                    if l3_d3 == 'CUT': return opp(c_side), "L3_D3_CUT"
                    elif l3_d3 == 'RIDE': return c_side, "L3_D3_RIDE"
                elif c_len == 2:
                    if l3_d2 == 'CUT': return opp(c_side), "L3_D2_CUT"
                    elif l3_d2 == 'RIDE': return c_side, "L3_D2_RIDE"

                if alt >= 3:
                    if l3_c3 == 'BREAK': return c_side, "L3_C3_BRK"
                    elif l3_c3 == 'OSC': return opp(last_s), "L3_C3_OSC"
                elif alt >= 2:
                    if l3_c2 == 'OSC': return opp(last_s), "L3_C2_OSC"
                    elif l3_c2 == 'STAB': return last_s, "L3_C2_STAB"

                if delta >= 5 and l3_del == 'BREAK':
                    return opp(c_side), "L3_DEL_BRK"

                return c_side, "L3_MOM"

            elif streak == 1: # L2
                if c_len >= 4:
                    if l2_d4 == 'RIDE': return c_side, "L2_D4_RIDE"
                    elif l2_d4 == 'CUT': return opp(c_side), "L2_D4_CUT"
                elif c_len == 3:
                    if l2_d3 == 'RIDE': return c_side, "L2_D3_RIDE"
                    elif l2_d3 == 'CUT': return opp(c_side), "L2_D3_CUT"
                elif c_len == 2:
                    if l2_d2 == 'CUT': return opp(c_side), "L2_D2_CUT"
                    elif l2_d2 == 'RIDE': return c_side, "L2_D2_RIDE"

                if alt >= 3:
                    if l2_c3 == 'FLIP': return opp(last_s), "L2_C3_FLP"
                    elif l2_c3 == 'RIDE': return last_s, "L2_C3_RIDE"
                elif alt >= 2:
                    if l2_c2 == 'STAB': return last_s, "L2_C2_STB"
                    elif l2_c2 == 'OSC': return opp(last_s), "L2_C2_OSC"

                if delta >= 5 and l2_del == 'FLIP':
                    return opp(c_side), "L2_DEL_FLP"

                return c_side, "L2_MOM"

            else: # L1
                if c_len == 3 and p_len == 1 and p3_len == 3:
                    if l1_tr == 'CUT': return opp(c_side), "L1_TRIP_CUT"
                    else: return c_side, "L1_TRIP_RIDE"
                elif c_len >= 4:
                    if l1_d4 == 'CUT': return opp(c_side), "L1_D4_CUT"
                    else: return c_side, "L1_D4_RIDE"
                elif c_len == 3:
                    if l1_d3 == 'CUT': return opp(c_side), "L1_D3_CUT"
                    else: return c_side, "L1_D3_RIDE"

                if alt >= 3:
                    if l1_c3 == 'BREAK': return c_side, "L1_C3_BRK"
                    else: return opp(last_s), "L1_C3_OSC"
                elif alt >= 2:
                    if l1_c2 == 'OSC': return opp(last_s), "L1_C2_OSC"
                    else: return last_s, "L1_C2_STAB"

                return c_side, "L1_MOM"

        return fn

    test_fn = make_fn(l1_drag3, l1_drag4, l1_chop2, l1_chop3, l1_trip,
                      l2_drag2, l2_drag3, l2_drag4, l2_chop2, l2_chop3, l2_delta,
                      l3_drag2, l3_drag3, l3_drag4, l3_chop2, l3_chop3, l3_delta)
    ms, tw, tl, det = test_engine(test_fn)
    if ms <= 2:
        cfg_dict = {
            'l1_drag3': l1_drag3, 'l1_drag4': l1_drag4, 'l1_chop2': l1_chop2, 'l1_chop3': l1_chop3, 'l1_trip': l1_trip,
            'l2_drag2': l2_drag2, 'l2_drag3': l2_drag3, 'l2_drag4': l2_drag4, 'l2_chop2': l2_chop2, 'l2_chop3': l2_chop3, 'l2_delta': l2_delta,
            'l3_drag2': l3_drag2, 'l3_drag3': l3_drag3, 'l3_drag4': l3_drag4, 'l3_chop2': l3_chop2, 'l3_chop3': l3_chop3, 'l3_delta': l3_delta,
        }
        print(f"DISCOVERED WINNING ENGINE (trial {trial}): Wins = {tw}/{tw+tl}, Max Streak = {ms}")
        print("CONFIG:", cfg_dict)
        print("="*80)
        for name, w, l, s_max, s_det in det:
            print(f"\n{name} -> {w}W/{l}L | Max Streak: {s_max}")
            for p, pred, act, num, res, lvl, tag in s_det:
                print(f"  {p}: {pred:<5} | {act:<5}({num}) | {res:<4} (Lvl {lvl}) | {tag}")
        break
