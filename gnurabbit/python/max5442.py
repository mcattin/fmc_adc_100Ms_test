#!/usr/bin/python

import sys
import rr
import time
import spi
import csr

class CMAX5442:


    def __init__(self, spi, slave):
        self.spi = spi
        self.slave = slave

    # offset = value to write to the DAC (2 bytes)
    def set_offset(self, offset):
        tx = [(offset & 0xFF), ((offset & 0xFF00)>>8)]
        #print('[max5442] Set offset: %.4X') % offset
        #for i in range(len(tx)):
        #    print('[max5442] tx[%d]: %.2X') %(i, tx[i])
        self.spi.transaction(self.slave, tx)

