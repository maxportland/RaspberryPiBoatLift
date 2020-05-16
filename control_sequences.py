import lift_status
from lift_controls import *
import RPi.GPIO as GPIO


def close_all_valves():
    close_master_valve()
    close_rear_valves()
    close_front_valves()


def init_sequence():
    status_lcd.backlight(0)
    GPIO.add_event_detect(UP_BUTTON, GPIO.FALLING, callback=up_button_callback, bouncetime=1000)
    GPIO.add_event_detect(DOWN_BUTTON, GPIO.FALLING, callback=down_button_callback, bouncetime=1000)
    turn_off_blower()
    close_all_valves()


def lift_is_in_sequence():
    return (lift_status.state_object["lift_state"] == LiftState.LIFTING or
            lift_status.state_object["lift_state"] == LiftState.LOWERING)


def up_button_callback():
    if lift_is_in_sequence():
        abort()
    elif lift_status.state_object["lift_state"] != LiftState.UP:
        lift_boat()


def down_button_callback():
    if lift_is_in_sequence():
        abort()
    elif lift_status.state_object["lift_state"] != LiftState.DOWN:
        lower_boat()


def lower_sequence_started():
    lift_status.state_object["lift_state"] = LiftState.LOWERING
    status_lcd.backlight(1)
    set_primary_status("--- LOWERING ---")


def lower_sequence_ended():
    lift_status.state_object["lift_state"] = LiftState.DOWN
    status_lcd.lcd_clear()
    set_primary_status("-- BOAT  DOWN --")
    set_secondary_status("       :)       ")


def lift_sequence_started():
    lift_status.state_object["lift_state"] = LiftState.LIFTING
    status_lcd.backlight(1)
    set_primary_status("--- LIFTING ----")


def lift_sequence_ended():
    lift_status.state_object["lift_state"] = LiftState.UP
    status_lcd.lcd_clear()
    set_primary_status("--- BOAT  UP ---")
    set_secondary_status("       :)       ")


def lower_rear_pause():
    sleep(LOWER_REAR_WAIT)


def lower_front_pause():
    sleep(LOWER_FRONT_WAIT)


def lift_front_pause():
    sleep(LIFT_FRONT_WAIT)


def lift_rear_pause():
    sleep(LIFT_REAR_WAIT)


def lift_both_pause():
    sleep(LIFT_BOTH_WAIT)


def lower_boat():
    sequence = (turn_off_blower, open_master_valve, open_rear_valves,
                lower_rear_pause, open_front_valves, lower_front_pause())
    lower_sequence_started()
    run_sequence(sequence)
    lower_sequence_ended()


def lift_boat():
    sequence = (close_master_valve, open_front_valves, turn_on_blower, lift_front_pause, open_rear_valves,
                lift_rear_pause, close_front_valves, lift_both_pause, close_rear_valves, turn_off_blower)
    lift_sequence_started()
    run_sequence(sequence)
    lift_sequence_ended()


def run_sequence(sequence):
    for sequence_function in sequence:
        if lift_status.state_object["lift_state"] == LiftState.ABORT:
            return
        sequence_function()


def abort():
    lift_status.state_object["lift_state"] = LiftState.ABORT
    close_rear_valves()
    close_rear_valves()
    close_master_valve()
    turn_off_blower()
