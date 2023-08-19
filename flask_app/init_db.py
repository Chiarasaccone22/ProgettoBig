import sqlite3
#qui è con il file di estensione .db
connection=sqlite3.connect('database.db')
with open('crea_posts.sql') as f:
    connection.executescript(f.read())
#ora salviamo le modifiche al file con commit
connection.commit()
connection.close()