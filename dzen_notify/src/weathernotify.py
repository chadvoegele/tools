#!/usr/bin/env python
import urllib.request, urllib.parse, urllib.error, os

def getWeatherNoaa():
  zipcode = 60637
  url = 'http://www.weather.gov/data/current_obs/KMDW.xml'
  try:
    weather = str(urllib.request.urlopen(url).read())
     # Get conditions
    conditions = weather.split("</weather>")[0].split("<weather>")[1]
    # Get temperature
    temp = weather.split("</temp_f>")[0].split("<temp_f>")[1]
    outString = temp + "F, " + conditions
    return (outString, 3600)
  except:
    return ("!", 60)
