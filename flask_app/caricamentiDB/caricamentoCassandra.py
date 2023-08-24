import csv

def caricamentodb(connessione):
    # connessione a cassandra
    session = connessione
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

    #cluster.shutdown()
    return session