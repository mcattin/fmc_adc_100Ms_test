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

    time.sleep(.5)

    fmc_adc.i2c_scan()
    fmc_adc.print_unique_id()
    
    for i in range(1000):
        fmc_adc.print_temp()
        time.sleep(1)

    print '\nBye bye ...'
    sys.exit()
