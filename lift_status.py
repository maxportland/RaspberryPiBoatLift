import RPi_I2C_driver
from lift_state import LiftState, BlowerState, ValveState

status_lcd = RPi_I2C_driver.lcd()

state_object = {
    "lift_state": LiftState.UP,
    "blower_state": BlowerState.OFF,
    "master_valve_state": ValveState.CLOSED,
    "rear_valves": ValveState.CLOSED,
    "front_valves": ValveState.CLOSED
}


def set_primary_status(status_text):
    print(status_text)
    status_lcd.lcd_display_string(status_text, 1)


def set_secondary_status(status_text):
    print(status_text)
    status_lcd.lcd_display_string(status_text, 2)
