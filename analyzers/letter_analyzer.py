from collections import Counter

def letter_frequency(text):
    # Harfleri seç ve küçük harfe çevir
    letters = [char.lower() for char in text if char.isalpha()]
    # Harf frekanslarını hesapla
    return dict(Counter(letters))
