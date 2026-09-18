import random
import time
import sys

print("======================================================================")
print("   1,000,000 ROUNDS DUAL-DIRECTION (FORWARD & REVERSE) APEX RESEARCH   ")
print("======================================================================")

# 1. Generate 1,000,000 realistic casino WinGo rounds
def generate_million_rounds(total=1000000, seed=42):
    random.seed(seed)
    print(f"Generating {total:,} realistic WinGo rounds (Dragons, Doublets, Chops, Noise)...")
    t0 = time.time()
    
    rounds = []
    curr_size = "BIG"
    run_len = 0
    
    # Realistic casino regime distribution:
    # - 1-1 Chops (lengths 1, 1, 1, 1)
    # - Doublets (lengths 2, 2, 2)
    # - Short Dragons (lengths 3, 4, 5)
    # - Long Dragons (lengths 6, 7, 8, 9, 10, 12)
    regime_lengths = [1]*35 + [2]*25 + [3]*15 + [4]*10 + [5]*6 + [6]*4 + [7]*2 + [8]*1 + [10]*1 + [12]*1
    target_len = random.choice(regime_lengths)
    
    for i in range(1, total + 1):
        if run_len >= target_len:
            curr_size = "SMALL" if curr_size == "BIG" else "BIG"
            run_len = 0
            target_len = random.choice(regime_lengths)
            
        run_len += 1
        
        # Realistic digit generation based on size
        if curr_size == "BIG":
            # 5,6,7,8,9 with natural slight variance
            digit = random.choice([5, 6, 7, 8, 9, 7, 8])
        else:
            # 0,1,2,3,4 with natural slight variance
            digit = random.choice([0, 1, 2, 3, 4, 2, 3])
            
        rounds.append({
            'period': str(i),
            'number': digit,
            'size': curr_size
        })
        
    print(f"Generated {total:,} rounds in {time.time() - t0:.2f}s.")
    return rounds

million_data = generate_million_rounds(1000000)

# Helper functions
def opp(s): return "SMALL" if s == "BIG" else "BIG"

def evaluate_strategy(dataset, name, predict_fn):
    t0 = time.time()
    hist = []
    loss_streak = 0
    max_loss_streak = 0
    wins, losses = 0, 0
    l1_w, l2_w, l3_w, busts = 0, 0, 0, 0
    
    for r in dataset:
        if len(hist) < 3:
            hist.append(r)
            continue
            
        pred, regime = predict_fn(hist, loss_streak)
        won = (pred == r['size'])
        
        if won:
            wins += 1
            if loss_streak == 0: l1_w += 1
            elif loss_streak == 1: l2_w += 1
            elif loss_streak == 2: l3_w += 1
            loss_streak = 0
        else:
            losses += 1
            loss_streak += 1
            max_loss_streak = max(max_loss_streak, loss_streak)
            if loss_streak > 2:
                busts += 1
                loss_streak = 0
                
        hist.append(r)
        if len(hist) > 50:
            hist.pop(0)
            
    total_rounds = wins + losses
    total_cycles = l1_w + l2_w + l3_w + busts
    elapsed = time.time() - t0
    
    return {
        'name': name,
        'rounds': total_rounds,
        'wins': wins,
        'losses': losses,
        'raw_wr': wins / total_rounds * 100,
        'max_loss': max_loss_streak,
        'l1_w': l1_w,
        'l2_w': l2_w,
        'l3_w': l3_w,
        'busts': busts,
        'cycle_wr': (total_cycles - busts) / total_cycles * 100 if total_cycles else 0,
        'time': elapsed
    }

# Benchmark candidates on both Forward and Reverse
def test_candidate_both_ways(pred_fn, name):
    print(f"\nEvaluating '{name}' across 2,000,000 evaluations (1M Forward + 1M Reverse)...")
    res_fwd = evaluate_strategy(million_data, f"{name} (Forward 1 -> 1,000,000)", pred_fn)
    
    # Reverse dataset
    reversed_data = list(reversed(million_data))
    # Re-index period for clarity
    res_rev = evaluate_strategy(reversed_data, f"{name} (Reverse 1,000,000 -> 1)", pred_fn)
    
    print(f"--- {res_fwd['name']} ---")
    print(f"  Raw Win Rate: {res_fwd['raw_wr']:.2f}% | Max Consecutive Losses: {res_fwd['max_loss']}")
    print(f"  L1: {res_fwd['l1_w']:,} ({res_fwd['l1_w']/(res_fwd['l1_w']+res_fwd['l2_w']+res_fwd['l3_w']+res_fwd['busts'])*100:.1f}%) | L2: {res_fwd['l2_w']:,} | L3: {res_fwd['l3_w']:,} | Busts: {res_fwd['busts']:,}")
    print(f"  Cycle Win Rate (Within 3 Levels): {res_fwd['cycle_wr']:.2f}% (Time: {res_fwd['time']:.2f}s)")
    
    print(f"--- {res_rev['name']} ---")
    print(f"  Raw Win Rate: {res_rev['raw_wr']:.2f}% | Max Consecutive Losses: {res_rev['max_loss']}")
    print(f"  L1: {res_rev['l1_w']:,} ({res_rev['l1_w']/(res_rev['l1_w']+res_rev['l2_w']+res_rev['l3_w']+res_rev['busts'])*100:.1f}%) | L2: {res_rev['l2_w']:,} | L3: {res_rev['l3_w']:,} | Busts: {res_rev['busts']:,}")
    print(f"  Cycle Win Rate (Within 3 Levels): {res_rev['cycle_wr']:.2f}% (Time: {res_rev['time']:.2f}s)")
    
    return res_fwd, res_rev

