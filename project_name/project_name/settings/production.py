from default import *

DEBUG = False

try:
    from local import *
except ImportError:
    pass
