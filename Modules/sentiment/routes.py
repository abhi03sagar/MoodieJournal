from flask import Blueprint, request, jsonify
from .logic import sentiment_score
sentiment_bp = Blueprint('sentiment_bp', __name__)

@sentiment_bp.route('/analyse', methods = ['POST'])
def analyse_text():
    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({"error": "Bad request"}), 400  

    result = sentiment_score(data['text'])
    return jsonify({"status": "success", "data": result})
