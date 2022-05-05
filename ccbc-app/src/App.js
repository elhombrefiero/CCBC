import './App.css';
// import Temperatures from './components/Temperatures';
// import Heater from './components/Heater'
import Pump from './components/Pump'
import Grid from '@mui/material/Grid';


function App() {
  return (
    <div className="App">
      {/* <div className="top-sticky-container">
        <h1>CCBC Control Panel</h1>
        <Temperatures />
      </div> */}
      {/* <div className="controls-container">
        <Heater name="Hot Water Tank"/>
        <Heater name="HERMS"/>
        <Heater name="Boil Tank"/>
      </div> */}
      <Grid container space={2}>
        <Grid item xs={6} md={4}>
          <Pump id="0" name="Pump 1" />
        </Grid>
        <Grid item xs={6} md={4}>
          <Pump id="1" name="Pump 2" />
        </Grid>
        <Grid item xs={6} md={4}>
          <Pump id="2" name="Pump 3" />
        </Grid>
      </Grid>      
    </div>
  );
}

export default App;
