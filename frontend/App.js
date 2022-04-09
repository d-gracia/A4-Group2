import logo from './logo.svg';
import './App.css';
import Form_tutorial from './Form_tutorial';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <form className="App-form">
          <label>
            Zip code:
          <input type="text" name="name" />
          </label>
          <input type="submit" value="Submit" />
        </form>
      </header>
    </div>
  );
}

export default App;

/////////////////////////////////////////////////////////////////////////////