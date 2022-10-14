import mysql.connector

mydb = mysql.connector.connect(host='localhost', user='root', password='', database='showeringapp')

if mydb.is_connected():
    print("Connected")

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM all_data")
print(type(mycursor.fetchall()))

QUERY_CLEAN = """
    DROP TABLE IF EXISTS cleaned_data;
    CREATE TABLE cleaned_data;
    SELECT * AS data
    FROM all_data
    WHERE data IS NOT NULL;
    """

QUERY_CREATE_TEMPERATURE = """
    DROP TABLE IF EXISTS temperatures;
    CREATE TABLE temperatures;
    SELECT user_id, temperature
    FROM cleaned_data;
"""
QUERY_CREATE_TIME = """
    DROP TABLE IF EXISTS times;
    CREATE TABLE times;
    SELECT user_id, shower_time
    FROM cleaned_data;
"""

mycursor.execute(QUERY_CLEAN)
mydb.close()

mydb = mysql.connector.connect(host='localhost', user='root', password='', database='showeringapp')
mycursor = mydb.cursor()
mycursor.execute(QUERY_CREATE_TEMPERATURE)
mydb.close()

mydb = mysql.connector.connect(host='localhost', user='root', password='', database='showeringapp')
mycursor = mydb.cursor()
mycursor.execute(QUERY_CREATE_TIME)
mydb.close()