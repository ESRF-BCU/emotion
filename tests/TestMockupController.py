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
  <controller class="mockup" name="test">
    <host value="mydummyhost1"/>
    <port value="5000"/>
    <axis name="robz">
      <!-- degrees per second -->
      <velocity value="100"/>
    </axis>
  </controller>
  <controller class="mockup">
    <host value="mydummyhost2"/>
    <port value="5000"/>
    <axis name="roby" class="MockupAxis">
      <backlash value="2"/>
      <steps_per_unit value="10"/>
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
            self.steps_per_unit() if motion.backlash else 0
        return Axis._handle_move(self, motion)


class mockup_axis_module:

    def __getattr__(self, attr):
        return MockupAxis

sys.modules["MockupAxis"] = mockup_axis_module()
###


class TestMockupController(unittest.TestCase):

    def setUp(self):
        emotion.load_cfg_fromstring(config_xml)

    def test_get_axis(self):
        robz = emotion.get_axis("robz")
        self.assertTrue(robz)

    def test_property_setting(self):
        robz = emotion.get_axis("robz")
        self.assertEqual(robz.velocity(), 100)

    def test_controller_from_axis(self):
        robz = emotion.get_axis("robz")
        self.assertEqual(robz.controller.name, "test")

    def test_axis_move(self):
        robz = emotion.get_axis("robz")
        self.assertEqual(robz.state(), "READY")
        move_greenlet = robz.move(180, wait=False)
        self.assertNotEqual(robz.position(), None)
        self.assertEqual(robz.state(), "MOVING")
        move_greenlet.join()
        self.assertEqual(robz.state(), "READY")

    def test_axis_multiple_move(self):
        robz = emotion.get_axis("robz")

        for i in range(250):
            self.assertEqual(robz.state(), "READY")
            move_greenlet = robz.move(180, wait=False)
            self.assertEqual(robz.state(), "MOVING")
            move_greenlet.join()
            self.assertEqual(robz.state(), "READY")
            time.sleep(0.0001)

    def test_axis_init(self):
        robz = emotion.get_axis("robz")
        self.assertEqual(robz.settings.get("init_count"), 1)

    def test_stop(self):
        robz = emotion.get_axis('robz')
        self.assertEqual(robz.state(), "READY")
        robz.move(180, wait=False)
        self.assertEqual(robz.state(), "MOVING")
        robz.stop()
        self.assertEqual(robz.state(), "READY")

    def test_backlash(self):
        roby = emotion.get_axis("roby")
        self.assertEqual(roby.state(), "READY")
        roby.move(0)
        move_greenlet = roby.move(-180, wait=False)
        time.sleep(0)
        self.assertEqual(roby.backlash_move, -182)
        move_greenlet.join()
        self.assertEqual(roby.position(), -180)
        roby.move(-179)
        roby.limits(-181, 180)
        self.assertRaises(ValueError, roby.move, -180)

    def test_backlash2(self):
        roby = emotion.get_axis("roby")
        self.assertEqual(roby.state(), "READY")
        roby.move(0)
        move_greenlet = roby.move(180, wait=False)
        time.sleep(0)
        self.assertEqual(roby.backlash_move, 0)
        move_greenlet.join()
        self.assertEqual(roby.position(), 180)

    def test_axis_steps_per_unit(self):
        roby = emotion.get_axis("roby")
        self.assertEqual(roby.state(), "READY")
        move_greenlet = roby.move(180, wait=False)
        self.assertEqual(roby.state(), "MOVING")
        move_greenlet.join()
        self.assertEqual(roby.state(), "READY")
        self.assertEqual(roby.target_pos, roby.steps_per_unit() * 180)

    def test_axis_set_pos(self):
        roby = emotion.get_axis("roby")
        self.assertEqual(roby.position(0), 0)
        self.assertEqual(roby.position(), 0)
        roby.position(10)
        self.assertEqual(roby.position(), 10)

    def test_axis_set_velocity(self):
        roby = emotion.get_axis("roby")
        org = roby.velocity()
        vel = 5000
        self.assertEqual(roby.velocity(vel), vel)
        roby.velocity(org)

    def test_axis_set_acctime(self):
        roby = emotion.get_axis("roby")
        acc = 0.250
        self.assertEqual(roby.acctime(acc), acc)

    def test_axis_get_measured_position(self):
        roby = emotion.get_axis("roby")
        _meas_pos = -1.2345
        self.assertEqual(roby.measured_position(), _meas_pos)

    def test_axis_custom_method(self):
        roby = emotion.get_axis("roby")
        self.assertEqual(roby.get_identifier(), roby.name)

    def test_axis_config_velocity(self):
        roby = emotion.get_axis("roby")
        self.assertEqual(roby.velocity(), roby.config.get("velocity", int))

    def test_home_search(self):
        roby = emotion.get_axis("roby")
        self.assertEqual(roby.state(), 'READY')
        roby.home(38930, wait=False)
        self.assertEqual(roby.state(), 'MOVING')
        roby.wait_move()
        self.assertEqual(roby.state(), 'READY')
        self.assertEqual(roby.position(), 38930)
        self.assertEqual(roby.offset, -38930)

    def test_ctrlc(self):
        robz = emotion.get_axis("robz")
        final_pos = robz.position() + 100
        move_greenlet = robz.move(final_pos, wait=False)
        self.assertEqual(robz.state(), "MOVING")
        gevent.sleep(0.5)
        move_greenlet.kill(KeyboardInterrupt)
        self.assertEqual(robz.state(), "READY")
        self.assertTrue(robz.position() < final_pos)

    def test_limits(self):
        robz = emotion.get_axis("robz")
        low_limit = robz.position() - 1
        high_limit = robz.position() + 1
        robz.limits(low_limit, high_limit)
        self.assertEquals(robz.limits(), (low_limit, high_limit))
        self.assertRaises(ValueError, robz.move, robz.position() + 1.1)
        self.assertRaises(ValueError, robz.move, robz.position() - 1.1)
        robz.limits(-1E9, 1E9)
        robz.rmove(1)
        robz.rmove(-2)

if __name__ == '__main__':
    unittest.main()
