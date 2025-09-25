import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import json
import ast
import os

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

# Konversi kolom preprocessed_text ke format JSON dengan error handling
def safe_json_convert(x):
    try:
        if isinstance(x, str):
            # Use ast.literal_eval instead of eval for security
            evaluated = ast.literal_eval(x)
            return json.dumps(evaluated)
        else:
            return json.dumps(x)
    except (ValueError, SyntaxError, NameError) as e:
        print(f"Warning: Could not convert preprocessed_text: {e}")
        return json.dumps(str(x))  # Fallback to string conversion

df['preprocessed_text'] = df['preprocessed_text'].apply(safe_json_convert)

# Menambahkan kolom created_at dan updated_at
current_time = datetime.now()
df['created_at'] = current_time
df['updated_at'] = current_time

# Membuat koneksi ke database menggunakan environment variables
try:
    db_host = os.getenv('DB_HOST', 'localhost')
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', '')
    db_name = os.getenv('DB_NAME', 'db_sentimen')
    
    connection_string = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}?connect_timeout=60'
    engine = create_engine(connection_string)
    
    batch_size = 1000
    with engine.begin() as connection:
        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i + batch_size]
            batch.to_sql(table_name, con=connection, if_exists='append', index=False)
    print("Data berhasil dimasukkan ke dalam database.")
except Exception as e:
    print(f"Error inserting data into database: {e}")
