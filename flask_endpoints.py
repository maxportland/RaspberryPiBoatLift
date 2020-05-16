from flask import Flask, render_template
import json
from control_sequences import *
from lift_status import *

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/status", methods=['GET'])
def web_status_callback():
    return json.dumps(state_object)


@app.route("/down", methods=['POST'])
def web_down_button_callback():
    down_button_callback()
    return json.dumps(state_object)


@app.route("/up", methods=['POST'])
def web_up_button_callback():
    up_button_callback()
    return json.dumps(state_object)


@app.route("/frontValvesOpen", methods=['POST'])
def web_open_front_valves():
    open_front_valves()
    return json.dumps(state_object)


@app.route("/frontValvesClose", methods=['POST'])
def web_close_front_valves():
    close_front_valves()
    return json.dumps(state_object)


@app.route("/rearValvesOpen", methods=['POST'])
def web_open_rear_valves():
    open_rear_valves()
    return json.dumps(state_object)


@app.route("/rearValvesClose", methods=['POST'])
def web_close_rear_valves():
    close_rear_valves()
    return json.dumps(state_object)


@app.route("/masterValveOpen", methods=['POST'])
def web_open_master_valve():
    open_master_valve()
    return json.dumps(state_object)


@app.route("/masterValveClose", methods=['POST'])
def web_close_master_valve():
    close_master_valve()
    return json.dumps(state_object)


@app.route("/blowerOn", methods=['POST'])
def web_turn_on_blower():
    turn_on_blower()
    return json.dumps(state_object)


@app.route("/blowerOff", methods=['POST'])
def web_turn_off_blower():
    turn_off_blower()
    return json.dumps(state_object)
