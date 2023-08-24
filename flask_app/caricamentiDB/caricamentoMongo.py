import pandas as pd

# Gestione del caricamento dei dataset nel database Mongo

def caricamentoMon(connessione):
    # connessione al db
    mongo = connessione
    
    # database e collezione li ho creati mediante l'interfaccia mongoGUI
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

    return mongo
