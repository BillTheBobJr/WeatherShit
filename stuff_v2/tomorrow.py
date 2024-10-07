import requests, json
from collections import defaultdict
from dateutil import parser
from datetime import timedelta

key_map = {
    'temperature' : 'temperature',
    'windSpeed' : 'windSpeed',
    'windDirection' : 'windDirection',
    'humidity' : 'humidity'
}

def make_request():
    apiKey = 'YHgJKgnWuro3Zr4pJjvj5ZgBt3CQ32sS'

    url = f"https://api.tomorrow.io/v4/weather/forecast?location=ames&timesteps=1h&apikey={apiKey}"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    # print(json.loads(response.text)['timelines']['hourly'][:12])

    return json.loads(response.text)['timelines']['hourly'][:12]

def filter_data(data):
    filtered_data = defaultdict(dict)
    for i in range(12):
        time = (parser.parse(data[i]['time']) - timedelta(hours=5)).strftime('%d-%m-%y+%H_%M_%S_%f')
        for key in key_map.keys():
            filtered_data[time][key_map[key]] = data[i]['values'][key]

    return filtered_data

def get_data():
    response = make_request()
    return filter_data(response)
