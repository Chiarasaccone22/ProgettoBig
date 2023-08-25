
def caricamentoPostgres(connessione):
    
    cursor = connessione.cursor()

    # Esecuzione della query per creare la tabella
    cursor.execute('DROP TABLE IF EXISTS voli; CREATE TABLE voli ( anno int, mese int, giorno int, giorno_settimana int, compagnia text, volo_id int, aeromobile text, origine text, destinazione text, partenza_prevista int, partenza int, decollo int, distanza int, atterraggio int, arrivo_previsto int, arrivo int, deviazione int, cancellato int, motivo_cancellazione text, ritardo_malfunzionamento int, ritardo_sicurezza int, ritardo_compagnia int, ritardo_aereo int, ritardo_maltempo int)')

    # Caricamento dei dati dal file CSV nella tabella
    with open('./timestamp_1000.csv', 'r') as f:
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