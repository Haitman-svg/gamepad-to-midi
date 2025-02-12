# === CONFIGURATIONS ===
MIDI_CHANNEL = 0  # MIDI channel (0-15)

# MIDI Control Change (CC) mappings
CC_LX = 1         # Left Stick X-axis → Modulation
CC_LY = 16        # Left Stick Y-axis → Generic
CC_RX = 17        # Right Stick X-axis → Expression
CC_RY = 11        # Right Stick Y-axis → Generic
CC_LTR = 18       # Left Trigger → Custom
CC_RTR = 19       # Right Trigger → Custom

# Button-to-MIDI mapping (Gamepad buttons to MIDI Notes)
BUTTON_NOTE_MAP = {0: 60, 1: 62, 2: 64, 3: 65}  # A, B, X, Y → MIDI Notes

# Joystick deadzone (small movements are ignored)
DEAD_ZONE = 0.1

# MIDI update rate (10ms refresh rate to limit CPU usage)
MIDI_UPDATE_RATE = 0.01

# Joystick sensitivity (adjustable at runtime)
SENSITIVITY = 0.7

# Maximum inactivity duration (in seconds) to stop sending MIDI signals
INACTIVITY_TIMEOUT = 3
