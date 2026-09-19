from research_cascade_breaker import all_12_seqs, get_runs, opp
import random
import sys

def evaluate(predictor_fn):
    total_max = 0
    results = []
    for name, seq in all_12_seqs:
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
                if streak > max_streak: max_streak = streak
                details.append((item['period'], pred, act, 'LOSS', streak, tag))
            history.append(item)
        total_max = max(total_max, max_streak)
        results.append((name, wins, losses, max_streak, details))
    return total_max, results

def make_custom_engine(params):
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

        # Features dictionary
        # L3 Recovery
        if streak >= 2:
            action = params.get('l3_default', 'C')
            if c_len >= 3 and 'l3_drag3' in params: action = params['l3_drag3']
            elif c_len == 2 and 'l3_drag2' in params: action = params['l3_drag2']
            elif c_len == 1 and p_len == 2 and 'l3_p2c1' in params: action = params['l3_p2c1']
            elif alt >= 3 and 'l3_alt3' in params: action = params['l3_alt3']
            elif alt >= 2 and 'l3_alt2' in params: action = params['l3_alt2']
            elif delta >= 5 and 'l3_delta5' in params: action = params['l3_delta5']
            
        elif streak == 1:
            action = params.get('l2_default', 'C')
            if c_len >= 3 and 'l2_drag3' in params: action = params['l2_drag3']
            elif c_len == 2 and 'l2_drag2' in params: action = params['l2_drag2']
            elif c_len == 1 and p_len == 2 and 'l2_p2c1' in params: action = params['l2_p2c1']
            elif alt >= 3 and 'l2_alt3' in params: action = params['l2_alt3']
            elif alt >= 2 and 'l2_alt2' in params: action = params['l2_alt2']
            elif delta >= 5 and 'l2_delta5' in params: action = params['l2_delta5']

        else: # L1
            action = params.get('l1_default', 'W')
            if c_len == 3 and p_len == 1 and p3_len == 3 and 'l1_trip_cap' in params:
                action = params['l1_trip_cap']
            elif c_len >= 3 and 'l1_drag3' in params: action = params['l1_drag3']
            elif c_len == 2 and 'l1_drag2' in params: action = params['l1_drag2']
            elif c_len == 1 and p_len == 2 and p3_len == 1 and 'l1_p1p2c1' in params:
                action = params['l1_p1p2c1']
            elif c_len == 1 and p_len == 2 and 'l1_p2c1' in params:
                action = params['l1_p2c1']
            elif alt >= 3 and 'l1_alt3' in params: action = params['l1_alt3']
            elif alt >= 2 and 'l1_alt2' in params: action = params['l1_alt2']

        # Map action to side
        if action == 'C': return c_side, f"RULE({action})"
        elif action == 'O': return opp(c_side), f"RULE({action})"
        elif action == 'P': return p_side, f"RULE({action})"
        elif action == 'OP': return opp(p_side), f"RULE({action})"
        elif action == 'W':
            w = sizes[-5:]
            b_score = sum(1.5**i for i, s in enumerate(w) if s == "BIG")
            s_score = sum(1.5**i for i, s in enumerate(w) if s == "SMALL")
            if b_score > s_score: return "BIG", "TREND(B)"
            elif s_score > b_score: return "SMALL", "TREND(S)"
            else: return last_s, "MOMENTUM"
        return last_s, "DEFAULT"

    return predict

print("Searching and printing verified models...", flush=True)

random.seed(42)
found_count = 0

for iteration in range(100000):
    params = {}
    params['l1_default'] = random.choice(['W', 'C', 'O'])
    if random.random() < 0.7: params['l1_drag3'] = random.choice(['C', 'O'])
    if random.random() < 0.5: params['l1_drag2'] = random.choice(['C', 'O'])
    if random.random() < 0.7: params['l1_trip_cap'] = random.choice(['O', 'C'])
    if random.random() < 0.7: params['l1_p1p2c1'] = random.choice(['P', 'C', 'O'])
    if random.random() < 0.7: params['l1_alt2'] = random.choice(['O', 'C'])
    if random.random() < 0.7: params['l1_alt3'] = random.choice(['O', 'C'])

    params['l2_default'] = random.choice(['C', 'O', 'W'])
    if random.random() < 0.8: params['l2_drag3'] = random.choice(['C', 'O'])
    if random.random() < 0.8: params['l2_drag2'] = random.choice(['C', 'O'])
    if random.random() < 0.8: params['l2_p2c1'] = random.choice(['P', 'C', 'O'])
    if random.random() < 0.8: params['l2_alt2'] = random.choice(['O', 'C'])
    if random.random() < 0.8: params['l2_alt3'] = random.choice(['O', 'C'])
    if random.random() < 0.5: params['l2_delta5'] = random.choice(['O', 'C'])

    params['l3_default'] = random.choice(['C', 'O', 'W'])
    if random.random() < 0.8: params['l3_drag3'] = random.choice(['C', 'O'])
    if random.random() < 0.8: params['l3_drag2'] = random.choice(['C', 'O'])
    if random.random() < 0.8: params['l3_p2c1'] = random.choice(['P', 'C', 'O'])
    if random.random() < 0.8: params['l3_alt2'] = random.choice(['O', 'C'])
    if random.random() < 0.8: params['l3_alt3'] = random.choice(['O', 'C'])
    if random.random() < 0.5: params['l3_delta5'] = random.choice(['O', 'C'])

    engine = make_custom_engine(params)
    tot_max, results = evaluate(engine)
    if tot_max <= 2:
        found_count += 1
        total_wins = sum(r[1] for r in results)
        total_losses = sum(r[2] for r in results)
        print(f"\n🏆 FOUND MODEL #{found_count} (iter {iteration}): Max Loss = {tot_max}, Total Wins = {total_wins}/{total_wins+total_losses} ({total_wins/(total_wins+total_losses)*100:.1f}%)", flush=True)
        print(f"PARAMS = {params}", flush=True)
        for r in results:
            print(f"   {r[0]}: {r[1]}W/{r[2]}L (max streak: {r[3]})", flush=True)
        if found_count >= 5:
            break
