import string

def count_punctuation(text):
    return sum([1 for char in text if char in string.punctuation])
