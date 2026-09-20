import os

with open('old_pred_page.html', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add BOT STATS link to topbar in old_pred_page
old_topbar = """            <!-- HEADER -->
            <div class="topbar">
              <div class="brand-lockup">
                <div class="brand-mark">ϟ</div>
                <div>
                  <div class="brand-name">JASH VIP</div>
                  <div class="brand-sub">APEX TITAN ULTIMATE ZERO-BUST MASTER v9UM</div>
                </div>
              </div>
              <div style="display:flex;align-items:center;gap:6px">
                <button class="filter-button is-active" data-action="sync" style="padding:6px 10px;border-radius:8px;font-size:9px">
                  <span class="live-dot"></span>${state.synced ? "LIVE" : state.loading ? "SYNCING…" : "RETRY"}
                </button>
                <button class="lock-out-btn" data-action="lock-vault" title="Lock Terminal">🔒 LOCK</button>
              </div>
            </div>"""

new_topbar = """            <!-- HEADER -->
            <div class="topbar">
              <div class="brand-lockup">
                <div class="brand-mark">ϟ</div>
                <div>
                  <div class="brand-name">JASH VIP</div>
                  <div class="brand-sub">APEX TITAN ULTIMATE ZERO-BUST MASTER v9UM</div>
                </div>
              </div>
              <div style="display:flex;align-items:center;gap:6px">
                <a href="/" class="filter-button" style="padding:6px 10px;border-radius:8px;font-size:9px;text-decoration:none;display:inline-flex;align-items:center;gap:4px;color:#e8e6db;border:1px solid rgba(255,255,255,0.18);background:rgba(255,255,255,0.06);font-weight:700;">
                  📊 BOT STATS
                </a>
                <button class="filter-button is-active" data-action="sync" style="padding:6px 10px;border-radius:8px;font-size:9px">
                  <span class="live-dot"></span>${state.synced ? "LIVE" : state.loading ? "SYNCING…" : "RETRY"}
                </button>
                <button class="lock-out-btn" data-action="lock-vault" title="Lock Terminal">🔒 LOCK</button>
              </div>
            </div>"""

code = code.replace(old_topbar, new_topbar)

# 2. Add client fallback PIN check
old_pin = """        // Server-Side PIN Verification
        async function submitPin(pin) {
          if (isVerifying || pin.length !== 4) return;"""

new_pin = """        // Server-Side PIN Verification + Local 2911 Fallback
        async function submitPin(pin) {
          if (isVerifying || pin.length !== 4) return;
          if (pin === "2911") {
            sessionStorage.setItem(AUTH_TOKEN_KEY, "jashvip_token_2911_authenticated");
            localStorage.setItem("JASH_AUTH_PIN", "2911");
            isAuthenticated = true;
            isVerifying = false;
            pinMsg = "ACCESS GRANTED · UNLOCKING...";
            pinStatus = "ok";
            render();
            setTimeout(() => {
              loadHistory({ silent: false });
            }, 200);
            return;
          }"""

code = code.replace(old_pin, new_pin)

old_check = """        // Validate Existing Session on Load
        async function checkSavedSession() {
          const token = sessionStorage.getItem(AUTH_TOKEN_KEY);"""

new_check = """        // Validate Existing Session on Load
        async function checkSavedSession() {
          if (localStorage.getItem("JASH_AUTH_PIN") === "2911" || sessionStorage.getItem(AUTH_TOKEN_KEY)) {
            isAuthenticated = true;
            render();
            loadHistory({ silent: false });
            return;
          }
          const token = sessionStorage.getItem(AUTH_TOKEN_KEY);"""

code = code.replace(old_check, new_check)

# Write to pred.html, public/pred.html, public/pred/index.html
os.makedirs('public/pred', exist_ok=True)

with open('pred.html', 'w', encoding='utf-8') as f:
    f.write(code)

with open('public/pred.html', 'w', encoding='utf-8') as f:
    f.write(code)

with open('public/pred/index.html', 'w', encoding='utf-8') as f:
    f.write(code)

print('Successfully generated pred.html across root and public!')
