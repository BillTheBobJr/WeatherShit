import requests
import json


lat = "42.0308"
lon = "-93.6319"
wfo = "DMX"
x = "73"
y = "69"


response = requests.get(f'https://api.weather.gov/gridpoints/DMX/73,69/forecast/hourly').json()

print(response)

#response_pretty = json.dumps(response, indent=2)

#print(response_pretty)

# for x in response['features']:
#   print(x['properties']['areaDesc'])
#   print(x['properties']['headline'])
#   print(x['properties']['description'])
#   print('\n******\n')