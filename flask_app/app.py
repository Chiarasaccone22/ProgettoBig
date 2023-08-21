from flask import Flask, render_template
from waitress import serve
import psycopg2
import boto3
import pymongo


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT']=0

@app.route('/')
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

@app.route('/connDynamo')
#funzione che gestisce la home page
def connDynamo():
    region_name = 'us-east-1'
    #dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    print('connessione...')
    dynamodb = boto3.resource('dynamodb',region_name=region_name)
    print('creo tabella...')
    table = dynamodb.create_table(
        TableName='Books',
        KeySchema=[
            {
                'AttributeName': 'book_id',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'title',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'book_id',
                # AttributeType refers to the data type 'N' for number type and 'S' stands for string type.
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'title',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            # ReadCapacityUnits set to 10 strongly consistent reads per second
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10  # WriteCapacityUnits set to 10 writes per second
        }
    )
    print("Status:",dynamodb.tables.all())
    return render_template('index.html')

@app.route('/connMongo')
def connMongo():
    connessione = pymongo.MongoClient("mongodb://172.22.0.2:27017/")
    l = connessione.list_database_names()
    return render_template('index.html',posts=l)

if __name__ == "__main__":
    #app.run(debug=True)
    serve(app, host="0.0.0.0", port=8080)
