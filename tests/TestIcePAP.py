import unittest
import sys
import os
import optparse




"""
Emotion generic library
"""
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import emotion




"""
IcePAP specific library
"""
sys.path.insert(0, os.path.abspath("/segfs/bliss/source/hardware/IcePAP/client/python/"))
import icepap.lib




"""
Example of Emotion configuration
"""
config_xml = """
<config>
  <controller class="IcePAP" name="test">
    <host value="%s"/>
    <libdebug value="3"/>
    <axis name="mymot">
      <address   value="%s"/>
      <step_size value="2000"/>
      <backlash  value="0.01"/>
    </axis>
  </controller>
</config>
"""



"""
Global resources, yes, I know it's bad
"""
hostname = ""
address  = ""



"""
UnitTest list of tests
"""
class TestIcePAPController(unittest.TestCase):
  global hostname
  global address

  # called for each test
  def setUp(self):
    emotion.load_cfg_fromstring(config_xml%(hostname, address))

  def test_get_axis(self):
    mymot = emotion.get_axis("mymot")
    self.assertTrue(mymot)

  def test_get_position(self):
    mymot = emotion.get_axis("mymot")
    pos   = mymot.position()

  """
  def test_get_id(self):
    mymot = emotion.get_axis("mymot")
    print "\"mymot\" ID:", mymot.controller._get_identifier()
  """

  def test_axis_state(self):
    mymot = emotion.get_axis("mymot")
    mymot.state()

  def test_axis_stop(self):
    mymot = emotion.get_axis("mymot")
    mymot.stop()

  def test_axis_move(self):
    mymot = emotion.get_axis("mymot")
    pos   = mymot.position()
    mymot.controller._set_lib_verbose_level(3)
    mymot.move(pos+0.1)

  def test_axis_move_backlash(self):
    mymot = emotion.get_axis("mymot")
    pos   = mymot.position()
    mymot.move(pos-0.1)

  def test_axis_rmove(self):
    mymot = emotion.get_axis("mymot")
    mymot.rmove(0.1)


"""
Main entry point
"""
if __name__ == '__main__':

  # Get arguments
  usage  = "Usage: %prog [options] hostname motor_address"
  parser = optparse.OptionParser(usage)
  argv   = sys.argv
  (settings, args) = parser.parse_args(argv)

  # Minimum check on arguements
  if len(args) <= 2:
    parser.error("Missing mandatory IcePAP hostname and motor address")
    sys.exit(-1)

  # Mandatory argument is the IcePAP hostname
  hostname = args[1]
  address  = args[2]

  # Avoid interaction of our arguments with unittest class
  del sys.argv[1:]

  # Launch the tests sequence
  print "\nTesting IcePAP control on system \"%s\"\n"%hostname
  print "\n".rjust(70,"-")

  # Change the default unittest test sequence order from cmp() to line number
  loader = unittest.TestLoader()
  ln = lambda f: getattr(TestIcePAPController, f).\
		         im_func.func_code.co_firstlineno
  lncmp = lambda a, b: cmp(ln(a), ln(b))
  loader.sortTestMethodsUsing = lncmp

  # NOTE: unittest.main(verbosity=2) not supported under Python 2.6
  suite  = loader.loadTestsFromTestCase(TestIcePAPController)
  unittest.TextTestRunner(verbosity=3).run(suite)
 
