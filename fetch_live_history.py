import urllib.request
import json
import ssl
import time

ctx = ssl._create_unverified_context()

def fetch_page(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        res = urllib.request.urlopen(req, context=ctx, timeout=10)
        data = json.loads(res.read().decode('utf-8'))
        return data.get('data', {}).get('list', [])
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []

list_30s = fetch_page('https://draw.ar-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json')
list_1m = fetch_page('https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json')

print(f"Fetched {len(list_30s)} 30S rounds and {len(list_1m)} 1M rounds.")
with open("live_feed_cache.json", "w") as f:
    json.dump({"30S": list_30s, "1M": list_1m}, f, indent=2)
print("Saved to live_feed_cache.json")
