// Reads in temperature sensor data and outputs it to the serial port
// Listens to inputs coming from the serial to
// open and shut switches (pins)
// Written by Rene Valdez

// Libraries obtained from:
// https://github.com/milesburton/Arduino-Temperature-Control-Library
#include <OneWire.h>
#include <DallasTemperature.h>

// Data wire connected to port 2 on the Arduino
#define ONE_WIRE_PORT 10

// Setup a oneWire instance to communicate with any oneWire devices
OneWire oneWire(ONE_WIRE_PORT);

// Pass oneWire reference to Dallas Temperature
DallasTemperature sensors(&oneWire);

// Arrays to hold device addresses
DeviceAddress T1, T2, T3, T4, T5, T6, T7, T8, T9;

// Array to hold device Addresses
uint8_t *myTSensors[] = {
  T1,
  T2,
  T3,
  T4,
  T5,
  T6,
  T7,
  T8,
  T9,
};

// Declare number of sensors in global scope
int numSensors = 9;

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
  
  // Get number of sensors
  byte SensorCount = sensors.getDeviceCount();
  
  // Print devices found and respective addresses
  Serial.print("Assuming ");
  Serial.print(numSensors);
  Serial.println(" devices.");
  
  // Assigning an address to each member of myTSensor array
  for (int i = 0; i < numSensors; i ++)
  {
    if (!sensors.getAddress(myTSensors[i], i)) 
    {
      Serial.print("Unable to find address for Device ");
      Serial.println(i);
    }
    delay(100);   
  }
  
  // Return all temperature sensor serials 
  Serial.println("Printing addresses for all sensors");
  for (int i = 0; i < numSensors; i++)
  {
    printAddress(myTSensors[i]);
    Serial.println();
    delay(100); 
  }
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
  /* IMPORTANT!!!
     The python script reads in the data in data pairs separated by an equal sign (=),
     Each sensor will have all its attributes in this format, with a pound sign (#)
     separating each sensor. 
     For temperatures, the python script uses serial number to map that to a specific 
     sensor.
     Format of the arduino data is in the following form:
     Arduino variable name (e.g., Name=Temp1)
     Serial number (e.g., serial_num="28FF4A778016477")
     Value of the parameter (e.g., value=108.5)
     Units of the parameter (e.g., units=F)
     An example, using two temperature probes:
     name=Temp1,serial_num=blahblah1,value=55.55,units=F#name=Temp2,serial_num=blahblah2,value=69.69,units=F
     If you change this format here, change it in the python script as well! */
  for (int i = 0; i < numSensors; i++)
  {
    float tempF = sensors.getTempFByIndex(i);
    // Only include valid temperature readings
    if (tempF > 32)
    {
      Serial.print("tempsensor:");
      Serial.print("name=Temp");
      Serial.print(i);
      Serial.print(",serial_num=");
      printAddress(myTSensors[i]);
      Serial.print(",value=");
      Serial.print(tempF);
      Serial.println(",units=F");      
    }
  }

  // A delay of half a second works well for the interaction between Ard and rPi.
  // A faster time results in the rPi hanging (likely due to too much being sent through serial at once)
  delay(500); // in milliseconds
  
}

void setSwitchOnOff(int pin, String status_of_pin)
{
  if (status_of_pin == "ON") {
    digitalWrite(pin, HIGH);
    //Serial.print("Pin ");
    //Serial.print(pin);
    //Serial.print(" set to high");
    //Serial.println();
  }
  else {
    digitalWrite(pin, LOW);
    //Serial.print("Pin ");
    //Serial.print(pin);
    //Serial.print(" set to low");
    //Serial.println();
  }
}
