from flask import Flask, render_template, request, jsonify
from analyzers.character_analyzer import count_characters
from analyzers.word_analyzer import count_words
from analyzers.sentence_analyzer import count_sentences
from analyzers.paragraph_analyzer import count_paragraphs
from analyzers.punctuation_analyzer import count_punctuation
from analyzers.digit_analyzer import count_digits
from analyzers.letter_analyzer import letter_frequency
from analyzers.word_frequency_analyzer import word_frequency

app = Flask(__name__)

# Analiz sonuçlarını saklayacak global değişkenler
letter_freq = {}
word_freq = {}

# Ana sayfa
@app.route('/')
def anasayfa():
    return render_template('index.html')

# Metni analiz etme işlemi
@app.route('/analyze', methods=['POST'])
def analiz():
    global letter_freq, word_freq

    metin = request.form['text']

    if not metin:
        return jsonify({"hata": "Metin boş olamaz!"}), 400

    # Harf ve kelime frekanslarını global değişkenlere kaydet
    letter_freq = letter_frequency(metin)
    word_freq = word_frequency(metin)

    analiz_sonuclari = {
        "Toplam Karakter Sayısı": count_characters(metin),
        "Toplam Kelime Sayısı": count_words(metin),
        "Toplam Cümle Sayısı": count_sentences(metin),
        "Toplam Paragraf Sayısı": count_paragraphs(metin),
        "Toplam Noktalama İşareti Sayısı": count_punctuation(metin),
        "Toplam Rakam Sayısı": count_digits(metin)
    }

    return jsonify(analiz_sonuclari)

# Harf frekansı arama işlemi
@app.route('/search_letter', methods=['POST'])
def arama_harf():
    global letter_freq

    harf = request.form['letter']
    result = letter_freq.get(harf, "Harf bulunamadı")

    return jsonify({"Harf Frekansı": result})

# Kelime frekansı arama işlemi
@app.route('/search_word', methods=['POST'])
def arama_kelime():
    global word_freq

    kelime = request.form['word']
    result = word_freq.get(kelime, "Kelime bulunamadı")

    return jsonify({"Kelime Frekansı": result})

if __name__ == "__main__":
    app.run(debug=True)
