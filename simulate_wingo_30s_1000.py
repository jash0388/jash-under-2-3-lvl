"""
Rigorous 1,000-Round WinGo 30-Second Simulation & Bankroll Stress Test
Starting Balance: ₹300
Base Bet: ₹3 (Martingale Progression: 3 -> 7 -> 15 -> 31 -> 63 -> 127 -> 255)
Game Mode: WinGo 30 Seconds (Fast alternating micro-patterns, dragon runs, and parity skews)
Engine: APEX NEURAL CONSENSUS (ANH-7)
"""

import random
import numpy as np
from collections import Counter

def generate_wingo_30s_stream(n_rounds=1000, seed=42):
    """
    WinGo 30S specific generator:
    - 30S game has rapid micro-cycles
    - Shorter dragon runs (3 to 6 avg), fast zig-zag waves (4 to 8 avg)
    - Reversals and parity spikes
    """
    random.seed(seed)
    stream = []
    regimes = ['noise', 'dragon_streak', 'zigzag_alt', 'doublets', 'parity_spike']
    weights = [0.35, 0.25, 0.25, 0.10, 0.05]
    
    current_regime = 'noise'
    rounds_left = 0
    
    for i in range(n_rounds):
        if rounds_left <= 0:
            current_regime = random.choices(regimes, weights=weights)[0]
            rounds_left = random.randint(3, 12) # 30S cycles are shorter
            
        rounds_left -= 1
        
        if current_regime == 'noise':
            num = random.randint(0, 9)
        elif current_regime == 'dragon_streak':
            last_side = stream[-1]['size'] if stream else 'BIG'
            if random.random() < 0.78:
                num = random.choice([5,6,7,8,9] if last_side == 'BIG' else [0,1,2,3,4])
            else:
                num = random.choice([0,1,2,3,4] if last_side == 'BIG' else [5,6,7,8,9])
        elif current_regime == 'zigzag_alt':
            last_side = stream[-1]['size'] if stream else 'BIG'
            target_side = 'SMALL' if last_side == 'BIG' else 'BIG'
            if random.random() < 0.80:
                num = random.choice([5,6,7,8,9] if target_side == 'BIG' else [0,1,2,3,4])
            else:
                num = random.choice([0,1,2,3,4] if target_side == 'BIG' else [5,6,7,8,9])
        elif current_regime == 'doublets':
            if len(stream) >= 2 and stream[-1]['size'] == stream[-2]['size']:
                target = 'SMALL' if stream[-1]['size'] == 'BIG' else 'BIG'
            else:
                target = stream[-1]['size'] if stream else 'BIG'
            num = random.choice([5,6,7,8,9] if target == 'BIG' else [0,1,2,3,4])
        elif current_regime == 'parity_spike':
            # Rapid odds / evens
            num = random.choice([1,3,5,7,9] if (i % 2 == 0) else [0,2,4,6,8])
            
        size = 'BIG' if num >= 5 else 'SMALL'
        color = 'RED' if num in [2,4,6,8,0] else 'GREEN'
        stream.append({'period': i + 1, 'number': num, 'size': size, 'color': color})
    return stream

def algo_apex_30s(history):
    if len(history) < 3:
        return 'BIG', 7, 65
    nums = [x['number'] for x in history[-30:]]
    sizes = [x['size'] for x in history[-30:]]
    last_size = sizes[-1]
    
    streak = 1
    for i in range(len(sizes)-2, -1, -1):
        if sizes[i] == last_size: streak += 1
        else: break
        
    alt = 1
    for i in range(len(sizes)-1, 0, -1):
        if sizes[i] != sizes[i-1]: alt += 1
        else: break
        
    m_big, m_small = 1.0, 1.0
    if len(sizes) >= 5:
        k2 = (sizes[-2], sizes[-1])
        for i in range(len(sizes)-2):
            if (sizes[i], sizes[i+1]) == k2:
                if sizes[i+2] == 'BIG': m_big += 1.5
                else: m_small += 1.5
                
    ewma_b, ewma_s = 0.0, 0.0
    for i, s in enumerate(reversed(sizes[-15:])):
        w = 0.85 ** i
        if s == 'BIG': ewma_b += w
        else: ewma_s += w
        
    score_b, score_s = 0.0, 0.0
    if 3 <= streak <= 6:
        if last_size == 'BIG': score_b += 5.5
        else: score_s += 5.5
    elif streak > 6:
        if last_size == 'BIG': score_s += 5.0
        else: score_b += 5.0
    elif alt >= 3:
        target = 'SMALL' if last_size == 'BIG' else 'BIG'
        if target == 'BIG': score_b += 5.2
        else: score_s += 5.2
    else:
        score_b += (m_big/(m_big+m_small))*3.2 + (ewma_b/(ewma_b+ewma_s))*2.5
        score_s += (m_small/(m_big+m_small))*3.2 + (ewma_s/(ewma_b+ewma_s))*2.5
        
    pred_size = 'BIG' if score_b >= score_s else 'SMALL'
    allowed = [5,6,7,8,9] if pred_size == 'BIG' else [0,1,2,3,4]
    freq = Counter(nums[-20:])
    best_num = min(allowed, key=lambda n: (freq[n], abs(n - (7 if pred_size == 'BIG' else 2))))
    return pred_size, best_num, 75

# 1. Run a sample single detailed 1000-round run
def run_detailed_1000_round_session(seed=12345):
    stream = generate_wingo_30s_stream(n_rounds=1000, seed=seed)
    balance = 300.0
    bet_seq = [3, 7, 15, 31, 63, 127, 255]
    step = 0
    
    peak_balance = balance
    peak_round = 0
    bust_round = None
    
    wins = 0
    losses = 0
    history_log = []
    
    milestones = {} # balance at round 100, 200, 300...
    
    current_loss_streak = 0
    max_loss_streak = 0
    current_win_streak = 0
    max_win_streak = 0
    
    for r in range(len(stream)):
        if balance < 1.0:
            if bust_round is None:
                bust_round = r
            break
            
        history_slice = stream[max(0, r-30):r]
        pred_size, pred_num, conf = algo_apex_30s(history_slice)
        actual = stream[r]
        
        current_bet = bet_seq[step] if step < len(bet_seq) else bet_seq[-1]
        if current_bet > balance:
            current_bet = balance
            
        won = (pred_size == actual['size'])
        
        if won:
            wins += 1
            profit = current_bet * 0.96
            balance += profit
            step = 0
            current_win_streak += 1
            max_win_streak = max(max_win_streak, current_win_streak)
            current_loss_streak = 0
        else:
            losses += 1
            balance -= current_bet
            step += 1
            current_loss_streak += 1
            max_loss_streak = max(max_loss_streak, current_loss_streak)
            current_win_streak = 0
            
        if balance > peak_balance:
            peak_balance = balance
            peak_round = r + 1
            
        if (r + 1) in [50, 100, 200, 300, 400, 500, 750, 1000]:
            milestones[r + 1] = balance
            
    return {
        'seed': seed,
        'final_balance': max(0.0, balance),
        'peak_balance': peak_balance,
        'peak_round': peak_round,
        'bust_round': bust_round,
        'rounds_completed': r if bust_round else 1000,
        'wins': wins,
        'losses': losses,
        'win_rate': wins / (wins + losses) * 100 if (wins + losses) else 0,
        'max_loss_streak': max_loss_streak,
        'max_win_streak': max_win_streak,
        'milestones': milestones
    }

# 2. Run Monte Carlo over 1,000 distinct 1,000-round sessions
def run_monte_carlo_1000_rounds(n_simulations=1000):
    all_results = []
    
    for s in range(n_simulations):
        stream = generate_wingo_30s_stream(n_rounds=1000, seed=50000 + s)
        balance = 300.0
        bet_seq = [3, 7, 15, 31, 63, 127, 255]
        step = 0
        peak_balance = balance
        peak_round = 0
        bust_round = None
        wins, losses = 0, 0
        
        for r in range(1000):
            if balance < 1.0:
                bust_round = r + 1
                break
                
            history_slice = stream[max(0, r-30):r]
            pred_size, _, _ = algo_apex_30s(history_slice)
            actual = stream[r]
            
            current_bet = bet_seq[step] if step < len(bet_seq) else bet_seq[-1]
            if current_bet > balance: current_bet = balance
            
            won = (pred_size == actual['size'])
            if won:
                wins += 1
                balance += current_bet * 0.96
                step = 0
            else:
                losses += 1
                balance -= current_bet
                step += 1
                
            if balance > peak_balance:
                peak_balance = balance
                peak_round = r + 1
                
        all_results.append({
            'busted': bust_round is not None,
            'bust_round': bust_round,
            'final_balance': max(0.0, balance),
            'peak_balance': peak_balance,
            'peak_round': peak_round,
            'rounds_played': bust_round if bust_round else 1000
        })
        
    return all_results

if __name__ == '__main__':
    print("=====================================================================")
    print("🎯 WINGO 30 SECONDS — 1,000 ROUNDS RIGOROUS EXPERIMENT")
    print("💰 Starting Bankroll: ₹300 | Base Bet: ₹3 | Strategy: APEX NEURAL ANH-7")
    print("=====================================================================")
    
    # Run 5 Sample Sessions with different random market profiles
    for i, seed_val in enumerate([101, 777, 999, 2026, 8888]):
        res = run_detailed_1000_round_session(seed=seed_val)
        print(f"\n--- 🧪 TEST RUN #{i+1} (Seed {seed_val}) ---")
        print(f"  • Total Rounds Played    : {res['rounds_completed']} / 1000")
        print(f"  • Flat Win Rate          : {res['win_rate']:.2f}% ({res['wins']}W / {res['losses']}L)")
        print(f"  • Max Win Streak         : {res['max_win_streak']} consecutive wins")
        print(f"  • Max Loss Streak        : {res['max_loss_streak']} consecutive losses")
        print(f"  • 🏔️ HIGHEST PEAK BALANCE: ₹{res['peak_balance']:.2f} (Reached at Round {res['peak_round']})")
        if res['bust_round']:
            print(f"  • 💥 BUSTED AT ROUND     : Round {res['bust_round']}")
        else:
            print(f"  • 🏆 SURVIVED ALL 1000!  : Final Balance ₹{res['final_balance']:.2f}")
            
        print(f"  • 📊 Balance Milestones  :")
        for rnd, bal in sorted(res['milestones'].items()):
            print(f"      Round {rnd:4d}: ₹{bal:7.2f}")
            
    # Aggregate Monte Carlo across 1,000 sessions of 1,000 rounds
    print("\n\n=====================================================================")
    print("📈 AGGREGATE MONTE CARLO ANALYSIS (1,000 PLAYERS x 1,000 ROUNDS)")
    print("=====================================================================")
    mc_results = run_monte_carlo_1000_rounds(1000)
    
    busted = [r for r in mc_results if r['busted']]
    survived = [r for r in mc_results if not r['busted']]
    bust_rounds = [r['bust_round'] for r in busted]
    peak_balances = [r['peak_balance'] for r in mc_results]
    peak_rounds = [r['peak_round'] for r in mc_results]
    
    print(f"Total 1,000-Round Simulations : 1,000")
    print(f"Players who Busted before 1000: {len(busted)/10:.1f}% ({len(busted)}/1000)")
    print(f"Players who Survived all 1000 : {len(survived)/10:.1f}% ({len(survived)}/1000)")
    
    print(f"\n🏔️ PEAK BALANCE STATISTICS (All Players):")
    print(f"  • Average Peak Balance Reached : ₹{np.mean(peak_balances):.2f}")
    print(f"  • Median Peak Balance Reached  : ₹{np.median(peak_balances):.2f}")
    print(f"  • Highest Record Peak Reached  : ₹{np.max(peak_balances):.2f}")
    print(f"  • Average Round of Peak        : Round {np.mean(peak_rounds):.1f}")
    print(f"  • Median Round of Peak         : Round {np.median(peak_rounds):.0f}")
    
    print(f"\n💥 BUST ROUND STATISTICS (For Busted Players):")
    print(f"  • Average Round of Bust        : Round {np.mean(bust_rounds):.1f}")
    print(f"  • Median Round of Bust         : Round {np.median(bust_rounds):.0f}")
    print(f"  • Earliest Bust (Bad Luck)     : Round {np.min(bust_rounds)}")
    print(f"  • Latest Bust                  : Round {np.max(bust_rounds)}")
    
    # Milestone Survival Distribution
    print(f"\n📊 SURVIVAL PROBABILITY BY ROUND MILESTONE:")
    for m in [50, 100, 200, 300, 400, 500, 750, 1000]:
        surv_m = sum(1 for r in mc_results if r['rounds_played'] >= m)
        print(f"  • Round {m:4d} : {surv_m/10:.1f}% of players still alive")
