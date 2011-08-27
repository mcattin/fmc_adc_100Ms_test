#!/usr/bin/python

import sys
import rr
import time
import onewire


class CDS18B20:

    # ROM commands
    ROM_SEARCH = 0xF0
    ROM_READ = 0x33
    ROM_MATCH = 0x55
    ROM_SKIP = 0xCC
    ROM_ALARM_SEARCH = 0xEC

    # DS18B20 fonctions commands
    CONVERT_TEMP = 0x44
    WRITE_SCRATCHPAD = 0x4E
    READ_SCRATCHPAD = 0xBE
    COPY_SCRATCHPAD = 0x48
    RECALL_EEPROM = 0xB8
    READ_POWER_SUPPLY = 0xB4

    # Thermometer resolution configuration
    RES = {'9-bit':0x0, '10-bit':0x1, '11-bit':0x2, '12-bit':0x3}

    def __init__(self, onewire, port):
        self.onewire = onewire
        self.port = port

    def read_serial_number(self):
        print('[DS18B20] Reading serial number')
        if(1 != self.onewire.reset(self.port)):
            print('[DS18B20] No presence pulse detected')
            return -1
        else:
            print('[DS18B20] Write ROM command %.4X') % ROM_READ
            err = self.onewire.write_byte(self.port, ROM_READ)
            family_code = self.onewire.read_byte(self.port)
            for i in range(6):
                serial_number |= self.onewire.read_byte(self.port) << (i*8)
            crc = self.onewire.read_byte(self.port)
            print('[DS18B20] Family code  : %.2X') % family_code
            print('[DS18B20] Serial number: %.12X') % serial_number
            print('[DS18B20] CRC          : %.2X') % crc
        return ((crc<<56) | (serial_number<<8) | family_code)

    def access(self, serial_number):
        print('[DS18B20] Accessing device')
        if(1 != self.onewire.reset(self.port)):
            print('[DS18B20] No presence pulse detected')
            return -1
        else:
            print('[DS18B20] Write ROM command %.4X') % ROM_MATCH
            err = self.onewire.write_byte(self.port, ROM_MATCH)
            self.onewire.write_block(self.port, serial_number)
            return 0

    def read_temp(self, serial_number):
        print('[DS18B20] Reading temperature')
        err = self.access(serial_number)
        print('[DS18B20] Write function command %.4X') % CONVERT_TEMP
        err = self.onewire.write_byte(self.port, CONVERT_TEMP)
        time.sleep(1)
        err = self.access(serial_number)
        print('[DS18B20] Write function command %.4X') % READ_SCRATCHPAD
        err = self.onewire.write_byte(self.port, READ_SCRATCHPAD)
        data = self.onewire.read_block(self.port, 9)
        temp = ((data[1] << 12) | ((data[0] & 0xFF00)>>4)) + (((data[0] & 0x00FF)<<4)/256.0)
        return temp

    # Set temperature thresholds

    # Configure thermometer resolution
