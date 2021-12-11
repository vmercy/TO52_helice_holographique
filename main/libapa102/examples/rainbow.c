/*
  blinkanim.c: Display a line
*/

#include "apa102.h"
#include <wiringPi.h>

void writeFrame(strip, strip2, frame)
{
  APA102_Fill(strip, frame);
  APA102_Fill(strip2, frame);
}

int main()
{
  // Initialize strip
  int sensorPin = 2;
  wiringPiSetup();
  pinMode(sensorPin, INPUT);
  struct APA102 *strip = APA102_Init(20, 0);
  struct APA102 *strip2 = APA102_Init(20, 1);
  struct APA102_Frame* offFrame = APA102_CreateFrame(0x00, 0x00, 0x00, 0x00);
  struct APA102_Frame* red = APA102_CreateFrame(31, 255, 0, 0);
  struct APA102_Frame* orange = APA102_CreateFrame(31, 255, 127, 0);
  struct APA102_Frame* yellow = APA102_CreateFrame(31, 255, 255, 0);
  struct APA102_Frame* green = APA102_CreateFrame(31, 0, 255, 0);
  struct APA102_Frame* blue = APA102_CreateFrame(31, 0, 0, 255);
  struct APA102_Frame* indigo = APA102_CreateFrame(31, 46, 43, 95);
  struct APA102_Frame* violet = APA102_CreateFrame(31, 139, 0, 255);
  while (1)
  {
    if (digitalRead(sensorPin))
    {
      writeFrame(strip, strip2, red);
      writeFrame(strip, strip2, orange);
      writeFrame(strip, strip2, yellow);
      writeFrame(strip, strip2, green);
      writeFrame(strip, strip2, blue);
      writeFrame(strip, strip2, indigo);
      writeFrame(strip, strip2, violet);
      writeFrame(strip, strip2, offFrame);
    }

  }
  // Delay and kill
  delay(10000);
}