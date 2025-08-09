// backend/app.js
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const cookieParser = require('cookie-parser');
const config = require('./config');

// Routes
const authRoutes = require('./routes/auth');
const entriesRoutes = require('./routes/entries');

const app = express();

// CORS: allow your frontend origin and send cookies
app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:3000',
  credentials: true
}));

app.use(express.json());
// enable parsing of cookies from incoming requests
app.use(cookieParser());

// API Routes
app.use('/api/auth', authRoutes);
app.use('/api/entries', entriesRoutes);

// DB Connection & Server Start
mongoose.connect(config.MONGO_URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true
  })
  .then(() => app.listen(config.PORT, () =>
      console.log(`Server running at http://localhost:${config.PORT}`)
    )
  )
  .catch(err => {
    console.error('DB connection error:', err.message);
    process.exit(1);
  });
