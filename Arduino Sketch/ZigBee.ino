#include <string.h>
int pin[3]={7,8,9};
int control[]={10,11};
int i,j,state=LOW;
int sensor_read(int pin);
void control_pin(int pin,int state);
void setup(){
   for(i=0;pin[i];i++){
   pinMode(pin[i],INPUT);
   }
   for(j=0;pin[j];j++){
   pinMode(control[i],OUTPUT);
   }
   Serial.begin(9600);
}
void loop(){
  int b;
  String x;
  String c,a=Serial.readStringUntil('*');
    
  if(a.substring(0,9) == "GPIO 1 ON")
  {
    digitalWrite(control[0],HIGH);
  }
  
  else if (a.substring(0,10)=="GPIO 1 OFF")
  {
    control_pin(control[0],LOW);
  }
  
  else if (a.substring(0,10)=="GPIO 2 ON")
  {
    control_pin(control[1],HIGH);
  }
  
  else if (a.substring(0,10)=="GPIO 2 OFF")
  {
    control_pin(control[1],LOW);
  }
  
  else if (a.substring(0,8)=="Read pin")
  {
        x=a.substring(9,10);
        j=x.toInt();     
        switch(j)
        {
          case 1:
              b=sensor_read(pin[0]);
              Serial.print(b);
              break;
          case 2:
              b=sensor_read(pin[1]);
              Serial.print(b);
              break;
          case 3:
              b=sensor_read(pin[2]);
              Serial.print(b);
              break;
          case 4:
              b=sensor_read(pin[3]);
              Serial.print(b);
              break; 
       }
  }
     
}
int sensor_read(int pin)
{
  int a ;
  a=digitalRead(pin);
  return a;
}
void control_pin(int pin,int state)
{
  digitalWrite(pin,state);
}

