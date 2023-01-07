import sys
from .event_helpers import *


def debug_logger(*args, **kwargs):
    try:
        print(*args, file=sys.stderr, **kwargs)
    except Exception:
        pass
