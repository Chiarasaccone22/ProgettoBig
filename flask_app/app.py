from flask import Flask, render_template,jsonify,Response, redirect, url_for,  request
from waitress import serve
from py2neo import Graph
import psycopg2
import boto3
from boto3.dynamodb.conditions import Key, Attr
import pymongo
from cassandra.cluster import Cluster
import pandas as pd
import csv
import caricamentoDy, caricamentoPos, caricamentoMongo, caricamentoCassandra
import logging
from bson import json_util

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT']=0
logging.basicConfig(level=logging.INFO)

#creiamo variabili globali di connessione inizializzandole 

connessioneMongo= pymongo.MongoClient("mongodb://mongoDb:27017/") 

connessioneNeo=Graph("bolt://neo4jDbGUI:7687")

connessioneCassandra=Cluster(['cassandraDb'], port=9042).connect()

connessioneDynamo= boto3.resource('dynamodb',endpoint_url='http://dynamoDbGUI:8000',region_name='us-east-1')

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'  # '*' consente a qualsiasi dominio di accedere, ma è possibile specificare un dominio specifico
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

#apertura di default
@app.route('/')
def index():
    logging.debug('Apro le connessioni...')
    return render_template('index.html')


#richiesta postgres
@app.route('/selectpostgres/<partenzaPrevista>', methods=['GET'])
def selectpostgres(partenzaPrevista):
    #estrai il parametro in input con la request
    #param = request.args.get('partenzaPrevista')
    param = partenzaPrevista
    #apri connessione
    connessionePostgres=psycopg2.connect(
        host="postgresDb",
        port="5432",
        user="postgres",
        password="password",
        database="postgres"
    )
    cursor = connessionePostgres.cursor()
    # Esecuzione della query con il parametro in input
    cursor.execute("SELECT volo_id, compagnia, destinazione FROM volitimes WHERE partenza_prevista = %s" , (param,))
    #cursor.execute("SELECT * FROM volitimes WHERE partenza_prevista = %s" , (param,))
    results = cursor.fetchall()
    cursor.close()
    
    return jsonify(results)
   
#richiesta postgrescascata
@app.route('/selectpostgrescascata/<partenzaPrevista>', methods=['GET'])
def selectpostgrescascata(partenzaPrevista):
    #estrai il parametro in input con la request
    #param = request.args.get('partenzaPrevista')
    param = partenzaPrevista
    #apri connessione
    connessionePostgres=psycopg2.connect(
        host="postgresDb",
        port="5432",
        user="postgres",
        password="password",
        database="postgres"
    )
    
    cursor = connessionePostgres.cursor()
    # Esecuzione della query con il parametro in input
    cursor.execute("SELECT volo_id, compagnia, destinazione FROM volitimes WHERE partenza_prevista = %s" , (param,))
    results = cursor.fetchall()
    logging.critical(results)
    cursor.close()

    #file json di output
    output={
        'resultMongo': [],
        'resultDynamo': [],
        'resultCassandra': [],

    }

    logging.critical(results)
    #interrogazione a cassandra con il volo_id
    for volo in results:
            result=selectcassandra(str(volo[0]))
            output["resultCassandra"].append(result)

    #interrogazione a dynamo con la compagnia aerea
    for compagniaid in results:
            result=selectdynamo(compagniaid[1])
            output["resultDynamo"].append(result)

    #interrogazione a mongo con l'areoporto di destinazione
    for iatacode in results:
            result=selectmongo(iatacode[2])
            output["resultMongo"].append(result)
    
    logging.critical(output)
    return jsonify(output) 
   

#richiesta cassandra
@app.route('/selectcassandra/<idvolo>', methods=['GET'])
def selectcassandra(idvolo):
    #estrai il parametro in input con la request
    param = idvolo
    #apri connessione
    session = connessioneCassandra
    session.execute('USE ProgettoBig')
    # Esecuzione della query con il parametro in input
    rows = session.execute('SELECT * FROM voliInt WHERE volo_id= %s',  (param,))
    return json_util.dumps(rows)
    
#richiesta dynamo   
@app.route('/selectdynamo/<compagniaid>',methods=['GET'])
def selectdynamo(compagniaid):
    #connessione
    dynamodb = connessioneDynamo
    #parametro
    param=compagniaid
    table = dynamodb.Table("compagnieAeree")
    #query
    response = table.query(KeyConditionExpression= Key('compagnia_id').eq(param,))
    items = response.get('Items', [])
    # items = response['Items']
    return items
    #return jsonify(items)


#richiesta mongo   
@app.route('/selectmongo/<iatacode>',methods=['GET'])
def selectmongo(iatacode):
    #parametro
    param=iatacode
    #connessione
    mongo = connessioneMongo
    dataset = mongo["aeroporti"]
    tabella = dataset["aeroporto"]
    #query
    myquery = { "IATA_CODE": param }
    result = tabella.find(myquery)
    return json_util.dumps(result)




#Gestione connessione Postgres
@app.route('/connPostgres',methods=['GET'])
def connPostgres():
    connessionePostgres=psycopg2.connect(
        host="postgresDb",
        port="5432",
        user="postgres",
        password="password",
        database="postgres"
    )
    cursor = connessionePostgres.cursor()
    cursor.execute("SELECT DISTINCT partenza_prevista FROM volitimes ORDER BY partenza_prevista")
    results = cursor.fetchall()
    cursor.close()
    return jsonify(results)
    #return render_template('index.html', posts=results)


# Gestione del caricamento dei dataset nel database Postgres
@app.route('/caricamentoPostgres',methods=['GET'])
def caricamentoPostgresDB():
    connessionePostgres=psycopg2.connect(
        host="postgresDb",
        port="5432",
        user="postgres",
        password="password",
        database="postgres"
    )
    #carichiamo il database con i csv in caricamentoPos e facciamo una query select
    results=caricamentoPos.caricamentoPostgres(connessionePostgres)
    #cursor = postgres.cursor()

    return jsonify(results)
    #return render_template('index.html', posts=results)


# Gestione connessione Dynamo
@app.route('/connDynamo',methods=['GET'])
def connDynamo():
    #carichiamo il database con i csv in caricamentoPos e restituiamo tutte le tabelle
    dynamodb = connessioneDynamo
    #tables = list(dynamodb.tables.all())
    tabella = dynamodb.Table("compagnieAeree")
    response = tabella.scan()
    return jsonify(response)
    #return render_template('index.html', posts=tables)


# Gestione del caricamento dei dataset nel database Dynamo Db
@app.route('/caricamentoDynamo',methods=['GET'])
def caricamentoDynamoDB():
    dynamodb=caricamentoDy.caricamentoDynamo(connessioneDynamo)
    tabella = dynamodb.Table("compagnieAeree")
    response = tabella.scan()
    return jsonify(response)
    #return render_template('index.html', posts=tables)

# Gestione connessione Mongo
@app.route('/connMongo',methods=['GET'])
def connMongo():
    mongo = connessioneMongo
    lista = mongo.list_database_names()
    #if "voli" in lista:
    dbVoli = mongo["aeroporti"]
    collezioneVolo = dbVoli["aeroporto"]
    voli = {collezioneVolo.find()}
    """ voli_lista = []
    for documento in voli:
        documento['_id'] = str(documento['_id'])
        voli_lista.append(documento)
    return jsonify(voli_lista) """
    
    return json_util.dumps(voli)
    #return render_template('index.html',posts=lista)


# Gestione del caricamento dei dataset nel database Mongo
@app.route('/caricamentoMongo',methods=['GET'])
def caricamentoMongoDB():
    # Carichiamo il database con i csv in caricamentoMongo e restituiamo tutti i nomi delle tabelle
    mongo = caricamentoMongo.caricamentoMon(connessioneMongo)
    mongo = connessioneMongo
    lista = mongo.list_database_names()
    return jsonify(lista)
    #return render_template('index.html',posts=lista)


# Gestione connessione Neo4j
@app.route('/connNeo',methods=['GET'])
def connNeo():
    #connessione
    graph = connessioneNeo
    #query
    query = "MATCH (p:Person) RETURN p"
    result = graph.run(query)
    return jsonify(result)
    #return render_template('index.html', posts=result)


# Gestione connessione Cassandra
@app.route('/connCassandra',methods=['GET'])
def connCassandra():
    session = connessioneCassandra
    session.execute('USE ProgettoBig')
    rows = session.execute('SELECT * FROM voliInt')
    return json_util.dumps(rows)
    #return jsonify(rows)
    #return render_template('index.html', posts=rows)


# Gestione del caricamento dei dataset nel database Cassandra
@app.route('/caricamentoCassandra',methods=['GET'])
def caricamentoCassandraDB():
   # Carichiamo il database con i csv in caricamentoCassandra e restituiamo tutte le ennuple
    cassandra = caricamentoCassandra.caricamentodb(connessioneCassandra)
    cassandra.execute('USE ProgettoBig')
    rows = cassandra.execute('SELECT * FROM voliInt')
    return json_util.dumps(rows)
    #return jsonify(rows)
    #return render_template('index.html', posts=rows)


""" #richiesta postgrescascata
@app.route('/selectpostgrescascata/<partenzaPrevista>', methods=['GET'])
def selectpostgrescascata(partenzaPrevista):
    #estrai il parametro in input con la request
    #param = request.args.get('partenzaPrevista')
    param = partenzaPrevista
    #apri connessione
    connessionePostgres=psycopg2.connect(
        host="postgresDb",
        port="5432",
        user="postgres",
        password="password",
        database="postgres"
    )
    #query 1 che mi seleziona i voli id con quella partenza prevista
    cursor = connessionePostgres.cursor()
    cursor.execute("SELECT volo_id FROM volitimes WHERE partenza_prevista = %s" , (param,))
    voli = cursor.fetchall()
    cursor.close()

    #query 2 che mi seleziona i voli id con quella partenza prevista
    cursor = connessionePostgres.cursor()
    cursor.execute("SELECT  compagnia FROM volitimes WHERE partenza_prevista = %s" , (param,))
    compagnie = cursor.fetchall()
    cursor.close()

    #query 1 che mi seleziona i voli id con quella partenza prevista
    cursor = connessionePostgres.cursor()
    cursor.execute("SELECT destinazione FROM volitimes WHERE partenza_prevista = %s" , (param,))
    destinazioni = cursor.fetchall()
    cursor.close()
    
    return jsonify(results) """
   

if __name__ == "__main__":
    #app.run(debug=True)
    serve(app, host="0.0.0.0", port=8080)
