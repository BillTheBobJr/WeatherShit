import openmeteo_requests
import requests_cache
import pandas as pd
from collections import defaultdict
from dateutil import parser
from datetime import timedelta
from retry_requests import retry

key_map = {
	'temperature_2m' : 'temperature',
	'wind_speed_10m' : 'windSpeed', 
	'wind_direction_10m' : 'windDirection',
	'relative_humidity_2m' : 'humidity'
}

# Setup the Open-Meteo API client with cache and retry on error
def make_historical_request(time):
	cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
	retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
	openmeteo = openmeteo_requests.Client(session = retry_session)

	# Make sure all required weather variables are listed here
	# The order of variables in hourly or daily is important to assign them correctly below
	url = "https://api.open-meteo.com/v1/forecast"
	params = {
	"latitude": 42.0308,
	"longitude": -93.6319,
	"hourly": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m", "wind_direction_10m"],
	"wind_speed_unit": "mph",
	"forecast_days": 2
}
	responses = openmeteo.weather_api(url, params=params)

	# Process first location. Add a for-loop for multiple locations or weather models

	response = responses[0]
	# print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
	# print(f"Elevation {response.Elevation()} m asl")
	# print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
	# print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

	# Process hourly data. The order of variables needs to be the same as requested.
	hourly = response.Hourly()
	hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
	hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
	hourly_wind_speed_10m = hourly.Variables(2).ValuesAsNumpy()
	hourly_wind_direction_10m = hourly.Variables(3).ValuesAsNumpy()
       
	hourly_data = defaultdict(dict)
       
       
	time = pd.date_range(
		start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
		end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = hourly.Interval()),
		inclusive = "left"
	)
    
	for i in range(48):
		hourly_data[f'{time[i]}']["temperature_2m"] = hourly_temperature_2m[i]
		hourly_data[f'{time[i]}']["relative_humidity_2m"] = hourly_relative_humidity_2m[i]
		hourly_data[f'{time[i]}']["wind_speed_10m"] = hourly_wind_speed_10m[i]
		hourly_data[f'{time[i]}']["wind_direction_10m"] = hourly_wind_direction_10m[i]

	return hourly_data

	# hourly_dataframe = pd.DataFrame(data = hourly_data)
	# print(hourly_dataframe)

def filter_data(data):
	filtered_data = defaultdict(dict)
	for i in data.keys():
		time = (parser.parse(i) - timedelta(hours=5)).strftime('%d-%m-%y+%H_%M_%S_%f')
		for key in key_map.keys():
			filtered_data[time][key_map[key]] = data[f'{i}'][key].item()
	return filtered_data

def get_historical_data(time):
    response = make_historical_request(time)
    return filter_data(response)