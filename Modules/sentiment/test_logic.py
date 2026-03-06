from MoodieJournal.Modules.sentiment.logic import sentiment_score

def manual_test():
    test_cases = [
        "I love this product!",
        "This is terrible",
        "The movie was just okay at best.",
        "I have no strong feelings about this.",
    ]

    for text in test_cases:
        result = sentiment_score(text)
        print(f"Text: {text}, Result: {result}")

if __name__ == "__main__":
    manual_test()