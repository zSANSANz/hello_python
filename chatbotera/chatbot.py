import nltk
import string
import warnings
import zipfile
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
try:
    from flask import Flask, render_template, request, jsonify
    flask_available = True
except Exception:
    flask_available = False
import os

# Supress warnings
warnings.filterwarnings('ignore')

# Download NLTK resources (only once)
nltk_resources = ['punkt', 'wordnet', 'omw-1.4', 'punkt_tab']
print("Checking NLTK resources...")
for resource in nltk_resources:
    try:
        if resource == 'punkt' or resource == 'punkt_tab':
            nltk.data.find(f'tokenizers/{resource}')
        else:
            nltk.data.find(f'corpora/{resource}')
    except (LookupError, zipfile.BadZipFile):
        try:
            nltk.download(resource, quiet=True)
        except Exception:
            # If download fails, continue; tokenizer/tokenization may still work for some inputs
            pass
print("NLTK resource check complete.")

# === Data Aturan (HR Knowledge Base) ===
data_aturan = """
Jam kerja perusahaan dimulai pukul 08.00 WIB dan berakhir pukul 17.00 WIB hari Senin sampai Jumat.
Karyawan wajib melakukan presensi kehadiran menggunakan sidik jari atau aplikasi mobile saat datang dan pulang.
Keterlambatan lebih dari 15 menit akan dikenakan pemotongan tunjangan kehadiran.
Pakaian kerja hari Senin sampai Kamis adalah kemeja rapi atau seragam kantor.
Pakaian kerja hari Jumat adalah batik atau pakaian kasual yang sopan.
Cuti tahunan diberikan sebanyak 12 hari kerja setelah karyawan bekerja selama 1 tahun berturut-turut.
Pengajuan cuti harus dilakukan minimal 3 hari sebelum tanggal cuti melalui sistem HRIS.
Izin sakit harus disertai dengan surat keterangan dokter yang sah.
Lembur hanya dihitung jika ada surat perintah lembur dari atasan.
Karyawan berhak mendapatkan tunjangan kesehatan dan BPJS Ketenagakerjaan.
Dilarang merokok di dalam ruang kerja, merokok hanya diperbolehkan di area khusus merokok.
Setiap karyawan wajib menjaga kerahasiaan data perusahaan.
"""

kalimat_tokens = nltk.sent_tokenize(data_aturan)
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(w) for w in tokens]
    return " ".join(tokens)

def get_response(user_input):
    # Handle empty input and simple greetings here so callers (including tests)
    if not user_input or not str(user_input).strip():
        return "Silakan masukkan pertanyaan."

    normalized = str(user_input).strip().lower()
    if normalized in ['halo', 'hi', 'selamat pagi', 'pagi']:
        return "Halo juga! Ada yang bisa saya bantu terkait aturan kerja?"

    temp_tokens = kalimat_tokens + [user_input]
    TfidfVec = TfidfVectorizer(tokenizer=lambda x: x.split(), preprocessor=clean_text)
    tfidf_matrix = TfidfVec.fit_transform(temp_tokens)
    vals = cosine_similarity(tfidf_matrix[-1], tfidf_matrix)
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]

    if req_tfidf == 0:
        return "Maaf, saya tidak menemukan informasi terkait hal tersebut dalam aturan perusahaan."
    else:
        idx = vals.argsort()[0][-2]
        return kalimat_tokens[idx]

if flask_available:
    # === Flask App ===
    app = Flask(__name__)

    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/get", methods=["POST"])
    def chatbot_response():
        user_msg = request.form.get("msg", "")
        response = get_response(user_msg)
        return jsonify({"response": response})

    if __name__ == "__main__":
        print("Starting Flask app...")
        app.run(debug=True)
else:
    # Flask not available in this environment; module can still be imported for testing get_response
    pass