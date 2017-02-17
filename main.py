#!/usr/bin/env python

"""
main.py:
Module to start the Graphical User Interface and perform the snake robot simulation in parallel.
"""

__author__      = "Rotem Mordoch"


import time
import sys
import GUI
from threading import Thread
from serial_port import SerialPort


global gui_thread
MAX_FREQUENCY = 10  # maximum frequency value that is allowed to apply


def init_gui():
    """
    Initialize GUI
    """
    global app
    root = GUI.init_gui_aux()
    app = GUI.Application(root)
    root.mainloop()


class Simulation():
    """
    Snake robot simulation class
    """
    def __init__(self):
        self.sp = SerialPort()
        self.serial = self.sp.initialize()

    def init_simulation(self):
        """
        Initialize actual number of slaves that are found by the master
        Error is raised if no slaves were found after 5 seconds at most
        """
        t = 0
        prev_time = time.time()
        input_line = self.serial.readline()  # reading data from Arduino
        # update number of slaves according to message from master - 'total devices number: X'
        while not input_line.startswith('total devices number'):
            t += time.time() - prev_time
            prev_time = time.time()
            if t >= 5:  # allow up to 5 seconds wait for the update from master
                sys.exit('Error: could not find slaves')
            input_line = self.serial.readline()
        arr = input_line.split(':')
        if int(arr[1]) == 0:  # 'total devices number: 0'
            sys.exit('Error: 0 slaves were found')
        self.sp.set_num_of_slaves(int(arr[1]))  # set number of slaves that were found
        print (arr[1] + ' slaves were found')

    def perform_simulation(self):
        """
        Simulate gaits by updating joints positions
        """
        # simulate as long as the GUI is running
        while gui_thread.isAlive():
            if app.is_valid():
                # update frequency and amplitude according to speed scalar
                frequency, amplitude = self.update_speed()
                # fetch current parameters from GUI
                amplitude_list = amplitude[:self.sp.get_num_of_slaves()]
                frequency_list = frequency[:self.sp.get_num_of_slaves()]
                # when number of slaves is odd, update also the last joint
                if self.sp.get_num_of_slaves() % 2 == 1:
                    phase_o = app.get_robot_phase_o()[:self.sp.get_num_of_slaves() / 2 + 1]
                else:
                    phase_o = app.get_robot_phase_o()[:self.sp.get_num_of_slaves() / 2]
                phase_e = app.get_robot_phase_e()[:self.sp.get_num_of_slaves() / 2]
                # merge odd and even phase lists
                phase_list = [None] * self.sp.get_num_of_slaves()
                phase_list[::2] = phase_o
                phase_list[1::2] = phase_e
                # write command to master
                if app.is_rel():
                    self.sp.control_joints_individually_r(amplitude_list, frequency_list, phase_list)
                else:
                    self.sp.control_joints_individually_s(amplitude_list, frequency_list, phase_list)

    @staticmethod
    def update_speed():
        """
        Update frequency and amplitude according to speed scalar
        In case frequency exceeds MAX_FREQUENCY increase amplitude
        """
        speed = app.get_speed_scalar()
        frequency = [int(round(x * speed)) for x in app.get_robot_frequency()]  # update frequency according to speed scalar
        amplitude = app.get_robot_amplitude()
        max_freq = max(frequency)
        if max_freq > MAX_FREQUENCY:
            idx_max_freq = frequency.index(max_freq)
            # compute the new speed scalar to preserve the joints frequency ratio
            new_speed = float(MAX_FREQUENCY) / app.get_robot_frequency()[idx_max_freq]
            frequency = [int(round(x * new_speed)) for x in app.get_robot_frequency()]  # update frequency according to new speed scalar
            amplitude = [int(round(x * speed)) for x in app.get_robot_amplitude()]  # increase amplitude
        return frequency, amplitude


if __name__ == '__main__':
    gui_thread = Thread(target=init_gui, args=())  # initialize GUI thread
    gui_thread.setDaemon(True)  # set daemon = True, to terminate GUI thread when main thread dies
    gui_thread.start()
    sim = Simulation()
    sim.init_simulation()
    sim.perform_simulation()
