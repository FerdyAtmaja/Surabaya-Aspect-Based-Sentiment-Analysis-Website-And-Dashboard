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

4. **Konfigurasi Environment Variables**
Salin file `.env.example` ke `.env` dan sesuaikan dengan pengaturan Anda:
```bash
cp .env.example .env
```

Edit file `.env`:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=db_sentimen
SECRET_KEY=your-very-secret-key-here
FLASK_DEBUG=False
ADMIN_USERNAME=your_admin_username
ADMIN_PASSWORD=your_secure_password
```

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

## Keamanan

### Perbaikan Keamanan yang Telah Diterapkan:
- **Environment Variables**: Credentials database dan konfigurasi sensitif dipindahkan ke environment variables
- **Input Validation**: Validasi input untuk mencegah SQL injection dan XSS
- **Error Handling**: Error handling yang komprehensif untuk mencegah information disclosure
- **CSRF Protection**: Flask secret key untuk session management
- **Authorization**: Perbaikan sistem otorisasi untuk admin functions
- **Debug Mode**: Debug mode dinonaktifkan untuk production

### Best Practices:
1. Selalu gunakan environment variables untuk credentials
2. Jangan commit file `.env` ke repository
3. Gunakan HTTPS di production
4. Update dependencies secara berkala
5. Monitor logs untuk aktivitas mencurigakan

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