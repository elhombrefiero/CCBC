// Reads in temperature sensor data and outputs it to the serial port
// Listens to inputs coming from the serial to
// open and shut switches (pins)
// Written by Rene Valdez

// Libraries obtained from Arduino Library Manager:
// ArduinoSTL
// MAX 31850 DallasTemp
// MAX 31850 OneWire
#include <ArduinoSTL.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// Data wire connected to port 2 on the Arduino
#define ONE_WIRE_PORT 10

// Setup a oneWire instance to communicate with any oneWire devices
OneWire oneWire(ONE_WIRE_PORT);

// Pass oneWire reference to Dallas Temperature
DallasTemperature sensors(&oneWire);

// Vector to hold device addresses
std::vector<uint8_t *> myTSensors;

// Strings used to send and receive through serial
String readString;
String pinStatus;

void setup()
{
  Serial.begin(9600);
  while (! Serial); // Wait untilSerial is ready - Leonardo
  Serial.print("Craft Brewery Control Starting...");
  Serial.println();
  
  // Setup the library
  sensors.begin();

  // Get number of sensors
  int numSensors = sensors.getDeviceCount();
  
  // Print devices found and respective addresses
  Serial.print("Found ");
  Serial.print(numSensors);
  Serial.println(" temperature sensors.");
  
  // Assigning an address to each member of myTSensor vector
  for (int i = 0; i < numSensors; i ++)
  {
    myTSensors.push_back(new DeviceAddress);
    delay(10);   
  }
  
  // Return all temperature sensor serials 
  Serial.println("Printing addresses for all sensors");
  for (int i = 0; i < numSensors; i++)
  {
    Serial.print("TSensor ");
    Serial.print(i);
    Serial.print(": ");
    printAddress(myTSensors[i]);
    Serial.println();
    delay(10); 
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

void setPinStatus(String string) {
  // Find the index of the equals sign
  int equalssign_index = readString.indexOf("=");
  // Pin number is everything before that
  String pinNum = readString.substring(0, equalssign_index);
  int pin_num = pinNum.toInt();
  // Status is the string after = and before #
  int poundsign_index = readString.indexOf("#");
  String pinStatus = readString.substring(equalssign_index + 1, poundsign_index); 
  setSwitchOnOff(pin_num, pinStatus);
}

void readAnalogPins() {
  int val = 0;
  for (int i=0; i < 6; i++) {
    val = analogRead(i);
    Serial.print("analogpin:");
    Serial.print("name=");
    Serial.print("Pin");
    Serial.print(i);
    Serial.print(",pin_num=");
    Serial.print(i);
    Serial.print(",value=");
    Serial.println(val);
  }
}

void readDigitalPins() {
  int val = 0;
  for (int i=2; i < 10; i++) {
    val = digitalRead(i);
    Serial.print("digitalpin:");
    Serial.print("name=");
    Serial.print("Pin");
    Serial.print(i);
    Serial.print(",pin_num=");
    Serial.print(i);
    Serial.print(",value=");
    Serial.println(val);
  }
}

void returnAllInfo() {
  // Update the temperature readings
  sensors.requestTemperatures();
    
  // Send temperature information through serial
  /* IMPORTANT!!!
     The python script reads in the data in data pairs separated by an equal sign (=),
     Each sensor will have all its attributes in this format, with a new line (\n)
     separating each sensor. 
     For temperatures, the python script uses serial number to map that to a specific 
     sensor.
     Format of the arduino data is in the following form:
     Arduino variable name (e.g., Name=Temp1)
     Serial number (e.g., serial_num="28FF4A778016477")
     Value of the parameter (e.g., value=108.5)
     Units of the parameter (e.g., units=F)
     An example, using two temperature probes:
     name=Temp1,serial_num=blahblah1,value=55.55,units=F
     name=Temp2,serial_num=blahblah2,value=69.69,units=F
     If you change this format here, change it in the python script as well! */
  for (int i = 0; i < myTSensors.size(); i++)
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
  readAnalogPins();
  readDigitalPins();
}

void loop() 
{
  while(!Serial.available()) {}
  // serial read section
  while(Serial.available())
  {
    // Listens for an input from the USB port
    if (Serial.available() > 0) 
      {
      // Read the input from Python, which are
      // in the following format:
      // Switching pin statuses
      //   X=OFF or X=ON
      // where X is the pin number
      // Returning all information
      //   !
      char ch = Serial.read();
      readString += ch;
      // The character # is used to stop reading from serial
      if (ch == '!') 
        {
        returnAllInfo();
        readString="";
        }     
      if (ch == '#')
        {
          setPinStatus(readString);
          readString="";
        }
      }
  }
}


void setSwitchOnOff(int pin, String status_of_pin)
{
  if (status_of_pin == "ON") {
    digitalWrite(pin, HIGH);
  }
  else {
    digitalWrite(pin, LOW);
  }
}
