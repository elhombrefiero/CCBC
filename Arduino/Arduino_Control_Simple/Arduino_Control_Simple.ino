// Listens to inputs coming from the serial to
// simply open and shut switches (pins)



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
  Serial.print("Testing input to serial");
  Serial.println();
  
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