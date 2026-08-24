#!/usr/bin/env python3
"""
half_hour_chime.py

Plays a sound file at the top of every hour and every half hour
(e.g. 1:00, 1:30, 2:00, 2:30, ...).

Usage:
    python half_hour_chime.py                 # looks for a sound file automatically
    python half_hour_chime.py mychime.wav      # use a specific sound file

Just drop this script in the same folder as your sound file and run it.
Supports .wav and .mp3 (via platform-native players — no extra installs needed).
Leave the terminal window open; it runs until you stop it with Ctrl+C.
"""

import sys
import time
import datetime
import subprocess
import platform
import glob
import os

SUPPORTED_EXTENSIONS = (".wav", ".mp3", ".aiff", ".m4a")


def find_sound_file():
    """Look in the current folder for a sound file if none was specified."""
    for ext in SUPPORTED_EXTENSIONS:
        matches = glob.glob(f"*{ext}")
        if matches:
            return matches[0]
    return None


def play_sound(path):
    system = platform.system()
    try:
        if system == "Darwin":  # macOS
            subprocess.run(["afplay", path], check=True)
        elif system == "Windows":
            import winsound
            # winsound.PlaySound only handles .wav natively
            if path.lower().endswith(".wav"):
                winsound.PlaySound(path, winsound.SND_FILENAME)
            else:
                # Fall back to the default OS player association
                os.startfile(path)  # noqa: this only exists on Windows
        else:  # Linux and others
            # Try a few common players in order
            for player in (["paplay"], ["aplay"], ["ffplay", "-nodisp", "-autoexit"]):
                try:
                    subprocess.run(player + [path], check=True,
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    return
                except (FileNotFoundError, subprocess.CalledProcessError):
                    continue
            print("Couldn't find a working audio player (tried paplay, aplay, ffplay).")
    except Exception as e:
        print(f"Error playing sound: {e}")


def seconds_until_next_half_hour():
    now = datetime.datetime.now()
    if now.minute < 30:
        target = now.replace(minute=30, second=0, microsecond=0)
    else:
        target = (now.replace(minute=0, second=0, microsecond=0)
                  + datetime.timedelta(hours=1))
    return (target - now).total_seconds(), target


def main():
    args = [a for a in sys.argv[1:] if a != "--test"]
    if args:
        sound_path = args[0]
        if not os.path.isfile(sound_path):
            print(f"Sound file not found: {sound_path}")
            sys.exit(1)
    else:
        sound_path = find_sound_file()
        if not sound_path:
            print("No sound file found in this folder.")
            print(f"Supported types: {', '.join(SUPPORTED_EXTENSIONS)}")
            print("Either place one here, or run: python half_hour_chime.py yourfile.wav")
            sys.exit(1)
    
    
    print(f"Using sound file: {sound_path}")
    print("Chiming every :00 and :30. Press Ctrl+C to stop.\n")
    if "--test" in sys.argv:
        play_sound(sound_path)
        
    try:
        while True:
            wait_seconds, target_time = seconds_until_next_half_hour()
            print(f"Next chime at {target_time.strftime('%I:%M %p')} "
                  f"(in {int(wait_seconds // 60)} min {int(wait_seconds % 60)} sec)")
            time.sleep(max(wait_seconds, 0))
            print(f"[{datetime.datetime.now().strftime('%I:%M:%S %p')}] Chime!")
            play_sound(sound_path)
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()