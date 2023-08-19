#per prima cosa: pip install boto3
import boto3

#https://www.honeybadger.io/blog/using-dynamodb-with-python/

#Creeremo una tabella utilizzando la create_tablefunzione Dynamo. Qui chiamiamo la tabella "Libri".

#Questa tabella conterrà gli attributi per la chiave di partizione e la chiave di ordinamento. 
#Il " titolo " del libro sarà la nostra chiave di ordinamento e il " book_id " sarà la nostra chiave di partizione.

#Una chiave di ordinamento è un campo in un database che indica 
#l'ordine in cui i dati vengono archiviati (in ordine ordinato in base al valore della chiave di ordinamento). 
#In DynamoDB, la chiave di ordinamento per ogni campo è univoca.

#La chiave di partizione è l'attributo che identifica un elemento in un database. 
#I dati con la stessa chiave di partizione vengono archiviati insieme per consentire di eseguire query sui dati. 
#I dati di una chiave di partizione vengono ordinati utilizzando la chiave di ordinamento.



#dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

def create_books_table(dynamodb=None):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.create_table(
        TableName='Books',
        KeySchema=[
            {
                'AttributeName': 'book_id',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'title',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'book_id',
                # AttributeType refers to the data type 'N' for number type and 'S' stands for string type.
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'title',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            # ReadCapacityUnits set to 10 strongly consistent reads per second
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10  # WriteCapacityUnits set to 10 writes per second
        }
    )
    return table

if __name__ == '__main__':
    book_table = create_books_table()
    print("Status:", book_table.table_status)

#Nel codice sopra, abbiamo creato una tabella denominata Books ; book_idè la chiave di partizione e il titolo è la chiave di ordinamento. 
#Successivamente, abbiamo definito la nostra tabella dichiarando uno schema chiave memorizzato nella KeySchemavariabile.
#Abbiamo anche dichiarato i tipi di dati degli attributi. Dove "N" rappresenta un numero e "S" rappresenta una stringa, 
# abbiamo anche aggiunto la ProvisionedThroughputvariabile per ridurre il numero di operazioni di " lettura " e "scrittura" sul database al secondo.
# 'Infine, nell'ultima sezione del frammento di codice, abbiamo creato un'istanza della nostra classe.

