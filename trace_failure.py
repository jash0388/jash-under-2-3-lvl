from verify_v38_full import predict_apex_titan_v38

seq = [
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

print("=== STEP BY STEP TRACE ON PERIODS 10954-10963 ===")
hist = []
loss_streak = 0
for r in seq:
    if len(hist) < 3:
        hist.append(r)
        continue
    pred, reg = predict_apex_titan_v38(hist, loss_streak)
    won = (pred == r['size'])
    if won:
        loss_streak = 0
        status = "WIN"
    else:
        loss_streak += 1
        status = f"LOSS (Lvl {loss_streak})"
    print(f"{r['period']}: HistLast3={[h['size'] for h in hist[-3:]]} | Pred={pred:5s} | Act={r['size']:5s}({r['number']}) | {status} | {reg}")
    hist.append(r)
