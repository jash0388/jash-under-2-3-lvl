seq_1m_30 = [
    {'period': str(p), 'number': n, 'size': s} for p, n, s in [
        (10825, 8, 'BIG'), (10826, 6, 'BIG'), (10827, 5, 'BIG'), (10828, 6, 'BIG'), (10829, 8, 'BIG'),
        (10830, 3, 'SMALL'), (10831, 2, 'SMALL'), (10832, 2, 'SMALL'), (10833, 3, 'SMALL'), (10834, 2, 'SMALL'),
        (10835, 9, 'BIG'), (10836, 1, 'SMALL'), (10837, 5, 'BIG'), (10838, 6, 'BIG'), (10839, 1, 'SMALL'),
        (10840, 4, 'SMALL'), (10841, 5, 'BIG'), (10842, 4, 'SMALL'), (10843, 8, 'BIG'), (10844, 5, 'BIG'),
        (10845, 4, 'SMALL'), (10846, 0, 'SMALL'), (10847, 1, 'SMALL'), (10848, 9, 'BIG'), (10849, 5, 'BIG'),
        (10850, 4, 'SMALL'), (10851, 0, 'SMALL'), (10852, 1, 'SMALL'), (10853, 4, 'SMALL'), (10854, 5, 'BIG')
    ]
]

seq_1m = [
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
]

seq_30s_latest = [
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
]

seq_30s_prev1 = [
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

all_seqs = {
    'WinGo 1M Live (10825-10854)': seq_1m_30,
    'WinGo 1M Previous (10722-10741)': seq_1m,
    'WinGo 30S Latest (1406-1417)': seq_30s_latest,
    'WinGo 30S Long (1361-1384)': seq_30s_prev1
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

candidates = []

for l1_streak2 in ['SAME', 'OPP']:
    for l1_chop3 in ['SAME', 'OPP']:
        for l1_def in ['SAME', 'OPP']:
            for l2_policy in ['FOLLOW_LAST', 'FLIP_LAST', 'FOLLOW_DRAGON_ELSE_FLIP', 'FOLLOW_DRAGON_ELSE_SAME']:
                for l3_policy in ['FOLLOW_LAST', 'FLIP_LAST', 'INVERT_FAILING_GUESS', 'PATTERN_CONSENSUS']:
                    
                    def make_engine(l1_s2=l1_streak2, l1_c3=l1_chop3, l1_d=l1_def, l2_p=l2_policy, l3_p=l3_policy):
                        def predict(hist, loss_streak, last_guess=None):
                            sizes = [h['size'] for h in hist[-30:]]
                            last = sizes[-1]
                            runs = get_runs(sizes)
                            curr_l = runs[-1][1]
                            alt = 0
                            for s, l in reversed(runs):
                                if l == 1: alt += 1
                                else: break
                                
                            if loss_streak >= 2:
                                if l3_p == 'FOLLOW_LAST':
                                    return last, 'L3_FOLLOW_LAST'
                                elif l3_p == 'FLIP_LAST':
                                    return opp(last), 'L3_FLIP_LAST'
                                elif l3_p == 'INVERT_FAILING_GUESS':
                                    if last_guess: return opp(last_guess), 'L3_INVERT_GUESS'
                                    return last, 'L3_FOLLOW_LAST'
                                elif l3_p == 'PATTERN_CONSENSUS':
                                    if curr_l >= 2: return last, 'L3_DRAGON'
                                    return opp(last), 'L3_CHOP'
                                    
                            elif loss_streak == 1:
                                if l2_p == 'FOLLOW_LAST': return last, 'L2_FOLLOW'
                                elif l2_p == 'FLIP_LAST': return opp(last), 'L2_FLIP'
                                elif l2_p == 'FOLLOW_DRAGON_ELSE_FLIP':
                                    if curr_l >= 2: return last, 'L2_DRAGON'
                                    return opp(last), 'L2_CHOP'
                                elif l2_p == 'FOLLOW_DRAGON_ELSE_SAME':
                                    return last, 'L2_FOLLOW'
                                    
                            else:
                                if curr_l >= 3:
                                    if curr_l > 7: return opp(last), 'L1_FATIGUE'
                                    return last, 'L1_DRAGON'
                                elif curr_l == 2:
                                    return (last if l1_s2 == 'SAME' else opp(last)), 'L1_STREAK2'
                                elif alt >= 3:
                                    return (last if l1_c3 == 'SAME' else opp(last)), 'L1_CHOP3'
                                else:
                                    return (last if l1_d == 'SAME' else opp(last)), 'L1_DEF'
                        return predict
                    
                    engine = make_engine()
                    total_busts = 0
                    total_max_loss = 0
                    total_wins = 0
                    total_rounds = 0
                    per_data = {}
                    
                    for name, seq in all_seqs.items():
                        hist = []
                        loss_streak = 0
                        max_loss = 0
                        wins = 0
                        busts = 0
                        losses = 0
                        last_guess = None
                        for r in seq:
                            if len(hist) < 3:
                                hist.append(r)
                                continue
                            pred, tag = engine(hist, loss_streak, last_guess)
                            last_guess = pred
                            won = (pred == r['size'])
                            if won:
                                wins += 1
                                loss_streak = 0
                            else:
                                losses += 1
                                loss_streak += 1
                                max_loss = max(max_loss, loss_streak)
                                if loss_streak > 2:
                                    busts += 1
                                    loss_streak = 0
                            hist.append(r)
                        total_busts += busts
                        total_max_loss = max(total_max_loss, max_loss)
                        total_wins += wins
                        rounds = len(seq) - 3
                        total_rounds += rounds
                        per_data[name] = {'busts': busts, 'max_loss': max_loss, 'wr': wins/rounds}
                        
                    if total_busts == 0:
                        candidates.append({
                            'max_loss': total_max_loss,
                            'wr': total_wins / total_rounds,
                            'params': (l1_streak2, l1_chop3, l1_def, l2_policy, l3_policy),
                            'per_data': per_data
                        })

print(f"Search complete! Found {len(candidates)} zero-bust configurations.")
if candidates:
    candidates.sort(key=lambda x: x['wr'], reverse=True)
    best = candidates[0]
    print(f"\n★ BEST CONFIGURATION: Max Loss = {best['max_loss']}, Overall Win Rate = {best['wr']*100:.2f}%")
    print(f"Params: {best['params']}")
    for k, v in best['per_data'].items():
        print(f"  {k}: Max Loss = {v['max_loss']}, Win Rate = {v['wr']*100:.1f}%, Busts = {v['busts']}")
