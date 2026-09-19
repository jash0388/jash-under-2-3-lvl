from research_cascade_breaker import all_12_seqs, get_runs, opp
import random

seq_M = [
    {'period': '10785', 'number': 6, 'size': 'BIG'},
    {'period': '10786', 'number': 8, 'size': 'BIG'},
    {'period': '10787', 'number': 1, 'size': 'SMALL'},
    {'period': '10788', 'number': 1, 'size': 'SMALL'},
    {'period': '10789', 'number': 4, 'size': 'SMALL'},
    {'period': '10790', 'number': 4, 'size': 'SMALL'},
    {'period': '10791', 'number': 1, 'size': 'SMALL'},
    {'period': '10792', 'number': 5, 'size': 'BIG'},
    {'period': '10793', 'number': 8, 'size': 'BIG'},
]

all_13_seqs = all_12_seqs + [("Seq M (10785-10793 Screenshot 3)", seq_M)]

def evaluate_suite(predictor_fn):
    total_max = 0
    results = []
    for name, seq in all_13_seqs:
        history = seq[:3]
        streak = 0
        max_streak = 0
        wins, losses = 0, 0
        details = []
        for item in seq[3:]:
            pred, tag = predictor_fn(history, streak)
            act = item['size']
            if pred == act:
                wins += 1
                details.append((item['period'], pred, act, 'WIN', streak + 1, tag))
                streak = 0
            else:
                losses += 1
                streak += 1
                if streak > max_streak:
                    max_streak = streak
                details.append((item['period'], pred, act, 'LOSS', streak, tag))
            history.append(item)
        if max_streak > total_max:
            total_max = max_streak
        results.append((name, wins, losses, max_streak, details))
    return total_max, results

# Let's search across feature configurations
best_models = []
print("Searching for universal engine where max_loss <= 2 on ALL 13 sequences...")

def make_engine(cfg):
    def predict(history, streak):
        sizes = [x['size'] for x in history]
        nums = [x['number'] for x in history]
        runs = get_runs(sizes)
        c_side, c_len = runs[-1]
        p_side, p_len = runs[-2] if len(runs) >= 2 else (opp(c_side), 0)
        p3_side, p3_len = runs[-3] if len(runs) >= 3 else (c_side, 0)
        last_s = sizes[-1]
        last_n = nums[-1]
        prev_n = nums[-2] if len(nums) >= 2 else last_n
        delta = abs(last_n - prev_n)

        alt = 0
        for r_s, r_l in reversed(runs):
            if r_l == 1: alt += 1
            else: break

        # Level 3 Recovery
        if streak >= 2:
            act = cfg.get('l3_default', 'C')
            if c_len >= 4 and 'l3_drag4' in cfg: act = cfg['l3_drag4']
            elif c_len == 3 and 'l3_drag3' in cfg: act = cfg['l3_drag3']
            elif c_len == 2 and 'l3_drag2' in cfg: act = cfg['l3_drag2']
            elif alt >= 3 and 'l3_alt3' in cfg: act = cfg['l3_alt3']
            elif alt >= 2 and 'l3_alt2' in cfg: act = cfg['l3_alt2']
            elif delta >= 5 and 'l3_delta5' in cfg: act = cfg['l3_delta5']
            
        elif streak == 1:
            act = cfg.get('l2_default', 'C')
            if c_len >= 4 and 'l2_drag4' in cfg: act = cfg['l2_drag4']
            elif c_len == 3 and 'l2_drag3' in cfg: act = cfg['l2_drag3']
            elif c_len == 2 and 'l2_drag2' in cfg: act = cfg['l2_drag2']
            elif alt >= 3 and 'l2_alt3' in cfg: act = cfg['l2_alt3']
            elif alt >= 2 and 'l2_alt2' in cfg: act = cfg['l2_alt2']
            elif delta >= 5 and 'l2_delta5' in cfg: act = cfg['l2_delta5']

        else: # L1
            act = cfg.get('l1_default', 'C')
            if c_len == 3 and p_len == 1 and p3_len == 3 and 'l1_trip_cap' in cfg:
                act = cfg['l1_trip_cap']
            elif c_len >= 4 and 'l1_drag4' in cfg: act = cfg['l1_drag4']
            elif c_len == 3 and 'l1_drag3' in cfg: act = cfg['l1_drag3']
            elif c_len == 2 and 'l1_drag2' in cfg: act = cfg['l1_drag2']
            elif alt >= 3 and 'l1_alt3' in cfg: act = cfg['l1_alt3']
            elif alt >= 2 and 'l1_alt2' in cfg: act = cfg['l1_alt2']

        if act == 'C': return c_side, "C"
        elif act == 'O': return opp(c_side), "O"
        elif act == 'P': return p_side, "P"
        elif act == 'OP': return opp(p_side), "OP"
        elif act == 'W':
            w = sizes[-5:]
            b_score = sum(1.5**i for i, s in enumerate(w) if s == "BIG")
            s_score = sum(1.5**i for i, s in enumerate(w) if s == "SMALL")
            if b_score > s_score: return "BIG", "TREND_B"
            elif s_score > b_score: return "SMALL", "TREND_S"
            return last_s, "MOM"
        return last_s, "MOM"

    return predict

random.seed(42)
for i in range(150000):
    cfg = {}
    cfg['l1_default'] = random.choice(['C', 'W'])
    cfg['l1_drag3'] = random.choice(['C', 'O'])
    if random.random() < 0.5: cfg['l1_drag4'] = random.choice(['C', 'O'])
    if random.random() < 0.5: cfg['l1_drag2'] = random.choice(['C', 'O'])
    cfg['l1_alt2'] = random.choice(['O', 'C'])
    cfg['l1_alt3'] = random.choice(['O', 'C'])
    if random.random() < 0.5: cfg['l1_trip_cap'] = random.choice(['C', 'O'])

    cfg['l2_default'] = random.choice(['C', 'O'])
    cfg['l2_drag3'] = random.choice(['C', 'O'])
    if random.random() < 0.5: cfg['l2_drag4'] = random.choice(['C', 'O'])
    if random.random() < 0.5: cfg['l2_drag2'] = random.choice(['C', 'O'])
    cfg['l2_alt2'] = random.choice(['O', 'C'])
    cfg['l2_alt3'] = random.choice(['O', 'C'])
    if random.random() < 0.5: cfg['l2_delta5'] = random.choice(['O', 'C'])

    cfg['l3_default'] = random.choice(['C', 'O'])
    cfg['l3_drag3'] = random.choice(['C', 'O'])
    if random.random() < 0.5: cfg['l3_drag4'] = random.choice(['C', 'O'])
    if random.random() < 0.5: cfg['l3_drag2'] = random.choice(['C', 'O'])
    cfg['l3_alt2'] = random.choice(['O', 'C'])
    cfg['l3_alt3'] = random.choice(['O', 'C'])
    if random.random() < 0.5: cfg['l3_delta5'] = random.choice(['O', 'C'])

    fn = make_engine(cfg)
    tot_max, results = evaluate_suite(fn)
    if tot_max <= 2:
        total_wins = sum(r[1] for r in results)
        total_losses = sum(r[2] for r in results)
        best_models.append((tot_max, total_wins, cfg, results))
        print(f"🏆 FOUND MODEL #{len(best_models)} (iter {i}): Max Loss = {tot_max}, Wins = {total_wins}/{total_wins+total_losses}")
        print(f"CFG = {cfg}")
        if len(best_models) >= 5:
            break

if best_models:
    best_models.sort(key=lambda x: x[1], reverse=True)
    m = best_models[0]
    print("\n" + "="*80)
    print("BEST UNIVERSAL ENGINE DETAILS:")
    print("CFG:", m[2])
    for r in m[3]:
        print(f"  {r[0]}: {r[1]}W/{r[2]}L (max streak: {r[3]})")
else:
    print("No model found in initial random iterations. Expanding search...")
