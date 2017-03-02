#include "DSerial.h"
#include "DCommand.h"
#include "DMoto.h"
#include "DHolder.h"

DSerial serial;
DMoto moto;
DHolder holder;
void setup()
{
  serial.setBuadRate(9600);
  moto.setPin(8, 7, 6, 13, 12, 11);
  holder.setPin(9, 10);
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
                Serial.println(serial.getCommandData());
                break;
              case r_moto_id:
                moto.r_moto_run(serial.getCommandData());
                Serial.println(serial.getCommandData());
                break; 
//              case holder_1_id:
//                holder.holder_1_run(serial.getCommandData());
//                Serial.println(serial.getCommandData());
//                break;
//              case holder_2_id:
//                holder.holder_2_run(serial.getCommandData());
//                Serial.println(serial.getCommandData());
//                break;
              default:
                break;
            }
          }
    } 
}


