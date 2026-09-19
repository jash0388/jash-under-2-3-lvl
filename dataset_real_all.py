import random
import math
from collections import defaultdict

# --- ALL 17 REAL MARKET SEQUENCES FROM ALL SCREENSHOTS ---

seq_A = [
    {'period': '10859', 'number': 8, 'size': 'BIG'},
    {'period': '10860', 'number': 8, 'size': 'BIG'},
    {'period': '10861', 'number': 0, 'size': 'SMALL'},
    {'period': '10862', 'number': 2, 'size': 'SMALL'},
    {'period': '10863', 'number': 4, 'size': 'SMALL'},
    {'period': '10864', 'number': 2, 'size': 'SMALL'},
    {'period': '10865', 'number': 9, 'size': 'BIG'},
    {'period': '10866', 'number': 0, 'size': 'SMALL'},
    {'period': '10867', 'number': 0, 'size': 'SMALL'},
    {'period': '10868', 'number': 6, 'size': 'BIG'},
    {'period': '10869', 'number': 3, 'size': 'SMALL'},
    {'period': '10870', 'number': 1, 'size': 'SMALL'},
]

seq_B = [
    {'period': '10954', 'number': 2, 'size': 'SMALL'},
    {'period': '10955', 'number': 5, 'size': 'BIG'},
    {'period': '10956', 'number': 9, 'size': 'BIG'},
    {'period': '10957', 'number': 4, 'size': 'SMALL'},
    {'period': '10958', 'number': 8, 'size': 'BIG'},
    {'period': '10959', 'number': 2, 'size': 'SMALL'},
    {'period': '10960', 'number': 4, 'size': 'SMALL'},
    {'period': '10961', 'number': 3, 'size': 'SMALL'},
    {'period': '10962', 'number': 5, 'size': 'BIG'},
    {'period': '10963', 'number': 4, 'size': 'SMALL'},
]

seq_C = [
    {'period': '11015', 'number': 9, 'size': 'BIG'},
    {'period': '11016', 'number': 7, 'size': 'BIG'},
    {'period': '11017', 'number': 2, 'size': 'SMALL'},
    {'period': '11018', 'number': 9, 'size': 'BIG'},
    {'period': '11019', 'number': 8, 'size': 'BIG'},
    {'period': '11020', 'number': 3, 'size': 'SMALL'},
    {'period': '11021', 'number': 9, 'size': 'BIG'},
    {'period': '11022', 'number': 3, 'size': 'SMALL'},
    {'period': '11023', 'number': 0, 'size': 'SMALL'},
    {'period': '11024', 'number': 0, 'size': 'SMALL'},
    {'period': '11025', 'number': 8, 'size': 'BIG'},
    {'period': '11026', 'number': 7, 'size': 'BIG'},
    {'period': '11027', 'number': 2, 'size': 'SMALL'},
]

seq_D = [
    {'period': '52065', 'number': 1, 'size': 'SMALL'},
    {'period': '52066', 'number': 3, 'size': 'SMALL'},
    {'period': '52067', 'number': 2, 'size': 'SMALL'},
    {'period': '52068', 'number': 0, 'size': 'SMALL'},
    {'period': '52069', 'number': 4, 'size': 'SMALL'},
    {'period': '52070', 'number': 0, 'size': 'SMALL'},
    {'period': '52071', 'number': 8, 'size': 'BIG'},
    {'period': '52072', 'number': 6, 'size': 'BIG'},
    {'period': '52073', 'number': 7, 'size': 'BIG'},
    {'period': '52074', 'number': 2, 'size': 'SMALL'},
]

seq_E = [
    {'period': '11034', 'number': 0, 'size': 'SMALL'},
    {'period': '11035', 'number': 6, 'size': 'BIG'},
    {'period': '11036', 'number': 7, 'size': 'BIG'},
    {'period': '11037', 'number': 4, 'size': 'SMALL'},
    {'period': '11038', 'number': 5, 'size': 'BIG'},
    {'period': '11039', 'number': 4, 'size': 'SMALL'},
    {'period': '11040', 'number': 2, 'size': 'SMALL'},
    {'period': '11041', 'number': 0, 'size': 'SMALL'},
    {'period': '11042', 'number': 0, 'size': 'SMALL'},
    {'period': '11043', 'number': 4, 'size': 'SMALL'},
    {'period': '11044', 'number': 4, 'size': 'SMALL'},
    {'period': '11045', 'number': 7, 'size': 'BIG'},
    {'period': '11046', 'number': 9, 'size': 'BIG'},
    {'period': '11047', 'number': 2, 'size': 'SMALL'},
    {'period': '11048', 'number': 5, 'size': 'BIG'},
    {'period': '11049', 'number': 8, 'size': 'BIG'},
    {'period': '11050', 'number': 4, 'size': 'SMALL'},
    {'period': '11051', 'number': 5, 'size': 'BIG'},
    {'period': '11052', 'number': 5, 'size': 'BIG'},
    {'period': '11053', 'number': 1, 'size': 'SMALL'},
]

seq_F = [
    {'period': '11058', 'number': 3, 'size': 'SMALL'},
    {'period': '11059', 'number': 8, 'size': 'BIG'},
    {'period': '11060', 'number': 9, 'size': 'BIG'},
    {'period': '11061', 'number': 1, 'size': 'SMALL'},
    {'period': '11062', 'number': 5, 'size': 'BIG'},
    {'period': '11063', 'number': 0, 'size': 'SMALL'},
    {'period': '11064', 'number': 1, 'size': 'SMALL'},
    {'period': '11065', 'number': 2, 'size': 'SMALL'},
    {'period': '11066', 'number': 5, 'size': 'BIG'},
    {'period': '11067', 'number': 1, 'size': 'SMALL'},
    {'period': '11068', 'number': 2, 'size': 'SMALL'},
    {'period': '11069', 'number': 3, 'size': 'SMALL'},
    {'period': '11070', 'number': 9, 'size': 'BIG'},
    {'period': '11071', 'number': 0, 'size': 'SMALL'},
    {'period': '11072', 'number': 2, 'size': 'SMALL'},
    {'period': '11073', 'number': 0, 'size': 'SMALL'},
    {'period': '11074', 'number': 6, 'size': 'BIG'},
    {'period': '11075', 'number': 6, 'size': 'BIG'},
]

seq_G = [
    {'period': '11080', 'number': 7, 'size': 'BIG'},
    {'period': '11081', 'number': 7, 'size': 'BIG'},
    {'period': '11082', 'number': 8, 'size': 'BIG'},
    {'period': '11083', 'number': 6, 'size': 'BIG'},
    {'period': '11084', 'number': 3, 'size': 'SMALL'},
    {'period': '11085', 'number': 4, 'size': 'SMALL'},
    {'period': '11086', 'number': 0, 'size': 'SMALL'},
    {'period': '11087', 'number': 2, 'size': 'SMALL'},
    {'period': '11088', 'number': 4, 'size': 'SMALL'},
    {'period': '11089', 'number': 2, 'size': 'SMALL'},
    {'period': '11090', 'number': 1, 'size': 'SMALL'},
    {'period': '11091', 'number': 9, 'size': 'BIG'},
    {'period': '11092', 'number': 1, 'size': 'SMALL'},
    {'period': '11093', 'number': 7, 'size': 'BIG'},
    {'period': '11094', 'number': 9, 'size': 'BIG'},
    {'period': '11095', 'number': 2, 'size': 'SMALL'},
    {'period': '11096', 'number': 7, 'size': 'BIG'},
    {'period': '11097', 'number': 8, 'size': 'BIG'},
    {'period': '11098', 'number': 7, 'size': 'BIG'},
    {'period': '11099', 'number': 4, 'size': 'SMALL'},
]

seq_H = [
    {'period': '11119', 'number': 3, 'size': 'SMALL'},
    {'period': '11120', 'number': 9, 'size': 'BIG'},
    {'period': '11121', 'number': 0, 'size': 'SMALL'},
    {'period': '11122', 'number': 3, 'size': 'SMALL'},
    {'period': '11123', 'number': 1, 'size': 'SMALL'},
    {'period': '11124', 'number': 9, 'size': 'BIG'},
    {'period': '11125', 'number': 5, 'size': 'BIG'},
    {'period': '11126', 'number': 1, 'size': 'SMALL'},
    {'period': '11127', 'number': 6, 'size': 'BIG'},
    {'period': '11128', 'number': 0, 'size': 'SMALL'},
    {'period': '11129', 'number': 8, 'size': 'BIG'},
    {'period': '11130', 'number': 7, 'size': 'BIG'},
    {'period': '11131', 'number': 5, 'size': 'BIG'},
    {'period': '11132', 'number': 2, 'size': 'SMALL'},
    {'period': '11133', 'number': 3, 'size': 'SMALL'},
    {'period': '11134', 'number': 6, 'size': 'BIG'},
    {'period': '11135', 'number': 7, 'size': 'BIG'},
    {'period': '11136', 'number': 4, 'size': 'SMALL'},
    {'period': '11137', 'number': 9, 'size': 'BIG'},
    {'period': '11138', 'number': 4, 'size': 'SMALL'},
    {'period': '11139', 'number': 7, 'size': 'BIG'},
    {'period': '11140', 'number': 0, 'size': 'SMALL'},
    {'period': '11141', 'number': 7, 'size': 'BIG'},
]

seq_I = [
    {'period': '10385', 'number': 3, 'size': 'SMALL'},
    {'period': '10386', 'number': 4, 'size': 'SMALL'},
    {'period': '10387', 'number': 6, 'size': 'BIG'},
    {'period': '10388', 'number': 5, 'size': 'BIG'},
    {'period': '10389', 'number': 0, 'size': 'SMALL'},
    {'period': '10390', 'number': 1, 'size': 'SMALL'},
    {'period': '10391', 'number': 4, 'size': 'SMALL'},
    {'period': '10392', 'number': 9, 'size': 'BIG'},
]

seq_J = [
    {'period': '10410', 'number': 8, 'size': 'BIG'},
    {'period': '10411', 'number': 7, 'size': 'BIG'},
    {'period': '10412', 'number': 0, 'size': 'SMALL'},
    {'period': '10413', 'number': 2, 'size': 'SMALL'},
    {'period': '10414', 'number': 9, 'size': 'BIG'},
    {'period': '10415', 'number': 2, 'size': 'SMALL'},
    {'period': '10416', 'number': 1, 'size': 'SMALL'},
    {'period': '10417', 'number': 8, 'size': 'BIG'},
    {'period': '10418', 'number': 4, 'size': 'SMALL'},
]

seq_K = [
    {'period': '10548', 'number': 7, 'size': 'BIG'},
    {'period': '10549', 'number': 8, 'size': 'BIG'},
    {'period': '10550', 'number': 2, 'size': 'SMALL'},
    {'period': '10551', 'number': 9, 'size': 'BIG'},
    {'period': '10552', 'number': 0, 'size': 'SMALL'},
    {'period': '10553', 'number': 4, 'size': 'SMALL'},
    {'period': '10554', 'number': 6, 'size': 'BIG'},
    {'period': '10555', 'number': 6, 'size': 'BIG'},
    {'period': '10556', 'number': 4, 'size': 'SMALL'},
]

seq_L = [
    {'period': '10720', 'number': 2, 'size': 'SMALL'},
    {'period': '10721', 'number': 1, 'size': 'SMALL'},
    {'period': '10722', 'number': 7, 'size': 'BIG'},
    {'period': '10723', 'number': 0, 'size': 'SMALL'},
    {'period': '10724', 'number': 4, 'size': 'SMALL'},
    {'period': '10725', 'number': 2, 'size': 'SMALL'},
    {'period': '10726', 'number': 0, 'size': 'SMALL'},
    {'period': '10727', 'number': 7, 'size': 'BIG'},
    {'period': '10728', 'number': 0, 'size': 'SMALL'},
    {'period': '10729', 'number': 9, 'size': 'BIG'},
]

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

# NEW 30S Sequence from Screenshot 1 & 4 (52464 - 52480)
seq_N = [
    {'period': '52464', 'number': 9, 'size': 'BIG'},
    {'period': '52465', 'number': 4, 'size': 'SMALL'},
    {'period': '52466', 'number': 4, 'size': 'SMALL'},
    {'period': '52467', 'number': 5, 'size': 'BIG'},
    {'period': '52468', 'number': 8, 'size': 'BIG'},
    {'period': '52469', 'number': 6, 'size': 'BIG'},
    {'period': '52470', 'number': 5, 'size': 'BIG'},
    {'period': '52471', 'number': 5, 'size': 'BIG'},
    {'period': '52472', 'number': 4, 'size': 'SMALL'},
    {'period': '52473', 'number': 0, 'size': 'SMALL'},
    {'period': '52474', 'number': 4, 'size': 'SMALL'},
    {'period': '52475', 'number': 0, 'size': 'SMALL'},
    {'period': '52476', 'number': 8, 'size': 'BIG'},
    {'period': '52477', 'number': 8, 'size': 'BIG'},
    {'period': '52478', 'number': 0, 'size': 'SMALL'},
    {'period': '52479', 'number': 0, 'size': 'SMALL'},
    {'period': '52480', 'number': 6, 'size': 'BIG'},
]

# NEW 30S Sequence from Screenshot 2 (51819 - 51839)
seq_O = [
    {'period': '51819', 'number': 6, 'size': 'BIG'},
    {'period': '51820', 'number': 8, 'size': 'BIG'},
    {'period': '51821', 'number': 2, 'size': 'SMALL'},
    {'period': '51822', 'number': 0, 'size': 'SMALL'},
    {'period': '51823', 'number': 6, 'size': 'BIG'},
    {'period': '51824', 'number': 0, 'size': 'SMALL'},
    {'period': '51832', 'number': 0, 'size': 'SMALL'},
    {'period': '51833', 'number': 1, 'size': 'SMALL'},
    {'period': '51834', 'number': 9, 'size': 'BIG'},
    {'period': '51835', 'number': 0, 'size': 'SMALL'},
    {'period': '51836', 'number': 4, 'size': 'SMALL'},
    {'period': '51837', 'number': 4, 'size': 'SMALL'},
    {'period': '51838', 'number': 4, 'size': 'SMALL'},
    {'period': '51839', 'number': 8, 'size': 'BIG'},
]

# NEW 30S Sequence from Screenshot 3 (51989 - 52007)
seq_P = [
    {'period': '51989', 'number': 2, 'size': 'SMALL'},
    {'period': '51990', 'number': 6, 'size': 'BIG'},
    {'period': '51991', 'number': 6, 'size': 'BIG'},
    {'period': '51992', 'number': 5, 'size': 'BIG'},
    {'period': '51993', 'number': 6, 'size': 'BIG'},
    {'period': '51994', 'number': 3, 'size': 'SMALL'},
    {'period': '51995', 'number': 9, 'size': 'BIG'},
    {'period': '51996', 'number': 9, 'size': 'BIG'},
    {'period': '51997', 'number': 0, 'size': 'SMALL'},
    {'period': '52002', 'number': 9, 'size': 'BIG'},
    {'period': '52003', 'number': 9, 'size': 'BIG'},
    {'period': '52004', 'number': 3, 'size': 'SMALL'},
    {'period': '52005', 'number': 3, 'size': 'SMALL'},
    {'period': '52006', 'number': 7, 'size': 'BIG'},
    {'period': '52007', 'number': 5, 'size': 'BIG'},
]

all_real_sequences = [
    ("Seq A (1M 10859)", seq_A),
    ("Seq B (1M 10954)", seq_B),
    ("Seq C (1M 11015)", seq_C),
    ("Seq D (30S 52065)", seq_D),
    ("Seq E (1M 11034)", seq_E),
    ("Seq F (1M 11058)", seq_F),
    ("Seq G (1M 11080)", seq_G),
    ("Seq H (1M 11119)", seq_H),
    ("Seq I (1M 10385)", seq_I),
    ("Seq J (1M 10410)", seq_J),
    ("Seq K (1M 10548)", seq_K),
    ("Seq L (1M 10720)", seq_L),
    ("Seq M (1M 10785)", seq_M),
    ("Seq N (30S 52464 - Doublet Heavy)", seq_N),
    ("Seq O (30S 51819)", seq_O),
    ("Seq P (30S 51989)", seq_P),
]

def opp(s): return "SMALL" if s == "BIG" else "BIG"

def get_runs(sizes):
    runs = []
    if not sizes: return runs
    curr = sizes[0]
    l = 1
    for s in sizes[1:]:
        if s == curr: l += 1
        else:
            runs.append((curr, l))
            curr = s
            l = 1
    runs.append((curr, l))
    return runs

print(f"Loaded {len(all_real_sequences)} Real Market Sequences with {sum(len(s[1]) for s in all_real_sequences)} total real draws!")
