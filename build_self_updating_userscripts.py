import json
import re
import os
import shutil

with open('v9um_apex_titan_supreme_30s_rules.json', 'r') as f:
    rules_30s = json.load(f)

with open('v3um_enhanced_1m_rules.json', 'r') as f:
    rules_1m = json.load(f)

rules_30s_json = json.dumps(rules_30s)
rules_1m_json = json.dumps(rules_1m)

template_path = '/Users/jashwanthsingh/Downloads/jash_perc_win.user.js'
with open(template_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Build OTA sync engine block
ota_block = """  // ════════════════════════════════════════════════════════════
  // 3. REAL-TIME LIVE CLOUD OTA AUTO-SYNC & SELF-UPDATE ENGINE
  // ════════════════════════════════════════════════════════════
  let LIVE_RULES_VERSION = '70.4';
  let LAST_OTA_SYNC = Date.now();
  let OTA_SYNC_ACTIVE = true;

  function fetchLiveCloudRules() {
    try {
      if (typeof GM_xmlhttpRequest !== 'function') return;
      GM_xmlhttpRequest({
        method: 'GET',
        url: `https://jashvip.vercel.app/api/rules?t=${Date.now()}`,
        timeout: 6000,
        headers: { 'Cache-Control': 'no-cache' },
        onload: function (res) {
          try {
            if (res.status === 200) {
              const data = JSON.parse(res.responseText);
              if (data && data.success && data.rules_30s) {
                Object.assign(TITAN_RULES_30S, data.rules_30s);
                if (data.rules_1m) Object.assign(TITAN_RULES_1M, data.rules_1m);
                LIVE_RULES_VERSION = data.version || LIVE_RULES_VERSION;
                LAST_OTA_SYNC = Date.now();
                try {
                  GM_setValue('CACHED_TITAN_RULES_30S', JSON.stringify(TITAN_RULES_30S));
                  GM_setValue('CACHED_TITAN_RULES_1M', JSON.stringify(TITAN_RULES_1M));
                  GM_setValue('CACHED_RULES_VERSION', LIVE_RULES_VERSION);
                } catch (e) {}
                console.log(`%c✨ [JASH VIP] Cloud OTA Auto-Sync Successful! Active rules version: ${LIVE_RULES_VERSION} (${Object.keys(TITAN_RULES_30S).length} rules)`, 'background:#00f5a0;color:#000;font-weight:900;padding:4px 8px;border-radius:4px;');
                const badge = document.getElementById('jash-ota-badge');
                if (badge) {
                  badge.textContent = `⚡ OTA: v${LIVE_RULES_VERSION} LIVE`;
                  badge.style.color = '#00f5a0';
                }
              }
            }
          } catch (e) {}
        }
      });
    } catch (e) {}
  }

  // Restore cached rules on cold start
  try {
    const cached30s = GM_getValue('CACHED_TITAN_RULES_30S');
    const cached1m = GM_getValue('CACHED_TITAN_RULES_1M');
    if (cached30s) Object.assign(TITAN_RULES_30S, JSON.parse(cached30s));
    if (cached1m) Object.assign(TITAN_RULES_1M, JSON.parse(cached1m));
    const cachedVer = GM_getValue('CACHED_RULES_VERSION');
    if (cachedVer) LIVE_RULES_VERSION = cachedVer;
  } catch (e) {}

  // Periodic OTA cloud background sync every 15 seconds
  setInterval(fetchLiveCloudRules, 15000);
  setTimeout(fetchLiveCloudRules, 1000);
"""

# Check if ota_block is already present, if not add it right before // 4. Apex Titan
if 'REAL-TIME LIVE CLOUD OTA AUTO-SYNC' not in code:
    code = code.replace('  // ════════════════════════════════════════════════════════════\n  // 4. Apex Titan', ota_block + '\n  // ════════════════════════════════════════════════════════════\n  // 4. Apex Titan')

# Ensure TITAN_RULES_30S is let or non-frozen object
code = code.replace('const TITAN_RULES_30S = {', 'let TITAN_RULES_30S = {')
code = code.replace('const TITAN_RULES_1M = {', 'let TITAN_RULES_1M = {')

# Add OTA badge to HUD if not present
if 'id="jash-ota-badge"' not in code:
    hud_target = '<div style="font-size:10px;color:#94a3b8;font-weight:700" id="jash-mode-lbl">'
    hud_replacement = '<div style="font-size:10px;color:#94a3b8;font-weight:700" id="jash-mode-lbl">\n          <span id="jash-ota-badge" style="display:inline-block;padding:2px 6px;border-radius:4px;background:rgba(0,245,160,0.15);border:1px solid #00f5a0;color:#00f5a0;font-size:8.5px;font-weight:900;margin-left:6px">⚡ OTA AUTO-SYNC: ON</span>'
    code = code.replace(hud_target, hud_replacement)

# Make sure @connect includes jashvip.vercel.app and raw.githubusercontent.com
connect_block = """// @connect      draw.ar-lottery01.com
// @connect      jashvip.vercel.app
// @connect      raw.githubusercontent.com"""
code = code.replace('// @connect      draw.ar-lottery01.com', connect_block)

# Function to generate script for specific script filename
def generate_script(script_name):
    clean_name = script_name.replace('.user.js', '')
    url_name = script_name
    
    header_block = f"""// ==UserScript==
// @name         {clean_name} — Apex Titan v9UM (Auto-Updating Zero-Bust Master)
// @namespace    http://tampermonkey.net/
// @version      70.4
// @description  Universal 24/7 Overnight WinGo Auto-Betting Bot powered by Apex Titan v9UM Neural Quantum Supreme Engine with Cloud OTA Real-Time Auto-Update.
// @match        *://*.dmfirst17.com/*
// @match        *://*.dmfirst*.com/*
// @match        *://*.in999vv.com/*
// @match        *://*.in999*.com/*
// @match        *://*.muskan2.com/*
// @match        *://*.muskan22.com/*
// @match        *://*.muskan*.com/*
// @match        *://*.shreewin.net/*
// @match        *://*.shreewin1.com/*
// @match        *://*.dhanuwin88.com/*
// @match        *://*.daman*.com/*
// @match        *://*.tiranga*.com/*
// @match        *://*.bigdaddy*.com/*
// @match        *://*/*
// @grant        GM_xmlhttpRequest
// @grant        GM_getValue
// @grant        GM_setValue
// @connect      draw.ar-lottery01.com
// @connect      jashvip.vercel.app
// @connect      raw.githubusercontent.com
// @updateURL    https://jashvip.vercel.app/{url_name}
// @downloadURL  https://jashvip.vercel.app/{url_name}
// @run-at       document-start
// ==/UserScript=="""

    # Replace header in code
    res = re.sub(r'// ==UserScript==[\s\S]*?// ==/UserScript==', header_block, code, count=1)
    return res

target_scripts = [
    'signal_top1_follower.user.js',
    'jash_perc_win.user.js',
    'JASH_VIP_APEX_TITAN_V9UM_AUTOBET.user.js',
    'JASH_BOT.user.js',
]

# Ensure public dir exists
os.makedirs('public', exist_ok=True)

for s in target_scripts:
    content = generate_script(s)
    local_path = os.path.join('/Users/jashwanthsingh/Downloads', s)
    public_path = os.path.join('/Users/jashwanthsingh/Downloads/jashvip/public', s)
    root_path = os.path.join('/Users/jashwanthsingh/Downloads/jashvip', s)
    
    with open(local_path, 'w', encoding='utf-8') as f:
        f.write(content)
    with open(public_path, 'w', encoding='utf-8') as f:
        f.write(content)
    with open(root_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f'Generated self-updating userscript: {s} (Local + Public + Root)')

print('\nAll self-updating userscripts built successfully!')
