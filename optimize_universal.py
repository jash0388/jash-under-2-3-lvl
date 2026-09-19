import itertools
from solve_all_seven import all_seven, opp, get_runs

def evaluate_strategy(predictor_fn):
    results = []
    for name, seq in all_seven:
        history = seq[:3]
        wins = 0
        losses = 0
        streak = 0
        max_streak = 0
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
        results.append((name, wins, losses, max_streak, details))
    return results

def make_predictor(params):
    def predict(history, streak):
        if not history:
            return 'SMALL', 'DEFAULT'
        
        sizes = [h['size'] for h in history]
        last_s = sizes[-1]
        runs = get_runs(sizes)
        curr_run_side, curr_run_len = runs[-1]
        prev_run_side, prev_run_len = runs[-2] if len(runs) >= 2 else (None, 0)
        p3_run_side, p3_run_len = runs[-3] if len(runs) >= 3 else (None, 0)
        p4_run_side, p4_run_len = runs[-4] if len(runs) >= 4 else (None, 0)

        # Level 3 Recovery (streak == 2)
        if streak == 2:
            mode_l3 = params['l3_mode']
            if mode_l3 == 'momentum':
                return last_s, 'L3 MOMENTUM'
            elif mode_l3 == 'anti_momentum':
                return opp(last_s), 'L3 ANTI-MOMENTUM'
            elif mode_l3 == 'smart_cadence':
                # If we just had a single opposite ball (e.g. S after BBB or BB), cut back to dominant
                if curr_run_len == 1 and prev_run_len >= 2:
                    return prev_run_side, 'L3 REVERT TO DOM'
                if curr_run_len >= 2:
                    return curr_run_side, 'L3 DRAGON RIDE'
                return opp(last_s), 'L3 FLIP'
            elif mode_l3 == 'smart_pattern':
                # Check if alternating chop (1-1-1)
                if curr_run_len == 1 and prev_run_len == 1:
                    return opp(last_s), 'L3 CHOP FLIP'
                if curr_run_len == 1 and prev_run_len >= 2:
                    return prev_run_side, 'L3 RESTORE RUN'
                return curr_run_side, 'L3 FOLLOW'

        # Level 2 Recovery (streak == 1)
        if streak == 1:
            mode_l2 = params['l2_mode']
            if mode_l2 == 'momentum':
                return last_s, 'L2 MOMENTUM'
            elif mode_l2 == 'revert_if_single':
                if curr_run_len == 1 and prev_run_len >= 2:
                    return prev_run_side, 'L2 REVERT'
                return last_s, 'L2 FOLLOW'
            elif mode_l2 == 'chop_or_follow':
                if curr_run_len == 1 and prev_run_len == 1:
                    return opp(last_s), 'L2 CHOP'
                return last_s, 'L2 FOLLOW'
            elif mode_l2 == 'anti_momentum':
                return opp(last_s), 'L2 ANTI-MOMENTUM'

        # Level 1 Base Prediction (streak == 0)
        # Check Dragon
        dragon_thresh = params['dragon_thresh']
        if curr_run_len >= dragon_thresh:
            return curr_run_side, f'DRAGON ({curr_run_len})'

        # Check Doublet Cadence
        if params['doublet_cadence']:
            if curr_run_len == 1 and prev_run_len == 2:
                # e.g. BB -> S (now at S1) -> predict B to make BB -> S -> B
                return prev_run_side, 'DOUBLET INTERCEPT'
            if curr_run_len == 2 and prev_run_len == 1:
                # e.g. S -> BB -> cut to S
                return opp(curr_run_side), 'DOUBLET CUT'

        # Check Chop/Ping-Pong
        chop_thresh = params['chop_thresh']
        if curr_run_len == 1 and prev_run_len == 1 and p3_run_len == 1:
            return opp(last_s), 'CHOP'

        # Micro-trend / Momentum weighting
        w_len = params['micro_w_len']
        sub = sizes[-w_len:]
        b_score = sum(1.2**i for i, s in enumerate(sub) if s == 'BIG')
        s_score = sum(1.2**i for i, s in enumerate(sub) if s == 'SMALL')
        
        if b_score > s_score:
            return 'BIG', 'MICRO-TREND'
        else:
            return 'SMALL', 'MICRO-TREND'

    return predict

param_grid = {
    'l3_mode': ['smart_cadence', 'smart_pattern', 'momentum', 'anti_momentum'],
    'l2_mode': ['revert_if_single', 'chop_or_follow', 'momentum'],
    'dragon_thresh': [2, 3, 4],
    'doublet_cadence': [True, False],
    'chop_thresh': [2, 3],
    'micro_w_len': [4, 5, 6, 8]
}

keys, values = zip(*param_grid.items())
permutations_dicts = [dict(zip(keys, v)) for v in itertools.product(*values)]

print(f'Total candidates to evaluate: {len(permutations_dicts)}')

perfect = []
for p in permutations_dicts:
    pred_fn = make_predictor(p)
    res = evaluate_strategy(pred_fn)
    max_losses = [r[3] for r in res]
    total_max = max(max_losses)
    if total_max <= 2:
        perfect.append((p, total_max, max_losses, res))

print(f'Found {len(perfect)} perfect models with max consecutive losses <= 2 on ALL 7 sequences!')
for idx, (p, t_max, m_losses, res) in enumerate(perfect[:10]):
    print(f'--- Candidate {idx+1} ---')
    print('Param:', p)
    print('Max losses across [A, B, C, D, E, F, G]:', m_losses)
    for r in res:
        print(f"  {r[0]}: Wins={r[1]}, Losses={r[2]}, MaxLoss={r[3]}")
