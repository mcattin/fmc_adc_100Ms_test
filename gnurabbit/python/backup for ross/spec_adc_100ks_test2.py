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
from pylab import *

if __name__ == '__main__':

    GN4124_CSR = 0x0

    CSR = 0x40000

    CSR_STATUS = 0x00
    CSR_CTRL = 0x04

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

    # Objects declaration
    spec = rr.Gennum() # bind to the SPEC board
    gn4124 = gn4124.CGN4124(spec, GN4124_CSR)
    adc_csr = csr.CCSR(spec, CSR)

    print '\n### Configuration ###'

    # Set local bus frequency
    gn4124.set_local_bus_freq(160)
    print("GN4124 local bus frequency: %d") % gn4124.get_local_bus_freq()

    pages = gn4124.get_physical_addr()
    gn4124.set_memory_page(0, 0x0)
    gn4124.set_memory_page(1, 0x0)
    gn4124.set_memory_page(2, 0x0)
    gn4124.set_memory_page(3, 0x0)
    gn4124.set_memory_page(4, 0x0)

    #print 'Write debugging data (address) to DPRAM'
    #adc_csr.wr_reg(CSR_CTRL, 0x2)

    # reset acquisition
    time.sleep(.1)
    adc_csr.wr_reg(CSR_CTRL, 0x0)
    print("Command:%.8X") % adc_csr.rd_reg(CSR_CTRL)
    time.sleep(.1)





    # Acquire data
    channel_select = int(raw_input('Enter channel number: '))

    ################## start by looping here i think.....

    for sample_num in range(3): #ross
        if (((channel_select-1+sample_num)!=0) and ((channel_select-1+sample_num)!= 17)):
        
            print 'Start acquisition'
            ctrl=((channel_select-1+sample_num)<<2)+0x1   #ross
            adc_csr.wr_reg(CSR_CTRL, ctrl)
            print("Command:%.8X") % adc_csr.rd_reg(CSR_CTRL)

            print("Status:%.8X") % adc_csr.rd_reg(CSR_STATUS)

            while(0x1 != (0x1 & adc_csr.rd_reg(CSR_STATUS))):
                print("Status:%.8X") % adc_csr.rd_reg(CSR_STATUS)
                time.sleep(.1)

            print("Status:%.8X") % adc_csr.rd_reg(CSR_STATUS)

            print 'End of acquisition'


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

            print '\nWaiting for interrupt'
            gn4124.wait_irq()
            print '\nInterrupt received'
            print("DMA controller status : %s") % gn4124.get_dma_status()

            print '\nReading data from memory page 1,2,3 and 4'
            page1_data = gn4124.get_memory_page(1)
            page2_data = gn4124.get_memory_page(2)
            page3_data = gn4124.get_memory_page(3)
            page4_data = gn4124.get_memory_page(4)
            #print len(page1_data)
            print_length = 200
            for i in range(200):
                print("%.2X: %.8X") % (i, page1_data[i])

            #for i in range(0,2**10,2):
            #    sample = ((page1_data[i+1]<<16)+page1_data[i])
            #    if(i/2 != sample):
            #        print("\nDifference detected !! read:%d excpect:%d\n") % (sample, i/2)
            #        break


            channels = []
            for i in range(2**10):
            #for i in range(100):
                channels.append(page1_data[i] & 0xFFFF)
                #channels.append(page1_data[i]>>16)
                #print("page1_data[%3d]: %.8X") % (i, page1_data[i])
                #print("channels[%3d]  :     %.4X") % (i*2, channels[i*2])
                #print("channels[%3d]  : %.4X") % (i*2+1, channels[i*2+1])

            for i in range(2**10):
                channels.append(page2_data[i] & 0xFFFF)
                #channels.append(page2_data[i]>>16)

            for i in range(2**10):
                channels.append(page3_data[i] & 0xFFFF)
                #channels.append(page3_data[i]>>16)

            for i in range(2**10):
                channels.append(page4_data[i] & 0xFFFF)
                #channels.append(page4_data[i]>>16)

            for i in range(len(channels)):
                if(channels[i] & 0x8000):
                    channels[i] = -0x10000 + channels[i]

            print len(channels)
            time_base = arange(0,4097,1)

            filename="./adc_100k_acq_channel_" + str(channel_select-1+samples)
            file = open(filename, 'w')              ##ross
            for i in range(len(channels)): 
                file.write("%5d, %5d\n" % (time_base[i], channels[i]))






    ######################## loop until here
   

    print '\nBye bye ...'
    sys.exit()  #add back in for test of single channel
########################################################
    time_base = arange(0,2**12/2,1)
    #print len(time_base)
    channel1 = channels[0::16]
    channel2 = channels[1::16]
    channel3 = channels[2::16]
    channel4 = channels[3::16]
    channel5 = channels[4::16]
    channel6 = channels[5::16]
    channel7 = channels[6::16]
    channel8 = channels[7::16]
    channel9 = channels[8::16]
    channel10 = channels[9::16]
    channel11 = channels[10::16]
    channel12 = channels[11::16]
    channel13 = channels[12::16]
    channel14 = channels[13::16]
    channel15 = channels[14::16]
    channel16 = channels[15::16]
    
    #print len(channel1)

    #for i in range(20):
    #    print("channels:%.4X %.4X %.4X %.4X") % (channels[i*4], channels[1+i*4], channels[2+i*4], channels[3+i*4])
    #    print("channel1:%.4X") % (channel1[i])
    #    print("channel2:     %.4X") % (channel2[i])
    #    print("channel3:          %.4X") % (channel3[i])
    #    print("channel4:               %.4X") % (channel4[i])


    file = open("adc_100k_acq.txt", 'w')
    for i in range(len(channel1)):
        file.write("%5d, %5d, %5d, %5d, %5d, %5d, %5d, %5d, %5d, %5d, %5d, %5d, %5d, %5d, %5d, %5d, %5d\n" % (time_base[i], channel1[i], channel2[i], channel3[i], channel4[i], channel5[i], channel6[i], channel7[i], channel8[i], channel9[i], channel10[i], channel11[i], channel12[i], channel13[i], channel14[i], channel15[i], channel16[i]))
        #file.write("%d, %.4X, %.4X, %.4X, %.4X\n" % (time_base[i], channel1[i], channel2[i], channel3[i], channel4[i]))
        #print("%d, %.4X, %.4X, %.4X, %.4X" % (time_base[i], channel1[i], channel2[i], channel3[i], channel4[i]))
        #print("%d, %d, %d, %d, %d" % (time_base[i], channel1[i], channel2[i], channel3[i], channel4[i]))


    print '\nBye bye ...'
    sys.exit()
