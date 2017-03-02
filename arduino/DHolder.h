//created: 2017/2/22 dou

#include <Arduino.h>
#include <Servo.h> 

class DHolder
{
  private:
    int holder_1_pin;
    int holder_2_pin;
    Servo holder_1; 
    Servo holder_2; 

  public:
    void setPin(int pin_1, int pin_2);
    void holder_1_run(int data=255);
    void holder_2_run(int data=255);
  };

void DHolder::setPin(int pin_1, int pin_2)
{
  this->holder_1_pin = pin_1;
  this->holder_2_pin = pin_2;
  holder_1.attach(pin_1);
  holder_2.attach(pin_2);
  holder_1.write(90);
  holder_2.write(90);
  }

void DHolder::holder_1_run(int data)
{
  holder_1.write(data);
  }


void DHolder::holder_2_run(int data)
{
  holder_2.write(data);
  }
