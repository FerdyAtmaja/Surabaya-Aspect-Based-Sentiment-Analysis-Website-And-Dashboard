import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import json

# Path file Excel dan pengaturan database
excel_file = 'static/assets/insert_to_db_17.xlsx'  # Path file Excel
database_file = 'db_sentimen'
table_name = 'sentiment_analysis'  # Nama tabel di database

# Membaca file Excel
try:
    df = pd.read_excel(excel_file)
except Exception as e:
    print(f"Error reading Excel file: {e}")
    exit(1)

# Konversi kolom preprocessed_text ke format JSON
df['preprocessed_text'] = df['preprocessed_text'].apply(lambda x: json.dumps(eval(x)) if isinstance(x, str) else json.dumps(x))

# Menambahkan kolom created_at dan updated_at
current_time = datetime.now()
df['created_at'] = current_time
df['updated_at'] = current_time

# Membuat koneksi ke database
try:
    engine = create_engine('mysql+mysqlconnector://root:@localhost/db_sentimen?connect_timeout=60')
    batch_size = 1000
    with engine.begin() as connection:
        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i + batch_size]
            batch.to_sql(table_name, con=connection, if_exists='append', index=False)
    print("Data berhasil dimasukkan ke dalam database.")
except Exception as e:
    print(f"Error inserting data into database: {e}")
