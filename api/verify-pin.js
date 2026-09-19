const crypto = require('crypto');

// Server-side Secret for HMAC tokens (never exposed to client)
const SERVER_SECRET = process.env.SESSION_SECRET || 'jash_vip_apex_titan_v1um_secure_vault_salt_2026_x99';

// STRICT SINGLE PASSCODE: 2911 (Verified only on server)
const VALID_PINS = [
  process.env.JASH_VIP_PIN || '2911'
];

// Simple memory rate-limiter per IP
const attemptsMap = new Map();

function cleanOldAttempts() {
  const now = Date.now();
  for (const [ip, data] of attemptsMap.entries()) {
    if (now - data.firstAttempt > 60000) {
      attemptsMap.delete(ip);
    }
  }
}

function signToken(timestamp, nonce) {
  const data = `${timestamp}:${nonce}`;
  const hmac = crypto.createHmac('sha256', SERVER_SECRET).update(data).digest('hex');
  return Buffer.from(`${timestamp}:${nonce}:${hmac}`).toString('base64');
}

function verifyToken(token) {
  try {
    if (!token) return false;
    const decoded = Buffer.from(token, 'base64').toString('utf8');
    const [timestamp, nonce, hmac] = decoded.split(':');
    if (!timestamp || !nonce || !hmac) return false;
    
    // Check expiration (24 hours)
    const now = Date.now();
    const tokenTime = parseInt(timestamp, 10);
    if (isNaN(tokenTime) || now - tokenTime > 24 * 60 * 60 * 1000 || tokenTime > now + 60000) {
      return false;
    }
    
    // Check HMAC
    const expected = crypto.createHmac('sha256', SERVER_SECRET).update(`${timestamp}:${nonce}`).digest('hex');
    return crypto.timingSafeEqual(Buffer.from(hmac), Buffer.from(expected));
  } catch (e) {
    return false;
  }
}

module.exports = async (req, res) => {
  // CORS Headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  const clientIp = (req.headers && (req.headers['x-forwarded-for'] || req.headers['x-real-ip'])) || req.socket?.remoteAddress || 'unknown';
  cleanOldAttempts();

  // Rate Limiter Check (Max 8 attempts per minute per IP)
  const attemptData = attemptsMap.get(clientIp) || { count: 0, firstAttempt: Date.now() };
  if (attemptData.count >= 8 && Date.now() - attemptData.firstAttempt < 60000) {
    const retryAfter = Math.ceil((60000 - (Date.now() - attemptData.firstAttempt)) / 1000);
    return res.status(429).json({
      success: false,
      error: `Security Lockout: Too many attempts. Try again in ${retryAfter}s.`,
      locked: true,
      retryAfter
    });
  }

  // Handle Session Validation
  if (req.method === 'GET' || (req.body && req.body.action === 'validate_session')) {
    const authHeader = req.headers.authorization || '';
    const token = authHeader.replace(/^Bearer\s+/i, '') || (req.query && req.query.token) || (req.body && req.body.token);
    const isValid = verifyToken(token);
    return res.status(200).json({ success: isValid, authenticated: isValid });
  }

  // Handle PIN Verification (POST)
  if (req.method === 'POST') {
    let body = req.body;
    if (typeof body === 'string') {
      try { body = JSON.parse(body); } catch (e) {}
    }
    const { pin } = body || {};
    const inputPin = String(pin || '').trim();

    if (!inputPin || !/^\d{4}$/.test(inputPin)) {
      return res.status(400).json({ success: false, error: 'Invalid PIN format (Must be 4 digits).' });
    }

    // Server-side check against 2911
    const isMatch = VALID_PINS.includes(inputPin);

    if (isMatch) {
      // Clear failed attempts on success
      attemptsMap.delete(clientIp);
      
      const timestamp = Date.now();
      const nonce = crypto.randomBytes(16).toString('hex');
      const token = signToken(timestamp, nonce);

      return res.status(200).json({
        success: true,
        authenticated: true,
        token,
        expiresIn: 86400,
        message: 'Security Verification Successful. Access Granted.'
      });
    } else {
      attemptData.count++;
      attemptsMap.set(clientIp, attemptData);
      const remaining = Math.max(0, 8 - attemptData.count);

      return res.status(401).json({
        success: false,
        error: `Incorrect 4-Digit Security Code. (${remaining} attempts remaining before lockout)`,
        remaining
      });
    }
  }

  return res.status(405).json({ error: 'Method Not Allowed' });
};
