# from flask import Flask

# api = Flask(__name__)

# @api.route('/profile')
# def my_profile():
#     response_body = {
#         "name": "David",
#         "about": "Food",
#         "balls": "1"
#     }

#     return response_body

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

from flask import Flask, render_template
from flask import request
import requests
import json

app = Flask(__name__)

@app.route('/profile', methods = ['POST'])
def get_query_from_react():
    data = request.get_json()
    print(data)

    return data

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
        "third": get_query_from_react()
    }

    # return render_template('index.html', data1=weatherd) #, data2=simbad)
    return response_body
