// CP2103 GPIO test
// mcattin 2011

#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include <unistd.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/ioctl.h>
#include <asm/ioctls.h>
#include <fcntl.h>
#include <math.h>

#define DEV_NAME "/dev/ttyUSB"

#define GPIO_SET(bit, value) ((1 << (bit)) | ((value & 1) << ((bit) + 8)))

int main(int argc, char *argv[])
{
	int fd;
	int err;
	int gpio;
	int i;
	int select_gpio;
	int num;
	char dname[30];

	if (argc != 2) {
		printf("usage: %s <num>\n", argv[0]);
		exit(1);
	}
	sprintf(dname, "/dev/ttyUSB%d", atoi(argv[1]));

	fd = open(dname, O_RDWR | O_NONBLOCK);

	if(fd < 0) {
		fprintf(stderr, "Failed to open %s\n", DEV_NAME);
		return -1;
	}

	select_gpio = 3;

	err = ioctl(fd, 0x8000, &gpio);
	fprintf(stderr,"Read GPIOs: 0x%.4X\n", gpio);
	sleep(3);


	for (i = 0; i < 5; i++) {
		gpio = GPIO_SET(select_gpio, 0);
		err = ioctl(fd, 0x8001, 0xf);
		err = ioctl(fd, 0x8000, &gpio);
		fprintf(stderr, "err: %d, Read GPIOs: 0x%.4X\n", err, gpio);
		sleep(1);
		gpio = GPIO_SET(select_gpio, 1);
		err = ioctl(fd, 0x8001, 0x0);
		err = ioctl(fd, 0x8000, &gpio);
		fprintf(stderr, "err: %d, Read GPIOs: 0x%.4X\n", err, gpio);
		sleep(1);
	}

	err = ioctl(fd, 0x8000, &gpio);
	fprintf(stderr, "Read GPIOs: 0x%.4X\n", gpio);

	close(fd);

	return 0;
}
