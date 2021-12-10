#include <time.h>
#include <unistd.h>
#include <stdio.h>


int main(){
  clock_t begin = clock();
  sleep(1);
  clock_t end = clock();
  double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
  printf("%f\n", time_spent);
  return 0;
}