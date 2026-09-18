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

all_real_seqs = [
    ("Sequence A (10859-10870 1M)", seq_A),
    ("Sequence B (10954-10963 1M)", seq_B),
    ("Sequence C (11015-11027 1M)", seq_C),
    ("Sequence D (52065-52074 30S)", seq_D_30s),
    ("Sequence E (11034-11053 1M)", seq_E),
    ("Sequence F (11058-11075 1M)", seq_F),
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

def predict_apex_titan_v52(history, loss_streak):
    sizes = [h['size'] for h in history]
    if len(sizes) < 3: return "BIG", "INITIALIZING"
    runs = get_runs(sizes)
    curr_s, curr_l = runs[-1]
    last = curr_s
    prev_s, prev_l = runs[-2] if len(runs) >= 2 else (opp(curr_s), 1)

    alt = 0
    for s, l in reversed(runs):
        if l == 1: alt += 1
        else: break

    last12 = sizes[-12:]
    big_count = last12.count("BIG")
    small_count = last12.count("SMALL")
    dominant = "BIG" if big_count >= 7 else ("SMALL" if small_count >= 7 else None)

    # Multi-Order Cadence & Doublet Detection
    is_dbl_rhythm = False
    if len(runs) >= 3:
        r1, r2, r3 = runs[-3][1], runs[-2][1], runs[-1][1]
        if (r1 == 2 and r2 == 1 and r3 == 2) or (r1 == 1 and r2 == 2 and r3 == 1) or (r2 == 2 and r3 == 2) or (r1 == 2 and r2 == 2):
            is_dbl_rhythm = True

    # Triplet Cadence Detection (e.g. 3-1-3-1 or 3-2-3)
    is_triplet_rhythm = False
    past_dragons = [l for s, l in runs[:-1] if l >= 3]
    if len(past_dragons) >= 2 and past_dragons[-1] == 3 and past_dragons[-2] == 3:
        is_triplet_rhythm = True
    elif len(runs) >= 3:
        r1, r2, r3 = runs[-3][1], runs[-2][1], runs[-1][1]
        if (r1 == 3 and r2 == 1 and r3 == 3) or (r1 == 1 and r2 == 3 and r3 == 1):
            is_triplet_rhythm = True

    # --- LEVEL 3 (EMERGENCY ZERO-LOSS QUANTUM SHIELD) ---
    if loss_streak >= 2:
        if curr_l >= 3:
            if is_triplet_rhythm and curr_l == 3:
                return opp(last), f"🛑 LVL 3 TRIPLET CAP ({last} x3 -> FLIP)"
            else:
                return last, f"🛑 LVL 3 DRAGON LOCK ({last} x{curr_l})"
        elif curr_l == 2:
            if is_dbl_rhythm:
                return opp(last), f"🛑 LVL 3 DOUBLET CUT ({last} x2 -> FLIP)"
            elif prev_l >= 4:
                return last, f"🛑 LVL 3 COUNTER DRAGON ({last} x2)"
            else:
                return last, f"🛑 LVL 3 DRAGON RIDE ({last} x2)"
        elif curr_l == 1:
            if is_dbl_rhythm:
                return opp(last), f"🛑 LVL 3 DOUBLET ADVANCE ({opp(last)})"
            elif alt >= 3:
                return opp(last), f"🛑 LVL 3 CHOP FLIP (x{alt})"
            else:
                return last, f"🛑 LVL 3 MOMENTUM FOLLOW ({last})"
        else:
            return last, f"🛑 LVL 3 FLOW ({last})"

    # --- LEVEL 2 (RECOVERY) ---
    elif loss_streak == 1:
        if curr_l >= 3:
            if is_triplet_rhythm and curr_l == 3:
                return opp(last), f"🛡️ LVL 2 TRIPLET CAP ({last} x3 -> FLIP)"
            else:
                return last, f"🛡️ LVL 2 DRAGON LOCK ({last} x{curr_l})"
        elif curr_l == 2:
            if is_dbl_rhythm:
                return opp(last), f"🛡️ LVL 2 DOUBLET CUT ({last} x2)"
            elif prev_l >= 4:
                return last, f"🛡️ LVL 2 COUNTER DRAGON ({last} x2)"
            else:
                return last, f"🛡️ LVL 2 DRAGON RIDE ({last} x2)"
        elif curr_l == 1:
            if is_dbl_rhythm:
                return opp(last), f"🛡️ LVL 2 DOUBLET ADVANCE ({opp(last)})"
            elif alt >= 3:
                return opp(last), f"🛡️ LVL 2 CHOP FLIP (x{alt})"
            else:
                return last, f"🛡️ LVL 2 MOMENTUM FOLLOW ({last})"
        else:
            return last, f"🛡️ LVL 2 FOLLOW ({last})"

    # --- LEVEL 1 (NORMAL FLOW) ---
    else:
        if is_dbl_rhythm and curr_l == 2:
            return opp(last), f"⚡ DOUBLET CUT (x2)"
        elif is_dbl_rhythm and curr_l == 1:
            return opp(last), f"⚡ DOUBLET ADVANCE ({opp(last)})"
        elif is_triplet_rhythm and curr_l == 3:
            return opp(last), f"⚡ TRIPLET CAP (x3 -> FLIP)"
        elif curr_l >= 3 and curr_l <= 7:
            return last, f"🐉 DRAGON FLOW ({last} x{curr_l})"
        elif curr_l > 7:
            return opp(last), f"⚖️ FATIGUE CUT (x{curr_l})"
        elif curr_l == 2:
            return last, f"🐉 DRAGON SEED ({last} x2)"
        else:
            if alt >= 3:
                return opp(last), f"⚡ CHOP OSCILLATE (x{alt})"
            elif dominant:
                return dominant, f"🌊 DOMINANT FLOW ({dominant})"
            else:
                return last, f"🌊 FLOW MOMENTUM ({last})"

def test_strategy_on_all_seqs(pred_fn, name=""):
    print(f"\n==================== {name} ====================")
    for seq_name, seq in all_real_seqs:
        hist = []
        loss_streak = 0
        max_loss = 0
        wins, losses = 0, 0
        print(f"\n--- {seq_name} ---")
        for r in seq:
            if len(hist) < 3:
                hist.append(r)
                continue
            pred, reg = pred_fn(hist, loss_streak)
            won = (pred == r['size'])
            if won:
                wins += 1
                lvl = 1 if loss_streak == 0 else loss_streak + 1
                status = f"✅ WIN (Lvl {lvl})"
                loss_streak = 0
            else:
                losses += 1
                loss_streak += 1
                max_loss = max(max_loss, loss_streak)
                status = f"❌ LOSS (Lvl {loss_streak})"
            print(f"{r['period']}: Pred={pred:5s} | Act={r['size']:5s}({r['number']}) | {status:15s} | {reg}")
            hist.append(r)
        print(f"Result for {seq_name}: Wins={wins}, Losses={losses}, Max Consecutive Losses={max_loss}")

if __name__ == "__main__":
    test_strategy_on_all_seqs(predict_apex_titan_v52, "Apex Titan V52 Adaptive Quantum Master Engine")
