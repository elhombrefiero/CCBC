// Reads in temperature sensor data and outputs it to the serial port
// Listens to inputs coming from the serial to
// open and shut switches (pins)
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

// Arrays to hold device addresses
DeviceAddress T1, T2;

// Strings used to send and receive through serial
String readString;
String pinStatus;

void setup()
{
  // Set pins 2-13 as output
  for (int i=2; i<14; i++) {
    pinMode(i, OUTPUT);
  }
  Serial.begin(9600);
  while (! Serial); // Wait untilSerial is ready - Leonardo
  Serial.print("Coulson Craft Brewery Control");
  Serial.println();
  
  // Setup the library
  sensors.begin();
  
  // Print devices found and respective addresses
  Serial.print("Found ");
  Serial.print(sensors.getDeviceCount(), DEC);
  Serial.println(" devices.");
  
  // search for devices on the bus and assign based on an index.
  if (!sensors.getAddress(T1, 0)) Serial.println("Unable to find address for Device 0");   
  if (!sensors.getAddress(T2, 1)) Serial.println("Unable to find address for Device 1");
  
  // show address for devices
  Serial.print("Device 0 Address: ");
  printAddress(T1);
  Serial.println();
  Serial.print("Device 1 Address: ");
  printAddress(T2);
  Serial.println();
}

// function to print a device address
void printAddress(DeviceAddress deviceAddress)
{
  for (uint8_t i = 0; i < 8; i++)
  {
    if (deviceAddress[i] < 16) Serial.print("0");
    Serial.print(deviceAddress[i], HEX);
  }
}

void loop() 
{
  // Listens for an input from the USB port
  if (Serial.available())
  {
    // Read the input from Python, which is
    // in the format 
    // X=OFF or X=ON
    // where X is the pin number
    char ch = Serial.read();
    readString += ch;
      // The character # is used to stop reading from serial
      if (ch == '#')
      {
        // Find the index of the equals sign
        int equalssign_index = readString.indexOf("=");
        // Pin number is everything before that
        String pinNum = readString.substring(0, equalssign_index);
        int pin_num = pinNum.toInt();
        // Status is the string after = and before #
        int poundsign_index = readString.indexOf("#");
        String pinStatus = readString.substring(equalssign_index + 1, poundsign_index); 
        setSwitchOnOff(pin_num, pinStatus);
        readString="";
      }
  }
  // Send the temperature reading through serial
  sensors.requestTemperatures();
  
  // Send temperature information through serial
  // IMPORTANT!!!
  // The python script reads in the data in the following format:
  // ArduinoName::GeneralName::Value::Units followed by a comma
  // For example, for temperature probes 1 and 2, it will look like this:
  // T1::Temp1::100::F,T2::Temp2::150::F
  // If you change this format here, change it in the python script as well!
  float tempC1 = sensors.getTempCByIndex(0);
  float tempC2 = sensors.getTempCByIndex(1);
  Serial.print("T1::Temp1::");
  Serial.print(DallasTemperature::toFahrenheit(tempC1));
  Serial.print("::F,");
  Serial.print("T2::Temp2::");
  Serial.print(DallasTemperature::toFahrenheit(tempC2));
  Serial.print("::F\n");
  // A delay of 1 second works well for the interaction between Ard and rPi.
  // A faster time results in the rPi hanging (likely due to too much being sent through serial at once)
  delay(1000); // in milliseconds
  
}

void setSwitchOnOff(int pin, String status_of_pin)
{
  if (status_of_pin == "ON") {
    digitalWrite(pin, HIGH);
    Serial.print("Pin ");
    Serial.print(pin);
    Serial.print(" set to high");
    Serial.println();
  }
  else {
    digitalWrite(pin, LOW);
    Serial.print("Pin ");
    Serial.print(pin);
    Serial.print(" set to low");
    Serial.println();
  }
}
