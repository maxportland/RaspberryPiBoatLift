import RPi_I2C_driver
from lift_state import LiftState, BlowerState, ValveState
from app import socketio
import json
import datetime
import logging


status_lcd = RPi_I2C_driver.lcd()
logging.basicConfig(filename='/home/pi/lift.log',
                    level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


state_object = {
    "updated": datetime.datetime.now().isoformat(),
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
        LiftStatus.broadcast_state_change()

    @staticmethod
    def broadcast_state_change():
        state_object['updated'] = datetime.datetime.now().isoformat()
        socketio.emit('state_change', json.dumps(state_object))

    @staticmethod
    def set_primary_status(lcd_status_text, status_text):
        LiftStatus.add_to_messages(status_text)
        status_lcd.lcd_display_string(lcd_status_text, 1)

    @staticmethod
    def set_secondary_status(lcd_status_text, status_text):
        LiftStatus.add_to_messages(status_text)
        status_lcd.lcd_display_string(lcd_status_text, 2)

    @staticmethod
    def add_to_messages(message):
        now = datetime.datetime.now()
        if len(state_object["messages"]) > 10:
            state_object["messages"].pop(0)
        logging.info(message)
        message_with_date = now.strftime("[ %X %b %m ] - ") + message
        state_object["messages"].append(message_with_date)
        LiftStatus.broadcast_state_change()
