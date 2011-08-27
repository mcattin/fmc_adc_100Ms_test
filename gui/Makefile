CC = gcc

OBJS = spec_adc_test.o adc_stuff.o rr_lib.o

CFLAGS_SDL=$(shell sdl-config --cflags) $(shell pkg-config --cflags fftw3)  -lSDL_ttf
LDFLAGS_SDL=$(shell sdl-config --libs) $(shell pkg-config --libs fftw3) -lSDL_ttf

CFLAGS = $(CFLAGS_SDL) -fPIC
LDFLAGS = $(LDFLAGS_SDL)

TARGETS = spec_adc_test libadc.so

all:	$(TARGETS)

libadc.so: $(OBJS)
		${CC} -shared -o $(OUTPUT_SO) $(OBJS)
spec_adc_test: $(OBJS)
		${CC} -o $@ $(OBJS) $(LDFLAGS)
clean:
		rm -f $(OBJS) $(TARGETS)

