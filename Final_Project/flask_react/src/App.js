import { useState } from 'react'
import axios from "axios";
import './App.css';
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
    dict['name']="Name"
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
  const [name3, setName3] = useState('');

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

    POST('/post3', {name3: text}).then(
      async (resp) => {
        const json= await resp.json()
        console.log(json.name3)
        setName3(json.name3)
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
    <label>Enter Your Zip/Postal code and magnitude limit here </label>
    <p>Add a ",x" to the end of zipcode where x is the magnitude limit for your search</p>
    <p>We reccomend a magnitude limit of 6 or less if viewing with your naked eyes</p>
    <p>ex) 02134,6</p>
    <input value={text} onChange={onChange} />
    <input type="submit" value="Submit" onClick={onClick} />
    </form>
    <p>Viewing Reccomendation:<b>{name3}</b> </p>   
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