/*
  blinkanim.c: Runs a blinking animation for 2 seconds
*/

#include <apa102.h>
#include <wiringPi.h>

int main() {
  //Initialize strip
  struct APA102* strip = APA102_Init(20,0);
  struct APA102* strip2 = APA102_Init(20,1);

  //Run animation
  struct APA102_Animation* anim = APA102_BlinkAnimation(strip, strip2, APA102_CreateFrame(31, 0xFF, 0x0, 0x0), 50, 115);

  //Delay and kill
  delay(10000);
  APA102_KillAnimation(anim);
}