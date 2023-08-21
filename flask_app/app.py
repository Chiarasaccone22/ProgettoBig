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
#ora che abbiamo la lista python di posts, che sarebbero le ennuple del nostro database, dobbiamo passare la lista posts nel template html per il collegamento
#per aggiungere un qualsiasi oggetto e passarlo al tamplate html basta passarlo come argomento della funzione render_template : posts=posts dove il primo è il nome con cui lo accediamo in html e il secondo è ciò che abbiamo creato qui
#per il tamplate html
    return render_template('index.html')

if __name__ == "__main__":
    #app.run(debug=True)
    serve(app, host="0.0.0.0", port=8080)
