from enum import Enum


class LiftState(str, Enum):
    UP = "up"
    DOWN = "down"
    LOWERING = "lowering"
    LIFTING = "lifting"
    ABORT = "abort"


class ValveState(str, Enum):
    OPEN = "open"
    CLOSED = "closed"


class BlowerState(str, Enum):
    ON = "on"
    OFF = "off"
