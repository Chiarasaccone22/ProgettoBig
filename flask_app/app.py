from flask import Flask, render_template
from waitress import serve
import psycopg2
import boto3

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT']=0

@app.route('/connPostgres')
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

@app.route('/')
#funzione che gestisce la home page
def connDynamo():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Books')
    #Esegui una query sulla tabella utilizzando il titolo come chiave
    response = table.query(
        KeyConditionExpression= "book_id= :book_id",
        ExpressionAttributeValues= {
            ":book_id": {"N": "3"}
            } 
)



    items = response['Items']

    return render_template('index.html', posts=items)

if __name__ == "__main__":
    app.run(debug=True)
    serve(app, host="0.0.0.0", port=8080)
