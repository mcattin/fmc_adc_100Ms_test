#include <stdio.h>
#include <sys/time.h>

#include "rr_io.h"
#include "gpio.h"


void gpio_set1(uint32_t addr, uint8_t bit)
{
	uint32_t reg;

	reg = gennum_readl(addr);
	//printf("register:%.8X ", reg);
	reg |= (1 << bit);
	//printf("SET  :%.8X(%.2d):%.8X\n", addr, bit, reg);
	gennum_writel(reg, addr);
}

void gpio_set0(uint32_t addr, uint8_t bit)
{
	uint32_t reg;

	reg = gennum_readl(addr);
	//printf("register:%.8X ", reg);
	reg &= ~(1 << bit);
	//printf("CLEAR:%.8X(%.2d):%.8X\n", addr, bit, reg);
	gennum_writel(reg, addr);
}

uint8_t gpio_get(uint32_t addr, uint8_t bit)
{
	return (gennum_readl(addr) & (1 << bit)) ? 1 : 0;
}

void gpio_init(void)
{
	gennum_writel(0x00000000, FCL_CTRL);// FCL mode
	gennum_writel(0x00000017, FCL_EN);// FCL output enable
	gennum_writel(0x00000000, FCL_IODATA_OUT);// FCL outputs to 0

	gennum_writel(0x00002000, GPIO_DIRECTION_MODE); // GPIO direction (1=input)
	gennum_writel(0x0000D000, GPIO_OUTPUT_ENABLE); // GPIO output enable
	gennum_writel(0x00000000, GPIO_OUTPUT_VALUE); // GPIO output to 0
	gpio_set1(GPIO_OUTPUT_VALUE, GPIO_FLASH_CS);
}

void gpio_bootselect(uint8_t select)
{
	switch(select){

	case GENNUM_FLASH:
		gpio_set0(GPIO_OUTPUT_VALUE, GPIO_BOOTSEL0);
		gpio_set1(GPIO_OUTPUT_VALUE, GPIO_BOOTSEL1);
		break;

	case GENNUM_FPGA:
		gpio_set1(GPIO_OUTPUT_VALUE, GPIO_BOOTSEL0);
		gpio_set0(GPIO_OUTPUT_VALUE, GPIO_BOOTSEL1);
		break;

	case FPGA_FLASH:
		gennum_writel(0x00000000, FCL_EN);// FCL output all disabled
		gpio_set1(GPIO_OUTPUT_VALUE, GPIO_BOOTSEL0);
		gpio_set1(GPIO_OUTPUT_VALUE, GPIO_BOOTSEL1);
		break;

	default:
		break;
	}
}

static uint8_t spi_read8(void)
{
	uint8_t rx;
	int i;

	gpio_set0(FCL_IODATA_OUT, SPRI_CLKOUT);
	for(i = 0; i < 8;i++){
		usleep(SPI_DELAY);

		rx <<= 1;
		if (gpio_get(GPIO_INPUT_VALUE, GPIO_SPRI_DIN))
			rx |= 1;

		//usleep(SPI_DELAY);
		gpio_set1(FCL_IODATA_OUT, SPRI_CLKOUT);
		usleep(SPI_DELAY);
		gpio_set0(FCL_IODATA_OUT, SPRI_CLKOUT);
	}
	usleep(SPI_DELAY);
	return rx;
}

static void spi_write8(uint8_t tx)
{
	int i;

	gpio_set0(FCL_IODATA_OUT, SPRI_CLKOUT);
	for(i = 0; i < 8;i++){
		//usleep(SPI_DELAY);

		if(tx & 0x80)
			gpio_set1(FCL_IODATA_OUT, SPRI_DATAOUT);
		else
			gpio_set0(FCL_IODATA_OUT, SPRI_DATAOUT);

		tx<<=1;

		usleep(SPI_DELAY);
		gpio_set1(FCL_IODATA_OUT, SPRI_CLKOUT);
		usleep(SPI_DELAY);
		gpio_set0(FCL_IODATA_OUT, SPRI_CLKOUT);
	}
	usleep(SPI_DELAY);
}

uint8_t flash_read_status(void)
{
	uint8_t val;

	gpio_set0(GPIO_OUTPUT_VALUE, GPIO_FLASH_CS);
	usleep(SPI_DELAY);

	spi_write8(FLASH_RDSR);
	val = spi_read8();

	gpio_set1(GPIO_OUTPUT_VALUE, GPIO_FLASH_CS);
	usleep(SPI_DELAY);

	return val;
}

uint32_t flash_read_id(void)
{
	uint32_t val=0;

	gpio_set0(GPIO_OUTPUT_VALUE, GPIO_FLASH_CS);
	usleep(SPI_DELAY);

	spi_write8(FLASH_RDID);
	val = (spi_read8() << 16);
	val += (spi_read8() << 8);
	val += spi_read8();

	gpio_set1(GPIO_OUTPUT_VALUE, GPIO_FLASH_CS);
	usleep(SPI_DELAY);

	return val;
}
