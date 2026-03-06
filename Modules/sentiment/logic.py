from transformers import pipeline

model_name = "distilbert-base-uncased-finetuned-sst-2-english"
classifier = pipeline("sentiment-analysis", model=model_name)

def sentiment_score(text):

    result = classifier(text)[0]

    label = result['label'].upper()
    score = result['score']

    return {
        "text": text,
        "sentiment": label,
        "confidence": round(score, 4),
        "model": model_name
    }

if __name__ == "__main__":
    sample_text = "I love this product! It's amazing and works perfectly."
    print(sentiment_score(sample_text))
