from dataset_real_all import all_real_sequences, get_runs, opp

def test_two_state(alt_threshold=2):
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
            sizes = [x['size'] for x in history]
            runs = get_runs(sizes)
            c_side, c_len = runs[-1]
            last_s = sizes[-1]
            
            alt = 0
            for r_s, r_l in reversed(runs):
                if r_l == 1: alt += 1
                else: break

            # TWO-STATE ENGINE:
            if alt >= alt_threshold:
                pred = opp(last_s)
                tag = f"CHOP_OSC (alt={alt})"
            else:
                pred = c_side
                tag = f"MOMENTUM (len={c_len})"
                
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

for thresh in [2, 3, 4]:
    tm, tw, tl, res = test_two_state(thresh)
    print("="*80)
    print(f"TWO-STATE ENGINE (alt_threshold={thresh}): {tw}W / {tl}L ({(tw/(tw+tl))*100:.1f}%) | MAX CONSECUTIVE LOSSES = {tm}")
    print("="*80)
    for name, w, l, ms, det in res:
        print(f"  {name:<35}: {w}W/{l}L | Max Streak: {ms} | {'✅ PASS' if ms <= 2 else f'❌ FAIL ({ms})'}")
