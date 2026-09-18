import urllib.request
import json
import ssl
from verify_v38_full import predict_apex_titan_v38

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def fetch_and_test(url, name):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, context=ctx) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    
    rows = data['data']['list']
    # rows are newest first, so reverse to chronological
    chrono = []
    for r in reversed(rows):
        chrono.append({
            'period': str(r['issueNumber']),
            'number': int(r['number']),
            'size': 'BIG' if int(r['number']) >= 5 else 'SMALL'
        })
    
    print(f"\n=== LIVE TEST: {name} (Latest {len(chrono)} rounds) ===")
    hist = []
    loss_streak = 0
    wins, losses, max_loss = 0, 0, 0
    
    for r in chrono:
        if len(hist) < 3:
            hist.append(r)
            continue
        pred, reg = predict_apex_titan_v38(hist, loss_streak)
        won = (pred == r['size'])
        if won:
            wins += 1
            lvl = 1 if loss_streak == 0 else loss_streak + 1
            status = f'✅ WIN (Lvl {lvl})'
            loss_streak = 0
        else:
            losses += 1
            loss_streak += 1
            max_loss = max(max_loss, loss_streak)
            status = f'❌ LOSS (Lvl {loss_streak})'
        print(f"{r['period']}: Pred={pred:5s} | Act={r['size']:5s}({r['number']}) | {status:15s} | {reg}")
        hist.append(r)
        
    print(f"Summary {name}: Wins={wins}, Losses={losses}, Win Rate={wins/(wins+losses)*100:.1f}%, Max Consecutive Losses={max_loss}")

fetch_and_test("https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json", "WinGo 1M")
fetch_and_test("https://draw.ar-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json", "WinGo 30S")
