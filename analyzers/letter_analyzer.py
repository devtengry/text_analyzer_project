from collections import Counter

def letter_frequency(text):
    letters = [char.lower() for char in text if char.isalpha()]
    return dict(Counter(letters))
