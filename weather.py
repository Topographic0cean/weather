#!/usr/bin/env python

""" 
    Get weather for Point Loma, California and determine which days are best for sailing
"""
from datetime import datetime
import json
import pprint
import requests

# San Diego Bay
LATITUDE = 32.7270
LONGITUDE = -117.2058

# New Orleans French Quarter
LATITUDE = 29.95
LONGITUDE = -90.06


def get_weather_station(lat, long):
    """
    get the urls for the weather station at the given
    latitude and longitude.
    """
    result = requests.get(f"https://api.weather.gov/points/{lat},{long}", timeout=5)
    station = json.loads(result.text)
    grid = station["properties"]["gridId"]
    forecast_url = station["properties"]["forecast"]
    hourly_url = station["properties"]["forecastHourly"]
    # the following are not used yet
    # data_url = station["properties"]["forecastGridData"]
    # stations_url = station["properties"]["observationStations"]
#return grid, forecast_url + "?units=si", hourly_url + "?units=si"
    return grid, forecast_url, hourly_url 


def get_daily_forecast(url):
    """return an array with the 7 day forecast"""
    result = requests.get(url, timeout=10)
    forecast = json.loads(result.text)
    daily = []
    for prop in forecast["properties"]["periods"]:
        details = prop["detailedForecast"]
        name = prop["name"]
        rain = prop["probabilityOfPrecipitation"]["value"]
        if rain is None:
            rain = ""
        temp = prop["temperature"]
        wind = prop["windDirection"]
        speed = prop["windSpeed"]
        daily.append(
            {
                "name": name,
                "forecast": details,
                "temperature": temp,
                "rain": rain,
                "temp": temp,
                "wind": wind,
                "speed": speed,
            }
        )
    return daily


def get_hourly_forecast(url):
    """return array of forecast for 7 days each hour"""
    result = requests.get(url, timeout=10)
    forecast = json.loads(result.text)
    daily = []
    for prop in forecast["properties"]["periods"]:
        details = prop["shortForecast"]
        date = datetime.fromisoformat(prop["startTime"]).strftime("%a %H %H:%M")
        rain = prop["probabilityOfPrecipitation"]["value"]
        humidity = prop["relativeHumidity"]["value"]
        if rain is None:
            rain = ""
        temp = prop["temperature"]
        wind = prop["windDirection"]
        speed = prop["windSpeed"]
        daily.append(
            {
                "date": date,
                "forecast": details,
                "temperature": temp,
                "humidity": humidity,
                "rain": rain,
                "temp": temp,
                "wind": wind,
                "speed": speed,
            }
        )
    return daily

def bad_forecast(forecast):
    """ return true if the forecast is bad for sailing """
    description = forecast["forecast"].lower()
    wind = int(forecast["speed"].split()[0])
    temp = int(forecast["temp"])
    rain = int(forecast["rain"])
    if "fog" in description or "rain" in description:
        return True
    if wind < 15:
       return True
    if temp < 16 or temp > 35:
       return True
    if rain > 30:
       return True

    return False

def is_boundary(hour):
    if hour == "09:00" or hour == "12:00" or hour == "16:00":
        return True
    return False

def get_predictions(hourly):
    """return an array with predictions for blocks of daylight sailing"""
    predictions = []
    index = 0
    while index < len(hourly):
        hour = hourly[index]
        time = hour["date"].split()[2]
        if is_boundary(time):
            pred = "good"
            for index2 in range(4):
                if bad_forecast(hourly[index+index2]):
                        pred = "bad"
            predictions.append((pred,
                                hour["date"],
                                hour["temperature"],
                                hour["rain"],
                                hour["wind"],
                                hour["speed"],
                                hour["forecast"],
                                ))
        index += 1
    return predictions

def print_table(hourly):
    print(f"{'    date':12} {'temp':4} {'hum':4} {'rain':4} {'forecast':20}");
    if (hourly):
        for hour in hourly:
            print(f"{hour['date']:12} {hour['temp']:4} {hour['humidity']:4} {hour['rain']:4} {hour['forecast']:20} ")


def main():
    """main sequence"""
    _, _, hourly_url = get_weather_station(LATITUDE, LONGITUDE)
    hourly = get_hourly_forecast(hourly_url)
    print_table(hourly)
#   pprint.pprint(hourly)
#   sailing_prediction = get_predictions(hourly)
#   pprint.pprint(sailing_prediction)


if __name__ == "__main__":
    main()
