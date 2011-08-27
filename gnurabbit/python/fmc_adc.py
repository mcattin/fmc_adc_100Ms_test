#!   /usr/bin/env	python
#    coding: utf8

import sys
import rr
import random
import time
import spi
import ltc217x
import csr
import max5442
import i2c
import onewire
import ds18b20
#import mcp9801
import si57x


class CFmcAdc100Ms:

    FMC_SYS_I2C_ADDR = 0x60000

    FMC_SPI_ADDR = 0x70000
    FMC_SPI_DIV = 100
    FMC_SPI_SS = {'ADC': 0,'DAC1': 1,'DAC2': 2,'DAC3': 3,'DAC4': 4}

    FMC_I2C_ADDR = 0x80000
    #MCP9801_ADDR = 0x48
    SI570_ADDR = 0x55

    FMC_ONEWIRE_ADDR = 0xA0000

    FMC_CSR = {0x00:'Control register',
               0x04:'Status register',
               0x08:'Trigger configuration register',
               0x0C:'Trigger delay register',
               0x10:'Software trigger register',
               0x14:'Number of shots register',
               0x18:'Trigger UTC (LSB) register',
               0x1C:'Trigger UTC (MSB) register',
               0x20:'Start UTC (LSB) register',
               0x24:'Start UTC (MSB) register',
               0x28:'Stop UTC (LSB) register',
               0x2C:'Stop UTC (MSB) register',
               0x30:'Decimation factor register',
               0x34:'Pre-trigger samples register',
               0x38:'Post-trigger samples register',
               0x3C:'Samples counter register',
               0x40:'CH1 control register',
               0x44:'CH1 current value register',
               0x48:'CH2 control register',
               0x4C:'CH2 current value register',
               0x50:'CH3 control register',
               0x54:'CH3 current value register',
               0x58:'CH4 control register',
               0x5C:'CH4 current value register',}
    FMC_CSR_ADDR = 0x90000
    R_CTL = 0x00
    R_STA = 0x04
    R_TRIG_CFG = 0x08
    R_TRIG_DLY = 0x0C
    R_SW_TRIG = 0x10
    R_SHOTS = 0x14
    R_TRIG_UTC_L = 0x18
    R_TRIG_UTC_H = 0x1C
    R_START_UTC_L = 0x20
    R_START_UTC_H = 0x24
    R_STOP_UTC_L = 0x28
    R_STOP_UTC_H = 0x2C
    R_SRATE = 0x30
    R_PRE_SAMPLES = 0x34
    R_POST_SAMPLES = 0x38
    R_SAMP_CNT = 0x3C
    R_CH1_SSR = 0x40
    R_CH1_VALUE = 0x44
    R_CH2_SSR = 0x48
    R_CH2_VALUE = 0x4C
    R_CH3_SSR = 0x50
    R_CH3_VALUE = 0x54
    R_CH4_SSR = 0x58
    R_CH4_VALUE = 0x5C

    CTL_FSM_CMD = 0
    CTL_CLK_EN = 2
    CTL_OFFSET_DAC_CLR_N = 3
    CTL_BSLIP = 4
    CTL_TEST_DATA_EN = 5
    CTL_MASK = 0x2C

    FSM_CMD_MASK = 0x00000003
    FSM_CMD_START = 0x1
    FSM_CMD_STOP = 0x2

    STA_FSM = 0
    STA_SERDES_SYNCED = 4

    FSM_MASK = 0x00000007
    FSM_STATES = ['N/A','IDLE','PRE_TRIG','WAIT_TRIG',
                  'POST_TRIG','DECR_SHOT','N/A','others']

    TRIG_CFG_HW_SEL = 0
    TRIG_CFG_EXT_POL = 1
    TRIG_CFG_HW_EN = 2
    TRIG_CFG_SW_EN = 3
    TRIG_CFG_INT_SEL = 4
    TRIG_CFG_INT_THRES = 16

    INT_SEL_MASK = 0x00000030
    INT_THRES_MASK = 0xFFFF0000

    IN_TERM = (1<<3)
    IN_TERM_MASK = 0x08
    IN_RANGES = {'100mV': 0x23, '1V': 0x11, '10V': 0x45, 'CAL': 0x40}


    def channel_addr(self, channel, reg):
        if(channel < 1 or channel > 4):
            raise Exception('Channel number not in range (1 to 4).')
        else:
            addr = (reg + (8*(channel - 1)))
            #print("Channel %d address: %.2X") % (channel, addr)
            return addr

    def __init__(self, bus):
        self.bus = bus
        self.fmc_spi = spi.COpenCoresSPI(self.bus, self.FMC_SPI_ADDR, self.FMC_SPI_DIV)
        self.adc_cfg = ltc217x.CLTC217x(self.fmc_spi, self.FMC_SPI_SS['ADC'])
        self.fmc_i2c = i2c.COpenCoresI2C(self.bus, self.FMC_I2C_ADDR, 249)
        self.fmc_onewire = onewire.COpenCoresOneWire(self.bus, self.FMC_ONEWIRE_ADDR, 624, 124)
        self.ds18b20 = ds18b20.CDS18B20(self.fmc_onewire, 0)
        #self.mcp9801 = mcp9801.CMCP9801(self.fmc_i2c, self.MCP9801_ADDR)
        self.si570 = si57x.CSi57x(self.fmc_i2c, self.SI570_ADDR)
        self.fmc_adc_csr = csr.CCSR(self.bus, self.FMC_CSR_ADDR)
        self.dac_ch1 = max5442.CMAX5442(self.fmc_spi, self.FMC_SPI_SS['DAC1'])
        self.dac_ch2 = max5442.CMAX5442(self.fmc_spi, self.FMC_SPI_SS['DAC2'])
        self.dac_ch3 = max5442.CMAX5442(self.fmc_spi, self.FMC_SPI_SS['DAC3'])
        self.dac_ch4 = max5442.CMAX5442(self.fmc_spi, self.FMC_SPI_SS['DAC4'])
        self.fmc_adc_csr.wr_reg(self.R_CTL, ((1<<self.CTL_CLK_EN)|(1<<self.CTL_OFFSET_DAC_CLR_N)))
        self.adc_cfg.dis_testpat()

    #def __del__(self):
        # Disable ADC clock and reset offset correction DAC
        #self.fmc_adc_csr.wr_reg(self.R_CTL, 0)

    # print LTC2174 configuration
    def print_adc_config(self):
        print '\nLTC2174 configuration'
        print("Format and power down register : %.2X") % self.adc_cfg.get_fmt()
        print("Output mode register           : %.2X") % self.adc_cfg.get_outmode()
        print("Test pattern                   : %.4X") % self.adc_cfg.get_testpat()
        print("Test pattern status            : %.1X") % self.adc_cfg.get_testpat_stat()

    # print FMC unique ID
    def print_unique_id(self):
        print('FMC unique ID: %.12X') % self.ds18b20.read_serial_number()

    # print FMC temperature
    def print_temp(self):
        serial_number = self.ds18b20.read_serial_number()
        print("FMC temperature: %3.3f°C") % self.ds18b20.read_temp(serial_number)

    # scan FMC i2c bus
    def i2c_scan(self):
        print '\nScan I2C bus'
        self.fmc_i2c.scan()

    # Set input range
    def set_input_range(self, channel, range):
        addr = self.channel_addr(channel,self.R_CH1_SSR)
        reg = (self.IN_TERM_MASK & self.fmc_adc_csr.rd_reg(addr))
        #print("ssr reg ch%1d: %.8X") %(channel, reg)
        if(range in self.IN_RANGES):
            reg |= self.IN_RANGES[range]
        else:
            raise Exception('Unsupported parameter.')
        #print("ssr reg ch%1d: %.8X") %(channel, reg)
        self.fmc_adc_csr.wr_reg(addr, reg)
        #print("ssr reg ch%1d: %.8X") %(channel, self.fmc_adc_csr.rd_reg(addr))

    # DC offset calibration
    def dc_offset_calibr(self, channel, offset):
        if(1 == channel):
            self.dac_ch1.set_offset(offset)
        elif(2 == channel):
            self.dac_ch2.set_offset(offset)
        elif(3 == channel):
            self.dac_ch3.set_offset(offset)
        elif(4 == channel):
            self.dac_ch4.set_offset(offset)
        else:
            raise Exception('Unsupported parameter, channel number from 1 to 4')

    # Set 50ohms termination
    def set_input_term(self, channel, state):
        addr = self.channel_addr(channel,self.R_CH1_SSR)
        reg = self.fmc_adc_csr.rd_reg(addr)
        #print("ssr reg ch%1d: %.8X") %(channel, reg)
        if('ON' == state):
            reg |= self.IN_TERM
        elif('OFF' == state):
            reg &= ~(self.IN_TERM)
        else:
            raise Exception('Unsupported parameter, should be ON or OFF.')
        #print("ssr reg ch%1d: %.8X") %(channel, reg)
        self.fmc_adc_csr.wr_reg(addr, reg)
        #print("ssr reg ch%1d: %.8X") %(channel, self.fmc_adc_csr.rd_reg(addr))

    # Set decimation factor
    def set_decimation(self, factor):
        self.fmc_adc_csr.wr_reg(self.R_SRATE, factor)

    # Get decimation factor
    def get_decimation(self):
        return self.fmc_adc_csr.rd_reg(self.R_SRATE)

    # Enable Sampling clock (Si570)
    def en_sampfreq(self):
        self.fmc_adc_csr.wr_bit(self.R_CTL, self.CTL_CLK_EN, 1)

    # Disable Sampling clock (Si570)
    def dis_sampfreq(self):
        self.fmc_adc_csr.wr_bit(self.R_CTL, self.CTL_CLK_EN, 0)

    # Serdes calibration
    def serdes_sync(self):
        print("\nStart serdes synchro")
        pattern = 0x3456
        self.adc_cfg.set_testpat(pattern)
        self.adc_cfg.en_testpat()
        print("Test pattern                   : %.4X") % self.adc_cfg.get_testpat()
        print("Test pattern status            : %.1X") % self.adc_cfg.get_testpat_stat()
        while(pattern != self.fmc_adc_csr.rd_reg(self.R_CH1_VALUE)):
            print("CH1 value : %.4X")%self.fmc_adc_csr.rd_reg(self.R_CH1_VALUE)
            print("CH2 value : %.4X")%self.fmc_adc_csr.rd_reg(self.R_CH2_VALUE)
            print("CH3 value : %.4X")%self.fmc_adc_csr.rd_reg(self.R_CH3_VALUE)
            print("CH4 value : %.4X")%self.fmc_adc_csr.rd_reg(self.R_CH4_VALUE)
            self.fmc_adc_csr.wr_bit(self.R_CTL, self.CTL_BSLIP, 1)
            time.sleep(.1)
        self.adc_cfg.dis_testpat()
        print("Serdes synced!")

    # Enable test pattern
    def testpat_en(self, pattern):
        self.adc_cfg.set_testpat(pattern)
        self.adc_cfg.en_testpat()

    # Disable test pattern
    def testpat_dis(self):
        self.adc_cfg.dis_testpat()

    # Print adc config regs
    def print_adc_regs(self):
        self.adc_cfg.print_regs()

    # Set sampling frequency
    #def set_sampfreq(self, freq):

    # Get sampling frequency

    # Get channel configuration
    #def get_channel_config(self, channel):

    # Set trigger configuration
    def set_trig_config(self, hw_sel, ext_pol, hw_en, sw_en, int_sel, int_thres, delay):
        # Hardware trigger select (ext/int)
        self.fmc_adc_csr.wr_bit(self.R_TRIG_CFG, self.TRIG_CFG_HW_SEL, hw_sel)
        # External trigger pulse polarity
        self.fmc_adc_csr.wr_bit(self.R_TRIG_CFG, self.TRIG_CFG_EXT_POL, ext_pol)
        # Hardware trigger enable
        self.fmc_adc_csr.wr_bit(self.R_TRIG_CFG, self.TRIG_CFG_HW_EN, hw_en)
        # Software trigger enable
        self.fmc_adc_csr.wr_bit(self.R_TRIG_CFG, self.TRIG_CFG_SW_EN, sw_en)
        # Internal trigger channel select (1 to 4)
        reg = self.fmc_adc_csr.rd_reg(self.R_TRIG_CFG)
        reg |= ((int_sel<<self.TRIG_CFG_INT_SEL) & self.INT_SEL_MASK)
        self.fmc_adc_csr.wr_reg(self.R_TRIG_CFG, reg)
        # Internal trigger threshold
        reg = self.fmc_adc_csr.rd_reg(self.R_TRIG_CFG)
        reg |= ((int_thres<<self.TRIG_CFG_INT_THRES) & self.INT_THRES_MASK)
        self.fmc_adc_csr.wr_reg(self.R_TRIG_CFG, reg)
        # Trigger delay (in sampling clock ticks)
        self.fmc_adc_csr.wr_reg(self.R_TRIG_DLY, delay)

    # Get trigger configuration

    # Enable test data
    def test_data_en(self):
        reg = self.fmc_adc_csr.rd_reg(self.R_CTL)
        print("R_CTL:%.8X")%reg
        reg |= ((1<<self.CTL_TEST_DATA_EN) & self.CTL_MASK)
        print("R_CTL:%.8X")%reg
        self.fmc_adc_csr.wr_reg(self.R_CTL, reg)

    # Disable test data
    def test_data_dis(self):
        reg = self.fmc_adc_csr.rd_reg(self.R_CTL)
        print("R_CTL:%.8X")%reg
        reg &= (~(1<<self.CTL_TEST_DATA_EN) & self.CTL_MASK)
        print("R_CTL:%.8X")%reg
        self.fmc_adc_csr.wr_reg(self.R_CTL, reg)

    # Start acquisition
    def start_acq(self):
        # Wait for serdes to be synced
        while(0 == self.get_serdes_sync_stat()):
            print 'Wait for serdes to be synced'
            time.sleep(.1)
        reg = self.fmc_adc_csr.rd_reg(self.R_CTL)
        reg |= ((self.FSM_CMD_START<<self.CTL_FSM_CMD) & self.FSM_CMD_MASK)
        reg &= (self.CTL_MASK | self.FSM_CMD_MASK)
        print("R_CTL:%.8X")%reg
        self.fmc_adc_csr.wr_reg(self.R_CTL, reg)

    # Stop acquisition
    def stop_acq(self):
        reg = self.fmc_adc_csr.rd_reg(self.R_CTL)
        reg |= ((self.FSM_CMD_STOP<<self.CTL_FSM_CMD) & self.FSM_CMD_MASK)
        self.fmc_adc_csr.wr_reg(self.R_CTL, reg)

    # Software trigger
    def sw_trig(self):
        while('WAIT_TRIG' != self.get_acq_fsm_state()):
            print self.get_acq_fsm_state()
            time.sleep(.1)
        self.fmc_adc_csr.wr_reg(self.R_SW_TRIG, 0xFFFFFFFF)

    # Set pre-trigger samples
    def set_pre_trig_samples(self, samples):
        self.fmc_adc_csr.wr_reg(self.R_PRE_SAMPLES, samples)

    # Set post-trigger samples
    def set_post_trig_samples(self, samples):
        self.fmc_adc_csr.wr_reg(self.R_POST_SAMPLES, samples)

    # Set number of shots
    def set_shots(self, shots):
        self.fmc_adc_csr.wr_reg(self.R_SHOTS, shots)

    # Get acquisition state machine status
    def get_acq_fsm_state(self):
        state = (self.fmc_adc_csr.rd_reg(self.R_STA) & self.FSM_MASK)
        #print("FSM state: %d")%state
        return self.FSM_STATES[state]

    # Get serdes sync status
    def get_serdes_sync_stat(self):
        return (self.fmc_adc_csr.rd_bit(self.R_STA, self.STA_SERDES_SYNCED))

    # Get ADC core status
    #def get_status(self): 

    # Get Channel current ADC value
    def get_current_adc_value(self, channel):
        addr = self.channel_addr(channel,self.R_CH1_VALUE)
        return self.fmc_adc_csr.rd_reg(addr)

    # Print ADC core config/status
    def print_adc_core_config(self):
        print("\nADC core configuration/status")
        self.fmc_adc_csr.rd_reg(0x04) # Workaround for first read at 0x00 bug
        for i in range(0,0x60,4):
            print("%30s: %.8X") % (self.FMC_CSR[i],self.fmc_adc_csr.rd_reg(i))

    # Print Si570 config
    def print_si570_config(self):
        print("\nPrint Si570 configuration")
        print("RFREQ  : %3.28f") % self.si570.get_rfreq()
        print("N1     : %d") % self.si570.get_n1_div()
        print("HS_DIV : %d") % self.si570.get_hs_div()
