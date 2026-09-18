import time
from research_500k_rounds import generate_massive_wingo_stream

def strat_apex_ultra_titan(history):
    if len(history) < 6:
        return 'BIG'
        
    sizes = [h['size'] for h in history[-80:]]
    nums = [h['number'] for h in history[-80:]]
    
    # 1. Multi-Order Markov with Laplace Smoothing
    # Order 3:
    k3 = (sizes[-3], sizes[-2], sizes[-1])
    b3, s3 = 1.0, 1.0
    for i in range(len(sizes) - 3):
        if (sizes[i], sizes[i+1], sizes[i+2]) == k3:
            w = 1.0 + (i / len(sizes))
            if sizes[i+3] == 'BIG': b3 += w * 2.0
            else: s3 += w * 2.0
            
    # Order 2:
    k2 = (sizes[-2], sizes[-1])
    b2, s2 = 1.0, 1.0
    for i in range(len(sizes) - 2):
        if (sizes[i], sizes[i+1]) == k2:
            w = 1.0 + (i / len(sizes))
            if sizes[i+2] == 'BIG': b2 += w * 1.5
            else: s2 += w * 1.5
            
    # Order 1 (Streak length & persistence):
    last_size = sizes[-1]
    streak = 1
    for i in range(len(sizes)-2, -1, -1):
        if sizes[i] == last_size: streak += 1
        else: break
        
    # Alternation length:
    alt = 1
    for i in range(len(sizes)-1, 0, -1):
        if sizes[i] != sizes[i-1]: alt += 1
        else: break

    # Score synthesis
    p_b3 = b3 / (b3 + s3)
    p_s3 = s3 / (b3 + s3)
    p_b2 = b2 / (b2 + s2)
    p_s2 = s2 / (b2 + s2)
    
    score_b = p_b3 * 3.0 + p_b2 * 2.0
    score_s = p_s3 * 3.0 + p_s2 * 2.0
    
    # Streak & Wave overlays:
    if 3 <= streak <= 6:
        if last_size == 'BIG': score_b += 2.0
        else: score_s += 2.0
    elif streak > 6:
        if last_size == 'BIG': score_s += 2.2
        else: score_b += 2.2
        
    if alt >= 3:
        target = 'SMALL' if last_size == 'BIG' else 'BIG'
        if target == 'BIG': score_b += 2.2
        else: score_s += 2.2

    return 'BIG' if score_b >= score_s else 'SMALL'

stream = generate_massive_wingo_stream(500000, seed=888)

flat_wins = 0
total_rounds = len(stream) - 40

l2_wins, l2_cycles = 0, 0
l3_wins, l3_cycles = 0, 0
l2_step = 1
l3_step = 1

t0 = time.time()
for i in range(40, len(stream)):
    history_slice = stream[max(0, i-60):i]
    actual = stream[i]['size']
    pred = strat_apex_ultra_titan(history_slice)
    won = (pred == actual)
    
    if won: flat_wins += 1
    
    if l2_step == 1:
        if won: l2_wins += 1; l2_cycles += 1; l2_step = 1
        else: l2_step = 2
    elif l2_step == 2:
        l2_cycles += 1
        if won: l2_wins += 1
        l2_step = 1
        
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

print(f"APEX ULTRA TITAN on 500,000 Rounds:")
print(f"Flat Win Rate : {flat_wins/total_rounds*100:.2f}%")
print(f"2-Level Win Rate (1x-3x): {l2_wins/l2_cycles*100:.2f}%")
print(f"3-Level Win Rate (1x-3x-9x): {l3_wins/l3_cycles*100:.2f}%")
print(f"Speed: {time.time()-t0:.2f}s")
