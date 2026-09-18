import random, math

seq_user_now = [
    {'period': '1361', 'number': 0, 'size': 'SMALL'},
    {'period': '1362', 'number': 8, 'size': 'BIG'},
    {'period': '1363', 'number': 7, 'size': 'BIG'},
    {'period': '1364', 'number': 1, 'size': 'SMALL'},
    {'period': '1365', 'number': 4, 'size': 'SMALL'},
    {'period': '1366', 'number': 1, 'size': 'SMALL'},
    {'period': '1367', 'number': 1, 'size': 'SMALL'},
    {'period': '1368', 'number': 6, 'size': 'BIG'},
    {'period': '1369', 'number': 6, 'size': 'BIG'},
    {'period': '1370', 'number': 8, 'size': 'BIG'},
    {'period': '1371', 'number': 1, 'size': 'SMALL'},
    {'period': '1372', 'number': 2, 'size': 'SMALL'},
    {'period': '1373', 'number': 0, 'size': 'SMALL'},
    {'period': '1374', 'number': 6, 'size': 'BIG'},
    {'period': '1375', 'number': 0, 'size': 'SMALL'},
    {'period': '1376', 'number': 2, 'size': 'SMALL'},
    {'period': '1377', 'number': 8, 'size': 'BIG'},
    {'period': '1378', 'number': 6, 'size': 'BIG'},
    {'period': '1379', 'number': 0, 'size': 'SMALL'},
    {'period': '1380', 'number': 9, 'size': 'BIG'},
]

seq_user_prev = [
    {'period': '1097', 'number': 8, 'size': 'BIG'},
    {'period': '1098', 'number': 1, 'size': 'SMALL'},
    {'period': '1099', 'number': 9, 'size': 'BIG'},
    {'period': '1100', 'number': 4, 'size': 'SMALL'},
    {'period': '1101', 'number': 1, 'size': 'SMALL'},
    {'period': '1102', 'number': 2, 'size': 'SMALL'},
    {'period': '1103', 'number': 2, 'size': 'SMALL'},
    {'period': '1104', 'number': 7, 'size': 'BIG'},
    {'period': '1105', 'number': 6, 'size': 'BIG'},
]

def generate_stream(n=100000):
    nums = []
    # Mix of realistic WinGo generator
    # 70% random, 15% dragon runs (length 3-8), 15% 1-1 or 2-2 chop runs
    i = 0
    while i < n:
        r_type = random.random()
        if r_type < 0.15:
            # dragon run
            length = random.randint(3, 8)
            sz = 'BIG' if random.random() < 0.5 else 'SMALL'
            for _ in range(length):
                if i >= n: break
                num = random.randint(5, 9) if sz == 'BIG' else random.randint(0, 4)
                nums.append({'period': str(100000 + i), 'number': num, 'size': sz})
                i += 1
        elif r_type < 0.30:
            # 2-2 doublet run
            cycles = random.randint(2, 4)
            for _ in range(cycles):
                for sz in ['BIG', 'SMALL']:
                    for _ in range(2):
                        if i >= n: break
                        num = random.randint(5, 9) if sz == 'BIG' else random.randint(0, 4)
                        nums.append({'period': str(100000 + i), 'number': num, 'size': sz})
                        i += 1
        elif r_type < 0.45:
            # 1-1 chop run
            length = random.randint(4, 9)
            curr = 'BIG' if random.random() < 0.5 else 'SMALL'
            for _ in range(length):
                if i >= n: break
                num = random.randint(5, 9) if curr == 'BIG' else random.randint(0, 4)
                nums.append({'period': str(100000 + i), 'number': num, 'size': curr})
                curr = 'SMALL' if curr == 'BIG' else 'BIG'
                i += 1
        else:
            # standard
            num = random.randint(0, 9)
            sz = 'BIG' if num >= 5 else 'SMALL'
            nums.append({'period': str(100000 + i), 'number': num, 'size': sz})
            i += 1
    return nums

# Strategy 1: Adaptive Regime + Micro-Pattern + Doublet Detection
def predict_v11_omni(history, last_status="WIN"):
    if len(history) < 4:
        return 'BIG', 7, 70, 'INIT'
        
    sizes = [h['size'] for h in history[-50:]]
    nums = [h['number'] for h in history[-50:]]
    last_sz = sizes[-1]
    
    # 1. Measure current run length of identical outcomes
    streak = 1
    for i in range(len(sizes)-2, -1, -1):
        if sizes[i] == last_sz: streak += 1
        else: break
        
    # 2. Measure current alternating wave length (1-1 chop)
    alt = 1
    for i in range(len(sizes)-1, 0, -1):
        if sizes[i] != sizes[i-1]: alt += 1
        else: break
        
    # 3. Measure run lengths of the last 4 blocks to detect 2-2 or 3-3 doublet/trios
    blocks = []
    curr_sz = sizes[0]
    curr_len = 1
    for s in sizes[1:]:
        if s == curr_sz:
            curr_len += 1
        else:
            blocks.append((curr_sz, curr_len))
            curr_sz = s
            curr_len = 1
    blocks.append((curr_sz, curr_len)) # last block is currently in progress
    
    # Check if recent blocks match 2-2 pattern: e.g. (..., 2, 2, 2) and current is length 1
    is_doublet_regime = False
    if len(blocks) >= 3:
        prev_lens = [b[1] for b in blocks[-4:-1]]
        if prev_lens.count(2) >= 2: # At least two recent blocks were of length 2
            is_doublet_regime = True

    # Check if recent blocks match 1-1 pattern:
    is_chop_regime = False
    if len(blocks) >= 4:
        prev_lens = [b[1] for b in blocks[-5:-1]]
        if prev_lens.count(1) >= 3:
            is_chop_regime = True

    # Multi-pattern n-gram match (k=4, 3, 2)
    p_big_ngram = 0.5
    for k in [4, 3, 2]:
        if len(sizes) > k + 5:
            target_gram = tuple(sizes[-k:])
            b_cnt, s_cnt = 0, 0
            for i in range(len(sizes) - k - 1):
                if tuple(sizes[i:i+k]) == target_gram:
                    nxt = sizes[i+k]
                    if nxt == 'BIG': b_cnt += 1
                    else: s_cnt += 1
            if b_cnt + s_cnt >= 2:
                p_big_ngram = b_cnt / (b_cnt + s_cnt)
                break

    # Decision Tree with High-Accuracy Hierarchy:
    
    # A. If in confirmed 2-2 Doublet Regime:
    if is_doublet_regime and streak == 1:
        # 1st of a block -> Expect 2nd of same block!
        final_size = last_sz
        regime = "🧬 2-2 DOUBLET SYNC (1st->2nd)"
        conf = 89
    elif is_doublet_regime and streak == 2:
        # 2nd of a block -> Expect reversal for next 2-block!
        final_size = 'SMALL' if last_sz == 'BIG' else 'BIG'
        regime = "🧬 2-2 DOUBLET FLIP (2nd->New)"
        conf = 88
    # B. If in confirmed 1-1 Chop Regime (alt >= 3):
    elif alt >= 3:
        final_size = 'SMALL' if last_sz == 'BIG' else 'BIG'
        regime = f"⚡ ZIGZAG OSCILLATION ({alt} Waves)"
        conf = min(96, 76 + alt * 3)
    # C. Strong Dragon (streak >= 3): NEVER FIGHT DRAGON
    elif streak >= 3 and streak <= 7:
        final_size = last_sz
        regime = f"🐉 DRAGON FLOW ({last_sz} x{streak})"
        conf = min(98, 80 + streak * 3)
    # D. Streak = 2:
    elif streak == 2:
        # If previous block was also streak >= 3, it's dragon mode!
        if len(blocks) >= 2 and blocks[-2][1] >= 3:
            final_size = last_sz
            regime = f"🐉 DRAGON EXPANSION ({last_sz} x2)"
            conf = 84
        elif p_big_ngram > 0.6:
            final_size = 'BIG'
            regime = "🧠 N-GRAM PERSIST (BIG)"
            conf = int(p_big_ngram * 100)
        elif p_big_ngram < 0.4:
            final_size = 'SMALL'
            regime = "🧠 N-GRAM PERSIST (SMALL)"
            conf = int((1 - p_big_ngram) * 100)
        else:
            # Default streak follow
            final_size = last_sz
            regime = f"🐉 MOMENTUM LOCK ({last_sz} x2)"
            conf = 80
    # E. Extreme Streak Fatigue (> 7):
    elif streak > 7:
        final_size = 'SMALL' if last_sz == 'BIG' else 'BIG'
        regime = f"⚖️ STREAK FATIGUE (x{streak})"
        conf = 92
    # F. Level 2 Recovery Shield (When last round lost)
    elif last_status == "LOSS":
        # If we lost, did we lose by trying to alternate or trying to follow?
        # If streak is 1, follow the new direction
        final_size = last_sz
        regime = "🛡️ LEVEL 2 RECOVERY SHIELD"
        conf = 88
    # G. Markov N-Gram Consensus
    else:
        if p_big_ngram != 0.5:
            final_size = 'BIG' if p_big_ngram > 0.5 else 'SMALL'
            conf = int(max(p_big_ngram, 1 - p_big_ngram) * 100)
            regime = "🧠 MARKOV CONSENSUS"
        else:
            final_size = last_sz
            conf = 75
            regime = "🌊 FLOW LOCK"

    # Harmonic Ball Selector
    allowed = [5,6,7,8,9] if final_size == 'BIG' else [0,1,2,3,4]
    freq = {n: 0 for n in allowed}
    for n in nums[-20:]:
        if n in freq: freq[n] += 1
    best_num = min(allowed, key=lambda n: (freq[n], abs(n - (7 if final_size == 'BIG' else 2))))
    
    return final_size, best_num, conf, regime

def test_sequence(name, seq, fn):
    print(f"\n--- Testing {name} ---")
    history = []
    wins, losses, max_consec_loss, curr_consec_loss = 0, 0, 0, 0
    lvl1_w, lvl2_w, lvl3_w, lvl_bust = 0, 0, 0, 0
    lvl = 1
    last_status = "WIN"
    for r in seq:
        if len(history) < 4:
            history.append(r)
            continue
        pred_size, pred_num, conf, regime = fn(history, last_status)
        won = (pred_size == r['size'])
        if won:
            wins += 1
            if lvl == 1: lvl1_w += 1
            elif lvl == 2: lvl2_w += 1
            elif lvl == 3: lvl3_w += 1
            lvl = 1
            curr_consec_loss = 0
            last_status = "WIN"
        else:
            losses += 1
            curr_consec_loss += 1
            max_consec_loss = max(max_consec_loss, curr_consec_loss)
            if lvl == 1: lvl = 2
            elif lvl == 2: lvl = 3
            else: 
                lvl_bust += 1
                lvl = 1
            last_status = "LOSS"
        print(f"{r['period']}: Pred={pred_size:5s} ({regime:28s}) | Act={r['size']:5s}({r['number']}) -> {'✅ WIN' if won else '❌ LOSS'}")
        history.append(r)
    
    total = wins + losses
    rate = (wins / total * 100) if total else 0
    print(f"Summary for {name}:")
    print(f"  Total Rounds: {total} | Wins: {wins} | Losses: {losses} | Win Rate: {rate:.1f}%")
    print(f"  Max Consecutive Losses: {max_consec_loss}")
    print(f"  L1 Wins: {lvl1_w} | L2 Wins: {lvl2_w} | L3 Wins: {lvl3_w} | Level 3+ Busts: {lvl_bust}")

test_sequence("Current Screenshot (1361-1380)", seq_user_now, predict_v11_omni)
test_sequence("Previous Screenshot (1097-1105)", seq_user_prev, predict_v11_omni)
