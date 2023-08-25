import csv


def caricamentodb(connessione):
    # connessione a cassandra
    session = connessione
    """  # imposto ambiente di lavoro dove sono la table
    # Query per verificare l'esistenza di un keyspace
    keyspace_name = "ProgettoBig"
    query = f"SELECT keyspace_name FROM system_schema.keyspaces WHERE keyspace_name = '{keyspace_name}'"
    result = session.execute(query)

    if not(result.one()):
        query = f"CREATE KEYSPACE {keyspace_name} WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': 1}}"
        session.execute(query)
    query = f"USE {keyspace_name}"
    session.execute(query) """

    session.execute('USE ProgettoBig')
    # se non c'è crea table altrimenti mantiene
    session.execute('CREATE TABLE IF NOT EXISTS volint (anno int, mese int, giorno int, giorno_settimana int, compagnia text, volo_id int, aeromobile text, origine text, destinazione text, ritardo_partenza int, transito_pista_decollo int, durata_prevista int, durata int, tempo_volo int, distanza int, transito_pista_atterraggio int, ritardo_arrivo int, deviazione int, cancellato int, motivo_cancellazione text, ritardo_malfunzionamento int, ritardo_sicurezza int, ritardo_compagnia int, ritardo_aereo int, ritardo_maltempo int, PRIMARY KEY(volo_id))')
 
    """  with open('./intervalli_1000.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)     """    # Salta la riga dell'intestazione
        
    """ for line in range(24):
            #data = line.strip().split(',')
            listacolonne.append(csv_reader[line])
            #data = [int(x) if x.isdigit() else x for x in data]
            query = "INSERT INTO volint (anno, mese, giorno, giorno_settimana, compagnia, volo_id, aeromobile, origine, destinazione, ritardo_partenza, transito_pista_decollo, durata_prevista, durata, tempo_volo, distanza, transito_pista_atterraggio, ritardo_arrivo, deviazione, cancellato, motivo_cancellazione, ritardo_malfunzionamento, ritardo_sicurezza, ritardo_compagnia, ritardo_aereo, ritardo_maltempo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            session.execute(query, data) """

    # legge file csv
    csv_file_path = './intervalli_1000.csv'
    # scorre file csv
    with open(csv_file_path, 'r') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)  # Salta la riga dell'intestazione

        for row in csv_reader:
            anno=row[0]
            mese= row[1]
            giorno= row[2]
            giorno_settimana= row[3]
            compagnia= row[4]
            volo_id= row[5]
            aeromobile=row[6]
            origine=row[7]
            destinazione=row[8]
            ritardo_partenza=row[9]
            transito_pista_decollo=row[10]
            durata_prevista=row[11]
            durata=row[12]
            tempo_volo=row[13]
            distanza=row[14]
            transito_pista_atterraggio=row[15]
            ritardo_arrivo=row[16]
            deviazione=row[17]
            cancellato= row[18]
            motivo_cancellazione=row[19]
            ritardo_malfunzionamento= row[20]
            ritardo_sicurezza= row[21]
            ritardo_compagnia= row[22]
            ritardo_aereo= row[23]
            ritardo_maltempo=row[24]
            

            query = f"INSERT INTO volint (anno, mese, giorno, giorno_settimana, compagnia, volo_id, aeromobile, origine, destinazione, ritardo_partenza, transito_pista_decollo, durata_prevista, durata, tempo_volo, distanza, transito_pista_atterraggio, ritardo_arrivo, deviazione, cancellato, motivo_cancellazione, ritardo_malfunzionamento, ritardo_sicurezza, ritardo_compagnia, ritardo_aereo, ritardo_maltempo) VALUES (%i, %i, %i, %i, %s, %i, %s, %s, %s, %i, %i, %i, %i, %i, %i, %i, %i, %i, %i, %s, %i, %i, %i, %i, %i)"  # Sostituisci con il nome della tua tabella e le colonne corrispondenti
            session.execute(query, (anno, mese, giorno, giorno_settimana, compagnia, volo_id, aeromobile, origine, destinazione, ritardo_partenza, transito_pista_decollo, durata_prevista, durata, tempo_volo, distanza, transito_pista_atterraggio, ritardo_arrivo, deviazione, cancellato, motivo_cancellazione, ritardo_malfunzionamento, ritardo_sicurezza, ritardo_compagnia, ritardo_aereo, ritardo_maltempo))  # Sostituisci con i valori da inserire



    """ # legge file csv
    csv_file_path = './intervalli_1000.csv'
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
 """
    #cluster.shutdown()
    return session