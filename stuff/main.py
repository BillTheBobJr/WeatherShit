import open_meteo
import tomorrow
import weather
import ARA
from collections import defaultdict
import threading, schedule, time, json

meteo_dict = defaultdict('list')
tomorrow_dict = defaultdict('list')
weather_dict = defaultdict('list')

data_keys = ['temperature', 'windSpeed', 'windDirection', 'humidity']
file_name = 'data.txt'

def get_forecast_values(forecast_dictionary):
    forecast_to_now = []
    for i in forecast_dictionary.keys():
        curr_forecast = forecast_dictionary[i]
        if(len(curr_forecast) == int(i)):
            forecast_to_now.append(curr_forecast.pop(int(i)))
    
    return forecast_to_now

def update_forecast_values():
    meteo_data = open_meteo.get_data()
    tomorrow_data = tomorrow.get_data()
    weather_data = weather.get_data()
    for i in range(12):
        meteo_dict[f"{i}"].insert(0, meteo_data[i])
        tomorrow_dict[f"{i}"].insert(0, tomorrow_data[i])
        weather_dict[f"{i}"].insert(0, weather_data[i])


def check_forecast_values_accuracy():
    f = open(file_name, "a")
    meteo_data = get_forecast_values(meteo_dict)
    tomorrow_data = get_forecast_values(tomorrow_dict)
    weather_data = get_forecast_values(weather_dict)
    ARA_data = ARA.get_data()

    for key in data_keys:
        f.write(f"{key}")
        f.write(f"\nMeteo Data:")
        for i in range(len(meteo_data[key])):
            f.write(f"{abs(ARA_data[key] - meteo_data[key])}   ")
        f.write(f"\nTomorrow Data:")
        for i in range(len(tomorrow_data[key])):
            f.write(f"{abs(ARA_data[key] - tomorrow_data[key])}   ")
        f.write(f"\nWeather Data:")
        for i in range(len(weather_data[key])):
            f.write(f"{abs(ARA_data[key] - weather_data[key])}   ")

    f.write("\n\n\n")
    f.close()

    


update_forecast_values()
check_forecast_values_accuracy()