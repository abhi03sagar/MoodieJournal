// backend/utils/authMiddleware.js
const jwt = require('jsonwebtoken');
const config = require('../config');

module.exports = (req, res, next) => {
  // Grab the Authorization header
  const authHeader = req.headers.authorization || req.headers.Authorization;
  if (!authHeader?.startsWith('Bearer ')) {
    return res.status(401).json({ message: 'No token provided' });
  }

  const token = authHeader.slice(7); // remove "Bearer "

  try {
    // Verify using the same secret you sign with
    req.user = jwt.verify(token, config.JWT_SECRET);
    next();
  } catch (err) {
    console.error('JWT error:', err);
    const message =
      err.name === 'TokenExpiredError' ? 'Token expired' : 'Invalid token';
    res.status(401).json({ message });
  }
};
