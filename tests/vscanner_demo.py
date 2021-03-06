# Simple python program driving VSCANNER through EMotion.
import os
import sys
import time

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")))

import emotion
import emotion.log as elog

elog.level(10)

xml_config = """
<config>
  <controller class="VSCANNER">
    <serial_line value = "/dev/ttyS0" />
    <axis name="px">
      <chan_letter value="X"/>
      <velocity value="0" />
      <steps_per_unit value="1" />
   </axis>
  </controller>
</config>
"""

emotion.load_cfg_fromstring(xml_config)
my_axis = emotion.get_axis("px")

while True:
    for ii in range(10):
        print ii
        time.sleep(0.4)
        my_axis.move(ii)
