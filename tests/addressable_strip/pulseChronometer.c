#include <wiringPi.h>
#include <stdio.h>
#include <sys/time.h>
#include <unistd.h>

int main()
{
  const int sensor = 2;
  struct timeval begin, end;
  wiringPiSetup();
  pinMode(sensor, INPUT);
  usleep(1000);
  while(!digitalRead(sensor));
  gettimeofday(&begin, 0);
  while(digitalRead(sensor));
  usleep(1000);
  while(!digitalRead(sensor));
  gettimeofday(&end, 0);

  long seconds = end.tv_sec - begin.tv_sec;
  long microseconds = end.tv_usec-begin.tv_usec;
  double elapsed = seconds*1e6 + microseconds;
  printf("microseconds elapsed : %4.2f", elapsed);

  return 0;
}