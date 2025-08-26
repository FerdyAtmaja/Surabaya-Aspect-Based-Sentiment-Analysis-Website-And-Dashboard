# Sistem Analisis Sentimen Berbasis Aspek

Aplikasi web untuk menganalisis sentimen pengaduan warga Kota Surabaya berdasarkan aspek/topik menggunakan machine learning.

## Fitur Utama

- **Analisis Sentimen**: Klasifikasi otomatis sentimen (negatif/netral) dari teks keluhan
- **Pemodelan Topik**: Identifikasi aspek/topik keluhan menggunakan LDA (Latent Dirichlet Allocation)
- **Dashboard Interaktif**: Visualisasi data dengan grafik bubble, stacked bar, line chart, dan pie chart
- **Word Cloud**: Visualisasi kata-kata dominan berdasarkan sentimen dan aspek
- **Analisis File**: Upload dan analisis file Excel/CSV secara batch
- **Export Data**: Export hasil analisis ke format Excel dan PDF
- **Penyimpanan Database**: Simpan hasil analisis ke database MySQL

## Teknologi

- **Backend**: Flask (Python)
- **Database**: MySQL
- **Machine Learning**: scikit-learn, joblib
- **Visualisasi**: Plotly, WordCloud
- **Frontend**: HTML, CSS, JavaScript
- **Export**: pandas, ReportLab

## Instalasi

1. **Clone repository**
```bash
git clone <repository-url>
cd AS
```

2. **Install dependencies**
```bash
pip install flask pandas numpy scikit-learn joblib plotly mysql-connector-python wordcloud reportlab xlsxwriter
```

3. **Setup database**
```bash
mysql -u root -p < db_sentimen.sql
mysql -u root -p < sentiment_data.sql
mysql -u root -p < insert_aspect.sql
```

4. **Konfigurasi database**
Edit file `config/database.py` sesuai pengaturan MySQL Anda.

## Penggunaan

1. **Jalankan aplikasi**
```bash
python app.py
```

2. **Akses aplikasi**
Buka browser dan kunjungi `http://localhost:5000`

3. **Fitur yang tersedia**:
   - **Dashboard**: Lihat statistik dan visualisasi data keluhan
   - **Word Cloud**: Generate word cloud berdasarkan aspek dan sentimen
   - **Analyze**: Analisis teks individual atau file batch
   - **Documentation**: Panduan penggunaan aplikasi

## Struktur Project

```
AS/
├── config/
│   ├── __init__.py
│   └── database.py          # Konfigurasi database
├── models/
│   ├── LDATransformer.py    # Model LDA untuk topic modeling
│   ├── TextPreprocessor.py  # Preprocessing teks
│   ├── pipeline_sentiment.pkl # Model sentimen terlatih
│   └── pipeline_topic.pkl   # Model topik terlatih
├── static/assets/           # File statis (CSS, JS, images)
├── templates/               # Template HTML
├── uploads/                 # Folder upload file
├── app.py                   # Aplikasi utama Flask
└── README.md               # Dokumentasi ini
```

## Model Machine Learning

### Preprocessing
- Normalisasi teks
- Tokenisasi
- Stopword removal
- Stemming

### Klasifikasi Sentimen
- Model: Pipeline dengan preprocessing + classifier
- Output: negatif, netral

### Topic Modeling
- Algoritma: Latent Dirichlet Allocation (LDA)
- 17 topik aspek keluhan yang telah didefinisikan
- Mapping ke instansi terkait

## API Endpoints

- `GET /` - Halaman utama
- `GET /dashboard` - Dashboard visualisasi
- `POST /dashboard` - Filter dashboard berdasarkan tahun
- `GET /wordcloud` - Halaman word cloud
- `POST /wordcloud` - Generate word cloud
- `GET /analyze` - Halaman analisis
- `POST /process_text` - Analisis teks individual
- `POST /process_file` - Analisis file batch
- `GET /export_excel` - Export hasil ke Excel
- `GET /export_pdf` - Export laporan ke PDF
- `POST /save_to_database` - Simpan hasil ke database

## Kontribusi

1. Fork repository
2. Buat branch fitur (`git checkout -b feature/nama-fitur`)
3. Commit perubahan (`git commit -am 'Tambah fitur baru'`)
4. Push ke branch (`git push origin feature/nama-fitur`)
5. Buat Pull Request

## Lisensi

Proyek ini dibuat untuk keperluan skripsi/penelitian.

## Kontak

Untuk pertanyaan atau dukungan, silakan hubungi pengembang.