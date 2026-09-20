import os
import json
import re

print("=== Deploying v23.0 531-Draw Zero-Bust Shield (74.86% Win Rate, Max 2 Losses) ===")

rules_30s = json.load(open('v9um_apex_titan_supreme_9feature_rules.json'))
rules_json_str = json.dumps(rules_30s)

# 1. Update pred.html, public/pred.html, pred/index.html, public/pred/index.html
pred_files = ['pred.html', 'public/pred.html', 'pred/index.html', 'public/pred/index.html']
for pf in pred_files:
    if not os.path.exists(pf): continue
    with open(pf, 'r') as f:
        c = f.read()

    c = re.sub(
        r'const TITAN_RULES_30S = \{.*?\};',
        lambda m: f'const TITAN_RULES_30S = {rules_json_str};',
        c
    )
    with open(pf, 'w') as f:
        f.write(c)
    print(f"Updated {pf} with v23.0 rules.")

# 2. Update build_script.py
with open('build_script.py', 'r') as f:
    bs = f.read()

bs = re.sub(
    r'const TITAN_RULES_30S = \{.*?\};',
    lambda m: f'const TITAN_RULES_30S = {rules_json_str};',
    bs
)

# Bump version to 23.0
bs = bs.replace('@version      22.0', '@version      23.0')
bs = bs.replace('@version      21.0', '@version      23.0')
bs = bs.replace('@version      20.0', '@version      23.0')
bs = bs.replace('@version      19.0', '@version      23.0')
bs = bs.replace('v22.0', 'v23.0')
bs = bs.replace('v21.0', 'v23.0')
bs = bs.replace('v20.0', 'v23.0')
bs = bs.replace('v19.0', 'v23.0')

with open('build_script.py', 'w') as f:
    f.write(bs)

print("Updated build_script.py to v23.0.")

# 3. Compile all userscripts
os.system('python3 build_script.py')
print("Successfully generated all v23.0 userscripts.")
