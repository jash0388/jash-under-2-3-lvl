import json

with open("v9um_apex_titan_supreme_9feature_rules.json") as f:
    rules_30s = json.load(f)

with open("v9um_apex_titan_supreme_9feature_1m_rules.json") as f:
    rules_1m = json.load(f)

rules_30s_json = json.dumps(rules_30s)
rules_1m_json = json.dumps(rules_1m)

print(f"30S Rules count: {len(rules_30s)}")
print(f"1M Rules count: {len(rules_1m)}")

# Update pred.html and public/pred.html
for p in ['pred.html', 'public/pred.html', 'pred/index.html', 'public/pred/index.html']:
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace rules
    import re
    content = re.sub(r'const TITAN_RULES_30S = \{.*?\};', f'const TITAN_RULES_30S = {rules_30s_json};', content)
    content = re.sub(r'const TITAN_RULES_1M = \{.*?\};', f'const TITAN_RULES_1M = {rules_1m_json};', content)
    
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Synchronized rules in {p}")

# Update build_script.py
with open('build_script.py', 'r', encoding='utf-8') as f:
    b_code = f.read()

b_code = re.sub(r'const TITAN_RULES_30S = \{.*?\};', f'const TITAN_RULES_30S = {rules_30s_json};', b_code)
b_code = re.sub(r'const TITAN_RULES_1M = \{.*?\};', f'const TITAN_RULES_1M = {rules_1m_json};', b_code)

with open('build_script.py', 'w', encoding='utf-8') as f:
    f.write(b_code)
print("Synchronized rules in build_script.py")

