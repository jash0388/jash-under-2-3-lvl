from test_all_three_seqs import seq_A, seq_B, seq_C, test_on_all_seqs, opp
from million_rounds_deep_research import million_data, test_candidate_both_ways

def predict_triplet_matrix(history, loss_streak):
    sizes = [h['size'] for h in history]
    if len(sizes) < 3:
        return "BIG", "INITIALIZING"
        
    last3 = tuple(sizes[-3:]) # (t-2, t-1, t)
    s1, s2, s3 = last3
    
    # Calculate streak of current size
    streak = 1
    for i in range(len(sizes)-2, -1, -1):
        if sizes[i] == s3: streak += 1
        else: break
        
    # Triplet Deterministic Pattern Dispatcher:
    # 1. 'BBB': Dragon -> Follow BIG unless fatigue (>7)
    # 2. 'SSS': Dragon -> Follow SMALL unless fatigue (>7)
    # 3. 'BSB': 1-1 Chop -> Flip to SMALL
    # 4. 'SBS': 1-1 Chop -> Flip to BIG
    # 5. 'BSS': Doublet of S completed -> Flip to BIG
    # 6. 'SBB': Doublet of B completed -> Flip to SMALL
    # 7. 'SSB': 1st ball of B after SS -> In doublets it repeats to BB!
    # 8. 'BBS': 1st ball of S after BB -> In doublets it repeats to SS!
    
    if s1 == "BIG" and s2 == "BIG" and s3 == "BIG":
        if streak > 7:
            pred = "SMALL"
            reg = f"⚖️ FATIGUE CUT (BIG x{streak})"
        else:
            pred = "BIG"
            reg = f"🐉 DRAGON FLOW (BIG x{streak})"
            
    elif s1 == "SMALL" and s2 == "SMALL" and s3 == "SMALL":
        if streak > 7:
            pred = "BIG"
            reg = f"⚖️ FATIGUE CUT (SMALL x{streak})"
        else:
            pred = "SMALL"
            reg = f"🐉 DRAGON FLOW (SMALL x{streak})"
            
    elif s1 == "BIG" and s2 == "SMALL" and s3 == "BIG":
        pred = "SMALL"
        reg = "⚡ CHOP OSCILLATE (B-S-B -> S)"
        
    elif s1 == "SMALL" and s2 == "BIG" and s3 == "SMALL":
        pred = "BIG"
        reg = "⚡ CHOP OSCILLATE (S-B-S -> B)"
        
    elif s1 == "BIG" and s2 == "SMALL" and s3 == "SMALL":
        pred = "BIG"
        reg = "⚡ DOUBLET CUT (B-S-S -> B)"
        
    elif s1 == "SMALL" and s2 == "BIG" and s3 == "BIG":
        pred = "SMALL"
        reg = "⚡ DOUBLET CUT (S-B-B -> S)"
        
    elif s1 == "SMALL" and s2 == "SMALL" and s3 == "BIG":
        # We had SS, now 1st B. In doublet symmetry (2-2 or 1-2), B pairs up with B2!
        pred = "BIG"
        reg = "👥 DOUBLET PAIR (S-S-B -> B)"
        
    elif s1 == "BIG" and s2 == "BIG" and s3 == "SMALL":
        # We had BB, now 1st S. In doublet symmetry (2-2 or 1-2), S pairs up with S2!
        pred = "SMALL"
        reg = "👥 DOUBLET PAIR (B-B-S -> S)"
        
    else:
        pred = s3
        reg = "🌊 MOMENTUM"

    # Emergency Level 3 Dragon/Fatigue Lock
    if loss_streak >= 2:
        if streak >= 3:
            pred = s3
            reg = f"🛑 LVL 3 DRAGON LOCK ({s3} x{streak})"

    return pred, reg

test_on_all_seqs(predict_triplet_matrix, "Deterministic Triplet State Machine (Apex Titan V41)")

print("\n=== BENCHMARKING ON 2,000,000 ROUNDS ===")
test_candidate_both_ways(predict_triplet_matrix, "Deterministic Triplet State Machine (Apex Titan V41)")
