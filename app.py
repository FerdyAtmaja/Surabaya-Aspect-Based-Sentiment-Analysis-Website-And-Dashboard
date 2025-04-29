# Standard library imports
import io
import json
import re
from datetime import datetime

# Third-party imports
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file, session, Response
import joblib
import plotly
import plotly.express as px
import mysql.connector
from wordcloud import WordCloud
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

# Local imports
from config.database import connection, get_connection
from models.LDATransformer import LDATransformer
from models.TextPreprocessor import TextPreprocessor

app = Flask(__name__, static_folder='static', static_url_path='/static')

# Function to ensure connection is active
def ensure_connection():
    global connection
    try:
        if connection is None or not connection.is_connected():
            connection = get_connection()
    except:
        connection = get_connection()


# Load the pipeline models
topic_model = joblib.load('models/pipeline_topic.pkl')
sentiment_model = joblib.load('models/pipeline_sentiment.pkl')

# Definisikan judul untuk setiap topik
judul_topik = {
    1: "Kualitas Pelayanan Masyarakat",
    2: "Pengaduan dan Penyelesaian Keluhan",
    3: "Masalah Lingkungan di Masyarakat",
    4: "Proses Administrasi dan Informasi Publik",
    5: "Pelaporan dan Tindak Lanjut Masalah",
    6: "Kerusakan Fasilitas dan Infrastruktur",
    7: "Pendidikan dan Sekolah",
    8: "Keluhan Kebutuhan Lapangan Pekerjaan",
    9: "Permohonan Perbaikan Dan Pembaharuan",
    10: "Lamanya Proses Pengajuan ",
    11: "Permintaan Dan Pendaftaran Administrasi",
    12: "Durasi dan Efisiensi Layanan",
    13: "Permasalahan Parkir",
    14: "Masalah Pohon dan Gangguan Lingkungan",
    15: "Pemimpin Wilayah yang Bermasalah",
    16: "Kondisi Fisik Lingkungan",
    17: "Permintaan Dan Pendaftaran"
}

instansi_mapping = {
    1: "Dinas Penanaman Modal dan Pelayanan Terpadu Satu Pintu, Dinas Komunikasi dan Informatika",
    2: "Dinas Komunikasi dan Informatika",
    3: "Pemerintah Kota Surabaya",
    4: "Dinas Komunikasi dan Informatika",
    5: "Dinas Sosial, Dinas Perhubungan, Pemerintah Kota Surabaya",
    6: "Pemerintah Kota Surabaya, Dinas Perumahan Rakyat dan Kawasan Permukiman serta Pertanahan, Dinas Sumber Daya Air dan Bina Marga",
    7: "Dinas Pendidikan",
    8: "Dinas Perindustrian dan Tenaga Kerja",
    9: "Dinas Perumahan Rakyat dan Kawasan Permukiman serta Pertanahan",
    10: "Dinas Penanaman Modal dan Pelayanan Terpadu Satu Pintu",
    11: "Dinas Kependudukan dan Pencatatan Sipil",
    12: "Dinas Penanaman Modal dan Pelayanan Terpadu Satu Pintu",
    13: "Dinas Perhubungan",
    14: "Dinas Lingkungan Hidup",
    15: "Pemerintah Kota Surabaya",
    16: "Dinas Lingkungan Hidup",
    17: "Dinas Komunikasi dan Informatika"
}

    

@app.route('/')
def home():
    return render_template('index.html', active_page='home', content='home/home.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    ensure_connection()
    cursor = connection.cursor(dictionary=True)

    # Query untuk mendapatkan daftar tahun unik
    cursor.execute("SELECT DISTINCT YEAR(tanggal_keluhan) AS year FROM sentiment_analysis ORDER BY year")
    years = cursor.fetchall()

    # Default nilai tahun
    year_value = request.form.get('year') or 2023

    query = """
        SELECT
            sa.sentimen,
            sa.tanggal_keluhan,
            a.aspect
        FROM
            sentiment_analysis sa
        JOIN
            aspect a
        ON
            sa.aspect_id = a.aspect_id
        WHERE
            YEAR(sa.tanggal_keluhan) = %s;
    """
    df = pd.read_sql(query, connection, params=(year_value,))

    # Hitung KPI Index
    total_keluhan = len(df)
    keluhan_netral = len(df[df['sentimen'] == 'netral'])
    keluhan_negatif = len(df[df['sentimen'] == 'negatif'])

    # Chart Data
    bubble_chart = create_bubble_chart(df)
    stacked_chart = create_stacked_bar_chart(df)
    line_chart = create_line_chart(df)
    summary_table = create_summary_table(df)
    pie_chart, persentase_negatif, persentase_netral = create_pie_chart(df)

    # Buat explanationText berdasarkan persentase
    explanationText = ""
    percentage = ""
    if persentase_negatif > persentase_netral:
        explanationText = "Negatif"
        percentage = f"{persentase_negatif:.2f}%"
    else:
        explanationText = "Netral"
        percentage = f"{persentase_netral:.2f}%"
        
    return render_template(
        'index.html',
        active_page='dashboard',
        content='dashboard/dashboard.html',
        bubble_chart=json.dumps(bubble_chart, cls=plotly.utils.PlotlyJSONEncoder),
        stacked_chart=json.dumps(stacked_chart, cls=plotly.utils.PlotlyJSONEncoder),
        line_chart=json.dumps(line_chart, cls=plotly.utils.PlotlyJSONEncoder),
        summary_table=summary_table,
        pie_chart=json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder),
        explanationText=explanationText,
        percentage=percentage,
        years=years,  # Daftar tahun
        selected_year=int(year_value),  # Tahun terpilih
        total_keluhan=total_keluhan,
        keluhan_netral=keluhan_netral,
        keluhan_negatif=keluhan_negatif
    )

    
def create_summary_table(df):
    sentiment_map = {'negatif': -1, 'netral': 0}
    summary = df[df['sentimen'].isin(sentiment_map.keys())].groupby('aspect').agg(
        total=('sentimen', 'size'),
        negatif=('sentimen', lambda x: (x == 'negatif').sum()),
        netral=('sentimen', lambda x: (x == 'netral').sum())
    ).reset_index()
    
    summary['persentase_negatif'] = (summary['negatif'] / summary['total'] * 100).round(2)
    summary['persentase_netral'] = (summary['netral'] / summary['total'] * 100).round(2)

    table_html = ''.join(
        f"""
        <tr>
            <td>{row['aspect']}</td>
            <td>{row['total']}</td>
            <td>{row['negatif']}</td>
            <td>{row['netral']}</td>
            <td>{row['persentase_negatif']}%</td>
            <td>{row['persentase_netral']}%</td>
        </tr>
        """
        for _, row in summary.iterrows()
    )
    return table_html


def create_pie_chart(df):
    sentiment_counts = df[df['sentimen'].isin(['negatif', 'netral'])]['sentimen'].value_counts()
    
    # Pastikan hanya menampilkan data jika ada
    if sentiment_counts.empty:
        sentiment_counts = pd.Series([0, 0], index=['negatif', 'netral'])  # Menangani kasus tidak ada data

    # Hitung persentase
    total = sentiment_counts.sum()
    persentase_negatif = (sentiment_counts.get('negatif', 0) / total * 100) if total > 0 else 0
    persentase_netral = (sentiment_counts.get('netral', 0) / total * 100) if total > 0 else 0

    fig = px.pie(
        names=sentiment_counts.index,
        values=sentiment_counts.values,
        title="Proporsi Sentimen Negatif dan Netral",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    return fig, persentase_negatif, persentase_netral

def create_bubble_chart(df):
    bubble_data = df.groupby('aspect').agg(
        sentiment_score=('sentimen', lambda x: np.mean([{'negatif': -1, 'netral': 0}.get(i, 0) for i in x])),
        count=('aspect', 'size')
    ).reset_index()
    
    fig = px.scatter(
        bubble_data, 
        x='sentiment_score', 
        y='count', 
        size='count', 
        color='aspect', 
        title='Rata-rata Sentimen vs Jumlah Keluhan per Aspek',
        labels={'sentiment_score': 'Rata-rata Sentimen', 'count': 'Jumlah Keluhan'},
        color_discrete_sequence=px.colors.qualitative.Plotly,  # Warna yang lebih menarik
        hover_name='aspect',  # Menampilkan nama aspek saat hover
        template='plotly_white'  # Menggunakan template yang lebih bersih
    )
    
    return fig

def create_stacked_bar_chart(df):
    sentiment_counts = df[df['sentimen'].isin(['netral', 'negatif'])].groupby(['aspect', 'sentimen']).size().unstack(fill_value=0)
    sentiment_counts['total'] = sentiment_counts.sum(axis=1)
    sentiment_counts = sentiment_counts.sort_values('total', ascending=False)
    sentiment_counts = sentiment_counts.drop(columns='total')

    fig = px.bar(
        sentiment_counts, 
        orientation='h', 
        title='Distribusi Sentimen Negatif dan Netral per Aspek',
        barmode='stack',
        labels={'sentimen': 'Sentimen','value': 'Jumlah Keluhan', 'aspect': 'Aspek'}

    )
    
    return fig

def create_line_chart(df):
    df['month'] = pd.to_datetime(df['tanggal_keluhan']).dt.to_period('M').astype(str)
    trend_data = df.groupby(['month', 'aspect']).size().unstack(fill_value=0)
    
    fig = px.line(
        trend_data, 
        title='Tren Keluhan Bulanan per Aspek',
        labels={'value': 'Jumlah Keluhan', 'month': 'Bulan'},
        markers=True,  # Menambahkan marker di titik data
        template='plotly_white'  # Menggunakan template yang lebih bersih
    )
    
    return fig

    
@app.route('/wordcloud', methods=['GET', 'POST'])
def wordcloud():
    ensure_connection()
    cursor = connection.cursor(dictionary=True)

    # Ambil data aspek
    cursor.execute("SELECT aspect_id, aspect FROM aspect")
    aspects = [{'aspect_id': 'all', 'aspect': 'Semua Aspek'}] + cursor.fetchall()

    # Ambil daftar tahun
    cursor.execute("SELECT DISTINCT YEAR(tanggal_keluhan) AS year FROM sentiment_analysis ORDER BY year")
    years = cursor.fetchall()

    wordcloud_paths = {'netral': None, 'negatif': None, 'keseluruhan': None}
    message = None

    if request.method == 'POST':
        aspect_id = request.form.get('aspect_id')
        selected_year = request.form.get('year')

        sentiments = {
            'netral': "netral",
            'negatif': "negatif",
            'keseluruhan': None  # Semua data
        }

        has_data = False
        for sentiment, label in sentiments.items():
            # Query untuk data
            query = f"""
                SELECT preprocessed_text 
                FROM sentiment_analysis
                WHERE YEAR(tanggal_keluhan) = %s
                  AND (aspect_id = %s OR %s = 'all')
                  {f"AND sentimen = %s" if label else ""}
            """
            params = [selected_year, aspect_id, aspect_id]
            if label:
                params.append(label)

            cursor.execute(query, params)
            results = cursor.fetchall()

            # Proses data jika ada hasil
            text_data = []
            for row in results:
                if row['preprocessed_text']:
                    try:
                        preprocessed_text = json.loads(row['preprocessed_text'])
                        text_data.extend(preprocessed_text)
                    except json.JSONDecodeError:
                        continue  # Skip if there's a JSON decode error

            if text_data:
                has_data = True
                wc = WordCloud(width=800, height=400, background_color='white').generate(' '.join(text_data))
                wordcloud_path = f'static/assets/images/wordcloud/wordcloud_{selected_year}_{aspect_id}_{sentiment}.png'
                wc.to_file(wordcloud_path)
                wordcloud_paths[sentiment] = wordcloud_path

        # Jika tidak ada data
        if not has_data:
            message = "Data Tidak Ditemukan. Tidak ada data untuk kombinasi tahun dan aspek yang dipilih."

    return render_template(
        'index.html',
        active_page='wordcloud',
        content='wordcloud/wordcloud.html',
        aspects=aspects,
        years=years,
        wordcloud_paths=wordcloud_paths,
        message=message
    )

@app.route('/analyze')
def analyze():
    return render_template('index.html', active_page='analyze', content='analyze/analyze.html')

# Analyze related routes
@app.route('/process_text', methods=['POST'])
def process_text():
    if request.method == 'POST':
        text = request.form['textInput']
        
        # Perform sentiment analysis
        sentiment_prediction = sentiment_model.predict([text])[0]

        # Map 'Positive' and 'Negative'
        sentiment_map = {'netral': 'Netral', 'negatif': 'Negative'}
        sentimen = sentiment_map.get(sentiment_prediction, 'Unknown')

        # Perform topic modeling
        topic_prediction = topic_model.transform([text])[0]
        
        doc_vector = topic_prediction  # Use the transformed vector directly
        top_topic = doc_vector.argmax()

        if top_topic in judul_topik:
            topic = judul_topik[top_topic + 1]  # Simpan judul sesuai topik dominan
            
        if top_topic in instansi_mapping:
            instansi = instansi_mapping[top_topic + 1]
    
        return render_template('index.html', 
                               content='analyze/resultTextAnalyzing.html',
                               active_page='analyze',
                               sentiment=sentimen,
                               topic=topic,
                               instansi=instansi,
                               input_text=text)

@app.context_processor
def utility_processor():
    return dict(enumerate=enumerate)

# Variabel Global untuk Menyimpan Hasil Proses
processed_results = []

@app.route('/process_file', methods=['POST'])
def process_file():
    global processed_results
    processed_results = []  # Reset data sebelumnya

    if 'fileUpload' not in request.files:
        return "No file part", 400

    file = request.files['fileUpload']
    if file.filename == '':
        return "No selected file", 400

    if file:
        # Load file ke DataFrame
        df = pd.read_excel(file) if file.filename.endswith('.xlsx') else pd.read_csv(file)

        # Preprocess dan Analisis Data
        for _, row in df.iterrows():
            keluhan = row['keluhan']
            tanggal = pd.to_datetime(row['tanggal_keluhan']).strftime('%Y-%m-%d %H:%M:%S') # string ke datetime

            # Preprocessing Keluhan
            preprocessor = topic_model.named_steps['preprocessor']
            preprocessed = preprocessor.transform([keluhan])[0]  # Hasilnya berupa list
            preprocessed_text = json.dumps(preprocessed)  # Konversi list ke string JSON
            
            # Analisis Sentimen
            sentiment_prediction = sentiment_model.predict([keluhan])[0]
            sentimen = {'netral': 'Netral', 'negatif': 'Negatif'}.get(sentiment_prediction, 'Unknown')

            # Analisis Topik
            topic_prediction = topic_model.transform([keluhan])[0]
            top_topic = topic_prediction.argmax()
            topic_label = judul_topik.get(top_topic + 1, 'Topik Tidak Diketahui')
            instansi_label = instansi_mapping.get(top_topic + 1, 'Topik Tidak Diketahui')
            

            processed_results.append({
                'tanggal': tanggal,
                'keluhan': keluhan,
                'preprocessed_text': preprocessed_text,
                'sentimen': sentimen,
                'topik': topic_label,
                'instansi': instansi_label
            })

        # Tampilkan di halaman hasil
        return render_template('index.html', 
                               content='analyze/resultFileAnalyzing.html',
                               active_page='analyze',
                               results=processed_results)

@app.route('/export_excel', methods=['GET'])
def export_excel():
    global processed_results
    if not processed_results:
        return "No data to export", 400

    # Convert processed_results ke DataFrame
    df = pd.DataFrame(processed_results)

    # Save ke Excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Processed Results')

    output.seek(0)
    return Response(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={"Content-Disposition": "attachment;filename=processed_results.xlsx"}
    )

@app.route('/export_pdf', methods=['GET'])
def export_pdf():
    global processed_results
    if not processed_results:
        return "No data to export", 400

    # Menghitung jumlah sentimen negatif dan netral berdasarkan topik
    summary = {}
    total_negatif = 0
    total_netral = 0

    for record in processed_results:
        topik = record['topik']
        sentimen = record['sentimen']

        if topik not in summary:
            summary[topik] = {'Negatif': 0, 'Netral': 0}

        if sentimen in summary[topik]:
            summary[topik][sentimen] += 1

    # Hitung total
    for counts in summary.values():
        total_negatif += counts['Negatif']
        total_netral += counts['Netral']

    # Output stream
    output = io.BytesIO()
    pdf = SimpleDocTemplate(output, pagesize=landscape(A4),
                            leftMargin=1 * cm, rightMargin=1 * cm,
                            topMargin=2.5 * cm, bottomMargin=2 * cm)
    elements = []

    # Styles
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    subtitle_style = styles['Normal']
    subtitle_style.spaceAfter = 12
    subtitle_style.spaceBefore = 12

    # Header
    current_date = datetime.now().strftime("%d %B %Y, %H:%M:%S")
    header_title = Paragraph("Laporan Analisis Sentimen Berbasis Aspek", title_style)
    header_subtitle = Paragraph(f"Kota Surabaya - Tanggal Pembuatan: {current_date}", subtitle_style)
    header_description = Paragraph(
        "Laporan ini menyajikan jumlah sentimen negatif dan netral berdasarkan aspek/topik "
        "pengaduan warga Kota Surabaya.", subtitle_style)
    elements.extend([header_title, header_subtitle, header_description, Spacer(1, 0.5 * cm)])

    # Define column widths
    col_widths = [14 * cm, 4 * cm, 4 * cm]

    # Header dan data tabel
    data = [['Aspek/Topik', 'Jumlah Sentimen Negatif', 'Jumlah Sentimen Netral']]
    for topik, counts in summary.items():
        data.append([
            topik,
            counts['Negatif'],
            counts['Netral']
        ])

    # Tambahkan total
    data.append(['Total', total_negatif, total_netral])

    # Buat tabel
    table = Table(data, colWidths=col_widths)

    # Gaya tabel
    style = TableStyle([
        # Header style
        ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),

        # Data style
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),  # Align jumlah
        ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
        ('TEXTCOLOR', (0, 1), (-1, -2), colors.black),
        ('LINEBELOW', (0, 1), (-1, -2), 0.25, colors.grey),

        # Total row style
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightblue),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('ALIGN', (0, -1), (-1, -1), 'CENTER'),

        # Table borders
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ])
    table.setStyle(style)

    # Tambahkan tabel ke elemen
    elements.append(table)

    # Footer
    footer_note = Paragraph(
        "Laporan ini dihasilkan oleh sistem analisis sentimen berbasis aspek "
        "untuk pengaduan warga Kota Surabaya.", subtitle_style)
    elements.extend([Spacer(1, 1 * cm), footer_note])

    # Bangun PDF
    pdf.build(elements)
    output.seek(0)

    return Response(
        output,
        mimetype='application/pdf',
        headers={"Content-Disposition": "attachment;filename=laporan_ringkasan_sentimen_surabaya.pdf"}
    )

@app.route('/save_to_database', methods=['POST'])
def save_to_database():
    # Username dan password statis
    STATIC_USERNAME = "admin"
    STATIC_PASSWORD = "admin"
    
    # Terima data dari permintaan POST
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Validasi username dan password
    if username != STATIC_USERNAME or password != STATIC_PASSWORD:
        return {"success": False, "message": "Username atau password salah!"}, 401

    # Pastikan koneksi ke database aktif
    ensure_connection()
    cursor = connection.cursor()

    try:
        # Mengambil data hasil analisis dari global processed_results
        global processed_results
        if not processed_results:
            return {"success": False, "message": "Tidak ada data untuk disimpan!"}, 400

        # Normalisasi data di processed_results untuk konsistensi
        for row in processed_results:
            row['tanggal'] = pd.to_datetime(row['tanggal']).strftime('%Y-%m-%d %H:%M:%S')
            row['keluhan'] = row['keluhan'].strip().lower()

        # Ambil seluruh data tanggal_keluhan dan keluhan di database untuk pengecekan
        cursor.execute("SELECT DATE_FORMAT(tanggal_keluhan, '%Y-%m-%d %H:%i:%s'), LOWER(keluhan) FROM sentiment_analysis")
        existing_data = set((row[0], row[1]) for row in cursor.fetchall())

        # Filter data untuk hanya menyimpan baris baru
        rows_to_insert = []
        for row in processed_results:
            # Ambil aspek berdasarkan nama topik
            select_aspect_query = "SELECT aspect_id FROM aspect WHERE aspect = %s"
            cursor.execute(select_aspect_query, (row['topik'],))
            aspect = cursor.fetchone()

            if not aspect:
                return {"success": False, "message": f"Aspek {row['topik']} tidak ditemukan dalam database!"}, 400
            
            aspect_id = aspect[0]
            key = (row['tanggal'], row['keluhan'])

            # Debugging untuk memeriksa duplikasi
            print(f"Checking key: {key}")
            if key not in existing_data:
                print(f"Adding key: {key}")
                rows_to_insert.append((
                    row['sentimen'].lower(),  # sentimen
                    row['tanggal'],          # tanggal_keluhan
                    row['keluhan'],          # keluhan
                    row['preprocessed_text'],  # preprocessed_text
                    aspect_id                # aspect_id
                ))

        # Jika ada data untuk di-insert, lakukan insert batch
        if rows_to_insert:
            insert_query = """
                INSERT INTO sentiment_analysis 
                (sentimen, tanggal_keluhan, keluhan, preprocessed_text, aspect_id)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.executemany(insert_query, rows_to_insert)
            connection.commit()

        cursor.close()
        return {"success": True, "message": f"Data berhasil disimpan ke database! {len(rows_to_insert)} baris ditambahkan."}, 200

    except Exception as e:
        connection.rollback()  # Batalkan transaksi jika terjadi kesalahan
        return {"success": False, "message": f"Gagal menyimpan data: {e}"}, 500

@app.route('/documentation')
def documentation():
    return render_template('index.html', active_page='documentation', content='documentation/documentation.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
    