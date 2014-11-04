
# Very simple python program using EMotion.

import os
import sys

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..")))

import emotion

xml_config = """
<config>
  <controller class="mockup">
    <axis name="axis0">
    <velocity value="100"/>
    </axis>
  </controller>
</config>
"""

emotion.load_cfg_fromstring(xml_config)
my_axis = emotion.get_axis("axis0")

print my_axis.position()
my_axis.move(42)
print my_axis.position()
