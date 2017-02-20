#include "DSerial.h"
#include "DCommand.h"
#include "DMoto.h"

DSerial serial;
DMoto moto;
void setup()
{
  serial.setBuadRate(9600);
  moto.setPin(8, 7, 3, 4, 2, 5);
}

void loop()
{
   while (true)
   {
      if (serial.getCommand())
        {
          switch (serial.getCommandId())
          {
              case l_moto_id:
                moto.l_moto_run(serial.getCommandData());
                break;
              case r_moto_id:
                moto.r_moto_run(serial.getCommandData());
                break; 
              default:
                break;
            }
          }
    } 
}


