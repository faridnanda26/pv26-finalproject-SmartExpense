import pandas as pd
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

def train_category_model():
    # Dataset berdasarkan 8 kategori
    data = {
        'deskripsi': [
            # 1. Makanan
            'nasi goreng kambing', 'bakso urat', 'makan siang kantor', 'kopi senja', 'indomaret snack', 'ayam geprek',
            # 2. Minuman
            'jus alpukat', 'aqua galon', 'teh botol', 'kopi susu gula aren', 'minuman boba', 'susu uht',
            # 3. Pakaian
            'beli kaos polos', 'celana jeans', 'jaket hoddie', 'cuci baju laundry', 'sepatu running', 'kemeja kerja',
            # 4. Transportasi
            'bensin pertalite', 'tarif parkir', 'ojek online grab', 'tiket kereta api', 'service ganti oli', 'bayar tol',
            # 5. Hiburan
            'nonton bioskop xxi', 'langganan netflix', 'top up game', 'tiket konser', 'karaoke keluarga', 'buku novel',
            # 6. Tagihan & Listrik
            'token listrik pln', 'tagihan air pdam', 'iuran wifi indihome', 'pulsa pascabayar', 'cicilan rumah', 'pajak motor',
            # 7. Edukasi
            'beli buku pelajaran', 'kursus bahasa inggris', 'pembayaran ukt', 'alat tulis kantor', 'seminar web', 'fotokopi',
            # 8. Kesehatan
            'beli obat flu apotek', 'konsultasi dokter', 'vitamin c', 'masker medis', 'biaya rawat inap', 'pasta gigi sabun'
        ],
        'kategori': [
            'Makanan', 'Makanan', 'Makanan', 'Makanan', 'Makanan', 'Makanan',
            'Minuman', 'Minuman', 'Minuman', 'Minuman', 'Minuman', 'Minuman',
            'Pakaian', 'Pakaian', 'Pakaian', 'Pakaian', 'Pakaian', 'Pakaian',
            'Transportasi', 'Transportasi', 'Transportasi', 'Transportasi', 'Transportasi', 'Transportasi',
            'Hiburan', 'Hiburan', 'Hiburan', 'Hiburan', 'Hiburan', 'Hiburan',
            'Tagihan & Listrik', 'Tagihan & Listrik', 'Tagihan & Listrik', 'Tagihan & Listrik', 'Tagihan & Listrik', 'Tagihan & Listrik',
            'Edukasi', 'Edukasi', 'Edukasi', 'Edukasi', 'Edukasi', 'Edukasi',
            'Kesehatan', 'Kesehatan', 'Kesehatan', 'Kesehatan', 'Kesehatan', 'Kesehatan'
        ]
    }

    df = pd.DataFrame(data)

    # Membangun Pipeline (TF-IDF + Naive Bayes)
    model = make_pipeline(TfidfVectorizer(), MultinomialNB())
    model.fit(df['deskripsi'], df['kategori'])

    # Simpan ke folder assets/models
    os.makedirs("assets/models", exist_ok=True)
    joblib.dump(model, "assets/models/category_classifier.pkl")
    print("Model Klasifikasi 8 Kategori berhasil disimpan!")

if __name__ == "__main__":
    train_category_model()