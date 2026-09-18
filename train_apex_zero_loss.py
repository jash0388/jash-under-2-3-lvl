import json
import random
import time
from million_rounds_deep_research import million_data

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

all_real_seqs = [
    ("Seq A (10859-10870 1M)", seq_A),
    ("Seq B (10954-10963 1M)", seq_B),
    ("Seq C (11015-11027 1M)", seq_C),
    ("Seq D (52065-52074 30S)", seq_D_30s),
    ("Seq E (11034-11053 1M)", seq_E),
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

def eval_on_all_real(fn, verbose=False):
    max_losses = []
    total_wins = 0
    total_losses = 0
    for name, seq in all_real_seqs:
        hist = []
        loss_streak = 0
        seq_max_loss = 0
        w, l = 0, 0
        if verbose: print(f"\n--- {name} ---")
        for r in seq:
            if len(hist) < 3:
                hist.append(r)
                continue
            pred, reg = fn(hist, loss_streak)
            won = (pred == r['size'])
            if won:
                w += 1
                lvl = 1 if loss_streak == 0 else loss_streak + 1
                if verbose: print(f"{r['period']}: Pred={pred:5s} | Act={r['size']:5s}({r['number']}) | ✅ WIN (Lvl {lvl}) | {reg}")
                loss_streak = 0
            else:
                l += 1
                loss_streak += 1
                seq_max_loss = max(seq_max_loss, loss_streak)
                if verbose: print(f"{r['period']}: Pred={pred:5s} | Act={r['size']:5s}({r['number']}) | ❌ LOSS (Lvl {loss_streak}) | {reg}")
            hist.append(r)
        max_losses.append(seq_max_loss)
        total_wins += w
        total_losses += l
        if verbose: print(f"-> {name}: Wins={w}, Losses={l}, Max Consecutive Losses={seq_max_loss}")
    return max(max_losses), max_losses, total_wins, total_losses

print("Training script framework ready.")
