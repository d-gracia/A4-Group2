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
  const [text, setText] = useState('Enter your zipcode here');
  const [name, setName] = useState('');

  const onChange = e => {
    setText(e.target.value)
  }

  const onClick = e => {
    e.preventDefault();
    POST('/post', {name: text}).then(
      async (resp) => {
        const json= await resp.json()
        console.log(json.name)
        setName(json.name)
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
       
    {/* <label>Input</label> */}
    <input value={text} onChange={onChange} />
    <input type="submit" value="Submit" onClick={onClick} />
    </form>
    <p>Current Weather: <b>{name}</b></p>
    </header>
    </div>
    )
}

export default App;