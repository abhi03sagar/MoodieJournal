from flask import Flask, request, jsonify, send_file
from fpdf import FPDF
import io
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
@app.route('/pdf', methods=['POST'])
def generate_pdf():
    data = request.json
    text = data.get('text', '')
    if not text:
        return jsonify({'error':'No text'}), 400
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=text.encode('latin-1', 'replace').decode('latin-1')) # Use multi_cell for wrapping

    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return send_file(pdf_output, as_attachment=True, download_name="diary_entry.pdf", mimetype='application/pdf')


if __name__ == '__main__':
    app.run(port=5002)
