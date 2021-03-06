import time
import serial

from emotion import Controller
from emotion import log as elog
from emotion.controller import add_axis_method
from emotion.axis import AxisState


"""
Emotion controller for XXX.
"""


class XXX(Controller):

    def __init__(self, name, config, axes, encoders):
        Controller.__init__(self, name, config, axes, encoders)

        # self.com = self.config.get("com")

    def initialize(self):
        """
        """
        # opens communication

    def finalize(self):
        """
        """
        # Closes communication

    def initialize_axis(self, axis):
        """
        Reads specific config
        Adds specific methods
        """

    def read_position(self, axis):
        """
        Returns position's setpoint or measured position.

        Args:
            - <axis> : emotion axis.
            - [<measured>] : boolean : if True, function returns
              measured position in ???
        Returns:
            - <position> : float : axis setpoint in ???.
        """
        raise NotImplementedError

    def read_encoder(self, encoder):
        raise NotImplementedError

    def read_velocity(self, axis):
        """
        Args:
            - <axis> : Emotion axis object.
        Returns:
            - <velocity> : float
        """

    def set_velocity(self, axis, new_velocity):
        pass

    def state(self, axis):
        _ans = "whatever"
        if _ans == "moving":
            return AxisState("MOVING")
        else:
            return AxisState("READY")

    def prepare_move(self, motion):
        pass

    def start_one(self, motion):
        """
        """
        _cmd = ""
        self.send(motion.axis, _cmd)

    def stop(self, axis):
        # Halt a scan (not a movement ?)
        self.send(axis, "STOP")

    def raw_write(self, axis, cmd):
        self.serial.write(cmd)

    def raw_write_read(self, axis, cmd):
        self.serial.write(cmd)
        _ans = self.serial.readlines()
        return _ans

    def get_id(self, axis):
        """
        Returns firmware version.
        """
        return self.send(axis, "?VER")

    def get_info(self, axis):
        """
        Returns information about controller.
        """

        _txt = ""

        return _txt

    """
    VSCANNER Com
    """
    def send(self, axis, cmd):
        return _ans

    def send_no_ans(self, axis, cmd):
        pass
