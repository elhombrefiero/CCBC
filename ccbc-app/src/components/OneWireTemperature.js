import React, { useState, useEffect } from "react";

function OneWireTemperature() {

    const [temperature, setTemperature] = useState({});

    function fetchTemperature () {
        fetch('/temperatures').then(
            response => response.json()
        ).then(data => setTemperature(data))
    }

    useEffect(() => {
        const timer = setInterval(fetchTemperature, 1000);
        return () => clearInterval(timer);
    }, [])

    return (
        <div>
            <p>Temperature from Arduino: ({temperature.message})</p>
        </div>
    );
}

export default OneWireTemperature;
