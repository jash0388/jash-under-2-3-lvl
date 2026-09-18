from test_harness_ab import seq_A, seq_B, opp

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

def test_on_all_seqs(pred_fn, name=""):
    print(f"\n==================== {name} ====================")
    for seq_name, seq in [("Sequence A (10859-10870)", seq_A), 
                          ("Sequence B (10954-10963)", seq_B),
                          ("Sequence C (11015-11027)", seq_C)]:
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
