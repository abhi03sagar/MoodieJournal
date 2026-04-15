from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import datetime
import time
import os

client = None
db = None
collection = None
users_collection = None
def connect_with_retry(retries=5, delay=2):
    global client
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    for attempt in range(retries):
        try:
            client = MongoClient(mongo_uri, serverSelectionTimeoutMS=2000)
            client.admin.command('ping')
            print("Database connected")
            try:
                default_db = client.get_default_database()
            except Exception:
                default_db = None
            if default_db is not None:
                return default_db
            return client["moodie_journal_db"]
        except Exception as e:
            print(f"Attempt {attempt + 1} - DATABASE CONNECTION ERROR: {e}")
            if attempt < retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
    print("Failed to connect to MongoDB after multiple attempts. Exiting.")
db = connect_with_retry()
collection = db["entries"] if db is not None else None
users_collection = db["users"] if db is not None else None

if users_collection is not None:
    users_collection.create_index("username", unique=True)
    users_collection.create_index("email", unique=True)

def save_entry(text, sentiment, confidence):
    if collection is None:
        print("Cannot save entry: No database connection.")
        return None
    entry = {
        "text": text,
        "sentiment": sentiment,
        "confidence": confidence,
        "timestamp": datetime.datetime.now()
    }
    result = collection.insert_one(entry)
    return str(result.inserted_id)


def save_entry_for_user(text, sentiment, confidence, user_id=None, username=None, email=None):
    if collection is None:
        print("Cannot save entry: No database connection.")
        return None

    entry = {
        "text": text,
        "sentiment": sentiment,
        "confidence": confidence,
        "timestamp": datetime.datetime.now(),
    }

    if user_id:
        entry["user_id"] = str(user_id)
    if username:
        entry["username"] = username
    if email:
        entry["email"] = email

    result = collection.insert_one(entry)
    return str(result.inserted_id)

def get_all_entries():
    if collection is None:
        print("There are currently no entries.")
        return []
    entries = list(collection.find().sort("timestamp", -1))
    
    for entry in entries:
        entry["_id"] = str(entry["_id"])
        
        if "timestamp" in entry:
            entry["date_pretty"] = entry["timestamp"].strftime("%B %d, %Y")
        else:
            entry["date_pretty"] = "Legacy Entry (No Date)"
            
    return entries


def get_entries_for_user(user_id):
    if collection is None:
        print("There are currently no entries.")
        return []

    normalized_user_id = str(user_id or "").strip()
    if not normalized_user_id:
        return []

    entries = list(collection.find({"user_id": normalized_user_id}).sort("timestamp", -1))

    for entry in entries:
        entry["_id"] = str(entry["_id"])

        if "timestamp" in entry:
            entry["date_pretty"] = entry["timestamp"].strftime("%B %d, %Y")
        else:
            entry["date_pretty"] = "Legacy Entry (No Date)"

    return entries


def create_user(username, email, password_hash):
    if users_collection is None:
        return {"ok": False, "error": "No database connection."}

    user = {
        "username": username,
        "email": email,
        "password_hash": password_hash,
        "created_at": datetime.datetime.now()
    }

    try:
        result = users_collection.insert_one(user)
        return {"ok": True, "user_id": str(result.inserted_id)}
    except DuplicateKeyError:
        return {"ok": False, "error": "Username or email already exists."}


def authenticate_user(username, email):
    if users_collection is None:
        return None

    query = {"$or": []}

    if username:
        query["$or"].append({"username": username})

    if email:
        query["$or"].append({"email": email})

    if not query["$or"]:
        return None

    return users_collection.find_one(query)