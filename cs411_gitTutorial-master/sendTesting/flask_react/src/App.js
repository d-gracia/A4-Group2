import { useState } from 'react'
import axios from "axios";
import logo from './logo.svg';
import './App.css';

function App() {

  const [profileData, setProfileData] = useState(null)

  function getData() {
    axios({
      method: "GET",
      url:"/profile",
    })
    .then((response) => {
      const res =response.data
	    console.log(res);
      setProfileData(({
        profile_name: res.name,
        about_me: res.about,
        balls: res.balls,
        weather: res.weather,
        third: res.third}))
    }).catch((error) => {
      if (error.response) {
        console.log(error.response)
        console.log(error.response.status)
        console.log(error.response.headers)
        }
  })}

  function handlePostQuery(query){

    var myParams = {
        data: query
    }

    if (query != "") {
        axios.post('/profile', myParams)
            .then(function(response){
                console.log(response);
        //Perform action based on response
        })
        .catch(function(error){
            console.log(error);
        //Perform action based on error
        });
    } else {
        alert("The search query cannot be empty")
    }
  }

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>

        <p>To get your profile details: </p><button onClick={getData}>Click me</button>
        {profileData && <div>
              <p>Profile name: {profileData.profile_name}</p>
              <p>About me: {profileData.about_me}</p>
              <p>Balls: {profileData.balls}</p>
              <p>Current Weather: {profileData.weather}</p>
              <p>Third: {profileData.third}</p>
            </div>
        }
        <form>
          <label>
            Longitude:
            <input type="text" name="name" />
          </label>
          <button onClick={handlePostQuery("name")}>Submit</button>
        </form>
      </header>
    </div>
  );
}

export default App;
