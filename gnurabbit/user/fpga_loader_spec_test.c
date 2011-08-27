#include <stdio.h>
#include <unistd.h>
#include <sys/time.h>


#include "rr_io.h"
#include "gpio.h"


int main(int argc, char *argv[])
{
	uint32_t i=0;

	if(argc != 2){
		printf( "usage: %s filename \n", argv[0]);
	}
	else{
		rr_init();
		gpio_init();
		gpio_bootselect(GENNUM_FPGA);
		//gpio_bootselect(FPGA_FLASH);

		printf("CLK_CSR : %.8X\n", gennum_readl(0x808));
		/*
		while(1){
			i++;
			//printf("%5d Flash status : %.2X\n", i, flash_read_status());
			printf("%5d Flash status : %.8X\n", i, flash_read_id());
			sleep(1);
		}
		*/

		printf("Firmware to be loaded : %s \n", argv[1]);
		rr_load_bitstream_from_file(argv[1]);
		printf("Firmware loaded successfully ! \n");

	}
}
