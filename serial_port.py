#!/usr/bin/env python

"""
serial_port.py:
Module to establish communication with the master Arduino board of the snake robot via a USB port.
"""

__author__      = "Rotem Mordoch"


import serial
import platform
import sys
from command_conversion import old_command_2_new_command


class SerialPort():
    """
    Serial port class
    """
    def __init__(self):
        self.data_rate = 57600
        self.num_of_slaves = 20

    @staticmethod
    def find_serial_port():
        """
        Find port according to platform
        """
        system_name = platform.system()
        if system_name == 'Windows':
            return 'COM3'
        elif system_name == 'Darwin':
            # Mac
            return '/dev/tty.usbserial-A9007UX1'
        elif system_name == 'Linux':
            return '/dev/ttyUSB0'

    def initialize(self):
        """
        Initialize serial port
        """
        global ser
        port_name = self.find_serial_port()
        try:
            ser = serial.Serial(port_name, self.data_rate)
        except serial.SerialException as detail:
            print 'Handling serial error:', detail
            sys.exit('Error: could not find slaves')
        return ser

    def control_joints_individually_r(self, amplitude_list, frequency_list, phase_list):
        """
        Send command to master to update relative angles
        The old command format (<slave_id>:R:<amplitude>:<frequency>:<phase>) is converted to the new format before sending it
        """
        cmd = ''
        for i in xrange(1, self.num_of_slaves + 1):
            cmd += str(i) + ':R:' + str(amplitude_list[i - 1]) + ':' + str(frequency_list[i - 1]) + ':' + str(phase_list[i - 1])
            if i < self.num_of_slaves:
                cmd += '&'
        new_cmd = old_command_2_new_command(cmd)  # convert old format to new format
        if new_cmd:
            ser.write(bytearray(new_cmd))  # writing data to Arduino

    def control_joints_individually_s(self, amplitude_list, frequency_list, phase_list):
        """
        Send command to master to update absolute angles
        The old command format (<slave_id>:S:<amplitude>:<frequency>:<phase>) is converted to the new format before sending it
        """
        cmd = ''
        for i in xrange(1, self.num_of_slaves + 1):
            cmd += str(i) + ':S:' + str(amplitude_list[i - 1]) + ':' + str(frequency_list[i - 1]) + ':' + str(phase_list[i - 1])
            if i < self.num_of_slaves:
                cmd += '&'
        new_cmd = old_command_2_new_command(cmd)  # convert old format to new format
        if new_cmd:
            ser.write(bytearray(new_cmd))  # writing data to Arduino

    # getter
    def get_num_of_slaves(self):
        return self.num_of_slaves

    # setter
    def set_num_of_slaves(self, value):
        self.num_of_slaves = value
