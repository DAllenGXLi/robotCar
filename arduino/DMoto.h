//created: 2017/2/20 dou



#include <Arduino.h>

// 此类接受6个参数作为初始
// 分别对应ln298上面的IN1，IN2，ENA, IN3, IN4, ENB
// 接收标准协议控制信号处理输出

class DMoto
{
  private:
    int IN1;
    int IN2;
    int IN3;
    int IN4;
    int ENA;
    int ENB;
  public:
    DMoto();
    void setPin(int IN1, int IN2, int ENA, int IN3, int IN4, int ENB);
    void l_moto_run(int data=255);
    void r_moto_run(int data=255);
  };

DMoto::DMoto()
{
  }

void DMoto::setPin(int IN1, int IN2, int ENA, int IN3, int IN4, int ENB)
{
  this->IN1 = IN1;
  this->IN2 = IN2;
  this->IN3 = IN3;
  this->IN4 = IN4;
  this->ENA = ENA;
  this->ENB = ENB;
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  }

void DMoto::l_moto_run(int data) 
{
  if (data>=255)
  {
    Serial.println(data-255);
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    analogWrite(ENA, data-255);
    }
  if (data<255)
  {
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    analogWrite(ENA, 255-data);
    }
  }

void DMoto::r_moto_run(int data) 
{
  if (data>=255)
  {
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    analogWrite(ENB, data-255);
    }
  if (data<255)
  {
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
    analogWrite(ENB, 255-data);
    }
  }

  
