from flask import Flask, render_template, request, jsonify
from analyzers.character_analyzer import count_characters
from analyzers.word_analyzer import count_words
from analyzers.sentence_analyzer import count_sentences
from analyzers.paragraph_analyzer import count_paragraphs
from analyzers.punctuation_analyzer import count_punctuation
from analyzers.digit_analyzer import count_digits
from analyzers.letter_analyzer import letter_frequency
from analyzers.word_frequency_analyzer import word_frequency
from utils import save_analysis_to_file, save_analysis_to_json
import json

app = Flask(__name__)

# Ana sayfa
@app.route('/')
def anasayfa():
    return render_template('index.html')

# Analiz işlemi için endpoint
@app.route('/analyze', methods=['POST'])
def analiz():
    metin = request.form['text']

    if not metin:
        return jsonify({"hata": "Metin boş olamaz!"}), 400

    analiz_sonuclari = {
        "Toplam Karakter Sayısı": count_characters(metin),
        "Toplam Kelime Sayısı": count_words(metin),
        "Toplam Cümle Sayısı": count_sentences(metin),
        "Toplam Paragraf Sayısı": count_paragraphs(metin),
        "Toplam Noktalama İşareti Sayısı": count_punctuation(metin),
        "Toplam Rakam Sayısı": count_digits(metin),
        "Harf Frekansı": json.dumps(letter_frequency(metin), ensure_ascii=False),
        "Kelime Frekansı": json.dumps(word_frequency(metin), ensure_ascii=False)
    }

    return jsonify(analiz_sonuclari)

if __name__ == "__main__":
    app.run(debug=True)
