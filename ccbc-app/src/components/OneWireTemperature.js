import React, { useState, useEffect } from "react";

function OneWireTemperature() {

    const [temperature, setTemperature] = useState({});

    useEffect(() => {
        const timer = setInterval(() => {
            fetch('/temperatures').then(
                response => response.json()
            ).then(data => setTemperature(data))
        }, 10000);
        return () => clearInterval(timer);
    }, [])

    return (
        <div>
            <p>Temperature from Arduino: ({temperature.message})</p>
        </div>
    );
}

export default OneWireTemperature;
