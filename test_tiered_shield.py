from dataset_real_all import all_real_sequences
from test_regime_shield import rows, get_runs, opp

all_eval = [('User 244 Draws', rows)] + all_real_sequences

def sim_ensemble():
    total_wins = 0
    total_losses = 0
    global_max = 0
    streak_counts = {}
    
    for name, seq in all_eval:
        if len(seq) < 4: continue
        loss_streak = 0
        for i in range(3, len(seq)):
            hist = seq[:i]
            act = seq[i]['size']
            sizes = [x['size'] for x in hist]
            runs = get_runs(sizes)
            cRun = runs[-1]
            cSide = cRun['size']
            cLen = cRun['len']
            lastS = sizes[-1]
            
            alt = 0
            for r in reversed(runs):
                if r['len'] == 1: alt += 1
                else: break
                
            # --- TIERED HARMONIC SHIELD ---
            # Level 1: Momentum & Doublet Cutting
            # Level 2: Anti-Trap Recovery
            # Level 3: Invariant Dragon/Chop Lock
            
            if loss_streak == 0:
                if cLen >= 3:
                    pred = cSide # Dragon Ride
                elif cLen == 2:
                    pred = opp(cSide) # Doublet Cut
                elif alt >= 2:
                    pred = opp(lastS) # Chop Ride
                else:
                    pred = cSide # Base Follow
            elif loss_streak == 1:
                # Level 2 Recovery: If doublet cut failed, dragon is confirmed -> Ride Dragon!
                if cLen >= 3:
                    pred = cSide
                elif cLen == 2:
                    pred = opp(cSide)
                elif alt >= 3:
                    pred = opp(lastS)
                elif alt == 2:
                    pred = cSide
                else:
                    pred = opp(cSide)
            else:
                # Level 3 Recovery: ABSOLUTE SHIELD
                # Never fight dragon >= 2
                if cLen >= 2:
                    pred = cSide
                elif alt >= 2:
                    pred = opp(lastS)
                else:
                    pred = cSide
                    
            if pred == act:
                total_wins += 1
                loss_streak = 0
            else:
                total_losses += 1
                loss_streak += 1
                streak_counts[loss_streak] = streak_counts.get(loss_streak, 0) + 1
                if loss_streak > global_max: global_max = loss_streak
                
    print(f'Tiered Harmonic Shield: Wins={total_wins}, Losses={total_losses}, WinRate={total_wins/(total_wins+total_losses)*100:.1f}%, Global Max Loss={global_max}')
    print(f'Streak distribution: {streak_counts}')

sim_ensemble()
