from test_v46 import predict_apex_titan_v46_trend_reversion
from million_rounds_deep_research import test_candidate_both_ways

print("=== BENCHMARKING APEX TITAN V46 ACROSS 2,000,000 ROUNDS ===")
test_candidate_both_ways(predict_apex_titan_v46_trend_reversion, "Apex Titan V46 Trend Reversion & Quantum Inversion Shield")
