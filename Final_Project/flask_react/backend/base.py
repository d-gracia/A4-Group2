from urllib import response  #imports for the flask app and apis
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
from skyfield import api

app = Flask(__name__)

@app.post('/post')  #post for the weather for the next 48 hours
def testPost():
    zip = request.json.get('zip')
    current_app.logger.debug(zip)
    print("\n" + "Input: " + zip)

    # parse user input to extract postalCode
    postalCode = str(zip)
    list = postalCode.split(",")
    postalCode = str(list[0])

    # Put the zipcode searched into the mongo database
    # the certificate is locally stored for security reasons and is not on github
    uri = "mongodb+srv://cluster0.2tsfg.mongodb.net/api_key_test?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
    client = MongoClient(uri,       #connect to mongodb
                        tls=True,
                        tlsCertificateKeyFile='/Users/davidgracia/admin_user.pem',
                        server_api=ServerApi('1'))
    db = client['api_key_test']
    collection = db['weather_test']
 
    db_keys = client['private_keys']    #set database
    keys = db_keys['keys']              #set collection
    key_virtualearth = keys.find_one({"_id": "virtualearth"})   #find the key for the zipcode to coordinates api
    key = key_virtualearth["key"]   #set a var to the api key string

    map_url="https://dev.virtualearth.net/REST/v1/Locations/US/"+postalCode+"?&key="+key    #zipcode to coordinates api url
    map = requests.get(map_url)     #the responce from the api

    #print(map.json())  #prints out entire responce
    print("\n")
    print(map.json()['resourceSets'][0]["resources"][0]['bbox'][0]) #prints out just the 'latitude' value
    print(map.json()['resourceSets'][0]["resources"][0]['bbox'][1]) #prints out just the 'longitude' value

    lat = str(map.json()['resourceSets'][0]["resources"][0]['bbox'][0]) # set the 'latitude' value
    lon = str(map.json()['resourceSets'][0]["resources"][0]['bbox'][1]) # set the 'longitude' value

    key_openweathermap = keys.find_one({"_id": "openweathermap"})   #find the key for the coordinates to weather api
    key = key_openweathermap["key"] #set a var to the api key string
    weather_exclude = "minutely,daily,alerts" #set what the api call returns
    weather_api_url = "https://api.openweathermap.org/data/2.5/onecall?lat="+lat+"&lon="+lon+"&exclude="+weather_exclude+"&appid="+key #url
    weather = requests.get(weather_api_url) #the responce from the api

    i = 0           #iterrate over the responce and parse the data to a string
    weatherd = ""
    while i < 48:
       weatherd = weatherd + str(i) + "_" + weather.json()["hourly"][i]["weather"][0]["description"] + "_"
       i += 1
    
    # weatherd= weather.json()["hourly"][5]["weather"][0]["description"] + " " + weather.json()["hourly"][0]["weather"][0]["description"]
    print("\n" + "Current Weather: " + weather.json()["current"]["weather"][0]["description"] + "\n")

    return jsonify(zip=weatherd)    #return the weather as a json object to the front end

@app.post('/post3') #post for recomending viewinng times
def testPost3():
    name3 = request.json.get('name3')
    current_app.logger.debug(name3)
    print(str(name3))

    # parse user input to extract postalCode
    postalCode = str(name3)
    list = postalCode.split(",")
    postalCode = str(list[0])

    map_url="https://dev.virtualearth.net/REST/v1/Locations/US/"+postalCode+"?&key=Ag8WDTJmVQA6MknifiagqrnEH1AaAv3ce03GeTcN2rYX7mbqzxzG31hX0MChiZlC"    #url
    map = requests.get(map_url) #the responce from the api

    #print(map.json())  #prints out entire responce
    print("\n")
    print(map.json()['resourceSets'][0]["resources"][0]['bbox'][0]) #prints out just the 'latitude' value
    print(map.json()['resourceSets'][0]["resources"][0]['bbox'][1]) #prints out just the 'longitude' value

    lat = str(map.json()['resourceSets'][0]["resources"][0]['bbox'][0]) # set the 'latitude' value
    lon = str(map.json()['resourceSets'][0]["resources"][0]['bbox'][1]) # set the 'longitude' value

    weather_exclude = "minutely,daily,alerts" 
    weather_api_url = "https://api.openweathermap.org/data/2.5/onecall?lat="+lat+"&lon="+lon+"&exclude="+weather_exclude+"&appid=0f4cf3136e2801a4208f7b57cada4f2b"
    weather = requests.get(weather_api_url)
    #weather = session.get('weather', None)
    go = ["clear skys" , "few clouds"] #set good conditions
    hours = [10,20,30,40]
    recs= ''
    for i in hours:     #iterates to check if there are good conditions in a set number of hours
            found_a_string = False
            for item in go:    
                if item in weather.json()["hourly"][i]["weather"][0]["description"]:
                    found_a_string = True

            if found_a_string:
                 recs = recs + " In " + str(i) + " hours " + "may be a good time to view stars!"
            else:
                 recs =recs + " In " + str(i) + " hours, " +"we do not reccomend going to view stars."
    return jsonify(name3=recs)    #returns a json object to front end

@app.post('/post2') #post to return stars above a user
def testPost2():
    email = request.json.get('email')
    current_app.logger.debug(email)
    print(email)
    zip2 = request.json.get('zip2')
    current_app.logger.debug(zip2)

    # parse user input to extract postalCode
    postalCode = str(zip2)
    list = postalCode.split(",")
    postalCode = str(list[0])
    limitingmag = str(list[1])  #set limiting magnitude for stars returned

    map_url="https://dev.virtualearth.net/REST/v1/Locations/US/"+postalCode+"?&key=Ag8WDTJmVQA6MknifiagqrnEH1AaAv3ce03GeTcN2rYX7mbqzxzG31hX0MChiZlC"
    map = requests.get(map_url)

    #print(map.json())  #prints out entire responce
    print("\n")
    print(map.json()['resourceSets'][0]["resources"][0]['bbox'][0]) #prints out just the 'latitude' value
    print(map.json()['resourceSets'][0]["resources"][0]['bbox'][1]) #prints out just the 'longitude' value

    lat = float(round(map.json()['resourceSets'][0]["resources"][0]['bbox'][0],3))  #set 'latitude' as float to 3 decimal places
    lon = float(round(map.json()['resourceSets'][0]["resources"][0]['bbox'][1],3))  #set 'longitude' long as float to 3 decimal places

    #using skyfield to convert long lat to ra and dec (geospatial coordinates to coordinates on the celestial sphere)
    ts = api.load.timescale()   
    t = ts.now()    #gets current time
    geographic = api.wgs84.latlon(latitude_degrees=lat, longitude_degrees=lon)  #sets location based on lat long from inputted zipcode
    observer = geographic.at(t) #set to look from geographic at current time
    pos = observer.from_altaz(alt_degrees=90, az_degrees=0) #get the sky coordinates directly above the inputted zipcode
                                                            #this is called the zenith and the sky coordinate it points to changes as the earth rotates
    ra, dec, distance = pos.radec() #set zenith coordinates

    zenith_ra = ra._degrees     #set right ascension in degrees
    zenith_dec = dec.degrees    #set declination in degrees

    #set a rarnge for declination centered on zenith
    #checks to see if the range has allowed values and forces it to if it doesnt
    decmin = round(zenith_dec - 40.0,2) 
    decmax = round(zenith_dec + 40.0,2)
    if decmin < -90:
        decmin = -90.0
    if decmax > 90:
        decmax = 90.0

    #set a rarnge for right ascension centered on zenith
    #checks to see if the range has allowed values and forces it to if it doesnt
    ramin = round(zenith_ra - 40.0,2)
    ramax = round(zenith_ra + 40.0,2)
    if ramin < 0:
        ramin = 0.0
    if ramax > 360:
        ramax = 360.0

    sky_api_url="http://simbad.u-strasbg.fr/simbad/sim-sam?Criteria=ra+%3E+"+str(ramin)+"+%26+ra+%3C+"+str(ramax)+"%0D%0A%26+dec+%3E+"+str(decmin)+"+%26+dec+%3C+"+str(decmax)+"%0D%0A%26+Vmag+%3C+"+limitingmag+"&submit=submit+query&OutputMode=LIST&maxObject=100&output.format=ASCII"
    #url to get stars that can be seen based of user inputted location
    #the url sends a Criteria based query based on sky box made from min and max sky coordinates and the user input limiting magnitude
    #set to return 100 stars in an ASCII format (simbad cant return json objects from a url based api call)
    
    #get the responce and parse it to only look at the lines that include stars
    req = requests.get(sky_api_url)
    skyresponse  = req.text
    lines = skyresponse.split('\n')
    object_list_len = int(lines[7][20:24])
    objects = lines[11:-3]
    
    #iterate overr the lines and take create a 2d array of all the data
    box = [ [None]*(13) for k in range(object_list_len)]
    for i in range(object_list_len):
        for j in range(12):
            test = objects[i].split('|')
            box[i][j] = test[j]

    print(skyresponse)
    
    #create a string with just the information we want
    simbad = ""
    # 1 for ident, 3 for coords, 6 for V-Mag
    for i in range(object_list_len):
        simbad = simbad+(box[i][1])+"_"+(box[i][3])+"_"+(box[i][6])+"_"

    # Put the user data into the mongo database

    uri = "mongodb+srv://cluster0.2tsfg.mongodb.net/user_data?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
    client = MongoClient(uri,
                        tls=True,
                        tlsCertificateKeyFile='/Users/davidgracia/admin_user.pem',
                        server_api=ServerApi('1'))
    db = client['user_data']    #set to user database
    collection = db['users']

    inputresults = {    #format for how the info should be stored
    "zipcode": postalCode,
    "ra" : zenith_ra,
    "dec": zenith_dec,
    }

    collection.update_one({ "_id": email }, { "$push": {"results": inputresults}}) #update the databse with the latest user input
    
    return jsonify(zip2=simbad) #returns the object to front end

@app.post('/user_data') #searches for/creates user in database
def user_data():
    email = request.json.get('email')   #get user from front end
    current_app.logger.debug(email)
    print(email)
    name = request.json.get('name')     #get name from front end
    current_app.logger.debug(name)
    print(name)

    # Put the user data into the mongo database
    uri = "mongodb+srv://cluster0.2tsfg.mongodb.net/api_key_test?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
    client = MongoClient(uri,
                        tls=True,
                        tlsCertificateKeyFile='/Users/davidgracia/admin_user.pem',
                        server_api=ServerApi('1'))
    db = client['user_data']
    collection = db['users']

    if (collection.find_one({"_id": email})):   #check if user is in the database
        print("Found Exisitng User")
    else:
        print("Making New User")
        collection.insert_one({"_id": email, "Name": name,"results": []}) #adds the user if the user is not in the database

    return jsonify(email=email)

@app.route('/client_id', methods =["GET"]) #get the google clientID
def client_id():
    uri = "mongodb+srv://cluster0.2tsfg.mongodb.net/api_key_test?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
    client = MongoClient(uri,
                        tls=True,
                        tlsCertificateKeyFile='/Users/davidgracia/admin_user.pem',
                        server_api=ServerApi('1'))
    db = client['private_keys']
    collection = db['keys']
    key = collection.find_one({"_id": "googleclient"})  #gets google client ID
    id = key["key"]
    id = str(id)
    print(id)

    response_body = {"ClientID": id}

    return response_body #returns a json object of the clientID

# because backend and frontend use different ports, we have to enable cross-origin requests
cors = CORS(app, resources={'/*':{'origins': 'http://localhost:3000'}}) 

if __name__ == "__main__":
    app.run()


@app.route("/profile", methods=['GET']) #early version code of testing, does not affect to react
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
