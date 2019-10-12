from os import path
from datetime import datetime
import sys

__version__ = "DEVELOPMENT_VERSION"


LIBFAKETIME_DIR = path.dirname(path.realpath(__file__))


class FaketimeError(Exception):
    pass


class Faketime(object):
    def __init__(self, faketime_filename):
        self._faketime_filename = path.abspath(faketime_filename)
    
    def change_time(self, new_time):
        assert isinstance(new_time, datetime), "new_time should be of type/subtype datetime"
        with open(self._faketime_filename, "w") as faketimetxt_handle:
            faketimetxt_handle.write("@" + new_time.strftime("%Y-%m-%d %H:%M:%S"))
    
    @property
    def env_vars(self):
        """
        Dict containing environment variables required to run a process with libfaketime.
        """
        if sys.platform == "linux" or sys.platform == "linux2":
            return {
                'LD_PRELOAD': path.join(LIBFAKETIME_DIR, "libfaketime.so.1"),
                'FAKETIME_TIMESTAMP_FILE': self._faketime_filename,
            }
        elif sys.platform == "darwin":
            return {
                'DYLD_INSERT_LIBRARIES': path.join(LIBFAKETIME_DIR, "libfaketime.1.dylib"),
                'DYLD_FORCE_FLAT_NAMESPACE': '1',
                'FAKETIME_TIMESTAMP_FILE': self._faketime_filename,
            }
        else:
            raise FaketimeError("libfaketime does not support the '{}' platform".format(sys.platform))
        
        
## DEPRECATED
## The functions below are included to prevent old code from breaking
## They essentially do the same thing as the code above.

def get_environment_vars(filename):
    """Return a dict of environment variables required to run a service under faketime."""
    print("get_environment_vars is a deprecated function; see https://github.com/hitchdev/faketime for alternate usage.")
    if sys.platform == "linux" or sys.platform == "linux2":
        return {
            'LD_PRELOAD': path.join(LIBFAKETIME_DIR, "libfaketime.so.1"),
            'FAKETIME_SKIP_CMDS': 'nodejs',     # node doesn't seem to work in the current version.
            'FAKETIME_TIMESTAMP_FILE': filename,
        }
    elif sys.platform == "darwin":
        return {
            'DYLD_INSERT_LIBRARIES': path.join(LIBFAKETIME_DIR, "libfaketime.1.dylib"),
            'DYLD_FORCE_FLAT_NAMESPACE': '1',
            'FAKETIME_TIMESTAMP_FILE': filename,
        }
    else:
        raise RuntimeError("libfaketime does not support '{}' platform".format(sys.platform))


def change_time(filename, newtime):
    """Change the time of a process or group of processes by writing a new time to the time file."""
    with open(filename, "w") as faketimetxt_handle:
        faketimetxt_handle.write("@" + newtime.strftime("%Y-%m-%d %H:%M:%S"))
