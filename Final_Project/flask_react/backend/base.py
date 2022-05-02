from flask_pymongo import PyMongo
import flask
from flask import Flask, render_template
from flask import request
import requests
import json
from flask import Flask, request, jsonify, current_app
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)

@app.post('/post')
def testPost():
    zip = request.json.get('zip')
    current_app.logger.debug(zip)
    print("\n" + "Input: " + zip)
    # input = request.json.get('input')
    # current_app.logger.debug(input)
    # print("\n" + "Input: " + input)

    # Put the zipcode searched into the mongo database
    # the certificate is locally stored for security reasons
    uri = "mongodb+srv://cluster0.2tsfg.mongodb.net/api_key_test?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
    client = MongoClient(uri,
                        tls=True,
                        tlsCertificateKeyFile='/Users/davidgracia/admin_user.pem',
                        server_api=ServerApi('1'))
    db = client['api_key_test']
    collection = db['weather_test']
    collection.insert_one({"Zipcode": zip})

    # db.key.insert_one ({ "_id": 10, "item": "box", "qty": 20 })

    db_keys = client['private_keys']
    keys = db_keys['keys']
    key_virtualearth = keys.find_one({"_id": "virtualearth"})
    key = key_virtualearth["key"]
    postalCode = str(zip)
    map_url="https://dev.virtualearth.net/REST/v1/Locations/US/"+postalCode+"?&key="+key
    map = requests.get(map_url)

    #print(map.json())  #prints out entire responce
    print("\n")
    print(map.json()['resourceSets'][0]["resources"][0]['bbox'][0]) #prints out just the 'latitude' value
    print(map.json()['resourceSets'][0]["resources"][0]['bbox'][1]) #prints out just the 'longitude' value

    lat = str(map.json()['resourceSets'][0]["resources"][0]['bbox'][0])
    lon = str(map.json()['resourceSets'][0]["resources"][0]['bbox'][1])

    key_openweathermap = keys.find_one({"_id": "openweathermap"})
    key = key_openweathermap["key"]
    weather_exclude = "minutely,daily,alerts" 
    weather_api_url = "https://api.openweathermap.org/data/2.5/onecall?lat="+lat+"&lon="+lon+"&exclude="+weather_exclude+"&appid="+key
    weather = requests.get(weather_api_url)
    i = 0
    weatherd = ""
    while i < 48:
        if i == 10 or i ==20 or i==30 or i==40:
            found_a_string = False
            go = ""
            for item in go:    
                if item in weather.json()["hourly"][i]["weather"][0]["description"]:
                    found_a_string = True

            if found_a_string:
                weatherd = weatherd + "Weather in " + str(i) + " hour(s): " + weather.json()["hourly"][i]["weather"][0]["description"] + ".  " + "\n" + "Viewing Reccomendations: Today may be a good day to view stars!"
            else:
                weatherd = weatherd + "Weather in " + str(i) + " hour(s): " + weather.json()["hourly"][i]["weather"][0]["description"] + ".  " + "\n" + "Viewing Reccomendations: Depending on the current weather, we do not reccomend going to view stars."
        else:
            weatherd = weatherd + "Weather in " + str(i) + " hour(s): " + weather.json()["hourly"][i]["weather"][0]["description"] + ".  "
        i += 1
    # weatherd= weather.json()["hourly"][5]["weather"][0]["description"] + " " + weather.json()["hourly"][0]["weather"][0]["description"]
    print("\n" + "Current Weather: " + weather.json()["current"]["weather"][0]["description"] + "\n")

    return jsonify(zip=weatherd)

@app.post('/post2')
def testPost2():
    zip2 = request.json.get('zip2')
    current_app.logger.debug(zip2)
    
    # Simbad API
    ramin=  "0"
    ramax = "20"
    decmin = "0"
    decmax = "20"
    limitingmag = "6"
    
    req = requests.get("http://simbad.u-strasbg.fr/simbad/sim-sam?Criteria=ra+%3E+"+ramin+"+%26+ra+%3C+"+ramax+"%0D%0A%26+dec+%3E+"+decmin+"+%26+dec+%3C+"+decmax+"%0D%0A%26+Vmag+%3C+"+limitingmag+"&submit=submit+query&OutputMode=LIST&maxObject=2000&output.format=ASCII")
    skyresponse  = req.text
    lines = skyresponse.split('\n')
    object_list_len = int(lines[7][20:])
    objects = lines[11:-3]
    
    box = [ [None]*(13) for k in range(object_list_len)]
    for i in range(object_list_len):
        for j in range(12):
            test = objects[i].split('|')
            box[i][j] = test[j]
    
    
    simbad = ""
    # 1 for ident, 3 for coords, 6 for V-Mag
    for i in range(object_list_len):
        simbad = simbad+(box[i][1])+"_"+(box[i][3])+"_"+(box[i][6])+"_"
    
    return jsonify(zip2=simbad)

@app.post('/user_data')
def user_data():
    email = request.json.get('email')
    current_app.logger.debug(email)
    print(email)
    name = request.json.get('name')
    current_app.logger.debug(name)
    print(name)

    # Put the user data into the mongo database
    uri = "mongodb+srv://cluster0.2tsfg.mongodb.net/api_key_test?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
    client = MongoClient(uri,
                        tls=True,
                        tlsCertificateKeyFile='/Users/davidgracia/admin_user.pem',
                        server_api=ServerApi('1'))
    db = client['api_key_test']
    collection = db['user_data']
    collection.insert_one(
   {
    "_id": email,
     "Name": name,
   })

    return jsonify(email=email)

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
