"""
Rigorous 2,000-Round WinGo 30-Second Simulation & Bankroll Stress Test
Starting Balance: ₹500
Base Bet: ₹2 (Martingale Progression: 2 -> 5 -> 11 -> 23 -> 47 -> 95 -> 191 -> 383)
Total Bankroll Protection: 7 Consecutive Losses Absorbed! (Wipeout requires 8 consecutive losses)
Engine: APEX NEURAL CONSENSUS (ANH-7)
"""

import random
import numpy as np
from collections import Counter
from simulate_wingo_30s_1000 import generate_wingo_30s_stream, algo_apex_30s

def run_single_2000_round_session(seed=12345):
    stream = generate_wingo_30s_stream(n_rounds=2000, seed=seed)
    balance = 500.0
    # Progression: 2, 5, 11, 23, 47, 95, 191, 383
    # Cumulative: 2, 7, 18, 41, 88, 183, 374 (Survives 7 losses on ₹500)
    bet_seq = [2, 5, 11, 23, 47, 95, 191, 383]
    step = 0
    
    peak_balance = balance
    peak_round = 0
    bust_round = None
    
    wins = 0
    losses = 0
    
    current_loss_streak = 0
    max_loss_streak = 0
    current_win_streak = 0
    max_win_streak = 0
    
    milestones = {}
    
    for r in range(len(stream)):
        if balance < 1.0:
            bust_round = r + 1
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
            
        if (r + 1) in [100, 250, 500, 750, 1000, 1500, 2000]:
            milestones[r + 1] = balance
            
    return {
        'seed': seed,
        'final_balance': max(0.0, balance),
        'peak_balance': peak_balance,
        'peak_round': peak_round,
        'bust_round': bust_round,
        'rounds_completed': r + 1 if bust_round else 2000,
        'wins': wins,
        'losses': losses,
        'win_rate': wins / (wins + losses) * 100 if (wins + losses) else 0,
        'max_loss_streak': max_loss_streak,
        'max_win_streak': max_win_streak,
        'milestones': milestones
    }

def run_monte_carlo_2000_rounds(n_simulations=1000):
    all_results = []
    
    for s in range(n_simulations):
        stream = generate_wingo_30s_stream(n_rounds=2000, seed=70000 + s)
        balance = 500.0
        bet_seq = [2, 5, 11, 23, 47, 95, 191, 383]
        step = 0
        peak_balance = balance
        peak_round = 0
        bust_round = None
        
        for r in range(2000):
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
                balance += current_bet * 0.96
                step = 0
            else:
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
            'rounds_played': bust_round if bust_round else 2000
        })
        
    return all_results

if __name__ == '__main__':
    print("=====================================================================")
    print("🚀 WINGO 30 SECONDS — 2,000 ROUNDS DEEP SIMULATION")
    print("💰 Starting Bankroll: ₹500 | Base Bet: ₹2 | Engine: APEX NEURAL ANH-7")
    print("🛡️ Bankroll Buffer: 7 Levels of Protection (Wipeout requires 8 losses)")
    print("=====================================================================")
    
    # 5 Sample test runs
    for i, seed_val in enumerate([101, 777, 999, 2026, 8888]):
        res = run_single_2000_round_session(seed=seed_val)
        print(f"\n--- 🧪 TEST RUN #{i+1} (Seed {seed_val}) ---")
        print(f"  • Total Rounds Played    : {res['rounds_completed']} / 2000")
        print(f"  • Flat Win Rate          : {res['win_rate']:.2f}% ({res['wins']}W / {res['losses']}L)")
        print(f"  • Max Win Streak         : {res['max_win_streak']} consecutive wins")
        print(f"  • Max Loss Streak        : {res['max_loss_streak']} consecutive losses")
        print(f"  • 🏔️ HIGHEST PEAK BALANCE: ₹{res['peak_balance']:.2f} (Reached at Round {res['peak_round']})")
        if res['bust_round']:
            print(f"  • 💥 BUSTED AT ROUND     : Round {res['bust_round']}")
        else:
            print(f"  • 🏆 SURVIVED ALL 2,000! : Final Balance ₹{res['final_balance']:.2f}")
            
        print(f"  • 📊 Balance Milestones  :")
        for rnd, bal in sorted(res['milestones'].items()):
            print(f"      Round {rnd:4d}: ₹{bal:8.2f}")
            
    # Aggregate Monte Carlo across 1,000 sessions of 2,000 rounds
    print("\n\n=====================================================================")
    print("📈 AGGREGATE MONTE CARLO ANALYSIS (1,000 PLAYERS x 2,000 ROUNDS)")
    print("=====================================================================")
    mc_results = run_monte_carlo_2000_rounds(1000)
    
    busted = [r for r in mc_results if r['busted']]
    survived = [r for r in mc_results if not r['busted']]
    bust_rounds = [r['bust_round'] for r in busted]
    peak_balances = [r['peak_balance'] for r in mc_results]
    peak_rounds = [r['peak_round'] for r in mc_results]
    
    print(f"Total 2,000-Round Simulations : 1,000")
    print(f"Players who Survived all 2,000: {len(survived)/10:.1f}% ({len(survived)}/1000)")
    print(f"Players who Busted before 2,000: {len(busted)/10:.1f}% ({len(busted)}/1000)")
    
    print(f"\n🏔️ PEAK BALANCE STATISTICS (All Players):")
    print(f"  • Average Peak Balance Reached : ₹{np.mean(peak_balances):.2f}")
    print(f"  • Median Peak Balance Reached  : ₹{np.median(peak_balances):.2f}")
    print(f"  • Highest Record Peak Reached  : ₹{np.max(peak_balances):.2f}")
    print(f"  • Average Round of Peak        : Round {np.mean(peak_rounds):.1f}")
    print(f"  • Median Round of Peak         : Round {np.median(peak_rounds):.0f}")
    
    if bust_rounds:
        print(f"\n💥 BUST ROUND STATISTICS (For Busted Players):")
        print(f"  • Average Round of Bust        : Round {np.mean(bust_rounds):.1f}")
        print(f"  • Median Round of Bust         : Round {np.median(bust_rounds):.0f}")
        print(f"  • Earliest Bust (Extreme Bad Luck): Round {np.min(bust_rounds)}")
        print(f"  • Latest Bust                  : Round {np.max(bust_rounds)}")
        
    print(f"\n📊 SURVIVAL PROBABILITY BY ROUND MILESTONE (₹500 Balance / ₹2 Bet):")
    for m in [50, 100, 200, 300, 500, 750, 1000, 1500, 2000]:
        surv_m = sum(1 for r in mc_results if r['rounds_played'] >= m)
        print(f"  • Round {m:4d} : {surv_m/10:5.1f}% of players still alive")
        
    print(f"\n🎯 TARGET HIT PROBABILITIES (₹500 Initial Bankroll):")
    for target in [750, 1000, 1500, 2000, 3000]:
        hit_target = sum(1 for r in mc_results if r['peak_balance'] >= target)
        print(f"  • Hit ₹{target:4d} ({target/500:.1f}x profit) : {hit_target/10:5.1f}% chance")
