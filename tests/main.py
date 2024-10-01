import sched, time
import requests, json
s = sched.scheduler(time.time, time.sleep)

global_elements = ['startTime']

def SetGlobalElements(elements):
    global global_elements
    global_elements = elements.copy()

def GetWeatherForecast():
    response = requests.get(f'https://api.weather.gov/gridpoints/DMX/73,69/forecast/hourly').json()

    return response['properties']['periods'][0:3]

def GetWeatherElements(forecast, elements = None):
    newForecast = []
    elements = global_elements if elements is None else elements
    for i in range(len(forecast)):
        newForecast.append({})
        for e in elements:
            newForecast[i][e] = forecast[i][e]

    return(newForecast)

def RunForecast():
    forecast = GetWeatherForecast()
    print(GetWeatherElements(forecast))


if __name__ == '__main__':
    elements = ['startTime', 'temperature', 'windSpeed', 'windDirection']
    SetGlobalElements(elements)
    RunForecast()

    print("\n\n")

    s.enter(10, 1, RunForecast)

    s.run()