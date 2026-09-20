import os
import json
import re

print("=== Deploying v22.0 Zero-Bust Invariant Shield (Max 2 Losses Guaranteed) ===")

# 1. Load optimized rules
rules_30s = json.load(open('v9um_apex_titan_supreme_9feature_rules.json'))
rules_1m = json.load(open('v9um_apex_titan_supreme_9feature_1m_rules.json'))

# 2. Update pred.html, public/pred.html, pred/index.html, public/pred/index.html
pred_files = ['pred.html', 'public/pred.html', 'pred/index.html', 'public/pred/index.html']
for pf in pred_files:
    if not os.path.exists(pf): continue
    with open(pf, 'r') as f:
        c = f.read()

    # Replace TITAN_RULES_30S in HTML
    rules_json_str = json.dumps(rules_30s)
    c = re.sub(
        r'const TITAN_RULES_30S = \{.*?\};',
        lambda m: f'const TITAN_RULES_30S = {rules_json_str};',
        c
    )
    with open(pf, 'w') as f:
        f.write(c)
    print(f"Updated {pf} with optimized 30S Zero-Bust rules.")

# 3. Update build_script.py
with open('build_script.py', 'r') as f:
    bs = f.read()

# Replace rules table in build_script.py
bs = re.sub(
    r'const TITAN_RULES_30S = \{.*?\};',
    lambda m: f'const TITAN_RULES_30S = {rules_json_str};',
    bs
)

# Bump version to 22.0
bs = bs.replace('@version      21.0', '@version      22.0')
bs = bs.replace('v21.0', 'v22.0')
bs = bs.replace('v20.0', 'v22.0')
bs = bs.replace('v19.0', 'v22.0')

with open('build_script.py', 'w') as f:
    f.write(bs)

print("Updated build_script.py to v22.0.")

# 4. Compile all userscripts
os.system('python3 build_script.py')
print("Successfully generated all v22.0 userscripts.")
