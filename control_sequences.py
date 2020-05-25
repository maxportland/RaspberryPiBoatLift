from lift_controls import LiftControls
from setting_constants import *
from lift_status import LiftStatus, status_lcd
from lift_state import *
import RPi.GPIO as GPIO
from time import sleep
import time, os, sys, sched, threading


class LiftSequences(object):
    @staticmethod
    def close_all_valves():
        LiftControls.close_master_valve()
        LiftControls.close_rear_valves()
        LiftControls.close_front_valves()

    @staticmethod
    def init_sequence():
        status_lcd.backlight(0)
        GPIO.add_event_detect(UP_BUTTON, GPIO.FALLING, callback=LiftSequences.up_button_callback, bouncetime=1000)
        GPIO.add_event_detect(DOWN_BUTTON, GPIO.FALLING, callback=LiftSequences.down_button_callback, bouncetime=1000)
        LiftControls.turn_off_blower()
        LiftSequences.close_all_valves()

    @staticmethod
    def lift_is_in_sequence():
        state_object = LiftStatus.get_state_object()
        return (state_object["lift_state"] == LiftState.LIFTING or
                state_object["lift_state"] == LiftState.LOWERING)

    @staticmethod
    def up_button_callback():
        state_object = LiftStatus.get_state_object()
        if state_object["lift_state"] != LiftState.UP and not LiftSequences.lift_is_in_sequence():
            LiftStatus.change_lift_state(LiftState.LIFTING)
            LiftSequences.lift_boat()

    @staticmethod
    def down_button_callback():
        state_object = LiftStatus.get_state_object()
        if state_object["lift_state"] != LiftState.DOWN and not LiftSequences.lift_is_in_sequence():
            LiftStatus.change_lift_state(LiftState.LOWERING)
            LiftSequences.lower_boat()

    @staticmethod
    def lower_sequence_started():
        status_lcd.backlight(1)
        LiftStatus.set_primary_status("--- LOWERING ---", "Lowering")

    @staticmethod
    def lower_sequence_ended():
        LiftStatus.change_lift_state(LiftState.DOWN)
        status_lcd.lcd_clear()
        LiftStatus.set_primary_status("-- BOAT  DOWN --", "Boat Down")
        LiftStatus.set_secondary_status("       :)       ", "")

    @staticmethod
    def lift_sequence_started():
        status_lcd.backlight(1)
        LiftStatus.set_primary_status("--- LIFTING ----", "Lifting")

    @staticmethod
    def lift_sequence_ended():
        LiftStatus.change_lift_state(LiftState.UP)
        status_lcd.lcd_clear()
        LiftStatus.set_primary_status("--- BOAT  UP ---", "Boat Up")
        LiftStatus.set_secondary_status("       :)       ", "")

    @staticmethod
    def lower_rear_pause():
        sleep(LOWER_REAR_WAIT)

    @staticmethod
    def lower_front_pause():
        sleep(LOWER_FRONT_WAIT)

    @staticmethod
    def lift_front_pause():
        sleep(LIFT_FRONT_WAIT)

    @staticmethod
    def lift_rear_pause():
        sleep(LIFT_REAR_WAIT)

    @staticmethod
    def lift_both_pause():
        sleep(LIFT_BOTH_WAIT)

    @staticmethod
    def lower_boat():
        sequence = (LiftSequences.turn_off_blower, LiftSequences.open_master_valve, LiftSequences.open_rear_valves,
                    LiftSequences.lower_rear_pause, LiftSequences.open_front_valves, LiftSequences.lower_front_pause)
        LiftSequences.lower_sequence_started()
        LiftSequences.run_sequence(sequence)
        LiftSequences.lower_sequence_ended()

    @staticmethod
    def lift_boat():
        sequence = (LiftSequences.close_master_valve, LiftSequences.open_front_valves, LiftSequences.turn_on_blower,
                    LiftSequences.lift_front_pause, LiftSequences.open_rear_valves, LiftSequences.lift_rear_pause,
                    LiftSequences.close_front_valves, LiftSequences.lift_both_pause, LiftSequences.close_rear_valves,
                    LiftSequences.turn_off_blower)
        LiftSequences.lift_sequence_started()
        LiftSequences.run_sequence(sequence)
        LiftSequences.lift_sequence_ended()

    @staticmethod
    def run_sequence(sequence):
        for sequence_function in sequence:
            state_object = LiftStatus.get_state_object()
            if state_object["lift_state"] == LiftState.ABORT:
                return
            sequence_function()

    @staticmethod
    def abort():
        LiftStatus.change_lift_state(LiftState.ABORT)
        LiftSequences.close_all_valves()
        LiftControls.turn_off_blower()
