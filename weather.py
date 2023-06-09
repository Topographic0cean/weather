#!/usr/bin/env python 

import requests
import json
import pprint


latitude = 32.7270
longitude = -117.2058

result = requests.get(f'https://api.weather.gov/points/{latitude},{longitude}')
station = json.loads(result.text)

grid = station['properties']['gridId']
forecastURL = station['properties']['forecast']
hourlyURL = station['properties']['forecastHourly']
dataURL = station['properties']['forecastGridData']
stationsURL = station['properties']['observationStations']

print(grid)

if False:
    result = requests.get(forecastURL+'?units=si')
    forecast = json.loads(result.text)
    for p in forecast['properties']['periods']:
        details = p['detailedForecast']
        name = p['name']
        rain = p['probabilityOfPrecipitation']['value']
        if rain == None:
            rain = ""
        temp = p['temperature']
        wind = p['windDirection']
        speed = p['windSpeed']
        print(f'{name:15} {rain:4}{str(temp):2}C  {speed:15} {wind:5} {details}')

if True:
    result = requests.get(hourlyURL+'?units=si')
    forecast = json.loads(result.text)
    pprint.pprint(forecast)
