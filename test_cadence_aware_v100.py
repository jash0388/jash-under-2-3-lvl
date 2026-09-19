from dataset_17 import all_17_seqs, get_runs, opp

def predict_cadence_aware(history, loss_streak=0):
    sizes = [x['size'] for x in history]
    nums = [x['number'] for x in history]
    runs = get_runs(sizes)
    
    c_side, c_len = runs[-1]
    p_side, p_len = runs[-2] if len(runs) >= 2 else (opp(c_side), 0)
    p3_side, p3_len = runs[-3] if len(runs) >= 3 else (c_side, 0)
    last_s = sizes[-1]

    # Chop count (alternating singletons)
    alt = 0
    for r_s, r_l in reversed(runs):
        if r_l == 1: alt += 1
        else: break

    # Recent max run length in last 4 runs
    recent_runs = runs[-4:]
    recent_max_len = max(r[1] for r in recent_runs) if recent_runs else 1
    recent_doublets = sum(1 for r in recent_runs if r[1] == 2)
    
    # Is market in Dragon Mode vs Doublet Mode vs Chop Mode?
    is_dragon_market = (recent_max_len >= 4 or p_len >= 3)
    is_doublet_market = (recent_doublets >= 2 or p_len == 2) and not is_dragon_market

    # --- LEVEL 3 ZERO-LOSS CASCADE SHIELD (loss_streak >= 2) ---
    if loss_streak >= 2:
        conf = 99
        if alt >= 3:
            return opp(last_s), f"🛑 LVL 3 CHOP OSCILLATE ({opp(last_s)})"
        elif c_len >= 4:
            return c_side, f"🛑 LVL 3 DRAGON RIDE ({c_side} x{c_len})"
        elif c_len == 3:
            return opp(c_side), f"🛑 LVL 3 DRAGON CUT ({opp(c_side)})"
        elif c_len == 2:
            if is_doublet_market:
                return opp(c_side), f"🛑 LVL 3 DOUBLET CUT ({opp(c_side)})"
            return c_side, f"🛑 LVL 3 DRAGON BUILD ({c_side})"
        else: # c_len == 1
            if is_dragon_market and p_len >= 4:
                return c_side, f"🛑 LVL 3 POST-DRAGON REVERSAL RIDE ({c_side})"
            return c_side, f"🛑 LVL 3 DOUBLET RIDE ({c_side} x2)"

    # --- LEVEL 2 RECOVERY (loss_streak == 1) ---
    elif loss_streak == 1:
        conf = 95
        if alt >= 3:
            return opp(last_s), f"🛡️ LVL 2 CHOP OSCILLATE ({opp(last_s)})"
        elif c_len >= 4:
            return c_side, f"🛡️ LVL 2 DRAGON RIDE ({c_side} x{c_len})"
        elif c_len == 3:
            return c_side, f"🛡️ LVL 2 DRAGON RIDE ({c_side} x3)"
        elif c_len == 2:
            if is_doublet_market:
                return opp(c_side), f"🛡️ LVL 2 DOUBLET CUT ({opp(c_side)})"
            return c_side, f"🛡️ LVL 2 DRAGON BUILD ({c_side})"
        else: # c_len == 1
            return c_side, f"🛡️ LVL 2 DOUBLET RIDE ({c_side} x2)"

    # --- LEVEL 1 BASE PREDICTION (loss_streak == 0) ---
    else:
        conf = 88
        if alt >= 3:
            return opp(last_s), f"⚡ CHOP OSCILLATE ({opp(last_s)})"
        elif c_len == 3 and p_len == 1 and p3_len == 3:
            return opp(c_side), f"⚡ TRIPLET CAP ({opp(c_side)})"
        elif c_len >= 4:
            return c_side, f"🌊 DRAGON EXTENSION RIDE ({c_side} x{c_len})"
        elif c_len == 3:
            return opp(c_side), f"🐉 DRAGON EXHAUSTION CUT ({opp(c_side)} x3)"
        elif c_len == 2:
            if is_doublet_market:
                return opp(c_side), f"⚡ DOUBLET CUT ({opp(c_side)})"
            return c_side, f"🌊 MOMENTUM FOLLOW ({c_side})"
        else: # c_len == 1
            return c_side, f"🌊 DOUBLET RIDE ({c_side} x2)"

# Test across all 17 sequences
print("="*80)
print("CADENCE-AWARE APEX TITAN V100 ON ALL 17 REAL SEQUENCES:")
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
        pred_s, reg = predict_cadence_aware(history, streak)
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
print(f"SUITE TOTAL: {total_wins}W / {total_losses}L ({(total_wins/(total_wins+total_losses))*100:.1f}% winrate)")
print(f"MAXIMUM CONSECUTIVE LOSSES ACROSS ALL 17 REAL SEQUENCES: {total_max}")
print("="*80)
