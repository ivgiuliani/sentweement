import os
import sys
import imp

__name__ = "sentweement"
__version__ = "0.1"

def get_version(): return __version__

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
            sys.stderr.write("WARNING: Config file %s not found, using default settings\n" % settings_path)
            return
        except Exception as e:
            sys.stderr.write("WARNING: Skipping config file import: %s\n" % str(e))
            return

        self.__import(module)

settings = LazySettings()

