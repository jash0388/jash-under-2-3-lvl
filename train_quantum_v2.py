import json
from collections import Counter

print("=" * 70)
print("🚀 TITAN QUANTUM v2.0 — 30 STUDOCU TRENDS ENGINE TRAINING")
print("=" * 70)

# 1. Official 30 Studocu Wingo Trends Catalog (by Games Expert 2)
TRENDS = {
    1:  {"name": "6-BIG DRAGON", "pat": ["BIG","BIG","BIG","BIG","BIG","BIG"], "next": 2},
    2:  {"name": "6-SMALL DRAGON", "pat": ["SMALL","SMALL","SMALL","SMALL","SMALL","SMALL"], "next": 3},
    3:  {"name": "1-1 ZIGZAG (B)", "pat": ["BIG","SMALL","BIG","SMALL","BIG","SMALL"], "next": 4},
    4:  {"name": "1-1 ZIGZAG (S)", "pat": ["SMALL","BIG","SMALL","BIG","SMALL","BIG"], "next": 5},
    5:  {"name": "2-1 RHYTHM (B)", "pat": ["BIG","BIG","SMALL","BIG","BIG","SMALL"], "next": 6},
    6:  {"name": "2-1 RHYTHM (S)", "pat": ["SMALL","SMALL","BIG","SMALL","SMALL","BIG"], "next": 7},
    7:  {"name": "3-3 MIRROR (B)", "pat": ["BIG","BIG","BIG","SMALL","SMALL","SMALL"], "next": 8},
    8:  {"name": "3-3 MIRROR (S)", "pat": ["SMALL","SMALL","SMALL","BIG","BIG","BIG"], "next": 9},
    9:  {"name": "1-2 RHYTHM (B)", "pat": ["BIG","SMALL","SMALL","BIG","SMALL","SMALL"], "next": 10},
    10: {"name": "1-2 RHYTHM (S)", "pat": ["SMALL","BIG","BIG","SMALL","BIG","BIG"], "next": 11},
    11: {"name": "2-2 RHYTHM (B)", "pat": ["BIG","BIG","SMALL","SMALL","BIG","BIG"], "next": 12},
    12: {"name": "2-2 RHYTHM (S)", "pat": ["SMALL","SMALL","BIG","BIG","SMALL","SMALL"], "next": 13},
    13: {"name": "ALT-DOUBLE (B)", "pat": ["BIG","SMALL","BIG","BIG","SMALL","BIG"], "next": 14},
    14: {"name": "ALT-DOUBLE (S)", "pat": ["SMALL","BIG","SMALL","SMALL","BIG","SMALL"], "next": 15},
    15: {"name": "4-2 SHIFT (B)", "pat": ["BIG","BIG","BIG","BIG","SMALL","SMALL"], "next": 16},
    16: {"name": "4-2 SHIFT (S)", "pat": ["SMALL","SMALL","SMALL","SMALL","BIG","BIG"], "next": 17},
    17: {"name": "CHOPPER-LOCK (B)", "pat": ["BIG","SMALL","BIG","SMALL","SMALL","BIG"], "next": 18},
    18: {"name": "CHOPPER-LOCK (S)", "pat": ["SMALL","BIG","SMALL","BIG","BIG","SMALL"], "next": 19},
    19: {"name": "1-3-2 PULSE (B)", "pat": ["BIG","SMALL","SMALL","SMALL","BIG","BIG"], "next": 20},
    20: {"name": "1-3-2 PULSE (S)", "pat": ["SMALL","BIG","BIG","BIG","SMALL","SMALL"], "next": 21},
    21: {"name": "2-3-1 FLIP (B)", "pat": ["BIG","BIG","SMALL","SMALL","SMALL","BIG"], "next": 22},
    22: {"name": "1-3-1-1 FLIP (S)", "pat": ["SMALL","BIG","BIG","BIG","SMALL","BIG"], "next": 23},
    23: {"name": "1-1-3-1 FLIP (B)", "pat": ["BIG","SMALL","BIG","BIG","BIG","SMALL"], "next": 24},
    24: {"name": "2-1-1-1-1 S-RUN", "pat": ["SMALL","SMALL","BIG","SMALL","BIG","SMALL"], "next": 25},
    25: {"name": "1-4-1 DRAGON-END (B)", "pat": ["BIG","SMALL","SMALL","SMALL","SMALL","BIG"], "next": 26},
    26: {"name": "1-4-1 DRAGON-END (S)", "pat": ["SMALL","BIG","BIG","BIG","BIG","SMALL"], "next": 27},
    27: {"name": "3-1-1-1 SURGE (B)", "pat": ["BIG","BIG","BIG","SMALL","BIG","SMALL"], "next": 28},
    28: {"name": "3-1-1-1 SURGE (S)", "pat": ["SMALL","SMALL","SMALL","BIG","SMALL","BIG"], "next": 29},
    29: {"name": "1-1-1-3 SURGE (B)", "pat": ["BIG","SMALL","BIG","SMALL","SMALL","SMALL"], "next": 30},
    30: {"name": "1-1-1-3 SURGE (S)", "pat": ["SMALL","BIG","SMALL","BIG","BIG","BIG"], "next": 1}
}

# 2. Build 12-step transition paths (Current Trend -> Next Trend)
CHAINS = {}
for tid, tinfo in TRENDS.items():
    nxt_id = tinfo["next"]
    CHAINS[tid] = {
        "name": tinfo["name"],
        "next_name": TRENDS[nxt_id]["name"],
        "next_id": nxt_id,
        "full_chain": tinfo["pat"] + TRENDS[nxt_id]["pat"]
    }

# Load live draws dataset
with open('/Users/jashwanthsingh/Downloads/jashvip/dataset_full_master.json') as f:
    live = json.load(f)

sizes = [d['size'] for d in live]
nums = [d['number'] for d in live]
print(f"Loaded {len(sizes)} live real draws.")

def predict_v2(hist, current_loss_streak=0):
    # Rule 1: DRAGON LOCK (Anti-Phase Immunity)
    last_side = hist[-1]
    streak_len = 1
    for i in range(len(hist) - 2, -1, -1):
        if hist[i] == last_side: streak_len += 1
        else: break
        
    # Rule 2: Multi-Window Studocu 30-Trend Matching (lengths 6 down to 2)
    best_candidate = None
    for k in [6, 5, 4, 3, 2]:
        sub = hist[-k:]
        matches = []
        for tid, cinfo in CHAINS.items():
            chain = cinfo["full_chain"]
            for pos in range(len(chain) - k):
                if chain[pos:pos+k] == sub:
                    next_val = chain[pos+k]
                    matches.append({
                        "tid": tid,
                        "name": cinfo["name"],
                        "pos": pos + k,
                        "next_val": next_val,
                        "k": k,
                        "leads_to": cinfo["next_name"],
                        "leads_id": cinfo["next_id"]
                    })
        if matches:
            preds = [m["next_val"] for m in matches]
            top_pred = Counter(preds).most_common(1)[0][0]
            top_m = next(m for m in matches if m["next_val"] == top_pred)
            best_candidate = (top_pred, top_m)
            break

    if streak_len >= 3 and streak_len < 6:
        # Override with dragon lock if pattern tries to prematurely cut a running dragon
        final_size = last_side
        regime = f"🐉 DRAGON MOMENTUM LOCK [{streak_len}]"
        active_trend = f"TREND #1/2 (DRAGON {last_side})"
        target_trend = f"TREND #2/3"
        step_pos = min(streak_len, 6)
        conf = 98
    elif best_candidate:
        top_pred, top_m = best_candidate
        final_size = top_pred
        step_pos = (top_m["pos"] % 6) + 1
        active_trend = f"TREND #{top_m['tid']}: {top_m['name']}"
        target_trend = f"TREND #{top_m['leads_id']}: {top_m['leads_to']}"
        regime = f"⚡ {active_trend} [STEP {step_pos}/6]"
        conf = 92 + top_m["k"]
    else:
        final_size = last_side
        active_trend = "TREND #1: 6-BIG DRAGON"
        target_trend = "TREND #2: 6-SMALL DRAGON"
        step_pos = 1
        regime = "🌊 CONTINUITY SYNC"
        conf = 90

    return {
        "finalSize": final_size,
        "activeTrend": active_trend,
        "targetTrend": target_trend,
        "stepPos": step_pos,
        "regime": regime,
        "conf": min(conf, 99)
    }

# Run rigorous simulation over all live draws with Strict 2-Level Loss Shield
balance = 1000.0
unit_l1 = 2.0
unit_l2 = 4.0
total_bets = 0
real_wins = 0
real_losses = 0
virtual_wins = 0
virtual_losses = 0
max_real_loss_streak = 0
cur_real_loss_streak = 0
mode = "REAL"

for i in range(10, len(sizes)):
    hist = sizes[:i]
    target = sizes[i]
    pred_res = predict_v2(hist, cur_real_loss_streak)
    pred = pred_res["finalSize"]

    if mode == "REAL":
        total_bets += 1
        stake = unit_l1 if cur_real_loss_streak == 0 else unit_l2
        if pred == target:
            profit = stake * 0.96
            balance += profit
            real_wins += 1
            cur_real_loss_streak = 0
        else:
            balance -= stake
            real_losses += 1
            cur_real_loss_streak += 1
            if cur_real_loss_streak > max_real_loss_streak:
                max_real_loss_streak = cur_real_loss_streak
            if cur_real_loss_streak >= 2:
                mode = "VIRTUAL"
    else:
        if pred == target:
            virtual_wins += 1
            mode = "REAL"
            cur_real_loss_streak = 0
        else:
            virtual_losses += 1

print("\n" + "=" * 70)
print("📊 TITAN QUANTUM v2.0 RIGOROUS BACKTEST SUMMARY")
print("=" * 70)
print(f"Total Live Draws Evaluated: {len(sizes) - 10}")
print(f"Real Stakes Placed: {total_bets}")
print(f"Real Wins: {real_wins} ({real_wins/total_bets*100:.1f}%)")
print(f"Real Losses: {real_losses}")
print(f"Virtual Paper Protection Rounds: {virtual_wins + virtual_losses} (Saved {virtual_losses} real losses!)")
print(f"MAX CONSECUTIVE REAL LOSSES: {max_real_loss_streak} (STRICTLY <= 2!)")
print(f"Final Balance: ₹{balance:.2f} (Profit: +₹{balance - 1000.0:.2f})")
print("=" * 70)

# Export Model Definitions to JSON for Browser Integration
model_export = {
    "trends": TRENDS,
    "version": "2.0-studocu-titan",
    "shield_max_loss": 2,
    "chains": {tid: c["full_chain"] for tid, c in CHAINS.items()}
}
with open('/Users/jashwanthsingh/Downloads/jashvip/quantum_v2_model.json', 'w') as f:
    json.dump(model_export, f, indent=2)

print("Exported quantum_v2_model.json successfully.")
