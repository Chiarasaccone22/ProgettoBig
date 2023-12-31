
from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, config

grafo= config.DATABASE_URL = 'bolt://neo4j:password@localhost:7687' 

class Book(StructuredNode):
    title = StringProperty(unique_index=True)
    author = RelationshipTo('Author', 'AUTHOR')

class Author(StructuredNode):
    name = StringProperty(unique_index=True)
    books = RelationshipFrom('Book', 'AUTHOR')

harry_potter = Book(title='Harry potter and the..').save()
rowling =  Author(name='J. K. Rowling').save()
harry_potter.author.connect(rowling)

query = "MATCH (a:Author) RETURN a"
result = grafo.run(query)

for record in result:
    print(record)
