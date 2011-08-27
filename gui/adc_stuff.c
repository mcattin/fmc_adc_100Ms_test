#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>

#include "fpga_regs.h"
#include "fmc_adc_100Ms_csr.h"
#include "adc_stuff.h"

#include "rr_lib.h"


void adc_record(sample_t *buf, int samples)
{
  uint32_t acq_status, dma_status;
  int i = 0;
  int j = 0;
  int even, odd;
        uint32_t carrier_addr;
        uint32_t host_addr;
        uint32_t dma_length;
        uintptr_t plist[256];

        // get page pointer list
	//fprintf(stderr, "Get pointer list from Gennum driver.\n");
        rr_getplist(&plist);

        // Enable sampling clock
	//fprintf(stderr, "Enable sampling clock.\n");
	//fprintf(stderr, "ADC core: status reg: %.8X\n", rr_readl(BASE_ADC_CORE_CSR + STA));
        rr_writel(FMC_ADC_CORE_CTL_FMC_CLK_OE |
                  //FMC_ADC_CORE_CTL_TEST_DATA_EN |
                  FMC_ADC_CORE_CTL_OFFSET_DAC_CLR_N, BASE_ADC_CORE_CSR + CTL);
        //fprintf(stderr, "ADC core: status reg: %.8X\n", rr_readl(BASE_ADC_CORE_CSR + STA));
        //fprintf(stderr, "ADC core: control reg: %.8X\n", rr_readl(BASE_ADC_CORE_CSR + CTL));
        do{
                acq_status = rr_readl(BASE_ADC_CORE_CSR + STA);
        }while(!(acq_status & FMC_ADC_CORE_STA_SERDES_SYNCED));
        //fprintf(stderr, "ADC core: status reg: %.8X\n", rr_readl(BASE_ADC_CORE_CSR + STA));

        // start acquisition
	//fprintf(stderr, "Start acquisition.\n");
        rr_writel(FSM_CMD_START |
                  FMC_ADC_CORE_CTL_FMC_CLK_OE |
                  //FMC_ADC_CORE_CTL_TEST_DATA_EN |
                  FMC_ADC_CORE_CTL_OFFSET_DAC_CLR_N, BASE_ADC_CORE_CSR + CTL);
        //fprintf(stderr, "ADC core: control reg: %.8X\n", rr_readl(BASE_ADC_CORE_CSR + CTL));

        // wait for pre-trigger done
	//fprintf(stderr, "Wait for pre-trigger to be done.\n");
        do{
                acq_status = rr_readl(BASE_ADC_CORE_CSR + STA);
        }while(!((acq_status & FSM_MASK) & FSM_WAIT_TRIG));

        // software trigger
	//fprintf(stderr, "Generate software trigger.\n");
        rr_writel(0xFFFFFFFF, BASE_ADC_CORE_CSR + SW_TRIG);

        // wait for end of acquisition
	//fprintf(stderr, "Wait for the end of acquisition.\n");
        do{
                acq_status = rr_readl(BASE_ADC_CORE_CSR + STA);
        }while(!((acq_status & FSM_MASK) & FSM_IDLE));

/*
        for(i=0;i<0x10;i+=4){
                host_addr = 0x1000 + i;
                host_writel(0, host_addr);
                fprintf(stderr, "%.8X: %.8X\n", host_addr, host_readl(host_addr));
        }
*/

        // DMA to read samples
        dma_length = 0x100;//samples; // in bytes

        for(i=0;i<4;i++){
                // Read data from board to DMA page
                for(j=0;j<(0x1000/dma_length);j++){
                        //fprintf(stderr, "Begin DMA: %d:%d\n", i, j);


                        carrier_addr = i*0x1000 + j*dma_length;
                        host_addr = (plist[1]<<12) + j*dma_length;
                        //fprintf(stderr, "DMA %d: carrier addr: %.8X\n", i, carrier_addr);
                        //fprintf(stderr, "DMA %d: host addr   : %.8X\n", i, host_addr);

                        rr_writel(carrier_addr, BASE_DMA_CSR + DMA_CARRIER_START_ADDR);
                        rr_writel(host_addr, BASE_DMA_CSR + DMA_HOST_START_ADDR_L);
                        rr_writel(0x0, BASE_DMA_CSR + DMA_HOST_START_ADDR_H);
                        rr_writel(dma_length, BASE_DMA_CSR + DMA_LENGTH);
                        rr_writel(0x0, BASE_DMA_CSR + DMA_NEXT_ITEM_ADDR_L);
                        rr_writel(0x0, BASE_DMA_CSR + DMA_NEXT_ITEM_ADDR_H);
                        rr_writel(0x0, BASE_DMA_CSR + DMA_ATTRIB); // dir=from carrier to host, last item

                        // start DMA
                        rr_writel(DMA_CTL_START, BASE_DMA_CSR + DMA_CTL);

                        // wait for end of DMA irq
                        rr_irqwait();
                        //do{
                        //        dma_status = rr_readl(BASE_DMA_CSR + DMA_STA);
                        //}while(!(dma_status & DMA_STA_DONE));
                        usleep(100);
                        //fprintf(stderr, "End DMA: %d:%d\n", i, j);
                }
                // Store data from DMA page to buffer
                for(j=0;j<0x200;j++)
                {
                        even = (2*j << 2);
                        odd = (2*j+1 << 2);

                        buf[i*0x200+j].ch1 = (host_readl(0x1000+even) & 0xffff)>>2;
                        buf[i*0x200+j].ch2 = (host_readl(0x1000+even) >> 16)>>2;
                        buf[i*0x200+j].ch3 = (host_readl(0x1000+odd) & 0xffff)>>2;
                        buf[i*0x200+j].ch4 = (host_readl(0x1000+odd) >> 16)>>2;
                }
        }


/*
        for(i=0;i<0x10;i+=4){
                host_addr = 0x1000 + i;
                //fprintf(stderr, "%.8X: %.8X\n", host_addr, host_readl(host_addr));
                fprintf(stderr, "buf[%3d].ch4: %.8X\n", i, buf[i].ch4);
        }
*/
/*
        // copy samples from DMA page to buffer
        for(i=0;i<samples*2;i++)
        {
                even = (2*i << 2);
                odd = (2*i+1 << 2);
                if(i<samples/4){
                        buf[i].ch1 = (host_readl(0x1000+even) & 0xffff)>>2;
                        buf[i].ch2 = (host_readl(0x1000+even) >> 16)>>2;
                        buf[i].ch3 = (host_readl(0x1000+odd) & 0xffff)>>2;
                        buf[i].ch4 = (host_readl(0x1000+odd) >> 16)>>2;
                }
                else if(i<(2*(samples/4))){
                        buf[i].ch1 = (host_readl(0x2000+even) & 0xffff)>>2;
                        buf[i].ch2 = (host_readl(0x2000+even) >> 16)>>2;
                        buf[i].ch3 = (host_readl(0x2000+odd) & 0xffff)>>2;
                        buf[i].ch4 = (host_readl(0x2000+odd) >> 16)>>2;
                }
                else if(i<(3*(samples/4))){
                        buf[i].ch1 = (host_readl(0x3000+even) & 0xffff)>>2;
                        buf[i].ch2 = (host_readl(0x3000+even) >> 16)>>2;
                        buf[i].ch3 = (host_readl(0x3000+odd) & 0xffff)>>2;
                        buf[i].ch4 = (host_readl(0x3000+odd) >> 16)>>2;
                }
                else{
                        buf[i].ch1 = (host_readl(0x4000+even) & 0xffff)>>2;
                        buf[i].ch2 = (host_readl(0x4000+even) >> 16)>>2;
                        buf[i].ch3 = (host_readl(0x4000+odd) & 0xffff)>>2;
                        buf[i].ch4 = (host_readl(0x4000+odd) >> 16)>>2;
                }
        }
*/

}


void adc_record_single(int channel, int *buf, int samples)
{
	sample_t tmp[32768];
	int i;

	adc_record(tmp, samples);

	for(i=0;i<samples+1; i++)
	{
		switch(channel)
		{
                case 1: buf[i] = tmp[i].ch1; break;
                case 2: buf[i] = tmp[i].ch2; break;
                case 3: buf[i] = tmp[i].ch3; break;
                case 4: buf[i] = tmp[i].ch4; break;
		}
	}
}


int adc_init()
{
        fprintf(stdout, "Use Python program to initialize the board !!\n");

        /*
        pdma_init();
        spi_init();
        ltc2175_init();
        adc_calibrate_serdes();

        gpio_set_dir(PIN_DAC_RST, 1);
        gpio_set_state(PIN_DAC_RST, 1);
        */
}


