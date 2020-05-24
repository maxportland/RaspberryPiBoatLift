from flask_endpoints import *


if __name__ == '__main__':
    init_sequence()
    socketio.run(app, debug=True, host="0.0.0.0", port="80")
