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
from emotion.axis import Axis
#from emotion import log
#log.level(log.DEBUG)

config_xml = """
<config>
  <controller class="mockup">
    <host value="mydummyhost2"/>
    <port value="5000"/>
    <axis name="m0">
      <velocity value="500"/>
      <acceleration value="10"/>
    </axis>
    <axis name="s1f">
      <velocity value="500"/>
      <steps_per_unit value="-1000"/>
      <acceleration value="10"/>
    </axis>
    <axis name="s1b">
      <velocity value="500"/>
      <steps_per_unit value="1000"/>
      <acceleration value="10"/>
    </axis>
    <axis name="s1u">
      <velocity value="500"/>
      <steps_per_unit value="-1000"/>
      <acceleration value="10"/>
    </axis>
    <axis name="s1d">
      <velocity value="500"/>
      <steps_per_unit value="1000"/>
      <acceleration value="10"/>
    </axis>
  </controller>
  <controller class="slits" name="test">
    <axis name="s1f" tags="real front"/>
    <axis name="s1b" tags="real back"/>
    <axis name="s1u" tags="real up"/>
    <axis name="s1d" tags="real down"/>
    <axis name="s1vg" tags="vgap"/>
    <axis name="s1vo" tags="voffset"/>
    <axis name="s1hg" tags="hgap"/>
    <axis name="s1ho" tags="hoffset"/>
  </controller>
</config>
"""


class TestSlits(unittest.TestCase):

    def setUp(self):
        emotion.load_cfg_fromstring(config_xml)
        
    def testTags(self):
        s1ho = emotion.get_axis("s1ho")
        controller = s1ho.controller
        for tag, axis_name in {"front": "s1f",
                               "back": "s1b",
                               "up": "s1u",
                               "down": "s1d",
                               "hgap": "s1hg",
                               "hoffset": "s1ho",
                               "vgap": "s1vg",
                               "voffset": "s1vo"}.iteritems():
            self.assertEquals(controller._tagged[tag][0].name, axis_name)

    def testRealTags(self):
        s1ho = emotion.get_axis("s1ho")
        controller = s1ho.controller
        self.assertEquals(
            [x.name for x in controller._tagged["real"]],
            ["s1f", "s1b", "s1u", "s1d"])

    def testHasTag(self):
        self.assertTrue(emotion.get_axis("s1ho").has_tag("hoffset"))
        self.assertFalse(emotion.get_axis("s1ho").has_tag("vgap"))
        self.assertFalse(emotion.get_axis("s1vg").has_tag("real"))
        self.assertTrue(emotion.get_axis("s1u").has_tag("real"))

    def testRealsList(self):
        s1ho = emotion.get_axis("s1ho")
        controller = s1ho.controller
        self.assertEquals(len(controller.reals), 4)
        self.assertTrue(all([isinstance(x, Axis) for x in controller.reals]))

    def testPseudosList(self):
        s1ho = emotion.get_axis("s1ho")
        controller = s1ho.controller
        self.assertEquals(len(controller.pseudos), 4)
        self.assertTrue(all([isinstance(x, Axis) for x in controller.pseudos]))

    def testPseudoAxisAreExported(self):
        self.assertTrue(all((emotion.get_axis("s1vg"),
                             emotion.get_axis("s1vo"),
                             emotion.get_axis("s1hg"),
                             emotion.get_axis("s1ho"))))

    def testRealAxisIsRightObject(self):
        s1f = emotion.get_axis('s1f')
        m0 = emotion.get_axis('m0')
        s1ho = emotion.get_axis("s1ho")
        controller = s1ho.controller
        self.assertEquals(s1f.controller, m0.controller)
        self.assertEquals(s1f, controller.axes['s1f'])

    def testPseudoAxisState(self):
        self.testPseudoAxisAreExported()
        controller = emotion.config.CONTROLLERS["test"]["object"]
        self.assertTrue(
            all([axis.state() == 'READY' for axis in controller.pseudos]))

    def testPseudoAxisPosition(self):
        self.testPseudoAxisAreExported()
        s1f = emotion.get_axis("s1f")
        s1b = emotion.get_axis("s1b")
        s1u = emotion.get_axis("s1u")
        s1d = emotion.get_axis("s1d")
        s1f.position(0)
        s1b.position(1)
        s1u.position(0)
        s1d.position(1)
        self.assertEquals(emotion.get_axis("s1vg").position(), 1)
        self.assertEquals(emotion.get_axis("s1vo").position(), -0.5)
        self.assertEquals(emotion.get_axis("s1hg").position(), 1)
        self.assertEquals(emotion.get_axis("s1ho").position(), 0.5)

    def testPseudoAxisMove(self):
        s1b  = emotion.get_axis("s1b")
        s1f  = emotion.get_axis("s1f")
        s1hg = emotion.get_axis("s1hg")

        s1f.move(0)
        s1b.move(0)

        hgap = 0.5
        s1hg.move(hgap)
        self.assertAlmostEquals(hgap, s1hg.position(), places=6)

    def testPseudoAxisMove2(self):
        s1ho = emotion.get_axis("s1ho")
        s1b  = emotion.get_axis("s1b")
        s1f  = emotion.get_axis("s1f")
        s1hg = emotion.get_axis("s1hg")

        s1f.move(0)
        s1b.move(0)
        s1hg.move(.5)
        hgap = s1hg.position()
        s1ho.move(2)
        self.assertEquals(s1b.state(), "READY")
        self.assertEquals(s1f.state(), "READY")
        self.assertAlmostEquals(hgap, s1hg.position(), places=4)
        self.assertEquals(s1b.position(), 2 + (hgap / 2.0))
        self.assertEquals(s1f.position(), (hgap / 2.0) - 2)

    def testPseudoAxisScan(self):
        s1ho = emotion.get_axis("s1ho")
        s1b  = emotion.get_axis("s1b")
        s1f  = emotion.get_axis("s1f")
        s1hg = emotion.get_axis("s1hg")

        s1f.move(0)
        s1b.move(0)

        hgap = 0.5
        s1hg.move(hgap)

        # scan the slits under the motors resolution
        ho_step = (1.0/s1b.steps_per_unit) / 10.0
        for i in range(100):
            s1ho.rmove(ho_step)

        self.assertAlmostEquals(hgap, s1hg.position(), places=4)
     
    def testSetPosition(self):
        s1ho = emotion.get_axis("s1ho")
        s1b  = emotion.get_axis("s1b")
        s1f  = emotion.get_axis("s1f")
        s1hg = emotion.get_axis("s1hg")
        s1b.move(0); s1f.move(0);     
        s1hg.move(4)
        self.assertAlmostEquals(2, s1b.position(), places=4)
        self.assertAlmostEquals(2, s1f.position(), places=4)
        self.assertAlmostEquals(0, s1ho.position(), places=4)
        s1hg.position(0)
        s1hg.move(1)
        self.assertAlmostEquals(2.5, s1b.position(), places=4)
        self.assertAlmostEquals(2.5, s1f.position(), places=4)
        self.assertAlmostEquals(1, s1hg.position(), places=4)
        self.assertAlmostEquals(0, s1ho.position(), places=4)




if __name__ == '__main__':
    unittest.main()
