/*
  blinkanim.c: Display a line
*/

#include "apa102.h"
#include <wiringPi.h>
#include <stdio.h>
#include <signal.h>

#define SENSOR_PIN 2
#define MOTOR_PIN 22
#define BUZZER_PIN 3

void writeFrame(struct APA102* strip,struct  APA102* strip2,struct  APA102_Frame* frame)
{
  APA102_Fill(strip, frame);
  APA102_Fill(strip2, frame);
}

void handle_sigint()
{
  struct APA102 *strip = APA102_Init(48, 0);
  struct APA102 *strip2 = APA102_Init(48, 1);
  struct APA102_Frame* offFrame = APA102_CreateFrame(0x00, 0x00, 0x00, 0x00);
  writeFrame(strip, strip2, offFrame);
  digitalWrite(MOTOR_PIN, LOW);
}

void startMotor(){
  digitalWrite(MOTOR_PIN, HIGH);
}

int main()
{
  // Initialize strip
  int sectorDelay = 0;
  printf("Saisir un delai (en microsecondes) entre chaque secteur : ");
  scanf("%i",&sectorDelay);
  wiringPiSetup();
  pinMode(SENSOR_PIN, INPUT);
  pinMode(MOTOR_PIN, OUTPUT);
  startMotor();
  struct APA102 *strip = APA102_Init(48, 0);
  struct APA102 *strip2 = APA102_Init(48, 1);
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
    if (digitalRead(SENSOR_PIN))
    {
      writeFrame(strip, strip2, red);
      delayMicroseconds(sectorDelay);
      writeFrame(strip, strip2, orange);
      delayMicroseconds(sectorDelay);
      writeFrame(strip, strip2, yellow);
      delayMicroseconds(sectorDelay);
      writeFrame(strip, strip2, green);
      delayMicroseconds(sectorDelay);
      writeFrame(strip, strip2, blue);
      delayMicroseconds(sectorDelay);
      writeFrame(strip, strip2, indigo);
      delayMicroseconds(sectorDelay);
      writeFrame(strip, strip2, violet);
      delayMicroseconds(sectorDelay);
      writeFrame(strip, strip2, offFrame);
      delayMicroseconds(sectorDelay);
    }

  }
  
}