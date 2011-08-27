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


if __name__ == '__main__':

    GN4124_CSR = 0x0

    STAT_REGS = 0x40000
    STAT_DUMMY1 = 0x0
    STAT_DUMMY2 = 0x4
    STAT_DUMMY3 = 0x8
    STAT_SWITCH = 0xC

    CTRL_REGS = 0x80000
    CTRL_DUMMY1 = 0x0
    CTRL_DUMMY2 = 0x4
    CTRL_DUMMY3 = 0x8
    CTRL_LED = 0xC
    CTRL_LED_GREEN = (1<<0)
    CTRL_LED_RED = (1<<1)


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
        reg = csr.rd_reg(CTRL_LED)
        for i in range(3):
            csr.wr_reg(CTRL_LED, (reg | CTRL_LED_GREEN | CTRL_LED_RED))
            time.sleep(.2)
            csr.wr_reg(CTRL_LED, (reg & ~(CTRL_LED_GREEN | CTRL_LED_RED)))
            time.sleep(.2)
            sys.stdout.write(".")
            sys.stdout.flush()
        print ''

    # Objects declaration
    spec = rr.Gennum() # bind to the SPEC board
    gn4124 = gn4124.CGN4124(spec, GN4124_CSR)
    status_regs = csr.CCSR(spec, STAT_REGS)
    control_regs = csr.CCSR(spec, CTRL_REGS)


    print '\n### Configuration ###'

    # Set local bus frequency
    gn4124.set_local_bus_freq(200)
    print("GN4124 local bus frequency: %d") % gn4124.get_local_bus_freq()

    print '\nPrint status registers'
    print("Dummy register 1 : %.8X") % (status_regs.rd_reg(STAT_DUMMY1))
    print("Dummy register 2 : %.8X") % (status_regs.rd_reg(STAT_DUMMY2))
    print("Dummy register 3 : %.8X") % (status_regs.rd_reg(STAT_DUMMY3))
    print("Switch register  : %.8X") % (status_regs.rd_reg(STAT_SWITCH))

    #print("Blink LEDs")
    #carrier_led_test(control_regs)

    #sys.exit()

    print '\nGet physical memory pages address list'
    pages = gn4124.get_physical_addr()
    for i in range(10):
        print("Host DMA pages %3d: %.8X") % (i, pages[i])

    print '\nInitialise memory pages'
    gn4124.set_memory_page(0, 0x0)
    gn4124.set_memory_page(1, 0xC0FFEE11)
    gn4124.set_memory_page(2, 0xDEADBABE)
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



    print '\nReading data from memory page 2 (before DMA)'
    page2_data_before = gn4124.get_memory_page(2)

    print '\nPreparing DMA'
    dma_length = 0x4 # DMA length in bytes
    gn4124.add_dma_item(0, pages[1], dma_length, 1, 1) # write from page 1 to SPEC memory
    gn4124.add_dma_item(0, pages[2], dma_length, 0, 0) # read from SPEC memory to page 2

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

    print '\nWaiting for interrupt'
    gn4124.wait_irq()
    print '\nInterrupt received'
    print("DMA controller status : %s") % gn4124.get_dma_status()

    print '\nReading data from memory page 1 and 2'
    page1_data = gn4124.get_memory_page(1)
    page2_data = gn4124.get_memory_page(2)

    #print len(page1_data)
    print_length = 0x20
    print '\nPage 2'
    for i in range(print_length):
        print("%.2X: before:%.8X  after:%.8X") % (i, page2_data_before[i], page2_data[i])

    #for i in range(0,2**10,2):
    #    sample = ((page1_data[i+1]<<16)+page1_data[i])
    #    if(i/2 != sample):
    #        print("\nDifference detected !! read:%d excpect:%d\n") % (sample, i/2)
    #        break


    print '\nBye bye ...'
    sys.exit()
