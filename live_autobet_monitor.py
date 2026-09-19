import urllib.request
import json
import time
import sys
from datetime import datetime

API_URL_1M = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"
API_URL_30S = "https://draw.ar-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json"

def opp(s): return "SMALL" if s == "BIG" else "BIG"

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

def predict_apex_titan_v80(nums, loss_streak=0):
    if len(nums) < 3:
        return "BIG", 7, "TITAN INITIALIZING"
    sizes = ["BIG" if n >= 5 else "SMALL" for n in nums][-50:]
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
        if r_l == 1:
            alt += 1
        else:
            break

    # Level 3 Recovery (Zero-Loss Cascade Shield)
    if loss_streak >= 2:
        if c_len >= 3:
            final_size = c_side
            regime = f"🛑 LVL 3 DRAGON RIDE ({c_side} x{c_len})"
        elif c_len == 2:
            final_size = c_side
            regime = f"🛑 LVL 3 DOUBLET RIDE ({c_side} x2)"
        elif alt >= 3:
            final_size = c_side
            regime = f"🛑 LVL 3 CHOP BREAK RIDE ({c_side})"
        elif alt >= 2:
            final_size = opp(c_side)
            regime = f"🛑 LVL 3 CHOP OSCILLATE ({opp(c_side)})"
        elif delta >= 5:
            final_size = opp(c_side)
            regime = f"🛑 LVL 3 VOLATILE DELTA BREAK (d={delta})"
        else:
            final_size = opp(c_side)
            regime = f"🛑 LVL 3 CASCADE SHIELD FLIP ({opp(c_side)})"

    # Level 2 Recovery (streak == 1)
    elif loss_streak == 1:
        if c_len >= 3:
            final_size = opp(c_side)
            regime = f"🛡️ LVL 2 DRAGON EXHAUSTION CUT ({opp(c_side)})"
        elif alt >= 3:
            final_size = opp(last_s)
            regime = f"🛡️ LVL 2 DEEP CHOP FLIP ({opp(last_s)})"
        elif alt >= 2:
            final_size = last_s
            regime = f"🛡️ LVL 2 CHOP STABILIZE ({last_s})"
        elif delta >= 5:
            final_size = opp(c_side)
            regime = f"🛡️ LVL 2 VOLATILE DELTA FLIP (d={delta})"
        else:
            final_size = c_side
            regime = f"🛡️ LVL 2 MOMENTUM LOCK ({c_side})"

    # Level 1 Base Prediction (streak == 0)
    else:
        if c_len == 3 and p_len == 1 and p3_len == 3:
            final_size = c_side
            regime = f"⚡ TRIPLET CADENCE FOLLOW ({c_side})"
        elif c_len >= 3:
            final_size = opp(c_side)
            regime = f"🐉 DRAGON EXHAUSTION CUT ({opp(c_side)} x{c_len})"
        elif alt >= 3:
            final_size = c_side
            regime = f"⚡ DEEP CHOP BREAK FLOW ({c_side})"
        elif alt >= 2:
            final_size = opp(last_s)
            regime = f"⚡ CHOP OSCILLATE ({opp(last_s)})"
        else:
            final_size = c_side
            regime = f"🌊 MOMENTUM FOLLOW ({c_side})"

    # Harmonic Lucky Ball
    allowed = [5, 6, 7, 8, 9] if final_size == "BIG" else [0, 1, 2, 3, 4]
    freq = {n: 0 for n in allowed}
    for n in nums[-20:]:
        if n in freq: freq[n] += 1
    best_num = min(allowed, key=lambda n: (freq[n], abs(n - (7 if final_size == "BIG" else 2))))

    return final_size, best_num, regime

import ssl

def fetch_history(url):
    ctx = ssl._create_unverified_context()
    req = urllib.request.Request(f"{url}?_t={int(time.time()*1000)}", headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=5, context=ctx) as res:
        data = json.loads(res.read().decode())
        items = data.get("data", {}).get("list", [])
        return [{
            "period": str(x.get("issueNumber") or x.get("period")),
            "number": int(x.get("number")),
            "size": "BIG" if int(x.get("number")) >= 5 else "SMALL"
        } for x in items if x.get("number") is not None]

def main():
    print("=" * 65)
    print("⚡ JASH VIP — APEX TITAN V70 LIVE AUTOBET ENGINE MONITOR")
    print("=" * 65)
    
    loss_streak = 0
    base_bet = 5
    stakes = [base_bet, base_bet * 3, base_bet * 9]
    wins = 0
    losses = 0
    profit = 0.0
    pending = None
    processed_periods = set()

    print("\n🟢 Connecting to WinGo 1M Live Feed...")
    
    while True:
        try:
            history = fetch_history(API_URL_1M)
            if not history:
                time.sleep(2)
                continue
                
            latest = history[0]
            latest_period = latest["period"]
            
            # Settle pending
            if pending and pending["period"] == latest_period:
                actual = latest["size"]
                pred = pending["pred"]
                stake = pending["stake"]
                won = (actual == pred)
                
                if won:
                    wins += 1
                    profit += stake * 0.96
                    lvl = loss_streak + 1
                    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] ✅ WIN on #{latest_period} | Result: {actual} ({latest['number']}) | +₹{stake*0.96:.2f} (Lvl {lvl}) | Total Profit: ₹{profit:.2f}")
                    loss_streak = 0
                else:
                    losses += 1
                    profit -= stake
                    loss_streak = min(2, loss_streak + 1)
                    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] ❌ LOSS on #{latest_period} | Result: {actual} ({latest['number']}) | -₹{stake:.2f} | Next Step: Lvl {loss_streak+1} (₹{stakes[loss_streak]}) | Total Profit: ₹{profit:.2f}")
                pending = None
            
            # Form next prediction
            next_period = str(int(latest_period) + 1)
            if next_period not in processed_periods:
                nums_chronological = [x["number"] for x in reversed(history)]
                pred_size, lucky_num, regime = predict_apex_titan_v80(nums_chronological, loss_streak)
                current_stake = stakes[loss_streak]
                
                pending = {
                    "period": next_period,
                    "pred": pred_size,
                    "num": lucky_num,
                    "stake": current_stake,
                    "regime": regime
                }
                processed_periods.add(next_period)
                
                rate = round((wins / (wins + losses) * 100)) if (wins + losses) > 0 else 100
                lvl_str = f"🟢 L1 (1x: ₹{current_stake})" if loss_streak == 0 else (f"🟡 L2 (3x: ₹{current_stake})" if loss_streak == 1 else f"🛑 L3 (9x: ₹{current_stake})")
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 🎯 Target: #{next_period} | Signal: {pred_size:<5} #{lucky_num} | Stake: ₹{current_stake:<3} [{lvl_str}] | Regime: {regime} | Stats: {wins}W/{losses}L ({rate}%)")
                
            time.sleep(2)
        except KeyboardInterrupt:
            print("\nStopped.")
            break
        except Exception as e:
            time.sleep(3)

if __name__ == "__main__":
    main()
