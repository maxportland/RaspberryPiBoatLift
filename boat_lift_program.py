import RPi.GPIO as GPIO
from time import sleep
import RPi_I2C_driver
import signal
from enum import Enum
from threading import Event

exit = Event()

GPIO.setwarnings(False)

SMALL_VALVE_TIMING = 4
LARGE_VALVE_TIMING = 5
LOWER_BACK_WAIT = 35
LOWER_FRONT_WAIT = 25
RAISE_FRONT_TIMING = 20
RAISE_REAR_TIMING = 15
RAISE_BOTH_TIMING = 20

class State(Enum):
    UP = 1
    DOWN = 2
    LOWERING = 3
    LIFTING = 4
    ABORT = 5

BLOWER = 4
MASTER_VALVE = 5

# Rear
REAR_VALVE_POWER = 19
REAR_LEFT_VALVE = 6
REAR_RIGHT_VALVE = 12
REAR_VALVES = [REAR_LEFT_VALVE, REAR_RIGHT_VALVE]

# Front
FRONT_VALVE_POWER = 20
FRONT_LEFT_VALVE = 13
FRONT_RIGHT_VALVE = 16
FRONT_VALVES = [FRONT_LEFT_VALVE, FRONT_RIGHT_VALVE]

# Buttons 
UP_BUTTON = 18
DOWN_BUTTON = 17

# All
VALVE_POWER = [FRONT_VALVE_POWER, REAR_VALVE_POWER]
ALL_VALVES = FRONT_VALVES + REAR_VALVES
BUTTONS = [UP_BUTTON, DOWN_BUTTON]

state = State.DOWN

GPIO.setmode(GPIO.BCM)
GPIO.setup(ALL_VALVES + VALVE_POWER + [BLOWER, MASTER_VALVE], GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

status_lcd = RPi_I2C_driver.lcd()

def up_button_callback(channel):
    if(state != State.LIFTING and state != State.UP):
        lift_boat()
    elif(state == State.LIFTING or state == State.LOWERING):
        abort()
    
def down_button_callback(channel):
    if(state != State.LOWERING and state != State.DOWN):
        lower_boat()
    elif(state == State.LIFTING or state == State.LOWERING):
        abort()

def turn_off_blower():
    #GPIO.output(BLOWER, True)
    set_secondary_status("BLOWER: OFF     ")
    
def turn_on_blower():
    #GPIO.output(BLOWER, False)
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

def set_primary_status(status_text):
    print(status_text)
    status_lcd.lcd_display_string(status_text, 1)
    
def set_secondary_status(status_text):
    print(status_text)
    status_lcd.lcd_display_string(status_text, 2)

def lower_boat():
    global state
    status_lcd.backlight(1)
    state = State.LOWERING
    set_primary_status("--- LOWERING ---")
    turn_off_blower()
    open_master_valve()
    open_rear_valves()
    sleep(LOWER_BACK_WAIT)
    open_front_valves()
    sleep(LOWER_FRONT_WAIT)
    state = State.DOWN
    status_lcd.lcd_clear()
    set_primary_status("-- BOAT  DOWN --")
    set_secondary_status("       :)       ")
    sleep(10)
    if(state == State.DOWN):
        status_lcd.backlight(0)

def lift_boat():
    global state
    status_lcd.backlight(1)
    state = State.LIFTING
    set_primary_status("--- LIFTING ----")
    close_master_valve()
    open_front_valves()
    turn_on_blower()
    sleep(RAISE_FRONT_TIMING)
    open_rear_valves()
    sleep(RAISE_REAR_TIMING)
    close_front_valves()
    sleep(RAISE_BOTH_TIMING)
    close_rear_valves()
    turn_off_blower()
    state = State.UP
    status_lcd.lcd_clear()
    set_primary_status("--- BOAT  UP ---")
    set_secondary_status("       :)       ")
    sleep(10)
    if(state == State.UP):
        status_lcd.backlight(0) 
    
    
def abort():
    state = State.ABORT

def main():
    while not exit.is_set():
        sleep(20)

def quit(signo, _frame):
    print("Interrupted by %d, shutting down" % signo)
    GPIO.cleanup()
    exit.set()

if __name__ == '__main__':
    
    for sig in ('TERM', 'HUP', 'INT'):
        signal.signal(getattr(signal, 'SIG'+sig), quit);
    
    status_lcd.backlight(0)
    
    GPIO.add_event_detect(UP_BUTTON, GPIO.FALLING, callback=up_button_callback, bouncetime=1000)
    GPIO.add_event_detect(DOWN_BUTTON, GPIO.FALLING, callback=down_button_callback, bouncetime=1000)
    
    GPIO.output(VALVE_POWER, False)
    GPIO.output(ALL_VALVES + [MASTER_VALVE], True)
    sleep(SMALL_VALVE_TIMING)
    GPIO.output(VALVE_POWER, True)
    
    main()
