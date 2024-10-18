import sys, json, datetime, re
import matplotlib.pyplot as plt
from collections import defaultdict
from open_meteo import get_historical_data



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Incorrect number of arguments")
        exit()

    file_name = sys.argv[1]
    all_forecasts_dict = None
    try:
        with open(file_name, "r") as f:
            all_forecasts_dict = json.loads(f.read())
    except:
        print("Invalid file name: " + file_name)
        exit()


    parsed_time = re.search("^.*?_-_(\\d{2}-\\d{2}-\\d{2}\\+\\d{2}_\\d{2}_\\d{2}_\\d{6})\\.txt$", file_name)

    time = datetime.datetime.strptime(parsed_time[1], '%d-%m-%y+%H_%M_%S_%f') + datetime.timedelta(hours=5)

    actual_time = get_historical_data(time)

    forecast_time = []
    forecast_dict = defaultdict(list)
    actual_dict = defaultdict(list)

    for key in actual_time.keys():
        for i in len(all_forecasts_dict.keys()):
            actual_dict[key].apped(actual_time[key])

    for time_out in all_forecasts_dict.keys():
        forecast_time.append(int(time_out))
        individual_forecast = all_forecasts_dict[time_out]
        for key in individual_forecast.keys():
            forecast_dict[key].append(float(individual_forecast[key]))


    print(forecast_dict)
    print(forecast_time)

    for key in forecast_dict:
        print(key)
        plt.plot(forecast_time, forecast_dict[key], marker = 'o', label = 'Forecasted')
        plt.plot(forecast_time, actual_dict[key], marker = 'o', label = 'Actual')

        plt.xlabel("Hours out")
        plt.ylabel(key)

        plt.show()



