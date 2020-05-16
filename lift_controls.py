from lift_status import *
from time import sleep
from setting_constants import *
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(ALL_VALVES + VALVE_POWER + [BLOWER, MASTER_VALVE], GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def turn_off_blower():
    GPIO.output(BLOWER, True)
    set_secondary_status("BLOWER: OFF     ")


def turn_on_blower():
    GPIO.output(BLOWER, False)
    set_secondary_status("BLOWER: ON      ")


def open_master_valve():
    GPIO.output(MASTER_VALVE, False)
    set_secondary_status("MSTR VALVE: OPEN")
    sleep(LARGE_VALVE_TIMING)


def close_master_valve():
    GPIO.output(MASTER_VALVE, True)
    set_secondary_status("MSTR VALVE: CLSE")
    sleep(LARGE_VALVE_TIMING)


def open_rear_valves():
    GPIO.output(REAR_VALVE_POWER, False)
    GPIO.output(REAR_VALVES, False)
    set_secondary_status("REAR VALVES:OPEN")
    sleep(SMALL_VALVE_TIMING)
    GPIO.output(REAR_VALVE_POWER, True)


def close_rear_valves():
    GPIO.output(REAR_VALVE_POWER, False)
    GPIO.output(REAR_VALVES, True)
    set_secondary_status("REAR VALVES:CLSE")
    sleep(SMALL_VALVE_TIMING)
    GPIO.output(REAR_VALVE_POWER, True)


def open_front_valves():
    GPIO.output(FRONT_VALVE_POWER, False)
    GPIO.output(FRONT_VALVES, False)
    set_secondary_status("FRNT VALVES:OPEN")
    sleep(4)
    GPIO.output(FRONT_VALVE_POWER, True)


def close_front_valves():
    GPIO.output(FRONT_VALVE_POWER, False)
    GPIO.output(FRONT_VALVES, True)
    set_secondary_status("FRNT VALVES:CLSE")
    sleep(SMALL_VALVE_TIMING)
    GPIO.output(FRONT_VALVE_POWER, True)
