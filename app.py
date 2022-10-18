from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'showering-app'
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/statistics')
def statistics():
    return render_template('statistics.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api/data', methods=['POST'])
def data():
    # Fetch data from the request
    request_data = request.get_json()
    temperature = request_data['temperature']
    duration = request_data['time']
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Data cleaning
    exec(open('Data.py').read())

    # Insert data into the database
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO raw_data (temperature, duration, date) VALUES (%s, %s, %s)", (temperature, duration, date))
    mysql.connection.commit()
    cursor.close()
    
    # Return response
    return '''
Successfully received data.
Average temperature of session is: {}C
The session took {} minutes
The date of the session is: {}'''.format(temperature, duration, date)
