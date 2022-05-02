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

function App(props) {
  const [text, setText] = useState('');
  const [zip, setZip] = useState('');
  const [input, setInput] = useState('');
  const [name2, setName2] = useState('');

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

    POST('/post2', {name2: text}).then(
      async (resp) => {
        const json= await resp.json()
        console.log(json.name2)
        setName2(json.name2)
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
    <label>Enter Your Zip/Postal code here ~~~ </label>
    <input value={text} onChange={onChange} />
    <input type="submit" value="Submit" onClick={onClick} />
    </form>
    <p>Hourly Weather Report for the next 48 hours: <b>{zip}</b></p>
    <p>Objects that can be seen: <b>{name2}</b></p>
    {/* <table>
        <tr>
          <th>Name</th>
          <th>Coordinate</th>
          <th>Magnitude</th>
        </tr>
        {json.loads(name2).map((val, key) => {
          return (
            <tr key={key}>
              <td>{val.name}</td>
              <td>{val.coord}</td>
              <td>{val.mag}</td>
            </tr>
          )
        })}
      </table> */}
    </header>
    </div>
    )
}

export default App;