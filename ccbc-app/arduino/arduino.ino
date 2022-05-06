#define pump1 13

void setup() {
    // put your setup code here to run once
    Serial.begin(9600);
    pinMode(pump1, OUTPUT);
}

void loop() {
    // put your main code here to run repeatedly
    if (Serial.available()) {

        String command = Serial.readString();

        if (command == "ON") {
            digitalWrite(pump1, HIGH);
        } else if (command == "OFF") {
            digitalWrite(pump1, LOW);
        } else {
            Serial.println("Invalid command. Supply ON or OFF.");
        }
    }
}
