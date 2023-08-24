from flask import Flask, render_template
from waitress import serve
from py2neo import Graph
import psycopg2
import boto3
import pymongo
from cassandra.cluster import Cluster
import pandas as pd
import csv
import caricamentoDy


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT']=0

#creiamo variabili globali di connessione inizializzandole a None
connessionePostgres=psycopg2.connect(
        host="postgresDb",
        port="5432",
        user="postgres",
        password="password",
        database="postgres"
    )
connessioneMongo= pymongo.MongoClient("mongodb://mongoDb:27017/") 

connessioneNeo=Graph("bolt://neo4jDbGUI:7687")

connessioneCassandra=Cluster(['cassandraDb'], port=9042).connect()

connessioneDynamo= boto3.resource('dynamodb',endpoint_url='http://dynamoDbGUI:8000',region_name='us-east-1')

#apertura di default
@app.route('/')
def index():

    """ #connesione Postgres
        connessionePostgres = psycopg2.connect(
            host="postgresDb",
            port="5432",
            user="postgres",
            password="password",
            database="postgres"
        ) """

    return render_template('index.html')

@app.route('/connPostgres')
def connPostgres():
    """ conn = psycopg2.connect(
        host="postgresDb",
        port="5432",
        user="postgres",
        password="password",
        database="postgres"
    ) """

    cursor = connessionePostgres.cursor()
    cursor.execute("SELECT * FROM posts")
    results = cursor.fetchall()
    """   cursor.close()
        connessionePostgres.close() """

    return render_template('index.html', posts=results)


# Caricamento dati da csv a postgres con csv nella webapp
@app.route('/caricamentoPostgres')
def caricamentoPostgres():
    """     # Connessione a postgres
        conn = psycopg2.connect(
            host="postgresDb",
            port="5432",
            user="postgres",
            password="password",
            database="postgres"
        ) """
    
    
    cursor = connessionePostgres.cursor()

    # Esecuzione della query per creare la tabella
    cursor.execute('DROP TABLE IF EXISTS voli; CREATE TABLE voli ( colonna1 text,colonna2 text)')

    # Caricamento dei dati dal file CSV nella tabella
    with open('./airlines.csv', 'r') as f:
        next(f)  # Salta la riga dell'intestazione
        print('inserisco...')
        cursor.copy_from(f, 'voli', sep=',', null='')  # Copia i dati nel database

    # Commit delle modifiche e chiusura della connessione
    connessionePostgres.commit()
    cursor.execute("SELECT * FROM voli")
    # mi da tutte le ennuple come righe
    results = cursor.fetchall()
   
    """ # chiudo connessione
    cursor.close()
    conn.close() """

    return render_template('index.html', posts=results)


@app.route('/connDynamo')
#funzione che gestisce la home page
def connDynamo():
    dynamodb = connessioneDynamo
    tables = list(dynamodb.tables.all())
    return render_template('index.html', posts=tables)

@app.route('/caricamentoDynamo')
#funzione che gestisce la home page
def caricamentoDynamoDB():
    dynamodb=caricamentoDy.caricamentoDynamo(connessioneDynamo)
    tables = list(dynamodb.tables.all())
    return render_template('index.html', posts=tables)


@app.route('/connMongo')
def connMongo():
    mongo = connessioneMongo
    lista = mongo.list_database_names()
    return render_template('index.html',posts=lista)


# Inserisco dati da csv in Mongo (crea sia db che collezione se non esistono)
@app.route('/caricamentoMongo')
def caricamentoMongo():
    # connessione al db
    mongo = connessioneMongo
    # database e collezione li ho creati mediante l'interfaccia mongoGUI
    # prendo database
    db_name = 'voli'
    if db_name in mongo.list_database_names():
        db = mongo.get_database(db_name)
    else:
        db = mongo[db_name]
    
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
    """  connessione.close() """
    # visualizzo i dati caricati
    return render_template('index.html',posts=data_json)


@app.route('/connNeo')
#funzione che gestisce database Neo4j
def connNeo():
    graph = connessioneNeo

    query = "MATCH (p:Person) RETURN p"
    result = graph.run(query)
    
    return render_template('index.html', posts=result)


@app.route('/connCassandra')
def connCassandra():
   
    session = connessioneCassandra
    #session.execute("""
    #CREATE KEYSPACE IF NOT EXISTS cityinfo
    #WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}""")
    session.execute('USE cityinfo')
    session.execute('CREATE TABLE IF NOT EXISTS prova (id int,PRIMARY KEY(id))')
    # rows = session.execute('INSERT INTO prova (id) VALUES (0)')
    rows = session.execute('SELECT * FROM prova')

    return render_template('index.html', posts=rows)

@app.route('/caricamentoCassandra')
def caricamentoCassandra():
    # connessione a cassandra
    
    session = connessioneCassandra
    
    # imposto ambiente di lavoro dove sono la table
    # Query per verificare l'esistenza di un keyspace
    keyspace_name = "cityinfo"
    query = f"SELECT keyspace_name FROM system_schema.keyspaces WHERE keyspace_name = '{keyspace_name}'"
    result = session.execute(query)

    if not(result.one()):
        query = f"CREATE KEYSPACE {keyspace_name} WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': 1}}"
        session.execute(query)
    query = f"USE {keyspace_name}"
    session.execute(query)

    #session.execute('USE cityinfo')

    # se non c'è crea table altrimenti mantiene
    session.execute('CREATE TABLE IF NOT EXISTS prova (id text,campo text,PRIMARY KEY(id))')
    # legge file csv
    csv_file_path = './airlines.csv'

    # scorre file csv
    with open(csv_file_path, 'r') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)  # Salta la riga dell'intestazione

        for row in csv_reader:
            colonna1 = row[0]
            colonna2 = row[1]
            # Estrai altre colonne...

            query = f"INSERT INTO prova (id, campo) VALUES (%s, %s)"  # Sostituisci con il nome della tua tabella e le colonne corrispondenti
            session.execute(query, (colonna1, colonna2))  # Sostituisci con i valori da inserire

    # chiusura cluster e relativa sessione
    rows = session.execute('SELECT * FROM prova')
    #cluster.shutdown()
    return render_template('index.html', posts=rows)

if __name__ == "__main__":
    #app.run(debug=True)
    serve(app, host="0.0.0.0", port=8080)
