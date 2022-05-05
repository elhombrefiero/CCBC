import React, { useEffect, useState } from "react";
import './Heater.css'

function Heater(props) {

  const [setpoint, setSetpoint] = useState(170);
  const [backendData, setBackendData] = useState([{}]);

  function incrementByOne() {
    setSetpoint(setpoint + 1);
  }
 
  function decrementByOne() {
    setSetpoint(setpoint - 1);
  }
  
  function incrementByFive() {
    setSetpoint(setpoint + 5);
  }
 
  function decrementByFive() {
    setSetpoint(setpoint - 5);
  }
 
  function handleTransfer() {
      console.log('transfer')
  }
//       fetch('/heater-water-tank', {
//           method: 'POST',
//           headers: { "Content-Type": "application/json" },
//           body: JSON.stringify({"setpoint": setpoint})
//       }).then(() => {
//           console.log("Heater (Water Tank) Setpoint: " + setpoint)
//       })

//       fetch('/heater-water-tank').then(
//         response => response.json()
//       ).then(data => setBackendData(data))
//   }

//   useEffect(() => {
//       fetch('/heater-water-tank').then(
//         response => response.json()
//       ).then(data => setBackendData(data))
//   }, [])
   
  return (
    <div className="heater-input">
      <div className="heading-container">
        <h3>{props.name} Heater</h3>
      </div>
      <div className="button-container">
        <button onClick={incrementByOne}>+1</button>
        <button onClick={decrementByOne}>-1</button>
      </div>
      <div className="button-container">
        <button onClick={incrementByFive}>+5</button>
        <button onClick={decrementByFive}>-5</button>
      </div>
      <div className="setpoint-container">
        <p>New Setpoint: {setpoint}F</p>
        <p>Current Setpoint: {backendData.backendCount}F</p>
      </div>
      <div className="button-container">
        <button onClick={handleTransfer}>Update</button>
      </div>
    </div>
  );
}

export default Heater;
