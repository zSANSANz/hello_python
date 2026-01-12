import csv
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Unduh resource NLTK jika belum ada
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)

# Langkah 1: Baca file CSV dan ekstrak teks pidatoimport csv
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Unduh resource NLTK jika belum ada
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)

# Langkah 1: Baca file CSV dan ekstrak teks pidato
def read_speech_from_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        lines = [row[0] for row in reader if row]
    full_text = ' '.join(lines)
    return full_text

# Langkah 2: Pra-pemrosesan teks
def preprocess_text(text):
    # Hapus tanda kutip ganda berlebih dan baris kosong
    text = re.sub(r'""', '"', text)
    # Hapus bagian metadata non-esensial (opsional)
    text = re.sub(r'PIDATO PERDANA PRESIDEN.*?2025', '', text, flags=re.DOTALL)
    text = re.sub(r'Sumber :.*', '', text, flags=re.DOTALL)
    text = re.sub(r'https?://\S+', '', text)  # hapus URL

    sentences = sent_tokenize(text)

    # Hanya pertahankan huruf dan spasi, lalu lowercase
    clean_text = re.sub(r'[^a-zA-Z\s]', ' ', text.lower())
    tokens = word_tokenize(clean_text)

    # Stopwords Bahasa Indonesia + Inggris
    stop_words = set(stopwords.words('indonesian') + stopwords.words('english'))
    # Tambahkan stopwords umum dalam teks politik
    custom_stop = {'yang', 'di', 'ke', 'dari', 'ini', 'itu', 'kami', 'kita', 'mereka', 'akan', 'dengan', 'untuk', 'pada', 'adalah', 'juga', 'namun', 'sebagai', 'dalam', 'oleh', 'semua', 'harus', 'bisa', 'jadi', 'akan', 'harap', 'mari', 'kata', 'katakan', 'katakanlah'}
    stop_words.update(custom_stop)

    tokens = [word for word in tokens if word not in stop_words and len(word) > 2]
    return tokens, sentences

# Langkah 3: Ekstrak 5 topik penting berdasarkan frasa kontekstual
def extract_top_topics(sentences):
    keyword_sets = [
        ("Palestina", "Israel", "dua negara", "solusi dua negara", "Gaza"),
        ("PBB", "Perserikatan Bangsa-Bangsa", "multilateralisme", "Dewan Keamanan"),
        ("perubahan iklim", "kenaikan permukaan laut", "emisi nol bersih", "energi terbarukan", "hutan"),
        ("ketahanan pangan", "beras", "swasembada", "lumbung pangan", "FAO"),
        ("perdamaian", "Pasukan Penjaga Perdamaian", "konflik", "keadilan", "solidaritas")
    ]

    labels = [
        "Isu Palestina dan Solusi Dua Negara",
        "Komitemen terhadap PBB dan Multilateralisme",
        "Aksi Nyata terhadap Perubahan Iklim",
        "Ketahanan Pangan dan Swasembada Beras",
        "Perdamaian Global dan Peran Indonesia"
    ]

    found_topics = []
    for keywords, label in zip(keyword_sets, labels):
        for sentence in sentences:
            if any(kw.lower() in sentence.lower() for kw in keywords):
                if label not in found_topics:
                    found_topics.append(label)
                break
    return found_topics[:5]

# Main execution
if __name__ == "__main__":
    file_path = r"pindato_prabowo.csv"
    
    speech_text = read_speech_from_csv(file_path)
    tokens, sentences = preprocess_text(speech_text)
    top_topics = extract_top_topics(sentences)

    print("\n5 Topik Penting dalam Pidato Prabowo di PBB:\n")
    for i, topic in enumerate(top_topics, 1):
        print(f"{i}. {topic}")

    # === Tambahkan WordCloud ===
    word_freq = Counter(tokens)
    
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        colormap='viridis',
        collocations=False  # agar tidak menggabungkan frasa (misal "dua negara" jadi satu)
    ).generate_from_frequencies(word_freq)

    plt.figure(figsize=(12, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title("Word Cloud – Kata-Kata Dominan dalam Pidato Prabowo di PBB", fontsize=16, pad=20)
    plt.tight_layout()
    plt.show()
def read_speech_from_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        lines = [row[0] for row in reader if row]  # Ambil setiap baris pertama (asumsi 1 kolom)
    # Gabungkan semua baris jadi satu teks
    full_text = ' '.join(lines)
    return full_text

# Langkah 2: Pra-pemrosesan teks
def preprocess_text(text):
    # Hapus tanda kutip ganda berlebih dan baris kosong
    text = re.sub(r'""', '"', text)
    # Hanya ambil bagian antara pembuka dan penutup pidato (opsional)
    # Di sini kita ambil semua teks karena struktur sudah bersih
    # Tokenisasi kalimat
    sentences = sent_tokenize(text)
    # Gabungkan lagi untuk proses kata
    clean_text = re.sub(r'[^a-zA-Z\s]', ' ', text.lower())
    tokens = word_tokenize(clean_text)
    stop_words = set(stopwords.words('indonesian') + stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words and len(word) > 2]
    return tokens, sentences

# Langkah 3: Ekstrak 5 topik penting berdasarkan frasa kontekstual
def extract_top_topics(sentences):
    # Kita gunakan pendekatan berbasis frasa kunci yang muncul dalam konteks penting
    topics = []

    # Daftar frasa/frasa indikator topik penting
    keyword_sets = [
        ("Palestina", "Israel", "dua negara", "solusi dua negara", "Gaza"),
        ("PBB", "Perserikatan Bangsa-Bangsa", "multilateralisme", "Dewan Keamanan"),
        ("perubahan iklim", "kenaikan permukaan laut", "emisi nol bersih", "energi terbarukan", "hutan"),
        ("ketahanan pangan", "beras", "swasembada", "lumbung pangan", "FAO"),
        ("perdamaian", "Pasukan Penjaga Perdamaian", "konflik", "keadilan", "solidaritas")
    ]

    found_topics = []
    for i, keywords in enumerate(keyword_sets, 1):
        for sentence in sentences:
            if any(kw.lower() in sentence.lower() for kw in keywords):
                label = {
                    1: "Isu Palestina dan Solusi Dua Negara",
                    2: "Komitemen terhadap PBB dan Multilateralisme",
                    3: "Aksi Nyata terhadap Perubahan Iklim",
                    4: "Ketahanan Pangan dan Swasembada Beras",
                    5: "Perdamaian Global dan Peran Indonesia"
                }[i]
                if label not in found_topics:
                    found_topics.append(label)
                break  # Cukup temukan 1 kalimat representatif

    return found_topics[:5]

# Main execution
if __name__ == "__main__":
    file_path = r"pindato_prabowo.csv"
    
    speech_text = read_speech_from_csv(file_path)
    tokens, sentences = preprocess_text(speech_text)
    top_topics = extract_top_topics(sentences)

    print("\n5 Topik Penting dalam Pidato Prabowo di PBB:\n")
    for i, topic in enumerate(top_topics, 1):
        print(f"{i}. {topic}")