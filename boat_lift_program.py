import RPi.GPIO as GPIO
from time import sleep
import signal
from enum import Enum
GPIO.setwarnings(False)

class State(Enum):
    UP = 1
    DOWN = 2
    LOWERING = 3
    LIFTING = 4
    ABORT = 5

BLOWER = 4
MASTER_VALVE = 5

# Rear
REAR_VALVE_POWER = 20
REAR_LEFT_VALVE = 6
REAR_RIGHT_VALVE = 12
REAR_VALVES = [REAR_LEFT_VALVE, REAR_RIGHT_VALVE]

# Front
FRONT_VALVE_POWER = 19
FRONT_LEFT_VALVE = 13
FRONT_RIGHT_VALVE = 16
FRONT_VALVES = [FRONT_LEFT_VALVE, FRONT_RIGHT_VALVE]

# Buttons 
UP_BUTTON = 17
DOWN_BUTTON = 18

# All
VALVE_POWER = [FRONT_VALVE_POWER, FRONT_VALVES]
ALL_VALVES = REAR_VALVES + REAR_VALVES
BUTTONS = [UP_BUTTON, DOWN_BUTTON]

STATE = State.UP

GPIO.setmode(GPIO.BCM) 
GPIO.setup(ALL_VALVES + VALVE_POWER, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def up_button_callback(channel):
    if(STATE != State.LIFTING and STATE != State.UP):
        lift_boat()
    elif(STATE == State.LIFTING or STATE == State.LOWERING):
        abort()
    
def down_button_callback(channel):
    if(STATE != State.LOWERING and STATE != State.DOWN):
        lower_boat()
    elif(STATE == State.LIFTING or STATE == State.LOWERING):
        abort()

def turn_off_blower():
    GPIO.output(BLOWER, True)
    
def turn_on_blower():
    GPIO.output(BLOWER, False)
    
def open_master_valve():
    GPIO.output(MASTER_VALVE, False)
    sleep(5)
    
def close_master_valve():
    GPIO.output(MASTER_VALVE, True)
    sleep(5)

def open_rear_valves():
    GPIO.output(REAR_VALVE_POWER, False)
    GPIO.output(REAR_VALVES, False)
    sleep(3)
    GPIO.output(REAR_VALVE_POWER, True)
    
def open_front_valves():
    GPIO.output(FRONT_VALVE_POWER, False)
    GPIO.output(FRONT_VALVES, False)
    sleep(3)
    GPIO.output(FRONT_VALVE_POWER, True)
    
def close_rear_valves():
    GPIO.output(REAR_VALVE_POWER, False)
    GPIO.output(REAR_VALVES, True)
    sleep(3)
    GPIO.output(REAR_VALVE_POWER, True)
    
def close_front_valves():
    GPIO.output(FRONT_VALVE_POWER, False)
    GPIO.output(FRONT_VALVES, True)
    sleep(3)
    GPIO.output(FRONT_VALVE_POWER, True)

def lower_boat():
    turn_off_blower()
    open_master_valve()
    open_rear_valves()
    sleep(35)
    open_front_valves()
    sleep(35)

def lift_boat():
    close_master_valve()
    open_front_valves()
    turn_on_blower()
    sleep(20)
    open_rear_valves()
    sleep(15)
    close_front_valves()
    sleep(25)
    close_rear_valves()
    turn_off_blower()
    
    
def abort():
    STATE = State.ABORT
    
GPIO.add_event_detect(17, GPIO.FALLING, callback=up_button_callback, bouncetime=500)
GPIO.add_event_detect(18, GPIO.FALLING, callback=down_button_callback, bouncetime=500)

message = input("Press enter to quit\n\n") # Run until someone presses enter
GPIO.cleanup()