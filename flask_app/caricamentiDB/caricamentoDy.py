
import boto3
import pandas as pd

#https://www.honeybadger.io/blog/using-dynamodb-with-python/

#Creeremo una tabella utilizzando la create_tablefunzione Dynamo.

#Questa tabella conterrà gli attributi per la chiave di partizione e la chiave di ordinamento. 
#Il " titolo " del libro sarà la nostra chiave di ordinamento e il " book_id " sarà la nostra chiave di partizione.

#Una chiave di ordinamento è un campo in un database che indica 
#l'ordine in cui i dati vengono archiviati (in ordine ordinato in base al valore della chiave di ordinamento). 
#In DynamoDB, la chiave di ordinamento per ogni campo è univoca.

#La chiave di partizione è l'attributo che identifica un elemento in un database. 
#I dati con la stessa chiave di partizione vengono archiviati insieme per consentire di eseguire query sui dati. 
#I dati di una chiave di partizione vengono ordinati utilizzando la chiave di ordinamento.

def caricamentoDynamo(connessione):
    dynamodb = connessione

    table_name='CompagnieAeree'

    # Controlla se la tabella esiste già
    # Ottieni la lista delle tabelle
    tables = list(dynamodb.tables.all())

    # Estrai i nomi delle tabelle dalla lista di oggetti Table
    table_names = [table.name for table in tables]
    print(table_names)
    print(table_name)

    #Se la tabella non esiste la crei e poi inserisci il contenuto del file csv
    if table_name not in table_names:

        table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'compagnia_id',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'name',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'compagnia_id',
                # AttributeType refers to the data type 'N' for number type and 'S' stands for string type.
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'name',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            # ReadCapacityUnits set to 10 strongly consistent reads per second
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10  # WriteCapacityUnits set to 10 writes per second
        }
    )

    #se invece la tabella già esiste si salta la creazione e inserisce direttamente i dati del file csv dentro la tabella 

    # Importa dati dal file CSV

    # Leggi il file CSV utilizzando pandas
    csv_file = '/home/chiara/Documenti/GitHub/ProgettoBig/flask_app/dataset/airlines.csv'
    data = pd.read_csv(csv_file)

    # Itera attraverso le righe del DataFrame e inserisci i dati in DynamoDB
    for index, row in data.iterrows():
        item = {
            'compagnia_id': str(row['compagnia_id']),  # Sostituisci con il nome della chiave primaria
            'name': str(row['name']),         # Sostituisci con i nomi degli attributi
            }
        
        # Inserisci l'elemento nella tabella DynamoDB
        
        table=dynamodb.Table(table_name)
        table.put_item(Item=item)
    return dynamodb


if __name__ == '__main__':
    tabella = caricamentoDynamo()
    print("Status:", tabella.table_status)
