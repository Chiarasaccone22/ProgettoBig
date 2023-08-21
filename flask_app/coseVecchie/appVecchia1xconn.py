from flask import Flask, render_template
from waitress import serve
import sqlite3
import psycopg2

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT']=0

@app.route('/')
#funzione che gestisce la home page
def index():
#connessione tra database e pagina web
    connection=sqlite3.connect('database.db')
    connection.row_factory= sqlite3.Row #ho messo .row perchè la connessione al database è organizzata in righe e infatti il nostro database è fatto dalle ennuple
    posts=connection.execute('SELECT * FROM posts').fetchall() #.fetchall fa in modo che le ennuple siano organizzate in una lista python semplice
    connection.close()

#ora che abbiamo la lista python di posts, che sarebbero le ennuple del nostro database, dobbiamo passare la lista posts nel template html per il collegamento
#per aggiungere un qualsiasi oggetto e passarlo al tamplate html basta passarlo come argomento della funzione render_template : posts=posts dove il primo è il nome con cui lo accediamo in html e il secondo è ciò che abbiamo creato qui
#per il tamplate html
    return render_template('index.html', posts=posts)

#connessione postgres tramite codice py conessione fatto per docker
""" @app.route('/connectionpostgres')
def connection():
   


    conn = psycopg2.connect(
    host="localhost",
    port="5432",
    user="postgres",
    password="password",
    database="postgres"
)

    cursor = conn.cursor()
    cursor.execute("CREATE TABLE posts ( titolo TEXT, info TEXT)")
    results = cursor.fetchall()

    for row in results:
        print(row)

    cursor.close()
    conn.close()
 """

if __name__ == "__main__":
    app.run(debug=True)
    serve(app, host="0.0.0.0", port=8080)
