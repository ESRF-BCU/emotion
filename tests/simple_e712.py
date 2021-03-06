#!/usr/bin/python
# Very simple python program using EMotion.

import os
import sys


os.path.join(os.environ["HOME"], "emotion")

EMOTION_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

sys.path.insert(0, EMOTION_PATH)
sys.path.insert(0, os.path.join(EMOTION_PATH, "tango"))
sys.path.insert(1, "/bliss/users/blissadm/python/bliss_modules")
sys.path.insert(1, "/bliss/users/blissadm/python/bliss_modules/debian6")


sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..")))

import emotion

xml_config = """
<config>
  <controller class="PI_E712">
    <host value="id31pie712a" />
    <port value="50000" />
    
    <axis name="e712">
		<channel value="1" />
		<settings>
	    	<low_limit value="-1000000000.0" />
	    	<high_limit value="1000000000.0" />
	    	<velocity value="2500.0" />
	    	<acctime value="125.0" />
    	    <position value="1.0" />
    	</settings>
	</axis>
  </controller>
</config>

"""

emotion.load_cfg_fromstring(xml_config)

my_axis = emotion.get_axis("e712")

print my_axis.position()
print my_axis.state()
print my_axis.GetInfo()

