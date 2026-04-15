from functools import lru_cache
from transformers import pipeline

model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"


@lru_cache(maxsize=1)
def load_classifier():
    return pipeline("sentiment-analysis", model=model_name)


def sentiment_score(text):

    if not text or len(text.strip()) == 0:
        return {
            "text": text,
            "sentiment": "NEUTRAL",
            "confidence": 0.0,
        }
    try:
        classifier = load_classifier()
        result = classifier(text)[0]  
        return {
            "text": text,
            "sentiment": result['label'],
            "confidence": round(result['score'], 4)
        }

    except Exception as e:
        print(f"Error occurred while analyzing sentiment for text: {text}")
        print(f"Error details: {e}")

if __name__ == "__main__":
    sample_text = "I hate to say this but I am starting to admit his talent over mine."
    print(sentiment_score(sample_text))
