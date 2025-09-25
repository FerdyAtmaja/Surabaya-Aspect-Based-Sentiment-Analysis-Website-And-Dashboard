import mysql.connector
import os

# Database configuration using environment variables
config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'db_sentimen')
}

def get_connection():
    try:
        # Establish connection
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print('Connected to MySQL database')
            return connection
    except mysql.connector.Error as error:
        print(f'Failed to connect to MySQL database: {error}')
        return None