from flask import Flask, render_template
from waitress import serve
from py2neo import Graph
import psycopg2
import boto3
import pymongo
from cassandra.cluster import Cluster
import pandas as pd
import csv
<<<<<<< Updated upstream
import caricamentoDy, caricamentoPos, caricamentoMongo, caricamentoCassandra

=======
import caricamentoDy
import logging
>>>>>>> Stashed changes

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT']=0
logging.basicConfig(level=logging.INFO)

#creiamo variabili globali di connessione inizializzandole 

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
<<<<<<< Updated upstream
=======
    logging.debug('Apro le connessioni...')
    """ #connesione Postgres
        connessionePostgres = psycopg2.connect(
            host="postgresDb",
            port="5432",
            user="postgres",
            password="password",
            database="postgres"
        ) """
>>>>>>> Stashed changes

    return render_template('index.html')


#Gestione connessione Postgres
@app.route('/connPostgres')
def connPostgres():

    cursor = connessionePostgres.cursor()
    cursor.execute("SELECT * FROM posts")
    results = cursor.fetchall()

    return render_template('index.html', posts=results)


# Gestione del caricamento dei dataset nel database Postgres
@app.route('/caricamentoPostgres')
def caricamentoPostgresDB():
    #carichiamo il database con i csv in caricamentoPos e facciamo una query select
    postgres=caricamentoPos.caricamentoPostgres(connessionePostgres)
    cursor = postgres.cursor()
    cursor.execute("SELECT * FROM posts")
    results = cursor.fetchall()
    return render_template('index.html', posts=results)


# Gestione connessione Dynamo
@app.route('/connDynamo')
def connDynamo():
    #carichiamo il database con i csv in caricamentoPos e restituiamo tutte le tabelle
    dynamodb = connessioneDynamo
    tables = list(dynamodb.tables.all())
    return render_template('index.html', posts=tables)


# Gestione del caricamento dei dataset nel database Dynamo Db
@app.route('/caricamentoDynamo')
def caricamentoDynamoDB():
    dynamodb=caricamentoDy.caricamentoDynamo(connessioneDynamo)
    tables = list(dynamodb.tables.all())
    return render_template('index.html', posts=tables)

# Gestione connessione Mongo
@app.route('/connMongo')
def connMongo():
    mongo = connessioneMongo
    lista = mongo.list_database_names()
    return render_template('index.html',posts=lista)


# Gestione del caricamento dei dataset nel database Mongo
@app.route('/caricamentoMongo')
def caricamentoMongoDB():
    # Carichiamo il database con i csv in caricamentoMongo e restituiamo tutti i nomi delle tabelle
    mongo = caricamentoMongo.caricamentoMon(connessioneMongo)
    mongo = connessioneMongo
    lista = mongo.list_database_names()
    return render_template('index.html',posts=lista)


# Gestione connessione Neo4j
@app.route('/connNeo')
def connNeo():
    #connessione
    graph = connessioneNeo
    #query
    query = "MATCH (p:Person) RETURN p"
    result = graph.run(query)
    return render_template('index.html', posts=result)


# Gestione connessione Cassandra
@app.route('/connCassandra')
def connCassandra():
    session = connessioneCassandra
    session.execute('USE cityinfo')
    session.execute('CREATE TABLE IF NOT EXISTS prova (id text,campo text,PRIMARY KEY(id))')
    rows = session.execute('SELECT * FROM prova')
    return render_template('index.html', posts=rows)


# Gestione del caricamento dei dataset nel database Cassandra
@app.route('/caricamentoCassandra')
def caricamentoCassandraDB():
   # Carichiamo il database con i csv in caricamentoCassandra e restituiamo tutte le ennuple
    cassandra = caricamentoCassandra.caricamentodb(connessioneCassandra)
    cassandra.execute('USE cityinfo')
    rows = cassandra.execute('SELECT * FROM prova')
    return render_template('index.html', posts=rows)







if __name__ == "__main__":
    #app.run(debug=True)
    serve(app, host="0.0.0.0", port=8080)
