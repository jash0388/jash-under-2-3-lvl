from collections import Counter
import itertools

seqs = {
    '1M_latest_10825_10845': [
        {'period': '10825', 'number': 8, 'size': 'BIG'},
        {'period': '10826', 'number': 6, 'size': 'BIG'},
        {'period': '10827', 'number': 5, 'size': 'BIG'},
        {'period': '10828', 'number': 6, 'size': 'BIG'},
        {'period': '10829', 'number': 8, 'size': 'BIG'},
        {'period': '10830', 'number': 3, 'size': 'SMALL'},
        {'period': '10831', 'number': 2, 'size': 'SMALL'},
        {'period': '10832', 'number': 2, 'size': 'SMALL'},
        {'period': '10833', 'number': 3, 'size': 'SMALL'},
        {'period': '10834', 'number': 2, 'size': 'SMALL'},
        {'period': '10835', 'number': 9, 'size': 'BIG'},
        {'period': '10836', 'number': 1, 'size': 'SMALL'},
        {'period': '10837', 'number': 5, 'size': 'BIG'},
        {'period': '10838', 'number': 6, 'size': 'BIG'},
        {'period': '10839', 'number': 1, 'size': 'SMALL'},
        {'period': '10840', 'number': 4, 'size': 'SMALL'},
        {'period': '10841', 'number': 5, 'size': 'BIG'},
        {'period': '10842', 'number': 4, 'size': 'SMALL'},
        {'period': '10843', 'number': 8, 'size': 'BIG'},
        {'period': '10844', 'number': 5, 'size': 'BIG'},
        {'period': '10845', 'number': 4, 'size': 'SMALL'},
    ],
    '1M_prev_10722_10741': [
        {'period': '10722', 'number': 0, 'size': 'SMALL'},
        {'period': '10723', 'number': 5, 'size': 'BIG'},
        {'period': '10724', 'number': 2, 'size': 'SMALL'},
        {'period': '10725', 'number': 5, 'size': 'BIG'},
        {'period': '10726', 'number': 6, 'size': 'BIG'},
        {'period': '10727', 'number': 0, 'size': 'SMALL'},
        {'period': '10728', 'number': 3, 'size': 'SMALL'},
        {'period': '10729', 'number': 8, 'size': 'BIG'},
        {'period': '10730', 'number': 0, 'size': 'SMALL'},
        {'period': '10731', 'number': 5, 'size': 'BIG'},
        {'period': '10732', 'number': 7, 'size': 'BIG'},
        {'period': '10733', 'number': 2, 'size': 'SMALL'},
        {'period': '10734', 'number': 5, 'size': 'BIG'},
        {'period': '10735', 'number': 2, 'size': 'SMALL'},
        {'period': '10736', 'number': 0, 'size': 'SMALL'},
        {'period': '10737', 'number': 1, 'size': 'SMALL'},
        {'period': '10738', 'number': 5, 'size': 'BIG'},
        {'period': '10739', 'number': 2, 'size': 'SMALL'},
        {'period': '10740', 'number': 1, 'size': 'SMALL'},
        {'period': '10741', 'number': 9, 'size': 'BIG'},
    ],
    '30S_latest_1406_1417': [
        {'period': '1406', 'number': 4, 'size': 'SMALL'},
        {'period': '1407', 'number': 9, 'size': 'BIG'},
        {'period': '1408', 'number': 6, 'size': 'BIG'},
        {'period': '1409', 'number': 9, 'size': 'BIG'},
        {'period': '1410', 'number': 9, 'size': 'BIG'},
        {'period': '1411', 'number': 9, 'size': 'BIG'},
        {'period': '1412', 'number': 3, 'size': 'SMALL'},
        {'period': '1413', 'number': 5, 'size': 'BIG'},
        {'period': '1414', 'number': 2, 'size': 'SMALL'},
        {'period': '1415', 'number': 3, 'size': 'SMALL'},
        {'period': '1416', 'number': 4, 'size': 'SMALL'},
        {'period': '1417', 'number': 5, 'size': 'BIG'},
    ],
    '30S_1361_1384': [
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
        {'period': '1381', 'number': 3, 'size': 'SMALL'},
        {'period': '1382', 'number': 7, 'size': 'BIG'},
        {'period': '1383', 'number': 5, 'size': 'BIG'},
        {'period': '1384', 'number': 0, 'size': 'SMALL'},
    ]
}

def get_runs(sizes):
    runs = []
    curr = sizes[0]
    l = 1
    for s in sizes[1:]:
        if s == curr: l += 1
        else:
            runs.append((curr, l))
            curr = s
            l = 1
    runs.append((curr, l))
    return runs

def opp(s): return 'SMALL' if s == 'BIG' else 'BIG'

# Let's write a generator of strategies
def evaluate(pred_func):
    total_busts = 0
    total_max_streak = 0
    total_wins = 0
    total_rounds = 0
    
    for name, seq in seqs.items():
        hist = []
        loss_streak = 0
        max_s = 0
        wins = 0
        busts = 0
        for r in seq:
            if len(hist) < 3:
                hist.append(r)
                continue
            pred = pred_func(hist, loss_streak)
            if pred == r['size']:
                wins += 1
                loss_streak = 0
            else:
                loss_streak += 1
                max_s = max(max_s, loss_streak)
                if loss_streak > 2:
                    busts += 1
                    loss_streak = 0
            hist.append(r)
        total_busts += busts
        total_max_streak = max(total_max_streak, max_s)
        total_wins += wins
        total_rounds += (len(seq) - 3)
    return total_busts, total_max_streak, total_wins / total_rounds

# Strategy template
# In Level 3 (loss_streak >= 2):
# We need to test all possible combinations of (action when curr_len>=3, action when curr_len==2, action when curr_len==1 and prev_len==2, action when curr_len==1 and alt>=3, action default)
actions = ['SAME', 'OPP']

best_result = None

for l3_dragon in actions:
    for l3_doublet in actions:
        for l3_pair in actions:
            for l3_chop in actions:
                for l3_def in actions:
                    for l2_dragon in actions:
                        for l2_doublet in actions:
                            for l2_pair in actions:
                                for l2_chop in actions:
                                    for l2_def in actions:
                                        for l1_dragon in actions:
                                            for l1_doublet in actions:
                                                for l1_pair in actions:
                                                    for l1_chop in actions:
                                                        for l1_def in actions:
                                                            def make_f(l3_dr=l3_dragon, l3_db=l3_doublet, l3_p=l3_pair, l3_ch=l3_chop, l3_df=l3_def,
                                                                       l2_dr=l2_dragon, l2_db=l2_doublet, l2_p=l2_pair, l2_ch=l2_chop, l2_df=l2_def,
                                                                       l1_dr=l1_dragon, l1_db=l1_doublet, l1_p=l1_pair, l1_ch=l1_chop, l1_df=l1_def):
                                                                def fn(hist, loss_streak):
                                                                    sizes = [h['size'] for h in hist[-30:]]
                                                                    last = sizes[-1]
                                                                    runs = get_runs(sizes)
                                                                    curr_s, curr_l = runs[-1]
                                                                    prev_l = runs[-2][1] if len(runs) >= 2 else 1
                                                                    alt = 0
                                                                    for s, l in reversed(runs):
                                                                        if l == 1: alt += 1
                                                                        else: break
                                                                        
                                                                    def act(rule):
                                                                        return last if rule == 'SAME' else opp(last)
                                                                        
                                                                    if loss_streak >= 2:
                                                                        if curr_l >= 3: return act(l3_dr)
                                                                        elif curr_l == 2: return act(l3_db)
                                                                        elif curr_l == 1 and prev_l == 2: return act(l3_p)
                                                                        elif curr_l == 1 and alt >= 3: return act(l3_ch)
                                                                        else: return act(l3_df)
                                                                    elif loss_streak == 1:
                                                                        if curr_l >= 3: return act(l2_dr)
                                                                        elif curr_l == 2: return act(l2_db)
                                                                        elif curr_l == 1 and prev_l == 2: return act(l2_p)
                                                                        elif curr_l == 1 and alt >= 3: return act(l2_ch)
                                                                        else: return act(l2_df)
                                                                    else:
                                                                        if curr_l >= 3:
                                                                            if curr_l > 7: return opp(last)
                                                                            return act(l1_dr)
                                                                        elif curr_l == 2: return act(l1_db)
                                                                        elif curr_l == 1 and prev_l == 2: return act(l1_p)
                                                                        elif curr_l == 1 and alt >= 3: return act(l1_ch)
                                                                        else: return act(l1_df)
                                                                return fn
                                                            
                                                            f = make_f()
                                                            busts, max_s, wr = evaluate(f)
                                                            if busts == 0:
                                                                if best_result is None or wr > best_result['wr']:
                                                                    best_result = {
                                                                        'busts': busts,
                                                                        'max_s': max_s,
                                                                        'wr': wr,
                                                                        'config': (l3_dragon, l3_doublet, l3_pair, l3_chop, l3_def,
                                                                                   l2_dragon, l2_doublet, l2_pair, l2_chop, l2_def,
                                                                                   l1_dragon, l1_doublet, l1_pair, l1_chop, l1_def)
                                                                    }

print('Search complete!')
if best_result:
    print(f"FOUND ZERO BUST STRATEGY! Max Streak = {best_result['max_s']}, Overall Win Rate = {best_result['wr']*100:.2f}%")
    print(f"Config: {best_result['config']}")
else:
    print("No 0 bust config found in strict discrete search.")
