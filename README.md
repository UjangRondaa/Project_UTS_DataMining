---
title: ObesityScan
emoji: 🏥
colorFrom: green
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
license: mit
short_description: Sistem prediksi status obesitas dengan Random Forest
---

# ObesityScan - Sistem Prediksi Status Obesitas

Aplikasi web berbasis Flask dan Random Forest untuk klasifikasi status obesitas dan rekomendasi manajemen berat badan, sebagai bagian dari UTS Proyek Data Mining.

## Tentang Sistem

Sistem ini memprediksi status obesitas berdasarkan tujuh indikator antropometri dan gaya hidup yaitu tinggi badan, berat badan, usia, jenis kelamin, frekuensi aktivitas fisik (FAF), konsumsi makanan tinggi kalori (FAVC), dan konsumsi air harian (CH2O).

## Metodologi

- **Algoritma utama** : Random Forest Classifier
- **Akurasi model** : 96.93 persen pada 423 sampel data uji
- **Dataset** : ObesityDataSet oleh Palechor dan Manotas (2019), dataset publik 2.111 sampel
- **Komparasi baseline** : Decision Tree dan K-Nearest Neighbor

## Fitur Aplikasi

- Klasifikasi tiga kelas yaitu Kurus, Normal, dan Obesitas
- Distribusi probabilitas tiap kelas
- Perhitungan BMI dengan kategorisasi WHO
- Rekomendasi rentang berat ideal personal
- Saran gaya hidup yang dipersonalisasi berdasarkan input

## Stack Teknologi

- **Backend** : Flask 3.0.3 dengan Gunicorn
- **Machine Learning** : scikit-learn 1.5.1
- **Frontend** : HTML, CSS murni dengan desain clinical-modern
- **Deployment** : Docker pada HuggingFace Spaces

## Referensi

Palechor, F. M., dan Manotas, A. D. L. H. (2019). Dataset for estimation of obesity levels based on eating habits and physical condition in individuals from Colombia, Peru and Mexico. Data in Brief, 25, 104344. DOI 10.1016/j.dib.2019.104344
