import requests, re, json
from collections import defaultdict

data_map = {
    'temperature' : 'temperature',
    'humidity' : {
        'relativeHumidity' : 'value'
    },
    'windSpeed' : 'windSpeed',
    'windDirection' : 'windDirection'
}

direction_map = {
    'N' : 0,
    'NNE' : 22.5,
    'NE' : 45,
    'ENE' : 67.5,
    'E' : 90,
    'ESE' : 112.5,
    'SE' : 135,
    'SSE' : 157.5,
    'S' : 180,
    'SSW' : 202.5,
    'SW' : 225,
    'WSW' : 247.5,
    'W' : 270,
    'WNW' : 292.5,
    'NW' : 315,
    'NNW' : 337.5,
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

def filter_data(data):
    print('enter')
    filtered_data = defaultdict(dict)
    for i in range(len(data)):
        for key in data_map.keys():
            access = data_map[key]
            if(type(access) == dict):
                for e in data_map[key].keys():
                    filtered_data[f'{i}'][key] = data[i][e][data_map[key][e]]
            else:
                filtered_data[f'{i}'][key] = data[i][data_map[key]]
    return filtered_data

def normalize_data(data):
    for i in data.keys():
        wind_speed_string = data[i]['windSpeed']
        wind_speed_range = re.search('\\d*', wind_speed_string).span()

        data[i]['temperature'] = 5*(data[i]['temperature'] - 32)/9
        data[i]['windSpeed'] = int(wind_speed_string[wind_speed_range[0]:wind_speed_range[1]])
        data[i]['windDirection'] = direction_map[data[i]['windDirection']]



def get_data():
    response = make_request()
    filtered_data = filter_data(response)
    normalize_data(filtered_data)
    return filtered_data