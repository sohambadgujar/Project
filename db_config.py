import pymysql

# Database configuration dictionary.
# IMPORTANT: Update these credentials if your local MySQL setup requires a password or different user.
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Add your MySQL root password here if you have one
    'database': 'smart_photo_studio',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_connection():
    """
    Returns a connection to the MySQL database.
    Make sure to close the connection after use.
    """
    try:
        connection = pymysql.connect(**DB_CONFIG)
        return connection
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL Database: {e}")
        return None
