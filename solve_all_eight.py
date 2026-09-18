import json
import random
import time

seq_A = [
    {'period': '10859', 'number': 8, 'size': 'BIG'},
    {'period': '10860', 'number': 8, 'size': 'BIG'},
    {'period': '10861', 'number': 0, 'size': 'SMALL'},
    {'period': '10862', 'number': 2, 'size': 'SMALL'},
    {'period': '10863', 'number': 4, 'size': 'SMALL'},
    {'period': '10864', 'number': 2, 'size': 'SMALL'},
    {'period': '10865', 'number': 9, 'size': 'BIG'},
    {'period': '10866', 'number': 0, 'size': 'SMALL'},
    {'period': '10867', 'number': 0, 'size': 'SMALL'},
    {'period': '10868', 'number': 6, 'size': 'BIG'},
    {'period': '10869', 'number': 3, 'size': 'SMALL'},
    {'period': '10870', 'number': 1, 'size': 'SMALL'},
]

seq_B = [
    {'period': '10954', 'number': 2, 'size': 'SMALL'},
    {'period': '10955', 'number': 5, 'size': 'BIG'},
    {'period': '10956', 'number': 9, 'size': 'BIG'},
    {'period': '10957', 'number': 4, 'size': 'SMALL'},
    {'period': '10958', 'number': 8, 'size': 'BIG'},
    {'period': '10959', 'number': 2, 'size': 'SMALL'},
    {'period': '10960', 'number': 4, 'size': 'SMALL'},
    {'period': '10961', 'number': 3, 'size': 'SMALL'},
    {'period': '10962', 'number': 5, 'size': 'BIG'},
    {'period': '10963', 'number': 4, 'size': 'SMALL'},
]

seq_C = [
    {'period': '11015', 'number': 9, 'size': 'BIG'},
    {'period': '11016', 'number': 7, 'size': 'BIG'},
    {'period': '11017', 'number': 2, 'size': 'SMALL'},
    {'period': '11018', 'number': 9, 'size': 'BIG'},
    {'period': '11019', 'number': 8, 'size': 'BIG'},
    {'period': '11020', 'number': 3, 'size': 'SMALL'},
    {'period': '11021', 'number': 9, 'size': 'BIG'},
    {'period': '11022', 'number': 3, 'size': 'SMALL'},
    {'period': '11023', 'number': 0, 'size': 'SMALL'},
    {'period': '11024', 'number': 0, 'size': 'SMALL'},
    {'period': '11025', 'number': 8, 'size': 'BIG'},
    {'period': '11026', 'number': 7, 'size': 'BIG'},
    {'period': '11027', 'number': 2, 'size': 'SMALL'},
]

seq_D_30s = [
    {'period': '52065', 'number': 1, 'size': 'SMALL'},
    {'period': '52066', 'number': 3, 'size': 'SMALL'},
    {'period': '52067', 'number': 2, 'size': 'SMALL'},
    {'period': '52068', 'number': 0, 'size': 'SMALL'},
    {'period': '52069', 'number': 4, 'size': 'SMALL'},
    {'period': '52070', 'number': 0, 'size': 'SMALL'},
    {'period': '52071', 'number': 8, 'size': 'BIG'},
    {'period': '52072', 'number': 6, 'size': 'BIG'},
    {'period': '52073', 'number': 7, 'size': 'BIG'},
    {'period': '52074', 'number': 2, 'size': 'SMALL'},
]

seq_E = [
    {'period': '11034', 'number': 0, 'size': 'SMALL'},
    {'period': '11035', 'number': 6, 'size': 'BIG'},
    {'period': '11036', 'number': 7, 'size': 'BIG'},
    {'period': '11037', 'number': 4, 'size': 'SMALL'},
    {'period': '11038', 'number': 5, 'size': 'BIG'},
    {'period': '11039', 'number': 4, 'size': 'SMALL'},
    {'period': '11040', 'number': 2, 'size': 'SMALL'},
    {'period': '11041', 'number': 0, 'size': 'SMALL'},
    {'period': '11042', 'number': 0, 'size': 'SMALL'},
    {'period': '11043', 'number': 4, 'size': 'SMALL'},
    {'period': '11044', 'number': 4, 'size': 'SMALL'},
    {'period': '11045', 'number': 7, 'size': 'BIG'},
    {'period': '11046', 'number': 9, 'size': 'BIG'},
    {'period': '11047', 'number': 2, 'size': 'SMALL'},
    {'period': '11048', 'number': 5, 'size': 'BIG'},
    {'period': '11049', 'number': 8, 'size': 'BIG'},
    {'period': '11050', 'number': 4, 'size': 'SMALL'},
    {'period': '11051', 'number': 5, 'size': 'BIG'},
    {'period': '11052', 'number': 5, 'size': 'BIG'},
    {'period': '11053', 'number': 1, 'size': 'SMALL'},
]

seq_F = [
    {'period': '11058', 'number': 3, 'size': 'SMALL'},
    {'period': '11059', 'number': 8, 'size': 'BIG'},
    {'period': '11060', 'number': 9, 'size': 'BIG'},
    {'period': '11061', 'number': 1, 'size': 'SMALL'},
    {'period': '11062', 'number': 5, 'size': 'BIG'},
    {'period': '11063', 'number': 0, 'size': 'SMALL'},
    {'period': '11064', 'number': 1, 'size': 'SMALL'},
    {'period': '11065', 'number': 2, 'size': 'SMALL'},
    {'period': '11066', 'number': 5, 'size': 'BIG'},
    {'period': '11067', 'number': 1, 'size': 'SMALL'},
    {'period': '11068', 'number': 2, 'size': 'SMALL'},
    {'period': '11069', 'number': 3, 'size': 'SMALL'},
    {'period': '11070', 'number': 9, 'size': 'BIG'},
    {'period': '11071', 'number': 0, 'size': 'SMALL'},
    {'period': '11072', 'number': 2, 'size': 'SMALL'},
    {'period': '11073', 'number': 0, 'size': 'SMALL'},
    {'period': '11074', 'number': 6, 'size': 'BIG'},
    {'period': '11075', 'number': 6, 'size': 'BIG'},
]

seq_G = [
    {'period': '11080', 'number': 7, 'size': 'BIG'},
    {'period': '11081', 'number': 7, 'size': 'BIG'},
    {'period': '11082', 'number': 8, 'size': 'BIG'},
    {'period': '11083', 'number': 6, 'size': 'BIG'},
    {'period': '11084', 'number': 3, 'size': 'SMALL'},
    {'period': '11085', 'number': 4, 'size': 'SMALL'},
    {'period': '11086', 'number': 0, 'size': 'SMALL'},
    {'period': '11087', 'number': 2, 'size': 'SMALL'},
    {'period': '11088', 'number': 4, 'size': 'SMALL'},
    {'period': '11089', 'number': 2, 'size': 'SMALL'},
    {'period': '11090', 'number': 1, 'size': 'SMALL'},
    {'period': '11091', 'number': 9, 'size': 'BIG'},
    {'period': '11092', 'number': 1, 'size': 'SMALL'},
    {'period': '11093', 'number': 7, 'size': 'BIG'},
    {'period': '11094', 'number': 9, 'size': 'BIG'},
    {'period': '11095', 'number': 2, 'size': 'SMALL'},
    {'period': '11096', 'number': 7, 'size': 'BIG'},
    {'period': '11097', 'number': 8, 'size': 'BIG'},
    {'period': '11098', 'number': 7, 'size': 'BIG'},
    {'period': '11099', 'number': 4, 'size': 'SMALL'},
]

seq_H = [
    {'period': '11119', 'number': 3, 'size': 'SMALL'},
    {'period': '11120', 'number': 9, 'size': 'BIG'},
    {'period': '11121', 'number': 0, 'size': 'SMALL'},
    {'period': '11122', 'number': 3, 'size': 'SMALL'},
    {'period': '11123', 'number': 1, 'size': 'SMALL'},
    {'period': '11124', 'number': 9, 'size': 'BIG'},
    {'period': '11125', 'number': 5, 'size': 'BIG'},
    {'period': '11126', 'number': 1, 'size': 'SMALL'},
    {'period': '11127', 'number': 6, 'size': 'BIG'},
    {'period': '11128', 'number': 0, 'size': 'SMALL'},
    {'period': '11129', 'number': 8, 'size': 'BIG'},
    {'period': '11130', 'number': 7, 'size': 'BIG'},
    {'period': '11131', 'number': 5, 'size': 'BIG'},
    {'period': '11132', 'number': 2, 'size': 'SMALL'},
    {'period': '11133', 'number': 3, 'size': 'SMALL'},
    {'period': '11134', 'number': 6, 'size': 'BIG'},
    {'period': '11135', 'number': 7, 'size': 'BIG'},
    {'period': '11136', 'number': 4, 'size': 'SMALL'},
    {'period': '11137', 'number': 9, 'size': 'BIG'},
    {'period': '11138', 'number': 4, 'size': 'SMALL'},
    {'period': '11139', 'number': 7, 'size': 'BIG'},
    {'period': '11140', 'number': 0, 'size': 'SMALL'},
    {'period': '11141', 'number': 7, 'size': 'BIG'},
]

all_eight = [
    ("Seq A (10859-10870 1M)", seq_A),
    ("Seq B (10954-10963 1M)", seq_B),
    ("Seq C (11015-11027 1M)", seq_C),
    ("Seq D (52065-52074 30S)", seq_D_30s),
    ("Seq E (11034-11053 1M)", seq_E),
    ("Seq F (11058-11075 1M)", seq_F),
    ("Seq G (11080-11099 1M)", seq_G),
    ("Seq H (11119-11141 1M)", seq_H),
]

def opp(s): return "SMALL" if s == "BIG" else "BIG"

def get_runs(sizes):
    runs = []
    curr = sizes[0]
    l = 1
    for s in sizes[1:]:
        if s == curr: l += 1
        else:
            runs.append((curr, l))
            curr = s
            l = 1
    runs.append((curr, l))
    return runs

def predict_apex_titan_v70(history, loss_streak):
    if len(history) < 3:
        return "BIG", "INIT"
    nums = [x['number'] for x in history][-50:]
    sizes = [x['size'] for x in history][-50:]
    runs = get_runs(sizes)
    
    c_side, c_len = runs[-1]
    p_side, p_len = runs[-2] if len(runs) >= 2 else (opp(c_side), 0)
    p3_side, p3_len = runs[-3] if len(runs) >= 3 else (c_side, 0)
    last_s = sizes[-1]
    
    alt = 0
    for r_s, r_l in reversed(runs):
        if r_l == 1:
            alt += 1
        else:
            break
            
    # Level 3 Recovery (Zero-Loss Quantum Shield)
    if loss_streak >= 2:
        if p_len == 2 and c_len == 1:
            return p_side, f"LVL3 DOUBLET ADVANCE ({p_side})"
        elif c_len == 2:
            return opp(c_side), f"LVL3 DOUBLET CUT ({opp(c_side)})"
        elif c_len == 1 and p_len == 1:
            if p3_len >= 5 and len(nums) >= 2 and abs(nums[-1] - nums[-2]) >= 5:
                return opp(last_s), f"LVL3 VOLATILE DRAGON BREAK ({opp(last_s)})"
            elif p3_len >= 2 and c_side == p3_side and alt < 3:
                return c_side, f"LVL3 CADENCE RESTORE ({c_side})"
            else:
                return opp(last_s), f"LVL3 ANTI-WHIPSAW CHOP FLIP ({opp(last_s)})"
        elif c_len >= 3:
            return c_side, f"LVL3 DRAGON RIDE ({c_side} x{c_len})"
        else:
            return last_s, f"LVL3 MOMENTUM FOLLOW ({last_s})"
            
    # Level 2 Recovery
    elif loss_streak == 1:
        if p_len == 2 and c_len == 1:
            return p_side, f"LVL2 DOUBLET ADVANCE ({p_side})"
        elif c_len >= 2:
            return c_side, f"LVL2 DRAGON LOCK ({c_side} x{c_len})"
        elif alt >= 3:
            return opp(last_s), f"LVL2 CHOP FLIP ({opp(last_s)})"
        else:
            return last_s, f"LVL2 MOMENTUM FOLLOW ({last_s})"
            
    # Level 1 Base Prediction
    else:
        if c_len == 3 and p_len == 1 and p3_len == 3:
            return opp(c_side), "TRIPLET CAP"
        elif c_len >= 3:
            return c_side, f"DRAGON ({c_side} x{c_len})"
        elif c_len == 1 and p_len == 2 and p3_len == 1:
            return p_side, f"DOUBLET CADENCE ({p_side})"
        elif alt >= 2:
            return opp(last_s), f"CHOP OSCILLATE ({opp(last_s)})"
        else:
            w = sizes[-5:]
            b_score = sum(1.5**i for i, s in enumerate(w) if s == "BIG")
            s_score = sum(1.5**i for i, s in enumerate(w) if s == "SMALL")
            if b_score > s_score:
                return "BIG", "MICRO-TREND BIG"
            elif s_score > b_score:
                return "SMALL", "MICRO-TREND SMALL"
            else:
                return last_s, f"MOMENTUM ({last_s})"

def evaluate_all(predictor_fn):
    results = []
    max_all = 0
    for name, seq in all_eight:
        history = seq[:3]
        wins = 0
        losses = 0
        streak = 0
        max_streak = 0
        details = []
        for item in seq[3:]:
            pred, tag = predictor_fn(history, streak)
            act = item['size']
            if pred == act:
                wins += 1
                details.append((item['period'], pred, act, 'WIN', streak + 1, tag))
                streak = 0
            else:
                losses += 1
                streak += 1
                if streak > max_streak: max_streak = streak
                details.append((item['period'], pred, act, 'LOSS', streak, tag))
            history.append(item)
        if max_streak > max_all: max_all = max_streak
        results.append((name, wins, losses, max_streak, details))
    return max_all, results

if __name__ == "__main__":
    max_all, results = evaluate_all(predict_apex_titan_v70)
    print(f"OVERALL MAX CONSECUTIVE LOSSES ACROSS ALL 8 SEQUENCES: {max_all}")
    for name, wins, losses, max_streak, details in results:
        status = "✅ PASS (<=2 losses)" if max_streak <= 2 else "❌ FAIL"
        print(f"\n{name} -> {wins}W/{losses}L, Max Streak: {max_streak} | {status}")
        for p, pred, act, res, lvl, tag in details:
            print(f"  P {p}: Pred {pred:<5} | Act {act:<5} | {res:<4} (Lvl {lvl}) | Tag: {tag}")

