from araweather import weather

location ='WilsonHall'
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

def get_data():
    response = make_request()[location]
    return filter_data(response)