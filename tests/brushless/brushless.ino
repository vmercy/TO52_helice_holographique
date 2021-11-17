#include <Servo.h>

Servo myServo;

void setup(){
  myServo.attach(9,1000,2000);
  Serial.begin(9600);
}

int potVal = 0;

void loop(){
  potVal = analogRead(A0);
  int out = map(potVal,0,1023,0,180);
  Serial.println(out);
  myServo.write(out);
  delay(100);
}
