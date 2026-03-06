import os
from flask import Flask, request, jsonify, send_file
from Modules.sentiment.routes import sentiment_bp
from Modules.sentiment.logic import sentiment_score
from Modules.pdf.generator import create_journal_pdf
from Modules.pdf.routes import pdf_bp
from Modules.database.mongo_client import save_entry, get_all_entries

app = Flask(__name__)

app.register_blueprint(sentiment_bp, url_prefix='/api/sentiment')
app.register_blueprint(pdf_bp, url_prefix='/api/pdf')

@app.route('/')
def home():
    return {"message": "Moodie Journal API is running!"}


@app.route('/api/complete-entry', methods=['POST'])
def complete_entry():
    data = request.get_json()
    text = data.get('text', '')

    analysis = sentiment_score(text)
    
    db_id = save_entry(text, analysis['sentiment'], analysis['confidence'])

    file_path = create_journal_pdf(text, analysis['sentiment'])

    try:
        return send_file(
            os.path.abspath(file_path), 
            mimetype='application/pdf', 
            as_attachment=True, 
            download_name=f"journal_{db_id}.pdf"
        )
    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/api/history', methods=['GET'])
def history():
    return jsonify(get_all_entries())

if __name__ == '__main__':
    app.run(debug=True) 