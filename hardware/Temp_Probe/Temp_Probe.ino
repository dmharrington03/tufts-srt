#include <OneWire.h>
#include <DallasTemperature.h>

// Data wire is connteced to digital pin 5 on ESP32 (CHANGE THIS IF DIFFERENT PIN BEING USED!!)
#define ONE_WIRE_BUS 5

// Setup a oneWire instance to communicate with any OneWire devices
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature sensor 
DallasTemperature sensors(&oneWire);

void setup(void)
{
  // Start serial communication to transmit data (make sure baud rate matches that being used in daemon.py)
  Serial.begin(9600);
  sensors.begin();
}

void loop(void){ 
  // Call sensors.requestTemperatures() to issue a global temperature and Requests to all devices on the bus
  sensors.requestTemperatures(); 
  // Print data in celcius
  Serial.print(sensors.getTempCByIndex(0)); 
  // Make sure delay matches that being used in daemon.py
  delay(500);
}
