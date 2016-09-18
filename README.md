###About
----

Pyano is a free and open-source virtual MIDI controller program which allows you to use your keyboard (as in QWERTY keyboard) as a keyboard instrument (as in pianos, harpsichords, organs).

Born of a need for an instrument to play while away from home, the Pyano project hopes to allow musicians to express themselves with nothing more than a computer or laptop, and optionally many external USB keyboards. 

###How It Works
----

Pyano focuses on the front-end of things; which is to say, it provides a user interface that captures keystroke events from the user's keyboard. Upon detecting a keypress, the program sends a MIDI signal to an external synthesizer program (such as Fluidsynth), which produces the sounds. On its own, Pyano does **not** make any sound.

###Getting Started
----

####Prerequisites

1. The latest version of Pyano (the one that supports multiple-keyboards as multiple instruments) can only be run on Linux, and has only been tested on Ubuntu 14.04, though other flavours of Linux should work.  
   Alternatively, there is an older version on a separate branch, version1, which should work on other operating systems out of the box (tested on Windows 8 and Windows 10).

2. Pyano is built on [Python 2.7](https://www.python.org/), the [Pygame library](http://www.pygame.org/hifi.html) and the [Python EvDev](https://python-evdev.readthedocs.org/en/latest/) library, so you need to have these installed on your computer.

3. You also need to install a real-time software synthesizer which supports MIDI input. ([Fluidsynth](http://www.fluidsynth.org/) has been tested and is recommended)

####Setup

1. Clone the latest build of Pyano from the Github [page](https://github.com/JunShern/Pyano).

2. Run the software synthesizer, make sure it is working and ready to accept MIDI input. Don't forget to pick a SoundFont file on your synthesizer! (FluidR3\_GM.sf2 has been tested and is great)

3. Execute main.py in administrator mode (this is necessary for the software to be able to recognize different keyboard devices).

4. You should see a list of available output devices, choose the one which corresponds to your software synthesizer. 

5. Make some music! 

###Screenshots
----

Current version, shows multiple keyboards and status lines for each keyboard:

![multikey](https://raw.githubusercontent.com/JunShern/Pyano/master/img/multikey.png?raw=true "multikey")

Older, Windows-compatible version (in branch version1), showing keyboard layout:  

![version1](https://raw.githubusercontent.com/JunShern/Pyano/master/img/version1.png?raw=true "version1")


###Instructions
----

* **Volume** control UP/DOWN using HOME/END buttons  
  * Note that HOME/END only controls volume for your current keyboard; if you'd like to change global volume, use your mouse to manually change the volume settings on your system tray

* **Velocity** control UP/DOWN using SHIFT+HOME/END  

* Use the SPACEBAR as a **sustain** pedal  
  * SHIFT+SPACE toggles sharing of sustain between multiple keyboards.

* **Transpose** your instrument using the arrow keys  
  * Use the UP/DOWN arrow keys to shift all active keyboards (except percussion) by one semitone.  
  * Use SHIFT+UP (or DOWN) to shift only your current instrument by one semitone.  
  >(Pro tip: Hit it twice for that chorus, nobody likes a one-semitone key change)  

  * Want to go higher but reached the top of your keyboard? Just hit the RIGHT (or LEFT) arrow key to shift your instrument by an octave.

* **Change instruments** using PAGEUP and PAGEDOWN  
  * The instrument sound you get will depend on your software synthesizer and the SoundFont you have chosen. For example, FluidGM2.SF has over 100 instruments and sounds you can use. 
  * Percussion instruments are a special case; see point "Percussion instruments" below.

* **Save up to 9 settings** in the program's sound bank  
  * Use CTRL+SHIFT+F# or CTRL+SHIFT+KP# where # is the sound bank number you want to save it to.

* Quickly **load up saved settings** to jump between your favourite instruments  
  * Just hit F# or KP# where # is the sound bank number you want to load from.

* Access **percussion instruments** using F10 or KP0
  * Jump back to non-percussion instruments using any other F# or KP# keys.

* Use multiple keyboards for **multiple instruments**!  
  * Plug in an extra USB keyboard before you run Pyano; you'll be able to control each keyboard individually as a different instrument. Handy for getting more octaves in range! 
  * Be careful though, Pyano doesn't support plugging/unplugging while running, so don't unplug your keyboards after Pyano has started up.

###Similar projects
----

* [Virtual MIDI Piano Keyboard (VMPK)](http://vmpk.sourceforge.net/)
