import mysql.connector


def connect_to_mysql():
    """
    Connect to the MySQL database and return the connection object.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",  # Use "localhost" or the hostname of your server
            user="root",       # Replace with your MySQL username
            password="2023",   # Replace with your MySQL password
            database="bizdoc_db",  # Replace with your database name
            port=3307          # Use the port your MySQL server is running on
        )
        print("Connected to MySQL database")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
