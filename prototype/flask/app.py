"""
app.py
This file allows to get data from Simbad api with user input values.
The results are passed and displayed to a webpage.
This file uses two rendering templates: 
  -index.html 
  -layout.html
"""

from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index(): 
    # input values
    query = {
      'output.format': 'ASCII',
      'Radius' : '1',
      'Radius.unit' : 'deg',
      'Coord':'7 12 6 + 65 40 8'
    }
    
    req = requests.get("http://simbad.u-strasbg.fr/simbad/sim-coo",query) 
       
    data = req.content

    postalCode =  "85253" #input the zipcode you want here

    map_url="https://dev.virtualearth.net/REST/v1/Locations/US/"+postalCode+"?&key=Ag8WDTJmVQA6MknifiagqrnEH1AaAv3ce03GeTcN2rYX7mbqzxzG31hX0MChiZlC"

    map = requests.get(map_url)

    lat = str(map.json()['resourceSets'][0]["resources"][0]['bbox'][0])
    lon = str(map.json()['resourceSets'][0]["resources"][0]['bbox'][1])

    weather_exclude = "minutely,hourly,daily,alerts"

    weather_api_url = "https://api.openweathermap.org/data/2.5/onecall?lat="+lat+"&lon="+lon+"&exclude="+weather_exclude+"&appid=0f4cf3136e2801a4208f7b57cada4f2b"

    weather = requests.get(weather_api_url)

    Current_weather = weather.json()["current"]["weather"][0]["description"]


    print(Current_weather)
    print(lat)
    print(lon)
    return render_template('index.html',data=Current_weather)