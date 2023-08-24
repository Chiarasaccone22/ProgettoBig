from flask import Flask, render_template
from waitress import serve
from py2neo import Graph
import psycopg2
import boto3
import pymongo
from cassandra.cluster import Cluster
import pandas as pd


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT']=0

#apertura di default
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/connPostgres')
def connPostgres():
    conn = psycopg2.connect(
        host="postgresDb",
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


# Caricamento dati da csv a postgres con csv nella webapp
@app.route('/caricamentoPostgres')
def caricamentoPostgres():
    # Connessione a postgres
    conn = psycopg2.connect(
        host="postgresDb",
        port="5432",
        user="postgres",
        password="password",
        database="postgres"
    )
    # cursore che si muove su mmmh
    cur = conn.cursor()

    # Esecuzione della query per creare la tabella
    cur.execute('DROP TABLE IF EXISTS voli; CREATE TABLE voli ( colonna1 text,colonna2 text)')

    # Caricamento dei dati dal file CSV nella tabella
    with open('./airlines.csv', 'r') as f:
        next(f)  # Salta la riga dell'intestazione
        print('inserisco...')
        cur.copy_from(f, 'voli', sep=',', null='')  # Copia i dati nel database

    # Commit delle modifiche e chiusura della connessione
    conn.commit()
    cur.execute("SELECT * FROM voli")
    # mi da tutte le ennuple come righe
    results = cur.fetchall()
    # chiudo connessione
    cur.close()
    conn.close()
    return render_template('index.html', posts=results)


@app.route('/connDynamo')
#funzione che gestisce la home page
def connDynamo():
    dynamodb = boto3.resource('dynamodb',endpoint_url='http://dynamoDbGUI:8000',region_name='us-east-1')
    tables = list(dynamodb.tables.all())
    return render_template('index.html', posts=tables)

@app.route('/connMongo')
def connMongo():
    connessione = pymongo.MongoClient("mongodb://mongoDb:27017/") ##CAMBIARE OGNI VOLTA
    l = connessione.list_database_names()
    return render_template('index.html',posts=l)


# Inserisco dati da csv in Mongo (crea sia db che collezione se non esistono)
@app.route('/caricamentoMongo')
def caricamentoMongo():
    # connessione al db
    connessione = pymongo.MongoClient("mongodb://mongoDb:27017/") ##CAMBIARE OGNI VOLTA
    # database e collezione li ho creati mediante l'interfaccia mongoGUI
    # prendo database
    db_name = 'voli'
    if db_name in connessione.list_database_names():
        db = connessione.get_database(db_name)
    else:
        db = connessione[db_name]
    
    collection_name = 'volo'
    # verifico se c'è la collection
    if collection_name in db.list_collection_names():
        # c'è e la prendo
        collection = db[collection_name]
    else :
        # non c'è la creo
        collection = db.create_collection(collection_name)
   
    # leggo file csv da caricare
    data = pd.read_csv('./airlines.csv')
    # li metto da dataframe a json
    data_json = data.to_dict(orient='records')
    # inserisco i dati
    collection.insert_many(data_json)

    # chiudo connessione
    connessione.close()
    # visualizzo i dati caricati
    return render_template('index.html',posts=data_json)


@app.route('/connNeo')
#funzione che gestisce database Neo4j
def connNeo():
    graph = Graph("bolt://neo4jDbGUI:7687")

    query = "MATCH (p:Person) RETURN p"
    result = graph.run(query)
    
    return render_template('index.html', posts=result)

@app.route('/connCassandra')
def connCassandra():
    cluster = Cluster(['cassandraDb'], port=9042)
    session = cluster.connect()
    #session.execute("""
    #CREATE KEYSPACE IF NOT EXISTS cityinfo
    #WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}""")
    session.execute('USE cityinfo')
    session.execute('CREATE TABLE IF NOT EXISTS prova (id int,PRIMARY KEY(id))')
    rows = session.execute('INSERT INTO prova (id) VALUES (0)')
    rows = session.execute('SELECT * FROM prova')

    return render_template('index.html', posts=rows)


if __name__ == "__main__":
    #app.run(debug=True)
    serve(app, host="0.0.0.0", port=8080)
