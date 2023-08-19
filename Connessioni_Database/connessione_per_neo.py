from py2neo import Graph


graph = Graph("bolt://localhost:7687")

query = "MATCH (p:Person) RETURN p"
result = graph.run(query)

for record in result:
    print(record)
