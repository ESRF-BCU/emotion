#!/usr/bin/env python
# -*- coding:utf-8 -*- 


##############################################################################
## license :
##============================================================================
##
## File :        Motor.py
## 
## Project :     Abstract Stepper Motor
##
## This file is part of Tango device class.
## 
## Tango is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
## 
## Tango is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with Tango.  If not, see <http://www.gnu.org/licenses/>.
## 
##
## $Author :      meyer$
##
## $Revision :    $
##
## $Date :        $
##
## $HeadUrl :     $
##============================================================================
##            This file is generated by POGO
##    (Program Obviously used to Generate tango Object)
##
##        (c) - Software Engineering Group - ESRF
##############################################################################

"""An abstract class for stepper motot"""

__all__ = ["Motor", "MotorClass", "main"]

__docformat__ = 'restructuredtext'

import PyTango
import sys
# Add additional import
#----- PROTECTED REGION ID(Motor.additionnal_import) ENABLED START -----#

#----- PROTECTED REGION END -----#	//	Motor.additionnal_import

## Device States Description
## ON : The motor powered on and is ready to move.
## MOVING : The motor is moving
## FAULT : The motor indicates a fault.
## ALARM : The motor indicates an alarm state for example has reached
##         a limit switch.
## OFF : The power on the moror drive is switched off.
## DISABLE : The motor is in slave mode and disabled for normal use

class Motor (PyTango.Device_4Impl):

    #--------- Add you global variables here --------------------------
    #----- PROTECTED REGION ID(Motor.global_variables) ENABLED START -----#
    
    #----- PROTECTED REGION END -----#	//	Motor.global_variables

    def __init__(self,cl, name):
        PyTango.Device_4Impl.__init__(self,cl,name)
        self.debug_stream("In __init__()")
        Motor.init_device(self)
        #----- PROTECTED REGION ID(Motor.__init__) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Motor.__init__
        
    def delete_device(self):
        self.debug_stream("In delete_device()")
        #----- PROTECTED REGION ID(Motor.delete_device) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Motor.delete_device

    def init_device(self):
        self.debug_stream("In init_device()")
        self.get_device_properties(self.get_device_class())
        self.attr_Steps_per_unit_read = 0.0
        self.attr_Steps_read = 0
        self.attr_Position_read = 0.0
        self.attr_Acceleration_read = 0.0
        self.attr_Velocity_read = 0.0
        self.attr_Backlash_read = 0.0
        self.attr_Home_position_read = 0.0
        self.attr_HardLimitLow_read = False
        self.attr_HardLimitHigh_read = False
        self.attr_PresetPosition_read = 0.0
        self.attr_FirstVelocity_read = 0.0
        self.attr_Home_side_read = False
        self.attr_StepSize_read = 0.0
        #----- PROTECTED REGION ID(Motor.init_device) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Motor.init_device

    def always_executed_hook(self):
        self.debug_stream("In always_excuted_hook()")
        #----- PROTECTED REGION ID(Motor.always_executed_hook) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Motor.always_executed_hook

    #-----------------------------------------------------------------------------
    #    Motor read/write attribute methods
    #-----------------------------------------------------------------------------
    
    def read_Steps_per_unit(self, attr):
        self.debug_stream("In read_Steps_per_unit()")
        #----- PROTECTED REGION ID(Motor.Steps_per_unit_read) ENABLED START -----#
        attr.set_value(self.attr_Steps_per_unit_read)
        
        #----- PROTECTED REGION END -----#	//	Motor.Steps_per_unit_read
        
    def write_Steps_per_unit(self, attr):
        self.debug_stream("In write_Steps_per_unit()")
        data=attr.get_write_value()
        #----- PROTECTED REGION ID(Motor.Steps_per_unit_write) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Motor.Steps_per_unit_write
        
    def read_Steps(self, attr):
        self.debug_stream("In read_Steps()")
        #----- PROTECTED REGION ID(Motor.Steps_read) ENABLED START -----#
        attr.set_value(self.attr_Steps_read)
        
        #----- PROTECTED REGION END -----#	//	Motor.Steps_read
        
    def write_Steps(self, attr):
        self.debug_stream("In write_Steps()")
        data=attr.get_write_value()
        #----- PROTECTED REGION ID(Motor.Steps_write) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Motor.Steps_write
        
    def read_Position(self, attr):
        self.debug_stream("In read_Position()")
        #----- PROTECTED REGION ID(Motor.Position_read) ENABLED START -----#
        attr.set_value(self.attr_Position_read)
        
        #----- PROTECTED REGION END -----#	//	Motor.Position_read
        
    def write_Position(self, attr):
        self.debug_stream("In write_Position()")
        data=attr.get_write_value()
        #----- PROTECTED REGION ID(Motor.Position_write) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Motor.Position_write
        
    def read_Acceleration(self, attr):
        self.debug_stream("In read_Acceleration()")
        #----- PROTECTED REGION ID(Motor.Acceleration_read) ENABLED START -----#
        attr.set_value(self.attr_Acceleration_read)
        
        #----- PROTECTED REGION END -----#	//	Motor.Acceleration_read
        
    def write_Acceleration(self, attr):
        self.debug_stream("In write_Acceleration()")
        data=attr.get_write_value()
        #----- PROTECTED REGION ID(Motor.Acceleration_write) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Motor.Acceleration_write
        
    def read_Velocity(self, attr):
        self.debug_stream("In read_Velocity()")
        #----- PROTECTED REGION ID(Motor.Velocity_read) ENABLED START -----#
        attr.set_value(self.attr_Velocity_read)
        
        #----- PROTECTED REGION END -----#	//	Motor.Velocity_read
        
    def write_Velocity(self, attr):
        self.debug_stream("In write_Velocity()")
        data=attr.get_write_value()
        #----- PROTECTED REGION ID(Motor.Velocity_write) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Motor.Velocity_write
        
    def read_Backlash(self, attr):
        self.debug_stream("In read_Backlash()")
        #----- PROTECTED REGION ID(Motor.Backlash_read) ENABLED START -----#
        attr.set_value(self.attr_Backlash_read)
        
        #----- PROTECTED REGION END -----#	//	Motor.Backlash_read
        
    def write_Backlash(self, attr):
        self.debug_stream("In write_Backlash()")
        data=attr.get_write_value()
        #----- PROTECTED REGION ID(Motor.Backlash_write) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Motor.Backlash_write
        
    def read_Home_position(self, attr):
        self.debug_stream("In read_Home_position()")
        #----- PROTECTED REGION ID(Motor.Home_position_read) ENABLED START -----#
        attr.set_value(self.attr_Home_position_read)
        
        #----- PROTECTED REGION END -----#	//	Motor.Home_position_read
        
    def write_Home_position(self, attr):
        self.debug_stream("In write_Home_position()")
        data=attr.get_write_value()
        #----- PROTECTED REGION ID(Motor.Home_position_write) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Motor.Home_position_write
        
    def read_HardLimitLow(self, attr):
        self.debug_stream("In read_HardLimitLow()")
        #----- PROTECTED REGION ID(Motor.HardLimitLow_read) ENABLED START -----#
        attr.set_value(self.attr_HardLimitLow_read)
        
        #----- PROTECTED REGION END -----#	//	Motor.HardLimitLow_read
        
    def read_HardLimitHigh(self, attr):
        self.debug_stream("In read_HardLimitHigh()")
        #----- PROTECTED REGION ID(Motor.HardLimitHigh_read) ENABLED START -----#
        attr.set_value(self.attr_HardLimitHigh_read)
        
        #----- PROTECTED REGION END -----#	//	Motor.HardLimitHigh_read
        
    def read_PresetPosition(self, attr):
        self.debug_stream("In read_PresetPosition()")
        #----- PROTECTED REGION ID(Motor.PresetPosition_read) ENABLED START -----#
        attr.set_value(self.attr_PresetPosition_read)
        
        #----- PROTECTED REGION END -----#	//	Motor.PresetPosition_read
        
    def write_PresetPosition(self, attr):
        self.debug_stream("In write_PresetPosition()")
        data=attr.get_write_value()
        #----- PROTECTED REGION ID(Motor.PresetPosition_write) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Motor.PresetPosition_write
        
    def read_FirstVelocity(self, attr):
        self.debug_stream("In read_FirstVelocity()")
        #----- PROTECTED REGION ID(Motor.FirstVelocity_read) ENABLED START -----#
        attr.set_value(self.attr_FirstVelocity_read)
        
        #----- PROTECTED REGION END -----#	//	Motor.FirstVelocity_read
        
    def write_FirstVelocity(self, attr):
        self.debug_stream("In write_FirstVelocity()")
        data=attr.get_write_value()
        #----- PROTECTED REGION ID(Motor.FirstVelocity_write) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Motor.FirstVelocity_write
        
    def read_Home_side(self, attr):
        self.debug_stream("In read_Home_side()")
        #----- PROTECTED REGION ID(Motor.Home_side_read) ENABLED START -----#
        attr.set_value(self.attr_Home_side_read)
        
        #----- PROTECTED REGION END -----#	//	Motor.Home_side_read
        
    def read_StepSize(self, attr):
        self.debug_stream("In read_StepSize()")
        #----- PROTECTED REGION ID(Motor.StepSize_read) ENABLED START -----#
        attr.set_value(self.attr_StepSize_read)
        
        #----- PROTECTED REGION END -----#	//	Motor.StepSize_read
        
    def write_StepSize(self, attr):
        self.debug_stream("In write_StepSize()")
        data=attr.get_write_value()
        #----- PROTECTED REGION ID(Motor.StepSize_write) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Motor.StepSize_write
        
    
    
        #----- PROTECTED REGION ID(Motor.initialize_dynamic_attributes) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Motor.initialize_dynamic_attributes
            
    def read_attr_hardware(self, data):
        self.debug_stream("In read_attr_hardware()")
        #----- PROTECTED REGION ID(Motor.read_attr_hardware) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Motor.read_attr_hardware


    #-----------------------------------------------------------------------------
    #    Motor command methods
    #-----------------------------------------------------------------------------
    
    def On(self):
        """ Enable power on motor
        
        :param : 
        :type: PyTango.DevVoid
        :return: 
        :rtype: PyTango.DevVoid """
        self.debug_stream("In On()")
        #----- PROTECTED REGION ID(Motor.On) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Motor.On
        
    def Off(self):
        """ Desable power on motor
        
        :param : 
        :type: PyTango.DevVoid
        :return: 
        :rtype: PyTango.DevVoid """
        self.debug_stream("In Off()")
        #----- PROTECTED REGION ID(Motor.Off) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Motor.Off
        
    def GoHome(self):
        """ Move the motor to the home position given by a home switch.
        
        :param : 
        :type: PyTango.DevVoid
        :return: 
        :rtype: PyTango.DevVoid """
        self.debug_stream("In GoHome()")
        #----- PROTECTED REGION ID(Motor.GoHome) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Motor.GoHome
        
    def Abort(self):
        """ Stop immediately the motor
        
        :param : 
        :type: PyTango.DevVoid
        :return: 
        :rtype: PyTango.DevVoid """
        self.debug_stream("In Abort()")
        #----- PROTECTED REGION ID(Motor.Abort) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Motor.Abort
        
    def StepUp(self):
        """ perform a relative motion of ``stepSize`` in the forward direction.
         StepSize is defined as an attribute of the device.
        
        :param : 
        :type: PyTango.DevVoid
        :return: 
        :rtype: PyTango.DevVoid """
        self.debug_stream("In StepUp()")
        #----- PROTECTED REGION ID(Motor.StepUp) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Motor.StepUp
        
    def StepDown(self):
        """ perform a relative motion of ``stepSize`` in the backward direction.
         StepSize is defined as an attribute of the device.
        
        :param : 
        :type: PyTango.DevVoid
        :return: 
        :rtype: PyTango.DevVoid """
        self.debug_stream("In StepDown()")
        #----- PROTECTED REGION ID(Motor.StepDown) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Motor.StepDown
        

class MotorClass(PyTango.DeviceClass):
    #--------- Add you global class variables here --------------------------
    #----- PROTECTED REGION ID(Motor.global_class_variables) ENABLED START -----#
    
    #----- PROTECTED REGION END -----#	//	Motor.global_class_variables

    def dyn_attr(self, dev_list):
        """Invoked to create dynamic attributes for the given devices.
        Default implementation calls
        :meth:`Motor.initialize_dynamic_attributes` for each device
    
        :param dev_list: list of devices
        :type dev_list: :class:`PyTango.DeviceImpl`"""
    
        for dev in dev_list:
            try:
                dev.initialize_dynamic_attributes()
            except:
                import traceback
                dev.warn_stream("Failed to initialize dynamic attributes")
                dev.debug_stream("Details: " + traceback.format_exc())
        #----- PROTECTED REGION ID(Motor.dyn_attr) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Motor.dyn_attr

    #    Class Properties
    class_property_list = {
        }


    #    Device Properties
    device_property_list = {
        'Calibrated':
            [PyTango.DevBoolean,
            "When this property is different from 0, the motor is considered as calibrated\nand a certain number of attributes cannot be changed anymore.( e.g. step_per_unit)\nThe goal is to avoid undesired change when the calibratiuon process has been\nperformed.",
            [] ],
        }


    #    Command definitions
    cmd_list = {
        'On':
            [[PyTango.DevVoid, "none"],
            [PyTango.DevVoid, "none"]],
        'Off':
            [[PyTango.DevVoid, "none"],
            [PyTango.DevVoid, "none"]],
        'GoHome':
            [[PyTango.DevVoid, "none"],
            [PyTango.DevVoid, "none"]],
        'Abort':
            [[PyTango.DevVoid, "none"],
            [PyTango.DevVoid, "none"]],
        'StepUp':
            [[PyTango.DevVoid, "none"],
            [PyTango.DevVoid, "none"]],
        'StepDown':
            [[PyTango.DevVoid, "none"],
            [PyTango.DevVoid, "none"]],
        }


    #    Attribute definitions
    attr_list = {
        'Steps_per_unit':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label': "Steps per mm",
                'unit': "steps/mm",
                'format': "%7.1f",
                'Display level': PyTango.DispLevel.EXPERT,
                'Memorized':"true"
            } ],
        'Steps':
            [[PyTango.DevLong,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label': "Steps",
                'unit': "steps",
                'format': "%6d",
                'description': "number of steps in the step counter\n",
                'Memorized':"true"
            } ],
        'Position':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label': "position",
                'unit': "mm",
                'format': "%7.3f",
                'description': "The actual motor position.",
            } ],
        'Acceleration':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label': "Acceleration",
                'unit': "units/s^2",
                'format': "%.3f",
                'description': "The acceleration of the motor.",
                'Display level': PyTango.DispLevel.EXPERT,
                'Memorized':"true"
            } ],
        'Velocity':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label': "Velocity",
                'unit': "units/s",
                'format': "%.3f",
                'description': "The constant velocity of the motor.",
                'Display level': PyTango.DispLevel.EXPERT,
                'Memorized':"true"
            } ],
        'Backlash':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label': "Backlash",
                'unit': "mm",
                'format': "%5.3f",
                'description': "Backlash to be applied to each motor movement",
                'Display level': PyTango.DispLevel.EXPERT,
                'Memorized':"true"
            } ],
        'Home_position':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label': "Home position",
                'unit': "mm",
                'format': "%7.3f",
                'description': "Position of the home switch",
                'Display level': PyTango.DispLevel.EXPERT,
                'Memorized':"true"
            } ],
        'HardLimitLow':
            [[PyTango.DevBoolean,
            PyTango.SCALAR,
            PyTango.READ],
            {
                'label': "low limit switch state",
            } ],
        'HardLimitHigh':
            [[PyTango.DevBoolean,
            PyTango.SCALAR,
            PyTango.READ],
            {
                'label': "up limit switch state",
            } ],
        'PresetPosition':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label': "Preset Position",
                'unit': "mm",
                'format': "%.3f",
                'description': "preset the position in the step counter",
                'Display level': PyTango.DispLevel.EXPERT,
            } ],
        'FirstVelocity':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label': "first step velocity",
                'unit': "units/s",
                'format': "%.3f",
                'description': "number of unit/s for the first step and for the move reference",
                'Display level': PyTango.DispLevel.EXPERT,
                'Memorized':"true"
            } ],
        'Home_side':
            [[PyTango.DevBoolean,
            PyTango.SCALAR,
            PyTango.READ],
            {
                'description': "indicates if the axis is below or above the position of the home switch",
            } ],
        'StepSize':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'unit': "mm",
                'format': "%.3f",
                'description': "Size of the relative step performed by the StepUp and StepDown commands.\nThe StepSize is expressed in physical unit.",
                'Display level': PyTango.DispLevel.EXPERT,
                'Memorized':"true"
            } ],
        }


def main():
    try:
        py = PyTango.Util(sys.argv)
        py.add_class(MotorClass,Motor,'Motor')

        U = PyTango.Util.instance()
        U.server_init()
        U.server_run()

    except PyTango.DevFailed,e:
        print '-------> Received a DevFailed exception:',e
    except Exception,e:
        print '-------> An unforeseen exception occured....',e

if __name__ == '__main__':
    main()