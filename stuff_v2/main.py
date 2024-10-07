import open_meteo
import tomorrow
import weather
import ARA
from collections import defaultdict
import pandas as pd
from datetime import timedelta, datetime
import threading, schedule, time, json
import datetime

meteo_dict = defaultdict(dict)
tomorrow_dict = defaultdict(dict)
weather_dict = defaultdict(dict)

data_keys = ['temperature', 'windSpeed', 'windDirection', 'humidity']
file_name = 'data.txt'

def update_forecast_values():
    meteo_data = open_meteo.get_data()
    tomorrow_data = tomorrow.get_data()
    weather_data = weather.get_data()
    time_start = pd.Timestamp.now().ceil('60min').to_pydatetime() + timedelta(hours=2)

    for i in range(12):
        meteo_dict[(time_start + timedelta(hours = i)).strftime('%d-%m-%y+%H_%M_%S_%f')][f'{i}'] = meteo_data[time_start.strftime('%d-%m-%y+%H_%M_%S_%f')]
        tomorrow_dict[(time_start + timedelta(hours = i)).strftime('%d-%m-%y+%H_%M_%S_%f')][f'{i}'] = tomorrow_data[time_start.strftime('%d-%m-%y+%H_%M_%S_%f')]
        weather_dict[(time_start + timedelta(hours = i)).strftime('%d-%m-%y+%H_%M_%S_%f')][f'{i}'] = weather_data[time_start.strftime('%d-%m-%y+%H_%M_%S_%f')]

def write_forecast_values():
    time_start = pd.Timestamp.now().ceil('60min').to_pydatetime() + timedelta(hours=2)
    for key in meteo_dict.keys():
        if datetime.datetime.strptime(key, '%d-%m-%y+%H_%M_%S_%f') < time_start:
            data = meteo_dict.pop(key)
            f = open(key + ".txt", 'w')
            f.write(json.dumps(data))
            f.close()


# def get_forecast_values(forecast_dictionary):
#     forecast_to_now = []
#     for i in forecast_dictionary.keys():
#         curr_forecast = forecast_dictionary[i]
#         if(len(curr_forecast) == int(i)):
#             forecast_to_now.append(curr_forecast.pop(int(i) - 1))
    
#     return forecast_to_now

# def check_forecast_values_accuracy():
#     f = open(file_name, "a")
#     meteo_data = get_forecast_values(meteo_dict)
#     tomorrow_data = get_forecast_values(tomorrow_dict)
#     weather_data = get_forecast_values(weather_dict)
#     ARA_data = ARA.get_data()

#     for key in data_keys:
#         f.write(f"For key {key}:")
#         f.write(f"\nMeteo Data: ")
#         for i in range(len(meteo_data)):
#             f.write(f"{abs(ARA_data[key] - meteo_data[i][f"{key}"])}   ")
#         f.write(f"\nTomorrow Data: ")
#         for i in range(len(tomorrow_data)):
#             f.write(f"{abs(ARA_data[key] - tomorrow_data[i][f"{key}"])}   ")
#         f.write(f"\nWeather Data: ")
#         for i in range(len(weather_data)):
#             f.write(f"{abs(ARA_data[key] - weather_data[i][f"{key}"])}   ")

#         f.write("\n\n\n")

#     f.close()


update_forecast_values()
write_forecast_values()
for key in meteo_dict.keys():
    data = meteo_dict[key]
    f = open(key + ".txt", 'w')
    f.write(json.dumps(data))
    f.close()