#!/usr/bin/env python

"""
GUI.py:
Module to handle Graphical User Interface to control the snake robot according to an XML file of predefined gaits.
"""

__author__      = "Rotem Mordoch"


from Tkinter import *
import tkFileDialog
from xml.dom import minidom


MAX_NUM_OF_SLAVES = 20
LARGE_FONT = ("Verdana", 12)


class Application(Frame):
    """ GUI class """
    def __init__(self, parent):
        """
        Initialize some GUI widgets and parameters
        """
        Frame.__init__(self, parent)
        self.pack()
        title = Label(self, text="Please select the XML file of the defined gaits parameters:", font=LARGE_FONT)
        title.pack(pady=10, padx=10)
        self.xml_button = Button(self, text="Browse...", command=self.load_xml)
        self.xml_button.config(height=2, width=10)
        self.xml_button.pack()
        self.speed_value = DoubleVar()
        self.speed_value.set(1)
        self.slider = Scale(self, orient=HORIZONTAL, length=250, from_=0.2, to=2, tickinterval=0.2, resolution=0.2,
                            variable=self.speed_value)
        self.radio_value = StringVar()
        self.radio_value.set('R')
        self.valid = False  # boolean to check whether application is valid (xml file was loaded)
        self.gaits = []  # available gaits in xml file
        # current gaits parameters
        self.robot_frequency = [0] * (MAX_NUM_OF_SLAVES)
        self.robot_amplitude = [0] * (MAX_NUM_OF_SLAVES)
        self.robot_phase_o = [0] * (MAX_NUM_OF_SLAVES / 2)
        self.robot_phase_e = [0] * (MAX_NUM_OF_SLAVES / 2)

    def load_xml(self):
        """
        Load xml file and parse gaits widgets
        """
        fileName = tkFileDialog.askopenfilename(filetypes=(("XML Files", "*.xml"), ("All Files", "*")))
        self.xml_button['state'] = 'disabled'
        # parse xml file
        xml_doc = minidom.parse(fileName)
        self.gaits = xml_doc.getElementsByTagName('gait')
        if len(self.gaits) == 0:
            print 'Error: wrong XML format - no <gait> nodes. Please follow the format definition in the README file.'
            sys.exit()
        title = Label(self, text="Please select the desired gait:", font=LARGE_FONT)
        title.pack(pady=10, padx=10)
        self.create_gaits_widgets()
        self.create_const_widgets()
        self.valid = True  # application marked as valid after xml file was loaded

    def create_gaits_widgets(self):
        """
        Create gaits widgets according to xml file
        """
        for gait in self.gaits:
            gait_id = gait.getAttribute('id')
            if not gait_id:
                print 'Warning: id attribute is not defined (gait without a name). Can cause to unexpected behaviour.'
            widget = Button(self, text=gait_id, command=lambda gait_id=gait_id: self.callback(gait_id))
            widget.config(height=2, width=15)
            widget.pack()

    def create_const_widgets(self):
        """
        Create some constant widgets (not defined in xml file)
        """
        slider_title = Label(self, text="Speed")
        slider_title.pack(pady=10, padx=10)
        self.slider.pack()
        self.r_radio = Radiobutton(self, text="Relative", variable=self.radio_value, value='R')
        self.r_radio.pack()
        self.s_radio = Radiobutton(self, text="Absolute", variable=self.radio_value, value='S')
        self.s_radio.pack()
        self.r_radio['state'] = 'disabled'
        self.s_radio['state'] = 'disabled'
        curr_gait_title = Label(self, text='Current Gait Activated:')
        curr_gait_title.pack()
        self.gait_title = Label(self, text='')
        self.gait_title.pack()

    def callback(self, gait_name):
        """
        Widgets callback
        This function is called whenever a gait widget is selected
        """
        # allow only to 'Individual Control' gait to switch between relative and absolute
        if gait_name == 'Individual Control':
            self.r_radio['state'] = 'normal'
            self.s_radio['state'] = 'normal'
        else:
            self.radio_value.set('R')
            self.r_radio['state'] = 'disabled'
            self.s_radio['state'] = 'disabled'
        self.parse_robot_gait_parameters(gait_name)
        self.gait_title.config(text=gait_name)

    def parse_robot_gait_parameters(self, gait_name):
        """
        Fetch corresponding gait parameters from xml file and update application parameters
        """
        for gait in self.gaits:
            gait_id = gait.getAttribute('id')
            if gait_id == gait_name:  # find which gait widget is selected
                robot_freq_elements = gait.getElementsByTagName('freq_robot')
                robot_amp_elements = gait.getElementsByTagName('amp_robot')
                robot_phase_o_elements = gait.getElementsByTagName('phase_o_robot')
                robot_phase_e_elements = gait.getElementsByTagName('phase_e_robot')
                # gaits where all joints have the same parameters
                if (len(robot_freq_elements) == 1 and len(robot_amp_elements) == 1 and
                    len(robot_phase_o_elements) == 1 and len(robot_phase_e_elements) == 1):
                    # duplicate parameters values for all joints
                    robot_freq_elements *= MAX_NUM_OF_SLAVES
                    robot_amp_elements *= MAX_NUM_OF_SLAVES
                    robot_phase_o_elements *= (MAX_NUM_OF_SLAVES / 2)
                    robot_phase_e_elements *= (MAX_NUM_OF_SLAVES / 2)
                # convert strings to integers
                if (len(robot_freq_elements) == MAX_NUM_OF_SLAVES and
                    len(robot_amp_elements) == MAX_NUM_OF_SLAVES and
                    len(robot_phase_o_elements) == MAX_NUM_OF_SLAVES / 2 and
                    len(robot_phase_e_elements) == MAX_NUM_OF_SLAVES / 2):
                    self.robot_frequency = map(lambda x: int(x.firstChild.data), robot_freq_elements)
                    self.robot_amplitude = map(lambda x: int(x.firstChild.data), robot_amp_elements)
                    self.robot_phase_o = map(lambda x: int(x.firstChild.data), robot_phase_o_elements)
                    self.robot_phase_e = map(lambda x: int(x.firstChild.data), robot_phase_e_elements)
                # handle HOLD gait separately
                elif (len(robot_freq_elements) == 1 and len(robot_amp_elements) == 0 and
                      len(robot_phase_o_elements) == 0 and len(robot_phase_e_elements) == 0):
                    robot_freq_elements *= MAX_NUM_OF_SLAVES
                    self.robot_frequency = map(lambda x: int(x.firstChild.data), robot_freq_elements)
                else:
                    print ('Error: wrong XML format - the selected gait has either too many or too less parameters.\n'
                           'Please follow the format definition in the README file.')
                    sys.exit()

    # application getters
    def get_speed_scalar(self):
        return self.speed_value.get()

    def get_robot_frequency(self):
        return self.robot_frequency

    def get_robot_amplitude(self):
        return self.robot_amplitude

    def get_robot_phase_o(self):
        return self.robot_phase_o

    def get_robot_phase_e(self):
        return self.robot_phase_e

    def is_rel(self):
        if self.radio_value.get() == 'R':
            return True
        return False

    def is_valid(self):
        return self.valid


def init_gui_aux():
    """
    Auxiliary function to initialize GUI
    """
    root = Tk()
    root.title("Snake Robot GUI")
    root.geometry("600x633")
    root.resizable(width=False, height=False)
    return root
