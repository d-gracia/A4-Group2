import { useState } from "react"

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

function MyForm(props) {
  const [text, setText] = useState('Input your zipcode here');
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
       
    <label>Input</label>
    <input value={text} onChange={onChange} />
    <input type="submit" value="Submit" onClick={onClick} />
    </form>
    <p>Current Weather is: <b>{name}</b></p>
    </header>
    </div>
  )

}

export default MyForm;