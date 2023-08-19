from flask import Flask, render_template
from waitress import serve

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT']=0

@app.route('/')
#funzione che gestisce la home page
def index():
#per il tamplate html
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
    serve(app, host="0.0.0.0", port=8080)
