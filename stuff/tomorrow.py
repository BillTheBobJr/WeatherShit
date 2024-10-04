import requests, json
from collections import defaultdict

key_map = {
    'temperature' : 'temperature',
    'windSpeed' : 'windSpeed',
    'windDirection' : 'windDirection',
    'humidity' : 'humidity'
}

def make_request():
    apiKey = 'tlwqYbFKUV1N6RdATk9XDJK5RP22PJfF'

    url = f"https://api.tomorrow.io/v4/weather/forecast?location=ames&timesteps=1h&apikey={apiKey}"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    # print(json.loads(response.text)['timelines']['hourly'][:12])

    return json.loads(response.text)['timelines']['hourly'][:12]

def filter_data(data):
    filtered_data = defaultdict(dict)
    for i in range(12):
        for key in key_map.keys():
            filtered_data[f'{i + 1}'][key_map[key]] = data[i]['values'][key]

    return filtered_data

def get_data():
    response = make_request()
    return filter_data(response)


print(get_data())