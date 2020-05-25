from flask import render_template
from lift_controls import LiftControls
from control_sequences import LiftSequences
from lift_status import *
from app import app
import threading


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/status", methods=['GET'])
def web_status_callback():
    return json.dumps(state_object)


@app.route("/down", methods=['POST'])
def web_down_button_callback():
    socketio.start_background_task(target=LiftSequences.down_button_callback)
    return json.dumps(state_object)


@app.route("/up", methods=['POST'])
def web_up_button_callback():
    socketio.start_background_task(target=LiftSequences.up_button_callback)
    return json.dumps(state_object)


@app.route("/frontValvesOpen", methods=['POST'])
def web_open_front_valves():
    print("web_open_front_valves")
    socketio.start_background_task(target=LiftControls.open_front_valves)
    return json.dumps(state_object)


@app.route("/frontValvesClose", methods=['POST'])
def web_close_front_valves():
    socketio.start_background_task(target=LiftControls.close_front_valves)
    return json.dumps(state_object)


@app.route("/rearValvesOpen", methods=['POST'])
def web_open_rear_valves():
    socketio.start_background_task(target=LiftControls.open_rear_valves)
    return json.dumps(state_object)


@app.route("/rearValvesClose", methods=['POST'])
def web_close_rear_valves():
    socketio.start_background_task(target=LiftControls.close_rear_valves)
    return json.dumps(state_object)


@app.route("/masterValveOpen", methods=['POST'])
def web_open_master_valve():
    socketio.start_background_task(target=LiftControls.open_master_valve)
    return json.dumps(state_object)


@app.route("/masterValveClose", methods=['POST'])
def web_close_master_valve():
    socketio.start_background_task(target=LiftControls.close_master_valve)
    return json.dumps(state_object)


@app.route("/blowerOn", methods=['POST'])
def web_turn_on_blower():
    socketio.start_background_task(target=LiftControls.turn_on_blower)
    return json.dumps(state_object)


@app.route("/blowerOff", methods=['POST'])
def web_turn_off_blower():
    socketio.start_background_task(target=LiftControls.turn_off_blower)
    return json.dumps(state_object)


@app.route("/abort", methods=['GET'])
def web_abort():
    socketio.start_background_task(target=LiftSequences.abort)
    return json.dumps(state_object)
