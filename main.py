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

    metin = request.form.get('text', '')
    print(f"Gelen metin: {metin}")  # Loglama

    if not metin.strip():
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

    print(f"Analiz Sonuçları: {analiz_sonuclari}")  # Loglama
    return jsonify(analiz_sonuclari)

# Harf frekansı arama işlemi
@app.route('/search_letter', methods=['POST'])
def arama_harf():
    global letter_freq

    harf = request.form.get('letter', '').lower()
    print(f"Aranan harf: {harf}")  # Loglama

    if not harf or len(harf) != 1 or not harf.isalpha():
        return jsonify({"Harf Frekansı": "Geçerli bir harf giriniz!"})

    result = letter_freq.get(harf, 0)
    return jsonify({"Harf Frekansı": result})

# Kelime frekansı arama işlemi
@app.route('/search_word', methods=['POST'])
def arama_kelime():
    global word_freq

    kelime = request.form.get('word', '')
    print(f"Aranan kelime: {kelime}")  # Loglama

    if not kelime.strip():
        return jsonify({"Kelime Frekansı": "Geçerli bir kelime giriniz!"})

    result = word_freq.get(kelime, 0)
    return jsonify({"Kelime Frekansı": result})

if __name__ == "__main__":
    app.run(debug=True)
