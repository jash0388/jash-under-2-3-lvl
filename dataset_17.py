from dataset_real_all import all_real_sequences, get_runs, opp

# Add latest live sequence (Screenshot 52480 - 52494)
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

all_17_seqs = all_real_sequences + [("Seq Q (30S 52480 - Latest Live)", seq_Q)]

print(f"Total sequences: {len(all_17_seqs)}, Total draws: {sum(len(s[1]) for s in all_17_seqs)}")
