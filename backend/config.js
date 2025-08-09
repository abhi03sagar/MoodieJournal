// backend/config.js
require('dotenv').config();

const {
  MONGO_URI,
  JWT_SECRET,
  JWT_REFRESH_SECRET,
  PYTHON_SENTIMENT_URL,
  PYTHON_PDF_URL,
  FRONTEND_URL,
  PORT
} = process.env;

if (process.env.NODE_ENV === 'production') {
  if (!MONGO_URI) {
    throw new Error('MONGO_URI is required in production');
  }
  if (!JWT_SECRET || JWT_SECRET === 'the_key_that_is_the_key') {
    throw new Error('A secure JWT_SECRET is required in production');
  }
  if (!JWT_REFRESH_SECRET || JWT_REFRESH_SECRET === 'the_refresh_key_that_is_the_key') {
    throw new Error('A secure JWT_REFRESH_SECRET is required in production');
  }
}

module.exports = {
  MONGO_URI: MONGO_URI || 'mongodb://localhost:27017/virtual-diary',
  JWT_SECRET: JWT_SECRET || 'the_key_that_is_the_key',
  JWT_REFRESH_SECRET: JWT_REFRESH_SECRET || 'the_refresh_key_that_is_the_key',
  PYTHON_SENTIMENT_URL: PYTHON_SENTIMENT_URL || 'http://localhost:5001/analyze',
  PYTHON_PDF_URL: PYTHON_PDF_URL || 'http://localhost:5002/pdf',
  FRONTEND_URL: FRONTEND_URL || 'http://localhost:3000',
  PORT: parseInt(PORT, 10) || 5000,
  COOKIE_OPTIONS: {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'Strict',
    maxAge: 7 * 24 * 60 * 60 * 1000, // 7 days
  },
};
