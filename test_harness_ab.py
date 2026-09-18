import json
import random
import time

seq_A = [
    {'period': '10859', 'number': 8, 'size': 'BIG'},
    {'period': '10860', 'number': 8, 'size': 'BIG'},
    {'period': '10861', 'number': 0, 'size': 'SMALL'},
    {'period': '10862', 'number': 2, 'size': 'SMALL'},
    {'period': '10863', 'number': 4, 'size': 'SMALL'},
    {'period': '10864', 'number': 2, 'size': 'SMALL'},
    {'period': '10865', 'number': 9, 'size': 'BIG'},
    {'period': '10866', 'number': 0, 'size': 'SMALL'},
    {'period': '10867', 'number': 0, 'size': 'SMALL'},
    {'period': '10868', 'number': 6, 'size': 'BIG'},
    {'period': '10869', 'number': 3, 'size': 'SMALL'},
    {'period': '10870', 'number': 1, 'size': 'SMALL'},
]

seq_B = [
    {'period': '10954', 'number': 2, 'size': 'SMALL'},
    {'period': '10955', 'number': 5, 'size': 'BIG'},
    {'period': '10956', 'number': 9, 'size': 'BIG'},
    {'period': '10957', 'number': 4, 'size': 'SMALL'},
    {'period': '10958', 'number': 8, 'size': 'BIG'},
    {'period': '10959', 'number': 2, 'size': 'SMALL'},
    {'period': '10960', 'number': 4, 'size': 'SMALL'},
    {'period': '10961', 'number': 3, 'size': 'SMALL'},
    {'period': '10962', 'number': 5, 'size': 'BIG'},
    {'period': '10963', 'number': 4, 'size': 'SMALL'},
]

seq_C = [
    {'period': '11015', 'number': 9, 'size': 'BIG'},
    {'period': '11016', 'number': 7, 'size': 'BIG'},
    {'period': '11017', 'number': 2, 'size': 'SMALL'},
    {'period': '11018', 'number': 9, 'size': 'BIG'},
    {'period': '11019', 'number': 8, 'size': 'BIG'},
    {'period': '11020', 'number': 3, 'size': 'SMALL'},
    {'period': '11021', 'number': 9, 'size': 'BIG'},
    {'period': '11022', 'number': 3, 'size': 'SMALL'},
    {'period': '11023', 'number': 0, 'size': 'SMALL'},
    {'period': '11024', 'number': 0, 'size': 'SMALL'},
    {'period': '11025', 'number': 8, 'size': 'BIG'},
    {'period': '11026', 'number': 7, 'size': 'BIG'},
    {'period': '11027', 'number': 2, 'size': 'SMALL'},
]

def opp(s): return "SMALL" if s == "BIG" else "BIG"

def predict_apex_titan_v47(history, loss_streak):
    sizes = [h['size'] for h in history]
    if len(sizes) < 3:
        return "BIG", "INITIALIZING"
        
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
    last = curr_s
    
    prev_s, prev_l = runs[-2] if len(runs) >= 2 else (opp(curr_s), 1)
    prev2_s, prev2_l = runs[-3] if len(runs) >= 3 else (curr_s, 1)
    
    alt = 0
    for s, l in reversed(runs):
        if l == 1: alt += 1
        else: break
        
    last12 = sizes[-12:]
    big_count = last12.count("BIG")
    small_count = last12.count("SMALL")
    dominant = "BIG" if big_count >= 7 else ("SMALL" if small_count >= 7 else None)

    # LEVEL 3 (AFTER 2 LOSSES: EMERGENCY ZERO-LOSS SHIELD)
    if loss_streak >= 2:
        if curr_l >= 4:
            return last, f"🛑 LVL 3 DEEP DRAGON ({last} x{curr_l})"
        elif curr_l == 2:
            return opp(last), f"🛑 LVL 3 DOUBLET CUT ({last} x2 -> FLIP)"
        elif curr_l == 1:
            if alt >= 3:
                return opp(last), f"🛑 LVL 3 CHOP FLIP (x{alt})"
            elif dominant:
                return dominant, f"🛑 LVL 3 DOMINANT RECOVERY ({dominant})"
            else:
                return opp(last), f"🛑 LVL 3 BREAKOUT ({opp(last)})"
        else:
            return opp(last), f"🛑 LVL 3 INVERSION ({opp(last)})"

    # LEVEL 2 (AFTER 1 LOSS)
    elif loss_streak == 1:
        if curr_l >= 4:
            return last, f"🛡️ LVL 2 DEEP DRAGON ({last} x{curr_l})"
        elif curr_l == 2:
            return opp(last), f"🛡️ LVL 2 DOUBLET CUT ({last} x2)"
        elif curr_l == 1:
            if alt >= 3:
                return opp(last), f"🛡️ LVL 2 CHOP FLIP (x{alt})"
            elif prev_l >= 3:
                if dominant:
                    return dominant, f"🛡️ LVL 2 DOMINANT REBOUND ({dominant})"
                else:
                    return opp(last), f"🛡️ LVL 2 DRAGON REBOUND ({opp(last)})"
            elif alt == 2:
                return opp(last), f"🛡️ LVL 2 CHOP FLIP (x2)"
            else:
                return last, f"🛡️ LVL 2 MOMENTUM ({last})"
        else:
            return last, f"🛡️ LVL 2 FOLLOW ({last})"

    # LEVEL 1 (NORMAL FLOW)
    else:
        if curr_l >= 2 and curr_l <= 7:
            return last, f"🐉 DRAGON FLOW ({last} x{curr_l})"
        elif curr_l > 7:
            return opp(last), f"⚖️ FATIGUE CUT (x{curr_l})"
        else:
            if alt >= 3:
                return opp(last), f"⚡ CHOP OSCILLATE (x{alt})"
            elif dominant:
                return dominant, f"🌊 DOMINANT FLOW ({dominant})"
            else:
                return last, f"🌊 FLOW MOMENTUM ({last})"

def test_strategy_on_seqs(pred_fn, name=""):
    print(f"\n==================== {name} ====================")
    for seq_name, seq in [("Sequence A (10859-10870)", seq_A), 
                          ("Sequence B (10954-10963)", seq_B),
                          ("Sequence C (11015-11027)", seq_C)]:
        hist = []
        loss_streak = 0
        max_loss = 0
        wins, losses = 0, 0
        print(f"\n--- {seq_name} ---")
        for r in seq:
            if len(hist) < 3:
                hist.append(r)
                continue
            pred, reg = pred_fn(hist, loss_streak)
            won = (pred == r['size'])
            if won:
                wins += 1
                lvl = 1 if loss_streak == 0 else loss_streak + 1
                status = f"✅ WIN (Lvl {lvl})"
                loss_streak = 0
            else:
                losses += 1
                loss_streak += 1
                max_loss = max(max_loss, loss_streak)
                status = f"❌ LOSS (Lvl {loss_streak})"
            print(f"{r['period']}: Pred={pred:5s} | Act={r['size']:5s}({r['number']}) | {status:15s} | {reg}")
            hist.append(r)
        print(f"Result for {seq_name}: Wins={wins}, Losses={losses}, Max Consecutive Losses={max_loss}")

if __name__ == "__main__":
    test_strategy_on_seqs(predict_apex_titan_v47, "Apex Titan V47 Multi-Regime Master")
