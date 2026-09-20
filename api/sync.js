const fs = require('fs');
const path = require('path');

const STATE_FILE = path.join('/tmp', 'jash_bot_state.json');

function loadState() {
  try {
    if (fs.existsSync(STATE_FILE)) {
      return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
    }
  } catch (e) {}
  return {
    lastSeen: 0,
    liveWalletBal: 400.0,
    startBankroll: 400.0,
    sessionProfit: 0.0,
    wins: 0,
    losses: 0,
    currentBet: 2,
    baseBet: 2,
    takeProfitTarget: 50000.0,
    martingaleStep: 0,
    maxSteps: 3,
    running: false,
    gameMode: '30S',
    timer: 30,
    nextPeriod: '--',
    nextPred: '--',
    status: 'STOPPED',
    history: [],
    pendingCommands: []
  };
}

function saveState(st) {
  try {
    fs.writeFileSync(STATE_FILE, JSON.stringify(st), 'utf8');
  } catch (e) {}
}

module.exports = (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  const state = loadState();

  if (req.method === 'POST') {
    const body = req.body || {};

    // 1. Telemetry from Phone / Userscript
    if (body.isTelemetry || body.fromBot) {
      state.lastSeen = Date.now();
      if (body.liveWalletBal != null) state.liveWalletBal = parseFloat(body.liveWalletBal);
      if (body.currentBalance != null) state.liveWalletBal = parseFloat(body.currentBalance);
      if (body.startBankroll != null) state.startBankroll = parseFloat(body.startBankroll);
      if (body.sessionProfit != null) state.sessionProfit = parseFloat(body.sessionProfit);
      if (body.wins != null) state.wins = parseInt(body.wins);
      if (body.losses != null) state.losses = parseInt(body.losses);
      if (body.currentStake != null) state.currentBet = parseInt(body.currentStake);
      if (body.currentBet != null) state.currentBet = parseInt(body.currentBet);
      if (body.baseBet != null) state.baseBet = parseInt(body.baseBet);
      if (body.takeProfitTarget != null) state.takeProfitTarget = parseFloat(body.takeProfitTarget);
      if (body.martingaleStep != null) state.martingaleStep = parseInt(body.martingaleStep);
      if (body.maxSteps != null) state.maxSteps = parseInt(body.maxSteps);
      if (body.running !== undefined) state.running = Boolean(body.running);
      if (body.gameMode) state.gameMode = body.gameMode;
      if (body.gameType) state.gameMode = body.gameType.includes('30S') ? '30S' : '1M';
      if (body.timer != null) state.timer = parseInt(body.timer);
      if (body.nextPeriod) state.nextPeriod = String(body.nextPeriod);
      if (body.nextPred) state.nextPred = String(body.nextPred);
      if (body.status) state.status = String(body.status);
      if (Array.isArray(body.history)) state.history = body.history.slice(0, 50);

      // Pop any pending command to send back to bot
      let command = null;
      if (state.pendingCommands && state.pendingCommands.length > 0) {
        command = state.pendingCommands.shift();
      }

      saveState(state);
      return res.status(200).json({ success: true, command, state });
    }

    // 2. Command or Settings update from Web Dashboard
    if (body.action || body.type) {
      const cmdType = body.action || body.type;
      const cmdPayload = body.payload || body;

      if (!state.pendingCommands) state.pendingCommands = [];
      state.pendingCommands.push({ type: cmdType, payload: cmdPayload, timestamp: Date.now() });

      // Immediate optimistic local update
      if (cmdType === 'TOGGLE_RUNNING' && cmdPayload.running !== undefined) {
        state.running = Boolean(cmdPayload.running);
      }
      if (cmdType === 'SET_GAME_MODE' && cmdPayload.mode) {
        state.gameMode = cmdPayload.mode;
      }
      if (cmdType === 'SET_BASE_BET' && cmdPayload.baseBet != null) {
        state.baseBet = parseInt(cmdPayload.baseBet);
      }
      if (cmdType === 'SET_TAKE_PROFIT' && cmdPayload.takeProfitTarget != null) {
        state.takeProfitTarget = parseFloat(cmdPayload.takeProfitTarget);
      }
      if (cmdType === 'RESET_SESSION') {
        state.wins = 0;
        state.losses = 0;
        state.sessionProfit = 0;
        state.martingaleStep = 0;
        state.currentBet = state.baseBet;
      }

      saveState(state);
      return res.status(200).json({ success: true, message: `Command ${cmdType} queued`, state });
    }

    // Generic update
    Object.assign(state, body);
    saveState(state);
    return res.status(200).json({ success: true, state });
  }

  // GET Request: return live bot state to Web Dashboard
  const isOnline = (Date.now() - state.lastSeen) < 7000;
  return res.status(200).json({
    success: true,
    isOnline,
    lastSeenSecondsAgo: Math.round((Date.now() - state.lastSeen) / 1000),
    state
  });
};
