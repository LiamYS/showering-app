import mysql.connector
CONFIG = {
    'host':'localhost',
    'user':'root',
    'password':'',
    'database':'showering-app',
    'autocommit':True
}

mydb = mysql.connector.connect(**CONFIG)
mycursor = mydb.cursor()

QUERY_UPDATE = """
    DROP TABLE IF EXISTS cleaned_data;
"""

mycursor.execute(QUERY_UPDATE)
mycursor.close()

mydb = mysql.connector.connect(**CONFIG)
mycursor = mydb.cursor()

QUERY_COPY = """
    CREATE TABLE IF NOT EXISTS cleaned_data AS
        SELECT session_id, temperature, duration, date
        FROM raw_data;
    """

mycursor.execute(QUERY_COPY)
mycursor.close()

mydb = mysql.connector.connect(**CONFIG)
mycursor = mydb.cursor()

QUERY_REMOVE_EMPTY = """
    DELETE FROM cleaned_data
    WHERE session_id = '' OR temperature = '' OR duration = '' OR date = '';
"""

mycursor.execute(QUERY_REMOVE_EMPTY)
mycursor.close()

mydb = mysql.connector.connect(**CONFIG)
mycursor = mydb.cursor()

QUERY_REMOVE_DUPLICATE = """
    DELETE n1 FROM cleaned_data n1, cleaned_data n2 
    WHERE n1.session_id = n2.session_id AND n1.date > n2.date;
"""

mycursor.execute(QUERY_REMOVE_DUPLICATE)
mycursor.close()

mydb = mysql.connector.connect(**CONFIG)
mycursor = mydb.cursor()

QUERY_REMOVE_WEIRD = """
    DELETE FROM cleaned_data 
    WHERE temperature < 0 OR temperature > 55 OR duration < 1 OR duration > 120;
"""

mycursor.execute(QUERY_REMOVE_WEIRD)
mycursor.close()

