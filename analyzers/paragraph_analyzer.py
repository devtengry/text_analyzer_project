def count_paragraphs(text):
    paragraphs = [p for p in text.split('\n') if p.strip() != '']
    return len(paragraphs)
