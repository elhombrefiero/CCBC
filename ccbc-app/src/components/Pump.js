import React, { useState, useEffect } from "react";
import Card from '@mui/material/Card';
import CardHeader from '@mui/material/CardHeader';
import CardContent from '@mui/material/CardContent';
import PowerSettingsNewIcon from '@mui/icons-material/PowerSettingsNew';
import MuiToggleButton from "@mui/material/ToggleButton";
import { styled } from "@mui/material/styles";
import './Pump.css'

function Pump(props) {

  const ToggleButton = styled(MuiToggleButton)({
    "&.Mui-selected, &.Mui-selected:hover": {
      color: "white",
      backgroundColor: '#d32f2f'
    }
  });

  const [status, setStatus] = useState({});

  // TODO: Need to figure out how to fetch get a initial startup to populate
  //       status from configuration file.
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
        "pin": data['data'][props.id]['pin'],
        "status": data['data'][props.id]['status']
      }))
    }, [])
  
  return (
    <Card variant="outlined" className="pump-card">
      <CardHeader title={props.name}></CardHeader>
      <CardContent>
        <ToggleButton
          value="check"
          color="primary"
          selected={status['status']}
          onChange={() => {
            setStatus({
              "id": props.id,
              "name": props.name,
              "pin": props.pin, 
              "status": !status['status']
            });
          }}
        >
          <PowerSettingsNewIcon />
        </ToggleButton>
      </CardContent>
      <p>Pump Status: {status.status ? 'ON' : 'OFF'}</p>
    </Card>
  );
}

export default Pump;
