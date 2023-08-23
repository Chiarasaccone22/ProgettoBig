from cassandra.cluster import Cluster

cluster = Cluster(['192.168.16.2'], port=9042)
session = cluster.connect()

session.execute('USE cityinfo')
session.execute('CREATE TABLE prova (id int,PRIMARY KEY(id))')
rows = session.execute('INSERT INTO prova (id) VALUES (0)')
rows = session.execute('SELECT * FROM prova')
for row in rows:
    print(row.id)
#session.execute('DROP TABLE prova')