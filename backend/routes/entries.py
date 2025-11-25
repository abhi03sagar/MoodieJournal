from flask import Blueprint, request, jsonify, Response, stream_with_context, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from extensions import mongo
from datetime import datetime
# Import TextBlob here
from textblob import TextBlob
import requests # Replaces axios
from fpdf import FPDF
import io

entries_bp = Blueprint('entries', __name__)

@entries_bp.route('/', methods=['POST'])
@jwt_required()
def create_entry():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    text = data.get('text', '')

    # --- CHANGED SECTION START ---
    # We use TextBlob locally instead of calling port 5001
    try:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        if polarity > 0.1:
            sentiment = "Positive"
        elif polarity < -0.1:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
            
    except Exception as e:
        print(f"Sentiment Error: {e}")
        sentiment = "Unknown"
    # --- CHANGED SECTION END ---

    entry = {
        "user": current_user_id,
        "text": text,
        "date": datetime.utcnow(),
        "sentiment": sentiment
    }
    
    result = mongo.db.entries.insert_one(entry)
    entry['_id'] = str(result.inserted_id) # Convert ObjectId to string for JSON
    
    return jsonify(entry), 201

@entries_bp.route('/', methods=['GET'])
@jwt_required()
def get_entries():
    current_user_id = get_jwt_identity()
    
    # Find entries for this user and sort by date descending
    entries_cursor = mongo.db.entries.find({"user": current_user_id}).sort("date", -1)
    
    entries = []
    for doc in entries_cursor:
        doc['_id'] = str(doc['_id'])
        entries.append(doc)
        
    return jsonify(entries)

# 1. GET SINGLE ENTRY
@entries_bp.route('/<id>', methods=['GET'])
@jwt_required()
def get_entry(id):
    try:
        entry = mongo.db.entries.find_one({"_id": ObjectId(id)})
    except:
        return jsonify({"message": "Invalid ID format"}), 400

    if not entry:
        return jsonify({"message": "Entry not found"}), 404
        
    # Ensure the user owns this entry
    if entry['user'] != get_jwt_identity():
        return jsonify({"message": "Unauthorized access"}), 403

    entry['_id'] = str(entry['_id'])
    return jsonify(entry), 200

# 2. UPDATE ENTRY
@entries_bp.route('/<id>', methods=['PUT'])
@jwt_required()
def update_entry(id):
    data = request.get_json()
    new_text = data.get('text')
    
    if not new_text:
        return jsonify({"message": "Text is required"}), 400

    try:
        # Find and update in one go, ensuring user ownership
        # We also re-run sentiment analysis on the new text
        from textblob import TextBlob
        blob = TextBlob(new_text)
        polarity = blob.sentiment.polarity
        if polarity > 0.1: sentiment = "Positive"
        elif polarity < -0.1: sentiment = "Negative"
        else: sentiment = "Neutral"

        result = mongo.db.entries.update_one(
            {"_id": ObjectId(id), "user": get_jwt_identity()},
            {"$set": {
                "text": new_text, 
                "sentiment": sentiment,
                "last_modified": datetime.utcnow()
            }}
        )
    except:
        return jsonify({"message": "Invalid ID format"}), 400

    if result.matched_count == 0:
        return jsonify({"message": "Entry not found or unauthorized"}), 404

    return jsonify({"message": "Entry updated successfully"}), 200

# 3. DELETE ENTRY
@entries_bp.route('/<id>', methods=['DELETE'])
@jwt_required()
def delete_entry(id):
    try:
        result = mongo.db.entries.delete_one({
            "_id": ObjectId(id), 
            "user": get_jwt_identity()
        })
    except:
        return jsonify({"message": "Invalid ID format"}), 400

    if result.deleted_count == 0:
        return jsonify({"message": "Entry not found or unauthorized"}), 404

    return jsonify({"message": "Entry deleted successfully"}), 200

@entries_bp.route('/<id>/download', methods=['GET'])
@jwt_required()
def download_entry(id):
    try:
        entry = mongo.db.entries.find_one({"_id": ObjectId(id)})
    except:
        return jsonify({"message": "Invalid ID format"}), 400

    if not entry:
        return jsonify({"message": "Entry not found"}), 404

    try:
        # 2. Create PDF in memory
        pdf = FPDF()
        pdf.add_page()
        # Use Helvetica (Standard PDF font) instead of Arial to prevent errors
        pdf.set_font("Helvetica", size=12)
        
        # Add Content
        # Note: In fpdf2, arguments are text=..., new_x=..., new_y=... 
        # but ln=1 is still supported for backward compatibility.
        pdf.cell(200, 10, text="Moodie Journal Entry", ln=1, align='C')
        pdf.ln(10)
        pdf.cell(200, 10, text=f"Date: {entry['date']}", ln=1)
        pdf.cell(200, 10, text=f"Sentiment: {entry['sentiment']}", ln=1)
        pdf.ln(10)
        
        # Multi_cell for wrapping text
        pdf.multi_cell(0, 10, text=entry['text'])

        # 3. Save to memory buffer
        # fpdf2 output() returns a bytearray, which we can pass directly to BytesIO
        pdf_bytes = pdf.output()
        buffer = io.BytesIO(pdf_bytes)
        buffer.seek(0)

        # 4. Send file
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f"journal_entry_{id}.pdf",
            mimetype='application/pdf'
        )
    except Exception as e:
        print(f"PDF Generation Error: {e}")
        return jsonify({"message": "Could not generate PDF", "error": str(e)}), 500