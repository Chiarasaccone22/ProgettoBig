from py2neo import Graph, Node, Relationship


#Crea un'istanza dell'oggetto Graph specificando l'URL del server Neo4j corrispondente al tuo container Docker:
#Assicurati di specificare l'URL corretto del tuo server Neo4j, che potrebbe includere l'host, la porta e le eventuali credenziali di autenticazione.
graph = Graph("bolt://localhost:7687")

#Una volta stabilita la connessione, puoi eseguire query o operazioni sul database Neo4j. Ad esempio, puoi eseguire una semplice query per recuperare nodi o relazioni:
#Questo esempio esegue una query Cypher per selezionare i primi 5 nodi nel database e quindi li stampa a schermo.

person1 = Node("Person", name="John", age=30)
person2 = Node("Person", name="Alice", age=28)

knows = Relationship(person1, "KNOWS", person2, since=2010)

graph.create(person1)
graph.create(person2)
graph.create(knows)

query = "MATCH (p:Person) RETURN p"
result = graph.run(query)

for record in result:
    print(record)
