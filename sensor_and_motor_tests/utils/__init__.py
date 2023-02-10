import sys
from ev3dev2.port import LegoPort

from .event_helpers import *


def debug_logger(*args, **kwargs):
    try:
        print(*args, file=sys.stderr, **kwargs)
    except Exception:
        pass


def safe_init_port(port_letter, keyword_args):
    port_x = f"port_{port_letter.lower()}"
    outX = f"out{port_letter.upper()}"
    return keyword_args[port_x] or LegoPort(outX)
