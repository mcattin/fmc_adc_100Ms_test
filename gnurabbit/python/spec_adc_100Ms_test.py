#!   /usr/bin/env	python
#    coding: utf8

import sys
import rr
import random
import time
import spi
import csr
import i2c
import fmc_adc
import gn4124
from pylab import *


if __name__ == '__main__':

    GN4124_CSR = 0x0

    CARRIER_CSR = 0x30000

    CSR_TYPE_VER = 0x00
    CSR_BSTM_TYPE = 0x04
    CSR_BSTM_DATE = 0x08
    CSR_STATUS = 0x0C
    CSR_CTRL = 0x10

    PCB_VER_MASK = 0x000F
    CARRIER_TYPE_MASK = 0xFFFF0000

    STATUS_FMC_PRES = (1<<0)
    STATUS_P2L_PLL_LCK = (1<<1)
    STATUS_SYS_PLL_LCK = (1<<2)
    STATUS_DDR3_CAL_DONE = (1<<3)

    CTRL_LED_GREEN = (1<<0)
    CTRL_LED_RED = (1<<1)
    CTRL_DAC_CLR_N = (1<<2)


    def set_local_bus_freq(gennum, freq):
        # freq in MHz
        # LCLK = (25MHz*(DIVFB+1))/(DIVOT+1)
        # DIVFB = 31
        # DIVOT = (800/LCLK)-1
        divot = int(round((800/freq)-1,0))
        data = 0xe001f00c + (divot << 4)
        print 'Set local bus freq to %dMHz' % freq
        gennum.iwrite(4, 0x808, 4, data)
        print("GN4124:CLK_CSR: %.8X") % gennum.iread(4, 0x808, 4)

    def carrier_led_test(csr):
        reg = csr.rd_reg(CSR_CTRL)
        for i in range(3):
            csr.wr_reg(CSR_CTRL, (reg | CTRL_LED_GREEN | CTRL_LED_RED))
            time.sleep(.2)
            csr.wr_reg(CSR_CTRL, (reg & ~(CTRL_LED_GREEN | CTRL_LED_RED)))
            time.sleep(.2)
            sys.stdout.write(".")
            sys.stdout.flush()
        print ''

    # Objects declaration
    spec = rr.Gennum() # bind to the SPEC board
    gn4124 = gn4124.CGN4124(spec, GN4124_CSR)
    carrier_csr = csr.CCSR(spec, CARRIER_CSR)
    fmc_adc = fmc_adc.CFmcAdc100Ms(spec)


    print '\n### Configuration ###'

    # Set local bus frequency
    #gn4124.set_local_bus_freq(160)
    print("GN4124 local bus frequency: %d") % gn4124.get_local_bus_freq()

    print '\nCarrier'
    print("PCB version    : %d") % (PCB_VER_MASK & carrier_csr.rd_reg(CSR_TYPE_VER))
    print("Carrier type   : %d") % ((CARRIER_TYPE_MASK & carrier_csr.rd_reg(CSR_TYPE_VER))>>16)
    print("Bitstream type : %d") % (carrier_csr.rd_reg(CSR_BSTM_TYPE))
    print("Bitstream date : %d") % (carrier_csr.rd_reg(CSR_BSTM_DATE))
    print("Status         : %.8X") % (carrier_csr.rd_reg(CSR_STATUS))
    print("Control        : %.8X") % (carrier_csr.rd_reg(CSR_CTRL))
    print("Blink LEDs")
    carrier_led_test(carrier_csr)



    pages = gn4124.get_physical_addr()
    gn4124.set_memory_page(0, 0x0)
    gn4124.set_memory_page(1, 0x0)
    gn4124.set_memory_page(2, 0x0)
    gn4124.set_memory_page(3, 0x0)
    gn4124.set_memory_page(4, 0x0)

    #print '\nAbort DMA'
    #gn4124.abort_dma()
    """
    print '\nLoad pattern to DDR'
    gn4124.set_memory_page(2,0xDEADBEEF)

    gn4124.add_dma_item(0, pages[2], 0x200, 1, 1)
    gn4124.add_dma_item(0, pages[3], 0x200, 0, 0)
    print("DMA controller status : %s") % gn4124.get_dma_status()

    print '\n Start DMA transfer'
    gn4124.start_dma()
    print("DMA controller status : %s") % gn4124.get_dma_status()
    #while('Done' != gn4124.get_dma_status()):
    #    print("DMA controller status : %s") % gn4124.get_dma_status()
    #    time.sleep(.5)

    print '\nWaiting for interrupt'
    gn4124.wait_irq()
    print '\nInterrupt received'
    print("DMA controller status : %s") % gn4124.get_dma_status()
    """
    #print '\nReading data from memory page 3'
    #page3_data = gn4124.get_memory_page(3)
    #for i in range(0x200/4):
    #    print("%3d: %.8X") % (i, page3_data[i])

    time.sleep(.5)

    fmc_adc.i2c_scan()
    fmc_adc.print_unique_id()
    fmc_adc.print_temp()

    #sys.exit()

    fmc_adc.print_adc_config()

    fmc_adc.print_si570_config()

    print '\nSet input termination'
    fmc_adc.set_input_term(1, 'OFF')
    fmc_adc.set_input_term(2, 'OFF')
    fmc_adc.set_input_term(3, 'OFF')
    fmc_adc.set_input_term(4, 'OFF')

    print '\nSet input range'
    fmc_adc.set_input_range(1, '10V')
    fmc_adc.set_input_range(2, '10V')
    fmc_adc.set_input_range(3, '10V')
    fmc_adc.set_input_range(4, '10V')

    print '\nCalibrate DC offset'
    #fmc_adc.dc_offset_calibr(1, 0xA000)
    #fmc_adc.dc_offset_calibr(2, 0x8000)
    #fmc_adc.dc_offset_calibr(3, 0xFFFF)
    #fmc_adc.dc_offset_calibr(4)
    #time.sleep(1)

    print '\nSet decimation factor'
    fmc_adc.set_decimation(1)

    #print '\nEnable ADC test pattern'
    #fmc_adc.testpat_en(0x0001)


    #print '\nEnable test data'
    #fmc_adc.test_data_en()

    nb_shots = 1
    print("Number of shots: %d") % nb_shots

    fmc_adc.print_adc_core_config()

    print '\nGet acquisition FSM state:'
    print 'FSM state: ' + fmc_adc.get_acq_fsm_state()

    print '\nSet trigger configuration'
    fmc_adc.set_trig_config(1, 0, 1, 1, 0, 0, 0)

    print '\nSet number of pre-trigger samples'
    fmc_adc.set_pre_trig_samples(500)

    print '\nSet number of post-trigger samples'
    fmc_adc.set_post_trig_samples(500)

    print '\nSet number of shots'
    fmc_adc.set_shots(nb_shots)

    print '\nStart acquisition'
    fmc_adc.start_acq()
    print 'FSM state: ' + fmc_adc.get_acq_fsm_state()

    print '\nSoftware trigger'

    for i in range(nb_shots):

        while('WAIT_TRIG' != fmc_adc.get_acq_fsm_state()):
            print fmc_adc.get_acq_fsm_state()
            time.sleep(.1)

        print("\nTrigger %d") % i
        fmc_adc.sw_trig()


    while('IDLE' != fmc_adc.get_acq_fsm_state()):
        print fmc_adc.get_acq_fsm_state()
        time.sleep(1)

    print '\nEnd of acquisition'





    #print '\nDisable test data'
    #fmc_adc.test_data_dis()





    print '\nReading data from memory page 1 (before DMA)'
    page1_data_before = gn4124.get_memory_page(1)

    print '\nPreparing DMA'
    dma_length = 0x1000 # DMA length in bytes
    for i in range(10):
        print("Host DMA pages %3d: %.8X") % (i, pages[i])
    gn4124.add_dma_item(0*dma_length, pages[1]+0*dma_length, dma_length, 0, 1)
    gn4124.add_dma_item(1*dma_length, pages[2]+0*dma_length, dma_length, 0, 1)
    gn4124.add_dma_item(2*dma_length, pages[3]+0*dma_length, dma_length, 0, 1)
    gn4124.add_dma_item(3*dma_length, pages[4]+0*dma_length, dma_length, 0, 0)
    #gn4124.add_dma_item(1*dma_length, pages[1]+1*dma_length, dma_length, 0, 1)
    #gn4124.add_dma_item(2*dma_length, pages[1]+2*dma_length, dma_length, 0, 1)
    #gn4124.add_dma_item(3*dma_length, pages[1]+3*dma_length, dma_length, 0, 0)

    print '\nPage 0 data - DMA next items'
    page0_data = gn4124.get_memory_page(0)
    for i in range(4*(0x20/4)):
        print("[%.2X]:%.8X") % (pages[0]+i*4,page0_data[i])

    print("DMA controller status : %s") % gn4124.get_dma_status()

    print '\n Start DMA transfer'
    gn4124.start_dma()

    while('Done' != gn4124.get_dma_status()):
        print("DMA controller status : %s") % gn4124.get_dma_status()
        time.sleep(.5)

    import os
    os.system("dmesg |tail")
    print '\nWaiting for interrupt'
    gn4124.wait_irq()
    print '\nInterrupt received'
    print("DMA controller status : %s") % gn4124.get_dma_status()

    """
    print '\nSecond DMA'
    gn4124.add_dma_item(2*dma_length, pages[2], dma_length, 0, 1)
    gn4124.add_dma_item(3*dma_length, pages[2]+dma_length, dma_length, 0, 0)
    print("DMA controller status : %s") % gn4124.get_dma_status()

    print '\n Start DMA transfer'
    gn4124.start_dma()

    while('Done' != gn4124.get_dma_status()):
        print("DMA controller status : %s") % gn4124.get_dma_status()
        time.sleep(.5)

    print '\nWaiting for interrupt'
    gn4124.wait_irq()
    print '\nInterrupt received'
    print("DMA controller status : %s") % gn4124.get_dma_status()


    print '\nThird DMA'
    gn4124.add_dma_item(4*dma_length, pages[3], dma_length, 0, 1)
    gn4124.add_dma_item(5*dma_length, pages[3]+dma_length, dma_length, 0, 0)
    print("DMA controller status : %s") % gn4124.get_dma_status()

    print '\n Start DMA transfer'
    gn4124.start_dma()

    while('Done' != gn4124.get_dma_status()):
        print("DMA controller status : %s") % gn4124.get_dma_status()
        time.sleep(.5)

    print '\nWaiting for interrupt'
    gn4124.wait_irq()
    print '\nInterrupt received'
    print("DMA controller status : %s") % gn4124.get_dma_status()


    print '\nFourth DMA'
    gn4124.add_dma_item(6*dma_length, pages[4], dma_length, 0, 1)
    gn4124.add_dma_item(7*dma_length, pages[4]+dma_length, dma_length, 0, 0)
    print("DMA controller status : %s") % gn4124.get_dma_status()

    print '\n Start DMA transfer'
    gn4124.start_dma()

    while('Done' != gn4124.get_dma_status()):
        print("DMA controller status : %s") % gn4124.get_dma_status()
        time.sleep(.5)

    print '\nWaiting for interrupt'
    gn4124.wait_irq()
    print '\nInterrupt received'
    print("DMA controller status : %s") % gn4124.get_dma_status()
    """

    print '\nReading data from memory page 1,2,3 and 4'
    page1_data = gn4124.get_memory_page(1)
    page2_data = gn4124.get_memory_page(2)
    page3_data = gn4124.get_memory_page(3)
    page4_data = gn4124.get_memory_page(4)
    #print len(page1_data)
    #print_length = 200
    #print '\nPage 1 data :'
    #for i in range(0x200/4):
    #    print("%.2X:%.8X") % (i, page1_data[i])

    #for i in range(0,2**10,2):
    #    sample = ((page1_data[i+1]<<16)+page1_data[i])
    #    if(i/2 != sample):
    #        print("\nDifference detected !! read:%d excpect:%d\n") % (sample, i/2)
    #        break


    channels = []
    for i in range(2**10):
    #for i in range(100):
        channels.append(page1_data[i] & 0xFFFF)
        channels.append(page1_data[i]>>16)
        #print("page1_data[%3d]: %.8X") % (i, page1_data[i])
        #print("channels[%3d]  :     %.4X") % (i*2, channels[i*2])
        #print("channels[%3d]  : %.4X") % (i*2+1, channels[i*2+1])

    for i in range(2**10):
        channels.append(page2_data[i] & 0xFFFF)
        channels.append(page2_data[i]>>16)

    for i in range(2**10):
        channels.append(page3_data[i] & 0xFFFF)
        channels.append(page3_data[i]>>16)

    for i in range(2**10):
        channels.append(page4_data[i] & 0xFFFF)
        channels.append(page4_data[i]>>16)

    time_base = arange(0,2**12/2,1)
    #print len(time_base)
    channel1 = channels[0::4]
    channel2 = channels[1::4]
    channel3 = channels[2::4]
    channel4 = channels[3::4]
    #print len(channel1)

    for i in range(20):
        print("channels:%.4X %.4X %.4X %.4X") % (channels[i*4], channels[1+i*4], channels[2+i*4], channels[3+i*4])
        #print("channel1:%.4X") % (channel1[i])
        #print("channel2:     %.4X") % (channel2[i])
        #print("channel3:          %.4X") % (channel3[i])
        #print("channel4:               %.4X") % (channel4[i])


    file = open("adc_acq.txt", 'w')
    for i in range(2048):
        file.write("%d, %d, %d, %d, %d\n" % (time_base[i], channel1[i], channel2[i], channel3[i], channel4[i]))
        #file.write("%d, %.4X, %.4X, %.4X, %.4X\n" % (time_base[i], channel1[i], channel2[i], channel3[i], channel4[i]))
        #print("%d, %.4X, %.4X, %.4X, %.4X" % (time_base[i], channel1[i], channel2[i], channel3[i], channel4[i]))
        #print("%d, %d, %d, %d, %d" % (time_base[i], channel1[i], channel2[i], channel3[i], channel4[i]))


    """
    print ''
    for j in range(1,5):
        for i in range(5):
            print("Channel %d value:%.4X") % (j,fmc_adc.get_current_adc_value(j))
    """

    """
    print '\nSoftware trigger'
    for i in range(10):
        print("trigger : %d") % i
        fmc_adc.sw_trig()
        time.sleep(1)
    """

    print '\nBye bye ...'
    sys.exit()
