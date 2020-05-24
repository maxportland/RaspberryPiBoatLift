from lift_status import *
from time import sleep
from setting_constants import *
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(ALL_VALVES + VALVE_POWER + [BLOWER, MASTER_VALVE], GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def loop_pause(seconds):
    for i in range(seconds):
        sleep(1)


def turn_off_blower():
    GPIO.output(BLOWER, True)
    change_blower_state(BlowerState.OFF)
    set_secondary_status("BLOWER: OFF     ", "Blower Off")


def turn_on_blower():
    GPIO.output(BLOWER, False)
    change_blower_state(BlowerState.ON)
    set_secondary_status("BLOWER: ON      ", "Blower On")


def open_master_valve():
    GPIO.output(MASTER_VALVE, False)
    change_master_valve_state(ValveState.OPEN)
    set_secondary_status("MSTR VALVE: OPEN", "Master Valve Open")
    loop_pause(LARGE_VALVE_TIMING)


def close_master_valve():
    GPIO.output(MASTER_VALVE, True)
    change_master_valve_state(ValveState.CLOSED)
    set_secondary_status("MSTR VALVE: CLSE", "Master Valve Closed")
    loop_pause(LARGE_VALVE_TIMING)


def open_rear_valves():
    GPIO.output(REAR_VALVE_POWER, False)
    GPIO.output(REAR_VALVES, False)
    set_secondary_status("REAR VALVES:OPEN", "Rear Valves Opened")
    loop_pause(SMALL_VALVE_TIMING)
    GPIO.output(REAR_VALVE_POWER, True)
    change_rear_valve_state(ValveState.OPEN)


def close_rear_valves():
    GPIO.output(REAR_VALVE_POWER, False)
    GPIO.output(REAR_VALVES, True)
    set_secondary_status("REAR VALVES:CLSE", "Rear Valves Closed")
    loop_pause(SMALL_VALVE_TIMING)
    GPIO.output(REAR_VALVE_POWER, True)
    change_rear_valve_state(ValveState.CLOSED)


def open_front_valves():
    GPIO.output(FRONT_VALVE_POWER, False)
    GPIO.output(FRONT_VALVES, False)
    set_secondary_status("FRNT VALVES:OPEN", "Front Valves Opened")
    loop_pause(SMALL_VALVE_TIMING)
    GPIO.output(FRONT_VALVE_POWER, True)
    change_front_valve_state(ValveState.OPEN)


def close_front_valves():
    GPIO.output(FRONT_VALVE_POWER, False)
    GPIO.output(FRONT_VALVES, True)
    set_secondary_status("FRNT VALVES:CLSE", "Front Valves Closed")
    loop_pause(SMALL_VALVE_TIMING)
    GPIO.output(FRONT_VALVE_POWER, True)
    change_front_valve_state(ValveState.CLOSED)
