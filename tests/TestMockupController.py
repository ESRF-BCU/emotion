import unittest
import time
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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
      <velocity value="500"/>
      <backlash value="2"/>
      <step_size value="10"/>
      <velocity  value="2500"/>
    </axis>
  </controller>
  <group name="group1">
    <axis name="robz"/>
    <axis name="roby"/>
  </group>
</config>
"""

### THIS IS FOR TESTING SPECIFIC FEATURES OF AXIS OBJECTS
class MockupAxis(Axis):
  def __init__(self, *args, **kwargs):
    Axis.__init__(self, *args, **kwargs)

  def _handle_move(self, target_pos, delta, backlash=0):
    self.target_pos = target_pos
    self.backlash_move = target_pos/self.step_size() if backlash else 0
    return Axis._handle_move(self, target_pos, delta, backlash)

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

    def test_group_creation(self):
        grp = emotion.get_group("group1")
        self.assertTrue(grp)

    def test_axis_move(self):
        robz = emotion.get_axis("robz")
        self.assertEqual(robz.state(), "READY")
        move_greenlet=robz.move(180, wait=False)
        self.assertEqual(robz.state(), "MOVING")
        move_greenlet.join()
        self.assertEqual(robz.state(), "READY")

    def test_axis_init(self):
        robz = emotion.get_axis("robz")
        self.assertEqual(robz.settings.get("init_count"), 1)

    def test_stop(self):
        robz = emotion.get_axis('robz')
        self.assertEqual(robz.state(), "READY")
        move_greenlet=robz.move(180, wait=False)
        self.assertEqual(robz.state(), "MOVING")
        robz.stop()
        self.assertEqual(robz.state(), "READY")

    def test_backlash(self):
        roby = emotion.get_axis("roby")
        self.assertEqual(roby.state(), "READY")
        roby.move(0)
        move_greenlet=roby.move(-180, wait=False)
        time.sleep(0)
        self.assertEqual(roby.backlash_move, -182)
        move_greenlet.join()
        self.assertEqual(roby.position(), -180)
       
    def test_backlash2(self):
        roby = emotion.get_axis("roby")
        self.assertEqual(roby.state(), "READY")
        roby.move(0)
        move_greenlet=roby.move(180, wait=False)
        time.sleep(0)
        self.assertEqual(roby.backlash_move, 0)
        move_greenlet.join()
        self.assertEqual(roby.position(), 180)

    def test_axis_stepsize(self):
        roby = emotion.get_axis("roby")
        self.assertEqual(roby.state(), "READY")
        move_greenlet=roby.move(180, wait=False)
        self.assertEqual(roby.state(), "MOVING")
        move_greenlet.join()
        self.assertEqual(roby.state(), "READY")
        self.assertEqual(roby.target_pos, roby.step_size()*180)

    def test_axis_set_pos(self):
        roby = emotion.get_axis("roby")
        roby.position(0)
        self.assertEqual(roby.position(), 0)
        roby.position(10)
        self.assertEqual(roby.position(), 10)

    def test_axis_set_velocity(self):
        roby = emotion.get_axis("roby")
        org  = roby.velocity()
        vel  = 5000
        self.assertEqual(roby.velocity(vel), vel)
        roby.velocity(org)

    def test_axis_set_acctime(self):
        roby = emotion.get_axis("roby")
        acc   = 0.250
        self.assertEqual(roby.acctime(acc), acc)

    def test_axis_custom_method(self):
        roby = emotion.get_axis("roby")
        self.assertEqual(roby.get_identifier(), roby.name)

    def test_axis_config_velocity(self):
        roby = emotion.get_axis("roby")
        self.assertEqual(roby.velocity(), roby.config.get("velocity", int))

if __name__ == '__main__':
    unittest.main()
