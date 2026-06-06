# DataScience-KOMDIGI

Proyek ini dibuat dari awal untuk mendemonstrasikan alur Data Science lengkap pada dataset Iris menggunakan google colab dan gemini ai.
Langkah-langkah yang didukung:
- Analisis awal dataset
- Validasi missing value, outlier, dan data tidak valid
- Pembersihan data dan imputasi
- Transformasi numerik dan rekayasa fitur
- Pelabelan data dan distribusi label
- Dokumentasi dan visualisasi

## Struktur proyek

- `data/` - folder dataset input dan output
- `src/` - modul python untuk membangun pipeline data
- `reports/` - dokumentasi dan output analisis
- `reports/figures/` - grafik hasil visualisasi

## Instalasi

1. Buka folder `DataScience-KOMDIGI`
2. Aktifkan environment Python:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
3. Pasang dependensi:
   ```powershell
   pip install -r requirements.txt
   ```

## Menjalankan analisis

```powershell
python src\run_analysis.py
```

Skrip akan membuat dataset Iris lokal di `data/iris_data.csv` bila belum ada.

## Hasil

Setelah dijalankan, folder `reports/` akan berisi:
- `analysis_report.md` : ringkasan analisis dan pembersihan data
- `label_distribution.csv` : distribusi label hasil pelabelan
- `figures/` : grafik histogram, boxplot, dan scatter plot
- `data/iris_data_cleaned.csv` : dataset hasil pembersihan
- `data/iris_data_transformed.csv` : dataset hasil transformasi dan encoding

## Catatan

Dokumen `reports/data_transformation_documentation.md` dan `reports/labeling_report.md` berisi teknik transformasi dan pelabelan yang digunakan.
