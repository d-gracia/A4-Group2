"""
API_testing.py

This file demos how to use and get data from apis.
This is not the actual back end, but the code will be able to be used on the backend.

Note: The API keys all belong to Fin, use them all you want but there is a daily limit,
so dont test it 100s of times for no reason please!
"""
import requests #use to get data from apis





"""
Return location from IP address

Probably dont want to use this, but i found it helpful in testing so im leaving it in for now.
"""

ip_address =  "  "#input your IPv4 adress here as a string

location_api_url = "https://api.ipgeolocation.io/ipgeo?apiKey=5c91ae956d134951a8900ac10248384c&ip="+ip_address

location = requests.get(location_api_url)

#print(location.json())  #prints out entire responce

print(location.json()['latitude']) #prints out just the 'latitude' value
print(location.json()['longitude'])
print("\n")
#other interesting returns
#['offset'] Timezone offset from UTC
#['is_dst'] is it daylight savings
#['dst_savings']  change in time from daylight savings
#['current_time_unix'] current system time






"""
Return weather from lat and long
"""

#we will take these values in from the front end or somewhere else
#set to boston for testing purposed
lat="42.360081"
lon="-71.058884"
weather_exclude = "minutely,hourly,daily,alerts" 
"""For a location it can output: current,minutely,hourly,daily,alerts

We likely do not need all of this, so either we can write a simple switch
to figure out which outputs we want, or we can just get all of it and 
only return what the front end asks for."""

weather_api_url = "https://api.openweathermap.org/data/2.5/onecall?lat="+lat+"&lon="+lon+"&exclude="+weather_exclude+"&appid=0f4cf3136e2801a4208f7b57cada4f2b"

weather = requests.get(weather_api_url)

#print(weather.json())  #prints out entire responce
print(weather.json()["current"]["weather"][0]["description"])

"""
other interesting returns

['offset'] #Timezone offset from UTC
['is_dst'] #is it daylight savings
['dst_savings'] # change in time from daylight savings
['current_time_unix'] #current system time
['timezone_offset'] #timezone difference from UTC in seconds

['current']['dt'] #system time
['current']['sunrise'] #system time
['current']['sunset'] #system time
['current']['clouds'] #Cloudiness, % of sky
['current']['temp'] #temp in kelvin
['current']['visibility'] # verage visibility, metres. The maximum value of the visibility is 10km
['current']['wind_speed'] #Wind speed. Units default: metre/sec, metric: metre/sec, imperial: miles/hour.
['current']['wind_deg'] #Wind direction, degrees (meteorological)
["current"]["weather"][0]["id"] #code for weather, can look at link for list of code meaning
["current"]["weather"][0]["main"] #Group of weather parameters, ie Rain
["current"]["weather"][0]["description"] #specific desciption of the weather, ie Heavy Rain
["current"]["weather"][0]["icon"] #index of icon that could be used to show weather,would have to import icons file

#https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2
"""






"""
Return visable based on location

Fin will come in and add this code later. Waiting on an email from dev
to see if a package called astroquery can be used. 
"""
