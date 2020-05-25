import RPi_I2C_driver
from lift_state import LiftState, BlowerState, ValveState
from app import socketio
import json


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


class LiftStatus(object):

    @staticmethod
    def get_state_object():
        return state_object

    @staticmethod
    def change_lift_state(lift_state):
        state_object["lift_state"] = lift_state
        LiftStatus.broadcast_state_change()

    @staticmethod
    def change_blower_state(blower_state):
        state_object["blower_state"] = blower_state
        LiftStatus.broadcast_state_change()

    @staticmethod
    def change_master_valve_state(master_valve_state):
        state_object["master_valve_state"] = master_valve_state
        LiftStatus.broadcast_state_change()

    @staticmethod
    def change_rear_valve_state(rear_valve_state):
        state_object["rear_valve_state"] = rear_valve_state
        LiftStatus.broadcast_state_change()

    @staticmethod
    def change_front_valve_state(front_valve_state):
        state_object["front_valve_state"] = front_valve_state
        print("change_front_valve_state")
        LiftStatus.broadcast_state_change()

    @staticmethod
    def broadcast_state_change():
        print("broadcast_state_change")
        socketio.emit('state_change', json.dumps(state_object))

    @staticmethod
    def set_primary_status(lcd_status_text, status_text):
        print(status_text)
        state_object["messages"].append(status_text)
        LiftStatus.broadcast_state_change()
        status_lcd.lcd_display_string(lcd_status_text, 1)

    @staticmethod
    def set_secondary_status(lcd_status_text, status_text):
        print(status_text)
        state_object["messages"].append(status_text)
        LiftStatus.broadcast_state_change()
        status_lcd.lcd_display_string(lcd_status_text, 2)
