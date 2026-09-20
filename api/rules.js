const fs = require('fs');
const path = require('path');

module.exports = (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  try {
    const rules30sPath = path.join(process.cwd(), 'v9um_apex_titan_supreme_30s_rules.json');
    const rules1mPath = path.join(process.cwd(), 'v3um_enhanced_1m_rules.json');

    let rules30s = {};
    let rules1m = {};

    if (fs.existsSync(rules30sPath)) {
      rules30s = JSON.parse(fs.readFileSync(rules30sPath, 'utf8'));
    }
    if (fs.existsSync(rules1mPath)) {
      rules1m = JSON.parse(fs.readFileSync(rules1mPath, 'utf8'));
    }

    return res.status(200).json({
      success: true,
      engine: 'Apex Titan v9UM Ultimate Master',
      version: '70.4',
      rulesCount30S: Object.keys(rules30s).length,
      rulesCount1M: Object.keys(rules1m).length,
      timestamp: Date.now(),
      rules_30s: rules30s,
      rules_1m: rules1m
    });
  } catch (error) {
    return res.status(500).json({ success: false, error: error.message });
  }
};
