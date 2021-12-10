#include <wiringPi.h>
#include <stdio.h>
#include <time.h>

int main()
{
  const int sensor = 2;
  struct timespec ts;
  //unsigned long ts.tv_nsec
  wiringPiSetup();
  pinMode(sensor, INPUT);

  while (1)
  {
    
  }
  

  return 0;
}