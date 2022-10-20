from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from datetime import datetime
import helpers

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'showering-app'
mysql = MySQL(app)

@app.route('/')
def index():
    # Query the database
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT ROUND(AVG(temperature), 1), ROUND(AVG(duration), 1) FROM raw_data")
    data = cursor.fetchall()
    mysql.connection.commit()
    cursor.execute("SELECT ROUND(AVG(temperature), 1), SUM(duration) FROM raw_data WHERE date BETWEEN '{}' AND '{}'".format(helpers.get_date_range('days'), helpers.get_date_tomorrow()))
    daily_data = cursor.fetchall()
    mysql.connection.commit()
    cursor.execute("SELECT temperature, duration, date FROM raw_data WHERE date BETWEEN '{}' AND '{}' ORDER BY date ASC".format(helpers.get_date_range('weeks'), helpers.get_date_tomorrow()))
    graph_data = cursor.fetchall()
    mysql.connection.commit()
    cursor.close()
    # Generate comparison string for template
    if 9.1 - float(data[0][1]) > 0:
        comparison_string = "Your current shower time is {} min, which is {} min lower than the world average.".format(data[0][1], round(9.1 - float(data[0][1]), 2))
    else:
        comparison_string = "Your current shower time is {} min, which is {} min higher than the world average.".format(data[0][1], round(float(data[0][1]) - 9.1, 2))
    # Render the template
    return render_template('index.html', comparison_string=comparison_string, data=data, daily_data=daily_data, graph_data=graph_data, strftime=datetime.strftime)

@app.route('/statistics/', defaults={'timeframe': 'days', 'period': helpers.get_date_range('days')})
@app.route('/statistics/timeframe/<string:timeframe>/period/<period>')
def statistics(timeframe, period):
    # Query the database on specific timeframes
    if timeframe == 'days':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT temperature, duration, date FROM raw_data WHERE date BETWEEN '{}' AND '{}' ORDER BY date ASC".format(helpers.get_date_range('days'), helpers.get_date_tomorrow()))
        data = cursor.fetchall()
        mysql.connection.commit()
        cursor.execute("SELECT ROUND(AVG(temperature), 1), ROUND(AVG(duration), 1) FROM raw_data WHERE date BETWEEN '{}' AND '{}'".format(helpers.get_date_range('days'), helpers.get_date_tomorrow()))
        average = cursor.fetchall()
        mysql.connection.commit()
        cursor.close()
    elif timeframe == 'weeks':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT AVG(temperature), AVG(duration), date FROM raw_data WHERE date BETWEEN '{}' AND '{}' GROUP BY day(date) ORDER BY date ASC".format(helpers.get_date_range('weeks'), helpers.get_date_tomorrow()))
        data = cursor.fetchall()
        mysql.connection.commit()
        cursor.execute("SELECT ROUND(AVG(temperature), 1), ROUND(AVG(duration), 1) FROM raw_data WHERE date BETWEEN '{}' AND '{}'".format(helpers.get_date_range('weeks'), helpers.get_date_tomorrow()))
        average = cursor.fetchall()
        mysql.connection.commit()
        cursor.close()
    elif timeframe == 'months':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT AVG(temperature), AVG(duration), date FROM raw_data WHERE date BETWEEN '{}' AND '{}' GROUP BY day(date) ORDER BY date ASC".format(helpers.get_date_range('months'), helpers.get_date_tomorrow()))
        data = cursor.fetchall()
        mysql.connection.commit()
        cursor.execute("SELECT ROUND(AVG(temperature), 1), ROUND(AVG(duration), 1) FROM raw_data WHERE date BETWEEN '{}' AND '{}'".format(helpers.get_date_range('months'), helpers.get_date_tomorrow()))
        average = cursor.fetchall()
        mysql.connection.commit()
        cursor.close()
    elif timeframe == 'years':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT AVG(temperature), AVG(duration), date FROM raw_data WHERE date BETWEEN '{}' AND '{}' GROUP BY day(date) ORDER BY date ASC".format(helpers.get_date_range('years'), helpers.get_date_tomorrow()))
        data = cursor.fetchall()
        mysql.connection.commit()
        cursor.execute("SELECT ROUND(AVG(temperature), 1), ROUND(AVG(duration), 1) FROM raw_data WHERE date BETWEEN '{}' AND '{}'".format(helpers.get_date_range('years'), helpers.get_date_tomorrow()))
        average = cursor.fetchall()
        mysql.connection.commit()
        cursor.close()
    # Return view rendering the data and return 404 if timeframe is invalid
    if timeframe == 'days' or timeframe == 'weeks' or timeframe == 'months' or timeframe == 'years':
        return render_template('statistics.html', timeframe=timeframe, period=period, get_date_range=helpers.get_date_range, strftime=datetime.strftime, data=data, average=average)
    else:
        return render_template('404.html'), 404

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

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
