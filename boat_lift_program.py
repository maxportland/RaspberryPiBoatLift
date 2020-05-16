from control_sequences import init_sequence
from flask_endpoints import app


def main():
    app.run(debug=True, threaded=True, host="0.0.0.0", port="80")


if __name__ == '__main__':
    init_sequence()
    main()
