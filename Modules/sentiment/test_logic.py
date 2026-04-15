from Modules.sentiment.logic import sentiment_score

def manual_test():
    test_cases = [
        "I love this product!",
        "This is terrible",
        "Politics is such a deep topic of discussion.",
        "To me it is not much special but not bad at all.",
    ]

    for text in test_cases:
        result = sentiment_score(text)
        print(f"Text: {text}, Result: {result}")

if __name__ == "__main__":
    manual_test()