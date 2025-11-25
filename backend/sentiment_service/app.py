from flask import Flask, request, jsonify
from textblob import TextBlob
from flask_cors import CORS
app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    text = data.get('text', '')
    if not text:
        return jsonify({'error': 'Text field is required'}), 400
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        sentiment = 'positive'
    elif polarity < -0.1:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'
    return jsonify({'sentiment': sentiment, 'polarity': polarity})

if __name__ == '__main__':
    app.run(port=5001)
