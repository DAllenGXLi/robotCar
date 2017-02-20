//created: 2017/2/17 dou
//modified: 2017/2/17 dou
//member：
//command 当前command
//function:
//getCommand(): 获取串口信息，如果信息获取错误，返回false，command记录在类成员中
//getCommandId：从当前获取的command中读取id
//getCommandData：从当前command中读取data
//waitForCommand：主要是为了阻塞等待数据

#include <Arduino.h>


//此类封装串口，负责获取通讯命令
//提供提取信息，校验信息等接口

class DSerial
{
  private:
    char command[8];
    bool checkCommand();
    void resetCommand();
  public:
    DSerial(int buadrate=9600);
    void setBuadRate(int buadrate=9600);
    bool getCommand();
    int getCommandId();
    int getCommandData();
    char getCommandChar(int loc); //测试用
  };



DSerial::DSerial(int buadrate)
{
  this->resetCommand();
  }



void DSerial::setBuadRate(int buadrate)
{
  Serial.begin(buadrate);
  }


void DSerial::resetCommand()
{
  for (int i=0; i<8; i++)
    this->command[i] = '0';
  }



//接收通讯指令，并且校验通讯指令
//如果校验失败，则清空缓存，并且返回false
//无论校验是否成功，都会写入command中
bool DSerial::getCommand()
{
  int count = 0;
  char data;
  char comm[8];
  // wait for input
  while (Serial.available()<=0)
    delay(5);
  delay(5);
  
  if (Serial.available()>=8 && char(Serial.read())=='*')
  {
    this->command[count++] = '*';
    for (; count<8; count++)
      {
        delay(2);
        this->command[count] = char(Serial.read());
        }
     if (this->checkCommand())
     {
         return true;
      }
      else 
      {
        this->resetCommand();
        return false;
        }
    }
  this->resetCommand();
  Serial.flush();  
  return false;
 }



//从当前command中提取指令id
int DSerial::getCommandId()
{
  int id = (this->command[1]-'0')*10+(this->command[2]-'0');
  return id;
  }



//从当前command中提取指令数据
int DSerial::getCommandData()
{
  int data = (this->command[3]-'0')*1000+(this->command[4]-'0')*100+(this->command[5]-'0')*10+(this->command[6]-'0');
  return data;
  }



//从当前command提取指令的特定字节，测试用
char DSerial::getCommandChar(int loc)
{
    return this->command[loc];
  }

  

// 校验当前指令是否符合格式
bool DSerial::checkCommand()
{
  if (this->command[0]!='*' || this->command[7]!='#')
  {
    return false;
    }
  for (int i=1; i<7; i++)
  {
      if (this->command[i]>'9' || this->command[i]<'0')
      {
        return false;
        }
    }
   return true;
  }








