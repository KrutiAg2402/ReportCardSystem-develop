import mysql.connector as sqltor
from mysql.connector import Error

def get_connection():
    return sqltor.connect(
        host ='127.0.0.1',
        user='root',
        password='admin123',
        database='Naman_project'
    )
   
