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
    time_start = pd.Timestamp.now().ceil('60min').to_pydatetime()

    for i in range(12):
        meteo_dict[(time_start + timedelta(hours = i)).strftime('%d-%m-%y+%H_%M_%S_%f')][f'{i}'] = meteo_data[time_start.strftime('%d-%m-%y+%H_%M_%S_%f')]
        tomorrow_dict[(time_start + timedelta(hours = i)).strftime('%d-%m-%y+%H_%M_%S_%f')][f'{i}'] = tomorrow_data[time_start.strftime('%d-%m-%y+%H_%M_%S_%f')]
        weather_dict[(time_start + timedelta(hours = i)).strftime('%d-%m-%y+%H_%M_%S_%f')][f'{i}'] = weather_data[time_start.strftime('%d-%m-%y+%H_%M_%S_%f')]

def write_data(name, data):
    f = open(name, 'w')
    f.write(json.dumps(data))
    f.close()

def write_done_forecast_values():
    time_start = pd.Timestamp.now().ceil('60min').to_pydatetime() + timedelta(hours=2)
    meteo_keys = list(meteo_dict.keys())
    tomorrow_keys = list(tomorrow_dict.keys())
    weather_keys = list(weather_dict.keys())

    for key in meteo_keys:
        if datetime.datetime.strptime(key, '%d-%m-%y+%H_%M_%S_%f') < time_start:
            write_data("meteo_-_" + key + ".txt", meteo_dict.pop(key))

    for key in tomorrow_keys:
        if datetime.datetime.strptime(key, '%d-%m-%y+%H_%M_%S_%f') < time_start:
            write_data("tomorrow_-_" + key + ".txt", tomorrow_dict.pop(key))

    for key in weather_keys:
        if datetime.datetime.strptime(key, '%d-%m-%y+%H_%M_%S_%f') < time_start:
            write_data("weather_-_" + key + ".txt", weather_dict.pop(key))

def dump_forecast_values():
    meteo_keys = list(meteo_dict.keys())
    tomorrow_keys = list(tomorrow_dict.keys())
    weather_keys = list(weather_dict.keys())

    for key in meteo_keys:
        write_data("meteo_-_" + key + ".txt", meteo_dict.pop(key))

    for key in tomorrow_keys:
        write_data("tomorrow_-_" + key + ".txt", tomorrow_dict.pop(key))

    for key in weather_keys:
        write_data("weather_-_" + key + ".txt", weather_dict.pop(key))


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


# update_forecast_values()
# write_forecast_values()
# for key in meteo_dict.keys():
#     data = meteo_dict[key]
#     f = open(key + ".txt", 'w')
#     f.write(json.dumps(data))
#     f.close()


def run_continuously(interval=1):
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


def background_job():
    print('Hello from the background thread')


schedule.every().hour.do(update_forecast_values)

min = 60
hour = 60*min
# Start the background thread
stop_run_continuously = run_continuously(10*min)
print("start")
# Do some other things...
time.sleep(6*hour)

# Stop the background thread
stop_run_continuously.set()

print("done")
time.sleep(1*min)

dump_forecast_values()
