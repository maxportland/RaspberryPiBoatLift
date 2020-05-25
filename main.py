from flask_endpoints import *
from control_sequences import LiftSequences


if __name__ == '__main__':
    LiftSequences.init_sequence()
    socketio.run(app, debug=True, host="0.0.0.0", port="80")
