// backend/routes/entries.js
const express = require('express');
const auth = require('../utils/authMiddleware');
const entryController = require('../controller/entryController');
const router = express.Router();

// Create a new entry
router.post('/', auth, entryController.createEntry);

// Get all entries for the authenticated user
router.get('/', auth, entryController.getEntries);

// Edit an entry by ID
router.put('/:id', auth, entryController.editEntry);

// Delete an entry by ID
router.delete('/:id', auth, entryController.deleteEntry);

// Download a single entry as PDF
router.get('/:id/download', auth, entryController.downloadPDF);

module.exports = router;

