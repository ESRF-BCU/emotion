import gevent
import gevent.event
import functools
from .task_utils import task
from .settings import AxisSettings
from .axis import MOVING, READY

class Controller:
  def __init__(self, name, config, axes):
    self.__name = name
    self.__config = config
    self.__initialized_axis = dict()
    self._axes = dict()

    self.axis_settings = AxisSettings()

    for axis_name, axis_class, axis_config in axes:
        axis = axis_class(self, axis_config)
        self._axes[axis_name] = axis
        self.__initialized_axis[axis] = False
 
        # push config from XML file into axes settings.
        self.axis_settings.set_from_config(axis, axis.config)

        # install axis.settings set/get methods
        axis.settings.set = functools.partial(self.axis_settings.set, axis)
        axis.settings.get = functools.partial(self.axis_settings.get, axis)

  @property
  def axes(self):
    return self._axes

  @property
  def name(self):
    return self.__name

  @property
  def config(self):
    return self.__config

  def get_property(self, property_name, converter=str):
     property_attrs = self.__config.get(property_name)
     if property_attrs is not None:
       return converter(property_attrs.get("value"))
     else:
       raise KeyError("no property '%s` in config" % property_name)

  def get_axis(self, axis_name):
    axis = self._axes[axis_name]

    if not self.__initialized_axis[axis]:
      self.initialize_axis(axis)
      self.__initialized_axis[axis] = True

    return axis

  def initialize_axis(self, axis):
    raise NotImplementedError

  def prepare_move(self, axis, target_pos, delta):
    raise NotImplementedError

  def start_move(self, axis):
    raise NotImplementedError

  def stop(self, axis):
    raise NotImplementedError

  def read_position(self, axis, measured=False):
    raise NotImplementedError

  def read_velocity(self, axis):
    raise NotImplementedError

  def read_state(self, axis):
    raise NotImplementedError


