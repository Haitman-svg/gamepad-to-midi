# Gamepad to MIDI Converter

This project allows you to convert gamepad inputs (analog sticks, triggers, and buttons) into MIDI signals.

## Why This Project?

The reason I created this app is because many existing gamepad-to-MIDI solutions are outdated or no longer maintained. I wanted a more responsive customizable solution for myself.

## Features

- **Real-Time MIDI Control:** Convert analog stick and trigger movements to MIDI Control Change (CC) messages.
- **Button-to-MIDI Mapping:** Map gamepad buttons to MIDI notes (e.g., A, B, X, Y buttons).
- **Customizable Sensitivity:** Adjust joystick sensitivity dynamically.
- **Auto MIDI Port Detection:** Automatically detects and selects the connected MIDI device.

## Requirements
- **Virtual MIDI Port:** You will need a virtual MIDI driver (e.g., LoopBe1 or LoopMidi) to route MIDI data from the app to your DAW or MIDI software.
- **Python Dependencies:** The requirement file automatically includes dependencies for Pygame and Mido.

## Installation

1. **Install Python** (if not already installed) from the official website: [https://www.python.org/downloads/](https://www.python.org/downloads/).
2. **Clone this repository**:
   ```bash
   git clone https://github.com/Krocosr/gamepad-to-midi.git
	```

## Running the App

1. **Navigate to the project folder** in your terminal or command prompt.
2. **Run the .bat file:**
   - On Windows: Double-click the `Run.bat` file.
3. The application will start, and the gamepad will be mapped to MIDI controls. You can adjust the joystick sensitivity by pressing the **Start** button on your gamepad at any time.

## Configuration

You can configure the following settings:

- **Joystick Sensitivity:** Adjust the sensitivity of the analog sticks and triggers. Default is set to `0.7`.
- **Button Mapping:** The buttons on the gamepad are mapped to MIDI notes (A, B, X, Y). You can adjust this mapping in the code if needed.
- **Dead Zone:** The dead zone is set to `0.1` by default to ignore small joystick movements. This can also be adjusted in the config file.

## Contributing

Feel free to fork this repository and make improvements! Contributions are always welcome.