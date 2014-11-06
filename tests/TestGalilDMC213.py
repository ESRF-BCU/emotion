import unittest
import sys
import os
import time

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..")))

import emotion
from emotion.axis import READY,MOVING
import emotion.log
emotion.log.level(emotion.log.DEBUG)

config_xml = """
<config>
  <controller class="GalilDMC213">
    <host value="192.168.0.2"/>
    <axis name="omega">
      <channel value="A"/>
      <steps_per_unit value="-12800"/>
      <velocity value="50"/>
      <acctime value="0.125"/>
    </axis>
  </controller>
</config>
"""


class TestGalilDMC213(unittest.TestCase):

    def setUp(self):
        emotion.load_cfg_fromstring(config_xml)
   
    def testCommunication(self):
        o = emotion.get_axis("omega")
        self.assertEquals(o.controller._galil_query("MG 1+3"), "4.0000")
        self.assertRaises(RuntimeError, o.controller._galil_query, "BLA")
        self.assertTrue(o.controller._galil_query(chr(18)+chr(22)).startswith("DMC2112"))
  
    def testVelocity(self):
        o = emotion.get_axis("omega")
        self.assertEquals(o.velocity(), 50) 
        self.assertEquals(o.acceleration(), 50/0.125)
        t0 = time.time()
        o.rmove(100)
        dt = time.time()-t0
        self.assertTrue(dt < 2.4)
        o.velocity(100)
        self.assertEquals(o.acceleration(), 100/0.125)
        self.assertEquals(o.acctime(), 0.125)
        t0 = time.time()
        o.rmove(-100)
        dt = time.time() - t0
        self.assertTrue(dt < 1.4)
          

    """
    def testHomeSearch(self):
        o = emotion.get_axis("omega")
        o.home()
    
    def testPosition(self):
        o = emotion.get_axis("omega")
        p = o.position()
        o.rmove(10)
        self.assertAlmostEquals(o.position(), p+10, places=3)
    """
 
if __name__ == '__main__':
    unittest.main()
