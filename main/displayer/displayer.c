/*
  displayer.c: Display an image
*/

#include "apa102.h"
#include <wiringPi.h>
#include <stdio.h>
#include <signal.h>

#define SENSOR_PIN 2
#define MOTOR_PIN 22
#define BUZZER_PIN 3

#include "sequenced_image.h"

#define NB_SECTORS_MAX 30
#define NB_LEDS_PER_STRIP_MAX 35

#define NB_COLOR_POINTS_MAX (NB_SECTORS_MAX * NB_LEDS_PER_STRIP_MAX * 2)

void writeFrameAllStrips(struct APA102 *strip, struct APA102 *strip2, uint8_t colorsStrip[][3], uint8_t colorsStrip2[][3])
{
  for (uint8_t i = 0; i < NB_LEDS_PER_STRIP_MAX; i++)
  {
    APA102_FillWithDifferentColors(strip, colorsStrip);
    APA102_FillWithDifferentColors(strip2, colorsStrip2);
  }
}

void writeFrame(struct APA102 *strip, struct APA102 *strip2, struct APA102_Frame *frame)
{
  APA102_Fill(strip, frame);
  APA102_Fill(strip2, frame);
}

void handle_sigint()
{
  struct APA102 *strip = APA102_Init(48, 0);
  struct APA102 *strip2 = APA102_Init(48, 1);
  struct APA102_Frame *offFrame = APA102_CreateFrame(0x00, 0x00, 0x00, 0x00);
  writeFrame(strip, strip2, offFrame);
  //digitalWrite(MOTOR_PIN, LOW);
  exit(0);
}

void startMotor()
{
  //digitalWrite(MOTOR_PIN, HIGH);
}

int main(int argc, char *argv[])
{

  if(argc!=3)
  {
    printf('There must be exactly 2 arguments supplied : angular resolution and radial resolution.');
    exit(0);
  }

  //TODO: add checks (2 aguments must be >0 and inferior to their respective limits)
  int nbSectorsUsed = atoi(argv[1]); //angular resolution
  int nbLedsUsed = atoi(argv[2]); //radial resolution

  int nbColorPoints = 2*nbSectorsUsed*nbLedsUsed;

  // Initialize strip
  signal(SIGINT, handle_sigint);

  wiringPiSetup();
  pinMode(SENSOR_PIN, INPUT);
  //pinMode(MOTOR_PIN, OUTPUT);
  startMotor();
  struct APA102 *strip = APA102_Init(nbLedsUsed, 0);
  struct APA102 *strip2 = APA102_Init(nbLedsUsed, 1);
  struct APA102_Frame *offFrame = APA102_CreateFrame(0x00, 0x00, 0x00, 0x00);
  writeFrame(strip, strip2, offFrame);
  strip = APA102_Init(nbLedsUsed, 0);
  strip2 = APA102_Init(nbLedsUsed, 1);
  struct APA102_Frame *red = APA102_CreateFrame(31, 255, 0, 0);
  struct APA102_Frame *green = APA102_CreateFrame(31, 0, 255, 0);

  uint8_t colorsForStrip[NB_SECTORS_MAX][NB_LEDS_PER_STRIP_MAX][3];
  uint8_t colorsForStrip2[NB_SECTORS_MAX][NB_LEDS_PER_STRIP_MAX][3];

  int colorPoints[][5] = COLOR_POINTS;
  for (int i = 0; i < nbColorPoints; i++)
  {
    uint8_t sectorIndex = colorPoints[i][0];
    int rIndex = colorPoints[i][1];
    if (rIndex >= 0)
    {
      colorsForStrip[sectorIndex][rIndex][0] = colorPoints[i][2];
      colorsForStrip[sectorIndex][rIndex][1] = colorPoints[i][3];
      colorsForStrip[sectorIndex][rIndex][2] = colorPoints[i][4];
    }
    else
    {
      rIndex = -rIndex;
      colorsForStrip2[sectorIndex][rIndex][0] = colorPoints[i][2];
      colorsForStrip2[sectorIndex][rIndex][1] = colorPoints[i][3];
      colorsForStrip2[sectorIndex][rIndex][2] = colorPoints[i][4];
    }
  }

  while (1)
  {
    if (digitalRead(SENSOR_PIN))
    {
      for (uint8_t sector = 0; sector < nbSectorsUsed; sector++)
      {
          APA102_FillWithDifferentColors(strip, colorsForStrip[sector]);
          APA102_FillWithDifferentColors(strip2, colorsForStrip2[sector]);
      }
      writeFrame(strip, strip2, offFrame);
    }
  }
}