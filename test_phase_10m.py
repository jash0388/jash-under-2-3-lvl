"""
Testing Phase Density Discriminator on 10,000,000 Rounds
"""

import random
import numpy as np
import time
from collections import defaultdict

def test_phase_density_10M(seed=42):
    random.seed(seed)
    n_rounds = 10000000
    
    flat_wins = 0
    l2_wins, l2_cycles = 0, 0
    l3_wins, l3_cycles = 0, 0
    l2_step = 1
    l3_step = 1
    
    history_sizes = []
    loss_streak = 0
    
    regimes = [0, 1, 2, 3, 4]
    regime_weights = [0.35, 0.25, 0.25, 0.10, 0.05]
    curr_regime = 0
    regime_len = 0
    curr_size = 1
    
    t0 = time.time()
    
    for r in range(n_rounds):
        if regime_len <= 0:
            curr_regime = random.choices(regimes, weights=regime_weights)[0]
            regime_len = random.randint(3, 15)
        regime_len -= 1
        
        if curr_regime == 0: actual = random.randint(0, 1)
        elif curr_regime == 1: actual = curr_size if random.random() < 0.80 else 1 - curr_size
        elif curr_regime == 2: actual = (1 - curr_size) if random.random() < 0.82 else curr_size
        elif curr_regime == 3: actual = 1 if ((r // 2) % 2 == 0) else 0; actual = (1-actual) if random.random() < 0.20 else actual
        else: actual = 1 if random.random() < 0.70 else 0
        curr_size = actual
        
        if len(history_sizes) < 10:
            pred = 1
        else:
            last_s = history_sizes[-1]
            
            # 1. Streak Length
            stk = 1
            for k in range(len(history_sizes)-2, max(-1, len(history_sizes)-15), -1):
                if history_sizes[k] == last_s: stk += 1
                else: break
                
            # 2. Alternation Length
            alt = 1
            for k in range(len(history_sizes)-1, max(0, len(history_sizes)-15), -1):
                if history_sizes[k] != history_sizes[k-1]: alt += 1
                else: break
                
            # 3. Phase Density in last 20
            # Count alternations vs streaks in last 20
            alts_20 = 0
            for k in range(len(history_sizes)-1, max(0, len(history_sizes)-20), -1):
                if history_sizes[k] != history_sizes[k-1]: alts_20 += 1
                
            is_choppy_phase = alts_20 >= 11 # > 55% alternations
            
            # --- PREDICTION LOGIC ---
            if loss_streak == 1:
                # LEVEL 2 RECOVERY DISCRIMINATOR:
                # If market is in choppy alternating phase -> predict inverse
                # If market is in trending phase -> predict same (dragon continuation)
                if is_choppy_phase:
                    pred = 1 - last_s
                else:
                    pred = last_s
            elif 2 <= stk <= 6:
                pred = last_s # Follow dragon
            elif stk > 6:
                pred = 1 - last_s # Reversal
            elif alt >= 3:
                pred = 1 - last_s # ZigZag wave
            else:
                pred = 1 - last_s if is_choppy_phase else last_s
                
        won = (pred == actual)
        history_sizes.append(actual)
        if len(history_sizes) > 50: history_sizes.pop(0)
        
        if won:
            flat_wins += 1
            loss_streak = 0
        else:
            loss_streak += 1
            
        # 2-Level
        if l2_step == 1:
            if won: l2_wins += 1; l2_cycles += 1; l2_step = 1
            else: l2_step = 2
        elif l2_step == 2:
            l2_cycles += 1
            if won: l2_wins += 1
            l2_step = 1
            
        # 3-Level
        if l3_step == 1:
            if won: l3_wins += 1; l3_cycles += 1; l3_step = 1
            else: l3_step = 2
        elif l3_step == 2:
            if won: l3_wins += 1; l3_cycles += 1; l3_step = 1
            else: l3_step = 3
        elif l3_step == 3:
            l3_cycles += 1
            if won: l3_wins += 1
            l3_step = 1

    print(f"Phase Density Discriminator on 10,000,000 Rounds:")
    print(f"Flat Win Rate  : {flat_wins/n_rounds*100:.3f}% ({flat_wins:,} wins)")
    print(f"2-Level Win Rate: {l2_wins/l2_cycles*100:.3f}% ({l2_wins:,} / {l2_cycles:,} cycles)")
    print(f"3-Level Win Rate: {l3_wins/l3_cycles*100:.3f}% ({l3_wins:,} / {l3_cycles:,} cycles)")
    print(f"Time: {time.time()-t0:.2f}s")

if __name__ == '__main__':
    test_phase_density_10M(seed=123)
