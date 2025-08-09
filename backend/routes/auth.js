// backend/routes/auth.js

const express = require('express');
const router = express.Router();
const authController = require('../controller/authController');

// User registration
router.post('/register', authController.register);

// User login (issues access & refresh tokens)
router.post('/login', authController.login);

// Refresh access token
router.post('/refresh-token', authController.refreshToken);

// Logout (revokes refresh token)
router.post('/logout', authController.logout);

module.exports = router;
