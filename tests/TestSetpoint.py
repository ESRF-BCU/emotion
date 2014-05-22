import unittest
import gevent
import time
import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..")))

import emotion
from emotion.axis import Axis

config_xml = """
<config>
  <controller class="setpoint" name="test">
    <target_attribute value="id16ni/semidyn/cyril/target_sp"/>
    <port value="5000"/>
    <axis name="sp1">
      <!-- degrees per second -->
      <velocity value="100"/>
    </axis>
  </controller>
</config>
"""

# THIS IS FOR TESTING SPECIFIC FEATURES OF AXIS OBJECTS


class SetpointAxis(Axis):

    def __init__(self, *args, **kwargs):
        Axis.__init__(self, *args, **kwargs)

    def _handle_move(self, motion):
        self.target_pos = motion.target_pos
        self.backlash_move = motion.target_pos / self.steps_per_unit() if motion.backlash else 0
        return Axis._handle_move(self, motion)


class setpoint_axis_module:

    def __getattr__(self, attr):
        return MockupAxis

sys.modules["SetpointAxis"] = setpoint_axis_module()
###


class TestSetpointController(unittest.TestCase):

    def setUp(self):
        emotion.load_cfg_fromstring(config_xml)

    def test_get_axis(self):
        sp1 = emotion.get_axis("sp1")
        self.assertTrue(sp1)

if __name__ == '__main__':
    unittest.main()
