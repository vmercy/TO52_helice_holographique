/*
  blinkanim.c: Display a line
*/

#include "apa102.h"
#include <wiringPi.h>

int main()
{
  // Initialize strip
  int sensorPin = 2;
  wiringPiSetup();
  pinMode(sensorPin, INPUT);
  struct APA102 *strip = APA102_Init(20, 0);
  struct APA102 *strip2 = APA102_Init(20, 1);
  struct APA102_Frame* LineFrame = APA102_CreateFrame(31, 0xFF, 0xFF, 0);
  struct APA102_Frame* offFrame = APA102_CreateFrame(0x00, 0x00, 0x00, 0x00);
  while (1)
  {
    if (digitalRead(sensorPin))
    {
      APA102_Fill(strip, LineFrame);
      APA102_Fill(strip2, LineFrame);
      APA102_Fill(strip, offFrame);
      APA102_Fill(strip2, offFrame);
    }

  }
  // Delay and kill
  delay(10000);
}