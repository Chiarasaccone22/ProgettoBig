from flask import Flask, render_template
from waitress import serve
import psycopg2
import boto3
import pymongo


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT']=0

#apertura di default
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/connPostgres')
def connPostgres():

    conn = psycopg2.connect(
        host="172.22.0.6",
        port="5432",
        user="postgres",
        password="password",
        database="postgres"
    )

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts")
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('index.html', posts=results)

@app.route('/connDynamo')
#funzione che gestisce la home page
def connDynamo():
    dynamodb = boto3.resource('dynamodb')
    tables = list(dynamodb.tables.all())
  

    return render_template('index.html', posts=tables)

@app.route('/connMongo')
def connMongo():
    connessione = pymongo.MongoClient("mongodb://172.22.0.2:27017/")
    l = connessione.list_database_names()
    return render_template('index.html',posts=l)




if __name__ == "__main__":
    #app.run(debug=True)
    serve(app, host="0.0.0.0", port=8080)
