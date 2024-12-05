import io
from flask import Flask, render_template, request, jsonify, send_file
from analyzers.character_analyzer import count_characters
from analyzers.word_analyzer import count_words
from analyzers.sentence_analyzer import count_sentences
from analyzers.paragraph_analyzer import count_paragraphs
from analyzers.punctuation_analyzer import count_punctuation
from analyzers.digit_analyzer import count_digits
from analyzers.letter_analyzer import letter_frequency
from analyzers.word_frequency_analyzer import word_frequency
import matplotlib.pyplot as plt

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

    return jsonify({"Harf Sıklığı": result})

# Kelime frekansı arama işlemi
@app.route('/search_word', methods=['POST'])
def arama_kelime():
    global word_freq

    kelime = request.form['word']
    result = word_freq.get(kelime, "Kelime bulunamadı")

    return jsonify({"Kelime Sıklığı": result})

# Görsel oluşturma işlemi
@app.route('/draw_image', methods=['POST'])
def draw_image():
    metin = request.form['text']

    if not metin:
        return jsonify({"hata": "Metin boş olamaz!"}), 400

    # Analiz verilerini al
    analiz_sonuclari = {
        "Kelime Sayısı": count_words(metin),
        "Cümle S.": count_sentences(metin),
        "Paragraf S.": count_paragraphs(metin),
        "Noktalama İşareti S.": count_punctuation(metin),
        "Rakam S.": count_digits(metin)
    }

    # Grafik çizimi
    labels = list(analiz_sonuclari.keys())
    values = list(analiz_sonuclari.values())

    plt.figure(figsize=(8, 6))
    plt.bar(labels, values, color=['skyblue', 'orange', 'green', 'purple', 'red'])
    plt.title('Metin Analiz Sonuçları')
    plt.xlabel('Özellikler')
    plt.ylabel('Değerler')
    plt.tight_layout()

    # Görseli belleğe kaydet
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)
