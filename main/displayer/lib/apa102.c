#include "apa102.h"

#include <stdio.h>
#include <stdlib.h>

#include <wiringPi.h>
#include <wiringPiSPI.h>

struct APA102 {
  int n_leds;
  int interface;
};

struct APA102_Frame* APA102_CreateFrame(uint8_t brightness, uint8_t r, uint8_t g, uint8_t b) {
  struct APA102_Frame* led;

  led = (struct APA102_Frame*)malloc(sizeof(struct APA102_Frame));

  led->brightness = brightness;
  led->r = r;
  led->g = g;
  led->b = b;
  return led;
}

struct APA102* APA102_Init(int n_leds, int interface) {
  struct APA102* strip;

  strip = (struct APA102*)malloc(sizeof(struct APA102));
  strip->n_leds = n_leds;
  strip->interface = interface;

  wiringPiSetup();
  if(wiringPiSPISetup(interface, 6000000) < 0) {
    printf("WiringPiSPISetup failed\n");
    return 0;
  }
  return strip;
}

void APA102_Begin(int interface) {
  uint8_t buf[1];
  int i;

  for(i = 0; i < 4; i++) {
    buf[0] = 0x00;
    wiringPiSPIDataRW(interface, buf, 1);
  }
}

void APA102_End(int interface) {
  uint8_t buf[1];
  int i;

  for(i = 0; i < 4; i++) {
    buf[0] = 0xFF;
    wiringPiSPIDataRW(interface, buf, 1);
  }
}

void APA102_WriteLED(struct APA102_Frame* led, int interface) {
  uint8_t led_frame[4];

  if(led->brightness > 31) {
    led->brightness = 31;
  }

  led_frame[0] = 0b11100000 | (0b00011111 & led->brightness);
  led_frame[1] = led->b;
  led_frame[2] = led->g;
  led_frame[3] = led->r;

  wiringPiSPIDataRW(interface, led_frame, 4);
}

void APA102_Fill(struct APA102* strip, struct APA102_Frame* led) {
  uint8_t led_frame[4];
  int i;

  if(led->brightness > 31) {
    led->brightness = 31;
  }

  APA102_Begin(strip->interface);
  for(i = 0; i < strip->n_leds; i++) {
    led_frame[0] = 0b11100000 | (0b00011111 & led->brightness);
    led_frame[1] = led->b;
    led_frame[2] = led->g;
    led_frame[3] = led->r;

    wiringPiSPIDataRW(strip->interface, led_frame, 4);
  }
  APA102_End(strip->interface);
}

void APA102_FillWithDifferentColors(struct APA102* strip, uint8_t colors[][3]) {
  uint8_t led_frame[4];
  int i;

  APA102_Begin(strip->interface);
  for(i = 0; i < strip->n_leds; i++) {
    led_frame[0] = 0b11100000 | (0b00011111 & 31);
    led_frame[1] = colors[i][2];
    led_frame[2] = colors[i][1];
    led_frame[3] = colors[i][0];

    wiringPiSPIDataRW(strip->interface, led_frame, 4);
  }
  APA102_End(strip->interface);
}

void APA102_Stripes(struct APA102* strip, struct APA102_Frame* led, int stripe_size, int gap_size, int offset) {
  uint8_t led_frame[4];
  int i, ctr;

  ctr = offset;
  if(ctr < 0) {
    ctr = 0;
  }

  while(ctr > gap_size + stripe_size) {
    ctr -= gap_size+stripe_size;
    if(ctr < 0) {
      ctr = 0;
    }
  }

  if(led->brightness > 31) {
    led->brightness = 31;
  }

  APA102_Begin(strip->interface);
  for(i = 0; i < strip->n_leds; i++) {
    if(ctr < stripe_size) {
      led_frame[0] = 0b11100000 | (0b00011111 & led->brightness);
      led_frame[1] = led->b;
      led_frame[2] = led->g;
      led_frame[3] = led->r;
    } else {
      led_frame[0] = 0b11100000;
      led_frame[1] = 0x00;
      led_frame[2] = 0x00;
      led_frame[3] = 0x00;
    }

    wiringPiSPIDataRW(strip->interface, led_frame, 4);

    ctr++;
    if(ctr >= stripe_size + gap_size) {
      ctr = 0;
    }
  }
  APA102_End(strip->interface);
}

void APA102_MultiStripes(struct APA102* strip, struct APA102_Frame** leds, int stripe_size, int gap_size, int offset, int coffset) {
  uint8_t led_frame[4];
  int i, ctr, cctr, clen;
  struct APA102_Frame* ref;

  ref = leds[0];
  clen = 0;
  cctr = 0;

  while(1) {
    clen++;
    ref = leds[clen];
    if(ref == 0) {
      break;
    }
  }

  cctr = coffset;

  if(clen == 0) {
    printf("APA102_MultiStripes Error: leds must contain at least one color\n");
  }

  ctr = offset;
  if(ctr < 0) {
    ctr = 0;
  }

  while(ctr > gap_size + stripe_size) {
    ctr -= gap_size+stripe_size;
    if(ctr < 0) {
      ctr = 0;
    }
  }

  APA102_Begin(strip->interface);
  for(i = 0; i < strip->n_leds; i++) {

    if(ctr < stripe_size) {
      led_frame[0] = 0b11100000 | (0b00011111 & leds[cctr]->brightness);
      led_frame[1] = leds[cctr]->b;
      led_frame[2] = leds[cctr]->g;
      led_frame[3] = leds[cctr]->r;
    } else {
      led_frame[0] = 0b11100000;
      led_frame[1] = 0x00;
      led_frame[2] = 0x00;
      led_frame[3] = 0x00;
    }

    wiringPiSPIDataRW(strip->interface, led_frame, 4);

    ctr++;
    if(ctr >= stripe_size + gap_size) {
      ctr = 0;
      cctr++;
        if(cctr == clen) {
          cctr = 0;
        }
    }
  }
  APA102_End(strip->interface);
}
