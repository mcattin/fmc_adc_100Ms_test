#!/usr/bin/python

import sys
import rr
import time
import i2c


class CMCP9801:

    R_TA = 0x00
    R_CFG = 0x01
    R_THYST = 0x02
    R_TSET = 0x03

    CFG_ONESHOT = (1<<7)
    CFG_RES = (1<<5)
    CFG_FAULT = (1<<3)
    CFG_ALERT_POL = (1<<2)
    CFG_MODE = (1<<1)
    CFG_SHDN = (1<<0)

    RES = {'9bit':0x0, '10bit':0x1, '11bit':0x2, '12bit':0x3}
    FAULT = {1:0x0 , 2:0x1 , 4:0x2 , 6:0x6}

    def __init__(self, i2c, addr):
        self.i2c = i2c
        self.addr = addr

    def rd_reg(self, addr, size):
        data=[]
        self.i2c.start(self.addr, True)
        self.i2c.write(addr, False)
        self.i2c.start(self.addr, False)
        for i in range(0, size-1):
            data.append(self.i2c.read(False))
        data.append(self.i2c.read(True))
        return data

    def wr_reg(self, addr, data):
        self.i2c.start(self.addr, True)
        self.i2c.write(addr, False)
        for i in range(0, size-1):
            self.i2c.write(data[i], False)
        self.i2c.write(data[size-1], True)

    # get temperature
    #   return: float (Celsius)
    def get_temp(self):
        reg = self.rd_reg(self.R_TA, 2)
        return (reg[0]+(reg[1]/256.0))

    # shutdown
    def shutdown(self, state):
        reg[0] = self.rd_reg(self.R_CFG, 1)
        if('ON' == state):
            reg[0] |= CFG_SHDN
        elif('OFF' == state):
            reg[0] &= ~(CFG_SHDN)
        else:
            raise Exception('Unsupported parameter, should be ON or OFF.')
        self.wr_reg(self.R_CFG, reg)

    # set config
    #def set_config(self, shot, res, fault, alert_pol, mode):

    # get config

    # set hysteresis temp

    # get hysteresis temp

    # set limit temp

    # get limit temp
