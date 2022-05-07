import Navbar from './components/Navbar'
// import Temperatures from './components/Temperatures';
import OneWireTemperature from './components/OneWireTemperature'
import Heater from './components/Heater'
import Pump from './components/Pump'
import Grid from '@mui/material/Grid';
import './App.css';

// TODO: Add footer with "Collaborative design between Matthew Simoni, Ryan Coulson, and Rene Valdez."

function App() {
  return (
    <div className="App">
      <Navbar />
      {/* <div className="top-sticky-container">
        <h1>CCBC Control Panel</h1>
        <Temperatures />
      </div> */}
      <OneWireTemperature />
      <Grid container space={2}>
        <Grid item xs={6} md={4}>
          <Heater id="0" name="Hot Water Tank Heater" pin="5"/>
        </Grid>
        <Grid item xs={6} md={4}>
          <Heater id="1" name="HERMS Heater" pin="4" />
        </Grid>
        <Grid item xs={6} md={4}>
          <Heater id="2" name="Boil Kettle Heater" pin="3"/>
        </Grid>
      </Grid>
      {/* TODO: I think I can get rid of pin here and use whatever is in
      the configurationf file */}
      <Grid container space={2}>
        <Grid item xs={6} md={4}>
          <Pump id="0" name="Pump 1" pin="9" />
        </Grid>
        <Grid item xs={6} md={4}>
          <Pump id="1" name="Pump 2" pin="8" />
        </Grid>
        <Grid item xs={6} md={4}>
          <Pump id="2" name="Pump 3" pin="7" />
        </Grid>
      </Grid>      
    </div>
  );
}

export default App;
