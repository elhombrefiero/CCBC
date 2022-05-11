import React, { useEffect, useState } from "react";
import Card from '@mui/material/Card';
import CardHeader from '@mui/material/CardHeader';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import ButtonGroup from '@mui/material/ButtonGroup';
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward';
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward';
import TextField from '@mui/material/TextField';
import InputAdornment from '@mui/material/InputAdornment';
import './Heater.css'

// TODO: Add a slider from Material UI to control voltage to heater
// to provide less power during boil

function Heater(props) {

  const [status, setStatus] = useState({});

  function incrementSetpoint() {
    setStatus(previousValue => {
      return {
        ...previousValue,
        "setpoint": status.setpoint + 1
      };
    });
  }
 
  function decrementSetpoint() {
    setStatus(previousValue => {
      return {
        ...previousValue,
        "setpoint": status.setpoint - 1
      };
    });
  }
  
  function incrementDeadband() {
    setStatus(previousValue => {
      return {
        ...previousValue,
        "deadband": status.deadband + 1
      };
    });
  }
 
  function decrementDeadband() {
    setStatus(previousValue => {
      return {
        ...previousValue,
        "deadband": status.deadband - 1
      };
    });
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
    <Card variant="outlined" className="heater-input">
      <CardHeader title={props.name}></CardHeader>
      <CardContent>
        <div className="inputs-container" style={{ marginBottom: '2ch' }}>
          <TextField
            label="Setpoint"
            sx={{ width: '15ch' }}
            InputProps={{
              endAdornment: <InputAdornment position="end">F</InputAdornment>,
            }}
            InputLabelProps={{
              shrink: true,
            }}
            value={status.setpoint}
          />
          <Button variant="contained" onClick={incrementSetpoint}><ArrowUpwardIcon></ArrowUpwardIcon></Button>
          <Button variant="contained" onClick={decrementSetpoint}><ArrowDownwardIcon></ArrowDownwardIcon></Button>
        </div>

        <div className="inputs-container">
          <TextField
            label="Diff"
            id="outlined-end-adornment"
            sx={{ width: '15ch' }}
            InputProps={{
              endAdornment: <InputAdornment position="end">F</InputAdornment>,
            }}
            InputLabelProps={{
              shrink: true,
            }}
            value={status.deadband}
          />
          <Button variant="contained" onClick={incrementDeadband}><ArrowUpwardIcon></ArrowUpwardIcon></Button>
          <Button variant="contained" onClick={decrementDeadband}><ArrowDownwardIcon></ArrowDownwardIcon></Button>
        </div>
      </CardContent>

      <p>Heater Status: {status.status}</p>

    </Card>
  );
}

export default Heater;
