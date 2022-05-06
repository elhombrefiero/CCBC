#define pump1 9
#define pump2 8
#define pump3 7

// Strings used to send and receive through serial
String readString;
String pinStatus;

void setup() {
    // put your setup code here to run once
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
    if (Serial.available()) {
        // String command = Serial.readString();

        // if (command == "ON") {
        //     digitalWrite(pump1, HIGH);
        // } else if (command == "OFF") {
        //     digitalWrite(pump1, LOW);
        // } else {
        //     Serial.println("Invalid command. Supply ON or OFF.");
        // }

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
