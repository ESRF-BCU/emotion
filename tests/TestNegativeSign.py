import unittest
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
  <controller class="mockup">
    <host value="mydummyhost2"/>
    <port value="5000"/>
    <axis name="roby" class="MockupAxis">
      <backlash value="2"/>
      <steps_per_unit value="10"/>
      <sign value="-1"/>
      <velocity  value="2500"/>
    </axis>
  </controller>
</config>
"""

# THIS IS FOR TESTING SPECIFIC FEATURES OF AXIS OBJECTS


class MockupAxis(Axis):

    def __init__(self, *args, **kwargs):
        Axis.__init__(self, *args, **kwargs)

    def _handle_move(self, motion):
        self.target_pos = motion.target_pos
        self.backlash_move = motion.target_pos / \
            self.steps_per_unit if motion.backlash else 0
        return Axis._handle_move(self, motion)


class mockup_axis_module:

    def __getattr__(self, attr):
        return MockupAxis

sys.modules["MockupAxis"] = mockup_axis_module()
###


class TestMockupController(unittest.TestCase):

    def setUp(self):
        emotion.load_cfg_fromstring(config_xml)
    
    def test_backlash(self):
        roby = emotion.get_axis("roby")
        self.assertEqual(roby.state(), "READY")
        roby.move(0)
        move_greenlet = roby.move(-10, wait=False)
        time.sleep(0)
        self.assertEqual(roby.backlash_move, 0)
        move_greenlet.join()
        self.assertEqual(roby.position(), -10)
        roby.limits(-10, 9)
        self.assertRaises(ValueError, roby.move, 8)

    def test_backlash2(self):
        roby = emotion.get_axis("roby")
        self.assertEqual(roby.state(), "READY")
        roby.move(0)
        move_greenlet = roby.move(10, wait=False)
        time.sleep(0)
        self.assertEqual(roby.backlash_move, -12)
        move_greenlet.join()
        self.assertEqual(roby.position(), 10)

    def test_axis_steps_per_unit(self):
        roby = emotion.get_axis("roby")
        self.assertEqual(roby.state(), "READY")
        move_greenlet = roby.move(180, wait=False)
        self.assertEqual(roby.state(), "MOVING")
        move_greenlet.join()
        self.assertEqual(roby.state(), "READY")
        self.assertEqual(roby.target_pos, roby.sign * roby.steps_per_unit * 180)

    def test_axis_set_pos(self):
        roby = emotion.get_axis("roby")
        self.assertEqual(roby.position(0), 0)
        self.assertEqual(roby.position(), 0)
        roby.position(10)
        self.assertEqual(roby.position(), 10)

    def test_home_search(self):
        roby = emotion.get_axis("roby")
        self.assertEqual(roby.state(), 'READY')
        roby.home(38930, wait=False)
        self.assertEqual(roby.state(), 'MOVING')
        roby.wait_move()
        self.assertEqual(roby.state(), 'READY')
        self.assertEqual(roby.position(), 38930)
        self.assertEqual(roby.offset, 38930)

    def test_limits(self):
        roby = emotion.get_axis("roby")
        low_limit = roby.position() - 1
        high_limit = roby.position() + 1
        roby.limits(low_limit, high_limit)
        self.assertEquals(roby.limits(), (low_limit, high_limit))
        self.assertRaises(ValueError, roby.move, roby.position() + 1.1)
        self.assertRaises(ValueError, roby.move, roby.position() - 1.1)
        roby.limits(-1E9, 1E9)
        roby.rmove(1)
        roby.rmove(-2)
    
    def test_rmove(self):
        roby = emotion.get_axis("roby")
        roby.position(-1)
        self.assertEquals(roby.sign, -1)
        roby.rmove(2)
        self.assertEquals(roby.position(), 1)
        roby.rmove(-2)
        self.assertEquals(roby.position(), -1)
        roby.position(1)
        roby.rmove(2)
        self.assertEquals(roby.position(), 3)
        roby.rmove(-2)
        self.assertEquals(roby.position(), 1)


if __name__ == '__main__':
    unittest.main()