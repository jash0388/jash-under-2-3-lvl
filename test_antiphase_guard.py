from dataset_real_all import all_real_sequences, get_runs, opp

def run_antiphase_test(l3_mode='INVERT'):
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
        last_predictions = []
        
        for item in seq[3:]:
            sizes = [x['size'] for x in history]
            runs = get_runs(sizes)
            c_side, c_len = runs[-1]
            last_s = sizes[-1]
            
            alt = 0
            for r_s, r_l in reversed(runs):
                if r_l == 1: alt += 1
                else: break

            # 1. Base Prediction (Streak == 0)
            if alt >= 3:
                base_pred = opp(last_s)
                tag = f"CHOP_OSC (alt={alt})"
            elif c_len >= 3 and (len(runs) >= 2 and runs[-2][1] == 1):
                base_pred = opp(c_side) # Cut dragon after chop
                tag = f"DRAGON_CUT (len={c_len})"
            else:
                base_pred = c_side
                tag = f"MOMENTUM (len={c_len})"

            # 2. Apply Recovery Level State Machine
            if streak == 0:
                pred = base_pred
            elif streak == 1:
                # Level 2 Recovery
                if c_len >= 3:
                    pred = c_side # Ride dragon at L2
                    tag = "L2_DRAGON_RIDE"
                elif alt >= 2:
                    pred = last_s # Stabilize chop
                    tag = "L2_CHOP_STAB"
                else:
                    pred = opp(base_pred) # Flip
                    tag = "L2_FLIP"
            else: # streak >= 2 (Level 3 Zero-Loss Cascade Shield)
                if l3_mode == 'INVERT':
                    pred = opp(base_pred)
                    tag = "🛑 L3_ANTIPHASE_INVERT"
                elif l3_mode == 'MOM_LOCK':
                    pred = c_side
                    tag = "🛑 L3_MOM_LOCK"
                elif l3_mode == 'ADAPTIVE':
                    if c_len >= 2:
                        pred = c_side
                        tag = "🛑 L3_RUN_LOCK"
                    else:
                        pred = opp(last_s)
                        tag = "🛑 L3_CHOP_FLIP"
                
            act = item['size']
            if pred == act:
                wins += 1
                streak = 0
                details.append((item['period'], pred, act, item['number'], 'WIN', streak + 1, tag))
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

for mode in ['INVERT', 'MOM_LOCK', 'ADAPTIVE']:
    tm, tw, tl, res = run_antiphase_test(mode)
    print("="*80)
    print(f"L3 MODE = {mode}: {tw}W / {tl}L ({(tw/(tw+tl))*100:.1f}%) | MAX CONSECUTIVE LOSSES = {tm}")
    print("="*80)
    for name, w, l, ms, det in res:
        print(f"  {name:<35}: {w}W/{l}L | Max Streak: {ms} | {'✅ PASS' if ms <= 2 else f'❌ FAIL ({ms})'}")
