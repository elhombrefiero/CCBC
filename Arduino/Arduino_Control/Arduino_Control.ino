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
  if (!sensors.getAddress(T3, 2)) Serial.println("Unable to find address for Device 2");   
  if (!sensors.getAddress(T4, 3)) Serial.println("Unable to find address for Device 3");   
  if (!sensors.getAddress(T5, 4)) Serial.println("Unable to find address for Device 4");   
  if (!sensors.getAddress(T6, 5)) Serial.println("Unable to find address for Device 5");   
  if (!sensors.getAddress(T7, 6)) Serial.println("Unable to find address for Device 6");   
  if (!sensors.getAddress(T8, 7)) Serial.println("Unable to find address for Device 7");   
  if (!sensors.getAddress(T9, 8)) Serial.println("Unable to find address for Device 8");   

  // show address for devices
  Serial.print("Device 0 Address: ");
  printAddress(T1);
  Serial.println();
  Serial.print("Device 1 Address: ");
  printAddress(T2);
  Serial.println();
  Serial.print("Device 2 Address: ");
  printAddress(T3);
  Serial.println();
  Serial.print("Device 3 Address: ");
  printAddress(T4);
  Serial.println();
  Serial.print("Device 4 Address: ");
  printAddress(T5);
  Serial.println();
  Serial.print("Device 5 Address: ");
  printAddress(T6);
  Serial.println();
  Serial.print("Device 6 Address: ");
  printAddress(T7);
  Serial.println();
  Serial.print("Device 7 Address: ");
  printAddress(T8);
  Serial.println();
  Serial.print("Device 8 Address: ");
  printAddress(T9);
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
  float tempC1 = sensors.getTempCByIndex(0);
  float tempC2 = sensors.getTempCByIndex(1);
  float tempC3 = sensors.getTempCByIndex(2);
  float tempC4 = sensors.getTempCByIndex(3);
  float tempC5 = sensors.getTempCByIndex(4);
  float tempC6 = sensors.getTempCByIndex(5);
  float tempC7 = sensors.getTempCByIndex(6);
  float tempC8 = sensors.getTempCByIndex(7);
  float tempC9 = sensors.getTempCByIndex(8);

  Serial.print("name=Temp1,serial_num=");
  printAddress(T1);
  Serial.print(",value=");
  Serial.print(DallasTemperature::toFahrenheit(tempC1));
  Serial.print(",units=F#");
  Serial.print("name=Temp2,serial_num=");
  printAddress(T2);
  Serial.print(",value=");
  Serial.print(DallasTemperature::toFahrenheit(tempC2));
  Serial.print(",units=F#");
  Serial.print("name=Temp3,serial_num=");
  printAddress(T3);
  Serial.print(",value=");
  Serial.print(DallasTemperature::toFahrenheit(tempC3));
  Serial.print(",units=F#");
  Serial.print("name=Temp4,serial_num=");
  printAddress(T4);
  Serial.print(",value=");
  Serial.print(DallasTemperature::toFahrenheit(tempC4));
  Serial.print(",units=F#");
  Serial.print("name=Temp5,serial_num=");
  printAddress(T5);
  Serial.print(",value=");
  Serial.print(DallasTemperature::toFahrenheit(tempC5));
  Serial.print(",units=F#");
  Serial.print("name=Temp6,serial_num=");
  printAddress(T6);
  Serial.print(",value=");
  Serial.print(DallasTemperature::toFahrenheit(tempC6));
  Serial.print(",units=F#");
  Serial.print("name=Temp7,serial_num=");
  printAddress(T7);
  Serial.print(",value=");
  Serial.print(DallasTemperature::toFahrenheit(tempC7));
  Serial.print(",units=F#");
  Serial.print("name=Temp8,serial_num=");
  printAddress(T8);
  Serial.print(",value=");
  Serial.print(DallasTemperature::toFahrenheit(tempC8));
  Serial.print(",units=F#");
  Serial.print("name=Temp9,serial_num=");
  printAddress(T9);
  Serial.print(",value=");
  Serial.print(DallasTemperature::toFahrenheit(tempC9));
  Serial.println(",units=F#");  

  // A delay of 5 second works well for the interaction between Ard and rPi.
  // A faster time results in the rPi hanging (likely due to too much being sent through serial at once)
  delay(5000); // in milliseconds
  
}

void setSwitchOnOff(int pin, String status_of_pin)
{
  if (status_of_pin == "ON") {
    digitalWrite(pin, HIGH);
<<<<<<< HEAD
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
=======
    // Serial.print("Pin ");
    // Serial.print(pin);
    // Serial.print(" set to high");
    // Serial.println();
  }
  else {
    digitalWrite(pin, LOW);
    // Serial.print("Pin ");
    // Serial.print(pin);
    // Serial.print(" set to low");
    // Serial.println();
>>>>>>> Ready for ccbc
  }
}
