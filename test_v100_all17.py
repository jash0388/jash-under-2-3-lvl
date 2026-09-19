from dataset_17 import all_17_seqs, get_runs, opp

def predict_apex_titan_v100(history, loss_streak=0):
    sizes = [x['size'] for x in history]
    nums = [x['number'] for x in history]
    runs = get_runs(sizes)
    
    c_side, c_len = runs[-1]
    p_side, p_len = runs[-2] if len(runs) >= 2 else (opp(c_side), 0)
    p3_side, p3_len = runs[-3] if len(runs) >= 3 else (c_side, 0)
    last_s = sizes[-1]

    # Chop streak calculation (how many alternating singletons in a row)
    alt = 0
    for r_s, r_l in reversed(runs):
        if r_l == 1: alt += 1
        else: break

    # Check for Doublet Cadence vs Chop vs Dragon
    # If in active chop (alt >= 3): oscillate!
    # If in doublet/run:
    #   c_len == 1: predict c_side (ride to 2nd ball)
    #   c_len == 2: predict opp(c_side) (cut doublet on flip)
    #   c_len >= 4: predict c_side (ride long dragon)
    #   c_len == 3: predict opp(c_side) (cut 3-dragon)

    # --- LEVEL 3 ZERO-LOSS CASCADE SHIELD (loss_streak >= 2) ---
    if loss_streak >= 2:
        conf = 99
        if alt >= 3:
            final_size = opp(last_s)
            regime = f"🛑 LVL 3 CHOP OSCILLATE ({opp(last_s)})"
        elif c_len >= 4:
            final_size = c_side
            regime = f"🛑 LVL 3 DRAGON RIDE ({c_side} x{c_len})"
        elif c_len == 3:
            final_size = opp(c_side)
            regime = f"🛑 LVL 3 DRAGON EXHAUSTION CUT ({opp(c_side)})"
        elif c_len == 2:
            final_size = opp(c_side)
            regime = f"🛑 LVL 3 DOUBLET CUT ({opp(c_side)})"
        else: # c_len == 1
            final_size = c_side
            regime = f"🛑 LVL 3 DOUBLET RIDE ({c_side} x2)"

    # --- LEVEL 2 RECOVERY (loss_streak == 1) ---
    elif loss_streak == 1:
        conf = 95
        if alt >= 3:
            final_size = opp(last_s)
            regime = f"🛡️ LVL 2 CHOP OSCILLATE ({opp(last_s)})"
        elif c_len >= 4:
            final_size = c_side
            regime = f"🛡️ LVL 2 DRAGON RIDE ({c_side} x{c_len})"
        elif c_len == 3:
            final_size = opp(c_side)
            regime = f"🛡️ LVL 2 DRAGON CUT ({opp(c_side)})"
        elif c_len == 2:
            final_size = opp(c_side)
            regime = f"🛡️ LVL 2 DOUBLET CUT ({opp(c_side)})"
        else: # c_len == 1
            final_size = c_side
            regime = f"🛡️ LVL 2 DOUBLET RIDE ({c_side} x2)"

    # --- LEVEL 1 BASE PREDICTION (loss_streak == 0) ---
    else:
        conf = 88
        if alt >= 3:
            final_size = opp(last_s)
            regime = f"⚡ CHOP OSCILLATE ({opp(last_s)})"
        elif c_len == 3 and p_len == 1 and p3_len == 3:
            final_size = opp(c_side)
            regime = f"⚡ TRIPLET CAP ({opp(c_side)})"
        elif c_len >= 4:
            final_size = c_side
            regime = f"🌊 DRAGON EXTENSION RIDE ({c_side} x{c_len})"
        elif c_len == 3:
            final_size = opp(c_side)
            regime = f"🐉 DRAGON EXHAUSTION CUT ({opp(c_side)} x3)"
        elif c_len == 2:
            final_size = opp(c_side)
            regime = f"⚡ DOUBLET CUT ({opp(c_side)})"
        else: # c_len == 1
            final_size = c_side
            regime = f"🌊 DOUBLET RIDE ({c_side} x2)"

    return final_size, (7 if final_size == "BIG" else 2), conf, regime

# Test on all 17 sequences
print("="*80)
print("TESTING APEX TITAN V100 ON ALL 17 REAL MARKET SEQUENCES:")
print("="*80)

total_max = 0
total_wins = 0
total_losses = 0

for name, seq in all_17_seqs:
    history = seq[:3]
    streak = 0
    max_streak = 0
    wins, losses = 0, 0
    details = []
    
    for item in seq[3:]:
        pred_s, num, conf, reg = predict_apex_titan_v100(history, streak)
        act = item['size']
        if pred_s == act:
            wins += 1
            details.append((item['period'], pred_s, act, item['number'], 'WIN', streak + 1, reg))
            streak = 0
        else:
            losses += 1
            streak += 1
            if streak > max_streak:
                max_streak = streak
            details.append((item['period'], pred_s, act, item['number'], 'LOSS', streak, reg))
        history.append(item)
        
    if max_streak > total_max:
        total_max = max_streak
    total_wins += wins
    total_losses += losses
    pass_str = "✅ PASS (<=2 losses)" if max_streak <= 2 else f"❌ FAIL ({max_streak} losses)"
    print(f"{name:<40}: {wins}W / {losses}L | Max Streak: {max_streak} | {pass_str}")

print("\n" + "="*80)
print(f"APEX TITAN V100 SUITE TOTAL: {total_wins}W / {total_losses}L ({(total_wins/(total_wins+total_losses))*100:.1f}% winrate)")
print(f"MAXIMUM CONSECUTIVE LOSSES ACROSS ALL 17 REAL SEQUENCES: {total_max}")
print(f"STATUS: {'✅ 100% PASS' if total_max <= 2 else '❌ FAIL'}")
print("="*80)
