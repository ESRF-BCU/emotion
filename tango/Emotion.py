#!/usr/bin/env python
# -*- coding:utf-8 -*-
import emotion
import emotion.axis
import emotion.config
import PyTango
import traceback
import TgGevent
import sys

class Emotion(PyTango.Device_4Impl):
    def __init__(self, cl, name):
        PyTango.Device_4Impl.__init__(self,cl,name)
        self.debug_stream("In __init__()")
        self.init_device()

    def delete_device(self):
        self.debug_stream("In delete_device()")
        # must call finalize of controller ?

    def init_device(self):
        self.debug_stream("In init_device()")
        self.get_device_properties(self.get_device_class())

        try:
            emotion.load_cfg(self.config_file)
        except:
            self.set_state(PyTango.DevState.FAULT)
            self.set_status(traceback.format_exc())


class EmotionClass(PyTango.DeviceClass):
    #    Class Properties
    class_property_list = {
        }

    #    Device Properties
    device_property_list = {
        'config_file':
            [PyTango.DevString,
            "Path to the configuration file",
            [] ],
        }


## Device States Description
## ON : The motor powered on and is ready to move.
## MOVING : The motor is moving
## FAULT : The motor indicates a fault.
## ALARM : The motor indicates an alarm state for example has reached
##         a limit switch.
## OFF : The power on the moror drive is switched off.
## DISABLE : The motor is in slave mode and disabled for normal use
class EmotionAxis(PyTango.Device_4Impl):
    def __init__(self,cl, name):
        PyTango.Device_4Impl.__init__(self,cl,name)

        self._axis_name = name.split('/')[-1]

        self.debug_stream("In __init__()")
        self.init_device()

    def delete_device(self):
        self.debug_stream("In delete_device()")

    def init_device(self):
        self.debug_stream("In init_device()")
        self.get_device_properties(self.get_device_class())

        try:
            self.axis = TgGevent.get_proxy(emotion.get_axis, self._axis_name)
        except:
            self.set_status(traceback.format_exc())

        self.once = False

        """
        self.attr_Steps_per_unit_read = 0.0
        self.attr_Steps_read = 0
        self.attr_Position_read = 0.0
        self.attr_Measured_Position_read = 0.0
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
        """


    def always_executed_hook(self):
        self.debug_stream("In always_excuted_hook()")


        # here instead of in init_device due to (Py?)Tango bug :
        # device does not really exist in init_device... (Cyril)
        if not self.once:
            try:
                # Initialises "set" value of attributes.
                attr = self.get_device_attr().get_attr_by_name("Position")
                attr.set_write_value(self.axis.position())

                attr = self.get_device_attr().get_attr_by_name("Velocity")
                attr.set_write_value(float(self.axis.velocity()))

                try:
                    _acc = self.axis.acceleration()
                    attr = self.get_device_attr().get_attr_by_name("Acceleration")
                    attr.set_write_value(float(_acc))
                except:
                    print "No acceleration for axis %s"%self._axis_name

            except:
                print "ERROR : Cannot set one of attributs write value."
                print traceback.format_exc()

            finally:
                self.once = True

    def dev_state(self):
        """ This command gets the device state (stored in its device_state
        data member) and returns it to the caller.

        :param : none
        :type: PyTango.DevVoid
        :return: Device state
        :rtype: PyTango.CmdArgType.DevState """
        self.debug_stream("In dev_state()")
        argout = PyTango.DevState.UNKNOWN
        #----- PROTECTED REGION ID(TOTO.State) ENABLED START -----#

        try:
          if self.axis.state() == emotion.axis.READY:
            self.set_state(PyTango.DevState.ON)
          elif self.axis.state() == emotion.axis.MOVING:
            self.set_state(PyTango.DevState.MOVING)
          else:
            self.set_state(PyTango.DevState.FAULT)
        except:
          self.set_state(PyTango.DevState.FAULT)

        #----- PROTECTED REGION END -----#      //      TOTO.State
        if argout != PyTango.DevState.ALARM:
            PyTango.Device_4Impl.dev_state(self)
        return self.get_state()


    def read_Steps_per_unit(self, attr):
        self.debug_stream("In read_Steps_per_unit()")
        attr.set_value(self.attr_Steps_per_unit_read)

    def write_Steps_per_unit(self, attr):
        self.debug_stream("In write_Steps_per_unit()")
        data=attr.get_write_value()


    def read_Steps(self, attr):
        self.debug_stream("In read_Steps()")
        attr.set_value(self.attr_Steps_read)

    def write_Steps(self, attr):
        self.debug_stream("In write_Steps()")
        data=attr.get_write_value()


    def read_Position(self, attr):
        try:
            self.debug_stream("In read_Position()")
            attr.set_value(self.axis.position())
        except:
            traceback.print_exc()
            raise

    def write_Position(self, attr):
        try:
            self.debug_stream("In write_Position()")
            self.axis.move(attr.get_write_value(), wait=False)
        except:
            traceback.print_exc()
            raise


    def read_Measured_Position(self, attr):
        self.debug_stream("In read_Measured_Position()")
        attr.set_value(self.attr_Measured_Position_read)


    def read_Acceleration(self, attr):
        print "want to read Acceleration"
        try:
            _acc = self.axis.acceleration()
            self.debug_stream("In read_Acceleration(%f)"%float(_acc))
            attr.set_value(_acc)
        except:
            print "unable to read Acceleration"
            traceback.print_exc()
            raise

    def write_Acceleration(self, attr):
        print "want to write Acceleration"
        try:
            data=float(attr.get_write_value())
            self.debug_stream("In write_Acceleration(%f)"%data)
            self.axis.acceleration(data)
        except:
            print "unable to write Acceleration"
            traceback.print_exc()
            raise


    def read_AccTime(self, attr):
        self.debug_stream("In read_AccTime()")
        attr.set_value(self.attr_AccTime_read)

    def write_AccTime(self, attr):
        data=attr.get_write_value()
        self.debug_stream("In write_AccTime(%f)"%float(data))



    def read_Velocity(self, attr):
        try:
            _vel = self.axis.velocity()
            attr.set_value(_vel)
            self.debug_stream("In read_Velocity(%g)"%_vel)
        except:
            traceback.print_exc()
            raise

    def write_Velocity(self, attr):
        try:
            data=float(attr.get_write_value())
            self.debug_stream("In write_Velocity(%g)"%data)
            self.axis.velocity(data)
        except:
            traceback.print_exc()
            raise


    def read_Backlash(self, attr):
        self.debug_stream("In read_Backlash()")
        attr.set_value(self.attr_Backlash_read)

    def write_Backlash(self, attr):
        self.debug_stream("In write_Backlash()")
        data=attr.get_write_value()


    def read_Home_position(self, attr):
        self.debug_stream("In read_Home_position()")
        attr.set_value(self.attr_Home_position_read)

    def write_Home_position(self, attr):
        self.debug_stream("In write_Home_position()")
        data=attr.get_write_value()


    def read_HardLimitLow(self, attr):
        self.debug_stream("In read_HardLimitLow()")
        attr.set_value(self.attr_HardLimitLow_read)

    def read_HardLimitHigh(self, attr):
        self.debug_stream("In read_HardLimitHigh()")
        attr.set_value(self.attr_HardLimitHigh_read)


    def read_PresetPosition(self, attr):
        self.debug_stream("In read_PresetPosition()")
        attr.set_value(self.attr_PresetPosition_read)

    def write_PresetPosition(self, attr):
        self.debug_stream("In write_PresetPosition()")
        data=attr.get_write_value()


    def read_FirstVelocity(self, attr):
        self.debug_stream("In read_FirstVelocity()")
        attr.set_value(self.attr_FirstVelocity_read)

    def write_FirstVelocity(self, attr):
        self.debug_stream("In write_FirstVelocity()")
        data=attr.get_write_value()


    def read_Home_side(self, attr):
        self.debug_stream("In read_Home_side()")
        attr.set_value(self.attr_Home_side_read)


    def read_StepSize(self, attr):
        self.debug_stream("In read_StepSize()")
        attr.set_value(self.attr_StepSize_read)

    def write_StepSize(self, attr):
        self.debug_stream("In write_StepSize()")
        data=attr.get_write_value()


    def read_attr_hardware(self, data):
        self.debug_stream("In read_attr_hardware()")


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

    def Off(self):
        """ Desable power on motor

        :param :
        :type: PyTango.DevVoid
        :return:
        :rtype: PyTango.DevVoid """
        self.debug_stream("In Off()")

    def GoHome(self):
        """ Move the motor to the home position given by a home switch.

        :param :
        :type: PyTango.DevVoid
        :return:
        :rtype: PyTango.DevVoid """
        self.debug_stream("In GoHome()")

    def Abort(self):
        """ Stop immediately the motor

        :param :
        :type: PyTango.DevVoid
        :return:
        :rtype: PyTango.DevVoid """
        self.debug_stream("In Abort()")
        self.axis.stop()

    def StepUp(self):
        """ perform a relative motion of ``stepSize`` in the forward direction.
         StepSize is defined as an attribute of the device.

        :param :
        :type: PyTango.DevVoid
        :return:
        :rtype: PyTango.DevVoid """
        self.debug_stream("In StepUp()")

    def StepDown(self):
        """ perform a relative motion of ``stepSize`` in the backward direction.
         StepSize is defined as an attribute of the device.

        :param :
        :type: PyTango.DevVoid
        :return:
        :rtype: PyTango.DevVoid """
        self.debug_stream("In StepDown()")


class EmotionAxisClass(PyTango.DeviceClass):
    #    Class Properties
    class_property_list = {
        }

    #    Device Properties
    device_property_list = {
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
                'description': "The desired motor position.",
            } ],
        'Measured_Position':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ],
            {
                'label': "position",
                'unit': "mm",
                'format': "%7.3f",
                'description': "The measured motor position.",
            } ],
        'Acceleration':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label': "Acceleration",
                'unit': "units/s^2",
                'format': "%10.3f",
                'description': "The acceleration of the motor.",
                'Display level': PyTango.DispLevel.EXPERT,
                'Memorized':"true"
            } ],
        'AccTime':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label': "Acceleration Time",
                'unit': "s",
                'format': "%10.6f",
                'description': "The acceleration time of the motor.",
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
                'format': "%10.3f",
                'description': "The constant velocity of the motor.",
#                'Display level': PyTango.DispLevel.EXPERT,
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
                'format': "%10.3f",
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
                'format': "%10.3f",
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
                'format': "%10.3f",
                'description': "Size of the relative step performed by the StepUp and StepDown commands.\nThe StepSize is expressed in physical unit.",
                'Display level': PyTango.DispLevel.EXPERT,
                'Memorized':"true"
            } ],
        }



def get_devices_from_server():

    #get sub devices
    fullpathExecName = sys.argv[0]
    execName = os.path.split(fullpathExecName)[-1]
    execName = os.path.splitext(execName)[0]
    personalName = '/'.join([execName,sys.argv[1]])
    db =  PyTango.Database()
    result = db.get_device_class_list(personalName)

    #"result" is :  DbDatum[
    #    name = 'server'
    # value_string = ['dserver/Emotion/cyril', 'DServer', 'pel/emotion/00', 'Emotion', 'pel/emotion_00/fd', 'EmotionAxis']]
    #print "--------------------"
    #print result
    #print "++++++++++++++++++++"
    class_dict = {}

    for i in range(len(result.value_string) / 2) :
        deviceName = result.value_string[i * 2]
        class_name = result.value_string[i * 2 + 1]
        if class_name not in class_dict:
            class_dict[class_name] = []

        class_dict[class_name].append(deviceName)

    return class_dict



"""
Removes Emotion axis devices from the database.
"""
def delete_emotion_axes():
    db = PyTango.Database()

    emotion_axis_device_names = get_devices_from_server().get('EmotionAxis')
    # print emotion_axis_device_names

    for _axis_device_name in get_devices_from_server()["EmotionAxis"]:
        print "deleting existing emotion axis :", _axis_device_name
        db.delete_device(_axis_device_name)

def main():
    try:
        delete_emotion_axes()
    except:
        print "can not delete emotion axes."

    try:
        py = PyTango.Util(sys.argv)

        py.add_class(EmotionClass, Emotion, 'Emotion')
        py.add_TgClass(EmotionAxisClass, EmotionAxis, 'EmotionAxis')

        U = PyTango.Util.instance()
        U.server_init()

        emotion_admin_device_names = get_devices_from_server().get('Emotion')
        # print emotion_admin_device_names

        if emotion_admin_device_names:
          blname, server_name, device_number = emotion_admin_device_names[0].split('/')
          # print "blname, server_name, device_number=", blname, server_name, device_number

          for axis_name in emotion.config.axis_names_list():
            device_name = '/'.join((blname,
                                    '%s_%s' % (server_name, device_number),
                                    axis_name))

            print "creating %s"%device_name
            U.create_device('EmotionAxis', device_name)
        else:
          print "No emotion supervisor ???"

        U.server_run()


    except PyTango.DevFailed,e:
        print '-------> Received a DevFailed exception:',e
    except Exception,e:
        print '-------> An unforeseen exception occured....',e

if __name__ == '__main__':
    main()
