#include "DSerial.h"

DSerial serial;
void setup()
{
  serial = DSerial(9600);
}

void loop()
{
  if(serial.getCommand())
    Serial.println(serial.getCommandData());
  if(serial.getCommand())
    Serial.println(serial.getCommandData());
}


