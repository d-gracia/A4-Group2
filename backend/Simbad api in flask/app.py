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
    print(data)
    return render_template('index.html',data=data)

