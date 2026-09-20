with open('generate_standalone_v26.py', 'r', encoding='utf-8') as f:
    c = f.read()

old_block = """          if (parsed.length >= 3) {
            // Sort ascending by period
            parsed.sort((a, b) => {
              try { return BigInt(a.period) > BigInt(b.period) ? 1 : -1; } catch (e) { return 0; }
            });
            LOTTERY_HISTORY = parsed;
            checkLastDrawOutcome();
            updateHud();
          }"""

new_block = """          if (parsed.length >= 3) {
            const map = new Map();
            LOTTERY_HISTORY.forEach(item => map.set(item.period, item));
            parsed.forEach(item => map.set(item.period, item));
            const merged = Array.from(map.values());
            merged.sort((a, b) => {
              try { return BigInt(a.period) > BigInt(b.period) ? 1 : -1; } catch (e) { return 0; }
            });
            LOTTERY_HISTORY = merged.slice(-100);
            checkLastDrawOutcome();
            updateHud();
          }"""

c = c.replace(old_block, new_block)

# Add lottery list interception into XHR
old_xhr = """        if (resJson && typeof resJson === 'object') {
          const b = resJson?.data?.balance ?? resJson?.data?.userBalance ?? resJson?.data?.money ?? resJson?.balance ?? resJson?.data?.amount;"""

new_xhr = """        if (resJson && typeof resJson === 'object') {
          const list = resJson?.data?.list || resJson?.list || resJson?.data?.games;
          if (Array.isArray(list) && list.length > 0 && (list[0].issueNumber || list[0].period)) {
            const parsed = list.map(item => {
              const p = String(item.issueNumber || item.period || '').trim();
              const n = parseInt(item.number);
              return { period: p, number: n, size: sizeFor(n) };
            }).filter(x => /^\\d+$/.test(x.period) && Number.isInteger(x.number));
            if (parsed.length > 0) {
              const map = new Map();
              LOTTERY_HISTORY.forEach(item => map.set(item.period, item));
              parsed.forEach(item => map.set(item.period, item));
              const merged = Array.from(map.values());
              merged.sort((a, b) => {
                try { return BigInt(a.period) > BigInt(b.period) ? 1 : -1; } catch (e) { return 0; }
              });
              LOTTERY_HISTORY = merged.slice(-100);
              checkLastDrawOutcome();
              updateHud();
            }
          }
          const b = resJson?.data?.balance ?? resJson?.data?.userBalance ?? resJson?.data?.money ?? resJson?.balance ?? resJson?.data?.amount;"""

c = c.replace(old_xhr, new_xhr)

with open('generate_standalone_v26.py', 'w', encoding='utf-8') as f:
    f.write(c)

print("Updated generate_standalone_v26.py successfully!")
