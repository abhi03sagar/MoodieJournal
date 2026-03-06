# 📔 Moodie Journal (Modular Monolith)

> **"Your Thoughts, Analyzed & Preserved."**

Moodie Journal is a next-generation journaling platform engineered as a **Modular Monolith**. It transcends traditional journaling by integrating **AI-powered Sentiment Analysis** to provide users with immediate emotional insights, while ensuring their memories are preserved in both a scalable **NoSQL database** and portable **PDF reports**.

## 🚀 The "Why" Factor

Why build a **Modular Monolith**?

In the era of microservices, we often overlook the complexity tax they incur. Moodie Journal adopts a **Modular Monolith** architecture to combine the best of both worlds:
- **Simplicity of Monoliths**: Single deployment unit, shared infrastructure, and easier debugging.
- **Flexibility of Microservices**: Distinct boundaries between the **AI**, **Database**, and **PDF** modules allow for independent development and future extraction into microservices if scaling demands it.

This architecture ensures **separation of concerns** while maintaining development velocity and reducing operational overhead.

---

## 🛠️ Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Language** | ![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python) | Core backend logic. |
| **Framework** | ![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey?logo=flask) | Lightweight WSGI web application framework. |
| **AI / ML** | ![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Transformers-yellow) | **DistilBERT** (SST-2) for robust sentiment analysis. |
| **Database** | ![MongoDB](https://img.shields.io/badge/MongoDB-Motor%2FPyMongo-green?logo=mongodb) | Flexible NoSQL storage for journal entries. |
| **Document** | ![FPDF](https://img.shields.io/badge/FPDF-PDF%20Generation-red) | Dynamic PDF report generation. |
| **Architecture** | **Modular Monolith** | Domain-driven design with Flask Blueprints. |

---

## 📂 Project Structure

Verified modular architecture designed for scalability:

```plaintext
MoodieJournal/
├── Modules/                  # 🧱 Domain Logic (The Core)
│   ├── __init__.py
│   ├── database/             # 💾 Persistence Layer
│   │   ├── __init__.py
│   │   └── mongo_client.py   # MongoDB Connection & CRUD
│   ├── pdf/                  # 📄 Document Layer
│   │   ├── __init__.py
│   │   ├── generator.py      # FPDF Generation Logic
│   │   └── routes.py         # Blueprint for PDF endpoints
│   └── sentiment/            # 🧠 AI Layer
│       ├── __init__.py
│       ├── logic.py          # Hugging Face DistilBERT Pipeline
│       └── routes.py         # Blueprint for Analysis endpoints
├── app.py                    # 🚀 Application Entry Point (Blueprints Reg)
├── requirements.txt          # 📦 Dependencies
└── README.md                 # 📖 Documentation
```

---

## ⚡ Technical Highlights

- **Automated End-to-End Pipeline**: A single API call triggers the flow: `Text Input` → `AI Analysis` → `DB Persistence` → `PDF Generation`.
- **Hybrid Data Handling**: MongoDB implementation includes logic to handle both legacy data structures and new schemas primarily involved in the sentiment upgrade.
- **Blueprints Architecture**: Features are encapsulated in blueprints (`sentiment_bp`, `pdf_bp`), making the codebase clean and maintainable.

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- MongoDB (Running locally or Atlas URI)

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/moodie-journal.git
cd moodie-journal/MoodieJournal
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
*(Dependencies include: `flask`, `pymongo`, `transformers`, `torch`, `fpdf`)*

### 4. Configuration (.env)
Create a `.env` file in the root directory to configure your environment variables.

```ini
# .env
FLASK_APP=app.py
FLASK_ENV=development

# Database
MONGO_URI=mongodb://localhost:27017/moodie_journal_db

# Optional: Model Configuration
HF_MODEL_NAME=distilbert-base-uncased-finetuned-sst-2-english
```
*Note: The current development version defaults to localhost if valid `.env` is not found.*

### 5. Run the Application
*Note: The first run may take a minute to download the Transformer model (~250MB) from Hugging Face.*
```bash
python app.py
```
Server will start at `http://localhost:5000`.

---

## 🔮 Upcoming Features

| Feature | Status | Description |
| :--- | :--- | :--- |
| **Streamlit UI** | 🚧 WIP | Interactive frontend for real-time journaling. |
| **Authentication** | ⏳ Planned | Secure JWT-based Login/Signup. |
| **AI Insights** | ⏳ Planned | Weekly mood trends and keyword extraction. |
| **Cloud Storage** | ⏳ Planned | Upload PDF reports to AWS S3. |

---

## 📝 API Reference

### 1. Complete Entry Workflow
- **Endpoint**: `POST /api/complete-entry`
- **Body**: `{"text": "I felt great today!"}`
- **Response**: Returns a downloadable PDF file containing the text and sentiment analysis.

### 2. Get History
- **Endpoint**: `GET /api/history`
- **Response**: JSON list of all past journal entries with sentiment scores.

---

> Built with ❤️ by the Moodie Journal Team.
