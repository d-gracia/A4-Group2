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
import requests
import json

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    req = requests.get('http://simbad.u-strasbg.fr/simbad/sim-coo?output.format=ASCII&Coord=12%2030%20%2b10%2020&Radius=5&Radius.unit=arcmin')
    data = req.content
    print(data)
    return render_template('index.html',data=data)



