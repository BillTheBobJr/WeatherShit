import requests, json

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
    filtered_data = {}
    for keys in key_map.keys():
        filtered_data[key_map[keys]] = data[keys]

def get_data():
    response = make_request()[:]['values']
    return filter_data(response)