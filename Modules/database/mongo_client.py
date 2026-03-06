from pymongo import MongoClient
import datetime

try:
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
    db = client["moodie_journal_db"]
    collection = db["entries"]
    client.server_info() 
except Exception as e:
    print(f"DATABASE CONNECTION ERROR: {e}")

def save_entry(text, sentiment, confidence):
    entry = {
        "text": text,
        "sentiment": sentiment,
        "confidence": confidence,
        "timestamp": datetime.datetime.now()
    }
    result = collection.insert_one(entry)
    return str(result.inserted_id)

def get_all_entries():
    entries = list(collection.find().sort("timestamp", -1))
    
    for entry in entries:
        entry["_id"] = str(entry["_id"])
        
        if "timestamp" in entry:
            entry["date_pretty"] = entry["timestamp"].strftime("%B %d, %Y")
        else:
            entry["date_pretty"] = "Legacy Entry (No Date)"
            
    return entries