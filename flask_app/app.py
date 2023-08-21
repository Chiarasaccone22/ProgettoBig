from flask import Flask, render_template
from waitress import serve
import psycopg2
import boto3
import pymongo


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT']=0

@app.route('/connPostgres')
def index():
    return render_template('index.html')

@app.route('/connPostgres')
def connPostgres():

    print('connessione...')
    conn = psycopg2.connect(
        host="172.22.0.6",
        port="5432",
        user="postgres",
        password="password",
        database="postgres"
    )
    print('connesso...')
    cursor = conn.cursor()
    print('faccio query...')
    cursor.execute("SELECT * FROM posts")
    results = cursor.fetchall()
    print('chiudo connessione...')
    cursor.close()
    conn.close()

    return render_template('index.html', posts=results)

@app.route('/')
#funzione che gestisce la home page
def connDynamo():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Books')
    #Esegui una query sulla tabella utilizzando il titolo come chiave
    response = table.query(
        KeyConditionExpression= "book_id= :book_id",
        ExpressionAttributeValues= {
            ":book_id": {"N": "3"}
            } 
)



    items = response['Items']

    return render_template('index.html', posts=items)

@app.route('/connMongo')
def connMongo():
    connessione = pymongo.MongoClient("mongodb://172.22.0.2:27017/")
    l = connessione.list_database_names()
    return render_template('index.html',posts=l)

if __name__ == "__main__":
    #app.run(debug=True)
    serve(app, host="0.0.0.0", port=8080)
