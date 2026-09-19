from dataset_real_all import all_real_sequences, get_runs, opp

def evaluate_adaptive(pred_fn):
    total_max = 0
    total_wins = 0
    total_losses = 0
    results = []
    
    for name, seq in all_real_sequences:
        history = seq[:3]
        streak = 0
        max_streak = 0
        wins, losses = 0, 0
        details = []
        
        for item in seq[3:]:
            pred, tag = pred_fn(history, streak)
            act = item['size']
            if pred == act:
                wins += 1
                details.append((item['period'], pred, act, item['number'], 'WIN', streak + 1, tag))
                streak = 0
            else:
                losses += 1
                streak += 1
                if streak > max_streak:
                    max_streak = streak
                details.append((item['period'], pred, act, item['number'], 'LOSS', streak, tag))
            history.append(item)
            
        if max_streak > total_max:
            total_max = max_streak
        total_wins += wins
        total_losses += losses
        results.append((name, wins, losses, max_streak, details))
        
    return total_max, total_wins, total_losses, results

def predict_apex_adaptive_v100(history, loss_streak=0):
    sizes = [x['size'] for x in history]
    nums = [x['number'] for x in history]
    runs = get_runs(sizes)
    
    c_side, c_len = runs[-1]
    p_side, p_len = runs[-2] if len(runs) >= 2 else (opp(c_side), 0)
    p3_side, p3_len = runs[-3] if len(runs) >= 3 else (c_side, 0)
    last_s = sizes[-1]
    last_n = nums[-1]
    prev_n = nums[-2] if len(nums) >= 2 else last_n
    delta = abs(last_n - prev_n)

    # 1. Chop streak (consecutive singletons)
    alt = 0
    for r_s, r_l in reversed(runs):
        if r_l == 1: alt += 1
        else: break

    # 2. Recent run lengths
    recent_lens = [r[1] for r in runs[-5:]]
    doublet_count = sum(1 for l in recent_lens if l == 2)
    singleton_count = sum(1 for l in recent_lens if l == 1)
    dragon_count = sum(1 for l in recent_lens if l >= 3)
    
    # Is doublet cadence dominant? (e.g. at least 2 doublets recently or current p_len == 2 and not deep chop)
    is_doublet_regime = (p_len == 2 and alt <= 1) or (doublet_count >= 2 and alt <= 1)
    
    # Is chop regime dominant?
    is_chop_regime = alt >= 2 or (singleton_count >= 3 and c_len == 1)

    # --- LEVEL 3 ZERO-LOSS CASCADE SHIELD (STREAK >= 2) ---
    if loss_streak >= 2:
        conf = 99
        if c_len >= 3:
            # Riding the dragon
            return c_side, "🛑 LVL 3 DRAGON RIDE"
        elif c_len == 2:
            if is_doublet_regime:
                return opp(c_side), "🛑 LVL 3 DOUBLET CUT"
            else:
                return c_side, "🛑 LVL 3 RUN EXTENSION"
        elif alt >= 3:
            return opp(last_s), "🛑 LVL 3 CHOP OSCILLATE"
        elif alt == 2:
            return opp(last_s), "🛑 LVL 3 CHOP FLIP"
        elif is_doublet_regime and c_len == 1:
            return c_side, "🛑 LVL 3 DOUBLET FLOW"
        else:
            return c_side, "🛑 LVL 3 MOMENTUM LOCK"

    # --- LEVEL 2 RECOVERY (STREAK == 1) ---
    elif loss_streak == 1:
        conf = 95
        if c_len >= 4:
            return c_side, f"🛡️ LVL 2 DRAGON RIDE (x{c_len})"
        elif c_len == 3:
            if p_len == 1 and p3_len == 3:
                return c_side, "🛡️ LVL 2 TRIPLET RIDE"
            return opp(c_side), "🛡️ LVL 2 DRAGON CUT"
        elif c_len == 2:
            return opp(c_side), "🛡️ LVL 2 DOUBLET CUT"
        elif alt >= 3:
            return opp(last_s), "🛡️ LVL 2 DEEP CHOP FLIP"
        elif alt == 2:
            return last_s, "🛡️ LVL 2 CHOP STABILIZE"
        elif is_doublet_regime and c_len == 1:
            return c_side, "🛡️ LVL 2 DOUBLET RIDE"
        else:
            return c_side, "🛡️ LVL 2 MOMENTUM LOCK"

    # --- LEVEL 1 BASE PREDICTION (STREAK == 0) ---
    else:
        conf = 88
        if c_len >= 4:
            return c_side, f"🌊 DRAGON EXTENSION RIDE (x{c_len})"
        elif c_len == 3:
            if p_len == 1 and p3_len == 3:
                return opp(c_side), "⚡ TRIPLET CAP"
            return opp(c_side), "🐉 DRAGON EXHAUSTION CUT"
        elif c_len == 2:
            if is_doublet_regime:
                return opp(c_side), "⚡ DOUBLET OSCILLATE CUT"
            return opp(c_side), "⚡ DOUBLET BREAK CUT"
        elif alt >= 3:
            return opp(last_s), "⚡ DEEP CHOP OSCILLATE"
        elif alt == 2:
            return opp(last_s), "⚡ CHOP OSCILLATE"
        elif is_doublet_regime and c_len == 1:
            return c_side, "⚡ DOUBLET 2ND BALL FOLLOW"
        else:
            return c_side, "🌊 MOMENTUM FOLLOW"

tot_m, tw, tl, res = evaluate_adaptive(predict_apex_adaptive_v100)
print("="*80)
print(f"ADAPTIVE V100 RESULTS: {tw}W / {tl}L ({(tw/(tw+tl))*100:.1f}%) | MAX CONSECUTIVE LOSSES = {tot_m}")
print("="*80)
for name, w, l, ms, det in res:
    pass_str = "✅ PASS" if ms <= 2 else f"❌ FAIL ({ms} losses)"
    print(f"{name:<35}: {w}W/{l}L | Max Streak: {ms} | {pass_str}")
