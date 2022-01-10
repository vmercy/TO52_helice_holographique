/*
  blinkanim.c: Display a line

  RESULT OF COUNT :
    - 20 sectors for 20 leds
    - 12 sectors for 48 leds
*/

#include "apa102.h"
#include <wiringPi.h>
#include <stdio.h>
#include <signal.h>

#define SENSOR_PIN 2
#define MOTOR_PIN 22
#define MAX_LEDS_PER_STRIP 48
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
  signal(SIGINT, handle_sigint);
  int nbSectors = 0, nbLedsPerStrip;
  printf("Saisir un nombre de secteurs : ");
  scanf("%i",&nbSectors);
  printf("\nSaisir un nombre de LEDS a utiliser par bandeau (max : %i) : ",MAX_LEDS_PER_STRIP);
  scanf("%i",&nbLedsPerStrip);
  while(nbLedsPerStrip>MAX_LEDS_PER_STRIP)
  {
    printf("\nSaisir un nombre de LEDS a utiliser par bandeau (MAX : %i) : ",MAX_LEDS_PER_STRIP);
    scanf("%i",&nbLedsPerStrip);
  }
  wiringPiSetup();
  pinMode(SENSOR_PIN, INPUT);
  pinMode(MOTOR_PIN, OUTPUT);
  startMotor();
  struct APA102 *strip = APA102_Init(nbLedsPerStrip, 0);
  struct APA102 *strip2 = APA102_Init(nbLedsPerStrip, 1);
  struct APA102_Frame* offFrame = APA102_CreateFrame(0x00, 0x00, 0x00, 0x00);
  writeFrame(strip, strip2, offFrame);
  strip = APA102_Init(nbLedsPerStrip, 0);
  strip2 = APA102_Init(nbLedsPerStrip, 1);
  struct APA102_Frame* red = APA102_CreateFrame(31, 255, 0, 0);
  struct APA102_Frame* green = APA102_CreateFrame(31, 0, 255, 0);
  while (1)
  {
    if (digitalRead(SENSOR_PIN))
    {
      for(uint8_t i=0; i<nbSectors; i++)
        writeFrame(strip, strip2, i%2 ? red : green);
      writeFrame(strip, strip2, offFrame);
    }
  }
}