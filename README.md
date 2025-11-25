# Moodie Journal 📝✨

Moodie Journal is a full-stack journaling application that helps users track their thoughts and emotions. It features secure authentication, automatic sentiment analysis of entries, and the ability to export journal entries as PDF files.

## 🚀 Features

*   **User Authentication:** Secure Register and Login using JWT (JSON Web Tokens).
*   **Create Entries:** Write journal entries which are stored securely in MongoDB.
*   **Sentiment Analysis:** Automatically analyzes the mood of your entry (Positive, Negative, Neutral) using NLP (`TextBlob`).
*   **CRUD Operations:** Full Create, Read, Update, and Delete functionality for entries.
*   **PDF Export:** Download any journal entry as a formatted PDF file.
*   **Security:** Password hashing with Bcrypt.

## 🛠️ Tech Stack

*   **Backend:** Python, Flask
*   **Database:** MongoDB
*   **Authentication:** Flask-JWT-Extended
*   **NLP:** TextBlob
*   **PDF Generation:** FPDF2
*   **Frontend:** Streamlit (Planned/In Progress)

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd moodie-journal
```

### 2. Backend Setup
Navigate to the backend folder:
```bash
cd backend
```

Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the `backend` folder (optional, or use `config.py` defaults) and add your MongoDB URI:
```env
MONGO_URI=mongodb://localhost:27017/moodie_journal_db
SECRET_KEY=super-complex-random-string-nobody-can-guess
JWT_SECRET=another-super-complex-random-string
```

### 4. Run the Server
```bash
python app.py
```
The server will start on `http://127.0.0.1:5000`.

## 📡 API Endpoints

### Authentication
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/auth/register` | Register a new user |
| `POST` | `/api/auth/login` | Login and get Access Token |

### Journal Entries (Requires Bearer Token)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/entries/` | Create a new entry |
| `GET` | `/api/entries/` | Get all entries for logged-in user |
| `GET` | `/api/entries/<id>` | Get a specific entry |
| `PUT` | `/api/entries/<id>` | Update an entry |
| `DELETE` | `/api/entries/<id>` | Delete an entry |
| `GET` | `/api/entries/<id>/download` | Download entry as PDF |

## 🧪 Testing

You can test the API using **Postman** or **Thunder Client**.

1.  **Login** to get an `accessToken`.
2.  Add the token to the **Headers** of subsequent requests:
    *   Key: `Authorization`
    *   Value: `Bearer YOUR_ACCESS_TOKEN`
