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
    with open('data/data.json','r') as f:
        complete_data = json.load(f)

    date = request.args.get('date')
    borough = request.args.get('borough')
    s_date = str(date)
    s_borough = str(borough)

    this_dict = {}
    message = ""
    interpretation = ""

    # Safe default values in case there's no data
    micro_rate = 0
    macro_rate = 0

    if s_borough in complete_data[s_date]:
        this_dict = complete_data[s_date][s_borough]
        message = "Here is your data for"

        total_black = this_dict.get("BLACK", {}).get("Total", 0)
        total_all = sum(r.get("Total", 0) for r in this_dict.values())
        if total_all > 0:
            micro_rate = total_black / total_all

        # Compute borough-wide average (macro)
        all_black, all_total = 0, 0
        for d in complete_data.values():
            if s_borough in d:
                for race, info in d[s_borough].items():
                    total = info.get("Total", 0)
                    all_total += total
                    if race.lower() == "black":
                        all_black += total
        if all_total > 0:
            macro_rate = all_black / all_total

        # Qualitative interpretation
        diff = micro_rate - macro_rate
        perc_diff = diff * 100

        if perc_diff > 15:
            interpretation = "Black individuals were arrested at a rate significantly higher than the borough's norm on this day."
        elif perc_diff > 5:
            interpretation = "Black arrests were somewhat elevated compared to the borough's average."
        elif perc_diff > -5:
            interpretation = "The rate of Black arrests was roughly in line with the borough's norm."
        elif perc_diff > -15:
            interpretation = "Black arrests were somewhat lower than usual for this borough."
        else:
            interpretation = "Black arrests were significantly lower than this borough's typical average."

    else:
        message = "Fortunately, nobody was arrested in"

    return render_template('date.html',date=date,borough=borough,data_dict=this_dict,message=message,interpretation=interpretation,micro_pct=round(micro_rate * 100, 2),macro_pct=round(macro_rate * 100, 2))
app.run(debug=True)