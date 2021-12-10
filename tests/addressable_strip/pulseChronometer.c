#include <wiringPi.h>
#include <stdio.h>
#include <sys/time.h>
#include <unistd.h>

int main()
{
  const int sensor = 2;
  struct timeval begin, end;
  //unsigned long ts.tv_nsec
  //wiringPiSetup();
  //pinMode(sensor, INPUT);

  gettimeofday(&begin, 0);
  sleep(1);
  gettimeofday(&end, 0);

  long microseconds = end.tv_usec-begin.tv_usec;

  printf("microseconds elapsed : %.3f", microseconds);

  return 0;
}