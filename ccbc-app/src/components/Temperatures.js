import React, { useState, useEffect } from "react";
import './Temperature.css'
import Item from './Item'

function Temperatures(props) {

    const [configurationData, setConfigurationData] = useState([{}]);
    
    useEffect(() => {
        fetch('/configuration').then(
        response => response.json()
        ).then(data => setConfigurationData(data))
    }, [])

    function populateTemperatures(e) {
        return (
            <Item key={e.id} name={e.name} />
        )
    }


    return (
        <div className="temperature-container">
            <p>Temperatures</p>
            {configurationData.temperature_sensors?.map(populateTemperatures)} 

            {/* <button onClick={printData}>Print</button> */}            
            
            {/* <p>Hot Water Tank: 0F</p>
            <p>Mash Tun High: 0F</p>
            <p>Mash Tun Low: 0F</p>
            <p>Boil Kettle: 0F</p> */}
        </div>
    );
}

export default Temperatures;
