from collections import Counter

def word_frequency(text):
    words = text.split()
    return dict(Counter(words))
