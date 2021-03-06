__package__ = 'emotion.config'

import sys
import os
from .. import event
from ..axis import Axis, AxisRef
from ..encoder import Encoder

try:
    from beacon.static import get_config as beacon_get_config
except ImportError, why:
    def beacon_get_config(*args):
        raise RuntimeError("Beacon is not imported: %r" % why)

BEACON_CONFIG = None

BACKEND = 'xml'

CONTROLLER_MODULES_PATH = [
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "controllers"))]
AXIS_MODULES_PATH = []
ENCODER_MODULES_PATH = []

CONTROLLERS = {}
CONTROLLER_BY_AXIS = {}
CONTROLLER_BY_ENCODER = {}
LOADED_FILES = set()

def set_backend(backend):
    global BACKEND
    if not BACKEND in ("xml", "beacon"):
        raise RuntimeError("Unknown backend '%s`" % backend)
    BACKEND = backend

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


def get_controller_class(
        controller_class_name,
        controller_modules_path=CONTROLLER_MODULES_PATH):
    """Get controller class object from controller class name

    Args:
        controller_class_name (str):
            The controller class name.
        controller_modules_path (list):
            Default CONTROLLER_MODULES_PATH;
            List of paths to look modules for.

    Returns:
        Controller class object

    Raises:
        RuntimeError
    """
    controller_module = _get_module(
        controller_class_name,
        controller_modules_path)
    try:
        controller_class = getattr(controller_module, controller_class_name)
    except:
        try:
            controller_class = getattr(
                controller_module,
                controller_class_name.title())
        except:
            raise RuntimeError(
                "could not find class '%s` in module '%s`" %
                (controller_class_name, controller_module))

    return controller_class


def get_axis_class(axis_class_name, axis_modules_path=AXIS_MODULES_PATH):
    """Get axis class object from axis class name

    Args:
        axis_class_name (str):
            The axis class name
        axis_modules_path (list):
            Default AXIS_MODULES_PATH;
            List of paths to look modules for

    Returns:
        Axis class object

    Raises:
        RuntimeError
    """
    return _get_class(axis_class_name, axis_modules_path)

def get_encoder_class(encoder_class_name, encoder_modules_path=ENCODER_MODULES_PATH):
    return _get_class(encoder_class_name, encoder_modules_path)

def _get_class(class_name, modules_path):
    module = _get_module(class_name, modules_path)

    try:
        klass = getattr(module, class_name)
    except:
        raise RuntimeError(
            "could not find class '%s` in module '%s`" %
            (class_name, module))
    else:
        return klass


def add_controller(
        controller_name,
        controller_config,
        controller_axes,
        controller_encoders,
        controller_class):
    """Instanciate a controller object from configuration, and store it in the global CONTROLLERS dictionary

    Args:
        controller_name (str):
            Controller name, has to be unique
        controller_config (dict):
            Dictionary containing the configuration of the controller
        controller_axes (list):
            A list of tuples (axis_name, axis_class_name, axis_config) for each axis in controller
        controller_encoders (list):
            A list of tuples (encoder_name, encoder_class_name, encoder_config) for each encoder in controller
        controller_class (class object):
            Controller class

    Returns:
        None
    """
    axes = list()
    for axis_name, axis_class_name, axis_config in controller_axes:
        if not CONTROLLER_BY_AXIS.get(axis_name):
            # new axis
            CONTROLLER_BY_AXIS[axis_name] = controller_name

            if axis_class_name is None:
                axis_class = Axis
            else:
                axis_class = get_axis_class(axis_class_name)

            axes.append((axis_name, axis_class, axis_config))
        else:
            # existing axis
            # TODO: check for duplicated axis
            axes.append((axis_name, AxisRef, axis_config))

    encoders = list()
    for encoder_name, encoder_class_name, encoder_config in controller_encoders:
        if not CONTROLLER_BY_ENCODER.get(encoder_name):
            # new encoder
            CONTROLLER_BY_ENCODER[encoder_name] = controller_name

            if encoder_class_name is None:
                encoder_class = Encoder
            else:
                encoder_class = get_encoder_class(encoder_class_name)

            encoders.append((encoder_name, encoder_class, encoder_config))
        else:
            # existing axis
            raise RuntimeError("Duplicated encoder '%s`" % encoder_name)

    controller = controller_class(controller_name, controller_config, axes, encoders)
    CONTROLLERS[controller_name] = {"object": controller,
                                    "initialized": False}


def get_axis(axis_name):
    """Get axis from loaded configuration or from Beacon

    If needed, instanciates the controller of the axis and initializes it.

    Args:
        axis_name (str):
            Axis name

    Returns:
        :class:`emotion.axis.Axis` object

    Raises:
        RuntimeError
    """
    if BACKEND=='beacon':
        global BEACON_CONFIG
        if BEACON_CONFIG is None:
            BEACON_CONFIG = beacon_get_config() 
        o = BEACON_CONFIG.get(axis_name)
        if not isinstance(o, Axis):
            raise AttributeError("'%s` is not an axis" % axis_name)
        return o
 
    try:
        controller_name = CONTROLLER_BY_AXIS[axis_name]
    except KeyError:
        raise RuntimeError("no axis '%s` in config" % axis_name)
    else:
        try:
            controller = CONTROLLERS[controller_name]
        except KeyError:
            raise RuntimeError(
                "no controller can be found for axis '%s`" %
                axis_name)

    try:
        controller_instance = controller["object"]
    except KeyError:
        raise RuntimeError(
            "could not get controller instance for axis '%s`" %
            axis_name)

    if not controller["initialized"]:
        controller_instance._update_refs()
        controller_instance.initialize()
        controller["initialized"] = True

    axis = controller_instance.get_axis(axis_name)
    event.connect(axis, "write_setting", write_setting)

    return axis


def axis_names_list():
    """Return list of all Axis objects names in loaded configuration"""
    return CONTROLLER_BY_AXIS.keys()


def get_encoder(encoder_name):
    if BACKEND == 'beacon':
        global BEACON_CONFIG
        if BEACON_CONFIG is None:
            BEACON_CONFIG = beacon_get_config()
        o = BEACON_CONFIG.get(encoder_name)
        if not isinstance(o, Encoder):
            raise AttributeError("'%s` is not an encoder" % encoder_name)
        return o

    try:
        controller_name = CONTROLLER_BY_ENCODER[encoder_name]
    except KeyError:
        raise RuntimeError("no encoder '%s` in config" % encoder_name)
    else:
        try:
            controller = CONTROLLERS[controller_name]
        except KeyError:
            raise RuntimeError("no controller can be found for encoder '%s`" % encoder_name)

    try:
        controller_instance = controller["object"]
    except KeyError:
        raise RuntimeError("could not get controller instance for encoder '%s`" % encoder_name)

    if not controller["initialized"]:
        controller_instance._update_refs()
        controller_instance.initialize()
        controller["initialized"] = True

    encoder = controller_instance.get_encoder(encoder_name)
    
    return encoder
   

def clear_cfg():
    """Clear configuration

    Remove all controllers; :func:`emotion.controller.finalize` is called on each one.
    """
    if BACKEND == 'beacon':
        global BEACON_CONFIG
        if BEACON_CONFIG is not None:
            BEACON_CONFIG._clear_instances()
    else:
        global CONTROLLERS
        global CONTROLLER_BY_AXIS
        global CONTROLLER_BY_ENCODER
        global LOADED_FILES

        for controller_name, controller in CONTROLLERS.iteritems():
             controller["object"].finalize()
        CONTROLLERS = {}
        CONTROLLER_BY_AXIS = {}
        CONTROLLER_BY_ENCODER = {}
        LOADED_FILES = set()


def load_cfg(filename, clear=True):
    """Load configuration from file

    Configuration is cleared first (calls :func:`clear_cfg`)
    Calls the right function depending on the current backend set by the
    BACKEND global variable. Defaults to 'xml'.

    Args:
        filename (str):
            Full path to configuration file

    Returns:
        None
    """

    if clear:
        clear_cfg()
    if filename in LOADED_FILES:
        return
    if BACKEND == 'xml':
        filename = os.path.abspath(filename)
        from .xml_backend import load_cfg
    elif BACKEND == 'beacon':
        from .beacon_backend import load_cfg
    try:
        load_cfg(filename)
    except:
        raise
    else:
        LOADED_FILES.add(filename)


def load_cfg_fromstring(config_str, clear=True):
    """Load configuration from string

    Configuration is cleared first (calls :func:`clear_cfg`)
    Calls the right function depending on the current backend set by the
    BACKEND global variable. Defaults to 'xml'.

    Args:
        config_str (str):
            Configuration string

    Returns:
        None
    """
    if clear:
        clear_cfg()
    if BACKEND == 'xml':
        from .xml_backend import load_cfg_fromstring
    elif BACKEND == 'beacon':
        from .beacon_backend import load_cfg_fromstring
    return load_cfg_fromstring(config_str)


def write_setting(axis_config, setting_name, setting_value, write):
    if BACKEND == 'xml':
        from .xml_backend import write_setting
    elif BACKEND == 'beacon':
        from .beacon_backend import write_setting

    write_setting(
        axis_config.config_dict, setting_name, setting_value, write)

def get_axis_setting(axis, setting_name):
    """Get setting value from axis and setting name

    Args:
        axis:
           Axis object (Axis object)
        
        setting_name (str):
            Setting name

    Returns:
        Setting value, or None if setting has never been set

    Raises:
        RuntimeError if settings does not exist for axis 
    """
    if BACKEND == 'xml':
        try:
            settings = axis.config.config_dict["settings"]
        except KeyError:
            raise RuntimeError
        else:
            setting_value = settings.get(setting_name)
            if setting_value is None:
                setting_value = axis.config.config_dict.get(setting_name)
            return setting_value["value"] if setting_value else None
    elif BACKEND == 'beacon':
        from .beacon_backend import get_axis_setting
        return get_axis_setting(axis, setting_name)


def StaticConfig(*args, **kwargs):
    if BACKEND == 'xml':
      from .xml_backend import StaticConfig
      return StaticConfig(*args, **kwargs)  
    elif BACKEND == 'beacon':
      from .beacon_backend import StaticConfig
      return StaticConfig(*args, **kwargs)  
