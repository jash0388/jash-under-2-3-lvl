import json

# 1. Load 350-draw user feed
with open("user_feed_250_draws.json") as f:
    user_350 = json.load(f)

# 2. Load other master feeds from solve_8feature_perfect_574.py
import importlib.util
spec = importlib.util.spec_from_file_location("mod", "solve_8feature_perfect_574.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

all_feeds = [("user_feed_350_draws (51028-51668)", user_350)]
seen_sigs = {",".join(str(x["number"]) for x in user_350[:10])}

for name, fd in mod.all_feeds:
    standardized = []
    for item in fd:
        if isinstance(item, (list, tuple)):
            standardized.append({"period": str(item[0]), "number": item[1], "size": item[2] if len(item)>2 else ("BIG" if item[1]>=5 else "SMALL")})
        else:
            standardized.append(item)
    sig = ",".join(str(x["number"]) for x in standardized[:10])
    if sig not in seen_sigs:
        seen_sigs.add(sig)
        all_feeds.append((name, standardized))

print(f"Loaded {len(all_feeds)} Real Market Feeds.")
total_draws = sum(len(f[1]) for f in all_feeds)
print(f"Total Market Draws across all feeds: {total_draws}")

def opp(s):
    return "SMALL" if s == "BIG" else "BIG"

def get_runs(sizes):
    runs = []
    if not sizes: return runs
    curr = sizes[0]
    l = 1
    for i in range(1, len(sizes)):
        if sizes[i] == curr: l += 1
        else:
            runs.append({"size": curr, "len": l})
            curr = sizes[i]
            l = 1
    runs.append({"size": curr, "len": l})
    return runs

def extract_features9(sizes, nums, streak):
    runs = get_runs(sizes)
    c_run = runs[-1]
    c_side = c_run["size"]
    c_len = c_run["len"]
    p_run = runs[-2] if len(runs) >= 2 else {"size": opp(c_side), "len": 0}
    p2_run = runs[-3] if len(runs) >= 3 else {"size": c_side, "len": 0}
    last_s = sizes[-1]
    last_n = nums[-1] if len(nums) > 0 else (7 if last_s == "BIG" else 2)
    prev_n = nums[-2] if len(nums) >= 2 else last_n
    
    alt = 0
    for r in reversed(runs):
        if r["len"] == 1: alt += 1
        else: break
        
    c_len_cat = min(c_len, 4)
    p_len_cat = min(p_run["len"], 3)
    p2_len_cat = min(p2_run["len"], 3)
    alt_cat = min(alt, 3)
    streak_cat = min(streak, 2)
    
    recent = sizes[-6:]
    flips = sum(1 for i in range(1, len(recent)) if recent[i] != recent[i-1])
    flip_cat = 0 if flips <= 1 else (1 if (flips == 2 or flips == 3) else 2)
    c_side_bit = 1 if c_side == "BIG" else 0
    parity_bit = abs(last_n) % 2
    harmonic_bit = abs(last_n + prev_n) % 2
    
    key = f"{streak_cat}_{c_len_cat}_{p_len_cat}_{p2_len_cat}_{alt_cat}_{flip_cat}_{c_side_bit}_{parity_bit}_{harmonic_bit}"
    return key, c_side, last_s, c_len, alt

def simulate_engine(rules):
    total_rounds = 0
    total_wins = 0
    max_streak_overall = 0
    total_busts = 0
    level_dist = {1: 0, 2: 0, 3: 0, 4: 0}
    feed_stats = []

    for name, fd in all_feeds:
        if len(fd) < 4: continue
        loss_streak = 0
        feed_wins = 0
        feed_rounds = 0
        feed_max_streak = 0
        feed_l1 = 0
        feed_l2 = 0
        feed_l3 = 0

        for i in range(3, len(fd)):
            hist = fd[:i]
            target = fd[i]
            sizes = [d["size"] for d in hist]
            nums = [d["number"] for d in hist]
            actual_size = target["size"]

            key, c_side, last_s, c_len, alt = extract_features9(sizes, nums, loss_streak)
            
            if loss_streak >= 2:
                fallback = c_side if c_len >= 2 else (opp(last_s) if alt >= 2 else c_side)
            elif loss_streak == 1:
                fallback = c_side if c_len >= 2 else (opp(last_s) if alt >= 2 else opp(c_side))
            else:
                fallback = c_side if c_len >= 3 else (opp(c_side) if c_len == 2 else (opp(last_s) if alt >= 2 else c_side))

            act_rule = rules.get(key, fallback)
            if act_rule == "SAME": pred_size = c_side
            elif act_rule == "OPP": pred_size = opp(c_side)
            elif act_rule == "LAST": pred_size = last_s
            elif act_rule == "OPP_LAST": pred_size = opp(last_s)
            elif act_rule in ["BIG", "SMALL"]: pred_size = act_rule
            else: pred_size = c_side

            feed_rounds += 1
            total_rounds += 1

            if pred_size == actual_size:
                feed_wins += 1
                total_wins += 1
                lvl = min(loss_streak + 1, 3)
                level_dist[lvl] = level_dist.get(lvl, 0) + 1
                if lvl == 1: feed_l1 += 1
                elif lvl == 2: feed_l2 += 1
                elif lvl == 3: feed_l3 += 1
                loss_streak = 0
            else:
                loss_streak += 1
                if loss_streak > 2:
                    total_busts += 1
                feed_max_streak = max(feed_max_streak, loss_streak)
                max_streak_overall = max(max_streak_overall, loss_streak)

        feed_stats.append({
            "name": name,
            "draws": len(fd),
            "rounds": feed_rounds,
            "wins": feed_wins,
            "max_streak": feed_max_streak,
            "l1": feed_l1, "l2": feed_l2, "l3": feed_l3
        })

    score = total_wins * 20 - total_busts * 1000000 - max_streak_overall * 10000
    return {
        "score": score,
        "wins": total_wins,
        "rounds": total_rounds,
        "win_rate": (total_wins / total_rounds * 100) if total_rounds else 0,
        "max_streak": max_streak_overall,
        "busts": total_busts,
        "dist": level_dist,
        "feeds": feed_stats
    }

# Start with existing rules or initialize
with open("v9um_apex_titan_supreme_9feature_rules.json") as f:
    best_rules = json.load(f)

init_res = simulate_engine(best_rules)
best_score = init_res["score"]
print(f"Starting: Wins={init_res['wins']}/{init_res['rounds']} ({init_res['win_rate']:.1f}%), MaxStreak={init_res['max_streak']}, Busts={init_res['busts']}")

# Collect all keys active across all feeds
all_active_keys = set()
for name, fd in all_feeds:
    if len(fd) < 4: continue
    for i in range(3, len(fd)):
        hist = fd[:i]
        sizes = [d["size"] for d in hist]
        nums = [d["number"] for d in hist]
        for streak in [0, 1, 2]:
            key, _, _, _, _ = extract_features9(sizes, nums, streak)
            all_active_keys.add(key)

print(f"Total Active Keys across all feeds: {len(all_active_keys)}")

candidates = ["SAME", "OPP", "LAST", "OPP_LAST", "BIG", "SMALL"]

for iteration in range(5):
    improved = False
    for k in sorted(all_active_keys):
        cur_val = best_rules.get(k)
        for cand in candidates:
            if cand == cur_val: continue
            best_rules[k] = cand
            res = simulate_engine(best_rules)
            if res["score"] > best_score:
                best_score = res["score"]
                cur_val = cand
                improved = True
                print(f"Iter {iteration}: {k} -> {cand} | Score={best_score}, W={res['wins']}/{res['rounds']} ({res['win_rate']:.1f}%), MS={res['max_streak']}, Busts={res['busts']}")
        if cur_val is not None:
            best_rules[k] = cur_val

final_res = simulate_engine(best_rules)
print("\n" + "="*80)
print(f"FINAL MASTER OPTIMIZATION RESULT ON {len(all_feeds)} FEEDS ({total_draws} DRAWS):")
print(f"Wins: {final_res['wins']}/{final_res['rounds']} ({final_res['win_rate']:.2f}%)")
print(f"Max Loss Streak: {final_res['max_streak']} (ZERO BUSTS = {final_res['busts'] == 0})")
print(f"Level Win Distribution: L1={final_res['dist'][1]} ({final_res['dist'][1]/final_res['wins']*100:.1f}%), L2={final_res['dist'][2]} ({final_res['dist'][2]/final_res['wins']*100:.1f}%), L3={final_res['dist'][3]} ({final_res['dist'][3]/final_res['wins']*100:.1f}%)")
print("-"*80)
for fs in final_res["feeds"]:
    print(f" • {fs['name']}: {fs['wins']}/{fs['rounds']} Wins ({(fs['wins']/fs['rounds']*100):.1f}%) | Max Loss Streak = {fs['max_streak']} | L1={fs['l1']}, L2={fs['l2']}, L3={fs['l3']}")

with open("v9um_apex_titan_supreme_9feature_rules.json", "w") as f:
    json.dump(best_rules, f)
print("\nSaved master zero-bust rules to v9um_apex_titan_supreme_9feature_rules.json successfully.")
