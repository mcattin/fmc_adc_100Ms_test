#!/usr/bin/python

import sys
import rr
import time

class COpenCoresSPI:

	R_RX = [0x00, 0x04, 0x08, 0x0C]
	R_TX = [0x00, 0x04, 0x08, 0x0C]
	R_CTRL = 0x10
	R_DIV = 0x14
	R_SS = 0x18

	LGH_MASK = (0x7F)
	CTRL_GO = (1<<8)
        CTRL_BSY = (1<<8)
	CTRL_RXNEG = (1<<9)
	CTRL_TXNEG = (1<<10)
	CTRL_LSB = (1<<11)
       	CTRL_IE = (1<<12)
        CTRL_ASS = (1<<13)

        DIV_MASK = (0xFFFF)

        SS_SEL = [0x1, 0x2, 0x4, 0x8, 0x10, 0x20, 0x40]

	conf = 0x0

	def wr_reg(self, addr, val):
		self.bus.iwrite(0, self.base_addr +  addr, 4, val)

	def rd_reg(self, addr):
		return self.bus.iread(0, self.base_addr + addr, 4)

	def __init__(self, bus, base_addr, divider):
		self.bus = bus;
		self.base_addr = base_addr;
		self.wr_reg(self.R_DIV, (divider & self.DIV_MASK));
		# default configuration
		self.conf = self.CTRL_ASS | self.CTRL_TXNEG

	def wait_busy(self):
		while(self.rd_reg(self.R_CTRL) & self.CTRL_BSY):
			pass

	def config(self, ass, rx_neg, tx_neg, lsb, ie):
		self.conf = 0
		if(ass):
			self.conf |= self.CTRL_ASS
		if(tx_neg):
			self.conf |= self.CTRL_TXNEG
		if(rx_neg):
			self.conf |= self.CTRL_RXNEG
		if(lsb):
			self.conf |= self.CTRL_LSB
		if(ie):
			self.conf |= self.CTRL_IE

	# slave = slave number (0 to 7)
	# data = byte data array to send, in case if read fill with dummy data of the right size
	def transaction(self, slave, data):
		txrx = [0x00000000, 0x00000000, 0x00000000, 0x00000000]
		for i in range(0,len(data)):
			txrx[i/4] += (data[i]<<((i%4)*8))
			#print("tx[%d]=%.8X data[%d]=%.2X") %(i,txrx[i/4],i,data[i])

		for i in range(0, len(txrx)):
			self.wr_reg(self.R_TX[i], txrx[i])

		self.wr_reg(self.R_SS, self.SS_SEL[slave])
		self.wr_reg(self.R_CTRL, (self.LGH_MASK & (len(data)<<3)) | self.CTRL_GO | self.conf)
		self.wait_busy()

		for i in range(0, len(txrx)):
			txrx[i] = self.rd_reg(self.R_RX[i])
			#print("rx[%d]=%.8X") %(i,txrx[i])

		return txrx

#gennum = rr.Gennum();
#spi = COpenCoresSPI(gennum, 0x80000, 500);
