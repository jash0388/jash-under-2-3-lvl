import json, re

# Load cleaned master dataset
data = json.load(open('dataset_full_master.json'))

def get_num(p):
    s = str(p).strip()
    digits = re.findall(r'\d+', s)
    return int(digits[0]) if digits else 0

unique_dict = {}
for d in data:
    k = get_num(d['period'])
    unique_dict[k] = {
        'period': k,
        'number': int(d['number']),
        'size': 'BIG' if int(d['number']) >= 5 else 'SMALL'
    }

sorted_keys = sorted(unique_dict.keys())
sorted_draws = [unique_dict[k] for k in sorted_keys]

def opp(s):
    return 'SMALL' if s == 'BIG' else 'BIG'

def predict_pure_prng(history):
    if len(history) < 5:
        return 'BIG', 7
    
    nums = history
    nLen = len(nums)
    lastNum = nums[-1]

    # 1. 10x10 Markov
    matrix = [[0]*10 for _ in range(10)]
    for i in range(1, nLen):
        matrix[nums[i-1]][nums[i]] += 1
    
    lastRow = matrix[lastNum]
    bigSum = sum(lastRow[5:])
    smallSum = sum(lastRow[:5])
    markovSize = 'BIG' if bigSum >= smallSum else 'SMALL'

    # 2. LCG Residue (15-draw window)
    bestA, bestC, bestHits = 1, 9, -1
    window15 = nums[-15:]
    for a in [1, 3, 7, 9]:
        for c in range(10):
            hits = 0
            for j in range(1, len(window15)):
                if (a * window15[j-1] + c) % 10 == window15[j]:
                    hits += 1
            if hits > bestHits:
                bestHits = hits
                bestA = a
                bestC = c
    lcgResidue = (bestA * lastNum + bestC) % 10
    lcgSize = 'BIG' if lcgResidue >= 5 else 'SMALL'

    # 3. LFG Residue
    dMinus2 = nums[-2] if nLen >= 2 else lastNum
    dMinus4 = nums[-4] if nLen >= 4 else 0
    lfgResidue = ((dMinus2 - dMinus4) + 10) % 10
    lfgSize = 'BIG' if lfgResidue >= 5 else 'SMALL'

    # 4. Ensemble
    votes = [markovSize, lcgSize, lfgSize]
    bigVotes = votes.count('BIG')
    finalSize = 'BIG' if bigVotes >= 2 else 'SMALL'

    # 5. Dragon Momentum Safety
    streakLen = 1
    lastSide = 'BIG' if lastNum >= 5 else 'SMALL'
    for i in range(nLen - 2, -1, -1):
        s = 'BIG' if nums[i] >= 5 else 'SMALL'
        if s == lastSide:
            streakLen += 1
        else:
            break
    if 3 <= streakLen < 6:
        finalSize = lastSide

    return finalSize, lastRow

def run_backtest():
    print(f"Loaded {len(sorted_draws)} chronological draws ({sorted_draws[0]['period']} to {sorted_draws[-1]['period']}).")
    
    # Precompute raw predictions
    raw_preds = []
    for i in range(len(sorted_draws)):
        if i < 20:
            raw_preds.append(('BIG', [1]*10))
        else:
            hist = [d['number'] for d in sorted_draws[:i]]
            raw_preds.append(predict_pure_prng(hist))

    # Dual-Phase Hysteresis Engine K=7 (low<=2, high>=3)
    curr_phase = 'STRAIGHT'
    phase_history = []
    
    bankroll = 0.0
    real_bets = 0
    real_wins = 0
    curr_real_loss_streak = 0
    in_virtual = False
    shield_saves = 0
    max_real_loss_streak = 0
    
    l1_wins = 0
    l2_wins = 0
    virtual_rounds = 0
    straight_rounds = 0
    reverse_rounds = 0

    results = []

    for i in range(20, len(sorted_draws)):
        actual = sorted_draws[i]['size']
        raw, lastRow = raw_preds[i]

        # Phase update
        K = 7
        if len(phase_history) >= K:
            rolling_hits = sum(1 for h in phase_history[-K:] if h)
            if curr_phase == 'STRAIGHT':
                if rolling_hits <= 2:
                    curr_phase = 'REVERSE'
            else:
                if rolling_hits >= 3:
                    curr_phase = 'STRAIGHT'

        pred = raw if curr_phase == 'STRAIGHT' else opp(raw)
        is_win = (pred == actual)
        raw_hit = (raw == actual)
        
        phase_history.append(raw_hit)
        if len(phase_history) > 25:
            phase_history.pop(0)

        if curr_phase == 'STRAIGHT':
            straight_rounds += 1
        else:
            reverse_rounds += 1

        if not in_virtual:
            real_bets += 1
            stake = 2 if curr_real_loss_streak == 0 else 4
            if is_win:
                real_wins += 1
                bankroll += stake * 0.96
                if curr_real_loss_streak == 0:
                    l1_wins += 1
                else:
                    l2_wins += 1
                curr_real_loss_streak = 0
            else:
                bankroll -= stake
                curr_real_loss_streak += 1
                if curr_real_loss_streak > max_real_loss_streak:
                    max_real_loss_streak = curr_real_loss_streak
                if curr_real_loss_streak >= 2:
                    in_virtual = True # Enter virtual paper mode!
        else:
            virtual_rounds += 1
            if is_win:
                in_virtual = False
                curr_real_loss_streak = 0 # Reset to Level 1
            else:
                shield_saves += 1

        results.append({
            'period': sorted_draws[i]['period'],
            'number': sorted_draws[i]['number'],
            'actual': actual,
            'pred': pred,
            'raw': raw,
            'phase': curr_phase,
            'is_win': is_win,
            'in_virtual': in_virtual
        })

    win_rate = (real_wins / real_bets * 100) if real_bets > 0 else 0
    print("=" * 60)
    print("⚡ TITAN SUPREME v2.0 DUAL-PHASE (STRAIGHT & REVERSE) REPORT")
    print("=" * 60)
    print(f"Total Rounds Simulated      : {len(results)}")
    print(f"Total Real Bets Placed      : {real_bets}")
    print(f"Total Real Wins             : {real_wins} ({win_rate:.2f}%)")
    print(f"Level 1 Wins                : {l1_wins}")
    print(f"Level 2 Wins                : {l2_wins}")
    print(f"Shield Saves (Rs 0 Bet)     : {shield_saves}")
    print(f"Virtual Paper Rounds        : {virtual_rounds}")
    print(f"Max Real Consecutive Losses : {max_real_loss_streak} (STRICT <= 2)")
    print(f"Straight Phase Rounds       : {straight_rounds}")
    print(f"Reverse Phase Rounds        : {reverse_rounds}")
    print(f"Final Net Profit            : Rs {bankroll:+.2f}")
    print("=" * 60)
    
    summary = {
        'total_draws': len(sorted_draws),
        'real_bets': real_bets,
        'real_wins': real_wins,
        'win_rate': round(win_rate, 2),
        'l1_wins': l1_wins,
        'l2_wins': l2_wins,
        'shield_saves': shield_saves,
        'max_real_loss_level': max_real_loss_streak,
        'final_profit_rs': round(bankroll, 2),
        'straight_rounds': straight_rounds,
        'reverse_rounds': reverse_rounds
    }
    with open('train_results_v2.json', 'w') as f:
        json.dump(summary, f, indent=2)

if __name__ == '__main__':
    run_backtest()
