import pygame
import mido
import time

# === CONFIGURATIONS ===
MIDI_CHANNEL = 0  # MIDI channel (0-15)
CC_LX = 16         # Left Stick X-axis → Modulation
CC_LY = 1        # Left Stick Y-axis → Generic
CC_RX = 17        # Right Stick X-axis → Expression
CC_RY = 11        # Right Stick Y-axis → Generic
CC_LTR = 18       # Left Trigger → Custom
CC_RTR = 19       # Right Trigger → Custom
BUTTON_NOTE_MAP = {0: 60, 1: 62, 2: 64, 3: 65}  # A, B, X, Y → MIDI Notes

DEAD_ZONE = 0.1   # Ignore small movements
MIDI_UPDATE_RATE = 0.01  # 10ms refresh rate (limits CPU usage)
SENSITIVITY = 1  # Sensitivity of the Joystick

class GamepadToMidiController:
    def __init__(self):
        self.joysticks = []
        self.midi_out = None
        self.button_states = {}
        self.previous_values = {
            "lx": 0, "ly": 0,
            "rx": 0, "ry": 0,
            "ltr": 0, "rtr": 0
        }
        # Initialize Pygame
        pygame.init()
        pygame.joystick.init()

        # Find and initialize all connected joysticks
        self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        for j in self.joysticks:
            j.init()

        if not self.joysticks:
            print("No gamepad detected! Connect one and restart.\n")
            exit()

        # Initialize MIDI output
        self.midi_out = self.select_midi_port(auto_select=False)
        print(f"Connected to MIDI {self.midi_out}\n")

    def select_midi_port(self, auto_select=True):
        """Select MIDI output port (auto or manual)."""
        midi_ports = mido.get_output_names()

        if not midi_ports:
            print("No MIDI ports found! Start a virtual MIDI port (e.g., LoopBe1) and restart.\n")
            exit()

        if auto_select:
            print(f"Auto selecting MIDI port: {midi_ports[0]}\n")
            return mido.open_output(midi_ports[0])
        else:
            print("\nAvailable MIDI ports:\n")
            for i, port in enumerate(midi_ports):
                print(f"{i}: {port}")

            while True:
                try:
                    selection = int(input("\nEnter the port number you want to use: "))
                    if 0 <= selection < len(midi_ports):
                        print(f"Selected MIDI port: {midi_ports[selection]}")
                        return mido.open_output(midi_ports[selection])
                    else:
                        print("Invalid selection, please try again.\n")
                except ValueError:
                    print("Invalid input. Please enter a valid number.\n")
                    
# === MAIN FUNCTIONS ===
        """Send a MIDI CC message."""
    def send_midi_cc(self, controller, value):
        self.midi_out.send(mido.Message('control_change', channel=MIDI_CHANNEL, control=controller, value=value))
        
        """Send a MIDI Note On message."""
    def send_midi_note_on(self, note):
        self.midi_out.send(mido.Message('note_on', channel=MIDI_CHANNEL, note=note, velocity=127))
        
        """Send a MIDI Note Off message."""
    def send_midi_note_off(self, note):
        self.midi_out.send(mido.Message('note_off', channel=MIDI_CHANNEL, note=note, velocity=0))

        """Convert joystick analog (-1 to 1) to MIDI range (0-127)."""
    def analog_to_midi(self, value):
        return int((((value) + 1) / 2) * 127)

        """Convert trigger input (0 to 1) to MIDI range (0-127)."""
    def trigger_to_midi(self, value):
        return int(value * 127)

        """Prompt the user to adjust the joystick sensitivity."""
    def adjust_joystick_sensitivity(self):
        global SENSITIVITY
        try:
            new_sensitivity = float(input("Enter new joystick sensitivity (0 to 1): "))
            if 0 <= new_sensitivity <= 1:
                SENSITIVITY = new_sensitivity
                print(f"Joystick sensitivity adjusted to {SENSITIVITY}")
                self.process_input()
            else:
                print("Please enter a value between 0 and 1.")
                self.adjust_joystick_sensitivity()
        except ValueError:
            print("Invalid input, please enter a number between 0 and 1.")



# === MAIN LOOP ===
        """Process gamepad input and send MIDI messages."""
    def process_input(self):

        for joystick in self.joysticks:
            # Read Left Stick values
            lx = joystick.get_axis(0)  * SENSITIVITY
            ly = -joystick.get_axis(1) * SENSITIVITY

            # Read Right Stick values
            rx = joystick.get_axis(2) * SENSITIVITY
            ry = -joystick.get_axis(3)* SENSITIVITY

            # Read trigger values
            ltr = joystick.get_axis(4)
            rtr = joystick.get_axis(5)

            # Apply dead zone filtering
            lx = 0 if abs(lx) < DEAD_ZONE else lx
            ly = 0 if abs(ly) < DEAD_ZONE else ly
            rx = 0 if abs(rx) < DEAD_ZONE else rx
            ry = 0 if abs(ry) < DEAD_ZONE else ry

            # Normalize trigger values
            ltr = (ltr + 1) / 2
            rtr = (rtr + 1) / 2 

            # Handle button presses for MIDI notes
            for button, note in BUTTON_NOTE_MAP.items():
                is_pressed = joystick.get_button(button)

                if is_pressed and self.button_states.get(button) != is_pressed:
                    self.send_midi_note_on(note)
                    input_detected = True
                    print(f"Button {button} pressed (Note {note})")
                elif not is_pressed and self.button_states.get(button) != is_pressed:
                    self.send_midi_note_off(note)
                    input_detected = True
                    print(f"Button {button} released (Note {note})")

                self.button_states[button] = is_pressed

            # Handle analog sticks and triggers only if there's a meaningful change
            if abs(lx - self.previous_values["lx"]) > DEAD_ZONE or abs(ly - self.previous_values["ly"]) > DEAD_ZONE:
                input_detected = True
                self.send_midi_cc(CC_LX, self.analog_to_midi(lx))
                self.send_midi_cc(CC_LY, self.analog_to_midi(ly))
                print(f"Left Stick: X={lx:.2f}, Y={ly:.2f}")
                self.previous_values["lx"], self.previous_values["ly"] = lx, ly

            if abs(rx - self.previous_values["rx"]) > DEAD_ZONE or abs(ry - self.previous_values["ry"]) > DEAD_ZONE:
                input_detected = True
                self.send_midi_cc(CC_RX, self.analog_to_midi(rx))
                self.send_midi_cc(CC_RY, self.analog_to_midi(ry))
                print(f"Right Stick: X={rx:.2f}, Y={ry:.2f}")
                self.previous_values["rx"], self.previous_values["ry"] = rx, ry

            if abs(ltr - self.previous_values["ltr"]) > DEAD_ZONE or abs(rtr - self.previous_values["rtr"]) > DEAD_ZONE:
                input_detected = True
                self.send_midi_cc(CC_LTR, self.trigger_to_midi(ltr))
                self.send_midi_cc(CC_RTR, self.trigger_to_midi(rtr))    
                print(f"Triggers: LT={ltr:.2f}, RT={rtr:.2f}")
                self.previous_values["ltr"], self.previous_values["rtr"] = ltr, rtr

           # Check if the Start button (typically button 7) is pressed to adjust sensitivity
            if joystick.get_button(7):  # Start button usually maps to button 7
                return False

        return True

        """Run the gamepad to MIDI controller logic."""
    def run(self):
        print("\nGamepad to MIDI Controller Running...\n")
        print("Press 'start' to adjust joystick sensitivity at any time..")

        try:
            while True:
                pygame.event.pump()
                if not self.process_input():
                    self.adjust_joystick_sensitivity()
                self.process_input()
                time.sleep(MIDI_UPDATE_RATE)

        except KeyboardInterrupt:
            print("\nExiting...")

        finally:
            pygame.quit()
            self.midi_out.close()

