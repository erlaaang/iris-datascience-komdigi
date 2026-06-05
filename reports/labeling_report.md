# Laporan Hasil Pelabelan Data

Dokumen ini menjelaskan pendekatan pelabelan data Iris dan distribusi label akhir.

## Strategi Pelabelan
- `petal_size_category` dibuat berdasarkan quantile `petal_area`.
- Kategori yang dihasilkan: `small`, `medium`, dan `large`.
- Label ini membantu membagi data berdasarkan ukuran bunga.

## Kategori Bentuk
- `shape_label` dibuat berdasarkan perbandingan `petal_area` dan `sepal_area`.
- `petal_dominant` ketika area petal lebih besar dari area sepal.
- `sepal_dominant` ketika area sepal lebih besar atau sama dengan area petal.

## Evaluasi Pelabelan
- Lakukan validasi distribusi label dengan `reports/label_distribution.csv`.
- Periksa apakah jumlah sampel di setiap kategori ukuran petal cukup seimbang.
- Pantau apakah label `large` tidak terlalu sedikit dibandingkan kategori lainnya.

## Tantangan dan Perbaikan
- Jika label asli telah ada, pastikan kriteria pelabelan baru selaras dengan SOP data.
- Untuk dataset yang tidak seimbang, pertimbangkan penyeimbangan data atau teknik klasifikasi berbobot.
- Komunikasikan definisi label `small`, `medium`, `large`, dan `petal_dominant` ke pemangku kepentingan.
