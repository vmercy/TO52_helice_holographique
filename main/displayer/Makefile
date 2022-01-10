all: libapa102.a

clean:
	rm -f libapa102.a 

libapa102.a: lib/build/apa102.o lib/build/apa102_anim.o
	ar rcs libapa102.a lib/build/apa102.o lib/build/apa102_anim.o

lib/build/apa102.o: lib/apa102.c lib/apa102.h
	gcc -c -o lib/build/apa102.o lib/apa102.c

lib/build/apa102_anim.o: lib/apa102_anim.c lib/apa102.h
	gcc -c  -o lib/build/apa102_anim.o lib/apa102_anim.c

display: displayer.c
	gcc -L. -I./lib  -o bin/displayer display.c -lwiringPi -lapa102 -lpthread