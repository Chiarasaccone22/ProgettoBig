from flask import Flask, render_template,jsonify,Response, redirect, url_for,  request
from waitress import serve
from py2neo import Graph, Node, Relationship
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
import json

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT']=0
logging.basicConfig(level=logging.INFO)

#creiamo variabili globali di connessione inizializzandole 

connessioneMongo= pymongo.MongoClient("mongodb://mongoDb:27017/") 

connessioneNeo=Graph("bolt://neo4jDbGUI:7687")

connessioneCassandra=Cluster(['cassandraDb'], port=9042).connect()

connessioneDynamo= boto3.resource('dynamodb',endpoint_url='http://dynamoDbGUI:8000',region_name='us-east-1')

@app.after_request
def add_csp_headers(response):
    """ response.headers['Access-Control-Allow-Origin'] = '*'  # '*' consente a qualsiasi dominio di accedere, ma è possibile specificare un dominio specifico
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type' """
    response.headers['Content-Security-Policy'] = "frame-ancestors 'self' http://localhost:7474/;"
    return response

#apertura di default
@app.route('/')
def index():
    logging.debug('Apro le connessioni...')
    return render_template('index.html')




# Gestione connessione Neo4j
#@app.route('/neo4j',methods=['GET'])
def neo4jElaborazione(output,strMetodo):
    #connessione
    graph = connessioneNeo
    
     #ripulisco tutto
    logging.critical('Ripolisco tutto neo4j...')
    query = "MATCH (n) DETACH DELETE n;"
    graph.run(query)


    # metto i dati del json in un array coì mi separo dalle key
    datiDb = []
    for key in output:
        datiDb.append(output[key])

    # in ognuna lista metto tutti i relativi dati perchè ci sono tanti impacchettamenti
    # potrei anche cancellarli per il momento li lascio
    postgresDati = []
    mongoDati = []
    dynamoDati = []
    cassandraDati = []

    # qui metto i nodi che creo in neo4j perchè poi mi servono per farvi le connessioni
    nodeCList = []
    nodeDList = []
    nodePList = []
    nodeMList = []
    i = 0

    # Dati spacchettati in base al metodo che li manda
    if strMetodo == 'P':
        
        # prendo i dati di mongo
        for m in datiDb[0]:
            mongoDati.append(m[0])
            # creare nodi e connessioni
            airport = m[0]['AIRPORT']
            logging.critical('AIRPORT:')
            logging.critical(airport)
            nodeM = Node("AEROPORTO", aeroporto=airport)
            graph.create(nodeM)
            nodeMList.append(nodeM)

        # prendo i dati di dynamo
        for d in datiDb[1]:
            dynamoDati.append(d[0])
            # creare nodi e connessioni
            cid = d[0]['compagnia_id']
            logging.critical('compagnia_id:')
            logging.critical(cid)
            nodeD = Node("COMPAGNIA_ID", compagnia_id=cid)
            graph.create(nodeD)
            nodeDList.append(nodeD)

        # prendo i dati di cassandra
        for c in datiDb[2]:
            cassandraDati.append(c)
            # creare nodi e connessioni
            zero = c[0]
            logging.critical('zero:')
            logging.critical(zero)
            nodeC = Node("ID_VOLO", idvolo=zero)
            graph.create(nodeC)
            nodeCList.append(nodeC)

   
        logging.critical('creazione archi')
        logging.critical(mongoDati)
        logging.critical(cassandraDati)
        logging.critical(dynamoDati)

        for m in range(len(mongoDati)):
            iatacode = mongoDati[m]['IATA_CODE']
            logging.critical('iatacode')
            logging.critical(iatacode)
            for c in range(len(cassandraDati)):
                logging.critical('c[2]')
                logging.critical(cassandraDati[c][2])
                logging.critical('c[1]')
                logging.critical(cassandraDati[c][1])
                if cassandraDati[c][2] == iatacode:
                    logging.critical('creo arco')
                    arco = Relationship(nodeMList[m],'aeroporto_compagnia',nodeCList[c])
                    graph.create(arco)
                for d in range(len(dynamoDati)):
                    compagniaId = dynamoDati[d]['compagnia_id']
                    logging.critical('compagnia_id')
                    logging.critical(compagniaId)
                    if cassandraDati[c][1] == compagniaId:
                        logging.critical('creo arco')
                        arco = Relationship(nodeCList[m],'compagnia_volo',nodeDList[d])
                        graph.create(arco)
  
            

    elif strMetodo == 'D':
        logging.critical('DATI PER NEO4J:')
        logging.critical(datiDb)

        # prendo i dati di postgres
        for p in datiDb[0]:
            postgresDati.append(p[0][9])
            # creare nodi e connessioni
            partenza = p[0][9]
            logging.critical('PARTENZA:')
            logging.critical(partenza)
            nodeP = Node("PARTENZA_PREVISTA",partenza_prevista=partenza)
            graph.create(nodeP)
            nodePList.append(nodeP)



        # prendo i dati di mongo 
        for m in datiDb[1]:
            mongoDati.append(m[0])
            # creare nodi e connessioni
            airport = m[0]['AIRPORT']
            logging.critical('AIRPORT:')
            logging.critical(airport)
            nodeM = Node("AEROPORTO", aeroporto=airport)
            graph.create(nodeM)
            nodeMList.append(nodeM)

        # prendo i dati di cassandra
        for c in datiDb[2]:
            cassandraDati.append(c)
            # creare nodi e connessioni
            zero = c[0]
            logging.critical('zero:')
            logging.critical(zero)
            nodeC = Node("ID_VOLO", idvolo=zero)
            graph.create(nodeC)
            nodeCList.append(nodeC)

    elif strMetodo == 'M':
        logging.critical('DATI PER NEO4J:')
        logging.critical(datiDb)

        # prendo i dati di postgres
        for p in datiDb[0]:
            postgresDati.append(p[0][9])
            # creare nodi e connessioni
            partenza = p[0][9]
            logging.critical('PARTENZA:')
            logging.critical(partenza)
            nodeP = Node("PARTENZA_PREVISTA",partenza_prevista=partenza)
            graph.create(nodeP)
            nodePList.append(nodeP)

        # prendo i dati di dynamo
        for d in datiDb[1]:
            dynamoDati.append(d[0])
            # creare nodi e connessioni
            cid = d[0]['compagnia_id']
            logging.critical('compagnia_id:')
            logging.critical(cid)
            nodeD = Node("COMPAGNIA_ID", compagnia_id=cid)
            graph.create(nodeD)
            nodeDList.append(nodeD)

        # prendo i dati di cassandra
        for c in datiDb[2]:
            cassandraDati.append(c)
            # creare nodi e connessioni
            zero = c[0]
            logging.critical('zero:')
            logging.critical(zero)
            nodeC = Node("ID_VOLO", idvolo=zero)
            graph.create(nodeC)
            nodeCList.append(nodeC)

    elif strMetodo == 'C':
        logging.critical('DATI PER NEO4J:')
        logging.critical(datiDb)

        # prendo i dati di postgres
        for p in datiDb[0]:
            postgresDati.append(p[0][9])
            # creare nodi e connessioni
            partenza = p[0][9]
            logging.critical('PARTENZA:')
            logging.critical(partenza)
            nodeP = Node("PARTENZA_PREVISTA",partenza_prevista=partenza)
            graph.create(nodeP)
            nodePList.append(nodeP)

        # prendo i dati di dynamo
        for d in datiDb[1]:
            dynamoDati.append(d[0])
            # creare nodi e connessioni
            cid = d[0]['compagnia_id']
            logging.critical('compagnia_id:')
            logging.critical(cid)
            nodeD = Node("COMPAGNIA_ID", compagnia_id=cid)
            graph.create(nodeD)
            nodeDList.append(nodeD)

        # prendo i dati di mongo
        for m in datiDb[2]:
            mongoDati.append(m[0])
            # creare nodi e connessioni
            airport = m[0]['AIRPORT']
            logging.critical('AIRPORT:')
            logging.critical(airport)
            nodeM = Node("AEROPORTO", aeroporto=airport)
            graph.create(nodeM)
            nodeMList.append(nodeM)


    logging.critical('Metodo:')
    logging.critical(strMetodo)
    logging.critical('DATI POSTGRES PER NEO4J:')
    logging.critical(postgresDati)
    logging.critical('DATI DYNAMO PER NEO4J:')
    logging.critical(dynamoDati)
    logging.critical('DATI MONGO PER NEO4J:')
    logging.critical(mongoDati)
    logging.critical('DATI CASSANDRA PER NEO4J:')
    logging.critical(cassandraDati)


    #query inserimento per visualizzazione
    # potremmo togliere non serve
    query = "MATCH (n) OPTIONAL MATCH (n)-[r]-() RETURN n, r;"
    result = graph.run(query)

    #logging.critical(result)

    # anche queto non serve
    valRitorno = []
    for i in result:
        #logging.critical(i)
        valRitorno.append(i)
    
    #logging.critical(valRitorno)
    return jsonify(valRitorno)


#########################################################################


#richiesta postgres cascata
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
        'resultMongo': [],#cursor.execute("SELECT * FROM volitimes WHERE partenza_prevista = %s" , (param,))
        'resultDynamo': [],
        'resultCassandra': [],

    }

    logging.critical(results)
    #interrogazione a cassandra con il volo_id
    for volo in results:
            result=selectcassandra(volo[0])
            result = json.loads(result)
            logging.critical('con 612 devono essere 2')
            logging.critical(result)
            #if result not in output["resultCassandra"]: abbiamo eliminato il DISTINCT
            if type(result[0]) == list:
                for l in result:
                    output["resultCassandra"].append(l)
            else:
                output["resultCassandra"].append(result)

    #interrogazione a dynamo con la compagnia aerea
    for compagniaid in results:
            result=selectdynamo(compagniaid[1])
            #if result not in output["resultDynamo"]: abbiamo eliminato il DISTINCT
            output["resultDynamo"].append(result)

    #interrogazione a mongo con l'areoporto di destinazione
    for iatacode in results:
            result=selectmongo(iatacode[2])
            result = json.loads(result)
            logging.critical(result)
            logging.critical(type(result))
            #if result not in output["resultMongo"]: abbiamo eliminato il DISTINCT
            output["resultMongo"].append(result)
    
    #PASSO DATI A NEO4J E STAMPO
    logging.critical('Caricamento dati in neo4j...')
    resultN4j = neo4jElaborazione(output,'P')

    logging.critical(output)
    return jsonify(output) 
   
################################################################

#richiesta cassandra cascata
@app.route('/selectcassandracascata/<idvolo>', methods=['GET'])
def selectcassandracascata(idvolo):
    #estrai il parametro in input con la request
    param = idvolo
    #apri connessione
    session = connessioneCassandra
    session.execute('USE ProgettoBig')
    # Esecuzione della query con il parametro in input
    rows= session.execute('SELECT volo_id, compagnia, destinazione FROM voliInt WHERE volo_id=%s',  (param,))
    

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
    resultPostgres=selectpostgresvoloid(idvolo)
    logging.critical(resultPostgres)
    output["resultPostgres"].append(resultPostgres)

    #interrogazione a mongo con (l'areoporto di destinazione, no iatacode che devo prendere in postgres)
    for r in rows:
        logging.critical('R.')
        logging.critical(r)
        resultMongo=selectmongo(r[2])
        daCaricare = json.loads(resultMongo)
        #if daCaricare not in output["resultMongo"]:  abbiamo eliminato il DISTINCT
        output["resultMongo"].append(daCaricare)

        resultDynamo=selectdynamo(r[1])
        #if resultDynamo not in output["resultDynamo"]: abbiamo eliminato il DISTINCT
        output["resultDynamo"].append(resultDynamo)

    logging.critical('Caricamento dati in neo4j...')
    resultN4j = neo4jElaborazione(output,'C')
    
    logging.critical(output)
    return jsonify(output) 
    
#######################################################################
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
    cursor.execute("SELECT volo_id, compagnia, destinazione FROM volitimes WHERE  volo_id= %s" , (param,))
    results = cursor.fetchall()
    cursor.close()
    return results


#########################################################################
#richiesta mongo cascata
@app.route('/selectmongocascata/<iatacode>', methods=['GET'])
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
        logging.critical(voloid[0]) #PRIMA ERA 5
        result=selectcassandra(str(voloid[0])) #PRIMA ERA 5
        daCaricare = json.loads(result)
        #if daCaricare not in output["resultCassandra"]: abbiamo eliminato il DISTINCT
        if type(daCaricare[0]) == list:
            for l in daCaricare:
                output["resultCassandra"].append(l)
        else:
            output["resultCassandra"].append(daCaricare)
    
    #NB: POICHE' DYNAMO CHE HA LE COMPAGNIE AEREE NON HA CONNESSIONI CON GLI AEROPORTI
    #ALLORA DOBBIAMO PASSARE IN POSTGRES, CHIEDERE IL RISULTATO TRAMITE LO IATA CODE 
    #E MANDIAMO A DYNAMO LA COMPAGNIA AEREA DEI VOLI RISULTANTI
    
    for compagniaid in appoggio[0]:
        logging.critical(compagniaid[1]) #PRIMA ERA 4
        result=selectdynamo(compagniaid[1]) #PRIMA ERA 4
        #if result not in output["resultDynamo"]: abbiamo eliminato il DISTINCT
        output["resultDynamo"].append(result)

    logging.critical('Output',output)
    #PASSO DATI A NEO4J E STAMPO
    logging.critical('Caricamento dati in neo4j...')
    resultN4j = neo4jElaborazione(output,'M')
    
    logging.critical(output)
    return jsonify(output) 

########################################################################

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
    cursor.execute("SELECT volo_id, compagnia, destinazione FROM volitimes WHERE destinazione= %s" , (param,))
    results = cursor.fetchall()
    cursor.close()
    return results


#########################################################################

#richiesta dynamo cascata
@app.route('/selectdynamocascata/<compagniaid>', methods=['GET'])
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
        logging.critical('lista di appoggio')
        logging.critical(voloid)
        logging.critical('sto stampando voloid 5')
        logging.critical(str(voloid[1]))
        result=selectcassandra(str(voloid[1]))
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
    resultN4j = neo4jElaborazione(output,'D')
    
    logging.critical(output)
    return jsonify(output) 



#########################################################################
#richiesta postgres partenza prevista
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
    results = cursor.fetchall()
    cursor.close()
    
    return jsonify(results)

#########################################################################


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
    cursor.execute("SELECT volo_id, compagnia, destinazione FROM volitimes WHERE  compagnia= %s" , (param,))
    results = cursor.fetchall()
    cursor.close()
    return results


#########################################################################

#richiesta cassandra
@app.route('/selectcassandra/<idvolo>', methods=['GET'])
def selectcassandra(idvolo):
    #estrai il parametro in input con la request
    idVolo = idvolo
    #apri connessione
    session = connessioneCassandra
    session.execute('USE ProgettoBig')
    # Esecuzione della query con il parametro in input
    rows = session.execute('SELECT * FROM voliInt WHERE volo_id= %s',  (str(idVolo),))
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
    logging.critical(result)

    valRitorno = []
    for i in result:
        logging.critical(i)
        valRitorno.append(i)

    return jsonify(valRitorno)


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



if __name__ == "__main__":
    #app.run(debug=True)
    serve(app, host="0.0.0.0", port=8080)
