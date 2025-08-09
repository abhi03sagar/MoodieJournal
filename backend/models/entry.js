const mongoose = require('mongoose');
const EntrySchema = new mongoose.Schema({
  user: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
  text: String,
  date: Date,
  sentiment: String, // To be filled after analysis
});
module.exports = mongoose.model('Entry', EntrySchema);
