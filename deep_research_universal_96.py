import json
from dataset_real_all import all_real_sequences, get_runs, opp

with open('user_live_95_draws.json', 'r') as f:
    seq_live_96 = json.load(f)

print(f"Loaded live sequence with {len(seq_live_96)} draws.")

# Analyze run distributions in the 96 live draws
sizes = [x['size'] for x in seq_live_96]
runs = get_runs(sizes)

print(f"Total runs: {len(runs)}")
run_lengths = {}
for r, l in runs:
    run_lengths[l] = run_lengths.get(l, 0) + 1

print("Run length distribution in the 96 live draws:")
for l in sorted(run_lengths.keys()):
    print(f"  Length {l}: {run_lengths[l]} times ({(run_lengths[l]/len(runs))*100:.1f}%)")

# Let's inspect all sequences
all_30s_dataset = [
    ("Seq D (30S 52065)", [s for s in all_real_sequences if s[0].startswith('Seq D')][0][1]),
    ("Seq N (30S 52464 - Doublet Heavy)", [s for s in all_real_sequences if s[0].startswith('Seq N')][0][1]),
    ("Seq O (30S 51819)", [s for s in all_real_sequences if s[0].startswith('Seq O')][0][1]),
    ("Seq P (30S 51989)", [s for s in all_real_sequences if s[0].startswith('Seq P')][0][1]),
    ("Seq Master 96-Draw Live Feed (50579-50739)", seq_live_96)
]

print(f"\nTotal testing draws in unified dataset: {sum(len(s[1]) for s in all_30s_dataset)}")
