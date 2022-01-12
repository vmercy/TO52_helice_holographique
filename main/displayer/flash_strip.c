/*
  blinkanim.c: Plays an animation on static LED strip selected from command-line
*/

#include <stdio.h>
#include "apa102.h"
#include <stdlib.h>
#include <signal.h>
#include "string.h"
#include "time.h"

#define NB_LEDS_PER_STRIP 48

void writeFrameAllStrips(struct APA102 *strip, struct APA102 *strip2, uint8_t colorsStrip[][3], uint8_t colorsStrip2[][3])
{
  for (uint8_t i = 0; i < NB_LEDS_PER_STRIP; i++)
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

int main(int argc, char *argv[])
{
   if( argc == 3 ) {
      printf("The color argument supplied is %s and delay is %s\n", argv[1], argv[2]);
   }
   else if( argc > 3 ) {
      printf("Too many arguments supplied. Expected arguments are a string describing color (red, yellow or green) and a delay in ms\n");
      exit(0);
   }
   else {
      printf("2 argument expected : color as string and delay as integer.\n");
      exit(0);
   }

   printf("before delay assignment\n");

  int color = atoi(argv[1]);
   int delay = atoi(argv[2]);

   printf("after delay assignment : delay = %i\n",delay);


 if(delay<0)
   {
     printf("Delay must be non-negative.\n");
     exit(0);
   }

   printf("Im here\n");

   int isRed = (color==0);
   int isYellow = (color==1);
   int isGreen = (color==2);

   printf("Colors : %i %i %i",isRed, isYellow, isGreen);

  if(!isRed && !isYellow && !isGreen)
  {
    printf("Unauthorized color supplied. Authorized colors are : red, yellow and green");
    exit(0);
  }

  struct APA102 *strip = APA102_Init(NB_LEDS_PER_STRIP, 0);
  struct APA102 *strip2 = APA102_Init(NB_LEDS_PER_STRIP, 1);
  struct APA102_Frame *offFrame = APA102_CreateFrame(0x00, 0x00, 0x00, 0x00);
  strip = APA102_Init(NB_LEDS_PER_STRIP, 0);
  strip2 = APA102_Init(NB_LEDS_PER_STRIP, 1);
  struct APA102_Frame *color = APA102_CreateFrame(31, (isRed||isYellow) ? 255 : 0, (isGreen||isYellow) ? 255 : 0 , 0);

  writeFrame(strip, strip2, color);

  sleep(delay);

  writeFrame(strip, strip2, offFrame);

  return 0;
}