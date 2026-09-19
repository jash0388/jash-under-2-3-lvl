from test_master_ensemble import all_seqs, opp
from test_ultra_optimizer import predict_apex_ultra

for name, seq in all_seqs.items():
    print(f"\n==================== {name} ====================")
    hist = []
    loss_streak = 0
    max_loss = 0
    wins, losses = 0, 0
    l1_w, l2_w, l3_w, busts = 0, 0, 0, 0
    for r in seq:
        if len(hist) < 3:
            hist.append(r)
            continue
        pred, reg = predict_apex_ultra(hist, loss_streak)
        won = (pred == r['size'])
        if won:
            wins += 1
            if loss_streak == 0: l1_w += 1
            elif loss_streak == 1: l2_w += 1
            elif loss_streak == 2: l3_w += 1
            lvl = 1 if loss_streak == 0 else loss_streak + 1
            status = f'✅ WIN (Lvl {lvl})'
            loss_streak = 0
        else:
            losses += 1
            loss_streak += 1
            max_loss = max(max_loss, loss_streak)
            if loss_streak > 2:
                busts += 1
                loss_streak = 0
            status = f'❌ LOSS (Lvl {loss_streak})'
        print(f"{r['period']}: Pred={pred:5s} | Act={r['size']:5s}({r['number']}) | {status:15s} | {reg}")
        hist.append(r)
    rounds = len(seq) - 3
    print(f"Summary {name}: Rounds={rounds}, Wins={wins}, WinRate={wins/rounds*100:.1f}%, MAX CONSECUTIVE LOSSES = {max_loss}, Busts = {busts}")
