import React, { useState, useEffect } from "react";
import Button from '@mui/material/Button'
import './Pump.css'


function Pump(props) {
 
  const [status, setStatus] = useState({});

  function turnOn() {
    setStatus({
      "id": props.id,
      "name": props.name,
      "digital_pin": props.pin, 
      "status": "ON"
    });
  };
  
  function turnOff() {
    setStatus({
      "id": props.id,
      "name": props.name,
      "digital_pin": props.pin, 
      "status": "OFF"
    });
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
        "id": props.id,
        "name": props.name, 
        "pin": data['pumpData'][props.id]['digital_pin'],
        "status": data['pumpData'][props.id]['status']
      }))
    }, [])
  
  console.log(status)

  return (
    <div className="pump-input">
      <h4>{props.name}</h4>
      <div className="pump-buttons-container">
        <Button variant="contained" color="error" onClick={turnOn}>On</Button>
        <Button variant="contained" color="primary" onClick={turnOff}>Off</Button>
      </div>
      <p>Current ID: {status.id}</p>
      <p>Current Name: {status.name}</p>
      <p>Current Pin: {status.pin}</p>
      <p>Current Status: {status.status}</p>
    </div>
  );
}

export default Pump;
