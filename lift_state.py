from enum import Enum


class LiftState(Enum):
    UP = 1
    DOWN = 2
    LOWERING = 3
    LIFTING = 4
    ABORT = 5


class ValveState(Enum):
    OPEN = 1
    CLOSED = 2


class BlowerState(Enum):
    ON = 1
    OFF = 2
