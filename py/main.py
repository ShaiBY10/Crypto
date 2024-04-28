import mysql.connector
from mysql.connector import Error
from config import *
def connect_db():
    """Create a database connection using credentials from an environment or config file."""
    try:
        connection = mysql.connector.connect(
            host=HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            port=PORT
        )
        if connection.is_connected():
            db_info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None


