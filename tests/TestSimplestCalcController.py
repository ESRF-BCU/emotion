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
  <controller class="mockup">
    <axis name="m0">
      <backlash value="0.1" />
      <velocity value="100" />
    </axis>
  </controller>
  <controller class="simpliest">
    <axis name="m0" tags="real m0" />
    <axis name="m1" tags="m1" />
  </controller>
</config>
"""


class TestSimplest(unittest.TestCase):

    def setUp(self):
        emotion.load_cfg_fromstring(config_xml)

    def testMoveReal(self):
        m1 = emotion.get_axis("m1")
        m0 = emotion.get_axis("m0")
        p1 = m1.position()
        p0 = m0.position()
        m0.rmove(1)
        self.assertEquals(p0 + 1, m0.position())
        self.assertEquals(m1.position(), p1 + 2)
        m0.rmove(-1)
        self.assertEquals(p0, m0.position())
        self.assertEquals(m1.position(), p1)

    def testMovePseudo(self):
        m1 = emotion.get_axis("m1")
        m0 = emotion.get_axis("m0")
        p1 = m1.position()
        p0 = m0.position()
        m1.rmove(2)
        self.assertEquals(p1 + 2, m1.position())
        self.assertEquals(m0.position(), p0 + 1)
        m1.rmove(-2)
        self.assertEquals(p0, m0.position())
        self.assertEquals(m1.position(), p1)

if __name__ == '__main__':
    unittest.main()
