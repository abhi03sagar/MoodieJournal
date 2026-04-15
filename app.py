import os
from flask import Flask, request, jsonify, send_file
from flask_jwt_extended import JWTManager, get_jwt, get_jwt_identity, jwt_required
from Modules.sentiment.routes import sentiment_bp
from Modules.sentiment.logic import sentiment_score
from Modules.pdf.generator import create_journal_pdf
from Modules.pdf.routes import pdf_bp
from Modules.database.mongo_client import save_entry_for_user, get_all_entries, get_entries_for_user
from Modules.user.routes import user_bp

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'change-this-in-production-jwt-secret-32chars')
jwt = JWTManager(app)

app.register_blueprint(sentiment_bp, url_prefix='/api/sentiment')
app.register_blueprint(pdf_bp, url_prefix='/api/pdf')
app.register_blueprint(user_bp, url_prefix='/api/users')

@app.route('/')
def home():
    return {"message": "Moodie Journal API is running!"}


@app.route('/api/complete-entry', methods=['POST'])
@jwt_required()
def complete_entry():
    data = request.get_json() or {}
    text = data.get('text', '')
    user_id = get_jwt_identity()
    claims = get_jwt()
    username = claims.get('username')
    email = claims.get('email')

    analysis = sentiment_score(text)

    db_id = save_entry_for_user(
        text,
        analysis['sentiment'],
        analysis['confidence'],
        user_id=user_id,
        username=username,
        email=email,
    )

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
@jwt_required()
def history():
    user_id = str(get_jwt_identity() or '').strip()
    if not user_id:
        return jsonify({"status": "error", "message": "Invalid token identity."}), 401
    return jsonify(get_entries_for_user(user_id))

if __name__ == '__main__':
    app.run(debug=True) 