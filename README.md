# 🧑‍🎓 Identitas Mahasiswa
**Nama:** Ahmad Rizal Dwi Nugraha
**NIM:** 23.11.5396

# ObesityScan

**Sistem Prediksi Status Obesitas dan Rekomendasi Manajemen Berat Badan Menggunakan Algoritma Random Forest**

Proyek ini merupakan implementasi dari penelitian UTS Mata Kuliah Proyek Data Mining yang bertujuan menjadi sistem pendukung pencegahan dini Penyakit Tidak Menular berbasis machine learning.

**Live Demo**
Untuk mencoba live demo silakan klik link dibawah
[KLIK DISINI](https://huggingface.co/spaces/ijalkeren/obesityscan)

**Notebook**
eksplorasi data, dan pelatihan model dapat dilihat pada link berikut:
[CLICK HERE]([https://github.com](https://colab.research.google.com/drive/1objdXQ1H-Zs4ngNihLWMlR52sd0Q9JO-?usp=sharing)).




---

## 📋 Tentang Proyek

ObesityScan adalah aplikasi web yang mengklasifikasikan status obesitas seseorang ke dalam tiga kategori yaitu **Kurus, Normal, dan Obesitas**, sekaligus memberikan rekomendasi manajemen berat badan yang dipersonalisasi berdasarkan profil gaya hidup pengguna.

Sistem ini dibangun berlandaskan pada data World Health Organization yang mencatat bahwa pada tahun 2022 sebanyak 2,5 miliar orang dewasa mengalami kelebihan berat badan, dengan 890 juta di antaranya tergolong obesitas. Di Indonesia, prevalensi obesitas dewasa meningkat dari 14,8 persen di tahun 2013 menjadi 21,8 persen di tahun 2018 menurut Riskesdas Kementerian Kesehatan RI.

---

## 🎯 Fitur Utama

- **Klasifikasi 3 kelas** berdasarkan input antropometri dan gaya hidup
- **Perhitungan BMI otomatis** dengan kategorisasi standar WHO
- **Distribusi probabilitas** untuk setiap kelas prediksi
- **Rekomendasi rentang berat ideal** berdasarkan tinggi badan pengguna
- **Saran gaya hidup personal** yang disesuaikan dengan input pengguna
- **Antarmuka clinical-modern** yang profesional dan mudah digunakan

---


### Dataset
Penelitian menggunakan dataset publik **ObesityDataSet** yang dipublikasikan Palechor dan Manotas (2019) pada jurnal Data in Brief dengan DOI 10.1016/j.dib.2019.104344. Dataset berisi 2.111 sampel individu dari Meksiko, Peru, dan Kolombia.

### Algoritma
Algoritma utama yang digunakan adalah **Random Forest Classifier** yang dipilih berdasarkan studi Grinsztajn, Oyallon, dan Varoquaux (2022) yang menunjukkan bahwa model berbasis tree konsisten unggul pada data tabular. Sebagai validasi metodologis, performa dibandingkan dengan Decision Tree dan K-Nearest Neighbor.
## 💻 Menjalankan Project Secara Lokal

Bagi yang ingin mencoba menjalankan project ini di laptop sendiri, berikut langkah-langkahnya.

### Prasyarat
- Python 3.9 atau lebih baru
- pip package manager
- Git (opsional, untuk clone repository)

### Langkah Instalasi

**1. Clone atau download repository ini**

\`\`\`bash
git clone https://huggingface.co/spaces/USERNAME/obesityscan
cd obesityscan
\`\`\`

Atau download manual dengan klik tab Files lalu download semua file.

**2. Buat virtual environment**

\`\`\`bash
python -m venv venv
source venv/bin/activate
\`\`\`

Untuk Windows gunakan `venv\Scripts\activate`

**3. Install dependensi**

\`\`\`bash
pip install -r requirements.txt
\`\`\`

**4. Jalankan aplikasi**

\`\`\`bash
python app.py
\`\`\`

**5. Akses di browser**

Buka `http://127.0.0.1:7860`
