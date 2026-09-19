from dataset_real_all import all_real_sequences, get_runs, opp

# Seq Q (30S 52480 - 52494)
seq_Q = [
    {'period': '52480', 'number': 6, 'size': 'BIG'},
    {'period': '52481', 'number': 0, 'size': 'SMALL'},
    {'period': '52482', 'number': 2, 'size': 'SMALL'},
    {'period': '52483', 'number': 1, 'size': 'SMALL'},
    {'period': '52484', 'number': 7, 'size': 'BIG'},
    {'period': '52485', 'number': 7, 'size': 'BIG'},
    {'period': '52486', 'number': 8, 'size': 'BIG'},
    {'period': '52487', 'number': 4, 'size': 'SMALL'},
    {'period': '52488', 'number': 0, 'size': 'SMALL'},
    {'period': '52489', 'number': 9, 'size': 'BIG'},
    {'period': '52490', 'number': 6, 'size': 'BIG'},
    {'period': '52491', 'number': 4, 'size': 'SMALL'},
    {'period': '52492', 'number': 6, 'size': 'BIG'},
    {'period': '52493', 'number': 7, 'size': 'BIG'},
    {'period': '52494', 'number': 2, 'size': 'SMALL'},
]

# Seq R (30S 52524 - 52537)
seq_R = [
    {'period': '52524', 'number': 7, 'size': 'BIG'},
    {'period': '52525', 'number': 0, 'size': 'SMALL'},
    {'period': '52526', 'number': 5, 'size': 'BIG'},
    {'period': '52527', 'number': 7, 'size': 'BIG'},
    {'period': '52528', 'number': 2, 'size': 'SMALL'},
    {'period': '52529', 'number': 8, 'size': 'BIG'},
    {'period': '52530', 'number': 3, 'size': 'SMALL'},
    {'period': '52531', 'number': 5, 'size': 'BIG'},
    {'period': '52532', 'number': 6, 'size': 'BIG'},
    {'period': '52533', 'number': 6, 'size': 'BIG'},
    {'period': '52534', 'number': 9, 'size': 'BIG'},
    {'period': '52535', 'number': 7, 'size': 'BIG'},
    {'period': '52536', 'number': 8, 'size': 'BIG'},
    {'period': '52537', 'number': 4, 'size': 'SMALL'},
]

# Seq S (30S 52570 - 52585 Extended Live Sequence)
seq_S = [
    {'period': '52570', 'number': 1, 'size': 'SMALL'},
    {'period': '52571', 'number': 4, 'size': 'SMALL'},
    {'period': '52572', 'number': 3, 'size': 'SMALL'},
    {'period': '52573', 'number': 3, 'size': 'SMALL'},
    {'period': '52574', 'number': 7, 'size': 'BIG'},
    {'period': '52575', 'number': 0, 'size': 'SMALL'},
    {'period': '52576', 'number': 5, 'size': 'BIG'},
    {'period': '52577', 'number': 7, 'size': 'BIG'},
    {'period': '52578', 'number': 2, 'size': 'SMALL'},
    {'period': '52579', 'number': 8, 'size': 'BIG'},
    {'period': '52580', 'number': 3, 'size': 'SMALL'},
    {'period': '52581', 'number': 5, 'size': 'BIG'},
    {'period': '52582', 'number': 6, 'size': 'BIG'},
    {'period': '52583', 'number': 0, 'size': 'SMALL'},
    {'period': '52584', 'number': 8, 'size': 'BIG'},
    {'period': '52585', 'number': 1, 'size': 'SMALL'},
]

all_18_seqs = all_real_sequences + [
    ("Seq Q (30S 52480 - Live)", seq_Q),
    ("Seq R (30S 52524 - Live)", seq_R),
    ("Seq S (30S 52570 - Live Extended)", seq_S),
]

if __name__ == "__main__":
    print(f"Total sequences: {len(all_18_seqs)}, Total draws: {sum(len(s[1]) for s in all_18_seqs)}")
