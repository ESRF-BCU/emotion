import time
import serial

from emotion import Controller
from emotion import log as elog
from emotion.controller import add_axis_method
from emotion.axis import AxisState


"""
Emotion controller for ESRF ISG VSCANNER voltage scanner unit.
Cyril Guilloud ESRF BLISS
Mon 17 Nov 2014 16:53:47
"""


class VSCANNER(Controller):

    def __init__(self, name, config, axes, encoders):
        Controller.__init__(self, name, config, axes, encoders)

        self.serial_line = self.config.get("serial_line")

    def initialize(self):
        """
        Opens a single socket for all 2
        """
        self.serial = serial.Serial(self.serial_line, 9600, bytesize=8, parity='N', stopbits=1, timeout=1)

        self._status = ""
        try:
            self.serial.write("?VER\r\n")
            _ans = self.serial.readline()
            # _ans =='VSCANNER 01.02\r\n'
            elog.debug(_ans)
            if _ans.index("VSCANNER") == 0:
                elog.debug("?VER -> %s" % _ans.rstrip())
        except:
            self._status = "communication error : no VSCANNER found on serial \"%s\"" % self.serial_line
            elog.debug(self._status)

    def finalize(self):
        """
        Closes the serial object.
        """
        self.serial.close()

    def initialize_axis(self, axis):
        """
        - Reads specific config
        - Adds specific methods
        """
        # can be "X" or "Y"
        axis.chan_letter = axis.config.get("chan_letter")

        add_axis_method(axis, self.get_id, types_info=(None, str))

        axis.config.config_dict.update({"steps_per_unit": {"value": axis.config.get("steps_per_unit")}})

        ini_pos = self.read_position(axis)
        if ini_pos < 0:
            elog.info("reseting VSCANNER negative position to 0 !!")
            _cmd = "V%s 0" % (axis.chan_letter)
            self.send_no_ans(axis, _cmd)

        if ini_pos > 10:
            elog.info("reseting VSCANNER >10-position to 10 !!")
            _cmd = "V%s 10" % (axis.chan_letter)
            self.send_no_ans(axis, _cmd)

        # ???
        # self.send(axis, "NOECHO")

    def read_position(self, axis):
        """
        * Returns position's setpoint in controller units (Volts)
        * Setpoint position (in Volts) command is ?VX or ?VY

        Args:
            - <axis> : emotion axis.
            - [<measured>] : boolean : if True, function must
              return measured position.
        Returns:
            - <position> : float : axis setpoint in Volts.
        """
        _cmd = "?V%s\r\n" % axis.chan_letter
        _ans = self.send(axis, _cmd)
        # elog.debug("_ans =%s" % _ans)
        _pos = float(_ans)
        elog.debug("position=%f" % _pos)

        return _pos

    def read_velocity(self, axis):
        """
        Args:
            - <axis> : Emotion axis object.
        Returns:
            - <velocity> : float
        """
        _ans = self.send(axis, "?VEL")
        # _ans should looks like '0.2 0.1' (yes with single quotes arround...)
        # First field is velocity (in V/ms)
        # Second field is "line waiting" (hummmm second field is not always present ???)
        _ans = _ans[1:][:-1]

        # (_vel, _line_waiting) = map(float, _ans.split())
        _float_ans = map(float, _ans.split())
        if len(_float_ans) == 1:
            _vel = _float_ans[0]
        elif len(_float_ans) == 2:
            (_vel, _line_waiting) = _float_ans
        else:
            print "WHAT THE F.... ?VEL answer is there ???"

        #     V/s = V/ms * 1000
        _velocity = _vel * 1000

        elog.debug("read_velocity : %g " % _velocity)
        return _velocity

    def set_velocity(self, axis, new_velocity):

        _new_vel = new_velocity / 1000.0

        # "VEL <vel>" command sets velocity in V/ms
        self.send_no_ans(axis, "VEL %f 0" % _new_vel)
        elog.debug("velocity set : %g" % _new_vel)

    def state(self, axis):
        _ans = self.send(axis, "?STATE")
        if _ans == "READY":
            return AxisState("READY")
        elif _ans == "LWAITING":
            return AxisState("MOVING")
        elif _ans == "LRUNNING":
            return AxisState("MOVING")
        elif _ans == "PWAITING":
            return AxisState("MOVING")
        elif _ans == "PRUNNING":
            return AxisState("MOVING")
        else:
            return AxisState("FAULT")

    def prepare_move(self, motion):
        _velocity = float(motion.axis.config.get("velocity"))
        if _velocity == 0:
            elog.debug("immediate move")
        else:
            elog.debug("scan move")

            if motion.axis.chan_letter == "X":
                scan_val1 = motion.delta
                scan_val2 = 0
            elif motion.axis.chan_letter == "Y":
                scan_val1 = 0
                scan_val2 = motion.delta
            else:
                print "ERRORR"

            number_of_pixel = 1
            line_mode = "C"  # mode continuous (S for stepping)
            _cmd = "LINE %g %g %d %s" % (scan_val1, scan_val2, number_of_pixel, line_mode)
            elog.debug("_cmd_LINE=%s" % _cmd)
            self.send_no_ans(motion.axis, _cmd)

            _cmd = "SCAN 0 0 1 U"
            elog.debug("_cmd_SCAN=%s" % _cmd)
            self.send_no_ans(motion.axis, _cmd)

            _cmd = "PSHAPE ALL"
            elog.debug("_cmd_PSHAPE=%s" % _cmd)
            self.send_no_ans(motion.axis, _cmd)

    def start_one(self, motion):
        """
        - Sends 'V<chan>  <voltage>' command
        Args:
            - <motion> : Emotion motion object.
        Returns:
            - None
        """
        _velocity = float(motion.axis.config.get("velocity"))
        if _velocity == 0:
            elog.debug("immediate move")
            _cmd = "V%s %s" % (motion.axis.chan_letter, motion.target_pos)
            self.send_no_ans(motion.axis, _cmd)
        else:
            elog.debug("SCAN move")
            _cmd = "START 1 NORET"
            elog.debug("_cmd_START=%s" % _cmd)
            self.send_no_ans(motion.axis, _cmd)

    def start_all(self, *motion_list):
        """
        Called once per controller with all the axis to move
        returns immediately,
        positions in motor units
        """
        elog.debug("start_all() called")

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

    def get_error(self, axis):
        _ans = self.send(axis, "?ERR")
        # no error -> VSCANNER returns "OK"

        return _ans

    def get_info(self, axis):
        """
        Returns a set of usefull information about controller.
        Helpful to tune the device.
        """

        _txt = ""
        _txt = _txt + "###############################\n"
        _txt = _txt + "firmware version   : " + self.send(axis, "?VER") + "\n"
        _txt = _txt + "output voltage     : " + self.send(axis, "?VXY") + "\n"
        _txt = _txt + "unit state         : " + self.send(axis, "?STATE") + "\n"
        _txt = _txt + "###############################\n"
        self.send_no_ans(axis, "?INFO")
        _txt = _txt + "    %s  \n%s\n" % ("Communication parameters",
                                          " ".join(self.serial.readlines()))

        _txt = _txt + "###############################\n"

        return _txt

    """
    VSCANNER Com
    """
    def send(self, axis, cmd):
        """
        - Adds the 'newline' terminator character : "\\\\r\\\\n"
        - Sends command <cmd> to the VSCANNER.
        - Channel is defined in <cmd>.
        - <axis> is passed for debugging purposes.
        - Returns answer from controller.

        Args:
            - <axis> : passed for debugging purposes.
            - <cmd> : command to send to controller (Channel is already mentionned  in <cmd>).

        Returns:
            - 1-line answer received from the controller (without "\\\\n" terminator).

        Raises:
            ?
        """
        elog.debug("cmd=%s" % repr(cmd))
        _cmd = cmd + "\r\n"
        self.serial.write(_cmd)
        _ans = self.serial.readline().rstrip()
        elog.debug("ans=%s" % repr(_ans))
        return _ans

    def send_no_ans(self, axis, cmd):
        """
        - Adds the 'newline' terminator character : "\\\\r\\\\n"
        - Sends command <cmd> to the VSCANNER.
        - Channel is defined in <cmd>.
        - <axis> is passed for debugging purposes.
        - Used for answer-less commands, then returns nothing.
        """
        elog.debug("cmd=\"%s\" " % cmd)
        _cmd = cmd + "\r\n"
        self.serial.write(_cmd)
