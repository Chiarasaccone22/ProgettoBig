from flask import Flask, render_template
from waitress import serve
import psycopg2

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT']=0

@app.route('/')
def index():

    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        user="postgres",
        password="password",
        database="postgres"
    )

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts")
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('index.html', posts=results)

if __name__ == "__main__":
    app.run(debug=True)
    serve(app, host="0.0.0.0", port=8080)
