import React, { useState, useEffect } from "react";
import Button from '@mui/material/Button'
import './Pump.css'


function Pump(props) {
 
  const [status, setStatus] = useState({});

  function turnOn() {
    setStatus({"name": props.name, "status": "ON"});
    console.log("TURNING ON");
    console.log(status);
  };
  
  function turnOff() {
    setStatus({"name": props.name, "status": "OFF"});
    console.log("TURNING OFF");
    console.log(status);
  };
   
  useEffect(() => {
    fetch('/pumps', {
        method: 'POST',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(status)
    }).then(() => {
        console.log(status)
    })    
  })

  useEffect(() => {
      fetch('/pumps').then(
        response => response.json()
      ).then(data => setStatus({
        "name": props.name, 
        "status": data['pumpData'][props.id]['status']
      }))
    }, [])

  console.log("CURRENT STATUS IN REACT: " + status.status)


  return (
    <div className="pump-input">
      <h4>{props.name}</h4>
      <div className="pump-buttons-container">
        <Button variant="contained" color="error" onClick={turnOn}>On</Button>
        <Button variant="contained" color="primary" onClick={turnOff}>Off</Button>
      </div>
      <p>Current Name: {status.name}</p>
      <p>Current Status: {status.status}</p>
    </div>
  );
}

export default Pump;
