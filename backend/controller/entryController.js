// backend/controller/entryController.js
const Entry = require('../models/entry');
const axios = require('axios');
const config = require('../config');

exports.createEntry = async (req, res) => {
  const { text } = req.body;
  const sentimentRes = await axios.post(config.PYTHON_SENTIMENT_URL, { text });
  const sentiment = sentimentRes.data.sentiment;
  const entry = new Entry({ user: req.user.userId, text, date: new Date(), sentiment });
  await entry.save();
  res.status(201).json(entry);
};

exports.getEntries = async (req, res) => {
  const entries = await Entry.find({ user: req.user.userId }).sort({ date: -1 });
  res.json(entries);
};

exports.editEntry = async (req, res) => {
  const { text } = req.body;
  const sentimentRes = await axios.post(config.PYTHON_SENTIMENT_URL, { text });
  const sentiment = sentimentRes.data.sentiment;
  const entry = await Entry.findOneAndUpdate(
    { _id: req.params.id, user: req.user.userId },
    { text, sentiment },
    { new: true }
  );
  res.json(entry);
};

exports.deleteEntry = async (req, res) => {
  await Entry.findOneAndDelete({ _id: req.params.id, user: req.user.userId });
  res.json({ message: "Entry deleted" });
};

exports.downloadPDF = async (req, res) => {
  const entry = await Entry.findOne({ _id: req.params.id, user: req.user.userId });
  if (!entry) return res.status(404).json({ message: "Entry not found" });

  const pdfRes = await axios.post(
    config.PYTHON_PDF_URL,
    { text: entry.text },
    { responseType: 'stream' }
  );
  res.setHeader('Content-Type', 'application/pdf');
  pdfRes.data.pipe(res);
};
