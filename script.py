from flask import Flask, jsonify, render_template, request
from flask_mysqldb import MySQL
import requests
import simplejson 
import json

app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'CovidData'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql = MySQL(app)

@app.route("/", methods=['GET', 'POST'])

def index():

    if request.method == 'POST':
        if request.form.get('submitBtn') == 'Отправить':
            pass 
            start_date = request.form.get('date-start')
            end_date = request.form.get('date-end')
            url = "https://covidtrackerapi.bsg.ox.ac.uk/api/v2/stringency/date-range/{}/{}".format(start_date, end_date)
            Uresponse = requests.get(url)
            try:
                Uresponse = requests.get(url)
            except requests.ConnectionError:
                return "Connection Error"  
            Jresponse = Uresponse.text
            data = json.loads(Jresponse)
            return Jresponse
    elif request.method == 'GET':
        return render_template('index.html')
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)