from flask import Flask, render_template
from flask import request
import requests
import json
from flask import Flask, request, jsonify, current_app
from flask_cors import CORS

app = Flask(__name__)

@app.post('/post')
def testPost():
    name = request.json.get('name')
    current_app.logger.debug(name)
    print("\n" + "Input: " + name)

    postalCode = str(name)
    map_url="https://dev.virtualearth.net/REST/v1/Locations/US/"+postalCode+"?&key=Ag8WDTJmVQA6MknifiagqrnEH1AaAv3ce03GeTcN2rYX7mbqzxzG31hX0MChiZlC"
    map = requests.get(map_url)

    #print(map.json())  #prints out entire responce
    print("\n")
    print(map.json()['resourceSets'][0]["resources"][0]['bbox'][0]) #prints out just the 'latitude' value
    print(map.json()['resourceSets'][0]["resources"][0]['bbox'][1]) #prints out just the 'longitude' value

    lat = str(map.json()['resourceSets'][0]["resources"][0]['bbox'][0])
    lon = str(map.json()['resourceSets'][0]["resources"][0]['bbox'][1])

    weather_exclude = "minutely,daily,alerts" 
    weather_api_url = "https://api.openweathermap.org/data/2.5/onecall?lat="+lat+"&lon="+lon+"&exclude="+weather_exclude+"&appid=0f4cf3136e2801a4208f7b57cada4f2b"
    weather = requests.get(weather_api_url)
    i = 0
    weatherd = ""
    while i < 48:
        weatherd = weatherd + "Weather in " + str(i) + " hour(s): " + weather.json()["hourly"][i]["weather"][0]["description"] + ".  "
        i += 1
    # weatherd= weather.json()["hourly"][5]["weather"][0]["description"] + " " + weather.json()["hourly"][0]["weather"][0]["description"]
    print("\n" + "Current Weather: " + weather.json()["current"]["weather"][0]["description"] + "\n")

    return jsonify(name=weatherd)


# because backend and frontend use different ports, we have to enable cross-origin requests
cors = CORS(app, resources={'/*':{'origins': 'http://localhost:3000'}}) 

if __name__ == "__main__":
    app.run()

"""
app.py
-This file demos how to get data from html form
 and display values to the webpage.
-This file doesn't parse or turn the output into python dictionaries
 but simply renders html and sends the results to the webpage.

This file uses two rendering templates: 
  -index.html 
  -layout.html

"""

@app.route("/profile", methods=['GET'])
def index():
    # Simbad API
    req = requests.get('http://simbad.u-strasbg.fr/simbad/sim-coo?output.format=ASCII&Coord=12%2030%20%2b10%2020&Radius=5&Radius.unit=arcmin')
    simbad = req.content
    print(simbad)

    # Weather API
    # "42.360081"
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
    weatherd= weather.json()["current"]["weather"][0]["description"]
    print(weather.json()["current"]["weather"][0]["description"])

    response_body = {
        "name": "David",
        "about": "Food",
        "balls": "1",
        "weather": weatherd,
        "third": "test"
    }

    # return render_template('index.html', data1=weatherd) #, data2=simbad)
    return response_body
