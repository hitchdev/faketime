from os import path
import sys


__version__ = "0.9.6"
LIBFAKETIME_DIR = path.dirname(path.realpath(__file__))


def get_environment_vars(filename):
    """Return a dict of environment variables required to run a service under faketime."""
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
