#!/usr/bin/env python

"""
command_conversion.py:
Function to convert the old command format that is sent to the master to the new format.
Reference: oldCommand2newCommand.m
"""

__author__      = "Emrecan Tarakci, Rotem Mordoch"


import math


def old_command_2_new_command(old):
    # return value
    new_cmd_int = []
    # components
    id = []  # joint ids
    cmd_type = []
    A = []  # amplitude
    f = []  # frequency
    p = []  # phase
    old_cmds = old.split('&')
    n = len(old_cmds)
    for i in xrange(n):
        # first byte
        joint_cmd = old_cmds[i]
        values = joint_cmd.split(':')
        if len(values) != 5:
            print ('Incorrect command pattern! Please use [id, command type, amplitude, frequency, phase]')
            return None
        id.append(int(values[0]))
        cmd_type.append(values[1])
        A.append(int(values[2]))
        f.append(int(values[3]))
        p.append(int(values[4]))

    for i in xrange(n):
        current_id = id[i]
        if current_id > 30:
            print ('Joint id exceeds 30')
            return None
        current_id = current_id << 3
        if cmd_type[i] == 'S':
            cmd = 0
        elif cmd_type[i] == 'R':
            cmd = 1
        else:
            cmd = 7
        if cmd >= 7:
            print ('Incorrect command type')
            return None
        first_byte = current_id + cmd

        # second byte
        if A[i] < 0 or A[i] >= 255:
            print ('Amplitude should be in 0-255')
            return None
        second_byte = A[i]

        # third byte
        if f[i] < 0 or f[i] >= 255:
            print ('Frequency should be in 0-255')
            return None
        third_byte = f[i]

        # fourth byte
        # if statement checks for p[i] < 629 and not 255. MATLAB code mistake?
        if p[i] < 0 or p[i] > 2*math.pi*100:
            print ('Phase should be in 0-255')
            return None
        fourth_byte = int(round(p[i] / 2.512))

        # integer format
        new_cmd_int += [first_byte, second_byte, third_byte, fourth_byte]

    # end of command addition
    new_cmd_int.append(255)
    return new_cmd_int
