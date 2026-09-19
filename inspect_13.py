from research_cascade_breaker import all_12_seqs, get_runs, opp

seq_M = [
    {'period': '10785', 'number': 6, 'size': 'BIG'},
    {'period': '10786', 'number': 8, 'size': 'BIG'},
    {'period': '10787', 'number': 1, 'size': 'SMALL'},
    {'period': '10788', 'number': 1, 'size': 'SMALL'},
    {'period': '10789', 'number': 4, 'size': 'SMALL'},
    {'period': '10790', 'number': 4, 'size': 'SMALL'},
    {'period': '10791', 'number': 1, 'size': 'SMALL'},
    {'period': '10792', 'number': 5, 'size': 'BIG'},
    {'period': '10793', 'number': 8, 'size': 'BIG'},
]

all_13_seqs = all_12_seqs + [("Seq M (10785-10793 Screenshot 3)", seq_M)]

# Let's inspect where Level 3 occurs across all sequences.
# In any sequence, what are the exact states where loss_streak >= 2 occurs?

for name, seq in all_13_seqs:
    print(f"\n--- {name} ---")
    sizes = [x['size'] for x in seq]
    nums = [x['number'] for x in seq]
    print("Sizes:", " ".join(sizes))
    print("Nums: ", " ".join(str(n) for n in nums))
