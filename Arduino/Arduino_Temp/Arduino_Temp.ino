// Reads in temperature sensor data and outputs it to the serial port
// Written by Rene Valdez

// Libraries obtained from:
// https://github.com/milesburton/Arduino-Temperature-Control-Library
#include <OneWire.h>
#include <DallasTemperature.h>

// Data wire connected to port 2 on the Arduino
#define ONE_WIRE_PORT 2

// Setup a oneWire instance to communicate with any oneWire devices
OneWire oneWire(ONE_WIRE_PORT);

// Pass oneWire reference to Dallas Temperature
DallasTemperature sensors(&oneWire);

void setup(void) {
  // start serial port
  Serial.begin(9600);
  Serial.println("DS18B20 demo");
  
  // setup the library
  sensors.begin();

}

void loop(void) {
  // Request temperature

  sensors.requestTemperatures();

  // Get temperature
  float tempC = sensors.getTempCByIndex(0);
  Serial.print("T1: ");
  Serial.print(DallasTemperature::toFahrenheit(tempC));
  Serial.println(" deg F\n");
  
  delay(500); // in milliseconds
  
}
