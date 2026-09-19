from million_rounds_deep_research import million_data, evaluate_strategy, test_candidate_both_ways, opp

# Test Hybrid Multi-Scale Engine with Dynamic Trend/Chop Adaptive Hysteresis
def predict_apex_ultra(history, loss_streak):
    sizes = [h['size'] for h in history[-30:]]
    last = sizes[-1]
    
    # 1. Streak Length
    streak = 1
    for i in range(len(sizes)-2, -1, -1):
        if sizes[i] == last: streak += 1
        else: break
        
    # 2. Alternation (Chop) Length
    alt = 1
    for i in range(len(sizes)-1, 0, -1):
        if sizes[i] != sizes[i-1]: alt += 1
        else: break
        
    # 3. Micro-regime volatility in last 10 rounds
    # Count flips in last 10 rounds
    flips = sum(1 for i in range(len(sizes)-1, max(0, len(sizes)-10), -1) if sizes[i] != sizes[i-1])
    is_high_volatility = flips >= 5  # Chop heavy market

    # LEVEL 3 EMERGENCY RECOVERY (loss_streak >= 2)
    if loss_streak >= 2:
        if is_high_volatility:
            # In chop market, always oscillate
            return opp(last), f'🛑 LVL 3 VOLATILITY FLIP (x{alt})'
        else:
            # In trend market, always ride momentum
            return last, f'🛑 LVL 3 TREND LOCK ({last} x{streak})'

    # LEVEL 2 RECOVERY (loss_streak == 1)
    elif loss_streak == 1:
        if alt >= 3:
            return opp(last), f'🛡️ LVL 2 CHOP FLIP (x{alt})'
        elif streak >= 2:
            return last, f'🛡️ LVL 2 DRAGON PERSIST ({last} x{streak})'
        elif is_high_volatility:
            return opp(last), f'🛡️ LVL 2 VOLATILITY FLIP'
        else:
            return last, f'🛡️ LVL 2 MOMENTUM ({last})'

    # LEVEL 1 NORMAL FLOW
    else:
        if streak >= 3 and streak <= 7:
            return last, f'🐉 DRAGON FLOW ({last} x{streak})'
        elif streak > 7:
            return opp(last), f'⚖️ FATIGUE CUT (x{streak})'
        elif alt >= 3:
            return opp(last), f'⚡ CHOP OSCILLATE (x{alt})'
        elif is_high_volatility and alt >= 2:
            return opp(last), f'⚡ VOLATILITY OSCILLATE (x{alt})'
        else:
            return last, f'🌊 FLOW MOMENTUM ({last})'

test_candidate_both_ways(predict_apex_ultra, "Apex Titan Ultra (Adaptive Volatility Hysteresis)")
