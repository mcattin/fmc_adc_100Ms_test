#!   /usr/bin/env	python
#    coding: utf8

import sys
import rr
import random
import time
import spi
import csr
import i2c
import gn4124


if __name__ == '__main__':

    GN4124_CSR = 0x0

    DEBUG = 0

    # Objects declaration
    spec = rr.Gennum() # bind to the SPEC board
    gn4124 = gn4124.CGN4124(spec, GN4124_CSR)

    print '\nGet physical memory pages address list'
    pages = gn4124.get_physical_addr()
    if DEBUG != 0:
        for i in range(10):
            print("Host DMA pages %3d: %.8X") % (i, pages[i])

    print '\nInitialise memory pages'
    gn4124.set_memory_page(0, 0x0)
    gn4124.set_memory_page(1, 0xC0FFEE11)
    gn4124.set_memory_page(2, 0xDEADBABE)
    gn4124.set_memory_page(3, 0x0)
    gn4124.set_memory_page(4, 0x0)

    print '\nReading data from memory page 2 (before DMA)'
    page2_data_before = gn4124.get_memory_page(2)

    print '\nPreparing DMA'
    dma_length = 0x100 # DMA length in bytes
    gn4124.add_dma_item(0, pages[1], dma_length, 1, 1) # write from page 1 to SPEC memory
    gn4124.add_dma_item(0, pages[2], dma_length, 0, 0) # read from SPEC memory to page 2

    print '\nPage 0 data - DMA next items'
    page0_data = gn4124.get_memory_page(0)
    if DEBUG != 0:
        for i in range(4*(0x20/4)):
            print("[%.2X]:%.8X") % (pages[0]+i*4,page0_data[i])

    for i in range(1000):
        print("                                   TEST => %d")%i
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
    #print_length = 0x20
    #print '\nPage 2'
    #for i in range(print_length):
    #    print("%.2X: before:%.8X  after:%.8X") % (i, page2_data_before[i], page2_data[i])

    #for i in range(0,2**10,2):
    #    sample = ((page1_data[i+1]<<16)+page1_data[i])
    #    if(i/2 != sample):
    #        print("\nDifference detected !! read:%d excpect:%d\n") % (sample, i/2)
    #        break


    print '\nBye bye ...'
    sys.exit()
