"""
Emotion generic library
"""
from emotion import Controller
from emotion.controller import add_axis_method
from emotion.axis import READY, MOVING
from emotion import task, error_cleanup, cleanup




"""
IcePAP specific library
"""
import icepap.lib



"""
"""
import random
import math
import time
import pdb


class IcePAP(Controller):
  """Implement IcePAP stepper motor controller access"""

  def __init__(self, name, config, axes):
    """Contructor"""
    Controller.__init__(self, name, config, axes)


  def initialize(self):
    """Controller initialization"""

    # Get controller config from emotion config
    # Mandatory parameters
    self.host = self.config.get("host")

    # Optional parameters
    try:
      self.libdebug = int(self.config.get("libdebug"))
    except:
      self.libdebug = 1

    # Create an IcePAP lib object to access the MASTER
    self.libdevice = icepap.lib.System(self.host, "verb=%d"%self.libdebug)

    # Create an IcePAP lib object as default group
    self.libgroup  = icepap.lib.Group("default")


  def finalize(self):
    """Controller no more needed"""	  
    # Remove any group in the IcePAP lib
    try:
      self.libgroup.delete()
    except:
      pass

    # Close IcePAP lib socket/threads
    #self.libdevice.close()


  def initialize_axis(self, axis):
    """Axis initialization"""

    # Get axis config from emotion config
    axis.address  = axis.config.get("address", int)

    # Create an IcePAP lib axis object
    device        = self.libdevice
    address       = axis.address
    name          = axis.name
    axis.libaxis  = icepap.lib.Axis(device, address, name)

    # Add the axis to the default IcePAP lib group 
    self.libgroup.add_axis(axis.libaxis)

    # Add new axis oject methods
    add_axis_method(axis, self.get_identifier)




  def position(self, axis, new_position=None, measured=False):
    """Returns axis position in motor units"""

    # Optionnal new position to set
    if new_position:
      pass

    # Always return the current position
    pos_stps = self.libgroup.pos([axis.libaxis])[axis.libaxis]

    return pos_stps


  def velocity(self, axis, new_velocity=None):
    """Returns axis current velocity in user units per seconds"""

    # Optionnal new velocity to set
    if new_velocity:
      pass

    # Always return the current velocity
    """    
    # TODO
    return self.axis_settings.get(axis, "velocity")
    """    


  def read_state(self, axis):
    """Returns the current axis state"""

    # The axis can only be accessed through a group in IcePAP lib
    # Use the default group
    status = self.libgroup.status([axis.libaxis])[axis.libaxis]

    # Convert status formats
    if(icepap.lib.status_moving(status)):
      return MOVING

    # TODO: check that instead of considering it as a default
    return READY


  def prepare_move(self, axis, target_pos, delta):
    """Called once before an axis motion, positions in motor units"""


  def start_move(self, axis, target_pos, delta):
    """Launch an axis moition, returns immediately, positions in motor units"""
    target_positions = icepap.lib.PosList()
    target_positions[axis.libaxis] = target_pos
    self.libgroup.move(target_positions)


  def stop(self, axis):
    """Stops smoothly an axis motion"""
    self.libgroup.stop([axis.libaxis])


  def abort(self, axis):
    """Stops as fast as possible an axis motion, emergency stop"""


  def _set_lib_verbose(self, val): 
    """Change IcePAP library verbose level"""
    self.libdevice.set_verbose(val)


  def get_identifier(self, axis):
    """Returns the unique string identifier of the specified axis"""
    return self.libgroup.command("?ID", [axis.libaxis])[axis.libaxis]

