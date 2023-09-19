from flask import Flask, render_template,jsonify,Response, redirect, url_for, send_file, request
#from flask_cors import CORS
from waitress import serve
from py2neo import Graph, Node, Relationship
import psycopg2
import boto3
from boto3.dynamodb.conditions import Key, Attr
import pymongo
from cassandra.cluster import Cluster
import pandas as pd
import csv
import caricamentoDy, caricamentoPos, caricamentoMongo, caricamentoCassandra, caricamentoNeo4j
import logging
from bson import json_util
import json
#from flask import CORS, cross_origin

app = Flask(__name__)
#CORS(app)
#cors = CORS(app, resources={r"/foo": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

app.config['SEND_FILE_MAX_AGE_DEFAULT']=0
logging.basicConfig(level=logging.INFO)

#creiamo variabili globali di connessione inizializzandole 

connessioneMongo= pymongo.MongoClient("mongodb://mongoDb:27017/") 

connessioneNeo=Graph("bolt://neo4jDbGUI:7687")

connessioneCassandra=Cluster(['cassandraDb'], port=9042).connect()

connessioneDynamo= boto3.resource('dynamodb',endpoint_url='http://dynamoDbGUI:8000',region_name='us-east-1')

@app.after_request
def add_csp_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'  # '*' consente a qualsiasi dominio di accedere, ma è possibile specificare un dominio specifico
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Content-Security-Policy'] = "frame-ancestors 'self' http://localhost:7474/;"
    return response

#apertura di default
@app.route('/')
#@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
def index():
    logging.debug('Apro le connessioni...')
    return render_template('index.html')


####################################################  METODI  PER  QUERY A CASCATA  ############################################

#richiesta postgres cascata
@app.route('/selectpostgrescascata/<partenzaPrevista>', methods=['GET'])
#@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
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
    
    logging.critical('Query su postgres...')
    cursor = connessionePostgres.cursor()
    # Esecuzione della query con il parametro in input
    cursor.execute("SELECT volo_id, compagnia, destinazione, partenza_prevista FROM volitimes WHERE partenza_prevista = %s" , (param,))
    results = cursor.fetchall()
    cursor.close()
    logging.critical(results)

    #file json di output
    output={
        'resultMongo': [],#cursor.execute("SELECT * FROM volitimes WHERE partenza_prevista = %s" , (param,))
        'resultDynamo': [],
        'resultCassandra': [],

    }

    logging.critical('Query su cassandra...')
    #interrogazione a cassandra con il volo_id
    for volo in results:
            result=selectcassandra(volo)
            result = json.loads(result)
            """ logging.critical('RESULT DI CASSANDRA')
            logging.critical(result) """
            #if result not in output["resultCassandra"]: abbiamo eliminato il DISTINCT
            if result != []:
                if type(result[0]) == list:
                    for l in result:
                        output["resultCassandra"].append(l)
                else:
                    output["resultCassandra"].append(result)
    logging.critical(output["resultCassandra"])
    logging.critical('Query su dynamo...')
    #interrogazione a dynamo con la compagnia aerea
    for compagniaid in results:
            result=selectdynamo(compagniaid[1])
            if result not in output["resultDynamo"]: # il DISTINCT
                output["resultDynamo"].append(result)
    logging.critical(output["resultDynamo"])
    logging.critical('Query su mongo...')
    #interrogazione a mongo con l'areoporto di destinazione
    for iatacode in results:
            result=selectmongo(iatacode[2])
            result = json.loads(result)
            """ logging.critical(result)
            logging.critical(type(result)) """
            if result not in output["resultMongo"]: # il DISTINCT
                output["resultMongo"].append(result)
    logging.critical(output["resultMongo"])
    
    #PASSO DATI A NEO4J E STAMPO
    logging.critical('Caricamento dati in neo4j...')
    resultN4j = caricamentoNeo4j.neo4jElaborazione(output,'P',connessioneNeo)

    logging.critical(output)
    return jsonify(output) 
   
################################################################################################

#richiesta cassandra cascata
@app.route('/selectcassandracascata/<idvolo>', methods=['GET'])
#@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
def selectcassandracascata(idvolo):
    #estrai il parametro in input con la request
    param = idvolo
    #apri connessione
    session = connessioneCassandra
    session.execute('USE ProgettoBig')
    # Esecuzione della query con il parametro in input

    logging.critical('Query in cassandra...')
    rows= session.execute('SELECT volo_id, compagnia, destinazione FROM voliInt WHERE volo_id=%s',  (param,))
    logging.critical(rows)

    #file json di output
    output={
        'resultPostgres': [],
        'resultDynamo': [],
        'resultMongo': [],
    }

    """ logging.critical('ROWS')
    logging.critical(rows) """
    #interrogazione a postgres con il volo_id
    #for volo in rows:
    logging.critical('Query in postgres...')
    resultPostgres=selectpostgresvoloid(idvolo)
    output["resultPostgres"].append(resultPostgres)
    logging.critical(output["resultPostgres"])

    #interrogazione a mongo con (l'areoporto di destinazione, no iatacode che devo prendere in postgres)
    logging.critical('Query in mongo e dynamo...')
    for r in rows:
        """ logging.critical('R.')
        logging.critical(r) """
        resultMongo=selectmongo(r[2])
        daCaricare = json.loads(resultMongo)
        #if daCaricare not in output["resultMongo"]:  abbiamo eliminato il DISTINCT
        output["resultMongo"].append(daCaricare)

        resultDynamo=selectdynamo(r[1])
        #if resultDynamo not in output["resultDynamo"]: abbiamo eliminato il DISTINCT
        output["resultDynamo"].append(resultDynamo)
    logging.critical(output["resultMongo"])
    logging.critical(output["resultDynamo"])

    logging.critical('Caricamento dati in neo4j...')
    resultN4j = caricamentoNeo4j.neo4jElaborazione(output,'C',connessioneNeo)
    
    logging.critical(output)
    return jsonify(output) 
    

#########################################################################################################

#richiesta mongo cascata
@app.route('/selectmongocascata/<iatacode>', methods=['GET'])
#@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
def selectmongocascata(iatacode):
    #estrai il parametro in input con la request
    param = iatacode
    #apri connessione
    mongo = connessioneMongo
    dataset = mongo["aeroporti"]
    tabella = dataset["aeroporto"]
    #query
    myquery = { "IATA_CODE": param }
    
    results = tabella.find(myquery)

    #file json di output
    output={
        'resultPostgres': [],
        'resultDynamo': [],
        'resultCassandra': [],
    }

    #lista di appoggio per dynamo con la selezione di postgres
    appoggio=[]

    logging.critical('result di mongo...')
    logging.critical(results)
    #ora nel mio result io ho le ennuple con IATACODE (codice aereoporto), nome aeroporto ecc

    #interrogazione a postgres con  lo IATACODE dell'areoporto, mi restituirà tutti i voli che hanno come destinazione quell'areoporto 
    for destinazione in results:
        result=selectpostgresdestinazione(destinazione['IATA_CODE'])
        #if result not in output["resultPostgres"]: abbiamo eliminato il DISTINCT
        output["resultPostgres"].append(result)
        appoggio.append(result)
    
    #NB: POICHE' IN CASSANDRA NON POSSIAMO FARE QUERY CHE NON SIA SULLA CHIAVE
    #ALLORA DOBBIAMO PASSARE IN POSTGRES, CHIEDERE TUTTI I VOLI_ID DEI RISULTATI E PASSARLI A CASSANDRA
    for voloid in appoggio[0]:
        """ logging.critical(voloid[0]) #PRIMA ERA 5 """
        result=selectcassandra(voloid) #PRIMA ERA 5
        daCaricare = json.loads(result)
        """ logging.critical('result cassandra con id di postgres')
        logging.critical(daCaricare) """
        #if daCaricare not in output["resultCassandra"]: abbiamo eliminato il DISTINCT
        if daCaricare != []:
            if type(daCaricare[0]) == list:
                for l in daCaricare:
                    output["resultCassandra"].append(l)
            else:
                output["resultCassandra"].append(daCaricare)
    
    #NB: POICHE' DYNAMO CHE HA LE COMPAGNIE AEREE NON HA CONNESSIONI CON GLI AEROPORTI
    #ALLORA DOBBIAMO PASSARE IN POSTGRES, CHIEDERE IL RISULTATO TRAMITE LO IATA CODE 
    #E MANDIAMO A DYNAMO LA COMPAGNIA AEREA DEI VOLI RISULTANTI
    
    for compagniaid in appoggio[0]:
        """ logging.critical(compagniaid[1]) #PRIMA ERA 4 """
        result=selectdynamo(compagniaid[1]) #PRIMA ERA 4
        if result not in output["resultDynamo"]: # il DISTINCT
            output["resultDynamo"].append(result)

    logging.critical('Output',output)
    #PASSO DATI A NEO4J E STAMPO
    logging.critical('Caricamento dati in neo4j...')
    resultN4j = caricamentoNeo4j.neo4jElaborazione(output,'M',connessioneNeo)
    
    logging.critical(output)
    return jsonify(output) 

############################################################################################################################

#richiesta dynamo cascata
@app.route('/selectdynamocascata/<compagniaid>', methods=['GET'])
#@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
def selectdynamocascata(compagniaid):
    #connessione
    dynamodb = connessioneDynamo
    #parametro
    param=compagniaid
    table = dynamodb.Table("compagnieAeree")
    #query
    response = table.query(KeyConditionExpression= Key('compagnia_id').eq(param,))
    items = response.get('Items', [])
    logging.critical('stampa degli items risultato della compagnia')
    logging.critical(items)

    #file json di output
    output={
        'resultPostgres': [],
        'resultMongo': [],
        'resultCassandra': [],
    }

    #lista di appoggio per mongo con la selezione di postgres
    appoggio=[]

    logging.critical(items)
    #ora nel mio result io ho le ennuple con IATACODE (codice aereoporto), nome aeroporto ecc

    #interrogazione a postgres con  la compagnia aerea, mi restituirà tutti i voli che hanno come compagnia quella compagnia aerea passata in input
    for compagniaid in items:
        result=selectpostgrescompagniaid(compagniaid['compagnia_id'])
        #if result not in output["resultPostgres"]: abbiamo eliminato il DISTINCT
        output["resultPostgres"].append(result)
        appoggio.append(result)

    #NB: POICHE' IN CASSANDRA NON POSSIAMO FARE QUERY CHE NON SIA SULLA CHIAVE
    #ALLORA DOBBIAMO PASSARE IN POSTGRES, CHIEDERE TUTTI I VOLI_ID DEI RISULTATI E PASSARLI A CASSANDRA
    
    for voloid in appoggio[0]:
        """ logging.critical('lista di appoggio')
        logging.critical(voloid)
        logging.critical('sto stampando voloid 5')
        logging.critical(str(voloid[1])) """
        result=selectcassandra(voloid)
        daCaricare = json.loads(result)
        #if daCaricare not in output["resultCassandra"]: abbiamo eliminato il DISTINCT
        if type(daCaricare[0]) == list:
            for l in daCaricare:
                output["resultCassandra"].append(l)
        else:
            output["resultCassandra"].append(daCaricare)
    
    #NB: POICHE' MONGO CHE HA GLI AEROPORTI NON HA CONNESSIONI CON LE COMPAGNIE AEREE  
    #ALLORA DOBBIAMO PASSARE IN POSTGRES, CHIEDERE IL RISULTATO TRAMITE LA COMPAGNIA AEREA
    #E MANDIAMO A MONGO LO IATA CODE DEGLI AEREOPORTI DEI VOLI RISULTANTI (AEROPORTI DI DESTINAZIONE)
    for iatacode in appoggio[0]:
        result=selectmongo(iatacode[2])
        daCaricare = json.loads(result)
        #if daCaricare not in output["resultMongo"]: abbiamo eliminato il DISTINCT
        output["resultMongo"].append(daCaricare)

    #PASSO DATI A NEO4J E STAMPO
    logging.critical('Caricamento dati in neo4j...')
    resultN4j = caricamentoNeo4j.neo4jElaborazione(output,'D',connessioneNeo)
    
    logging.critical(output)
    return jsonify(output) 



############################ METODI QUERY SELEZIONI SINGOLE POSTGRES SU VARI PARAMETRI ##########################

#METODO semplice select postgres tramite Id_volo
def selectpostgresvoloid(voloid):
    param = voloid
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
    cursor.execute("SELECT volo_id, compagnia, destinazione, partenza_prevista FROM volitimes WHERE  volo_id= %s" , (param,))
    results = cursor.fetchall()
    cursor.close()
    return results


#METODO semplice select postgres tramite destinazione
def selectpostgresdestinazione(destinazione):
    param = destinazione
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
    cursor.execute("SELECT volo_id, compagnia, destinazione, partenza_prevista FROM volitimes WHERE destinazione= %s" , (param,))
    results = cursor.fetchall()
    cursor.close()
    return results



#richiesta postgres partenza prevista
@app.route('/selectpostgres/<partenzaPrevista>', methods=['GET'])
#@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
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
    cursor.execute("SELECT volo_id, compagnia, destinazione,partenza_prevista FROM volitimes WHERE partenza_prevista = %s" , (param,))
    results = cursor.fetchall()
    cursor.close()
    
    return jsonify(results)


#METODO semplice select postgres tramite compagniaid
def selectpostgrescompagniaid(compagniaid):
    param = compagniaid
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
    cursor.execute("SELECT volo_id, compagnia, destinazione,partenza_prevista FROM volitimes WHERE  compagnia= %s" , (param,))
    results = cursor.fetchall()
    cursor.close()
    return results




####################################### METODI QUERY SELEZIONI SINGOLE CASSANDRA, DYNAMO, MONGO ###################################

#richiesta cassandra
@app.route('/selectcassandra/<volo>', methods=['GET'])
#@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
def selectcassandra(volo):
    #estrai il parametro in input con la request
    idVolo = volo[0]
    compagnia = volo[1]
    destinazione = volo[2]
    #apri connessione
    session = connessioneCassandra
    session.execute('USE ProgettoBig')
    # Esecuzione della query con il parametro in input
    rows = session.execute('SELECT * FROM voliInt WHERE volo_id= %s AND compagnia= %s AND destinazione= %s',  (str(idVolo),str(compagnia),str(destinazione),))
    return json_util.dumps(rows)
    
#richiesta dynamo   
@app.route('/selectdynamo/<compagniaid>',methods=['GET'])
#@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
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
#@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
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


############################################# METODI TEST PER CONNESSIONE ########################################

#Gestione connessione Postgres
@app.route('/connPostgres',methods=['GET'])
#@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
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


# Gestione connessione Dynamo
@app.route('/connDynamo',methods=['GET'])
#@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
def connDynamo():
    #carichiamo il database con i csv in caricamentoPos e restituiamo tutte le tabelle
    dynamodb = connessioneDynamo
    #tables = list(dynamodb.tables.all())
    tabella = dynamodb.Table("compagnieAeree")
    response = tabella.scan()
    return jsonify(response)
    #return render_template('index.html', posts=tables)


# Gestione connessione Mongo
@app.route('/connMongo',methods=['GET'])
#@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
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

# Gestione connessione Neo4j
@app.route('/connNeo',methods=['GET'])
#@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
def connNeo():
    #connessione
    graph = connessioneNeo
    #query
    query = "MATCH (p:Person) RETURN p"
    result = graph.run(query)
    logging.critical(result)

    valRitorno = []
    for i in result:
        logging.critical(i)
        valRitorno.append(i)

    return jsonify(valRitorno)


# Gestione connessione Cassandra
@app.route('/connCassandra',methods=['GET'])
#@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
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
    
    # Gestione del caricamento dei dataset nel database Dynamo Db
@app.route('/caricamentoDynamo',methods=['GET'])
def caricamentoDynamoDB():
    dynamodb=caricamentoDy.caricamentoDynamo(connessioneDynamo)
    tabella = dynamodb.Table("compagnieAeree")
    response = tabella.scan()
    return jsonify(response)
    #return render_template('index.html', posts=tables)
    
    
    # Gestione del caricamento dei dataset nel database Mongo
@app.route('/caricamentoMongo',methods=['GET'])
def caricamentoMongoDB():
    # Carichiamo il database con i csv in caricamentoMongo e restituiamo tutti i nomi delle tabelle
    mongo = caricamentoMongo.caricamentoMon(connessioneMongo)
    mongo = connessioneMongo
    lista = mongo.list_database_names()
    return jsonify(lista)
    #return render_template('index.html',posts=lista)


@app.route('/fly.png')
def serve_image():
    # Specifica il percorso del file immagine
    image_path = './fly.png'  # Sostituisci con il percorso reale del tuo file immagine
    # Invia il file immagine al client
    return send_file(image_path, mimetype='image/png')

if __name__ == "__main__":
    #app.run(debug=True)
    serve(app, host="0.0.0.0", port=8080)
