from search_best_strategy import generate_stream
from test_fix_5_losses import predict_pure_adaptive

stream = generate_stream(200000)
history = []
loss_streak = 0
max_loss_streak = 0
wins, losses = 0, 0
l1_w, l2_w, l3_w, busts = 0, 0, 0, 0

for r in stream:
    if len(history) < 20:
        history.append(r)
        continue
    pred_size, pred_num, conf, regime = predict_pure_adaptive(history, loss_streak)
    won = (pred_size == r['size'])
    if won:
        wins += 1
        if loss_streak == 0: l1_w += 1
        elif loss_streak == 1: l2_w += 1
        elif loss_streak == 2: l3_w += 1
        loss_streak = 0
    else:
        losses += 1
        loss_streak += 1
        max_loss_streak = max(max_loss_streak, loss_streak)
        if loss_streak > 2:
            busts += 1
            loss_streak = 0
    history.append(r)
    if len(history) > 100: history.pop(0)

total_cycles = l1_w + l2_w + l3_w + busts
print("\n================== 200,000 ROUNDS BENCHMARK (PURE ADAPTIVE) ==================")
print(f"Total Rounds: {wins+losses:,} | Wins: {wins:,} | Losses: {losses:,} | Raw Win Rate: {wins/(wins+losses)*100:.2f}%")
print(f"Level 1 Wins: {l1_w:,} ({l1_w/total_cycles*100:.1f}%)")
print(f"Level 2 Wins: {l2_w:,} ({l2_w/total_cycles*100:.1f}%)")
print(f"Level 3 Wins: {l3_w:,} ({l3_w/total_cycles*100:.1f}%)")
print(f"Cycle Win Rate (Resolved within <= 2 losses): {(total_cycles - busts)/total_cycles*100:.2f}%")
print(f"Level 3+ Busts: {busts:,} ({busts/total_cycles*100:.2f}%)")
