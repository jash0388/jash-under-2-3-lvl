from test_markov_ai import predict_self_learning_markov
from million_rounds_deep_research import test_candidate_both_ways

print("=== BENCHMARKING SELF-LEARNING DYNAMIC MARKOV ENGINE ON 2,000,000 ROUNDS ===")
test_candidate_both_ways(predict_self_learning_markov, "Self-Learning Dynamic Markov & Bayesian Prior Engine")
