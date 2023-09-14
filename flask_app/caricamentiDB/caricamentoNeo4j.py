import logging
from py2neo import Graph, Node, Relationship
from flask import jsonify

# Gestione connessione Neo4j
#@app.route('/neo4j',methods=['GET'])
def neo4jElaborazione(output,strMetodo,connessioneNeo):
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
                        arco = Relationship(nodeCList[c],'compagnia_volo',nodeDList[d])
                        graph.create(arco)
  
            

    elif strMetodo == 'D':
        logging.critical('DATI PER NEO4J:')
        logging.critical(datiDb)

        # prendo i dati di postgres
        for p in datiDb[0][0]:
            postgresDati.append(p)
            # creare nodi e connessioni
            compagnia = p[1]
            logging.critical('COMPAGNIA:')
            logging.critical(compagnia)
            nodeP = Node("COMPAGNIA",compagnia=compagnia)
            graph.create(nodeP)
            nodePList.append(nodeP)

        # prendo i dati di mongo 
        for m in datiDb[1]:
            mongoDati.append(m[0])
            # creare nodi e connessioni
            airport = m[0]['IATA_CODE']
            logging.critical('IATA_CODE:')
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

        for p in range(len(postgresDati)):
            iatacodeP = postgresDati[p][2]
            idvolo = postgresDati[p][0]
            logging.critical('iatacode')
            logging.critical(iatacodeP)
            for c in range(len(cassandraDati)):
                logging.critical('c[0]')
                logging.critical(cassandraDati[c][0])
                if cassandraDati[c][0] == idvolo:
                    logging.critical('creo arco')
                    arco = Relationship(nodePList[p],'compagnia_volo',nodeCList[c])
                    graph.create(arco)
            for m in range(len(mongoDati)):
                iatacode = mongoDati[m]['IATA_CODE']
                logging.critical('iatacode')
                logging.critical(iatacode)
                if iatacode == iatacodeP:
                    logging.critical('creo arco')
                    arco = Relationship(nodeMList[m],'aeroporto_compagnia',nodePList[p])
                    graph.create(arco)

    elif strMetodo == 'M':
        logging.critical('DATI PER NEO4J:')
        logging.critical(datiDb)

        # prendo i dati di postgres
        for p in datiDb[0][0]:
            logging.critical('p')
            logging.critical(p)
            
            # creare nodi e connessioni
            partenza = p[2]
            logging.critical('AEROPORTO:')
            logging.critical(partenza)
            nodeP = Node("AEROPORTO",aeroporto=partenza)
            if nodePList ==[]:
                graph.create(nodeP)
                nodePList.append(nodeP)
                postgresDati.append(p)
            else:
                for k in nodePList:
                    if k['aeroporto'] != partenza:
                        graph.create(nodeP)
                        nodePList.append(nodeP)
                        postgresDati.append(p)

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
        logging.critical(postgresDati)
        logging.critical(cassandraDati)
        logging.critical(dynamoDati)

        for p in range(len(postgresDati)):
            iatacode = postgresDati[p][2]
            logging.critical('iatacode')
            logging.critical(iatacode)
            for c in range(len(cassandraDati)):
                logging.critical('c[2]')
                logging.critical(cassandraDati[c][2])
                logging.critical('c[1]')
                logging.critical(cassandraDati[c][1])
                for d in range(len(dynamoDati)):
                    compagniaId = dynamoDati[d]['compagnia_id']
                    logging.critical('compagnia_id')
                    logging.critical(compagniaId)
                    if cassandraDati[c][1] == compagniaId:
                        logging.critical('creo arco')
                        arco = Relationship(nodeDList[d],'compagnia_volo',nodeCList[c])
                        graph.create(arco)
                    if cassandraDati[c][2] == iatacode:
                        logging.critical('creo arco')
                        arco = Relationship(nodePList[p],'aeroporto_compagnia',nodeDList[d])
                        graph.create(arco)

    elif strMetodo == 'C':
        logging.critical('DATI PER NEO4J:')
        logging.critical(datiDb)

        # prendo i dati di postgres
        for p in datiDb[0][0]:
            postgresDati.append(p)
            # creare nodi e connessioni
            voloid = p[0]
            logging.critical('volo_id:')
            logging.critical(voloid)
            nodeP = Node("VOLO_ID",voloid=voloid)
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
            airport = m[0]['IATA_CODE']
            logging.critical('AIRPORT:')
            logging.critical(airport)
            nodeM = Node("AEROPORTO", aeroporto=airport)
            graph.create(nodeM)
            nodeMList.append(nodeM)


        for p in range(len(postgresDati)):
            compagnia = postgresDati[p][1]
            iatacode = postgresDati[p][2]
            logging.critical('compagnia postgres')
            logging.critical(compagnia)
            logging.critical('iatacode postgres')
            logging.critical(iatacode)
            for d in range(len(dynamoDati)):
                compagniaD = dynamoDati[d]['compagnia_id']
                logging.critical('compagnia dynamo')
                logging.critical(compagniaD)
                if compagnia == compagniaD:
                    logging.critical('mettiamo arco')
                    arco = Relationship(nodeDList[d],'compagnia_volo',nodePList[p])
                    graph.create(arco)
            for m in range(len(mongoDati)):
                iatacodeM = mongoDati[m]['IATA_CODE']
                logging.critical('iatacode mongo')
                logging.critical(iatacodeM)
                if iatacodeM == iatacode:
                    arco = Relationship(nodePList[p],'volo_aeroporto',nodeMList[m])
                    graph.create(arco)



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