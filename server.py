# flask --app data_server run
from flask import Flask
from flask import render_template
import json


app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    f = open('data/data.json','r')
    complete_data = json.load(f)
    f.close()
    Jan_dates = complete_data.keys()
    return render_template('index.html',dates= Jan_dates)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/date')
def date():
    f = open('data/data.json','r')
    complete_data = json.load(f)
    f.close()
    return render_template('date.html')

app.run(debug=True)