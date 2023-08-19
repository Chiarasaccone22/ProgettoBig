from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')

#funzione che gestisce la home page

def index():
#per il tamplate html
    return render_template('index.html')

#if __name__ == '__main__':
   # app.run(host='0.0.0.0', port=5555)
