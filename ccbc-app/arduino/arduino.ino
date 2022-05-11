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


void controlPump(String cmd) {
  // Trim "pump=" from string.
  cmd.remove(0, 5);

  // Get index of equal sign.
  int equalIndex = cmd.indexOf("=");

  // Get pin number to left of equal sign.
  int pinNumber = cmd.substring(0, equalIndex).toInt();

  // Get status to right of equal sign.
  String status = cmd.substring(equalIndex + 1);

  // Convert status to lower case.
  status.toLowerCase();

  // Turn pump on or off.
  if (status == "true") {
    digitalWrite(pinNumber, HIGH);
  } else {
    digitalWrite(pinNumber, LOW);
  }

}


void setup() {
    // put your setup code here to run once
    // sensors.begin();
    Serial.begin(9600);
    pinMode(pump1, OUTPUT);
    pinMode(pump2, OUTPUT);
    pinMode(pump3, OUTPUT);
}


void loop() {
    // put your main code here to run repeatedly
    if (Serial.available() > 0) {

        String command = Serial.readString();

        if (command.startsWith("pump")) {
          controlPump(command);
        } else {
          Serial.println("DO NOTHING");
        }

        delay(500);

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
        //char ch = Serial.read();
        //Serial.println(ch);
        

        
        //readString += ch;
        // The character # is used to stop reading from serial
        //if (ch == '#')
        //    {
        //    setPinStatus(readString);
        //    readString="";
        //    }
    }
}
