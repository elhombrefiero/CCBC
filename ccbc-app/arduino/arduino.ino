// #include <OneWire.h>
// #include <DallasTemperature.h>

#define pump1 9
#define pump2 8
#define pump3 7
#define hot_water_heater 2

// Setup a oneWire instance to communicate with any OneWire device
// OneWire oneWire(hot_water_heater);

// Pass oneWire reference to DallasTemperature library
// DallasTemperature sensors(&oneWire);

// Strings used to send and receive through serial
String readString;
String pinStatus;

void setup() {
    // put your setup code here to run once
    // sensors.begin();
    Serial.begin(9600);
    pinMode(pump1, OUTPUT);
    pinMode(pump2, OUTPUT);
    pinMode(pump3, OUTPUT);
}

// Function copied from Rene.
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

// Function copied from Rene.
void setSwitchOnOff(int pin, String status_of_pin) {
  if (status_of_pin == "ON") {
    digitalWrite(pin, HIGH);
  }
  else {
    digitalWrite(pin, LOW);
  }
}

void loop() {
    // put your main code here to run repeatedly
    if (Serial.available() > 0) {

        // Send the command to get temperatures
        // sensors.requestTemperatures(); 

        // Print the temperature in Fahrenheit
        // Serial.print((sensors.getTempCByIndex(0) * 9.0) / 5.0 + 32.0);
        // Serial.println("F");
        
        // delay(500);

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
        if (ch == '#')
            {
            setPinStatus(readString);
            readString="";
            }
    }
}
