import { useState } from 'react'
import axios from "axios";
import './App.css';
import { Component } from "react";
import "../node_modules/bootstrap/dist/css/bootstrap.min.css";
import GoogleLoginComponent from "./googlebutton.component";

function POST(path, data) {
  return fetch(`http://localhost:5000${path}`,
  {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    }
  )
}

/* 
  function callData parses weatherd string into
  a list of dictionaries
*/
function callData(str) {
  var data = [];
  var parseArray = str.split('_')
  var dict = {};
    dict['hours']="Hours"
    dict['weather']="Weather"
    data.push(dict)
  let i = 0
  while (i < parseArray.length) {
    var dict2 = {};
    dict2['hours']=parseArray[i]
    dict2['weather']=parseArray[i+1]
    data.push(dict2)
    i=i+2
  }
  return data
}

/* 
  function callData2 parses simbad string into
  a list of dictionaries
*/
function callData2(str) {
  var data2 = [];
  var parseArray = str.split('_')
  var dict = {};
    dict['name']="NAME"
    dict['coord']="Coordinates"
    dict['mag']="Magnitude"
  data2.push(dict)
  let i = 0
  while (i < parseArray.length) {
    var dict2 = {};
    dict2['name']=parseArray[i]
    dict2['coord']=parseArray[i+1]
    dict2['mag']=parseArray[i+2]
    data2.push(dict2)
    i=i+3
  }
  return data2
}

/*
  function App sends user input to the frontend, 
  gets back data from the frontend, and displays on the app.
*/
function App(props) {
  const [text, setText] = useState('');
  const [zip, setZip] = useState('');
  const [input, setInput] = useState('');
  const [zip2, setZip2] = useState('');

  const onChange = e => {
    setText(e.target.value)
  }

  const onClick = e => {
    e.preventDefault();
    POST('/post', {zip: text}).then(
      async (resp) => {
        const json= await resp.json()
        console.log(json.zip)
        setZip(json.zip)
        console.log(json.input)
        setInput(json.input)
      }
    )

    POST('/post2', {zip2: text}).then(
      async (resp) => {
        const json= await resp.json()
        console.log(json.zip2)
        setZip2(json.zip2)
      }
    )
  }

  return (
    
    <div className="App">
    <header className="App-header">
    <form className="Form">

    <div className="Auth">
        <GoogleLoginComponent />
    </div>
    {/* <div>
    <input value={input} onChange={onChange} />
    </div> */}
    <p>Please enter your postal code.</p> 
    <p>To view objects with your naked eye, add ",n" at the end.</p>
    <p>To view objects with a telescope, add ",t" at the end. </p>
    <p>ex) 02134,n</p>
    <input value={text} onChange={onChange} />
    <input type="submit" value="Submit" onClick={onClick} />
    </form>
    <p>Hourly Weather Report for the next 48 hours:</p>
    <table>
        <tr>
        </tr>
        {callData(zip).map((val, key) => {
          return (
            <tr key={key}>
              <td>{val.hours}</td>
              <td>{val.weather}</td>
            </tr>
          )
        })}
      </table> 
    <p>Objects that can be seen:</p>
    <table>
        <tr>
        </tr>
        {callData2(zip2).map((val, key) => {
          return (
            <tr key={key}>
              <td>{val.name}</td>
              <td>{val.coord}</td>
              <td>{val.mag}</td>
            </tr>
          )
        })}
      </table>  
    </header>
    </div>
    )
}

export default App;