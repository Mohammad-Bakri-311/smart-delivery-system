# import mysql connector to connect Python with MySQL database
import mysql.connector

# this function creates connection with smart_delivery database
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="smart_delivery"
    )