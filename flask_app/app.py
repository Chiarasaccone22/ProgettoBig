from flask import Flask, render_template
from waitress import serve
import sqlite3
import psycopg2
import boto3

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT']=0

@app.route('/')
#funzione che gestisce la home page
def index():
#connessione tra database e pagina web
#ora che abbiamo la lista python di posts, che sarebbero le ennuple del nostro database, dobbiamo passare la lista posts nel template html per il collegamento
#per aggiungere un qualsiasi oggetto e passarlo al tamplate html basta passarlo come argomento della funzione render_template : posts=posts dove il primo è il nome con cui lo accediamo in html e il secondo è ciò che abbiamo creato qui
#per il tamplate html
    return render_template('index.html')

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

if __name__ == "__main__":
    app.run(debug=True)
    serve(app, host="0.0.0.0", port=8080)
