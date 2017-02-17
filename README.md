# GUI for Snake Robot
Task 1 of snake robot lab course - snake robot simulation


1. Connect the snake robot to your machine via a USB port.
2. Place main.py, GUI.py, serial_port.py and command_conversion.py in your working directory.
3. Make sure to install pySerial - Python serial port access library: pythonhosted.org/pyserial/
4. Run main.py.
5. Select gaits_params.xml or equivalent (explanation below) from your machine.
6. Select the desired gait by clicking the corresponding button. The speed of the gait is adjustable via the slider. 
   For the individual joint control you may also select whether the angles should be referred as relative or absolute. 


XML file format:
In order to define different gaits, you may create your own XML file. The XML file has to follow the same structure as 
the provided gaits_params.xml.
1. For gaits where all joints have the same parameters, define the following node:

	<gait id="NAME_OF_GAIT">
		<joint>
			<freq_robot> VALUE_OF_FREQUENCY </freq_robot>
			<amp_robot> VALUE_OF_AMPLITUDE </amp_robot>
			<phase_o_robot> VALUE_OF_ODD_JOINTS_PHASE </phase_o_robot>
			<phase_e_robot> VALUE_OF_EVEN_JOINTS_PHASE </phase_e_robot>
		</joint>
	</gait>
	
2. For gaits where each joint has different parameters, define the following 20 nodes:

	<gait id="NAME_OF_GAIT">
		<joint id="1">
			<freq_robot> VALUE_OF_FREQUENCY </freq_robot>
			<amp_robot> VALUE_OF_AMPLITUDE </amp_robot>
			<phase_o_robot> VALUE_OF_PHASE </phase_o_robot>
		</joint>
		
		...
		
		<joint id="20">
			<freq_robot> VALUE_OF_FREQUENCY </freq_robot>
			<amp_robot> VALUE_OF_AMPLITUDE </amp_robot>
			<phase_e_robot> VALUE_OF_PHASE </phase_e_robot>
		</joint>
	</gait>
