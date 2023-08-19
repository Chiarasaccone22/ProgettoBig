import pymongo

connessione = pymongo.MongoClient("mongodb://localhost:27017/")
print(connessione.list_database_names())