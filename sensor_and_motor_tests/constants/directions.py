from enum import Enum


class DriveDirection(Enum):
    FORWARDS = "forwards"
    REVERSE = "reverse"


class TurnDirection(Enum):
    LEFT = "left"
    RIGHT = "right"
    STRAIGHT = "straight"
