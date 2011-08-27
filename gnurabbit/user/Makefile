
CFLAGS = -Wall -ggdb -I../kernel

AS		= $(CROSS_COMPILE)as
LD		= $(CROSS_COMPILE)ld
CC		= $(CROSS_COMPILE)gcc
CPP		= $(CC) -E
AR		= $(CROSS_COMPILE)ar
NM		= $(CROSS_COMPILE)nm
STRIP		= $(CROSS_COMPILE)strip
OBJCOPY		= $(CROSS_COMPILE)objcopy
OBJDUMP		= $(CROSS_COMPILE)objdump

ALL = rrcmd flip fpga_loader_spec_test

all: $(ALL)

fpga_loader_spec_test: rr_io.c gpio.c fpga_loader_spec_test.c
	$(CC) -o fpga_loader_spec_test rr_io.c gpio.c fpga_loader_spec_test.c

clean:
	rm -f $(ALL) *.o *~