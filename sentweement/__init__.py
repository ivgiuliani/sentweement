import os
import sys
import imp

__name__ = "sentweement"
__version__ = "0.1"


class LazySettings(object):
    "Lazily load settings"
    CONFIG_MODULE = "__config"

    def __init__(self):
        # import default settings (we shouldn't hardcode the name though)
        m = "sentweement.default".split(".")
        module = __import__(m[0], globals(), locals(), m[1:], -1)
        module = getattr(module, m[-1], module)
        self.__import(module)

    def __import(self, module):
        for setting in dir(module):
            if setting == setting.upper():
                value = getattr(module, setting)
                setattr(self, setting, value)

    def use(self, settings_path):
        path = settings_path.rsplit(os.sep, 1)
        sys.modules[self.CONFIG_MODULE] = None
        try:
            module = imp.load_source(self.CONFIG_MODULE, *path)
        except IOError:
            err_str = "Config file %s not found, using default settings"
            self.print_warning(err_str % settings_path)
            return
        except Exception as e:
            err_str = "Skipping config file import: %s"
            self.print_warning(err_str % str(e))
            return

        self.__import(module)

    def print_warning(self, msg):
        sys.stderr.write("WARNING: %s\n" % msg)


def get_version():
    return __version__

settings = LazySettings()
