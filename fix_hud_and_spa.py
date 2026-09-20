import json
import re
import os

with open('v9um_apex_titan_supreme_30s_rules.json', 'r') as f:
    rules_30s = json.load(f)

with open('v3um_enhanced_1m_rules.json', 'r') as f:
    rules_1m = json.load(f)

rules_30s_json = json.dumps(rules_30s)
rules_1m_json = json.dumps(rules_1m)

template_path = '/Users/jashwanthsingh/Downloads/signal_top1_follower.user.js'
with open(template_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Enhance createHud with body check and auto-recovery
hud_create_patch = """  // ════════════════════════════════════════════════════════════
  // 9. CYBER DRAGGABLE HUD (SELF-ATTACHING & SPA-PERSISTENT)
  // ════════════════════════════════════════════════════════════
  function createHud() {
    if (document.getElementById('jash-v9UM-hud')) return;
    if (!document.body) {
      setTimeout(createHud, 300);
      return;
    }

    const hud = document.createElement('div');
    hud.id = 'jash-v9UM-hud';"""

code = re.sub(r'// ═+\s*// 9\. CYBER DRAGGABLE HUD[\s\S]*?const hud = document\.createElement\(\'div\'\);\s*hud\.id = \'jash-v9UM-hud\';', lambda m: hud_create_patch, code)

# Ensure init retries and attaches HUD continuously
init_patch = """  // ════════════════════════════════════════════════════════════
  // 11. INITIALIZATION & SPA CONTINUOUS RESCUE
  // ════════════════════════════════════════════════════════════
  function ensureHudAttached() {
    try {
      if (document.body && !document.getElementById('jash-v9UM-hud')) {
        createHud();
      }
    } catch (e) {}
  }

  function init() {
    createHud();
    setInterval(ensureHudAttached, 1000);
    setInterval(botCycle, 1000);
    setInterval(readScreenWalletBalance, 1500);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
  // Failsafe auto-init
  setTimeout(init, 500);
  setTimeout(init, 1500);"""

code = re.sub(r'// ═+\s*// 11\. INITIALIZATION[\s\S]*?\n\}\)\(\);', lambda m: init_patch + '\n})();', code)

# Ensure version is 70.6
def generate_script(script_name):
    clean_name = script_name.replace('.user.js', '')
    url_name = script_name
    
    header_block = f"""// ==UserScript==
// @name         {clean_name} — Apex Titan v9UM (Auto-Updating Zero-Bust Master)
// @namespace    http://tampermonkey.net/
// @version      70.6
// @description  Universal 24/7 Overnight WinGo Auto-Betting Bot powered by Apex Titan v9UM Neural Quantum Supreme Engine with Cloud OTA Real-Time Auto-Update.
// @match        *://*.dmfirst*.com/*
// @match        *://*.dmfirst17.com/*
// @match        *://*.dmfirst9.com/*
// @match        *://*.in999*.com/*
// @match        *://*.in999vv.com/*
// @match        *://*.muskan*.com/*
// @match        *://*.muskan2.com/*
// @match        *://*.muskan22.com/*
// @match        *://*.shreewin*.com/*
// @match        *://*.shreewin.net/*
// @match        *://*.dhanuwin*.com/*
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

    res = re.sub(r'// ==UserScript==[\s\S]*?// ==/UserScript==', lambda m: header_block, code, count=1)
    return res

target_scripts = [
    'signal_top1_follower.user.js',
    'jash_perc_win.user.js',
    'JASH_VIP_APEX_TITAN_V9UM_AUTOBET.user.js',
    'JASH_BOT.user.js',
]

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
        
    print(f'Enhanced with SPA-Persistent HUD + Auto-Attach: {s}')

print('\nAll scripts updated to v70.6!')
