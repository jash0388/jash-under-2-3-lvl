from solve_all_seven import all_seven, opp, get_runs
import itertools

def evaluate_all(predictor_fn):
    results = []
    max_all = 0
    for name, seq in all_seven:
        history = seq[:3]
        wins = 0
        losses = 0
        streak = 0
        max_streak = 0
        details = []
        for item in seq[3:]:
            pred, tag = predictor_fn(history, streak)
            act = item['size']
            if pred == act:
                wins += 1
                details.append((item['period'], pred, act, 'WIN', streak + 1, tag))
                streak = 0
            else:
                losses += 1
                streak += 1
                if streak > max_streak: max_streak = streak
                details.append((item['period'], pred, act, 'LOSS', streak, tag))
            history.append(item)
        if max_streak > max_all: max_all = max_streak
        results.append((name, wins, losses, max_streak, details))
    return max_all, results

def analyze_losses_deeply():
    # Let us examine why streaks happen and design precise logic for each type of sequence
    # What are the 7 sequences?
    # Seq A: [B, B, S, S, S, S, B, S, S, B, S, S]
    # Seq B: [S, B, B, S, B, S, S, S, B, S]
    # Seq C: [B, B, S, B, B, S, B, S, S, S, B, B, S]
    # Seq D: [S, S, S, S, S, S, B, B, B, S]
    # Seq E: [S, B, B, S, B, S, S, S, S, S, S, B, B, S, B, B, S, B, B, S]
    # Seq F: [S, B, B, S, B, S, S, S, B, S, S, S, B, S, S, S, B, B]
    # Seq G: [B, B, B, B, S, S, S, S, S, S, S, B, S, B, B, S, B, B, B, S]

    # Let us look at what predictor produces max consecutive losses <= 2 on all 7 sequences:
    # Let's test a neural/rule hybrid:
    pass

if __name__ == '__main__':
    print("Analyze losses deeply")
