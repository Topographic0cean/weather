#!/usr/bin/env python

""" 
    Get weather for Point Loma, California and determine which days are best for sailing
"""
from datetime import datetime
import json
import pprint
import requests


LATITUDE = 32.7270
LONGITUDE = -117.2058

result = requests.get(
    f"https://api.weather.gov/points/{LATITUDE},{LONGITUDE}", timeout=5
)
station = json.loads(result.text)

grid = station["properties"]["gridId"]
forecastURL = station["properties"]["forecast"]
hourlyURL = station["properties"]["forecastHourly"]
dataURL = station["properties"]["forecastGridData"]
stationsURL = station["properties"]["observationStations"]

result = requests.get(forecastURL + "?units=si", timeout=5)
forecast = json.loads(result.text)
for p in forecast["properties"]["periods"]:
    details = p["detailedForecast"]
    name = p["name"]
    rain = p["probabilityOfPrecipitation"]["value"]
    if rain is None:
        rain = ""
    temp = p["temperature"]
    wind = p["windDirection"]
    speed = p["windSpeed"]
    print(f"{name:15} {rain:4}{str(temp):2}C  {wind:4}{speed:15}  {details}")

result = requests.get(hourlyURL + "?units=si", timeout=10)
forecast = json.loads(result.text)
for p in forecast["properties"]["periods"]:
    details = p["shortForecast"]
    date = datetime.fromisoformat(p["startTime"]).strftime("%a %H")
    rain = p["probabilityOfPrecipitation"]["value"]
    if rain is None:
        rain = ""
    temp = p["temperature"]
    wind = p["windDirection"]
    speed = p["windSpeed"]
    print(f"{date:6} {rain:3}% {str(temp):2}C  {speed:8} {wind:4}{details}")

result = requests.get(dataURL, timeout=5)
forecast = json.loads(result.text)
pprint.pprint(forecast)

result = requests.get(stationsURL, timeout=5)
forecast = json.loads(result.text)
pprint.pprint(forecast)
