# MoodieJournal

A full-stack web application for journaling with sentiment analysis and PDF export. Built with React (frontend), Node.js/Express (backend), and Python/Flask microservices for sentiment and PDF generation.

---

## Features
- User authentication (register/login/logout)
- Create, edit, and delete diary entries
- Sentiment analysis of entries (Python microservice)
- Download entries as PDF (Python microservice)
- Secure JWT-based authentication with refresh tokens
- Responsive React frontend

---

## 🚧 Work in Progress (WIP)
- Add email field to registration for improved authentication and password recovery.
- Implement "forgot password" functionality.
- Refactor sentiment analysis: separate Python microservice (Flask API) from Node.js backend.
- Upgrade sentiment analysis to use transformers (distilroberta-base) instead of TextBlob for better accuracy.

---

## Project Structure
```
virtual-diary/
├── backend/              # Node.js/Express API
│   ├── app.js
│   ├── config.js
│   ├── controller/
│   ├── models/
│   ├── routes/
│   ├── utils/
│   ├── .env.example
│   └── package.json
├── frontend/             # React frontend
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   └── package.json
├── sentiment_service/    # Python microservices
│   ├── app.py            # Sentiment analysis
│   ├── pdf_service.py    # PDF generation
│   └── requirements.txt
└── README.md
```

---

## Prerequisites
- Node.js (v16+ recommended)
- Python 3.8+
- MongoDB Atlas (cloud database)

---

## Environment Variables

### Backend (`backend/.env`)
Copy `backend/.env.example` to `backend/.env` and fill in your values:
```
MONGO_URI=your_mongodb_atlas_connection_string
JWT_SECRET=your_strong_jwt_secret
JWT_REFRESH_SECRET=your_strong_jwt_refresh_secret
PYTHON_SENTIMENT_URL=http://localhost:5001/analyze
PYTHON_PDF_URL=http://localhost:5002/pdf
FRONTEND_URL=http://localhost:3000
PORT=5000
```

### Frontend (`frontend/.env`)
```
REACT_APP_API_URL=http://localhost:5000
```

---

## Setup & Run Locally

### 1. Backend
```bash
cd backend
npm install
npm start
```

### 2. Frontend
```bash
cd frontend
npm install
npm start
```

### 3. Sentiment & PDF Services
```bash
cd sentiment_service
pip install -r requirements.txt
# Start sentiment analysis service
python app.py
# Start PDF service (in another terminal)
python pdf_service.py
```

---

## Deployment (Render Example)
- Push your code to GitHub.
- Create three services on Render:
  - **Backend:** Web Service (Node), root directory: `backend`, start: `npm start`
  - **Frontend:** Static Site, root directory: `frontend`, build: `npm run build`, publish: `build`
  - **Sentiment Service:** Web Service (Python), root: `sentiment_service`, start: `python app.py`
- Set environment variables in Render dashboard for each service.
- Use MongoDB Atlas for your database (update `MONGO_URI`).

---

## API Endpoints (Backend)
- `POST   /api/auth/register`   Register new user
- `POST   /api/auth/login`      Login
- `POST   /api/auth/refresh-token` Refresh JWT
- `POST   /api/auth/logout`     Logout
- `GET    /api/entries`         Get all entries
- `POST   /api/entries`         Create entry
- `PUT    /api/entries/:id`     Edit entry
- `DELETE /api/entries/:id`     Delete entry
- `GET    /api/entries/:id/download` Download entry as PDF

---

## Notes
- The backend and microservices must be running for full functionality.
- For production, set secure values for all secrets and use cloud URLs for microservices.
- The frontend expects the backend API URL in `REACT_APP_API_URL`.

---

## License
MIT
