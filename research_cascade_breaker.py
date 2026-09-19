import json

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

seq_D_30s = [
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

# Latest user screenshot 1: periods 10385 to 10395 (Streak of 5 losses)
seq_I_10387 = [
    {'period': '10385', 'number': 3, 'size': 'SMALL'},
    {'period': '10386', 'number': 4, 'size': 'SMALL'},
    {'period': '10387', 'number': 6, 'size': 'BIG'},
    {'period': '10388', 'number': 5, 'size': 'BIG'},
    {'period': '10389', 'number': 0, 'size': 'SMALL'},
    {'period': '10390', 'number': 1, 'size': 'SMALL'},
    {'period': '10391', 'number': 4, 'size': 'SMALL'},
    {'period': '10392', 'number': 9, 'size': 'BIG'},
]

seq_J_10412 = [
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

seq_K_10550 = [
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

# Latest user screenshot 2: periods 10720 to 10730
seq_L_10722 = [
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

all_12_seqs = [
    ("Seq A (10859-10870 1M)", seq_A),
    ("Seq B (10954-10963 1M)", seq_B),
    ("Seq C (11015-11027 1M)", seq_C),
    ("Seq D (52065-52074 30S)", seq_D_30s),
    ("Seq E (11034-11053 1M)", seq_E),
    ("Seq F (11058-11075 1M)", seq_F),
    ("Seq G (11080-11099 1M)", seq_G),
    ("Seq H (11119-11141 1M)", seq_H),
    ("Seq I (10385-10392 1M - Screenshot 1)", seq_I_10387),
    ("Seq J (10410-10418 1M - Screenshot 1)", seq_J_10412),
    ("Seq K (10548-10556 1M - Screenshot 1)", seq_K_10550),
    ("Seq L (10720-10729 1M - Screenshot 2)", seq_L_10722),
]

def opp(s): return "SMALL" if s == "BIG" else "BIG"

def get_runs(sizes):
    runs = []
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

def test_engine(predictor_fn):
    total_max = 0
    results = []
    for name, seq in all_12_seqs:
        hist = []
        loss_streak = 0
        max_loss = 0
        wins, losses = 0, 0
        details = []
        for r in seq:
            if len(hist) < 3:
                hist.append(r)
                continue
            pred, tag = predictor_fn(hist, loss_streak)
            won = (pred == r['size'])
            if won:
                wins += 1
                details.append((r['period'], pred, r['size'], 'WIN', loss_streak + 1, tag))
                loss_streak = 0
            else:
                losses += 1
                loss_streak += 1
                max_loss = max(max_loss, loss_streak)
                details.append((r['period'], pred, r['size'], 'LOSS', loss_streak, tag))
            hist.append(r)
        total_max = max(total_max, max_loss)
        results.append((name, wins, losses, max_loss, details))
    return total_max, results
