import random
import copy
from dataset_real_all import all_real_sequences
import re

raw_user = '''
…00051548	7	SMALL 2	BIG 7	LOSSL3
…00051547	9	SMALL 2	BIG 9	LOSSL3
…00051546	8	SMALL 2	BIG 8	LOSSL3
…00051545	8	SMALL 2	BIG 8	LOSSL3
…00051544	9	SMALL 1	BIG 9	LOSSL3
…00051543	6	SMALL 3	BIG 6	LOSSL3
…00051542	5	SMALL 3	BIG 5	LOSSL3
…00051541	6	SMALL 3	BIG 6	LOSSL2
…00051540	8	SMALL 3	BIG 8	LOSSL1
…00051539	4	SMALL 3	SMALL 4	WINL2
…00051538	9	SMALL 3	BIG 9	LOSSL1
…00051537	9	BIG 6	BIG 9	WINL1
…00051536	4	SMALL 0	SMALL 4	WINL3
…00051535	7	SMALL 0	BIG 7	LOSSL3
…00051534	2	BIG 7	SMALL 2	LOSSL3
…00051533	1	BIG 6	SMALL 1	LOSSL2
…00051532	1	BIG 6	SMALL 1	LOSSL1
…00051531	5	BIG 6	BIG 5	WINL1
…00051530	5	BIG 7	BIG 5	WINL1
…00051529	9	BIG 7	BIG 9	WINL3
…00051528	3	BIG 7	SMALL 3	LOSSL2
…00051527	2	BIG 7	SMALL 2	LOSSL1
…00051526	1	SMALL 2	SMALL 1	WINL1
…00051525	8	BIG 8	BIG 8	WINL3
…00051524	0	BIG 8	SMALL 0	LOSSL3
…00051523	7	SMALL 2	BIG 7	LOSSL2
…00051522	5	SMALL 2	BIG 5	LOSSL1
…00051521	9	BIG 7	BIG 9	WINL1
…00051520	6	BIG 7	BIG 6	WINL1
…00051519	1	SMALL 1	SMALL 1	WINL1
…00051518	0	SMALL 1	SMALL 0	WINL1
…00051517	4	SMALL 1	SMALL 4	WINL2
…00051516	0	BIG 6	SMALL 0	LOSSL1
…00051515	9	BIG 6	BIG 9	WINL1
…00051514	4	SMALL 0	SMALL 4	WINL1
…00051513	3	SMALL 3	SMALL 3	WINL1
…00051512	2	SMALL 3	SMALL 2	WINL2
…00051511	4	BIG 5	SMALL 4	LOSSL1
…00051510	8	BIG 8	BIG 8	WINL2
…00051509	4	BIG 8	SMALL 4	LOSSL1
…00051508	2	SMALL 0	SMALL 2	WINL2
…00051507	1	BIG 8	SMALL 1	LOSSL1
…00051506	7	BIG 8	BIG 7	WINL1
…00051505	1	SMALL 1	SMALL 1	WINL1
…00051504	4	SMALL 1	SMALL 4	WINL1
…00051503	6	BIG 8	BIG 6	WINL1
…00051502	6	BIG 6	BIG 6	WINL3
…00051501	3	BIG 6	SMALL 3	LOSSL2
…00051500	2	BIG 6	SMALL 2	LOSSL1
…00051499	7	BIG 8	BIG 7	WINL2
…00051498	4	BIG 8	SMALL 4	LOSSL1
…00051497	2	SMALL 2	SMALL 2	WINL1
…00051496	7	BIG 8	BIG 7	WINL1
…00051495	3	SMALL 2	SMALL 3	WINL2
…00051494	0	BIG 5	SMALL 0	LOSSL1
…00051493	4	SMALL 2	SMALL 4	WINL3
…00051492	1	BIG 5	SMALL 1	LOSSL3
…00051491	0	BIG 5	SMALL 0	LOSSL2
…00051490	4	BIG 5	SMALL 4	LOSSL1
…00051489	6	BIG 6	BIG 6	WINL1
…00051488	7	BIG 6	BIG 7	WINL1
…00051487	7	BIG 7	BIG 7	WINL2
…00051486	1	BIG 7	SMALL 1	LOSSL1
…00051480	0	SMALL 2	SMALL 0	WINL2
…00051479	6	SMALL 2	BIG 6	LOSSL1
…00051478	0	SMALL 1	SMALL 0	WINL3
…00051477	0	BIG 5	SMALL 0	LOSSL3
…00051476	4	BIG 5	SMALL 4	LOSSL3
…00051475	7	SMALL 0	BIG 7	LOSSL2
…00051474	8	SMALL 3	BIG 8	LOSSL1
…00051473	3	SMALL 3	SMALL 3	WINL2
…00051472	1	BIG 7	SMALL 1	LOSSL1
…00051471	6	BIG 7	BIG 6	WINL1
…00051470	2	SMALL 3	SMALL 2	WINL1
…00051469	4	SMALL 3	SMALL 4	WINL3
…00051468	2	BIG 7	SMALL 2	LOSSL2
…00051467	1	BIG 7	SMALL 1	LOSSL1
…00051466	6	BIG 7	BIG 6	WINL1
…00051465	6	BIG 7	BIG 6	WINL1
…00051464	0	SMALL 2	SMALL 0	WINL1
…00051463	4	SMALL 2	SMALL 4	WINL3
…00051462	9	SMALL 1	BIG 9	LOSSL2
…00051461	1	BIG 7	SMALL 1	LOSSL1
…00051460	5	BIG 7	BIG 5	WINL1
…00051459	2	SMALL 2	SMALL 2	WINL1
…00051458	4	SMALL 4	SMALL 4	WINL1
…00051457	0	SMALL 4	SMALL 0	WINL2
…00051456	0	BIG 7	SMALL 0	LOSSL1
…00051455	6	BIG 7	BIG 6	WINL3
…00051454	3	BIG 7	SMALL 3	LOSSL2
…00051453	3	BIG 7	SMALL 3	LOSSL1
…00051452	2	SMALL 2	SMALL 2	WINL1
…00051451	6	BIG 7	BIG 6	WINL3
…00051450	0	BIG 7	SMALL 0	LOSSL3
…00051449	1	BIG 7	SMALL 1	LOSSL3
…00051448	3	BIG 7	SMALL 3	LOSSL2
…00051447	1	BIG 7	SMALL 1	LOSSL1
…00051446	4	SMALL 1	SMALL 4	WINL1
…00051445	0	SMALL 1	SMALL 0	WINL1
…00051444	5	BIG 7	BIG 5	WINL1
…00051443	2	SMALL 1	SMALL 2	WINL3
…00051442	6	SMALL 1	BIG 6	LOSSL3
…00051441	0	BIG 7	SMALL 0	LOSSL3
…00051440	2	BIG 7	SMALL 2	LOSSL3
…00051439	2	BIG 7	SMALL 2	LOSSL3
…00051438	9	SMALL 2	BIG 9	LOSSL2
…00051392	0	BIG 7	SMALL 0	LOSSL1
…00051391	4	SMALL 1	SMALL 4	WINL2
…00051390	5	SMALL 1	BIG 5	LOSSL1
…00051389	4	SMALL 1	SMALL 4	WINL3
…00051388	3	BIG 7	SMALL 3	LOSSL2
…00051387	4	BIG 7	SMALL 4	LOSSL1
…00051386	5	BIG 7	BIG 5	WINL2
…00051263	6	SMALL 2	BIG 6	LOSSL1
…00051262	0	SMALL 2	SMALL 0	WINL3
…00051261	9	SMALL 2	BIG 9	LOSSL2
…00051260	7	SMALL 2	BIG 7	LOSSL1
…00051259	7	BIG 6	BIG 7	WINL3
…00051258	4	BIG 6	SMALL 4	LOSSL3
…00051257	5	SMALL 2	BIG 5	LOSSL2
…00051256	7	SMALL 2	BIG 7	LOSSL1
…00051255	1	SMALL 2	SMALL 1	WINL1
…00051254	3	SMALL 2	SMALL 3	WINL3
…00051253	8	SMALL 2	BIG 8	LOSSL3
…00051252	8	SMALL 2	BIG 8	LOSSL2
…00051251	4	BIG 7	SMALL 4	LOSSL1
…00051219	4	SMALL 1	SMALL 4	WINL1
…00051218	6	BIG 6	BIG 6	WINL2
…00051217	0	BIG 6	SMALL 0	LOSSL1
…00051216	8	BIG 6	BIG 8	WINL1
…00051215	5	BIG 6	BIG 5	WINL3
…00051214	2	BIG 6	SMALL 2	LOSSL2
…00051213	2	BIG 6	SMALL 2	LOSSL1
…00051212	7	BIG 6	BIG 7	WINL1
…00051211	9	BIG 6	BIG 9	WINL3
…00051210	8	SMALL 2	BIG 8	LOSSL2
…00051209	4	BIG 6	SMALL 4	LOSSL1
…00051208	9	BIG 6	BIG 9	WINL2
…00051207	7	SMALL 2	BIG 7	LOSSL1
…00051206	9	BIG 6	BIG 9	WINL2
…00051205	8	SMALL 1	BIG 8	LOSSL1
…00051204	9	BIG 6	BIG 9	WINL1
…00051203	9	BIG 6	BIG 9	WINL2
…00051202	9	SMALL 1	BIG 9	LOSSL1
…00051201	7	BIG 7	BIG 7	WINL3
…00051200	3	BIG 7	SMALL 3	LOSSL3
…00051199	1	BIG 7	SMALL 1	LOSSL2
…00051198	0	BIG 7	SMALL 0	LOSSL1
…00051197	2	SMALL 1	SMALL 2	WINL1
…00051196	4	SMALL 1	SMALL 4	WINL3
…00051195	2	BIG 7	SMALL 2	LOSSL2
…00051194	4	BIG 7	SMALL 4	LOSSL1
…00051193	9	BIG 7	BIG 9	WINL2
…00051192	6	SMALL 2	BIG 6	LOSSL1
…00051191	4	SMALL 2	SMALL 4	WINL3
…00051190	3	BIG 7	SMALL 3	LOSSL3
…00051189	8	SMALL 2	BIG 8	LOSSL2
…00051188	0	BIG 6	SMALL 0	LOSSL1
…00051187	9	BIG 6	BIG 9	WINL1
…00051186	8	BIG 6	BIG 8	WINL2
…00051185	0	BIG 6	SMALL 0	LOSSL1
…00051184	5	BIG 6	BIG 5	WINL3
…00051183	4	BIG 6	SMALL 4	LOSSL2
…00051182	3	BIG 6	SMALL 3	LOSSL1
…00051181	5	BIG 6	BIG 5	WINL1
…00051180	0	SMALL 2	SMALL 0	WINL3
…00051179	4	BIG 6	SMALL 4	LOSSL2
…00051178	7	SMALL 2	BIG 7	LOSSL1
…00051177	3	SMALL 2	SMALL 3	WINL3
…00051176	8	SMALL 2	BIG 8	LOSSL2
…00051175	4	BIG 7	SMALL 4	LOSSL1
…00051174	8	BIG 7	BIG 8	WINL3
…00051173	3	BIG 7	SMALL 3	LOSSL3
…00051172	1	BIG 7	SMALL 1	LOSSL3
…00051171	3	BIG 7	SMALL 3	LOSSL2
…00051170	0	BIG 7	SMALL 0	LOSSL1
…00051169	9	BIG 7	BIG 9	WINL1
…00051168	3	SMALL 3	SMALL 3	WINL3
…00051167	1	BIG 7	SMALL 1	LOSSL2
…00051166	9	SMALL 1	BIG 9	LOSSL1
…00051165	4	SMALL 1	SMALL 4	WINL1
…00051164	6	BIG 8	BIG 6	WINL1
…00051163	4	SMALL 1	SMALL 4	WINL2
…00051162	5	SMALL 1	BIG 5	LOSSL1
…00051161	2	SMALL 1	SMALL 2	WINL1
…00051160	0	SMALL 1	SMALL 0	WINL1
…00051159	4	SMALL 1	SMALL 4	WINL1
…00051158	6	BIG 6	BIG 6	WINL3
…00051157	9	SMALL 1	BIG 9	LOSSL2
…00051156	0	BIG 7	SMALL 0	LOSSL1
…00051155	7	BIG 7	BIG 7	WINL2
…00051154	2	BIG 7	SMALL 2	LOSSL1
…00051153	8	BIG 7	BIG 8	WINL2
…00051152	3	BIG 7	SMALL 3	LOSSL1
…00051151	2	SMALL 2	SMALL 2	WINL1
…00051150	8	BIG 8	BIG 8	WINL1
…00051149	3	SMALL 2	SMALL 3	WINL3
…00051148	5	SMALL 0	BIG 5	LOSSL2
…00051147	6	SMALL 0	BIG 6	LOSSL1
…00051146	9	BIG 8	BIG 9	WINL1
…00051145	7	BIG 8	BIG 7	WINL3
…00051144	6	SMALL 0	BIG 6	LOSSL2
…00051143	5	SMALL 0	BIG 5	LOSSL1
…00051142	1	SMALL 1	SMALL 1	WINL1
…00051141	3	SMALL 1	SMALL 3	WINL3
…00051140	7	SMALL 1	BIG 7	LOSSL2
…00051139	5	SMALL 1	BIG 5	LOSSL1
…00051138	2	SMALL 2	SMALL 2	WINL2
…00051137	9	SMALL 2	BIG 9	LOSSL1
…00051136	6	BIG 5	BIG 6	WINL2
…00051135	4	BIG 5	SMALL 4	LOSSL1
…00051134	7	BIG 7	BIG 7	WINL1
…00051133	8	BIG 7	BIG 8	WINL2
…00051132	0	BIG 7	SMALL 0	LOSSL1
…00051131	0	SMALL 4	SMALL 0	WINL3
…00051130	6	SMALL 4	BIG 6	LOSSL2
…00051129	3	BIG 7	SMALL 3	LOSSL1
…00051128	3	SMALL 3	SMALL 3	WINL3
…00051127	0	BIG 7	SMALL 0	LOSSL2
…00051126	1	BIG 7	SMALL 1	LOSSL1
…00051125	2	SMALL 1	SMALL 2	WINL1
…00051124	2	SMALL 1	SMALL 2	WINL3
…00051123	9	SMALL 1	BIG 9	LOSSL3
…00051122	5	SMALL 1	BIG 5	LOSSL2
…00051121	9	SMALL 1	BIG 9	LOSSL1
…00051120	6	BIG 7	BIG 6	WINL2
…00051119	4	BIG 7	SMALL 4	LOSSL1
…00051118	5	BIG 7	BIG 5	WINL1
…00051117	9	BIG 7	BIG 9	WINL1
…00051042	7	BIG 7	BIG 7	WINL1
…00051041	2	SMALL 2	SMALL 2	WINL1
…00051040	0	SMALL 2	SMALL 0	WINL3
…00051039	4	BIG 7	SMALL 4	LOSSL2
…00051038	4	BIG 8	SMALL 4	LOSSL1
…00051037	5	BIG 8	BIG 5	WINL1
…00051036	6	BIG 6	BIG 6	WINL2
…00051035	1	BIG 6	SMALL 1	LOSSL1
…00051034	4	SMALL 2	SMALL 4	WINL2
…00051033	5	SMALL 2	BIG 5	LOSSL1
…00051032	1	SMALL 2	SMALL 1	WINL3
…00051031	3	BIG 6	SMALL 3	LOSSL2
…00051030	1	BIG 6	SMALL 1	LOSSL1
…00051029	9	BIG 6	BIG 9	WINL1
…00051028	7	BIG 7	BIG 7	WINL1
'''

lines = [l.strip() for l in raw_user.strip().split('\n') if l.strip()]
rows = []
for l in lines:
    parts = re.split(r'\t+|\s{2,}', l)
    if len(parts) >= 4:
        period = parts[0].replace('…', '').replace('.', '')
        num = int(parts[1])
        res_str = parts[3]
        size = 'BIG' if 'BIG' in res_str or num >= 5 else 'SMALL'
        rows.append({'period': period, 'number': num, 'size': size})
rows.reverse()

all_eval_seqs = all_real_sequences + [rows]

def get_runs(sizes):
    if not sizes: return []
    runs = []
    curr = sizes[0]; l = 1
    for i in range(1, len(sizes)):
        if sizes[i] == curr: l += 1
        else:
            runs.append({'size': curr, 'len': l})
            curr = sizes[i]; l = 1
    runs.append({'size': curr, 'len': l})
    return runs

def opp(s): return 'SMALL' if s == 'BIG' else 'BIG'

ACTIONS = ['SAME', 'OPP', 'LAST', 'OPP_LAST']

# All possible keys in the 3*5*4*4*3 space:
# streak (0,1,2), cLenCat (0..4), pLenCat (0..3), altCat (0..3), flipCat (0..2)
ALL_KEYS = []
for s in range(3):
    for c in range(5):
        for p in range(4):
            for a in range(4):
                for f in range(3):
                    ALL_KEYS.append(f'{s}_{c}_{p}_{a}_{f}')

def eval_table(table):
    total_wins = 0
    total_losses = 0
    global_max_loss = 0
    streak_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    
    for seq in all_eval_seqs:
        if len(seq) < 4: continue
        loss_streak = 0
        for i in range(3, len(seq)):
            hist = seq[:i]
            act = seq[i]['size']
            sizes = [x['size'] for x in hist]
            
            runs = get_runs(sizes)
            cRun = runs[-1]
            cSide = cRun['size']
            cLen = cRun['len']
            pRun = runs[-2] if len(runs) >= 2 else {'size': opp(cSide), 'len': 0}
            lastS = sizes[-1]
            
            alt = 0
            for r in reversed(runs):
                if r['len'] == 1: alt += 1
                else: break
                
            cLenCat = min(cLen, 4)
            pLenCat = min(pRun['len'], 3)
            altCat = min(alt, 3)
            streakCat = min(loss_streak, 2)
            
            recent = sizes[-6:]
            flips = 0
            for k in range(1, len(recent)):
                if recent[k] != recent[k-1]: flips += 1
            flipCat = 0 if flips <= 1 else (1 if flips in [2,3] else 2)
            
            key = f'{streakCat}_{cLenCat}_{pLenCat}_{altCat}_{flipCat}'
            actRule = table.get(key, 'SAME')
            
            if actRule == 'SAME': pred = cSide
            elif actRule == 'OPP': pred = opp(cSide)
            elif actRule == 'LAST': pred = lastS
            elif actRule == 'OPP_LAST': pred = opp(lastS)
            else: pred = cSide
            
            if pred == act:
                total_wins += 1
                loss_streak = 0
            else:
                total_losses += 1
                loss_streak += 1
                streak_counts[min(loss_streak, 5)] = streak_counts.get(min(loss_streak, 5), 0) + 1
                if loss_streak > global_max_loss:
                    global_max_loss = loss_streak
                    
    # Fitness score: maximize wins, severely penalize loss streaks >= 3
    penalty = (streak_counts.get(3, 0) * 1000) + (streak_counts.get(4, 0) * 5000) + (streak_counts.get(5, 0) * 20000) + (global_max_loss * 500)
    fitness = total_wins * 10 - total_losses * 5 - penalty
    return fitness, total_wins, total_losses, global_max_loss

# Initialize with intelligent heuristic
def make_seed_table():
    tbl = {}
    for k in ALL_KEYS:
        parts = [int(x) for x in k.split('_')]
        s, c, p, a, f = parts
        
        if s == 2: # Level 3 recovery
            if c >= 3: # Invariant dragon lock
                tbl[k] = 'SAME'
            elif c == 2: # Doublet cut
                tbl[k] = 'OPP'
            elif a >= 2: # Chop oscillate
                tbl[k] = 'OPP_LAST'
            else:
                tbl[k] = 'SAME' if f <= 1 else 'OPP'
        elif s == 1: # Level 2 recovery
            if c >= 3: # Dragon follow
                tbl[k] = 'SAME'
            elif c == 2: # Doublet cut
                tbl[k] = 'OPP'
            elif a >= 2: # Chop oscillate
                tbl[k] = 'OPP_LAST'
            else:
                tbl[k] = 'LAST'
        else: # Level 1 base
            if c >= 3:
                tbl[k] = 'SAME'
            elif c == 2:
                tbl[k] = 'OPP'
            elif a >= 2:
                tbl[k] = 'OPP_LAST'
            else:
                tbl[k] = 'SAME'
    return tbl

best_table = make_seed_table()
best_fit, best_w, best_l, best_m = eval_table(best_table)
print(f'Initial Seed Table: Wins={best_w}, Losses={best_l}, WinRate={best_w/(best_w+best_l)*100:.1f}%, MaxLoss={best_m}, Fitness={best_fit}')

# Run hill-climbing optimization
visited_keys = list(ALL_KEYS)
for iteration in range(2000):
    candidate = copy.copy(best_table)
    # Mutate 1-3 keys
    num_mut = random.randint(1, 3)
    for _ in range(num_mut):
        k = random.choice(visited_keys)
        candidate[k] = random.choice(ACTIONS)
        
    fit, w, l, m = eval_table(candidate)
    if fit > best_fit:
        best_fit = fit
        best_table = candidate
        best_w, best_l, best_m = w, l, m
        if iteration % 50 == 0 or m <= 2:
            print(f'Iter {iteration}: Wins={w}, Losses={l}, WinRate={w/(w+l)*100:.1f}%, MaxLoss={m}, Fitness={fit}')
        if m <= 2:
            print(f'>>> ZERO BUST (MAX LOSS <= 2) ACHIEVED AT ITER {iteration} <<<')
            break

print(f'\nFinal Results: Wins={best_w}, Losses={best_l}, WinRate={best_w/(best_w+best_l)*100:.1f}%, MaxLoss={best_m}')
import json
with open('solved_apex_rules.json', 'w') as f:
    json.dump(best_table, f)
print('Saved to solved_apex_rules.json')
