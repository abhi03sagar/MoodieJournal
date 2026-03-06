from flask import Blueprint, request, send_file
from .generator import create_journal_pdf

pdf_bp = Blueprint('pdf_bp', __name__)

@pdf_bp.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    text = data.get('text', 'No content')
    sentiment = data.get('sentiment', 'Unknown')
    
    file_path = create_journal_pdf(text, sentiment)
    
    return send_file(file_path, as_attachment=True)