from test_v18 import predict_apex_titan_v18
from search_best_strategy import generate_stream

print("Generating 200,000 WinGo rounds for massive stress test...")
stream = generate_stream(200000)

history = []
loss_streak = 0
max_loss_streak = 0
wins, losses = 0, 0
l1_w, l2_w, l3_w, busts = 0, 0, 0, 0

# Bankroll simulation: Rs 300 bankroll, Base bet Rs 3 (3, 7, 15)
balance = 300.0
base_bet = 3.0
bets = [3.0, 7.0, 16.0]
peak_balance = balance
min_balance = balance
bankruptcies = 0

for i, r in enumerate(stream):
    if len(history) < 20:
        history.append(r)
        continue
        
    bet_amount = bets[min(loss_streak, 2)]
    if balance < bet_amount:
        bankruptcies += 1
        balance = 300.0 # reset bankroll
        
    balance -= bet_amount
    
    pred_size, pred_num, conf, regime = predict_apex_titan_v18(history, loss_streak)
    won = (pred_size == r['size'])
    
    if won:
        wins += 1
        payout = bet_amount * 1.96
        balance += payout
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
            
    peak_balance = max(peak_balance, balance)
    min_balance = min(min_balance, balance)
    history.append(r)
    if len(history) > 100: history.pop(0)

total_cycles = l1_w + l2_w + l3_w + busts
print("\n================== 200,000 ROUNDS MASSIVE STRESS TEST ==================")
print(f"Total Rounds Evaluated: {wins+losses:,}")
print(f"Total Wins: {wins:,} | Losses: {losses:,} | Raw Hit Rate: {wins/(wins+losses)*100:.2f}%")
print(f"Level 1 Wins: {l1_w:,} ({l1_w/total_cycles*100:.1f}%)")
print(f"Level 2 Wins: {l2_w:,} ({l2_w/total_cycles*100:.1f}%)")
print(f"Level 3 Wins: {l3_w:,} ({l3_w/total_cycles*100:.1f}%)")
print(f"Total Recovery Cycle Success Rate (Wins within Level 1-3): {(total_cycles - busts)/total_cycles*100:.2f}%")
print(f"Level 3+ Busts: {busts:,} ({busts/total_cycles*100:.2f}%)")
print(f"Peak Balance Achieved: Rs {peak_balance:,.2f}")
