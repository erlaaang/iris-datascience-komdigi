# Dokumentasi Transformasi Data

Dokumentasi ini menjelaskan teknik transformasi yang digunakan dalam alur data Iris.

## 1. Normalisasi dan Scaling
- `MinMaxScaler` digunakan untuk menskalakan fitur numerik ke rentang 0-1.
- Kolom `scaled_*` dihasilkan untuk setiap fitur numerik sehingga skala fitur konsisten untuk analisis dan modeling.

## 2. Encoding Kategori
- Fitur `species` diubah menjadi variabel dummy (one-hot encoding).
- Encoding ini membuat label spesies dapat dimasukkan ke dalam model machine learning.

## 3. Rekayasa Fitur
- `sepal_area`: luas sepal dari hasil perkalian panjang dan lebar sepal.
- `petal_area`: luas petal dari hasil perkalian panjang dan lebar petal.
- `area_ratio`: rasio petal_area terhadap sepal_area untuk menangkap perbedaan bentuk bunga.

## 4. Imputasi Missing Value
- Nilai numerik yang hilang diisi dengan median kolom.
- Nilai kategorikal yang hilang diisi dengan modus kolom.
- Baris dengan lebih dari dua nilai hilang dihapus.

## 5. Validasi Data
- Nilai numerik diklipping ke kisaran realistis untuk fitur Iris.
- Duplikasi dibuang.

## Rekomendasi
- Sangat disarankan menyimpan `data/iris_data_cleaned.csv` sebagai sumber data bersih.
- `data/iris_data_transformed.csv` adalah dataset yang siap dipakai untuk analisis lebih lanjut atau model.
- Gunakan `reports/label_distribution.csv` untuk memeriksa keseimbangan kategori hasil pelabelan.
