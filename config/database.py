import mysql.connector

# Database configuration
config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'db_sentimen'
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

# Create a connection instance
connection = get_connection()