import React, { useEffect, useState } from "react";
import Button from '@mui/material/Button'
import SendIcon from '@mui/icons-material/Send'
import Grid from '@mui/material/Grid';
import './Heater.css'

// TODO: Add a slider from Material UI to control voltage to heater
// to provide less power during boil

function Heater(props) {

  const [status, setStatus] = useState({});

  function incrementSetpointByOne() {
    setStatus(previousValue => {
      return {
        ...previousValue,
        "setpoint": status.setpoint + 1
      };
    });
  }
 
  function decrementSetpointByOne() {
    setStatus(previousValue => {
      return {
        ...previousValue,
        "setpoint": status.setpoint - 1
      };
    });
  }
  
  function incrementSetpointByFive() {
    setStatus(previousValue => {
      return {
        ...previousValue,
        "setpoint": status.setpoint + 5
      };
    });
  }
 
  function decrementSetpointByFive() {
    setStatus(previousValue => {
      return {
        ...previousValue,
        "setpoint": status.setpoint - 5
      };
    });
  }
  
  function incrementDeadbandByOne() {
    setStatus(previousValue => {
      return {
        ...previousValue,
        "deadband": status.deadband + 1
      };
    });
  }
 
  function decrementDeadbandByOne() {
    setStatus(previousValue => {
      return {
        ...previousValue,
        "deadband": status.deadband - 1
      };
    });
  }
 
  function handleTransfer() {
      fetch('/heaters', {
          method: 'POST',
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(status)
      }).then(() => {
          console.log(status)
      })
  }

  useEffect(() => {
      fetch('/heaters', {
          method: 'POST',
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(status)
      }).then(() => {
          console.log(status)
      })
  })

  useEffect(() => {
      fetch('/heaters').then(
        response => response.json()
      ).then(data => setStatus({
        "id": props.id,
        "name": props.name, 
        "pin": data['data'][props.id]['digital_pin'],
        "status": data['data'][props.id]['status'],
        "setpoint": data['data'][props.id]['setpoint'],
        "deadband": data['data'][props.id]['deadband'],
      }))
    }, [])

  return (
    <div className="heater-input">
      <h4>{props.name}</h4>
      <p>Setpoint</p>
      {/* <div className="heater-buttons-container">
        <Button variant="outlined" color="primary" onClick={incrementSetpointByOne}>+1</Button>
        <Button variant="outlined" color="primary" onClick={decrementSetpointByOne}>-1</Button>
        <Button variant="outlined" color="primary" onClick={incrementSetpointByFive}>+5</Button>
        <Button variant="outlined" color="primary" onClick={decrementSetpointByFive}>-5</Button>
      </div> */}

      <Grid container space={2}>
        <Grid item xs={6} md={3}>
          <Button variant="outlined" color="primary" onClick={incrementSetpointByOne}>+1</Button>
        </Grid>
        <Grid item xs={6} md={3}>
          <Button variant="outlined" color="primary" onClick={decrementSetpointByOne}>-1</Button>
        </Grid>
        <Grid item xs={6} md={3}>
          <Button variant="outlined" color="primary" onClick={incrementSetpointByFive}>+5</Button>
        </Grid>
        <Grid item xs={6} md={3}>
          <Button variant="outlined" color="primary" onClick={decrementSetpointByFive}>-5</Button>
        </Grid>
      </Grid>
      <p>Deaband</p>
      <div className="heater-buttons-container">
        <Button variant="outlined" color="primary" onClick={incrementDeadbandByOne}>+1</Button>
        <Button variant="outlined" color="primary" onClick={decrementDeadbandByOne}>-1</Button>
      </div>
      <Button
        variant="contained" 
        color="primary" 
        endIcon={<SendIcon />} 
        onClick={handleTransfer}>
          Update
      </Button>
      <p>Status: {status.status}</p>
      <p>Setpoint: {status.setpoint}F</p>
      <p>Deadband: {status.deadband}F</p>
    </div>
  );
}

export default Heater;
