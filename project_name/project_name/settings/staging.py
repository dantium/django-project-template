from default import *

DEBUG = True

try:
    from local import *
except ImportError:
    pass
