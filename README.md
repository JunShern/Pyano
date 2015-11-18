About
Pyano is a free and open-source MIDI program which allows you to use your keyboard (as in QWERTY keyboard) as a keyboard instrument (as in pianos, harpsichords, organs).

Born of a need for an instrument to play while away from home, the Pyano project hopes to allow musicians to express themselves with nothing more than a computer or laptop, and optionally many external USB keyboards. 

How It Works
Pyano focuses on the front-end of things; which is to say, it provides a user interface that captures keystroke events from the user's keyboard. Upon detecting a keypress, the program sends a MIDI signal to an external synthesizer program (such as Fluidsynth), which produces the sounds. On its own, Pyano does not make any sound.

Getting Started
Prerequisites
1. The latest version of Pyano (the one that supports multiple-keyboards as multiple instruments) can only be run on Linux, and has only been tested on Ubuntu 14.04, though other flavours of Linux should work.
2. Pyano is built on Python 2.7, the Pygame library and the Python EvDev library, so you need to have these installed on your computer.
3. You also need to install a real-time software synthesizer which supports MIDI input. (Fluidsynth has been tested and is recommended)

Setup
1. Clone the latest build of Pyano from the Github page.
2. Run the software synthesizer, make sure it is working and ready to accept MIDI input. Don't forget to pick a SoundFont file for 
3. Execute main.py in administrator mode (this is necessary for the software to be able to recognize different keyboard devices).
4. You should see a list of available output devices, choose the one which corresponds to your software synthesizer. 
5. Make some music! 

Features
- Use the SPACEBAR as a sustain pedal.
SHIFT+SPACE toggles sharing of sustain between multiple keyboards.
- Transpose your instrument using the arrow keys! 
Want to hit that key change chorus but don't remember the key signature for the new key? Just hit the UP (or DOWN) arrow key to shift your entire instrument by one semitone. (Pro tip: Hit it twice for that chorus, nobody likes a one-semitone key change)
Want to go higher but reached the top of your keyboard? Just hit the RIGHT (or LEFT) arrow key to shift your instrument by an octave.
- Volume control using HOME/END buttons.
- Velocity control using SHIFT+HOME/END.
- Change instruments using PAGEUP and PAGEDOWN.
The instrument sound you get will depend on your software synthesizer and the SoundFont you have chosen. For example, FluidGM2.SF has over 100 instruments and sounds you can use. 
- Save up to 9 settings in the program's sound bank.
Use SHIFT+F# or SHIFT+KP# where # is the sound bank number you want to save it to.
- Quickly load up saved settings to jump between your favourite instruments.
Just hit F# or KP# where # is the sound bank number you want to load from.

Similar projects include:
- Virtual MIDI Piano Keyboard (VMPK) http://vmpk.sourceforge.net/
