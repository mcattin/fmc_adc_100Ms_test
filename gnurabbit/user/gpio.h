#define FCL_CTRL 0xB00
#define FCL_STATUS 0xB04
#define FCL_IODATA_IN 0xB08
#define FCL_IODATA_OUT 0xB0C
#define FCL_EN 0xB10

#define GPIO_DIRECTION_MODE 0xA04
#define GPIO_OUTPUT_ENABLE 0xA08
#define GPIO_OUTPUT_VALUE 0xA0C
#define GPIO_INPUT_VALUE 0xA10


#define SPRI_CLKOUT 0
#define SPRI_DATAOUT 1
#define SPRI_CONFIG 2
#define SPRI_DONE 3
#define SPRI_XI_SWAP 4
#define SPRI_STATUS 5

#define GPIO_SPRI_DIN 13
#define GPIO_FLASH_CS 12

#define GPIO_BOOTSEL0 15
#define GPIO_BOOTSEL1 14

#define SPI_DELAY 50

#define FLASH_WREN 0x06
#define FLASH_WRDI 0x04
#define FLASH_RDID 0x9F
#define FLASH_RDSR 0x05
#define FLASH_WRSR 0x01
#define FLASH_READ 0x03
#define FLASH_FAST_READ 0x0B
#define FLASH_PP 0x02
#define FLASH_SE 0xD8
#define FLASH_BE 0xC7

#define GENNUM_FLASH 1
#define GENNUM_FPGA  2
#define FPGA_FLASH   3


void gpio_init(void);
void gpio_bootselect(uint8_t select);
uint8_t flash_read_status(void);
uint32_t flash_read_id(void);
