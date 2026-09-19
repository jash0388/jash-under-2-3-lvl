from research_cascade_breaker import all_12_seqs, test_engine, opp, get_runs

def evaluate_engine_detailed(predictor_fn, title=""):
    print(f"\n==================== {title} ====================")
    total_max, results = test_engine(predictor_fn)
    all_pass = True
    for name, wins, losses, max_loss, details in results:
        passed = (max_loss <= 2)
        if not passed: all_pass = False
        p_str = "✅ PASS" if passed else f"❌ FAIL (max loss = {max_loss})"
        print(f"\n{name} -> {wins}W/{losses}L, Max Streak: {max_loss} | {p_str}")
        for p, pred, act, res, lvl, tag in details:
            print(f"  P {p}: Pred {pred:<5} | Act {act:<5} | {res:<4} (Lvl {lvl}) | Tag: {tag}")
    print(f"\nOVERALL MAX CONSECUTIVE LOSSES = {total_max} | ALL <= 2: {all_pass}")
    return total_max, all_pass

# Let's test a simple adaptive strategy
def make_predictor(p_l1_chop, p_l2_mode, p_l3_mode):
    def predictor(history, loss_streak):
        sizes = [x['size'] for x in history]
        nums = [x['number'] for x in history]
        runs = get_runs(sizes)
        c_side, c_len = runs[-1]
        p_side, p_len = runs[-2] if len(runs) >= 2 else (opp(c_side), 0)
        p3_side, p3_len = runs[-3] if len(runs) >= 3 else (c_side, 0)
        last_s = sizes[-1]

        alt = 0
        for r_s, r_l in reversed(runs):
            if r_l == 1: alt += 1
            else: break

        # Level 3
        if loss_streak >= 2:
            if p_l3_mode == "momentum":
                return last_s, f"LVL3 MOMENTUM ({last_s})"
            elif p_l3_mode == "chop_or_momentum":
                if alt >= 2: return opp(last_s), f"LVL3 CHOP FLIP ({opp(last_s)})"
                return last_s, f"LVL3 MOMENTUM ({last_s})"
            elif p_l3_mode == "smart_anti_cascade":
                # If we are in a dragon (c_len >= 2), NEVER cut against it on L3, ride it!
                if c_len >= 2: return c_side, f"LVL3 DRAGON RIDE ({c_side} x{c_len})"
                # If chop (alt >= 2), oscillate
                if alt >= 2: return opp(last_s), f"LVL3 CHOP FLIP ({opp(last_s)})"
                # Else follow last
                return last_s, f"LVL3 MOMENTUM ({last_s})"
            elif p_l3_mode == "strict_follow_last":
                return last_s, f"LVL3 FOLLOW LAST ({last_s})"

        # Level 2
        elif loss_streak == 1:
            if p_l2_mode == "momentum":
                return last_s, f"LVL2 MOMENTUM ({last_s})"
            elif p_l2_mode == "chop_or_momentum":
                if alt >= 3: return opp(last_s), f"LVL2 CHOP FLIP ({opp(last_s)})"
                return last_s, f"LVL2 MOMENTUM ({last_s})"
            elif p_l2_mode == "smart_anti_cascade":
                if c_len >= 2: return c_side, f"LVL2 DRAGON RIDE ({c_side} x{c_len})"
                if alt >= 3: return opp(last_s), f"LVL2 CHOP FLIP ({opp(last_s)})"
                return last_s, f"LVL2 MOMENTUM ({last_s})"

        # Level 1
        else:
            if c_len == 3 and p_len == 1 and p3_len == 3:
                return opp(c_side), "⚡ TRIPLET CAP"
            elif c_len >= 3:
                return c_side, f"🐉 DRAGON ({c_side} x{c_len})"
            elif c_len == 1 and p_len == 2 and p3_len == 1:
                return p_side, f"⚡ DOUBLET CADENCE ({p_side})"
            elif alt >= 2:
                return opp(last_s), f"⚡ CHOP OSCILLATE ({opp(last_s)})"
            else:
                w = sizes[-5:]
                b_score = sum(1.5**i for i, s in enumerate(w) if s == "BIG")
                s_score = sum(1.5**i for i, s in enumerate(w) if s == "SMALL")
                if b_score > s_score: return "BIG", "MICRO-TREND BIG"
                elif s_score > b_score: return "SMALL", "MICRO-TREND SMALL"
                else: return last_s, f"MOMENTUM ({last_s})"
    return predictor

if __name__ == "__main__":
    for l2 in ["momentum", "chop_or_momentum", "smart_anti_cascade"]:
        for l3 in ["momentum", "chop_or_momentum", "smart_anti_cascade", "strict_follow_last"]:
            pred = make_predictor(True, l2, l3)
            tot_max, results = test_engine(pred)
            print(f"Config: L2={l2:<20} | L3={l3:<20} -> Overall Max Loss = {tot_max}")
