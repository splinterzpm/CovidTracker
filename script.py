from flask import Flask, jsonify, render_template, request
import mysql.connector
import requests
import simplejson 
import json
import datetime

app = Flask(__name__)

config = {
    'user': '***REMOVED***',
    'password': '***REMOVED***',
    'database': 'marushov-mysqldb',
    'host': '***REMOVED***',
    'port': 3306,
    'ssl_ca': 'BaltimoreCyberTrustRoot.crt.pem',
    'ssl_verify_cert': 'true'
}


def create_table():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS tracker(id INT NOT NULL, date_value DATE, country_code VARCHAR(255), confirmed INT, deaths INT, stringency_actual INT, stringency INT, PRIMARY KEY (id))")
    conn.commit()
    cursor.close()
    conn.close()
    print ("table created")

def insert_to_db():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    date = datetime.date(2021, 8, 13)
    # ARG, CHN, ESP, DEU, GBR, ISR, ITA, JPN, RUS, USA
    url = "https://covidtrackerapi.bsg.ox.ac.uk/api/v2/stringency/date-range/{}/{}".format(date, datetime.date.today())
    Uresponse = requests.get(url)
    Jresponse = Uresponse.text
    data = json.loads(Jresponse)
    countries = ['ARG', 'CHN', 'ESP', 'GBR', 'DEU', 'ISR', 'ITA', 'JPN', 'RUS', 'USA']
    tableid = 2222
    while date < datetime.date.today():
        for id, i in enumerate(countries):
            if i in data["data"][date.strftime("%Y-%m-%d")]:
                tableid +=1
                date_value = data["data"][date.strftime("%Y-%m-%d")][i]["date_value"]
                country_code = data["data"][date.strftime("%Y-%m-%d")][i]["country_code"]
                confirmed = data["data"][date.strftime("%Y-%m-%d")][i]["confirmed"]
                deaths = data["data"][date.strftime("%Y-%m-%d")][i]["deaths"]
                stringency_actual = data["data"][date.strftime("%Y-%m-%d")][i]["stringency_actual"]
                stringency = data["data"][date.strftime("%Y-%m-%d")][i]["stringency"]
            else: id +=1
            sql = "INSERT IGNORE INTO tracker(id, date_value, country_code, confirmed, deaths, stringency_actual, stringency) " \
                "VALUES(%s, %s, %s, %s, %s, %s, %s)"
            values = (tableid, date_value, country_code, confirmed, deaths, stringency_actual, stringency)
            cursor.execute(sql, values)
            conn.commit()
            print ("inserted {} {} {}".format(tableid, date, i))
        date = date + datetime.timedelta(days=1)
    cursor.close()
    conn.close()
    return 'insertion completed'

@app.route("/", methods=['GET', 'POST'])

def index():
    create_table()
    insert_to_db()
    # if request.method == 'POST':
    #     pass
    #     # conn = mysql.connect()
    #     # cursor = conn.cursor() 
    #     # cursor.execute("USE marushov-mysqldb CREATE TABLE tracker(date_value DATE, country_code VARCHAR(255), confirmed INT, deaths INT, stringency_actual INT, stringency INT)")
    #     start_date = request.form.get('start_date')
    #     country_code = request.form.get('country_code')
    #     url = "https://covidtrackerapi.bsg.ox.ac.uk/api/v2/stringency/actions/{}/{}".format(country_code, start_date)
    #     Uresponse = requests.get(url)
    #     try:
    #         Uresponse = requests.get(url)
    #     except requests.ConnectionError:
    #         return "Connection Error"  
    #     Jresponse = Uresponse.text
    #     data = json.loads(Jresponse)
    #     return data # "confirmed {}".format(data["stringencyData"]["confirmed"])
    # else:
    return render_template('index.html')

@app.route("/data", methods=['GET','POST'])

def data():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor() 
    start_date = request.form.get('start_date')
    # try:
    #     start_date > datetime.date.today()
    # except:
    #     return "Wrong date error" 
    sql = "SELECT date_value, country_code, confirmed, deaths, stringency_actual, stringency FROM tracker WHERE date_value = %s ORDER BY deaths"
    cursor.execute(sql, (start_date,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('data.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)