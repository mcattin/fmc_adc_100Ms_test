#!/usr/bin/python

import sys
import rr
import time
import spi

class CLTC217x:

    R_RST = 0x00
    R_FMT = 0x01
    R_OUTMODE = 0x02
    R_TESTPAT_MSB = 0x03
    R_TESTPAT_LSB = 0x04

    RST = (1<<7)

    FMT_DCSOFF = (1<<7)
    FMT_RAND = (1<<6)
    FMT_TWOSCOMP = (1<<5)
    FMT_SLEEP = (1<<4)
    FMT_CH4_NAP = (1<<3)
    FMT_CH3_NAP = (1<<2)
    FMT_CH2_NAP = (1<<1)
    FMT_CH1_NAP = (1<<0)

    OUTMODE_ILVDS_3M5 = (0<<5)
    OUTMODE_ILVDS_4M0 = (1<<5)
    OUTMODE_ILVDS_4M5 = (2<<5)
    OUTMODE_ILVDS_3M0 = (4<<5)
    OUTMODE_ILVDS_2M5 = (5<<5)
    OUTMODE_ILVDS_2M1 = (6<<5)
    OUTMODE_ILVDS_1M75 = (7<<5)
    OUTMODE_TERMON = (1<<4)
    OUTMODE_OUTOFF = (1<<3)
    OUTMODE_2L_16B = (0<<0)
    OUTMODE_2L_14B = (1<<0)
    OUTMODE_2L_12B = (2<<0)
    OUTMODE_1L_14B = (5<<0)
    OUTMODE_1L_12B = (6<<0)
    OUTMODE_1L_16B = (7<<0)

    TESTPAT_MSB_OUTTEST = (1<<7)
    TESTPAT_MSB_MASK = 0x3F
    TESTPAT_LSB_MASK = 0xFF

    # addr = ltc217x register address (1 byte)
    # value = value to write to the register (1 byte)
    def wr_reg(self, addr, value):
        tx = [value, addr]
        self.spi.transaction(self.slave, tx)

    def rd_reg(self, addr):
        tx = [0xFF, (addr | 0x80)]
        rx = self.spi.transaction(self.slave, tx)
        return (rx[0] & 0xFF)

    def __init__(self, spi, slave):
        self.spi = spi
        self.slave = slave
        self.wr_reg(self.R_RST, self.RST)
        self.wr_reg(self.R_FMT, 0)
        self.wr_reg(self.R_OUTMODE, (self.OUTMODE_ILVDS_4M5 | self.OUTMODE_2L_16B | self.OUTMODE_TERMON))

    def get_fmt(self):
        return self.rd_reg(self.R_FMT)

    def get_outmode(self):
        return self.rd_reg(self.R_OUTMODE)

    def get_testpat(self):
        return (((self.rd_reg(self.R_TESTPAT_MSB) & self.TESTPAT_MSB_MASK)<<8)
                + (self.rd_reg(self.R_TESTPAT_LSB) & self.TESTPAT_LSB_MASK))

    def get_testpat_stat(self):
        return ((self.rd_reg(self.R_TESTPAT_MSB))>>7)

    def set_testpat(self, pattern):
        self.wr_reg(self.R_TESTPAT_MSB, ((pattern>>8) & self.TESTPAT_MSB_MASK))
        self.wr_reg(self.R_TESTPAT_LSB, (pattern & self.TESTPAT_LSB_MASK))

    def en_testpat(self):
        reg = self.rd_reg(self.R_TESTPAT_MSB)
        reg |= self.TESTPAT_MSB_OUTTEST
        self.wr_reg(self.R_TESTPAT_MSB, reg)

    def dis_testpat(self):
        reg = self.rd_reg(self.R_TESTPAT_MSB)
        reg &= ~self.TESTPAT_MSB_OUTTEST
        self.wr_reg(self.R_TESTPAT_MSB, reg)

    def print_regs(self):
        print '\nLTC217x registers:'
        for i in range(0,5):
            print("reg %d: %.2X") % (i, self.rd_reg(i))
