from million_rounds_deep_research import million_data, evaluate_strategy, opp
import random

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

def test_variants():
    data = million_data[:200000]
    
    # We want to test different rule combinations at Level 1, 2, 3
    # Let's see what happens on different chop/doublet thresholds
    def make_predictor(doublet_cutoff=2.2, alt_thresh=2, drag_max=7, flip_1ball=True):
        def pred(history, loss_streak):
            sizes = [h['size'] for h in history[-30:]]
            last = sizes[-1]
            runs = get_runs(sizes)
            curr_s, curr_l = runs[-1]
            prev_l = runs[-2][1] if len(runs) >= 2 else 1
            prev2_l = runs[-3][1] if len(runs) >= 3 else 1
            streak = curr_l
            recent_lens = [r[1] for r in runs[-6:]]
            avg_len = sum(recent_lens) / len(recent_lens)
            
            alt = 0
            for s, l in reversed(runs):
                if l == 1: alt += 1
                else: break

            if loss_streak >= 2:
                # Emergency resolution
                if streak >= 3:
                    return last, "L3_DRAGON"
                elif streak == 2:
                    if avg_len <= doublet_cutoff:
                        return opp(last), "L3_DOUBLET_CUT"
                    return last, "L3_DRAGON_TRY"
                else:
                    if prev_l == 2 and flip_1ball:
                        return opp(last), "L3_1BALL_FLIP"
                    elif prev_l == 1 and prev2_l == 2:
                        return last, "L3_2BALL_PAIR"
                    elif alt >= alt_thresh:
                        return opp(last), "L3_CHOP"
                    else:
                        return last, "L3_MOMENTUM"
            elif loss_streak == 1:
                if streak >= 3:
                    return last, "L2_DRAGON"
                elif streak == 2:
                    if avg_len <= doublet_cutoff:
                        return opp(last), "L2_DOUBLET_CUT"
                    return last, "L2_DRAGON_TRY"
                else:
                    if prev_l == 2 and flip_1ball:
                        return opp(last), "L2_1BALL_FLIP"
                    elif prev_l == 1 and prev2_l == 2:
                        return last, "L2_2BALL_PAIR"
                    elif alt >= alt_thresh:
                        return opp(last), "L2_CHOP"
                    else:
                        return last, "L2_MOMENTUM"
            else:
                if streak >= 3 and streak <= drag_max:
                    return last, "L1_DRAGON"
                elif streak > drag_max:
                    return opp(last), "L1_FATIGUE"
                elif streak == 2:
                    if avg_len <= doublet_cutoff:
                        return opp(last), "L1_DOUBLET_CUT"
                    return last, "L1_DRAGON_TRY"
                else:
                    if prev_l == 2 and flip_1ball:
                        return opp(last), "L1_1BALL_FLIP"
                    elif prev_l == 1 and prev2_l == 2:
                        return last, "L1_2BALL_PAIR"
                    elif alt >= alt_thresh:
                        return opp(last), "L1_CHOP"
                    else:
                        return last, "L1_MOMENTUM"
        return pred

    best_busts = 999999
    best_params = None
    
    for dc in [2.0, 2.2, 2.5, 3.0]:
        for at in [2, 3]:
            for dm in [6, 7, 8, 10]:
                for f1 in [True, False]:
                    p = make_predictor(dc, at, dm, f1)
                    res = evaluate_strategy(data, f"dc={dc},at={at},dm={dm},f1={f1}", p)
                    if res['busts'] < best_busts:
                        best_busts = res['busts']
                        best_params = (dc, at, dm, f1, res)
                        print(f"New Best: dc={dc}, at={at}, dm={dm}, f1={f1} -> Busts={res['busts']}, RawWR={res['raw_wr']:.2f}%, CycleWR={res['cycle_wr']:.2f}%")

test_variants()
