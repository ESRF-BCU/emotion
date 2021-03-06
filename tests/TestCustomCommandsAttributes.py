import unittest
import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..")))

import emotion

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
    <axis name="roby">
      <backlash value="2"/>
      <steps_per_unit value="10"/>
      <velocity  value="2500"/>
    </axis>
  </controller>
</config>
"""

class TestMockupController(unittest.TestCase):

    def setUp(self):
        emotion.load_cfg_fromstring(config_xml)

    def test_get_axis(self):
        robz = emotion.get_axis("robz")
        self.assertTrue(robz)

    def test_get_custom_methods_list(self):
        robz = emotion.get_axis("robz")
        print "\ncustom functions :"
        for (fname, types) in robz.custom_methods_list:
            print fname, types

    def test_custom_park(self):
        robz = emotion.get_axis("robz")
        robz.custom_park()

    def test_custom_get_forty_two(self):
        robz = emotion.get_axis("robz")
        print robz.custom_get_forty_two()

    def test_custom_get_twice(self):
        robz = emotion.get_axis("robz")
        self.assertEqual(robz.custom_get_twice(42), 84)

    def test_custom_get_chapi(self):
        robz = emotion.get_axis("robz")
        self.assertEqual(robz.custom_get_chapi("chapi"), "chapo")
        self.assertEqual(robz.custom_get_chapi("titi"), "toto")
        self.assertEqual(robz.custom_get_chapi("roooh"), "bla")

    def test_custom_send_command(self):
        robz = emotion.get_axis("robz")
        robz.custom_send_command("SALUT sent")


if __name__ == '__main__':
    unittest.main()
