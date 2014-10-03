import platform
import sys
import logging

logger = logging.getLogger(__name__)

def linux_distribution():
    try:
        return platform.linux_distribution()
    except:
        return "N/A"

def welcome():
    logger.info("====================================")
    logger.info("")
    logger.info("Welcome to Cloudscraper OSSE 0.0.1  ")
    logger.info("")
    logger.info("====================================")

def info():
    info = """Python version: %s
    dist: %s
    linux_distribution: %s
    system: %s
    machine: %s
    platform: %s
    uname: %s
    version: %s
    mac_ver: %s
    """ % (
    sys.version.split('\n'),
    str(platform.dist()),
    linux_distribution(),
    platform.system(),
    platform.machine(),
    platform.platform(),
    platform.uname(),
    platform.version(),
    platform.mac_ver(),
    )
    return info

def is_windows():
    return platform.system() == "Windows"

def is_linux():
    return platform.system() == "Linux"

def is_mac():
    return platform.system() == "Darwin"

def is_python_32bit():
    return "32 bit" in sys.version.split('\n')[0]

def is_os_64bit():
    if is_windows():
        return "AMD64" in platform.machine()
    elif is_linux() or is_mac():
        return "x86_64" in platform.machine()
    else:
        print "Unknown os! Using default 64-bit."
        return False

# works in Python 2 & 3
# taken from http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
class _Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Singleton(_Singleton('SingletonMeta', (object,), {})): pass
