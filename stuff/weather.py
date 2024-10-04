import requests
import json

data_map = {
    'temperature' : '',
    'humidity' : '',
    'windSpeed' : '',
    'windDirection' : ''
}

# lat = "42.0308"
# lon = "-93.6319"
# wfo = "DMX"
# x = "73"
# y = "69"

def make_request():
    response = requests.get(f'https://api.weather.gov/gridpoints/DMX/73,69/forecast/hourly').json()

    return response['properties']['periods'][:12]

#response_pretty = json.dumps(response, indent=2)

#print(response_pretty)

# for x in response['features']:
#   print(x['properties']['areaDesc'])
#   print(x['properties']['headline'])
#   print(x['properties']['description'])
#   print('\n******\n')

def normalize_data(data):
    return 0


def filter_data(data):
    filtered_data = {}
    for keys in key_map.keys():
        filtered_data[key_map[keys]] = data[keys]
    return filtered_data

def get_data():
    response = make_request()[:]['values']
    return filter_data(response)