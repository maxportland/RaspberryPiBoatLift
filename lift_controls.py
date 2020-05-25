from lift_status import LiftStatus
from lift_state import *
from time import sleep
from setting_constants import *
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(ALL_VALVES + VALVE_POWER + [BLOWER, MASTER_VALVE], GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)


class LiftControls(object):
    @staticmethod
    def turn_off_blower():
        GPIO.output(BLOWER, True)
        LiftStatus.change_blower_state(BlowerState.OFF)
        LiftStatus.set_secondary_status("BLOWER: OFF     ", "Blower Off")

    @staticmethod
    def turn_on_blower():
        GPIO.output(BLOWER, False)
        LiftStatus.change_blower_state(BlowerState.ON)
        LiftStatus.set_secondary_status("BLOWER: ON      ", "Blower On")

    @staticmethod
    def open_master_valve():
        GPIO.output(MASTER_VALVE, False)
        LiftStatus.change_master_valve_state(ValveState.OPEN)
        LiftStatus.set_secondary_status("MSTR VALVE: OPEN", "Master Valve Open")
        sleep(LARGE_VALVE_TIMING)

    @staticmethod
    def close_master_valve():
        GPIO.output(MASTER_VALVE, True)
        LiftStatus.change_master_valve_state(ValveState.CLOSED)
        LiftStatus.set_secondary_status("MSTR VALVE: CLSE", "Master Valve Closed")
        sleep(LARGE_VALVE_TIMING)

    @staticmethod
    def open_rear_valves():
        GPIO.output(REAR_VALVE_POWER, False)
        GPIO.output(REAR_VALVES, False)
        LiftStatus.set_secondary_status("REAR VALVES:OPEN", "Rear Valves Opened")
        sleep(SMALL_VALVE_TIMING)
        GPIO.output(REAR_VALVE_POWER, True)
        LiftStatus.change_rear_valve_state(ValveState.OPEN)

    @staticmethod
    def close_rear_valves():
        GPIO.output(REAR_VALVE_POWER, False)
        GPIO.output(REAR_VALVES, True)
        LiftStatus.set_secondary_status("REAR VALVES:CLSE", "Rear Valves Closed")
        sleep(SMALL_VALVE_TIMING)
        GPIO.output(REAR_VALVE_POWER, True)
        LiftStatus.change_rear_valve_state(ValveState.CLOSED)

    @staticmethod
    def open_front_valves():
        GPIO.output(FRONT_VALVE_POWER, False)
        GPIO.output(FRONT_VALVES, False)
        LiftStatus.set_secondary_status("FRNT VALVES:OPEN", "Front Valves Opened")
        sleep(SMALL_VALVE_TIMING)
        GPIO.output(FRONT_VALVE_POWER, True)
        LiftStatus.change_front_valve_state(ValveState.OPEN)

    @staticmethod
    def close_front_valves():
        GPIO.output(FRONT_VALVE_POWER, False)
        GPIO.output(FRONT_VALVES, True)
        LiftStatus.set_secondary_status("FRNT VALVES:CLSE", "Front Valves Closed")
        sleep(SMALL_VALVE_TIMING)
        GPIO.output(FRONT_VALVE_POWER, True)
        LiftStatus.change_front_valve_state(ValveState.CLOSED)
