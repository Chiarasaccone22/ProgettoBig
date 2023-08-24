
def caricamentoPostgres(connessione):
    
    cursor = connessione.cursor()

    # Esecuzione della query per creare la tabella
    cursor.execute('DROP TABLE IF EXISTS voli; CREATE TABLE voli ( colonna1 text,colonna2 text)')

    # Caricamento dei dati dal file CSV nella tabella
    with open('./airlines.csv', 'r') as f:
        next(f)  # Salta la riga dell'intestazione
        print('inserisco...')
        cursor.copy_from(f, 'voli', sep=',', null='')  # Copia i dati nel database

    # Commit delle modifiche 
    connessione.commit()
    
    #query
    cursor.execute("SELECT * FROM voli")
   
    # mi da tutte le ennuple come righe
    results = cursor.fetchall()
   
    """ # chiudo connessione
    cursor.close()
    conn.close() """

    return connessione