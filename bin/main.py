import subprocess
import sys
from pad2midi import GamepadToMidiController


def install_requirements():
    try:
        import pygame
        import mido
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def main():
    install_requirements()
    app = GamepadToMidiController()
    app.run()
    print("\n========= Running Gamepad To MIDI Converter =========")

if __name__ == "__main__":
    main()




