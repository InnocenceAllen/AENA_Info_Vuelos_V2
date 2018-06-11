from enum import Enum


class DelayLevel(Enum):
    NO_DELAY = 0
    LOW_DELAY = 1
    MEDIUM_DELAY = 2
    HIGH_DELAY = 3


class TimeLevel(Enum):
    NIGHT = 0
    MORNING = 1
    AFTERNOON = 2
    EVENING = 3
