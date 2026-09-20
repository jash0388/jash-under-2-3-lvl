import re
import os

with open('pred.html', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace the entire prediction engine in pred.html with the identical engine from build_script.py
new_engine = """        // === 👑 APEX TITAN v9UM CADENCE ENGINE (100% MATCH WITH PHONE BOT) ===
        function predictApexTitan30S(sizes, lossStreak) {
          if (!sizes || sizes.length === 0) return { finalSize: 'BIG', regime: 'INITIALIZING', conf: 85 };
          const runs = getRuns(sizes);
          const cRun = runs[runs.length - 1];
          const cSide = cRun.size;
          const cLen = cRun.len;
          const pRun = runs.length >= 2 ? runs[runs.length - 2] : { size: opp(cSide), len: 0 };
          const p3Run = runs.length >= 3 ? runs[runs.length - 3] : { size: cSide, len: 0 };
          const lastS = sizes[sizes.length - 1];

          let alt = 0;
          for (let i = runs.length - 1; i >= 0; i--) {
            if (runs[i].len === 1) alt++;
            else break;
          }

          // --- LEVEL 3 INVARIANT SHIELD (STREAK >= 2) ---
          if (lossStreak >= 2) {
            if (cLen >= 3) return { finalSize: cSide, regime: `🛑 L3 DRAGON LOCK (${cSide} x${cLen})`, conf: 99 };
            if (cLen === 2) return { finalSize: opp(cSide), regime: `🛑 L3 DOUBLET CUT (${opp(cSide)})`, conf: 98 };
            if (alt >= 2) return { finalSize: opp(lastS), regime: `🛑 L3 CHOP OSCILLATE (${opp(lastS)})`, conf: 99 };
            if (pRun.len === 2 && cLen === 1) return { finalSize: opp(cSide), regime: `🛑 L3 WAVE SHIELD (${opp(cSide)})`, conf: 97 };
            return { finalSize: opp(cSide), regime: `🛑 L3 SAFE RECOVERY (${opp(cSide)})`, conf: 96 };
          }

          // --- LEVEL 2 RECOVERY (STREAK == 1) ---
          if (lossStreak === 1) {
            if (cLen >= 3) return { finalSize: cSide, regime: `🛡️ L2 DRAGON RIDE (${cSide} x${cLen})`, conf: 96 };
            if (cLen === 2) return { finalSize: opp(cSide), regime: `🛡️ L2 DOUBLET CUT (${opp(cSide)})`, conf: 96 };
            if (alt >= 3) return { finalSize: opp(lastS), regime: `🛡️ L2 DEEP CHOP OSC (${opp(lastS)})`, conf: 95 };
            if (alt >= 2) return { finalSize: cSide, regime: `🛡️ L2 CHOP BREAK (${cSide})`, conf: 94 };
            if (pRun.len >= 3 && cLen === 1) return { finalSize: opp(cSide), regime: `🛡️ L2 POST-DRAGON FLIP (${opp(cSide)})`, conf: 95 };
            return { finalSize: cSide, regime: `🛡️ L2 MOMENTUM LOCK (${cSide})`, conf: 93 };
          }

          // --- LEVEL 1 BASE (STREAK == 0) ---
          if (cLen === 3 && pRun.len === 1 && p3Run.len === 3) {
            return { finalSize: opp(cSide), regime: `🎯 L1 3-1-3 HARMONIC CUT (${opp(cSide)})`, conf: 94 };
          }
          if (cLen >= 3) return { finalSize: cSide, regime: `🌊 L1 DRAGON RIDE (${cSide} x${cLen})`, conf: 94 };
          if (cLen === 2) return { finalSize: opp(cSide), regime: `🌊 L1 DOUBLET CUT (${opp(cSide)})`, conf: 95 };
          if (alt >= 3) return { finalSize: opp(lastS), regime: `⚡ L1 DEEP CHOP OSC (${opp(lastS)})`, conf: 93 };
          if (alt >= 2) return { finalSize: lastS, regime: `⚡ L1 CHOP STABILIZE (${lastS})`, conf: 92 };
          if (cLen === 1) return { finalSize: cSide, regime: `🌊 L1 PAIR BUILD (${cSide})`, conf: 91 };
          return { finalSize: cSide, regime: `🌊 L1 MOMENTUM (${cSide})`, conf: 90 };
        }

        function predictApexTitan1M(sizes, lossStreak) {
          return predictApexTitan30S(sizes, lossStreak);
        }

        // === APEX TITAN UNIVERSAL ULTRA MASTER (v9UM) ===
        function predictApexTitanV9UM(evidence, lossStreak = 0, mode = currentMode) {
          if (!evidence || evidence.length < 3) {
            return { size: "BIG", number: 7, confidence: 90, regime: "TITAN INITIALIZING" };
          }

          const nums = evidence.slice(-50);
          const sizes = nums.map(n => n >= 5 ? "BIG" : "SMALL");
          
          const res = (mode === "1M") ? predictApexTitan1M(sizes, lossStreak) : predictApexTitan30S(sizes, lossStreak);

          // Harmonic Lucky Ball Selector
          const allowed = res.finalSize === "BIG" ? [5, 6, 7, 8, 9] : [0, 1, 2, 3, 4];
          const freq = counts(nums.slice(-20));
          const bestNum = allowed.reduce((best, n) => {
            const target = res.finalSize === "BIG" ? 7 : 2;
            const diff = Math.abs(n - target);
            const bestDiff = Math.abs(best - target);
            return freq[n] < freq[best] || (freq[n] === freq[best] && diff < bestDiff) ? n : best;
          }, allowed[0]);

          return { size: res.finalSize, number: bestNum, confidence: res.conf, regime: res.regime };
        }"""

# Replace old dictionary and functions
pattern = r"// === 30S & 1M CADENCE ZERO-LOSS STATE TABLES[\s\S]*?return \{ size: res\.finalSize, number: bestNum, confidence: res\.conf, regime: res\.regime \};\s*\}"
code = re.sub(pattern, new_engine, code)

# In render(), support bot sync telemetry if bot is online
old_render_start = """          // Current Prediction:
          let prediction = pendingPrediction;
          if (!prediction && state.results.length >= 3) {
            const nums = state.results.map(r => r.number).reverse();
            const lossStreak = getLossStreak();
            prediction = predictApexTitanV9UM(nums, lossStreak, currentMode);
          }"""

new_render_start = """          // Current Prediction (Synced with Phone Bot if Online):
          let prediction = pendingPrediction;
          if (state.botPrediction && state.botOnline) {
            prediction = state.botPrediction;
          } else if (!prediction && state.results.length >= 3) {
            const nums = state.results.map(r => r.number).reverse();
            const lossStreak = getLossStreak();
            prediction = predictApexTitanV9UM(nums, lossStreak, currentMode);
          }"""

code = code.replace(old_render_start, new_render_start)

# Add bot telemetry poller before checkSavedSession()
bot_poller = """        // === REAL-TIME SYNC WITH PHONE BOT ===
        async function fetchBotSyncTelemetry() {
          if (!isAuthenticated) return;
          try {
            const res = await fetch("/api/sync?_t=" + Date.now());
            const data = await res.json();
            if (data && data.success && data.state) {
              const s = data.state;
              state.botOnline = Boolean(data.isOnline);
              if (data.isOnline && s.nextPred && s.nextPred.length > 1) {
                const isBig = s.nextPred.includes("BIG");
                const isSmall = s.nextPred.includes("SMALL");
                let num = isBig ? 7 : 2;
                const m = s.nextPred.match(/\[([0-9])\]/) || s.nextPred.match(/\\b([0-9])\\b/);
                if (m) num = parseInt(m[1]);
                const size = isBig ? "BIG" : (isSmall ? "SMALL" : "BIG");
                
                state.botPrediction = {
                  size,
                  number: num,
                  confidence: s.conf || (s.martingaleStep >= 2 ? 99 : (s.martingaleStep === 1 ? 96 : 92)),
                  regime: s.regime || s.status || `⚡ REGIME: 🌊 L1 APEX [${size}]`
                };
                if (s.timer != null && s.timer >= 0) {
                  state.seconds = s.timer;
                }
                if (s.nextPeriod && s.nextPeriod !== '--') {
                  const pStr = String(s.nextPeriod);
                  if (pStr.length >= 8) state.targetPeriod = pStr;
                }
                render();
              }
            }
          } catch (e) {}
        }
        setInterval(fetchBotSyncTelemetry, 1000);

        // Initial Session Check
        checkSavedSession();"""

code = code.replace("""        // Initial Session Check
        checkSavedSession();""", bot_poller)

# Write to all destinations
for path in ['pred.html', 'public/pred.html', 'public/pred/index.html', 'pred/index.html']:
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(code)
    print(f"Updated: {path}")

print("All /pred pages successfully synchronized with Phone Bot!")
