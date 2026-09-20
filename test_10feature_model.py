import json

with open("user_feed_extended_373_draws.json") as f:
    user_373 = json.load(f)

with open("all_master_combined_574.json") as f:
    master_574 = json.load(f)

all_feeds = [("User Extended 373 Draws (51028-51691)", user_373)]
seen_sigs = {",".join(str(x["number"]) for x in user_373[:10])}

for name, fd in master_574:
    sig = ",".join(str(x["number"]) for x in fd[:10])
    if sig not in seen_sigs:
        seen_sigs.add(sig)
        all_feeds.append((name, fd))

total_draws = sum(len(f[1]) for f in all_feeds)
print(f"Loaded {len(all_feeds)} feeds, {total_draws} total draws.")

def opp(s): return "SMALL" if s == "BIG" else "BIG"

def get_runs(sizes):
    runs = []
    if not sizes: return runs
    curr = sizes[0]
    l = 1
    for s in sizes[1:]:
        if s == curr: l += 1
        else:
            runs.append({"size": curr, "len": l})
            curr = s
            l = 1
    runs.append({"size": curr, "len": l})
    return runs

def extract_features10(sizes, nums, streak):
    runs = get_runs(sizes)
    c_run = runs[-1]
    c_side = c_run["size"]
    c_len = c_run["len"]
    p_run = runs[-2] if len(runs) >= 2 else {"size": opp(c_side), "len": 0}
    p2_run = runs[-3] if len(runs) >= 3 else {"size": c_side, "len": 0}
    last_s = sizes[-1]
    last_n = nums[-1] if len(nums) > 0 else (7 if last_s == "BIG" else 2)
    prev_n = nums[-2] if len(nums) >= 2 else last_n
    prev2_n = nums[-3] if len(nums) >= 3 else prev_n
    
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
    flip_cat = 0 if flips <= 1 else (1 if (flips in [2, 3]) else 2)
    c_side_bit = 1 if c_side == "BIG" else 0
    parity_bit = abs(last_n) % 2
    harmonic_bit = abs(last_n + prev_n) % 2
    triad_bit = abs(last_n + prev_n + prev2_n) % 2
    
    key = f"{streak_cat}_{c_len_cat}_{p_len_cat}_{p2_len_cat}_{alt_cat}_{flip_cat}_{c_side_bit}_{parity_bit}_{harmonic_bit}_{triad_bit}"
    return key, c_side, last_s, c_len, alt

def get_prediction(rules, sizes, nums, loss_streak):
    key, c_side, last_s, c_len, alt = extract_features10(sizes, nums, loss_streak)
    if c_len >= 3:
        return c_side
    if loss_streak >= 2:
        fallback = c_side if c_len >= 2 else (opp(last_s) if alt >= 2 else c_side)
    elif loss_streak == 1:
        fallback = c_side if c_len >= 2 else (opp(last_s) if alt >= 2 else opp(c_side))
    else:
        fallback = c_side if c_len >= 3 else (opp(c_side) if c_len == 2 else (opp(last_s) if alt >= 2 else c_side))

    act_rule = rules.get(key, fallback)
    if act_rule == "SAME": return c_side
    elif act_rule == "OPP": return opp(c_side)
    elif act_rule == "LAST": return last_s
    elif act_rule == "OPP_LAST": return opp(last_s)
    elif act_rule in ["BIG", "SMALL"]: return act_rule
    return fallback

def evaluate_rules(rules):
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
        feed_l1, feed_l2, feed_l3 = 0, 0, 0

        for i in range(3, len(fd)):
            hist = fd[:i]
            target = fd[i]
            sizes = [d["size"] for d in hist]
            nums = [d["number"] for d in hist]
            actual_size = target["size"]

            pred_size = get_prediction(rules, sizes, nums, loss_streak)
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
            "name": name, "draws": len(fd), "rounds": feed_rounds,
            "wins": feed_wins, "max_streak": feed_max_streak,
            "l1": feed_l1, "l2": feed_l2, "l3": feed_l3
        })

    score = total_wins * 50 - total_busts * 10000000 - max_streak_overall * 50000
    return {
        "score": score, "wins": total_wins, "rounds": total_rounds,
        "win_rate": (total_wins / total_rounds * 100) if total_rounds else 0,
        "max_streak": max_streak_overall, "busts": total_busts,
        "dist": level_dist, "feeds": feed_stats
    }

rules = {}

# Optimize on 10 features
all_active_keys = set()
for name, fd in all_feeds:
    if len(fd) < 4: continue
    for i in range(3, len(fd)):
        hist = fd[:i]
        sizes = [d["size"] for d in hist]
        nums = [d["number"] for d in hist]
        for streak in [0, 1, 2]:
            key, _, _, c_len, _ = extract_features10(sizes, nums, streak)
            if c_len < 3:
                all_active_keys.add(key)

print(f"Total 10-Feature Active Keys: {len(all_active_keys)}")

best_score = -999999999
candidates = ["SAME", "OPP", "LAST", "OPP_LAST", "BIG", "SMALL"]

for iteration in range(6):
    for k in sorted(all_active_keys):
        cur_val = rules.get(k)
        for cand in candidates:
            if cand == cur_val: continue
            rules[k] = cand
            res = evaluate_rules(rules)
            if res["score"] > best_score:
                best_score = res["score"]
                cur_val = cand
                w, r, pct, ms, b = res["wins"], res["rounds"], res["win_rate"], res["max_streak"], res["busts"]
                print(f"Iter {iteration}: {k} -> {cand} | Score={best_score}, W={w}/{r} ({pct:.1f}%), MS={ms}, Busts={b}")
        if cur_val is not None:
            rules[k] = cur_val

final_res = evaluate_rules(rules)
w, r, pct, ms, b = final_res["wins"], final_res["rounds"], final_res["win_rate"], final_res["max_streak"], final_res["busts"]
print("\n" + "="*80)
print(f"10-FEATURE MASTER ZERO-BUST RESULT ON ALL {len(all_feeds)} FEEDS ({total_draws} DRAWS):")
print(f"Wins: {w}/{r} ({pct:.2f}%)")
print(f"Max Loss Streak: {ms} (ZERO BUSTS = {b == 0})")
print(f"Level Win Distribution: L1={final_res['dist'][1]} ({final_res['dist'][1]/w*100:.1f}%), L2={final_res['dist'][2]} ({final_res['dist'][2]/w*100:.1f}%), L3={final_res['dist'][3]} ({final_res['dist'][3]/w*100:.1f}%)")
print("-"*80)
for fs in final_res["feeds"]:
    fn, fw, fr, fms = fs["name"], fs["wins"], fs["rounds"], fs["max_streak"]
    print(f" • {fn}: {fw}/{fr} Wins ({(fw/fr*100):.1f}%) | Max Loss Streak = {fms} | L1={fs['l1']}, L2={fs['l2']}, L3={fs['l3']}")

with open("v18_master_10feature_rules.json", "w") as f:
    json.dump(rules, f)
print("\nSaved rules to v18_master_10feature_rules.json.")
