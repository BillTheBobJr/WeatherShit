from araweather import weather

location ='AgronomyFarm'
key_map = {
    'Temperature' : 'temperature',
    'WindSpeed' : 'windSpeed',
    'WindDirection' : 'windDirection',
    'Humidity' : 'humidity'
}

def make_request():
    weather_data = weather.get_current_weather([location])
    return weather_data

def filter_data(data):
    filtered_data = {}
    for keys in key_map.keys():
        filtered_data[key_map[keys]] = data[keys]
    return filtered_data

def normalize_data(data):
    data['temperature'] = 5*(data['temperature'] - 32)/9

def get_data():
    response = make_request()[location]
    filtered_data = filter_data(response)
    normalize_data(filtered_data)
    return filtered_data