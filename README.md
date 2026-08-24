# Time-Chime
Time Chime, chimes on time.  Sounds a file of your choosing every half hour.

## License
This project is licensed under the [PolyForm Noncommercial License 1.0.0](LICENSE). Free for personal and non-commercial use. Commercial use is strictly prohibited.

## Description
Simple script to run a chime at the top of the hour and every half hour, add your wav, mp3, aiff, or m4a file to the same folder and run the script in a terminal.  Tested on Windows but should work on MacOS and Linux.

## Prerequisites
Python must be installed.

## Usage
Run this command in terminal.  
python half_hour_chime.py

To run with a specific file:
python half_hour_chime.py mychime.wav

To test playback immediately with file in folder or your specific file run with argument --test

Example: python half_hour_chime.py mychime.wav --test

Terminal must stay open to continue to run.  ctrl+c to stop or kill the terminal.
