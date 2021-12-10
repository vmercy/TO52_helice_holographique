//#include <wiringPi.h>
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
  usleep(500000);
  gettimeofday(&end, 0);

  long seconds = end.tv_sec - begin.tv_sec;
  long microseconds = end.tv_usec-begin.tv_usec;
  double elapsed = seconds*1e6 + microseconds;
  printf("microseconds elapsed : %4.2f", elapsed);

  return 0;
}