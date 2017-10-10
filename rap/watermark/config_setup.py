import importlib
import os
import sys

from rap.common.utils import filesystem as fs
from rap.watermark.defaults import config as defaults


CONFIG_ATTRIBUTES = ["watermark", "position", "ratio", "font", "font_color", "font_position", "font_ratio", "text"]

class Config:
    def __init__(self, *args):
        for arg in args:
            name, value = arg
            setattr(self, name, value)


def init(config_srcs, package_config_srcs):
    for src, package_src in zip(config_srcs, package_config_srcs):
        if not os.path.isfile(src):
            fs.copy(package_src, src)


def get_config(module_folder_path, module_name):
    module = __load_module(module_folder_path, module_name)
    conf_attributes = list(__get_config_attr(module, attr) for attr in CONFIG_ATTRIBUTES)
    return Config(*conf_attributes)


def __load_module(module_folder_path, module_name):
    sys.path.insert(0, module_folder_path)
    return importlib.import_module(module_name)


def __get_config_attr(module, name):
    attr = getattr(module, name, None)
    if attr is None:
        default = getattr(defaults, name, None)
        message = "WARNING: {} is not defined in the config file (defaults to: {})".format(name, default)
        print(message)
        return (name, default)
    return (name, attr)
