import RPi_I2C_driver
from lift_state import LiftState, BlowerState, ValveState

status_lcd = RPi_I2C_driver.lcd()

state_object = {
    "lift_state": LiftState.UP,
    "blower_state": BlowerState.OFF,
    "master_valve_state": ValveState.CLOSED,
    "rear_valve_state": ValveState.CLOSED,
    "front_valve_state": ValveState.CLOSED,
    "current_countdown": 0,
    "messages": []
}


def set_primary_status(short_status_text, status_text):
    print(status_text)
    state_object["messages"].append(status_text)
    status_lcd.lcd_display_string(short_status_text, 1)


def set_secondary_status(short_status_text, status_text):
    print(status_text)
    state_object["messages"].append(status_text)
    status_lcd.lcd_display_string(short_status_text, 2)
