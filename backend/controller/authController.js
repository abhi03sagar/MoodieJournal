// backend/controllers/authController.js
const User = require('../models/user');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const config = require('../config');

let refreshTokens=[];

const generateAccessToken = (userId) => {
  return jwt.sign({userId}, config.JWT_SECRET, {expiresIn: '1h'});
}

const generateRefreshToken = (userId) => {
  return jwt.sign({userId}, config.JWT_REFRESH_SECRET, {expiresIn: '7d'});
}

exports.register = async (req, res) => {
  const { username, password } = req.body;

  if (!username || !password)
    return res.status(400).json({ message: "Missing credentials" });

  if (await User.findOne({ username }))
    return res.status(409).json({ message: "Username taken" });

  const hash = await bcrypt.hash(password, 10);
  const user = new User({ username, password: hash });
  await user.save();

  // Generate tokens
  const accessToken = generateAccessToken(user._id);
  const refreshToken = generateRefreshToken(user._id);
  refreshTokens.push(refreshToken);

  // Set refresh token cookie
  res.cookie('refreshToken', refreshToken, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'Strict',
    maxAge: 7 * 24 * 60 * 60 * 1000,
  });

  // Return accessToken + username
  res.status(201).json({ accessToken, username: user.username });
};


exports.login = async (req, res) => {
  const { username, password } = req.body;
  const user = await User.findOne({ username });
  if (!user) return res.status(401).json({ message: "Invalid Username" });

  const isMatch = await bcrypt.compare(password, user.password);
  if (!isMatch) return res.status(401).json({ message: "Incorrect password" });

  const accessToken = generateAccessToken(user._id);
  const refreshToken = generateRefreshToken(user._id);

  refreshTokens.push(refreshToken);

  res.cookie('refreshToken', refreshToken, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'Strict',
    maxAge: 7 * 24 * 60 * 60 * 1000, 
  });
  res.json({ accessToken, username: user.username });
};

exports.refreshToken = (req, res) => {
  const token = req.cookies.refreshToken;
  if (!token) return res.status(401).json({ message: 'No refresh token provided' });
  if (!refreshTokens.includes(token)) return res.status(403).json({ message: 'Invalid refresh token' });

  jwt.verify(token, config.JWT_REFRESH_SECRET, (err, decoded) => {
    if (err) return res.status(403).json({ message: 'Expired or invalid refresh token' });

    const accessToken = generateAccessToken(decoded.userId);
    res.json({ accessToken });
  });
};

exports.logout = (req, res) => {
  const token = req.cookies.refreshToken;
  refreshTokens = refreshTokens.filter(t => t !== token);
  res.clearCookie('refreshToken');
  res.json({ message: 'Logged out successfully' });
};
