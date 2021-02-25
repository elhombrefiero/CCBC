/*
 Name:		    BrewCode.ino
 Description:	Controls a series of heaters and pumps based on
				temperature sensor readings.
 Author:	    Rene Valdez
*/

#include "OneWire.h"
#include "DallasTemperature.h"

// Create a structure of a heater
struct Heater {
	char name[50] = "Heater";
	float setpoint_high = 32.0;
	float setpoint_low = 31.0;
	float setpoint_max = 212.0;
	uint8_t* tsensor;
	bool status = FALSE;
	bool has_sensor = FALSE;
	int data_pin = LED_BUILTIN;
};

// Define some constants
#define ONE_WIRE_PIN 10     // Data pin for the temperature sensors
#define MAX_TEMP_SENSORS 10 // TODO: Figure out way to define temp sensors in runtime
#define NUMBER_OF_HEATERS 3 // TODO: Figure out way to create heaters in runtime
#define MAX_SERIALINPUT 256

// Setup a OneWire instance to communicate with oneWire devices
OneWire oneWire(ONE_WIRE_PIN);

// Create a DallasTemperature instance which takes in
// a reference to the oneWire object.
DallasTemperature sensors(&oneWire);

// Array of Device Addresses
DeviceAddress myDAddresses[MAX_TEMP_SENSORS];

// Array to hold pointers to the device addresses
uint8_t* myTSensors[MAX_TEMP_SENSORS];

// Create an array of heaters
Heater myHeaters[NUMBER_OF_HEATERS];

// Create an integer that stores the number of tsensors
uint8_t number_of_sensors = 0;

// String that will keep incoming serial info.
char SerialInput[MAX_SERIALINPUT];

// Logical used for software override
bool controller_override = FALSE;

// Debug variables
uint8_t MAX_COUNTER = 10;
uint8_t counter = 0;
bool turnOn = FALSE;
bool DEBUG = FALSE;

void printTempSensors() {
	if (DEBUG) {
		Serial.println("Printing Temp Sensor info.");
	}
	for (uint8_t i = 0; i < number_of_sensors; i++) {
		Serial.print("<Tsensor:index=");
		Serial.print((String)i);
		Serial.print(";serial=");
		printAddress(myTSensors[i]);
		Serial.print(";cur_temp=");
		float tempF = sensors.getTempFByIndex(i);
		Serial.print(tempF);
		Serial.println(">");
	}
}

void switchPin(int pin_num) {
	int current_status = digitalRead(pin_num);

	if (current_status == LOW) {
		digitalWrite(pin_num, HIGH);
	}
	else {
		digitalWrite(pin_num, LOW);
	}
	delay(1);

}

void return_daddress(DeviceAddress deviceAddress, char* return_char_array) {
	uint8_t i, j;
	static char hex[17] = "0123456789ABCDEF";
	for (i = 0, j = 0; i < 8; i++) {
		return_char_array[j++] = hex[deviceAddress[i] / 16];
		return_char_array[j++] = hex[deviceAddress[i] & 15];
	}
	return_char_array[j] = '\0';
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

void heater_add_tsensor(int heater_index, uint8_t* ptsensor) {
	// Assigns the heater tsensor the pointer to a temperature sensor
	if (DEBUG) {
		Serial.print("Added ");
		printAddress(ptsensor);
		Serial.print(" to ");
		Serial.println(myHeaters[heater_index].name);
	}
	myHeaters[heater_index].has_sensor = TRUE;
	myHeaters[heater_index].tsensor = ptsensor;
}

void heater_remove_tsensor(int heater_index) {
	// Set the pin to INPUT and turn off the data pin before removing the tsensor
	digitalWrite(myHeaters[heater_index].data_pin, LOW);
	myHeaters[heater_index].status = FALSE;
	myHeaters[heater_index].data_pin = LED_BUILTIN;
	myHeaters[heater_index].tsensor = nullptr;
	myHeaters[heater_index].has_sensor = FALSE;
}

void heater_check_setpoints(Heater& heater) {
	// Get the latest temperature for the heater
	if (!heater.has_sensor) return;

	float tempF = 999.0; // Peg it high so it won't turn the heater on
	if (sensors.validAddress(heater.tsensor)) {
		tempF = sensors.getTempF(heater.tsensor);
	}
	else {
		if (DEBUG) {
		    Serial.print("Error: Address for heater ");
		    Serial.print(heater.name);
		    Serial.println(" invalid.");
		    }
		return;
	}
	int val = digitalRead(heater.data_pin);
	if (val == HIGH) {
		heater.status = TRUE;
		if (tempF > heater.setpoint_high || tempF > heater.setpoint_max) {
			digitalWrite(heater.data_pin, LOW);
			heater.status = FALSE;
		}
	}
	if (val == LOW) {
		heater.status = FALSE;
		if (tempF < heater.setpoint_low) {
			digitalWrite(heater.data_pin, HIGH);
			heater.status = TRUE;
		}
	}
}

void update_heater_setpoint_high(int heater_index, float new_setpoint_high) {
	myHeaters[heater_index].setpoint_high = new_setpoint_high;
}

void update_heater_setpoint_low(int heater_index, float new_setpoint_low) {
	myHeaters[heater_index].setpoint_low = new_setpoint_low;
}

void update_heater_setpoint_max(int heater_index, float new_setpoint_max) {
	myHeaters[heater_index].setpoint_max = new_setpoint_max;
}

void set_heater_pin(int heater_index, int new_pin) {
	pinMode(myHeaters[heater_index].data_pin, INPUT);

	pinMode(new_pin, OUTPUT);
	myHeaters[heater_index].data_pin = new_pin;
}

void update_heater_name(int heater_index, char* new_heater_name) {
	if (DEBUG) {
		Serial.print("In update_heater_name. new_heater_name: ");
		Serial.println(new_heater_name);
	}
	strncpy(myHeaters[heater_index].name, new_heater_name, 50);
	if (DEBUG) {
		Serial.print("Name of heater after strcpy: ");
		Serial.println(myHeaters[heater_index].name);
	}
}

void update_heater_pin(int heater_index, int new_heater_pin) {
	// Turn off the previous pin and set it to INPUT.
	digitalWrite(myHeaters[heater_index].data_pin, LOW);
	pinMode(myHeaters[heater_index].data_pin, INPUT);

	// Set the new heater pin
	myHeaters[heater_index].data_pin = new_heater_pin;
	pinMode(new_heater_pin, OUTPUT);
}

void update_heater_tsensor(int heater_index, char* new_tsensor) {
	if (DEBUG) {
		Serial.print("In update_heater_tsensor. new_tsensor: ");
		Serial.println(new_tsensor);
	}

	for (int i = 0; i < number_of_sensors; i++) {
		char tsensor_addy[17];
		tsensor_addy[0] = '\0';
		return_daddress(myTSensors[i], tsensor_addy);
		if (DEBUG) {
			Serial.print("tsensor_addy: ");
			Serial.println(tsensor_addy);
		}
		if (strcmp(tsensor_addy, new_tsensor) == 0) {
			if (DEBUG) {
				Serial.print("Tsensor index ");
				Serial.print(i);
				Serial.print(" matches: ");
				Serial.println(new_tsensor);
			}
			heater_add_tsensor(heater_index, myTSensors[i]);
		}
	}
}

void print_all_heater_info() {
	for (int i = 0; i < NUMBER_OF_HEATERS; i++) {
		print_heater_info(i);
	}
}

// function to print heater information
void print_heater_info(int i) {
	Serial.print("<heater:name=");
	Serial.print(myHeaters[i].name);
	Serial.print(";index=");
	Serial.print(i);
	Serial.print(";setpoint_high=");
	Serial.print(myHeaters[i].setpoint_high);
	Serial.print(";setpoint_low=");
	Serial.print(myHeaters[i].setpoint_low);
	Serial.print(":setpoint_max=");
	Serial.print(myHeaters[i].setpoint_max);
	Serial.print(";pin=");
	Serial.print(myHeaters[i].data_pin);
	Serial.print(";status=");
	Serial.print(myHeaters[i].status);
	if (myHeaters[i].has_sensor) {
		Serial.print(";tsensor_address=");
		printAddress(myHeaters[i].tsensor);
		Serial.print(";tsensor_temp=");
		float mytemp = sensors.getTempF(myHeaters[i].tsensor);
		Serial.print(mytemp);
	}
	Serial.println(">");
}

void init_temp_sensors() {
	for (int i = 0; i < number_of_sensors; i++) {
		if (DEBUG) {
			Serial.print("Creating temperature sensor ");
			Serial.println(i);
		}
		if (!sensors.getAddress(myTSensors[i], i))
		{
			Serial.print("Failed to create temp sensor ");
			Serial.println(i);
		}
		delay(10);
	}
}

void return_all_info() {
	// Temperature Sensors
	printTempSensors();
	// Heaters
	print_all_heater_info();

	// Pressure Sensors

	// Pumps
};

int identify_heater() {
	// Looks at the serial input string and returns the heater index

	// A -1 means the heater was not found
	int heater_index = -1;
	static const char name_key[] = "name";
	static const char index_key[] = "index";
	char name[16];
	char index[16];
	name[0] = '\0';
	index[0] = '\0';

	if (DEBUG) {
		Serial.print("In Identify heater. Looking for name and index. SerialInput: ");
		Serial.println(SerialInput);
	}

	look_for_key_return_val(name_key, name);

	if (name[0] != '\0') {
		if (DEBUG) {
			Serial.print("Found heater by name (");
			Serial.print(name);
			Serial.println(")!");
		}
		for (int i = 0; i < NUMBER_OF_HEATERS; i++) {

			if (strcmp(myHeaters[i].name, name) == 0) {
				if (DEBUG) {
					Serial.print("Index: ");
					Serial.println(i);
				}
				return i;
			}
		}
	}

	look_for_key_return_val(index_key, index);

	if (index[0] != '\0') {
		if (DEBUG) {
			Serial.println("Found heater by index: ");
			Serial.println(index);
		}
		heater_index = atoi(index);
		return heater_index;
	}
	return heater_index;
}

void look_for_key_return_val(const char* lookup, char* return_array) {
	/*
	Remove anything up to and including the colon (:)
		heater:name=name;tsensor_address=blahblah;
	Grab each key/value pairs between each semi-colon(;)
		name=name
		tsensor_address=blahblah
	Compare each key and return the value if it matches
	*/

	char* pair; // setpoint_upper=150.0
	char* key_value; // setpoint_upper, 150.0
	char* id;

	char sinput_copy[MAX_SERIALINPUT];
	strcpy(sinput_copy, SerialInput); // Use copy of serial input to avoid overwritting original

	if (DEBUG) {
		Serial.print("look_for_key_return_val. Looking for : ");
		Serial.print(lookup);
		Serial.print(" in: ");
		Serial.println(sinput_copy);
	}

	id = strchr(sinput_copy, ':');

	if (id != NULL)
	{
		// Found a colon. Replace that part of the string with a null and then move to the rest
		*id = 0;
		++id;
		pair = strtok(id, ";");
	}
	else
	{
		// Use the entire serial input string since there is no identifier.
		pair = strtok(sinput_copy, ";");
	}

	if (DEBUG) {
		Serial.print("In look_for_key_return_val. First token: "); // heater
		Serial.println(pair);
	}
	while (pair != NULL)
	{
		// make a copy of the entry
		char compare[100];
		strcpy(compare, pair);
		//if (DEBUG) {
		//	Serial.print("This is compare: ");
		//	Serial.println(compare);
		//}
		char* key_val = strchr(compare, '=');
		if (key_val != NULL) {
			*key_val = 0;
			//if (DEBUG) {
			//	Serial.print("key: ");
			//	Serial.println(compare);
			//}
			if (strcmp(compare, lookup) == 0) {
				//if (DEBUG) {
				//	Serial.println("Compare matched lookup!");
				//}
				++key_val;
				if (DEBUG) {
					Serial.print("Found key: ");
					Serial.print(lookup);
					Serial.print("\tVal: ");
					Serial.println(key_val);
				}
				strcpy(return_array, key_val);
				return;
			}
		}
		pair = strtok(NULL, ";");
		if (DEBUG) {
			Serial.print("In look_for_key_return_val. Subsequent token: ");
			Serial.println(pair);
		}
	}
	if (DEBUG) {
		Serial.print("Got to end of look_for_key_return_val. SerialInput: ");
		Serial.println(SerialInput);
	}
	return_array[0] = '\0'; // If it got to end, fill first item of return array with null
}

void determine_action() {
	/*
	The heater string will look like the following:
	heater:key=value;...#
	where one the following is required:
		index=<num>
		name=<hname>
	the rest are valid entries for that heater:
		setpoint_upper=<num>
		setpoint_lower=<num>
		setpoint_max=<num>
		tsensor_address=<address>
	*/
	static const char heater_txt[] = "heater";
	static const char heater_new_name[] = "new_name";
	static const char heater_new_pin[] = "new_pin";
	static const char setpt_high_key[] = "setpoint_high";
	static const char setpt_low_key[] = "setpoint_low";
	static const char setpt_max_key[] = "setpoint_max";
	static const char tsensor_key[] = "tsensor_address";

	// Return values will be put into the following array
	char return_val[50];
	return_val[0] = '\0';

	int hindex = -1;

	if (DEBUG) {
		Serial.print("In determine action. This is serial: ");
		Serial.println(SerialInput);
	}

	// if Serial input starts with heater, then
	if (strncmp(SerialInput, heater_txt, 6) == 0) {
		if (DEBUG) {
			Serial.println("Houston, we have a heater. Entered heater routine.");
		}
		// Get index of heater
		hindex = identify_heater();
		if (hindex == -1) { return; }

		if (DEBUG) {
			Serial.println("Identified heater: ");
			print_heater_info(hindex);
		}
		return_val[0] = '\0';
		// Update setpoint high if found
		look_for_key_return_val(setpt_high_key, return_val);
		if (return_val[0] != '\0') {
			float setpoint_high = atof(return_val);
			if (DEBUG) {
				Serial.print("In determine action. Found setpoint high: ");
				Serial.println(setpoint_high);
				Serial.print("This is return_val: ");
				Serial.println(return_val);
			}
			update_heater_setpoint_high(hindex, setpoint_high);
		}

		return_val[0] = '\0';
		// Update setpoint low if found
		look_for_key_return_val(setpt_low_key, return_val);
		if (return_val[0] != '\0') {
			float setpoint_low = atof(return_val);
			update_heater_setpoint_low(hindex, setpoint_low);
		}

		return_val[0] = '\0';
		// Update setpoint max if found
		look_for_key_return_val(setpt_max_key, return_val);
		if (return_val[0] != '\0') {
			float setpoint_max = atof(return_val);
			update_heater_setpoint_max(hindex, setpoint_max);
		}

		return_val[0] = '\0';
		// Update heater name if found
		look_for_key_return_val(heater_new_name, return_val);
		if (return_val[0] != '\0') {
			update_heater_name(hindex, return_val);
		}

		return_val[0] = '\0';
		// Update heater pin if found
		look_for_key_return_val(heater_new_pin, return_val);
		if (return_val[0] != '\0') {
			int new_pin = atoi(return_val);
			update_heater_pin(hindex, new_pin);
		}

		return_val[0] = '\0';
		// Update tsensor if found
		look_for_key_return_val(tsensor_key, return_val);
		if (return_val[0] != '\0') {
			update_heater_tsensor(hindex, return_val);
		}
	}
}

void process_incoming_byte(const byte inByte) {
	static unsigned int input_pos = 0;

	switch (inByte) {
	case '!': // display all information
		return_all_info();
		clean_serial();
		input_pos = 0;
		break;
	case '#':
		determine_action();
		clean_serial();
		input_pos = 0;
		break;
	default:
		if (input_pos < (MAX_SERIALINPUT - 1)) {
			SerialInput[input_pos++] = inByte;
		}
		break;
	}
}

void clean_serial() {
	for (int i = 0; i < MAX_SERIALINPUT-1; i++) {
		SerialInput[i] = '\0';
	}
}

void setup()
{
	Serial.begin(9600);
	while (!Serial);
	delay(10);
	Serial.flush();
	Serial.print("Beginning brew process...");
	Serial.println();

	// Put the pointers to the device addresses in the myTempSensor array
	for (int i = 0; i < MAX_TEMP_SENSORS; i++)
	{
		myTSensors[i] = myDAddresses[i];
	}

	// Setup the sensors and get the number on the bus
	sensors.begin();
	number_of_sensors = sensors.getDeviceCount();
	if (DEBUG) {
		Serial.print("Found ");
		Serial.print(number_of_sensors);
		Serial.println(" Temperature Sensors");
	}

	init_temp_sensors();

	// Initialize the heaters
	if (DEBUG) {
		for (int i = 0; i < NUMBER_OF_HEATERS; i++) {
			char hname[12] = "Heater ";
			char index[16];
			itoa(i, index, 10);
			strcat(hname, index);
			update_heater_name(i, hname);
		}
		for (int i = 0; i < 2; i++) {
			heater_add_tsensor(i, myTSensors[i]);
			update_heater_setpoint_high(i, 80.0);
			update_heater_setpoint_low(i, 79.0);
		}
		set_heater_pin(0, 4);
		set_heater_pin(1, 6);
	}
}

void loop()
{
	// Update the temperatures from every device
	sensors.requestTemperatures();

	// Run checks on heaters
	for (int i = 0; i < NUMBER_OF_HEATERS; i++) {
		heater_check_setpoints(myHeaters[i]);
	}

	// Look for input from serial
	while (Serial.available()) {
		process_incoming_byte(Serial.read());
	}

	// Check for new OneWire sensors
	//counter += 1;
	//if (counter > 200) {
	//	if (number_of_sensors != sensors.getDeviceCount()) {
	//		number_of_sensors = sensors.getDeviceCount();
	//		init_temp_sensors();
	//	}
	//	counter = 0;
	//}
	delay(5);
}