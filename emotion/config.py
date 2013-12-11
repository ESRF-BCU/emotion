import xml.etree.cElementTree as ElementTree
import sys
import os
from .motor import Motor, MotorGroup

CONTROLLER_MODULES_PATH = [os.path.join(os.path.dirname(__file__), "controllers")]
AXIS_MODULES_PATH = []
CONFIG_TREE = None
CONTROLLERS = {}
AXES = {}
GROUPS = {}

class Item:
  def __init__(self, name, cfg_type, klass, cfg):
    self.name = name
    self.klass = klass
    self.instance = None
    self.cfg_type = cfg_type
    self.cfg = cfg
    
  def get_instance(self):
    if self.instance is None:
      self.instance = self.klass(self.name, self.cfg)
    return self.instance

class ConfigNode:
  def __init__(self, cfg_node):
    self.tree = cfg_node

  def get_property(self, name, converter=str):
    value_node = self.tree.find(name)
    if value_node is not None:
      return converter(value_node.attrib['value'])
    else:
      raise KeyError("no property '%s` in config node" % name)

class ControllerConfigNode(ConfigNode):
  def __init__(self, *args, **kwargs):
    ConfigNode.__init__(self, *args, **kwargs)

  def controller_axes(self):
    for controller_name, controller_cfg_item in CONTROLLERS.iteritems():
       if controller_cfg_item.cfg==self:
          return controller_cfg_item.axes
  

def _get_module(module_name, path_list):
  try:
    module = sys.modules[module_name]
  except KeyError:
    old_syspath = sys.path[:]
    for path in path_list:
      sys.path.insert(0, path)

    try:
      return __import__(module_name, globals(), locals(), [""])
    finally:
      sys.path = old_syspath
  else:
    return module

def load_cfg_fromstring(config_xml):
  global CONFIG_TREE

  CONFIG_TREE = ElementTree.fromstring(config_xml)

  return _load_config()

def load_cfg(config_file):
  global CONFIG_TREE

  CONFIG_TREE = ElementTree.parse(config_file)

  return _load_config()

def _load_config():
  global AXES

  for controller_config in CONFIG_TREE.findall("controller"):
    controller_name = controller_config.get("name")
    controller_class_name = controller_config.get("class")
    if controller_name is None:
      controller_name = "%s_%d" % (controller_class_name, id(controller_config))  
    
    controller_module = _get_module(controller_class_name, CONTROLLER_MODULES_PATH)
   
    try:
      controller_class = getattr(controller_module, controller_class_name.title())
    except:
      raise RuntimeError("could not find class '%s` in module '%s`" % (controller_class_name, controller_module))
    else:
      controller_axes = load_axes(controller_config)
      for axis_name, _, _ in controller_axes:
        AXES[axis_name] = controller_name
      new_config_item = Item(controller_name, 'controller', controller_class, ControllerConfigNode(controller_config))
      new_config_item.axes = controller_axes
      CONTROLLERS[controller_name] = new_config_item

  for group_node in CONFIG_TREE.findall("group"):
    group_name = group_node.get('name')
    if group_name is None:
      raise RuntimeError("%s: group with no name" % group_node)
    GROUPS[group_name] = Item(group_name, "group", MotorGroup, group_node)

def load_axes(config_node):
    """Return list of (axis name, axis_class, axis_config_node)"""
    axes = []
    for axis_config in config_node.findall('axis'):
      axis_name = axis_config.get("name")
      if axis_name is None:
        raise RuntimeError("%s: configuration for axis does not have a name" % config_node)
      axis_class = axis_config.get("class")
      if axis_class is None:
        axis_class = Motor
      else:
        axis_module = _get_module(axis_class, AXIS_MODULES_PATH)
        try:
          axis_class = getattr(axis_module, axis_class)
        except:
          raise RuntimeError("could not find class '%s` in module '%s`" % (axis_class, axis_module))
      axes.append((axis_name, axis_class, ConfigNode(axis_config)))
    return axes

def get_axis(axis_name): 
    try:
      controller_name = AXES[axis_name]
    except KeyError:
      raise RuntimeError("no axis '%s` in config" % axis_name)
    else:
      try:
        controller = CONTROLLERS[controller_name]
      except KeyError:
        raise RuntimeError("no controller can be found for axis '%s`" % axis_name)

    controller_instance = controller.get_instance()
    
    return controller_instance.axes.get(axis_name)

def get_group(group_name):
  try:
    group = GROUPS[group_name]
  except KeyError:
    raise RuntimeError("no group '%s` in config" % group_name)
  
  return group.get_instance()

