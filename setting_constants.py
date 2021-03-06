SMALL_VALVE_TIMING = 4
LARGE_VALVE_TIMING = 5

LOWER_REAR_WAIT = 96
LOWER_FRONT_WAIT = 158

LIFT_FRONT_WAIT = 32
LIFT_REAR_WAIT = 30
LIFT_BOTH_WAIT = 85

BLOWER = 4
MASTER_VALVE = 5

# Rear
REAR_VALVE_POWER = 19
REAR_LEFT_VALVE = 6
REAR_RIGHT_VALVE = 12
REAR_VALVES = [REAR_LEFT_VALVE, REAR_RIGHT_VALVE]

# Front
FRONT_VALVE_POWER = 20
FRONT_LEFT_VALVE = 13
FRONT_RIGHT_VALVE = 16
FRONT_VALVES = [FRONT_LEFT_VALVE, FRONT_RIGHT_VALVE]

# Buttons
UP_BUTTON = 18
DOWN_BUTTON = 17

# All
VALVE_POWER = [FRONT_VALVE_POWER, REAR_VALVE_POWER]
ALL_VALVES = FRONT_VALVES + REAR_VALVES
BUTTONS = [UP_BUTTON, DOWN_BUTTON]
