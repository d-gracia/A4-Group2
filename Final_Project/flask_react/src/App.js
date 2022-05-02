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
    </header>
    </div>
    )
}

export default App;