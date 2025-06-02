# flask --app data_server run
from flask import Flask
from flask import request 
from flask import render_template
import json
#if flask is messing up look at the version in the bottom left corner

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    f = open('data/data.json','r')
    complete_data = json.load(f)
    f.close()
    Jan_dates = complete_data.keys()
    # function that extracts colors for everything
    borough_totals = {}

    for precinct_data in complete_data.values():
        for borough, races in precinct_data.items():
            if borough not in borough_totals:
                borough_totals[borough] = {"BLACK": 0, "TOTAL": 0}
            for race, race_data in races.items():
                total = race_data.get("Total", 0)
                if race.upper() == "BLACK":
                    borough_totals[borough]["BLACK"] += total
                    borough_totals[borough]["TOTAL"] += total
                else:
                    borough_totals[borough]["TOTAL"] += total
    bx_colors = borough_totals["Bronx"]["BLACK"]/borough_totals["Bronx"]["TOTAL"]
    bk_colors = borough_totals["Brooklyn"]["BLACK"]/borough_totals["Brooklyn"]["TOTAL"]
    m_colors = borough_totals["Manhattan"]["BLACK"]/borough_totals["Manhattan"]["TOTAL"]
    s_colors = borough_totals["Staten Island"]["BLACK"]/borough_totals["Staten Island"]["TOTAL"]
    q_colors = borough_totals["Queens"]["BLACK"]/borough_totals["Queens"]["TOTAL"]
    bx_color = bx_colors * 100
    bk_color = bk_colors * 100
    m_color = m_colors * 100
    s_color = s_colors * 100
    q_color = q_colors * 100
    return render_template('index.html',dates= Jan_dates, bx_c = bx_color, bk_c = bk_color, m_c = m_color, s_c = s_color, q_c = q_color)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/date')
def date():
    f = open('data/data.json','r')
    complete_data = json.load(f)
    f.close()
    date = request.args.get('date')
    borough = request.args.get('borough')
    s_date = str(date)
    s_borough = str(borough)
    if s_borough in complete_data[s_date]:
        this_dict = complete_data[s_date][s_borough]
        message = "Here is your data for"
    if s_borough not in complete_data[s_date]:
        this_dict = {}
        message = "Fortunatly nobody was arrested in"
    print(this_dict)
    thing = len(this_dict)
    print(thing)

    return render_template('date.html',date = date, borough = borough, data_dict = this_dict, message = message, length = thing)

app.run(debug=True)