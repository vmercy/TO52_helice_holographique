#include <stdio.h>
#include "logo_utbm.h"

#define NB_SECTORS 10
#define NB_LEDS_PER_STRIP 48

#define NB_COLOR_POINTS 960

int main()
{
  int v[][5] = COLOR_POINTS;
  for (int i = 0; i < NB_COLOR_POINTS; i++)
  {
    printf("Color point : thetaIndex = %i, radialIndex = %i, r=%i,g=%i,b=%i\n", v[i][0], v[i][1], v[i][2], v[i][3], v[i][4]);
  }
  return 0;
}