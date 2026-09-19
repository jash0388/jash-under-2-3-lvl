from dataset_real_all import all_real_sequences, get_runs, opp

print("="*80)
print("DIAGNOSING ALL 16 SEQUENCES UNDER BASELINE MOMENTUM:")
print("="*80)

for name, seq in all_real_sequences:
    hist = seq[:3]
    st = 0
    max_st = 0
    w, l = 0, 0
    loss_events = []
    
    for item in seq[3:]:
        sizes = [x['size'] for x in hist]
        nums = [x['number'] for x in hist]
        runs = get_runs(sizes)
        c_side, c_len = runs[-1]
        p_side, p_len = runs[-2] if len(runs) >= 2 else (opp(c_side), 0)
        p3_side, p3_len = runs[-3] if len(runs) >= 3 else (c_side, 0)
        
        alt = 0
        for r_s, r_l in reversed(runs):
            if r_l == 1: alt += 1
            else: break
            
        pred = c_side # Baseline momentum
        act = item['size']
        if pred == act:
            w += 1
            st = 0
        else:
            l += 1
            st += 1
            if st > max_st: max_st = st
            loss_events.append((item['period'], c_side, c_len, p_side, p_len, alt, act, item['number'], st))
        hist.append(item)
        
    print(f"\n{name:<35} | {w}W / {l}L | Max Streak: {max_st}")
    for p, cs, cl, ps, pl, alt_v, act, num, st_v in loss_events:
        print(f"  Period {p}: Run=({cs} x{cl}), Prev=({ps} x{pl}), Alt={alt_v} -> Act={act}({num}) [Streak {st_v}]")
