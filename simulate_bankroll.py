"""
Monte Carlo Bankroll Simulation for WinGo Strategy
Initial Balance: ₹300
Base Bet: ₹3
Progression: Martingale with +1 increment (3 -> 7 -> 15 -> 31 -> 63 -> 127 -> 255...)
Win Payout: 1.96x (Standard 2% platform commission on WinGo)
Strategy: APEX NEURAL CONSENSUS (ANH-7) (~58% flat win rate on trending market, 50% on pure random)
"""

import random
import numpy as np
from test_deep_analysis import generate_market_data, algo_apex_v4, algo_random

def run_single_session(start_balance=300, base_bet=3, strategy_fn=algo_apex_v4, market_data=None, max_rounds=5000):
    balance = float(start_balance)
    peak_balance = float(start_balance)
    peak_round = 0
    
    # Progression levels: 3, 7, 15, 31, 63, 127, 255...
    # (Or 3, 7, 14, 28, 56, 112, 224...)
    bet_seq = [3, 7, 15, 31, 63, 127, 255]
    step = 0
    
    history = []
    rounds_played = 0
    bust_round = None
    
    for r_idx in range(len(market_data)):
        if balance <= 0:
            bust_round = r_idx
            break
            
        if r_idx >= max_rounds:
            break
            
        current_bet = bet_seq[step] if step < len(bet_seq) else bet_seq[-1]
        
        # If remaining balance is less than required bet, bet all remaining
        if current_bet > balance:
            current_bet = balance
            
        history_slice = market_data[max(0, r_idx-40):r_idx]
        if len(history_slice) < 3:
            pred_size = 'BIG'
        else:
            pred_size, _, _ = strategy_fn(history_slice)
            
        actual = market_data[r_idx]
        won = (pred_size == actual['size'])
        rounds_played += 1
        
        if won:
            # Win payout: Bet * 1.96 (profit is current_bet * 0.96)
            profit = current_bet * 0.96
            balance += profit
            step = 0  # Reset to Level 1
        else:
            balance -= current_bet
            step += 1 # Advance to next martingale level
            
        if balance > peak_balance:
            peak_balance = balance
            peak_round = rounds_played
            
        if balance < 1.0: # Bust
            bust_round = rounds_played
            break
            
    return {
        'rounds_played': rounds_played,
        'bust_round': bust_round,
        'busted': bust_round is not None,
        'final_balance': max(0.0, balance),
        'peak_balance': peak_balance,
        'peak_round': peak_round
    }

def simulate_monte_carlo(n_sessions=1000, strategy_name="APEX NEURAL", strategy_fn=algo_apex_v4):
    print(f"\n=======================================================")
    print(f"🎲 RUNNING {n_sessions} SESSIONS SIMULATION FOR: {strategy_name}")
    print(f"💰 Starting Balance: ₹300 | Base Bet: ₹3 | Payout: 1.96x")
    print(f"=======================================================")
    
    # Pre-generate market streams
    results = []
    
    # We will simulate multiple different player sessions
    for i in range(n_sessions):
        market = generate_market_data(n_rounds=2000, seed=10000 + i)
        res = run_single_session(start_balance=300, base_bet=3, strategy_fn=strategy_fn, market_data=market, max_rounds=2000)
        results.append(res)
        
    busted_sessions = [r for r in results if r['busted']]
    survived_sessions = [r for r in results if not r['busted']]
    
    bust_rounds = [r['bust_round'] for r in busted_sessions]
    peak_balances = [r['peak_balance'] for r in results]
    peak_rounds = [r['peak_round'] for r in results]
    
    doubled_count = sum(1 for r in results if r['peak_balance'] >= 600)
    hit_500_count = sum(1 for r in results if r['peak_balance'] >= 500)
    hit_400_count = sum(1 for r in results if r['peak_balance'] >= 400)
    
    print(f"Total Sessions Tested: {n_sessions}")
    print(f"Bust Rate (playing 2,000 continuous rounds): {len(busted_sessions)/n_sessions*100:.1f}% ({len(busted_sessions)}/{n_sessions})")
    print(f"Survival Rate (after 2,000 rounds): {len(survived_sessions)/n_sessions*100:.1f}%\n")
    
    if bust_rounds:
        print(f"📉 BUST ANALYSIS (When money runs out):")
        print(f"  • Average Rounds to Bust : {np.mean(bust_rounds):.1f} rounds")
        print(f"  • Median Rounds to Bust  : {np.median(bust_rounds):.0f} rounds")
        print(f"  • Fastest Bust (Worst Run): Round {np.min(bust_rounds)}")
        print(f"  • Longest Survival before Bust: Round {np.max(bust_rounds)}")
        
    print(f"\n📈 PEAK PROFIT ANALYSIS (Highest Balance Reached):")
    print(f"  • Average Peak Balance    : ₹{np.mean(peak_balances):.2f}")
    print(f"  • Highest Peak Achieved   : ₹{np.max(peak_balances):.2f}")
    print(f"  • Average Round of Peak   : Round {np.mean(peak_rounds):.1f}")
    print(f"  • Median Round of Peak    : Round {np.median(peak_rounds):.0f}")
    
    print(f"\n🎯 TARGET HIT PROBABILITIES (If you stop at a target):")
    print(f"  • Hit ₹400 (+33% Profit) : {hit_400_count/n_sessions*100:.1f}% chance")
    print(f"  • Hit ₹500 (+66% Profit) : {hit_500_count/n_sessions*100:.1f}% chance")
    print(f"  • Hit ₹600 (2x Double)   : {doubled_count/n_sessions*100:.1f}% chance")
    
    return results

if __name__ == '__main__':
    # Test Random vs APEX
    simulate_monte_carlo(n_sessions=500, strategy_name="Pure Random Baseline", strategy_fn=algo_random)
    simulate_monte_carlo(n_sessions=500, strategy_name="🔥 APEX NEURAL ANH-7", strategy_fn=algo_apex_v4)
