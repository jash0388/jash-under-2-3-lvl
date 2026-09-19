from test_all_three_seqs import seq_A, seq_B, seq_C, opp
from million_rounds_deep_research import million_data, evaluate_strategy

# Let's search across combinations of Level 1, Level 2, and Level 3 rules
# to find an engine that has MAX_LOSS <= 2 across Seq A, Seq B, Seq C,
# and maximizes 3-level cycle win rate on 200,000 rounds!

def run_parametric_search():
    def make_engine(dragon_min=3, chop_thresh=2, doublet_action="FLIP", l2_pair=True, l3_inversion=True):
        def predict(history, loss_streak):
            sizes = [h['size'] for h in history]
            last = sizes[-1]
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
            
            curr_s, curr_l = runs[-1]
            prev_l = runs[-2][1] if len(runs) >= 2 else 1
            prev2_l = runs[-3][1] if len(runs) >= 3 else 1
            
            alt = 0
            for s, l in reversed(runs):
                if l == 1: alt += 1
                else: break
                
            recent_lens = [r[1] for r in runs[-6:]]
            avg_len = sum(recent_lens) / len(recent_lens)

            # L3 EMERGENCY
            if loss_streak >= 2:
                if curr_l >= dragon_min:
                    return last, f"L3_DRAGON ({last} x{curr_l})"
                elif curr_l == 2:
                    if doublet_action == "FLIP":
                        return opp(last), f"L3_DOUBLET_FLIP"
                    else:
                        return last, f"L3_DOUBLET_REPEAT"
                else: # curr_l == 1
                    if prev_l >= 3 and l2_pair:
                        return last, f"L3_BREAK_PAIR"
                    elif alt >= chop_thresh:
                        return opp(last), f"L3_CHOP_FLIP"
                    else:
                        return opp(last) if l3_inversion else last, f"L3_DEFAULT"
            # L2
            elif loss_streak == 1:
                if curr_l >= dragon_min:
                    return last, f"L2_DRAGON"
                elif curr_l == 2:
                    if doublet_action == "FLIP":
                        return opp(last), f"L2_DOUBLET_FLIP"
                    else:
                        return last, f"L2_DOUBLET_REPEAT"
                else: # curr_l == 1
                    if prev_l >= 3 and l2_pair:
                        return last, f"L2_BREAK_PAIR"
                    elif alt >= chop_thresh:
                        return opp(last), f"L2_CHOP_FLIP"
                    else:
                        return last, f"L2_DEFAULT"
            # L1
            else:
                if curr_l >= dragon_min:
                    return last, f"L1_DRAGON"
                elif curr_l == 2:
                    if doublet_action == "FLIP":
                        return opp(last), f"L1_DOUBLET_FLIP"
                    else:
                        return last, f"L1_DOUBLET_REPEAT"
                else:
                    if prev_l >= 3 and l2_pair:
                        return last, f"L1_BREAK_PAIR"
                    elif alt >= chop_thresh:
                        return opp(last), f"L1_CHOP_FLIP"
                    else:
                        return last, f"L1_FLOW"
                        
        return predict

    best = []
    
    for dm in [3, 4]:
        for ct in [2, 3]:
            for da in ["FLIP", "REPEAT"]:
                for l2p in [True, False]:
                    for l3i in [True, False]:
                        fn = make_engine(dm, ct, da, l2p, l3i)
                        
                        # Test on all 3 sequences
                        max_losses = []
                        for seq in [seq_A, seq_B, seq_C]:
                            hist = []
                            ls = 0
                            ml = 0
                            for r in seq:
                                if len(hist) < 3:
                                    hist.append(r)
                                    continue
                                p, _ = fn(hist, ls)
                                if p == r['size']:
                                    ls = 0
                                else:
                                    ls += 1
                                    ml = max(ml, ls)
                                hist.append(r)
                            max_losses.append(ml)
                            
                        # If max consecutive losses across ALL 3 sequences is <= 2:
                        if max(max_losses) <= 2:
                            print(f"FOUND ZERO-BUST COMBO: dm={dm}, ct={ct}, da={da}, l2p={l2p}, l3i={l3i} | MaxLosses={max_losses}")
                            best.append((dm, ct, da, l2p, l3i, max_losses))
                            
    if not best:
        print("No exact <= 2 combo found with these basic parameters. Trying extended combinations...")
        for dm in [2, 3, 4]:
            for ct in [1, 2, 3]:
                for da in ["FLIP", "REPEAT"]:
                    for l2p in [True, False]:
                        for l3i in [True, False]:
                            fn = make_engine(dm, ct, da, l2p, l3i)
                            max_losses = []
                            for seq in [seq_A, seq_B, seq_C]:
                                hist = []
                                ls = 0
                                ml = 0
                                for r in seq:
                                    if len(hist) < 3:
                                        hist.append(r)
                                        continue
                                    p, _ = fn(hist, ls)
                                    if p == r['size']:
                                        ls = 0
                                    else:
                                        ls += 1
                                        ml = max(ml, ls)
                                    hist.append(r)
                                max_losses.append(ml)
                            if max(max_losses) <= 2:
                                print(f"EXTENDED MATCH: dm={dm}, ct={ct}, da={da}, l2p={l2p}, l3i={l3i} | MaxLosses={max_losses}")

run_parametric_search()
