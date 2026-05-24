"""
Aplikasi Web Flask untuk Sistem Prediksi Status Obesitas
Penelitian: Pengembangan Sistem Prediksi Status Obesitas dan Rekomendasi
            Manajemen Berat Badan Menggunakan Random Forest

Cara menjalankan:
    1. Pastikan file rf_model.pkl dan scaler.pkl ada di folder yang sama
    2. Install dependensi: pip install flask numpy scikit-learn
    3. Jalankan: python app.py
    4. Buka browser: http://127.0.0.1:5000
"""

from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import pandas as pd

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Memuat model dan scaler yang sudah disimpan dari tahap training
with open('rf_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# Urutan fitur harus sama persis dengan urutan saat training
FEATURE_ORDER = ['Height', 'Weight', 'Age', 'Gender', 'FAF', 'FAVC', 'CH2O']


def hitung_bmi(berat, tinggi):
    """Menghitung BMI berdasarkan rumus WHO yaitu berat dibagi kuadrat tinggi"""
    return round(berat / (tinggi ** 2), 2)


def kategori_bmi(bmi):
    """Mengkategorikan BMI sesuai standar WHO untuk orang dewasa"""
    if bmi < 18.5:
        return 'Kurus'
    elif bmi < 25:
        return 'Normal'
    else:
        return 'Overweight/Obesitas'


def rentang_berat_ideal(tinggi):
    """Menghitung rentang berat badan ideal berdasarkan BMI sehat 18.5 sampai 24.9"""
    berat_min = round(18.5 * (tinggi ** 2), 1)
    berat_max = round(24.9 * (tinggi ** 2), 1)
    return berat_min, berat_max


def generate_rekomendasi(prediksi, berat_aktual, tinggi, faf, favc, ch2o):
    """
    Menghasilkan rekomendasi personal berdasarkan kelas prediksi dan input pengguna
    Mengembalikan dictionary berisi target berat, selisih, arah, dan saran lifestyle
    """
    berat_min, berat_max = rentang_berat_ideal(tinggi)
    berat_target_tengah = round((berat_min + berat_max) / 2, 1)

    rekomendasi = {
        'berat_ideal_min': berat_min,
        'berat_ideal_max': berat_max,
        'berat_target': berat_target_tengah,
        'selisih': 0,
        'arah': '',
        'lifestyle': []
    }

    if prediksi == 'Kurus':
        rekomendasi['selisih'] = round(berat_min - berat_aktual, 1)
        rekomendasi['arah'] = 'naikkan'
        rekomendasi['lifestyle'] = [
            'Tingkatkan asupan kalori dengan makanan padat gizi seperti kacang-kacangan, alpukat, dan ikan',
            'Konsumsi 5 sampai 6 porsi kecil per hari daripada 3 porsi besar',
            'Lakukan latihan beban (strength training) 3 sampai 4 kali per minggu untuk membangun massa otot',
            'Pastikan tidur cukup 7 sampai 8 jam per malam untuk mendukung pemulihan dan pertumbuhan',
            'Konsultasikan dengan ahli gizi jika underweight berlangsung lama'
        ]
    elif prediksi == 'Normal':
        rekomendasi['selisih'] = 0
        rekomendasi['arah'] = 'pertahankan'
        rekomendasi['lifestyle'] = [
            'Pertahankan pola makan seimbang dengan porsi sayur dan buah yang cukup',
            'Lanjutkan aktivitas fisik minimal 150 menit per minggu sesuai rekomendasi WHO',
            'Pertahankan konsumsi air minimal 2 liter per hari',
            'Lakukan pemeriksaan kesehatan rutin minimal setahun sekali',
            'Hindari konsumsi makanan tinggi gula dan lemak jenuh secara berlebihan'
        ]
    else:  # Obesitas
        rekomendasi['selisih'] = round(berat_aktual - berat_max, 1)
        rekomendasi['arah'] = 'turunkan'
        saran = [
            'Targetkan defisit kalori 500 sampai 750 kkal per hari untuk penurunan 0.5 sampai 1 kg per minggu',
            'Tingkatkan aktivitas fisik minimal 30 menit per hari dengan intensitas sedang',
            'Kurangi konsumsi makanan tinggi kalori, gula tambahan, dan lemak jenuh'
        ]
        if favc == 1:
            saran.append('Berdasarkan input Anda yang sering konsumsi makanan tinggi kalori, batasi frekuensinya menjadi 1 sampai 2 kali per minggu saja')
        if faf < 1:
            saran.append('Aktivitas fisik Anda tergolong rendah, mulai dengan jalan kaki 30 menit per hari lalu tingkatkan bertahap')
        if ch2o < 2:
            saran.append('Konsumsi air Anda kurang dari rekomendasi, tingkatkan menjadi minimal 2 liter per hari untuk membantu metabolisme')
        saran.append('Konsultasi dengan dokter atau ahli gizi untuk program penurunan berat badan yang aman')
        rekomendasi['lifestyle'] = saran

    return rekomendasi


@app.route('/')
def home():
    """Menampilkan halaman utama dengan form input"""
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint untuk memproses input pengguna dan mengembalikan prediksi"""
    try:
        # Mengambil input dari form
        tinggi = float(request.form['height'])
        berat = float(request.form['weight'])
        umur = float(request.form['age'])
        gender = int(request.form['gender'])  # 1 untuk Male, 0 untuk Female
        faf = float(request.form['faf'])
        favc = int(request.form['favc'])  # 1 untuk yes, 0 untuk no
        ch2o = float(request.form['ch2o'])

        # Validasi input dasar
        if tinggi <= 0 or berat <= 0 or umur <= 0:
            return jsonify({'error': 'Input tidak boleh nol atau negatif'}), 400
        if tinggi < 1.0 or tinggi > 2.5:
            return jsonify({'error': 'Tinggi badan harus dalam rentang 1.0 sampai 2.5 meter'}), 400

        # Menyusun input sebagai DataFrame agar konsisten dengan feature names saat training
        input_df = pd.DataFrame([[tinggi, berat, umur, gender, faf, favc, ch2o]],
                                 columns=FEATURE_ORDER)

        # Transformasi menggunakan scaler yang sama dengan training
        input_scaled = scaler.transform(input_df)

        # Prediksi kelas
        prediksi = model.predict(input_scaled)[0]
        probabilitas = model.predict_proba(input_scaled)[0]
        kelas_model = model.classes_

        # Membuat dictionary probabilitas
        prob_dict = {kelas: round(float(prob) * 100, 2)
                     for kelas, prob in zip(kelas_model, probabilitas)}

        # Hitung BMI aktual
        bmi = hitung_bmi(berat, tinggi)
        kategori = kategori_bmi(bmi)

        # Generate rekomendasi
        rekomendasi = generate_rekomendasi(prediksi, berat, tinggi, faf, favc, ch2o)

        # Susun response
        hasil = {
            'prediksi': prediksi,
            'probabilitas': prob_dict,
            'bmi': bmi,
            'kategori_bmi': kategori,
            'rekomendasi': rekomendasi,
            'input_user': {
                'tinggi': tinggi,
                'berat': berat,
                'umur': int(umur),
                'gender': 'Laki-laki' if gender == 1 else 'Perempuan'
            }
        }

        return jsonify(hasil)

    except ValueError as e:
        return jsonify({'error': f'Format input tidak valid: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Terjadi kesalahan: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7860)
